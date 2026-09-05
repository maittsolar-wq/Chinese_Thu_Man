"""
Stroke Count Pass 03 -- production integration validator.

Compares the pre-integration manifest (pre_integration_manifest.py,
already run before the merge) against the CURRENT on-disk production
state, and against the approved Pass 02 draft
(vocabulary_stroke_draft.json), to prove:

  - only `strokeCount` changed, for exactly 5400 records, with zero
    unexpected field changes
  - production strokeCount == approved draft strokeCount for all 5400
  - every preserved field (examples, relatedWordIds, humanVerified,
    groundTruth, verificationStatus, characterIds, word, pinyin,
    meaningVi) is unchanged
  - no duplicate/lost/added ids

Read-only. Writes only its own report file.
"""
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent
LEVELS = [1, 2, 3, 4, 5, 6]
EXPECTED_LEVEL_COUNTS = {1: 300, 2: 200, 3: 500, 4: 1000, 5: 1600, 6: 1800}
EXPECTED_TOTAL = 5400

KNOWN_SUFFIX_EXPECTED = {
    "hsk6_0157": ("乘2", 10), "hsk6_0407": ("副2", 11), "hsk6_0413": ("该2", 8),
    "hsk6_0741": ("局1", 7), "hsk6_0742": ("局2", 7), "hsk6_0850": ("料1", 10),
    "hsk6_0851": ("料2", 10), "hsk6_0863": ("露1", 21), "hsk6_1169": ("升2", 4),
    "hsk6_1254": ("所2", 8), "hsk6_1653": ("则1", 6), "hsk6_1694": ("支2", 4),
}

PRESERVED_NON_STROKE_FIELDS = [
    "id", "word", "pinyin", "meaningVi", "examples", "relatedWordIds",
    "humanVerified", "groundTruth", "verificationStatus", "characterIds",
]

checks = []

