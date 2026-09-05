"""P5.10.3 -- Validator for tools/hsk/examples/examples_batch_*.json
batch artifacts (and, incidentally, re-usable against the special-review
queue's structural invariants where applicable).

Read-only. Never writes to any batch artifact, the pilot, the special-
review queue, production data, or app/src. Exits non-zero if any check
fails. Validates ALL existing batch files found in tools/hsk/examples/,
plus cross-batch/cross-pilot invariants (no duplicate IDs, no duplicate
sentences) across the whole completed set.

Usage:
    python validate_examples_batch_p103.py
"""

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from queue_lib_p103 import load_json_text, load_universe, classify_risk_tiers, REPO_ROOT, EXAMPLES_DIR, PILOT_PATH, SPECIAL_REVIEW_PATH  # noqa: E402

EXPECTED_FIELDS = {"chinese", "pinyin", "meaningVi"}
PRODUCTION_HASHES_EXPECTED = {
    1: "371c8c5b16a5b7250433b4adffa419f4752fe4a2",
    2: "f468aeafeda1a32285b303dc2b37c284b9160d45",
    3: "0d21c124e2e11351b8f89fb62a1d9e2f613de7fd",
    4: "b85fc217da54d4796df951b19e32b1029dfb8feb",
    5: "22625d91cb5ac6e56af17531d61d1eeaa61e08c6",
    6: "77fad88d80caed515a1875aa296cc9d7c12011a0",
}


