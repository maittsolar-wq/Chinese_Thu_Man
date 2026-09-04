"""P5.10.2 -- Validator for tools/hsk/examples/hsk_examples_p102_pilot_01.json.

Read-only. Never writes to the pilot artifact, production data, app/src,
or any prior-phase artifact. Exits non-zero if any check fails.

Usage:
    python validate_hsk_examples_p102.py
"""

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
PILOT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "hsk_examples_p102_pilot_01.json"

EXPECTED_PILOT_SIZE = 100
EXPECTED_FIELDS = {"chinese", "pinyin", "meaningVi"}
VALID_QA_STATUSES = {"pending", "passed", "needs_review", "rejected"}
VALID_REVIEWER_STATUSES = {"unreviewed", "human_reviewed"}

PRODUCTION_HASHES_EXPECTED = {
    1: "371c8c5b16a5b7250433b4adffa419f4752fe4a2",
    2: "f468aeafeda1a32285b303dc2b37c284b9160d45",
    3: "0d21c124e2e11351b8f89fb62a1d9e2f613de7fd",
    4: "b85fc217da54d4796df951b19e32b1029dfb8feb",
    5: "22625d91cb5ac6e56af17531d61d1eeaa61e08c6",
    6: "77fad88d80caed515a1875aa296cc9d7c12011a0",
}


def load_json_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def git_hash_object(path: Path) -> str:
    out = subprocess.check_output(["git", "hash-object", str(path)], cwd=REPO_ROOT)
    return out.decode("utf-8").strip()