def check(name, passed, detail=""):
    checks.append({"name": name, "passed": bool(passed), "detail": detail})
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}: {detail}")

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest = json.loads((OUT_DIR / "pre_integration_manifest.json").read_text(encoding="utf-8"))
    draft_doc = json.loads((OUT_DIR / "vocabulary_stroke_draft.json").read_text(encoding="utf-8"))
    draft_by_id = {r["id"]: r["strokeCount"] for r in draft_doc["records"]}

    current_by_level = {}
    current_hashes = {}
    for lvl in LEVELS:
        path = REPO_ROOT / "data" / "hsk" / f"hsk{lvl}" / f"hsk{lvl}_vocabulary_production.json"
        raw = path.read_bytes()
        current_hashes[lvl] = hashlib.sha256(raw).hexdigest()
        current_by_level[lvl] = json.loads(raw.decode("utf-8"))

    # A. Record count
    total_before = manifest["totalRecords"]
    total_after = sum(len(v) for v in current_by_level.values())
    check("A_record_count_before_5400", total_before == EXPECTED_TOTAL, f"{total_before}")
    check("A_record_count_after_5400", total_after == EXPECTED_TOTAL, f"{total_after}")
    for lvl in LEVELS:
        check(f"A_hsk{lvl}_count_unchanged",
              manifest["levels"][str(lvl)]["recordCount"] == len(current_by_level[lvl]) == EXPECTED_LEVEL_COUNTS[lvl],
              f"before={manifest['levels'][str(lvl)]['recordCount']} after={len(current_by_level[lvl])} expected={EXPECTED_LEVEL_COUNTS[lvl]}")

    # B. ID set identical before/after; M. no duplicate/lost/added records
    ids_before = set()
    for lvl in LEVELS:
        for r in manifest["levels"][str(lvl)]["records"]:
            ids_before.add(r["id"])
    ids_after = set()
    for lvl in LEVELS:
        for r in current_by_level[lvl]:
            ids_after.add(r["id"])
    check("B_id_set_identical", ids_before == ids_after,
          f"before={len(ids_before)} after={len(ids_after)} diff={ids_before.symmetric_difference(ids_after)}")

    dup_check_ok = True
    for lvl in LEVELS:
        current_ids = [r["id"] for r in current_by_level[lvl]]
        if len(current_ids) != len(set(current_ids)):
            dup_check_ok = False
    check("M_no_duplicate_ids_introduced", dup_check_ok, "")
    check("M_no_records_lost_or_duplicated", total_before == total_after == len(ids_after), "")

    # C. Word set identical
    words_before = set()
    for lvl in LEVELS:
        for r in manifest["levels"][str(lvl)]["records"]:
            words_before.add((r["id"], r["word"]))
    words_after = set()
    for lvl in LEVELS:
        for r in current_by_level[lvl]:
            words_after.add((r["id"], r["word"]))
    check("C_word_set_identical", words_before == words_after,
          f"diff={words_before.symmetric_difference(words_after)}")

    # D/E. Stroke coverage + validity
    all_current = [r for lvl in LEVELS for r in current_by_level[lvl]]
    null_count = sum(1 for r in all_current if r.get("strokeCount") is None)
    zero_count = sum(1 for r in all_current if r.get("strokeCount") == 0)
    negative_count = sum(1 for r in all_current if isinstance(r.get("strokeCount"), int) and r.get("strokeCount") < 0)
    non_int_count = sum(1 for r in all_current
                         if r.get("strokeCount") is not None
                         and (not isinstance(r.get("strokeCount"), int) or isinstance(r.get("strokeCount"), bool)))
    positive_int_count = sum(1 for r in all_current
                              if isinstance(r.get("strokeCount"), int)
                              and not isinstance(r.get("strokeCount"), bool)
                              and r.get("strokeCount") > 0)

    check("D_stroke_coverage_5400_populated", positive_int_count == EXPECTED_TOTAL, f"{positive_int_count}")
    check("D_zero_null_absent_count", null_count == 0, f"{null_count}")
    check("E_zero_zero_values", zero_count == 0, f"{zero_count}")
    check("E_zero_negative_values", negative_count == 0, f"{negative_count}")
    check("E_zero_non_integer_values", non_int_count == 0, f"{non_int_count}")

    # F. Draft parity
    mismatches = []
    for r in all_current:
        rid = r["id"]
        prod_val = r.get("strokeCount")
        draft_val = draft_by_id.get(rid)
        if prod_val != draft_val:
            mismatches.append({"id": rid, "production": prod_val, "draft": draft_val})
    check("F_draft_parity_5400_match", len(mismatches) == 0, f"mismatches={len(mismatches)}: {mismatches[:5]}")

    # G. Non-stroke field preservation
    current_by_id = {r["id"]: r for r in all_current}
    field_diffs = []
    for lvl in LEVELS:
        for before_rec in manifest["levels"][str(lvl)]["records"]:
            rid = before_rec["id"]
            after_rec = current_by_id.get(rid, {})
            for field in PRESERVED_NON_STROKE_FIELDS:
                before_val = before_rec[field]
                after_val = after_rec.get(field, "__ABSENT__")
                if before_val == "__ABSENT__":
                    # field didn't exist before either (e.g. HSK6 characterIds) -- must still be absent
                    if field in after_rec:
                        field_diffs.append({"id": rid, "field": field, "before": "__ABSENT__", "after": after_val})
                else:
                    if before_val != after_val:
                        field_diffs.append({"id": rid, "field": field, "before": before_val, "after": after_val})
    check("G_zero_unexpected_field_changes", len(field_diffs) == 0, f"count={len(field_diffs)} sample={field_diffs[:5]}")

    # H/I/J/K individually (subset of G, reported separately per spec)
    def count_field_diffs(field):
        return sum(1 for d in field_diffs if d["field"] == field)
    check("H_relatedWordIds_preserved", count_field_diffs("relatedWordIds") == 0, "")
    check("I_examples_preserved", count_field_diffs("examples") == 0, "")
    check("J_humanVerified_preserved", count_field_diffs("humanVerified") == 0, "")
    check("J_groundTruth_preserved", count_field_diffs("groundTruth") == 0, "")
    check("J_verificationStatus_preserved", count_field_diffs("verificationStatus") == 0, "")
    check("K_characterIds_preserved", count_field_diffs("characterIds") == 0, "")

    # L. Known suffix records
    suffix_failures = []
    for rid, (expected_word, expected_stroke) in KNOWN_SUFFIX_EXPECTED.items():
        rec = current_by_id.get(rid)
        if rec is None or rec["word"] != expected_word or rec.get("strokeCount") != expected_stroke:
            suffix_failures.append({"id": rid, "expected": (expected_word, expected_stroke),
                                     "actual": (rec.get("word") if rec else None, rec.get("strokeCount") if rec else None)})
    check("L_known_suffix_records_correct", len(suffix_failures) == 0, f"failures={suffix_failures}")

    # Whole-record byte equivalence check EXCLUDING strokeCount (belt-and-braces on top of G)
    exact_diffs = []
    for lvl in LEVELS:
        for before_rec in manifest["levels"][str(lvl)]["records"]:
            rid = before_rec["id"]
            after_rec = current_by_id.get(rid, {})
            before_copy = {k: v for k, v in before_rec.items() if k != "strokeCount"}
            after_copy = {k: after_rec.get(k, "__ABSENT__") for k in before_copy}
            if before_copy != after_copy:
                exact_diffs.append(rid)
    check("changed_field_is_only_strokeCount", len(exact_diffs) == 0, f"records_with_other_changes={len(exact_diffs)}")

    changed_record_count = sum(
        1 for lvl in LEVELS for before_rec in manifest["levels"][str(lvl)]["records"]
        if before_rec["strokeCount"] != current_by_id[before_rec["id"]].get("strokeCount")
    )
    check("changed_record_count_is_5400", changed_record_count == EXPECTED_TOTAL, f"{changed_record_count}")

    # Hash record (informational -- whole-file hash change is EXPECTED, not a failure)
    print("\n=== whole-file SHA-256 (expected to differ -- strokeCount changed) ===")
    for lvl in LEVELS:
        before_hash = manifest["levels"][str(lvl)]["sha256"]
        after_hash = current_hashes[lvl]
        print(f"HSK{lvl}: before={before_hash}")
        print(f"HSK{lvl}: after ={after_hash}")
        print(f"HSK{lvl}: changed={before_hash != after_hash} (expected: True)")

    total_checks = len(checks)
    passed_checks = sum(1 for c in checks if c["passed"])
    print(f"\nallChecksPassed: {passed_checks == total_checks}")
    print(f"checksTotal: {total_checks}")
    print(f"checksPassed: {passed_checks}")

    report = {
        "checksTotal": total_checks, "checksPassed": passed_checks,
        "allChecksPassed": passed_checks == total_checks, "checks": checks,
        "hashesBefore": {lvl: manifest["levels"][str(lvl)]["sha256"] for lvl in LEVELS},
        "hashesAfter": current_hashes,
    }
    (OUT_DIR / "integration_validation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return 0 if passed_checks == total_checks else 1

if __name__ == "__main__":
    sys.exit(main())