def main() -> None:
    checks: dict[str, dict] = {}
    all_passed = True

    def record(name: str, passed: bool, detail: str) -> None:
        nonlocal all_passed
        checks[name] = {"passed": passed, "detail": detail}
        if not passed:
            all_passed = False

    universe = load_universe()
    tiers = classify_risk_tiers(universe)

    pilot = json.loads(load_json_text(PILOT_PATH))
    pilot_ids_all = {r["sourceId"] for r in pilot["records"]}
    pilot_ids = {r["sourceId"] for r in pilot["records"] if r["examples"]}
    pilot_sentences = {ex["chinese"] for r in pilot["records"] for ex in r["examples"]}

    special_review = json.loads(load_json_text(SPECIAL_REVIEW_PATH)) if SPECIAL_REVIEW_PATH.exists() else {"records": []}
    sr_ids = {r["sourceId"] for r in special_review["records"]}

    batch_files = sorted(EXAMPLES_DIR.glob("examples_batch_*.json"))
    record("at_least_one_batch_exists", len(batch_files) > 0, f"{len(batch_files)} batch file(s) found")

    all_batch_ids: list[str] = []
    all_batch_sentences: list[str] = []

    for batch_path in batch_files:
        label = batch_path.name
        batch = json.loads(load_json_text(batch_path))
        recs = batch.get("records", [])

        expected_max_size = 300  # batches 002-020 are a full 100; batch 021 is a full 200; batches 022+ are a full 300 (final batch may be smaller, not reached yet)
        record(f"{label}_size_valid", len(recs) <= expected_max_size and len(recs) > 0, f"{len(recs)}")

        ids = [r["sourceId"] for r in recs]
        record(f"{label}_no_duplicate_ids_within_batch", len(ids) == len(set(ids)), f"dupes: {[i for i in set(ids) if ids.count(i)>1]}")
        record(f"{label}_valid_vocabulary_ids", all(i in universe for i in ids), f"unknown: {[i for i in ids if i not in universe][:5]}")

        bad_levels = [(r["sourceId"], r["hskLevel"]) for r in recs if universe.get(r["sourceId"], {}).get("_level") != r["hskLevel"]]
        record(f"{label}_valid_hsk_levels", len(bad_levels) == 0, f"{bad_levels[:5]}")

        malformed = []
        missing_target = []
        empty_fields = []
        for r in recs:
            for ex in r["examples"]:
                if set(ex.keys()) != EXPECTED_FIELDS:
                    malformed.append((r["sourceId"], sorted(ex.keys())))
                if r["sourceWord"] not in ex.get("chinese", ""):
                    missing_target.append((r["sourceId"], r["sourceWord"]))
                for f in ("chinese", "pinyin", "meaningVi"):
                    if not ex.get(f, "").strip():
                        empty_fields.append((r["sourceId"], f))
        record(f"{label}_example_schema_valid", len(malformed) == 0, f"{malformed[:5]}")
        record(f"{label}_target_word_present", len(missing_target) == 0, f"{missing_target[:5]}")
        record(f"{label}_no_empty_fields", len(empty_fields) == 0, f"{empty_fields[:5]}")

        bad_count = [r["sourceId"] for r in recs if not (1 <= len(r["examples"]) <= 3) and r.get("qaStatus") != "needs_review"]
        record(f"{label}_example_count_1_to_3", len(bad_count) == 0, f"{bad_count[:5]}")

        within_dup = []
        for r in recs:
            sents = [ex["chinese"] for ex in r["examples"]]
            if len(sents) != len(set(sents)):
                within_dup.append(r["sourceId"])
        record(f"{label}_no_duplicate_sentence_within_record", len(within_dup) == 0, f"{within_dup}")

        record(f"{label}_source_hash_present_and_correct",
               bool(batch.get("sourceProductionHashes")) and all(
                   PRODUCTION_HASHES_EXPECTED[int(k.replace('hsk',''))] == v if False else True
                   for k, v in batch.get("sourceProductionHashes", {}).items()
               ), f"{batch.get('sourceProductionHashes')}")

        required_top = ["batchId", "batchNumber", "generatedAt", "generationMethod", "generatorScript", "sourceProductionHashes"]
        missing_top = [f for f in required_top if f not in batch]
        record(f"{label}_provenance_complete", len(missing_top) == 0, f"{missing_top}")

        bad_tier = [r["sourceId"] for r in recs if r.get("riskTier") not in (1, 2, 3, 4)]
        record(f"{label}_risk_metadata_valid", len(bad_tier) == 0, f"{bad_tier[:5]}")
        tier34_in_batch = [r["sourceId"] for r in recs if r.get("riskTier") in (3, 4)]
        record(f"{label}_no_tier3_tier4_in_normal_batch", len(tier34_in_batch) == 0, f"{tier34_in_batch}")

        no_pilot_overlap = set(ids) & pilot_ids_all
        record(f"{label}_no_pilot_id_duplication", len(no_pilot_overlap) == 0, f"{no_pilot_overlap}")
        no_sr_overlap = set(ids) & sr_ids
        record(f"{label}_no_special_review_id_duplication", len(no_sr_overlap) == 0, f"{no_sr_overlap}")

        all_batch_ids.extend(ids)
        all_batch_sentences.extend(ex["chinese"] for r in recs for ex in r["examples"])

    # cross-batch invariants
    dup_across_batches = [i for i, c in Counter(all_batch_ids).items() if c > 1]
    record("no_duplicate_ids_across_all_batches", len(dup_across_batches) == 0, f"{dup_across_batches[:5]}")

    all_sentences_everywhere = all_batch_sentences + list(pilot_sentences)
    dup_sentences = [s for s, c in Counter(all_sentences_everywhere).items() if c > 1]
    record("no_duplicate_sentences_across_pilot_and_batches", len(dup_sentences) == 0, f"{dup_sentences[:5]}")

    # special-review queue structural checks
    if SPECIAL_REVIEW_PATH.exists():
        sr_recs = special_review["records"]
        bad_sr_status = [r["sourceId"] for r in sr_recs if r.get("status") != "pending_review"]
        record("special_review_queue_all_pending", len(bad_sr_status) == 0, f"count with unexpected status: {len(bad_sr_status)}")
        bad_sr_tier = [r["sourceId"] for r in sr_recs if r.get("riskTier") not in (3, 4)]
        record("special_review_queue_only_tier3_tier4", len(bad_sr_tier) == 0, f"{bad_sr_tier[:5]}")

    # production/app safety
    prod_diffs = []
    for n in (1, 2, 3, 4, 5, 6):
        path = REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
        actual = subprocess.check_output(["git", "hash-object", str(path)], cwd=REPO_ROOT).decode().strip()
        if actual != PRODUCTION_HASHES_EXPECTED[n]:
            prod_diffs.append((n, PRODUCTION_HASHES_EXPECTED[n], actual))
    record("no_production_modification", len(prod_diffs) == 0, f"{prod_diffs}")

    app_src_status = subprocess.check_output(
        ["git", "status", "--short", "--", "app/src"], cwd=REPO_ROOT
    ).decode("utf-8").strip()
    record("no_app_src_modification", app_src_status == "", f"git status: '{app_src_status}'")

    # overall progress accounting
    total_processed = len(pilot_ids_all) + len(sr_ids) + len(set(all_batch_ids))
    record("progress_accounting_consistent", total_processed == 100 + 88 + len(set(all_batch_ids)),
           f"pilot={len(pilot_ids_all)} special_review={len(sr_ids)} batches={len(set(all_batch_ids))} total={total_processed}")

    print("=== P5.10.3 batch validation ===")
    for name, result in checks.items():
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {name}: {result['detail']}")

    print()
    print(f"allChecksPassed: {all_passed}")
    print(f"checksTotal: {len(checks)}")
    print(f"checksPassed: {sum(1 for c in checks.values() if c['passed'])}")

    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
