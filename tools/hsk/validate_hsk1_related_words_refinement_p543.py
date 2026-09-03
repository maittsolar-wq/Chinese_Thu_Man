"""P5.4.3 -- Validator for tools/hsk/hsk1_related_words_refined_selection.json.

Read-only. Never writes to the refined artifact, the refinement report,
the P5.4.2 selection, the P5.4.1 candidate pool, or any production file.
Exits non-zero if any check fails -- no fake PASS is ever emitted.

Usage:
    python validate_hsk1_related_words_refinement_p543.py
"""

import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HSK1_PATH = REPO_ROOT / "data" / "hsk" / "hsk1" / "hsk1_vocabulary_production.json"
POOL_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_candidate_pool.json"
SELECTION_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_selection.json"
REFINED_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_refined_selection.json"
REPORT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_refinement_report.json"

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
    hsk1_relatedWordIds_before = {r["id"]: r.get("relatedWordIds") for r in hsk1_records}

    for p, label in [(POOL_PATH, "candidate pool"), (SELECTION_PATH, "P5.4.2 selection"),
                      (REFINED_PATH, "refined artifact"), (REPORT_PATH, "refinement report")]:
        if not p.exists():
            print(f"FAIL: {label} missing: {p}")
            raise SystemExit(1)

    pool_text = load_json_text(POOL_PATH)
    pool = json.loads(pool_text)
    pool_candidate_ids = {r["sourceId"]: {c["wordId"] for c in r["candidates"]} for r in pool["records"]}

    selection_text = load_json_text(SELECTION_PATH)
    selection = json.loads(selection_text)
    selection_ids_by_source = {r["sourceId"]: set(r["selectedRelatedWordIds"]) for r in selection["records"]}

    refined_text = load_json_text(REFINED_PATH)
    refined = json.loads(refined_text)
    records = refined.get("records", [])

    report = json.loads(load_json_text(REPORT_PATH))

    # 1. exactly 300 source records
    record("source_record_count", len(hsk1_records) == EXPECTED_SOURCE_COUNT,
           f"{len(hsk1_records)} (expected {EXPECTED_SOURCE_COUNT})")
    record("refined_record_count", len(records) == EXPECTED_SOURCE_COUNT,
           f"{len(records)} (expected {EXPECTED_SOURCE_COUNT})")

    ref_ids = [r["sourceId"] for r in records]
    ref_id_set = set(ref_ids)

    # 2. every source ID appears exactly once
    dup = [i for i in ref_id_set if ref_ids.count(i) > 1]
    record("every_source_appears_once", len(dup) == 0, f"duplicated: {dup[:10]}")

    # 17. no unexpected source IDs (+ no missing)
    missing = sorted(hsk1_ids - ref_id_set)
    unexpected = sorted(ref_id_set - hsk1_ids)
    record("no_missing_source_ids", len(missing) == 0, f"missing: {missing[:10]}")
    record("no_unexpected_source_ids", len(unexpected) == 0, f"unexpected: {unexpected[:10]}")

    # 3. every refined selected ID existed in P5.4.2
    outside_p542 = []
    for r in records:
        allowed = selection_ids_by_source.get(r["sourceId"], set())
        for wid in r.get("selectedRelatedWordIds", []):
            if wid not in allowed:
                outside_p542.append((r["sourceId"], wid))
    record("selected_ids_existed_in_p542", len(outside_p542) == 0, f"outside P5.4.2: {outside_p542[:10]}")

    # 4. every refined selected ID existed in P5.4.1 candidate pool
    outside_pool = []
    for r in records:
        allowed = pool_candidate_ids.get(r["sourceId"], set())
        for wid in r.get("selectedRelatedWordIds", []):
            if wid not in allowed:
                outside_pool.append((r["sourceId"], wid))
    record("selected_ids_within_candidate_pool", len(outside_pool) == 0, f"outside pool: {outside_pool[:10]}")

    # 5. no self references
    self_refs = [r["sourceId"] for r in records if r["sourceId"] in r.get("selectedRelatedWordIds", [])]
    record("no_self_references", len(self_refs) == 0, f"self-referencing: {self_refs[:10]}")

    # 6. no duplicate selected IDs
    dup_selected = []
    for r in records:
        ids = r.get("selectedRelatedWordIds", [])
        if len(ids) != len(set(ids)):
            dup_selected.append(r["sourceId"])
    record("no_duplicate_selected_ids", len(dup_selected) == 0, f"records with dupes: {dup_selected[:10]}")

    # 7. selectedCount matches array length
    count_mismatch = [
        r["sourceId"] for r in records
        if r.get("selectedCount") != len(r.get("selectedRelatedWordIds", []))
    ]
    record("selected_count_matches_array_length", len(count_mismatch) == 0, f"mismatches: {count_mismatch[:10]}")

    # 8. selectedCount <= 5
    over_max = [r["sourceId"] for r in records if r.get("selectedCount", 0) > MAX_SELECTED_PER_RECORD]
    record("max_selected_count_within_5", len(over_max) == 0, f"over max: {over_max[:10]}")

    # 9. valid statuses
    bad_status = [r["sourceId"] for r in records if r.get("status") not in VALID_STATUSES]
    record("status_valid", len(bad_status) == 0, f"invalid: {bad_status[:10]}")

    # 10. status/count consistency: a record's status must be internally
    #     consistent with whether it has an "uncertain" C-tier relation --
    #     since the refinement script's own promotion logic is opaque to
    #     this validator, we check the weaker but still meaningful
    #     invariant that needs_review records have >=1 tier-C reason, and
    #     that a 0-count record is never needs_review (0 relationships can
    #     never be "uncertain").
    inconsistent = []
    for r in records:
        reasons = r.get("selectionReasons", [])
        has_c = any(rr["category"] == "C" for rr in reasons)
        if r["status"] == "needs_review" and not has_c:
            inconsistent.append((r["sourceId"], "needs_review with no C-tier reason"))
        if r["status"] == "needs_review" and r.get("selectedCount", 0) == 0:
            inconsistent.append((r["sourceId"], "needs_review with 0 selections"))
    record("status_count_consistency", len(inconsistent) == 0, f"inconsistent: {inconsistent[:10]}")

    # 11/12/13/14/15. provenance complete + hashes correct + rules version
    required_fields = [
        "refinementVersion", "selectionArtifact", "selectionArtifactHash",
        "candidatePoolVersion", "candidatePoolHash", "sourceDatasetHash",
        "rulesVersion", "generatedAt", "records",
    ]
    missing_fields = [f for f in required_fields if f not in refined]
    record("provenance_fields_present", len(missing_fields) == 0, f"missing: {missing_fields}")

    record("selection_artifact_hash_correct",
           refined.get("selectionArtifactHash") == sha256_of(selection_text),
           f"recorded={refined.get('selectionArtifactHash')} actual={sha256_of(selection_text)}")

    record("candidate_pool_hash_correct",
           refined.get("candidatePoolHash") == sha256_of(pool_text),
           f"recorded={refined.get('candidatePoolHash')} actual={sha256_of(pool_text)}")

    record("source_hash_correct",
           refined.get("sourceDatasetHash") == sha256_of(hsk1_text),
           f"recorded={refined.get('sourceDatasetHash')} actual={sha256_of(hsk1_text)}")

    record("rules_version_present", bool(refined.get("rulesVersion")), f"value={refined.get('rulesVersion')}")

    # 16. no fabricated IDs
    fabricated = []
    hsk1_word_by_id = {r["id"]: r["word"] for r in hsk1_records}
    for r in records:
        for reason in r.get("selectionReasons", []):
            wid = reason["relatedWordId"]
            if wid not in hsk1_word_by_id:
                fabricated.append((r["sourceId"], wid))
    record("no_fabricated_ids", len(fabricated) == 0, f"fabricated: {fabricated[:10]}")

    # 18. refinement report consistent with artifact
    total_out_artifact = sum(r["selectedCount"] for r in records)
    report_consistent = (
        report.get("totalOutputRelationships") == total_out_artifact
        and report.get("outputRefinedArtifactHash") == sha256_of(refined_text)
    )
    record("refinement_report_consistent_with_artifact", report_consistent,
           f"report.totalOutput={report.get('totalOutputRelationships')} actual={total_out_artifact} "
           f"report.hash={report.get('outputRefinedArtifactHash')} actual={sha256_of(refined_text)}")

    # 19. deterministic ordering (tier A,B,C then id ascending within tier)
    tier_order = {"A": 0, "B": 1, "C": 2}
    unordered = []
    for r in records:
        reasons = r.get("selectionReasons", [])
        keys = [(tier_order.get(rr["category"], 9), rr["relatedWordId"]) for rr in reasons]
        if keys != sorted(keys):
            unordered.append(r["sourceId"])
    record("deterministic_ordering", len(unordered) == 0, f"unordered: {unordered[:10]}")

    # 20. production unchanged
    non_empty_production = [
        rid for rid, val in hsk1_relatedWordIds_before.items() if val not in (None, [])
    ]
    record("production_relatedWordIds_untouched", len(non_empty_production) == 0,
           f"non-empty in production: {non_empty_production[:10]}")

    print("=== P5.4.3 refinement validation ===")
    for name, result in checks.items():
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {name}: {result['detail']}")

    print()
    print(f"allChecksPassed: {all_passed}")

    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
