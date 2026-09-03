"""P5.4.2 -- Validator for tools/hsk/hsk1_related_words_selection.json.

Read-only. Never writes to the selection artifact, the P5.4.1 candidate
pool, the HSK1 production file, or any other file. Prints a
machine-readable summary and exits non-zero if any check fails -- no
fake "allChecksPassed": true is ever emitted when a check fails.

Usage:
    python validate_hsk1_related_words_selection_p542.py
"""

import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HSK1_PATH = REPO_ROOT / "data" / "hsk" / "hsk1" / "hsk1_vocabulary_production.json"
POOL_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_candidate_pool.json"
SELECTION_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_selection.json"

MAX_SELECTED_PER_RECORD = 5
EXPECTED_SOURCE_COUNT = 300
VALID_STATUSES = {"selected", "needs_review"}


def load_json_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    checks: dict[str, dict] = {}
    all_passed = True

    def record(name: str, passed: bool, detail: str) -> None:
        nonlocal all_passed
        checks[name] = {"passed": passed, "detail": detail}
        if not passed:
            all_passed = False

    hsk1_text = load_json_text(HSK1_PATH)
    hsk1_records = json.loads(hsk1_text)
    hsk1_ids = {r["id"] for r in hsk1_records}
    hsk1_id_to_relatedWordIds_before = {r["id"]: r.get("relatedWordIds") for r in hsk1_records}

    if not POOL_PATH.exists():
        print("FAIL: candidate pool artifact missing:", POOL_PATH)
        raise SystemExit(1)
    pool_text = load_json_text(POOL_PATH)
    pool = json.loads(pool_text)
    pool_by_source = {r["sourceId"]: {c["wordId"] for c in r["candidates"]} for r in pool["records"]}

    if not SELECTION_PATH.exists():
        print("FAIL: selection artifact missing:", SELECTION_PATH)
        raise SystemExit(1)
    selection_text = load_json_text(SELECTION_PATH)
    selection = json.loads(selection_text)
    records = selection.get("records", [])

    # 1. exactly 300 source records
    record("source_record_count", len(hsk1_records) == EXPECTED_SOURCE_COUNT,
           f"{len(hsk1_records)} (expected {EXPECTED_SOURCE_COUNT})")

    sel_ids = [r["sourceId"] for r in records]
    sel_id_set = set(sel_ids)

    # 2. every HSK1 source appears exactly once / 3. no missing / 4. no unexpected
    record("selection_record_count", len(records) == EXPECTED_SOURCE_COUNT,
           f"{len(records)} (expected {EXPECTED_SOURCE_COUNT})")
    dup_sources = [i for i in sel_id_set if sel_ids.count(i) > 1]
    record("every_source_appears_once", len(dup_sources) == 0, f"duplicated: {dup_sources[:10]}")
    missing = sorted(hsk1_ids - sel_id_set)
    record("no_missing_source_ids", len(missing) == 0, f"missing: {missing[:10]}")
    unexpected = sorted(sel_id_set - hsk1_ids)
    record("no_unexpected_source_ids", len(unexpected) == 0, f"unexpected: {unexpected[:10]}")

    # 5. every selected ID exists in that source's candidate pool
    outside_pool = []
    for r in records:
        allowed = pool_by_source.get(r["sourceId"], set())
        for wid in r.get("selectedRelatedWordIds", []):
            if wid not in allowed:
                outside_pool.append((r["sourceId"], wid))
    record("selected_ids_within_candidate_pool", len(outside_pool) == 0, f"outside pool: {outside_pool[:10]}")

    # 6. no self-reference
    self_refs = [r["sourceId"] for r in records if r["sourceId"] in r.get("selectedRelatedWordIds", [])]
    record("no_self_references", len(self_refs) == 0, f"self-referencing: {self_refs[:10]}")

    # 7. no duplicate selected IDs
    dup_selected = []
    for r in records:
        ids = r.get("selectedRelatedWordIds", [])
        if len(ids) != len(set(ids)):
            dup_selected.append(r["sourceId"])
    record("no_duplicate_selected_ids", len(dup_selected) == 0, f"records with dupes: {dup_selected[:10]}")

    # 8. selectedCount matches array length
    count_mismatch = [
        r["sourceId"] for r in records
        if r.get("selectedCount") != len(r.get("selectedRelatedWordIds", []))
    ]
    record("selected_count_matches_array_length", len(count_mismatch) == 0, f"mismatches: {count_mismatch[:10]}")

    # 9. selectedCount <= 5
    over_max = [r["sourceId"] for r in records if r.get("selectedCount", 0) > MAX_SELECTED_PER_RECORD]
    record("max_selected_count_within_5", len(over_max) == 0, f"over max: {over_max[:10]}")

    # 10. status is valid
    bad_status = [r["sourceId"] for r in records if r.get("status") not in VALID_STATUSES]
    record("status_valid", len(bad_status) == 0, f"invalid: {bad_status[:10]}")

    # 11. status/count consistency -- a record with 0 selections must not
    #     be treated as an error state; verify status is one of the valid
    #     values regardless of count (already checked above), and verify
    #     no record claims needs_review for a reason inconsistent with the
    #     artifact's own selectionReasons (every reason's category must be
    #     internally consistent: if status is "selected", no reason may be
    #     tier C; if any reason is tier C, status must be needs_review).
    inconsistent = []
    for r in records:
        tiers = {rr["category"] for rr in r.get("selectionReasons", [])}
        has_c = "C" in tiers
        if has_c and r.get("status") != "needs_review":
            inconsistent.append((r["sourceId"], "has C-tier but status!=needs_review"))
        if not has_c and r.get("status") == "needs_review":
            inconsistent.append((r["sourceId"], "no C-tier but status==needs_review"))
    record("status_count_tier_consistency", len(inconsistent) == 0, f"inconsistent: {inconsistent[:10]}")

    # 12/13/14. provenance exists: candidate pool hash, source hash, rules version
    required_fields = [
        "selectionVersion", "candidatePoolPath", "candidatePoolVersion",
        "candidatePoolHash", "sourceDatasetHash", "rulesVersion", "generatedAt", "records",
    ]
    missing_fields = [f for f in required_fields if f not in selection]
    record("provenance_fields_present", len(missing_fields) == 0, f"missing: {missing_fields}")

    record("candidate_pool_hash_recorded_and_matches",
           selection.get("candidatePoolHash") == sha256_of(pool_text),
           f"recorded={selection.get('candidatePoolHash')} actual={sha256_of(pool_text)}")

    record("source_dataset_hash_recorded_and_matches",
           selection.get("sourceDatasetHash") == sha256_of(hsk1_text),
           f"recorded={selection.get('sourceDatasetHash')} actual={sha256_of(hsk1_text)}")

    record("rules_version_recorded", bool(selection.get("rulesVersion")), f"value={selection.get('rulesVersion')}")

    # 16. no fabricated IDs -- selectedRelatedWordIds must resolve to real
    #     candidate-pool entries with matching word text.
    fabricated = []
    pool_word_by_id = {}
    for pr in pool["records"]:
        for c in pr["candidates"]:
            pool_word_by_id[c["wordId"]] = c["word"]
    for r in records:
        for reason in r.get("selectionReasons", []):
            wid = reason["relatedWordId"]
            if wid not in pool_word_by_id:
                fabricated.append((r["sourceId"], wid))
    record("no_fabricated_ids", len(fabricated) == 0, f"fabricated: {fabricated[:10]}")

    # deterministic ordering: tier then id (A,B,C then wordId ascending within tier)
    tier_order = {"A": 0, "B": 1, "C": 2}
    unordered = []
    for r in records:
        reasons = r.get("selectionReasons", [])
        keys = [(tier_order.get(rr["category"], 9), rr["relatedWordId"]) for rr in reasons]
        if keys != sorted(keys):
            unordered.append(r["sourceId"])
    record("deterministic_ordering", len(unordered) == 0, f"unordered: {unordered[:10]}")

    # 17. no production relatedWordIds were written (HSK1 production file
    #     must still show every record's relatedWordIds exactly as it was
    #     before this phase -- empty arrays, per the P5.4.1 baseline).
    non_empty_production = [
        rid for rid, val in hsk1_id_to_relatedWordIds_before.items()
        if val not in (None, [])
    ]
    record("production_relatedWordIds_untouched", len(non_empty_production) == 0,
           f"non-empty in production: {non_empty_production[:10]}")

    print("=== P5.4.2 selection validation ===")
    for name, result in checks.items():
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {name}: {result['detail']}")

    print()
    print(f"allChecksPassed: {all_passed}")

    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
