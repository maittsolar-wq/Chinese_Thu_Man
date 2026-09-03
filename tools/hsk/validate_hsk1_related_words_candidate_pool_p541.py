"""P5.4.1 -- Validator for tools/hsk/hsk1_related_words_candidate_pool.json.

Read-only. Never writes to the candidate pool artifact, the HSK1
production file, or any other production/artifact file. Prints a
machine-readable summary and exits non-zero if any check fails --
no fake "allChecksPassed": true is ever emitted when a check fails.

Usage:
    python validate_hsk1_related_words_candidate_pool_p541.py
"""

import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HSK1_PATH = REPO_ROOT / "data" / "hsk" / "hsk1" / "hsk1_vocabulary_production.json"
POOL_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_candidate_pool.json"

MAX_CANDIDATES_PER_RECORD = 20
EXPECTED_SOURCE_COUNT = 300


def load_json_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_candidate_universe() -> dict:
    universe: dict[str, dict] = {}
    for lvl in (1, 2, 3, 4, 5, 6):
        path = REPO_ROOT / "data" / "hsk" / f"hsk{lvl}" / f"hsk{lvl}_vocabulary_production.json"
        records = json.loads(load_json_text(path))
        for r in records:
            universe[r["id"]] = {"word": r["word"], "hskLevel": lvl}
    return universe


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
    hsk1_ids = [r["id"] for r in hsk1_records]
    hsk1_id_set = set(hsk1_ids)

    if not POOL_PATH.exists():
        print("FAIL: candidate pool artifact does not exist:", POOL_PATH)
        raise SystemExit(1)

    pool_text = load_json_text(POOL_PATH)
    pool = json.loads(pool_text)
    records = pool.get("records", [])

    universe = load_candidate_universe()

    # 1. source record count = 300
    record("source_record_count", len(hsk1_records) == EXPECTED_SOURCE_COUNT,
            f"{len(hsk1_records)} (expected {EXPECTED_SOURCE_COUNT})")

    # 2. candidate pool record count = 300
    record("pool_record_count", len(records) == EXPECTED_SOURCE_COUNT,
            f"{len(records)} (expected {EXPECTED_SOURCE_COUNT})")

    # 3 & 16 & 17. every sourceId exists / no source records missing / no unexpected source IDs
    pool_ids = [r["sourceId"] for r in records]
    pool_id_set = set(pool_ids)
    missing = sorted(hsk1_id_set - pool_id_set)
    unexpected = sorted(pool_id_set - hsk1_id_set)
    record("every_source_id_exists_in_hsk1", len(missing) == 0, f"missing: {missing[:10]}")
    record("no_unexpected_source_ids", len(unexpected) == 0, f"unexpected: {unexpected[:10]}")

    # 4. every sourceId appears exactly once
    dup_sources = [i for i in pool_id_set if pool_ids.count(i) > 1]
    record("source_id_appears_once", len(dup_sources) == 0, f"duplicated: {dup_sources[:10]}")

    # 5. candidate count <= 20
    over_limit = [r["sourceId"] for r in records if len(r.get("candidates", [])) > MAX_CANDIDATES_PER_RECORD]
    record("candidate_count_within_max", len(over_limit) == 0,
           f"records exceeding {MAX_CANDIDATES_PER_RECORD}: {over_limit[:10]}")

    # 6. no self references
    self_refs = []
    for r in records:
        for c in r.get("candidates", []):
            if c["wordId"] == r["sourceId"]:
                self_refs.append(r["sourceId"])
    record("no_self_references", len(self_refs) == 0, f"self-referencing: {self_refs[:10]}")

    # 7. no duplicate candidate IDs (within a record)
    dup_candidates = []
    for r in records:
        ids = [c["wordId"] for c in r.get("candidates", [])]
        if len(ids) != len(set(ids)):
            dup_candidates.append(r["sourceId"])
    record("no_duplicate_candidate_ids", len(dup_candidates) == 0, f"records with dupes: {dup_candidates[:10]}")

    # 8. every candidate ID exists in production universe
    unknown_candidates = []
    for r in records:
        for c in r.get("candidates", []):
            if c["wordId"] not in universe:
                unknown_candidates.append((r["sourceId"], c["wordId"]))
    record("all_candidate_ids_known", len(unknown_candidates) == 0,
           f"unknown refs: {unknown_candidates[:10]}")

    # 9. every candidate has valid HSK level (1-6, and matches the universe's own level for that id)
    bad_levels = []
    for r in records:
        for c in r.get("candidates", []):
            expected_level = universe.get(c["wordId"], {}).get("hskLevel")
            level = c.get("hskLevel")
            if level not in (1, 2, 3, 4, 5, 6) or (expected_level is not None and level != expected_level):
                bad_levels.append((r["sourceId"], c["wordId"], level, expected_level))
    record("valid_hsk_levels", len(bad_levels) == 0, f"mismatches: {bad_levels[:10]}")

    # 10. candidate ordering deterministic (sorted by wordId within each record)
    unordered = []
    for r in records:
        ids = [c["wordId"] for c in r.get("candidates", [])]
        if ids != sorted(ids):
            unordered.append(r["sourceId"])
    record("deterministic_ordering", len(unordered) == 0, f"unordered records: {unordered[:10]}")

    # 11. provenance fields exist
    required_top_fields = [
        "poolVersion", "sourceDataset", "sourceDatasetHash", "candidateUniverse",
        "candidateUniverseHash", "rulesVersion", "generatedAt", "records",
    ]
    missing_fields = [f for f in required_top_fields if f not in pool]
    record("provenance_fields_present", len(missing_fields) == 0, f"missing: {missing_fields}")

    # 12. source dataset hash exists (and matches the actual current HSK1 file)
    recorded_source_hash = pool.get("sourceDatasetHash")
    actual_source_hash = sha256_of(hsk1_text)
    record("source_dataset_hash_recorded_and_matches",
           bool(recorded_source_hash) and recorded_source_hash == actual_source_hash,
           f"recorded={recorded_source_hash} actual={actual_source_hash}")

    # 13. candidate universe hash exists
    record("candidate_universe_hash_recorded", bool(pool.get("candidateUniverseHash")),
           f"value={pool.get('candidateUniverseHash')}")

    # 14. rules version exists
    record("rules_version_recorded", bool(pool.get("rulesVersion")), f"value={pool.get('rulesVersion')}")

    # 15. no fabricated IDs -- every candidate id resolves AND every source id resolves
    #     to a real word (word/hskLevel are non-empty and match the universe / hsk1 file).
    fabricated = []
    for r in records:
        src = next((h for h in hsk1_records if h["id"] == r["sourceId"]), None)
        if src is None or src["word"] != r.get("sourceWord"):
            fabricated.append(("source", r["sourceId"]))
        for c in r.get("candidates", []):
            u = universe.get(c["wordId"])
            if u is None or u["word"] != c.get("word"):
                fabricated.append(("candidate", c["wordId"]))
    record("no_fabricated_ids", len(fabricated) == 0, f"fabricated/mismatched: {fabricated[:10]}")

    # Extra integrity: candidateCount field matches actual candidates length
    count_mismatches = [
        r["sourceId"] for r in records
        if r.get("candidateCount") != len(r.get("candidates", []))
    ]
    record("candidate_count_field_matches_array_length", len(count_mismatches) == 0,
           f"mismatches: {count_mismatches[:10]}")

    print("=== P5.4.1 candidate pool validation ===")
    for name, result in checks.items():
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {name}: {result['detail']}")

    print()
    print(f"allChecksPassed: {all_passed}")

    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
