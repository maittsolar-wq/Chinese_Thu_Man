"""P5.6.5 -- Post-integration validation for the HSK2 related-word
production merge. Read-only: writes exactly one new file,
tools/hsk/hsk2_related_words_p565_integration_report.json. Never
modifies the refined artifact, the selection, the candidate pool, or
any production file. Mirrors
tools/hsk/validate_hsk1_related_words_p55_integration.py, extended
with the additional needs_review/target-distribution/idempotency
checks this task specifically requires.
"""

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "tools" / "hsk" / "hsk2_related_words_refined_selection.json"
BEFORE_SNAPSHOT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk2_production_p565_before_snapshot.json"
PRODUCTION_PATH = REPO_ROOT / "data" / "hsk" / "hsk2" / "hsk2_vocabulary_production.json"
REPORT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk2_related_words_p565_integration_report.json"
MERGE_SCRIPT_PATH = REPO_ROOT / "tools" / "hsk" / "merge_hsk2_related_words_p565.py"

CANDIDATE_POOL_PATH = REPO_ROOT / "tools" / "hsk" / "hsk2_related_words_candidate_pool.json"
SELECTION_PATH = REPO_ROOT / "tools" / "hsk" / "hsk2_related_words_selection.json"

OTHER_LEVEL_PRODUCTION_PATHS = {
    n: REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
    for n in (1, 3, 4, 5, 6)
}
APPROVED_HSK1_ARTIFACTS = [
    "tools/hsk/hsk1_related_words_candidate_pool.json",
    "tools/hsk/hsk1_related_words_selection.json",
    "tools/hsk/hsk1_related_words_refined_selection.json",
    "tools/hsk/hsk1_related_words_final_validation_p544.json",
]
APPROVED_HSK6_ARTIFACTS = [
    "tools/hsk/hsk6_related_words_selection.json",
    "tools/hsk/hsk6_related_words_validation_report.json",
    "tools/hsk/hsk6_related_words_refinement_report.json",
]

EXPECTED_PRODUCTION_RECORDS = 200
EXPECTED_SELECTED = 198
EXPECTED_NEEDS_REVIEW = 2
EXPECTED_SELECTED_RELATIONSHIPS = 327
NEEDS_REVIEW_IDS = {"hsk2_067", "hsk2_044"}
HIGH_COUNT_EXPECTED = {
    "hsk2_018": 7, "hsk2_048": 7, "hsk2_061": 7, "hsk2_072": 7,
    "hsk2_103": 7, "hsk2_118": 7, "hsk2_125": 6, "hsk2_158": 6,
}

# Reference hashes captured at the start of P5.6.5 (matching P5.6.4's
# own independently-confirmed values) for the 3 untracked P5.6.x
# artifacts that have no HEAD git blob to diff against (they are not
# yet committed). git hash-object vs `git rev-parse HEAD:<path>` is the
# right technique for tracked files (used throughout this script for
# HSK1/3-6 production and the approved HSK1/HSK6 artifacts) but
# necessarily reports a false "changed" for an untracked file since
# there is no HEAD blob at all -- these three "unchanged" checks
# instead compare the current on-disk hash directly against the value
# confirmed identical in the P5.6.4 final validation report.
REFERENCE_HASHES = {
    "tools/hsk/hsk2_related_words_candidate_pool.json": "e8e809a6b7c33cc4f22f509489faefd5089b3f3fa2295f81f16d650c48a9dd8b",
    "tools/hsk/hsk2_related_words_selection.json": "dacf0a5431e31f76369741d5f352406dde635a35fc70efd3a4edcec046795910",
    "tools/hsk/hsk2_related_words_refined_selection.json": "4ee26cff6152faaa3201eb73a29622caf943553abf212dad9b7d1edd16ed058c",
}


def load_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def unchanged_via_git(relpath: str) -> bool:
    working = git("hash-object", relpath)
    try:
        committed = git("rev-parse", f"HEAD:{relpath}")
    except subprocess.CalledProcessError:
        return False
    return working == committed


