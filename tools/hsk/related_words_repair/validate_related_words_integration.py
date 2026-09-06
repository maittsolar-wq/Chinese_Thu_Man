"""
Related Words Pass 02 -- production integration validator.

Compares the git-committed pre-integration state (HEAD, i.e. commit
c540cc2) against the CURRENT on-disk production state, and against the
approved draft, to prove:

  - only `relatedWordIds` changed, for exactly 901 records
  - every changed record's new value matches the approved draft exactly
  - every record that already had non-empty relatedWordIds is untouched
  - HSK6 is completely untouched
  - strokeCount, examples, humanVerified, groundTruth, verificationStatus,
    characterIds, word, pinyin, meaningVi are all unchanged everywhere
  - no broken IDs, no self-references, no duplicate edges, no duplicate
    production records introduced

Read-only. Writes only its own report file.
"""
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent
LEVELS = [1, 2, 3, 4, 5, 6]
BASELINE_COMMIT = "c540cc27863cb1a045f5cc2a3cc1e3c594823fdf"

PRESERVED_FIELDS = [
    "id", "word", "pinyin", "meaningVi", "examples", "strokeCount",
    "humanVerified", "groundTruth", "verificationStatus", "characterIds",
]

checks = []

def check(name, passed, detail=""):
    checks.append({"name": name, "passed": bool(passed), "detail": detail})
    print(f"[{'PASS' if passed else 'FAIL'}] {name}: {detail}")

def git_show(commit: str, path: str) -> str:
    result = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=REPO_ROOT,
                             capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(f"git show failed for {path}: {result.stderr}")
    return result.stdout

def main():
    draft = json.loads((Path(__file__).resolve().parent / "related_words_draft.json").read_text(encoding="utf-8"))
    draft_by_id = {c["id"]: c["newRelatedWordIds"] for c in draft["changes"]}

    before_by_level = {}
    after_by_level = {}
    for lvl in LEVELS:
        rel = f"data/hsk/hsk{lvl}/hsk{lvl}_vocabulary_production.json"
        before_by_level[lvl] = json.loads(git_show(BASELINE_COMMIT, rel))
        after_by_level[lvl] = json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))

    before_by_id = {r["id"]: r for lvl in LEVELS for r in before_by_level[lvl]}
    after_by_id = {r["id"]: r for lvl in LEVELS for r in after_by_level[lvl]}

    check("record_count_before_5400", len(before_by_id) == 5400, f"{len(before_by_id)}")
    check("record_count_after_5400", len(after_by_id) == 5400, f"{len(after_by_id)}")
    check("id_set_identical", set(before_by_id) == set(after_by_id), "")

    # only relatedWordIds changed, exactly for the draft's 901 ids
    relatedWordIds_diffs = []
    other_field_diffs = []
    for rid, before in before_by_id.items():
        after = after_by_id[rid]
        if before.get("relatedWordIds") != after.get("relatedWordIds"):
            relatedWordIds_diffs.append(rid)
        for field in set(before.keys()) | set(after.keys()):
            if field == "relatedWordIds":
                continue
            if before.get(field) != after.get(field):
                other_field_diffs.append((rid, field))

    check("changed_field_is_only_relatedWordIds", len(other_field_diffs) == 0, f"{other_field_diffs[:5]}")
    check("exactly_901_records_changed", len(relatedWordIds_diffs) == 901, f"{len(relatedWordIds_diffs)}")
    check("changed_ids_match_draft_exactly", set(relatedWordIds_diffs) == set(draft_by_id.keys()),
          f"diff={set(relatedWordIds_diffs).symmetric_difference(draft_by_id.keys())}")

    # every changed record matches the approved draft value exactly
    mismatches = [rid for rid in relatedWordIds_diffs if after_by_id[rid].get("relatedWordIds") != draft_by_id.get(rid)]
    check("draft_parity_exact", len(mismatches) == 0, f"{mismatches[:5]}")

    # every record that already had non-empty relatedWordIds is untouched
    preexisting_nonempty = [rid for rid, r in before_by_id.items() if r.get("relatedWordIds")]
    touched_preexisting = [rid for rid in preexisting_nonempty if before_by_id[rid].get("relatedWordIds") != after_by_id[rid].get("relatedWordIds")]
    check("preexisting_nonempty_untouched", len(touched_preexisting) == 0, f"{touched_preexisting[:5]}")

    # HSK6 completely untouched
    hsk6_diffs = [r["id"] for r in before_by_level[6] if r != after_by_id[r["id"]]]
    check("hsk6_completely_untouched", len(hsk6_diffs) == 0, f"{hsk6_diffs[:5]}")

    # preserved fields
    field_diffs_detail = {f: 0 for f in PRESERVED_FIELDS}
    for rid, before in before_by_id.items():
        after = after_by_id[rid]
        for field in PRESERVED_FIELDS:
            if before.get(field) != after.get(field):
                field_diffs_detail[field] += 1
    for field, count in field_diffs_detail.items():
        check(f"preserved_{field}", count == 0, f"diffs={count}")

    # broken IDs / self-refs / duplicate edges in the FULL current dataset
    broken = []
    self_refs = []
    dup_edges = []
    for rid, r in after_by_id.items():
        rel = r.get("relatedWordIds") or []
        if len(rel) != len(set(rel)):
            dup_edges.append(rid)
        for t in rel:
            if t == rid:
                self_refs.append(rid)
            if t not in after_by_id:
                broken.append((rid, t))
    check("no_broken_ids_full_dataset", len(broken) == 0, f"{broken[:5]}")
    check("no_self_references_full_dataset", len(self_refs) == 0, f"{self_refs[:5]}")
    check("no_duplicate_edges_within_record_full_dataset", len(dup_edges) == 0, f"{dup_edges[:5]}")

    # no duplicate production records (id uniqueness per file)
    dup_ids_per_file = []
    for lvl in LEVELS:
        ids = [r["id"] for r in after_by_level[lvl]]
        if len(ids) != len(set(ids)):
            dup_ids_per_file.append(lvl)
    check("no_duplicate_production_records", len(dup_ids_per_file) == 0, f"{dup_ids_per_file}")

    total_checks = len(checks)
    passed_checks = sum(1 for c in checks if c["passed"])
    print(f"\nallChecksPassed: {passed_checks == total_checks}")
    print(f"checksTotal: {total_checks}  checksPassed: {passed_checks}")

    report = {"checksTotal": total_checks, "checksPassed": passed_checks,
              "allChecksPassed": passed_checks == total_checks, "checks": checks}
    (OUT_DIR / "integration_validation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if passed_checks == total_checks else 1

if __name__ == "__main__":
    sys.exit(main())