def main() -> None:
    checks: dict[str, dict] = {}
    all_passed = True

    def record(name: str, passed: bool, detail: str) -> None:
        nonlocal all_passed
        checks[name] = {"passed": passed, "detail": detail}
        if not passed:
            all_passed = False

    if not PILOT_PATH.exists():
        print(f"FAIL: pilot artifact missing: {PILOT_PATH}")
        raise SystemExit(1)

    artifact = json.loads(load_json_text(PILOT_PATH))
    recs = artifact.get("records", [])

    # 1. exactly 100 pilot vocabulary records
    record("exactly_100_pilot_records", len(recs) == EXPECTED_PILOT_SIZE, f"{len(recs)}")

    # 2. valid vocabulary IDs / 3. no duplicate IDs
    universe = {}
    for n in (1, 2, 3, 4, 5, 6):
        path = REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
        for r in json.loads(load_json_text(path)):
            universe[r["id"]] = {**r, "_level": n}

    ids = [r["sourceId"] for r in recs]
    record("valid_vocabulary_ids", all(rid in universe for rid in ids),
           f"unknown: {[rid for rid in ids if rid not in universe][:10]}")
    record("no_duplicate_vocabulary_ids", len(ids) == len(set(ids)), f"dupes: {[i for i in set(ids) if ids.count(i)>1]}")

    # 4. valid HSK levels
    bad_levels = [(r["sourceId"], r["hskLevel"]) for r in recs if universe.get(r["sourceId"], {}).get("_level") != r["hskLevel"]]
    record("valid_hsk_levels", len(bad_levels) == 0, f"{bad_levels[:10]}")

    # 5. source production hash present
    record("source_production_hash_present", bool(artifact.get("sourceProductionHashes")),
           f"{artifact.get('sourceProductionHashes')}")
    hash_mismatches = []
    for level_key, expected_hash in artifact.get("sourceProductionHashes", {}).items():
        n = int(level_key.replace("hsk", ""))
        path = REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
        actual = hashlib.sha256(load_json_text(path).encode("utf-8")).hexdigest()
        if actual != expected_hash:
            hash_mismatches.append((level_key, expected_hash, actual))
    record("source_production_hashes_correct", len(hash_mismatches) == 0, f"{hash_mismatches}")

    # 6. examples field exists in artifact
    record("examples_field_exists_on_every_record", all("examples" in r for r in recs), "checked")

    # 7. each example has exactly chinese/pinyin/meaningVi / 8. no English field
    malformed = []
    for r in recs:
        for ex in r["examples"]:
            if set(ex.keys()) != EXPECTED_FIELDS:
                malformed.append((r["sourceId"], sorted(ex.keys())))
    record("each_example_has_exactly_three_fields", len(malformed) == 0, f"{malformed[:10]}")
    record("no_english_field", all("english" not in ex for r in recs for ex in r["examples"]), "checked")

    # 9-11. non-empty chinese/pinyin/meaningVi
    empty_fields = []
    for r in recs:
        for ex in r["examples"]:
            for field in ("chinese", "pinyin", "meaningVi"):
                if not ex.get(field, "").strip():
                    empty_fields.append((r["sourceId"], field))
    record("chinese_non_empty", not any(f == "chinese" for _, f in empty_fields), f"{[e for e in empty_fields if e[1]=='chinese'][:10]}")
    record("pinyin_non_empty", not any(f == "pinyin" for _, f in empty_fields), f"{[e for e in empty_fields if e[1]=='pinyin'][:10]}")
    record("meaningVi_non_empty", not any(f == "meaningVi" for _, f in empty_fields), f"{[e for e in empty_fields if e[1]=='meaningVi'][:10]}")

    # 12. target word appears in chinese
    missing_target = []
    for r in recs:
        for ex in r["examples"]:
            if r["sourceWord"] not in ex["chinese"]:
                missing_target.append((r["sourceId"], r["sourceWord"], ex["chinese"]))
    record("target_word_appears_in_chinese", len(missing_target) == 0, f"{missing_target[:10]}")

    # 13. no duplicate examples (across the whole pilot)
    all_sentences = [ex["chinese"] for r in recs for ex in r["examples"]]
    dup_sentences = [s for s, c in Counter(all_sentences).items() if c > 1]
    record("no_duplicate_examples_across_pilot", len(dup_sentences) == 0, f"{dup_sentences}")

    # 14. no duplicate sentence within a record
    within_dup = []
    for r in recs:
        sents = [ex["chinese"] for ex in r["examples"]]
        if len(sents) != len(set(sents)):
            within_dup.append(r["sourceId"])
    record("no_duplicate_sentence_within_record", len(within_dup) == 0, f"{within_dup}")

    # 15. risk metadata valid
    bad_tier = [r["sourceId"] for r in recs if r.get("riskTier") not in (1, 2, 3, 4)]
    record("risk_metadata_valid", len(bad_tier) == 0, f"{bad_tier[:10]}")
    tier34_present = [r["sourceId"] for r in recs if r.get("riskTier") in (3, 4)]
    record("no_tier3_tier4_records_in_normal_pilot", len(tier34_present) == 0, f"{tier34_present}")

    # 16. QA status valid
    bad_qa = [r["sourceId"] for r in recs if r.get("qaStatus") not in VALID_QA_STATUSES]
    record("qa_status_valid", len(bad_qa) == 0, f"{bad_qa[:10]}")
    bad_reviewer = [r["sourceId"] for r in recs if r.get("reviewerStatus") not in VALID_REVIEWER_STATUSES]
    record("reviewer_status_valid", len(bad_reviewer) == 0, f"{bad_reviewer[:10]}")

    # needs_review records must have 0 examples and a reason
    nr_bad = [r["sourceId"] for r in recs if r["qaStatus"] == "needs_review" and (r["examples"] or not r.get("needsReviewReason"))]
    record("needs_review_records_have_zero_examples_and_a_reason", len(nr_bad) == 0, f"{nr_bad}")

    # 17. provenance valid
    required_top = ["pilotVersion", "generationBatch", "generatedAt", "generationMethod",
                     "generatorScript", "selectionRuleSummary", "sourceProductionHashes"]
    missing_top = [f for f in required_top if f not in artifact]
    record("provenance_fields_present", len(missing_top) == 0, f"{missing_top}")

    # 18. no production modification
    prod_diffs = []
    for n in (1, 2, 3, 4, 5, 6):
        path = REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
        actual_hash = git_hash_object(path)
        if actual_hash != PRODUCTION_HASHES_EXPECTED[n]:
            prod_diffs.append((n, PRODUCTION_HASHES_EXPECTED[n], actual_hash))
    record("no_production_modification", len(prod_diffs) == 0, f"{prod_diffs}")

    # 19. no app/src modification
    app_src_status = subprocess.check_output(
        ["git", "status", "--short", "--", "app/src"], cwd=REPO_ROOT
    ).decode("utf-8").strip()
    record("no_app_src_modification", app_src_status == "", f"git status: '{app_src_status}'")

    # ---- additional checks beyond the minimum 19 ----
    # word count per level matches expected allocation
    level_dist = Counter(r["hskLevel"] for r in recs)
    record("level_distribution_recorded", dict(level_dist) == {1: 6, 2: 4, 3: 9, 4: 18, 5: 30, 6: 33},
           f"{dict(level_dist)}")

    example_count_dist = Counter(len(r["examples"]) for r in recs)
    record("example_count_within_1_to_3_or_needs_review", all(
        len(r["examples"]) in (1, 2, 3) or r["qaStatus"] == "needs_review" for r in recs
    ), f"distribution: {dict(example_count_dist)}")

    total_examples = sum(len(r["examples"]) for r in recs)
    record("total_examples_matches_artifact_field", total_examples == artifact.get("totalExamples"),
           f"recomputed={total_examples} artifact={artifact.get('totalExamples')}")

    # opening-character repetition sanity (not a hard fail-closed threshold,
    # informational diversity signal only)
    openings = Counter(ex["chinese"][:2] for r in recs for ex in r["examples"])
    most_common = openings.most_common(1)
    max_opening_share = (most_common[0][1] / total_examples) if most_common and total_examples else 0
    record("no_single_opening_dominates_examples", max_opening_share < 0.15,
           f"most common opening '{most_common[0][0] if most_common else None}' = {max_opening_share:.1%} of examples")

    print("=== P5.10.2 pilot validation ===")
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
