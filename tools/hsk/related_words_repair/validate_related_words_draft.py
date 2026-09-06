"""
Related Words Pass 02 -- draft validator.

Read-only. Validates related_words_draft.json against production data
and the approved product rule before any integration is allowed.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent
LEVELS = [1, 2, 3, 4, 5, 6]

checks = []

def check(name, passed, detail=""):
    checks.append({"name": name, "passed": bool(passed), "detail": detail})
    print(f"[{'PASS' if passed else 'FAIL'}] {name}: {detail}")

def main():
    draft = json.loads((OUT_DIR / "related_words_draft.json").read_text(encoding="utf-8"))
    review = json.loads((OUT_DIR / "related_words_review.json").read_text(encoding="utf-8"))
    changes = draft["changes"]

    per_level_production = {}
    all_production = {}
    for lvl in LEVELS:
        path = REPO_ROOT / "data" / "hsk" / f"hsk{lvl}" / f"hsk{lvl}_vocabulary_production.json"
        recs = json.loads(path.read_text(encoding="utf-8"))
        per_level_production[lvl] = recs
        for r in recs:
            all_production[r["id"]] = r

    # A. every target ID exists
    broken = []
    for c in changes:
        for t in c["newRelatedWordIds"]:
            if t not in all_production:
                broken.append((c["id"], t))
    check("A_no_broken_ids", len(broken) == 0, f"{broken[:5]}")

    # B. no self-references
    self_refs = [c["id"] for c in changes if c["id"] in c["newRelatedWordIds"]]
    check("B_no_self_references", len(self_refs) == 0, f"{self_refs[:5]}")

    # C. no duplicate IDs inside a record
    dup_inside = [c["id"] for c in changes if len(c["newRelatedWordIds"]) != len(set(c["newRelatedWordIds"]))]
    check("C_no_duplicate_ids_within_record", len(dup_inside) == 0, f"{dup_inside[:5]}")

    # D. every record with pre-existing non-empty relatedWordIds is untouched
    changed_ids = {c["id"] for c in changes}
    current_nonempty_ids = {r["id"] for lvl in LEVELS for r in per_level_production[lvl] if r.get("relatedWordIds")}
    overlap = changed_ids & current_nonempty_ids
    check("D_existing_nonempty_never_in_changeset", len(overlap) == 0, f"{list(overlap)[:5]}")
    for c in changes:
        if c["oldRelatedWordIds"]:
            check(f"D_old_value_was_empty_for_{c['id']}", False, "old value was non-empty but appears in changeset")
    check("D_all_changes_have_empty_old_value", all(not c["oldRelatedWordIds"] for c in changes), "")

    # E. 0 needs_review relationships enter the draft
    check("E_no_needs_review_in_draft", all(c["selectionStatus"] == "selected" for c in changes), "")

    # F. every new edge has a valid selectionReasons/source record
    missing_reason = [c["id"] for c in changes if not c.get("selectionReasons") or not c.get("sourceFile")]
    check("F_every_change_has_reasons_and_source", len(missing_reason) == 0, f"{missing_reason[:5]}")
    # each reason entry must have a non-empty candidateId+reason and correspond 1:1 to newRelatedWordIds
    reason_mismatch = []
    for c in changes:
        reason_ids = [r["candidateId"] for r in c["selectionReasons"]]
        if reason_ids != c["newRelatedWordIds"]:
            reason_mismatch.append(c["id"])
    check("F_reasons_align_with_target_ids", len(reason_mismatch) == 0, f"{reason_mismatch[:5]}")

    # G. exactly 5400 records remain (production untouched by this validator; sanity check on universe)
    total_production = sum(len(per_level_production[lvl]) for lvl in LEVELS)
    check("G_5400_records_total", total_production == 5400, f"{total_production}")

    # HSK6 must be completely absent from the changeset
    hsk6_touched = [c["id"] for c in changes if c["hskLevel"] == 6]
    check("HSK6_never_touched", len(hsk6_touched) == 0, f"{hsk6_touched[:5]}")

    # I. data scope -- the draft itself only ever proposes relatedWordIds; structurally guaranteed by
    # the builder (it emits only id/word/hskLevel/old/new/added*/reasons/source/status fields, never
    # touching any other production field), reconfirmed here by checking the draft's own key set.
    allowed_keys = {"id","word","hskLevel","oldRelatedWordIds","newRelatedWordIds","addedIds",
                    "addedWords","addedHskLevels","selectionReasons","sourceFile","selectionStatus"}
    key_violations = [c["id"] for c in changes if not set(c.keys()) <= allowed_keys]
    check("I_draft_scope_relatedWordIds_only", len(key_violations) == 0, f"{key_violations[:5]}")

    total_checks = len(checks)
    passed_checks = sum(1 for c_ in checks if c_["passed"])
    print(f"\nallChecksPassed: {passed_checks == total_checks}")
    print(f"checksTotal: {total_checks}  checksPassed: {passed_checks}")

    report = {"checksTotal": total_checks, "checksPassed": passed_checks,
              "allChecksPassed": passed_checks == total_checks, "checks": checks}
    (OUT_DIR / "draft_validation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if passed_checks == total_checks else 1

if __name__ == "__main__":
    sys.exit(main())