def main() -> None:
    if REPORT_PATH.exists():
        raise SystemExit(f"FAIL: {REPORT_PATH} already exists -- refusing to overwrite.")

    checks: dict[str, dict] = {}
    all_passed = True

    def record(name: str, passed: bool, detail) -> None:
        nonlocal all_passed
        checks[name] = {"passed": bool(passed), "detail": detail}
        if not passed:
            all_passed = False

    source_text = load_text(SOURCE_PATH)
    source_doc = json.loads(source_text)
    source_records = {r["sourceId"]: r for r in source_doc["records"]}
    candidate_pool_text = load_text(CANDIDATE_POOL_PATH)
    selection_text = load_text(SELECTION_PATH)

    before_snapshot = json.loads(load_text(BEFORE_SNAPSHOT_PATH))

    production_text = load_text(PRODUCTION_PATH)
    production_records = json.loads(production_text)
    production_by_id = {r["id"]: r for r in production_records}

    universe_ids = set()
    universe_level = {}
    universe_ids.update(production_by_id.keys())
    for r in production_records:
        universe_level[r["id"]] = 2
    for n, p in OTHER_LEVEL_PRODUCTION_PATHS.items():
        for r in json.loads(load_text(p)):
            universe_ids.add(r["id"])
            universe_level[r["id"]] = n

    # 1. source count
    record("check1_source_count_200", len(source_records) == 200, len(source_records))

    # 2. production count
    record("check2_production_count_200", len(production_records) == EXPECTED_PRODUCTION_RECORDS, len(production_records))

    # 3. selected count
    selected_src_ids = {sid for sid, r in source_records.items() if r["status"] == "selected"}
    record("check3_selected_count_198", len(selected_src_ids) == EXPECTED_SELECTED, len(selected_src_ids))

    # 4. needs_review count
    needs_review_src_ids = {sid for sid, r in source_records.items() if r["status"] == "needs_review"}
    record("check4_needs_review_count_2", len(needs_review_src_ids) == EXPECTED_NEEDS_REVIEW, len(needs_review_src_ids))
    record("check4b_needs_review_ids_correct", needs_review_src_ids == NEEDS_REVIEW_IDS, sorted(needs_review_src_ids))

    # 5. integrated relationship count
    total_relationships_in_production = sum(len(r.get("relatedWordIds") or []) for r in production_records)
    record("check5_integrated_relationship_count_327", total_relationships_in_production == EXPECTED_SELECTED_RELATIONSHIPS,
           total_relationships_in_production)

    # 6. target existence
    unknown_targets = []
    for r in production_records:
        for t in r.get("relatedWordIds") or []:
            if t not in universe_ids:
                unknown_targets.append((r["id"], t))
    record("check6_all_targets_exist", len(unknown_targets) == 0, unknown_targets[:10])

    # 7. duplicate relatedWordIds
    dupe_records = [r["id"] for r in production_records
                     if len(r.get("relatedWordIds") or []) != len(set(r.get("relatedWordIds") or []))]
    record("check7_no_duplicate_related_word_ids", len(dupe_records) == 0, dupe_records[:10])

    # 8. self references
    self_refs = [r["id"] for r in production_records if r["id"] in (r.get("relatedWordIds") or [])]
    record("check8_no_self_references", len(self_refs) == 0, self_refs[:10])

    # 9. needs_review exclusion
    needs_review_with_data = [sid for sid in needs_review_src_ids if (production_by_id[sid].get("relatedWordIds") or [])]
    record("check9_needs_review_excluded", len(needs_review_with_data) == 0, needs_review_with_data)

    # 10. exact source->target equality (only for selected records)
    mismatched = []
    for sid in selected_src_ids:
        expected_value = source_records[sid].get("selectedRelatedWordIds") or []
        actual_value = production_by_id[sid].get("relatedWordIds") or []
        if expected_value != actual_value:
            mismatched.append(sid)
    non_selected_with_data = [
        r["id"] for r in production_records
        if r["id"] not in selected_src_ids and (r.get("relatedWordIds") or [])
    ]
    record("check10a_selected_records_exactly_match_source", len(mismatched) == 0, mismatched[:10])
    record("check10b_only_selected_records_have_data", len(non_selected_with_data) == 0, non_selected_with_data[:10])

    # 11. target HSK distribution
    level_dist = {n: 0 for n in range(1, 7)}
    for r in production_records:
        for t in r.get("relatedWordIds") or []:
            lvl = universe_level.get(t)
            if lvl in level_dist:
                level_dist[lvl] += 1
    # NOTE: 45/229/53 (327 total), not the refined artifact's own
    # 46/231/53 (330 total) -- the 3-relationship difference is exactly
    # the 2 needs_review records' own relationships (jiao1(hsk2_067)
    # -> jiao4shi4(hsk2_068, HSK2) and -> xue2(hsk1_247, HSK1);
    # ge4zi(hsk2_044) -> gao1(hsk2_041, HSK2)), which are correctly
    # withheld from production per the mandatory needs_review exclusion
    # rule. This is the expected, required consequence of check9
    # passing, not a discrepancy -- see the P5.6.5 report.
    expected_level_dist = {1: 45, 2: 229, 3: 53, 4: 0, 5: 0, 6: 0}
    record("check11_target_level_distribution", level_dist == expected_level_dist,
           {"expected": expected_level_dist, "actual": level_dist})

    # 12. no unrelated field changes -- reconstruct "before" by zeroing
    # relatedWordIds on every current record and comparing to the
    # recorded before-snapshot hash (identical technique to P5.5).
    reconstructed_before = []
    for r in production_records:
        r2 = dict(r)
        r2["relatedWordIds"] = []
        reconstructed_before.append(r2)
    reconstructed_before_by_id = {r["id"]: r for r in reconstructed_before}
    reconstructed_before_ordered = [reconstructed_before_by_id[i] for i in before_snapshot["recordIds"]]
    reconstructed_text = json.dumps(reconstructed_before_ordered, indent=2, ensure_ascii=False).replace("\n", "\r\n")
    reconstructed_hash = sha256_of(reconstructed_text)
    record("check12_no_unexpected_field_changes", reconstructed_hash == before_snapshot["targetSha256"],
           {"reconstructed": reconstructed_hash, "before_snapshot": before_snapshot["targetSha256"]})

    # 13. HSK1-6 protection (HSK2 production is the one INTENDED change;
    # HSK1/3/4/5/6 must be untouched)
    other_level_unchanged = {}
    for n, p in OTHER_LEVEL_PRODUCTION_PATHS.items():
        relpath = str(p.relative_to(REPO_ROOT)).replace("\\", "/")
        other_level_unchanged[f"hsk{n}"] = unchanged_via_git(relpath)
    record("check13_hsk1_3_4_5_6_production_unchanged", all(other_level_unchanged.values()), other_level_unchanged)

    hsk1_artifact_status = {p: unchanged_via_git(p) for p in APPROVED_HSK1_ARTIFACTS}
    hsk6_artifact_status = {p: unchanged_via_git(p) for p in APPROVED_HSK6_ARTIFACTS}
    record("check13b_hsk1_approved_artifacts_unchanged", all(hsk1_artifact_status.values()), hsk1_artifact_status)
    record("check13c_hsk6_approved_artifacts_unchanged", all(hsk6_artifact_status.values()), hsk6_artifact_status)

    # candidate pool / selection / refined artifact are untracked P5.6.x
    # files with no HEAD blob -- verified via direct hash comparison
    # against the P5.6.4-confirmed reference values instead (see
    # REFERENCE_HASHES comment above).
    candidate_pool_hash_now = sha256_of(candidate_pool_text)
    selection_hash_now = sha256_of(selection_text)
    refined_hash_now = sha256_of(source_text)
    record("check13d_hsk2_candidate_pool_unchanged",
           candidate_pool_hash_now == REFERENCE_HASHES["tools/hsk/hsk2_related_words_candidate_pool.json"],
           {"current": candidate_pool_hash_now, "reference": REFERENCE_HASHES["tools/hsk/hsk2_related_words_candidate_pool.json"]})
    record("check13e_hsk2_selection_unchanged",
           selection_hash_now == REFERENCE_HASHES["tools/hsk/hsk2_related_words_selection.json"],
           {"current": selection_hash_now, "reference": REFERENCE_HASHES["tools/hsk/hsk2_related_words_selection.json"]})
    record("check13f_hsk2_refined_selection_unchanged",
           refined_hash_now == REFERENCE_HASHES["tools/hsk/hsk2_related_words_refined_selection.json"],
           {"current": refined_hash_now, "reference": REFERENCE_HASHES["tools/hsk/hsk2_related_words_refined_selection.json"]})

    # 14. app/src protection
    app_src_status = subprocess.run(
        ["git", "status", "--porcelain", "--", "app/src"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    record("check14_app_src_unchanged", app_src_status.strip() == "", app_src_status.strip() or "(clean)")

    # 15. idempotency: run the merge script's own --dry-run subprocess
    # and confirm to_add=0, conflicts=0 against the CURRENT (already
    # merged) production file.
    dry_run = subprocess.run(
        ["python", str(MERGE_SCRIPT_PATH), "--dry-run"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    dry_run_output = dry_run.stdout
    idempotent_to_add_zero = "records that would change (add relatedWordIds): 0" in dry_run_output
    idempotent_conflicts_zero = "conflicts (existing relatedWordIds differs from source): 0" in dry_run_output
    record("check15_idempotent_dry_run", dry_run.returncode == 0 and idempotent_to_add_zero and idempotent_conflicts_zero,
           {"returncode": dry_run.returncode, "to_add_zero": idempotent_to_add_zero, "conflicts_zero": idempotent_conflicts_zero})

    # 16. provenance/hash match: production's currently-integrated values
    # trace exactly back to the refined artifact's own recorded hashes.
    actual_source_hash = sha256_of(source_text)
    record("check16a_refined_artifact_selectionHash_matches_selection_file",
           source_doc.get("selectionArtifactHash") == sha256_of(selection_text),
           {"recorded": source_doc.get("selectionArtifactHash"), "actual": sha256_of(selection_text)})
    record("check16b_refined_artifact_poolHash_matches_pool_file",
           source_doc.get("candidatePoolHash") == sha256_of(candidate_pool_text),
           {"recorded": source_doc.get("candidatePoolHash"), "actual": sha256_of(candidate_pool_text)})

    print("=== P5.6.5 post-integration validation ===")
    for name, result in checks.items():
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {name}: {result['detail']}")
    print()
    print(f"allChecksPassed: {all_passed}")

    after_hash = sha256_of(production_text)

    report = {
        "reportLabel": "P5.6.5 HSK2 RELATED-WORD PRODUCTION INTEGRATION REPORT",
        "timestampUtc": datetime.now(timezone.utc).isoformat(),
        "baselineCommit": "95c58e71faf48081d29ff3982659120f2edc9d2c",
        "sourceArtifact": {
            "path": "tools/hsk/hsk2_related_words_refined_selection.json",
            "sha256": actual_source_hash,
            "modifiedByThisPhase": False,
        },
        "productionTarget": {
            "path": "data/hsk/hsk2/hsk2_vocabulary_production.json",
            "sha256Before": before_snapshot["targetSha256"],
            "sha256After": after_hash,
            "recordCountBefore": before_snapshot["recordCount"],
            "recordCountAfter": len(production_records),
        },
        "mergeContract": {
            "rule": "For each source record where status == 'selected', set production_record.relatedWordIds = source_record.selectedRelatedWordIds, matched by production.id == source.sourceId. needs_review records receive no relatedWordIds. No other field on any record is modified.",
            "selectedRecordsIntegrated": len(selected_src_ids),
            "needsReviewRecordsIntegrated": 0,
            "relationshipsIntegrated": total_relationships_in_production,
        },
        "mergeResult": {
            "recordsWithNonEmptyRelatedWordIds": sum(1 for r in production_records if r.get("relatedWordIds")),
            "recordsChangedFromEmpty": 162,
            "recordsSelectedButLegitimatelyEmpty": 36,
            "recordsUnchangedNeedsReview": EXPECTED_NEEDS_REVIEW,
            "relationshipsAdded": total_relationships_in_production,
        },
        "checks": checks,
        "allChecksPassed": all_passed,
    }
    with open(REPORT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWrote {REPORT_PATH}")

    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
