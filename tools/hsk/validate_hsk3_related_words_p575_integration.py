"""P5.7.5 -- Post-integration validation for the HSK3 related-word
production merge. Read-only: writes exactly one new file,
tools/hsk/hsk3_related_words_p575_integration_report.json. Never
modifies the refined artifact, the selection, the candidate pool, or
any production file. Mirrors
tools/hsk/validate_hsk3_related_words_p565_integration.py (HSK2's own
P5.6.5 validator).
"""

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "tools" / "hsk" / "hsk3_related_words_refined_selection.json"
BEFORE_SNAPSHOT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk3_production_p575_before_snapshot.json"
PRODUCTION_PATH = REPO_ROOT / "data" / "hsk" / "hsk3" / "hsk3_vocabulary_production.json"
REPORT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk3_related_words_p575_integration_report.json"
MERGE_SCRIPT_PATH = REPO_ROOT / "tools" / "hsk" / "merge_hsk3_related_words_p575.py"

CANDIDATE_POOL_PATH = REPO_ROOT / "tools" / "hsk" / "hsk3_related_words_candidate_pool.json"
SELECTION_PATH = REPO_ROOT / "tools" / "hsk" / "hsk3_related_words_selection.json"

OTHER_LEVEL_PRODUCTION_PATHS = {
    n: REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
    for n in (1, 2, 4, 5, 6)
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
HSK2_PIPELINE_REFERENCE_HASHES = {
    "tools/hsk/hsk2_related_words_candidate_pool.json": "e8e809a6b7c33cc4f22f509489faefd5089b3f3fa2295f81f16d650c48a9dd8b",
    "tools/hsk/hsk2_related_words_selection.json": "dacf0a5431e31f76369741d5f352406dde635a35fc70efd3a4edcec046795910",
    "tools/hsk/hsk2_related_words_refined_selection.json": "4ee26cff6152faaa3201eb73a29622caf943553abf212dad9b7d1edd16ed058c",
    "data/hsk/hsk2/hsk2_vocabulary_production.json": None,  # checked via git, not hash reference
}

EXPECTED_PRODUCTION_RECORDS = 500
EXPECTED_SELECTED = 494
EXPECTED_NEEDS_REVIEW = 6
NEEDS_REVIEW_IDS = {"hsk3_030", "hsk3_115", "hsk3_139", "hsk3_159", "hsk3_210", "hsk3_403"}
PROMOTED_IDS = {"hsk3_234", "hsk3_347"}
HIGH_COUNT_EXPECTED = {"hsk3_017": 6, "hsk3_097": 6, "hsk3_181": 5, "hsk3_274": 6, "hsk3_380": 6}


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
        universe_level[r["id"]] = 3
    for n, p in OTHER_LEVEL_PRODUCTION_PATHS.items():
        for r in json.loads(load_text(p)):
            universe_ids.add(r["id"])
            universe_level[r["id"]] = n

    # 1. 500 production records
    record("check1_production_500", len(production_records) == EXPECTED_PRODUCTION_RECORDS, len(production_records))
    # 2. 500 refined source records
    record("check2_refined_source_500", len(source_records) == 500, len(source_records))

    # 3. selected count
    selected_src_ids = {sid for sid, r in source_records.items() if r["status"] == "selected"}
    record("check3_selected_count_494", len(selected_src_ids) == EXPECTED_SELECTED, len(selected_src_ids))

    # 4. needs_review count
    needs_review_src_ids = {sid for sid, r in source_records.items() if r["status"] == "needs_review"}
    record("check4_needs_review_count_6", len(needs_review_src_ids) == EXPECTED_NEEDS_REVIEW, len(needs_review_src_ids))
    record("check4b_needs_review_ids_correct", needs_review_src_ids == NEEDS_REVIEW_IDS, sorted(needs_review_src_ids))

    # 5. total refined relationships
    total_refined = sum(len(r.get("selectedRelatedWordIds") or []) for r in source_records.values())
    record("check5_total_refined_275", total_refined == 275, total_refined)

    # 6. selected relationship count / 7. needs_review relationship count
    selected_rel_count = sum(len(source_records[sid].get("selectedRelatedWordIds") or []) for sid in selected_src_ids)
    needs_review_rel_count = sum(len(source_records[sid].get("selectedRelatedWordIds") or []) for sid in needs_review_src_ids)
    record("check6_selected_relationships_267", selected_rel_count == 267, selected_rel_count)
    record("check7_needs_review_relationships_8", needs_review_rel_count == 8, needs_review_rel_count)
    record("check7b_arithmetic_reconciles", selected_rel_count + needs_review_rel_count == total_refined,
           f"{selected_rel_count}+{needs_review_rel_count}={selected_rel_count + needs_review_rel_count} vs total={total_refined}")

    # 8. exact production integrated count
    total_relationships_in_production = sum(len(r.get("relatedWordIds") or []) for r in production_records)
    record("check8_production_integrated_267", total_relationships_in_production == selected_rel_count,
           {"production": total_relationships_in_production, "expected": selected_rel_count})

    # 9. exact source->target mapping (only for selected records)
    mismatched = []
    for sid in selected_src_ids:
        expected_value = source_records[sid].get("selectedRelatedWordIds") or []
        actual_value = production_by_id[sid].get("relatedWordIds") or []
        if expected_value != actual_value:
            mismatched.append(sid)
    record("check9_source_target_mapping_exact", len(mismatched) == 0, mismatched[:10])

    # 10. target existence
    unknown_targets = []
    for r in production_records:
        for t in r.get("relatedWordIds") or []:
            if t not in universe_ids:
                unknown_targets.append((r["id"], t))
    record("check10_target_existence", len(unknown_targets) == 0, unknown_targets[:10])

    # 11. no fabricated IDs (derived from check10 + check9)
    record("check11_no_fabricated_ids", len(unknown_targets) == 0 and len(mismatched) == 0, "derived")

    # 12. no self references
    self_refs = [r["id"] for r in production_records if r["id"] in (r.get("relatedWordIds") or [])]
    record("check12_no_self_references", len(self_refs) == 0, self_refs[:10])

    # 13. no duplicate relatedWordIds
    dupe_records = [r["id"] for r in production_records
                     if len(r.get("relatedWordIds") or []) != len(set(r.get("relatedWordIds") or []))]
    record("check13_no_duplicate_related_word_ids", len(dupe_records) == 0, dupe_records[:10])

    # 14. needs_review exclusion
    needs_review_with_data = [sid for sid in needs_review_src_ids if (production_by_id[sid].get("relatedWordIds") or [])]
    record("check14_needs_review_excluded", len(needs_review_with_data) == 0, needs_review_with_data)
    non_selected_non_review_with_data = [
        r["id"] for r in production_records
        if r["id"] not in selected_src_ids and r["id"] not in needs_review_src_ids and (r.get("relatedWordIds") or [])
    ]
    record("check14b_only_selected_have_data", len(non_selected_non_review_with_data) == 0, non_selected_non_review_with_data[:10])

    # 15. promoted-record integration
    promoted_ok = {}
    for sid in PROMOTED_IDS:
        expected = source_records[sid].get("selectedRelatedWordIds") or []
        actual = production_by_id[sid].get("relatedWordIds") or []
        promoted_ok[sid] = (source_records[sid]["status"] == "selected") and (expected == actual) and (len(actual) > 0)
    record("check15_promoted_records_integrated", all(promoted_ok.values()), promoted_ok)

    # 16. target HSK distribution (refined total, excluded needs_review, actual production)
    refined_level_dist = {n: 0 for n in range(1, 7)}
    for r in source_records.values():
        for t in r.get("selectedRelatedWordIds") or []:
            lvl = universe_level.get(t)
            if lvl in refined_level_dist:
                refined_level_dist[lvl] += 1
    excluded_level_dist = {n: 0 for n in range(1, 7)}
    for sid in needs_review_src_ids:
        for t in source_records[sid].get("selectedRelatedWordIds") or []:
            lvl = universe_level.get(t)
            if lvl in excluded_level_dist:
                excluded_level_dist[lvl] += 1
    production_level_dist = {n: 0 for n in range(1, 7)}
    for r in production_records:
        for t in r.get("relatedWordIds") or []:
            lvl = universe_level.get(t)
            if lvl in production_level_dist:
                production_level_dist[lvl] += 1
    reconciled = all(
        refined_level_dist[n] - excluded_level_dist[n] == production_level_dist[n] for n in range(1, 7)
    )
    record("check16_target_distribution_reconciles", reconciled,
           {"refined": refined_level_dist, "excludedNeedsReview": excluded_level_dist, "production": production_level_dist})

    # 17. non-relatedWordIds field preservation
    reconstructed_before = []
    for r in production_records:
        r2 = dict(r)
        r2["relatedWordIds"] = []
        reconstructed_before.append(r2)
    reconstructed_before_by_id = {r["id"]: r for r in reconstructed_before}
    reconstructed_before_ordered = [reconstructed_before_by_id[i] for i in before_snapshot["recordIds"]]
    reconstructed_text = json.dumps(reconstructed_before_ordered, indent=2, ensure_ascii=False).replace("\n", "\r\n")
    reconstructed_hash = sha256_of(reconstructed_text)
    record("check17_non_related_field_preservation", reconstructed_hash == before_snapshot["targetSha256"],
           {"reconstructed": reconstructed_hash, "before_snapshot": before_snapshot["targetSha256"]})

    # 18/19/20. HSK1/HSK2/HSK4-6 protection
    hsk1_2_status = {}
    for n in (1, 2):
        relpath = str(OTHER_LEVEL_PRODUCTION_PATHS[n].relative_to(REPO_ROOT)).replace("\\", "/")
        hsk1_2_status[f"hsk{n}"] = unchanged_via_git(relpath)
    record("check18_19_hsk1_hsk2_production_unchanged", all(hsk1_2_status.values()), hsk1_2_status)

    hsk456_status = {}
    for n in (4, 5, 6):
        relpath = str(OTHER_LEVEL_PRODUCTION_PATHS[n].relative_to(REPO_ROOT)).replace("\\", "/")
        hsk456_status[f"hsk{n}"] = unchanged_via_git(relpath)
    record("check20_hsk4_5_6_production_unchanged", all(hsk456_status.values()), hsk456_status)

    hsk1_artifact_status = {p: unchanged_via_git(p) for p in APPROVED_HSK1_ARTIFACTS}
    hsk6_artifact_status = {p: unchanged_via_git(p) for p in APPROVED_HSK6_ARTIFACTS}
    record("hsk1_approved_artifacts_unchanged", all(hsk1_artifact_status.values()), hsk1_artifact_status)
    record("hsk6_approved_artifacts_unchanged", all(hsk6_artifact_status.values()), hsk6_artifact_status)

    hsk2_pipeline_status = {}
    for relpath, expected_hash in HSK2_PIPELINE_REFERENCE_HASHES.items():
        if expected_hash is None:
            continue
        actual = sha256_of(load_text(REPO_ROOT / relpath))
        hsk2_pipeline_status[relpath] = actual == expected_hash
    record("hsk2_completed_pipeline_unchanged", all(hsk2_pipeline_status.values()), hsk2_pipeline_status)

    candidate_pool_hash_now = sha256_of(candidate_pool_text)
    selection_hash_now = sha256_of(selection_text)
    refined_hash_now = sha256_of(source_text)
    REFERENCE_HASHES = {
        "tools/hsk/hsk3_related_words_candidate_pool.json": "67883077985d19319e1eabd6cfe40c47198df6a37d85edb3a8fc3a7847d25a27",
        "tools/hsk/hsk3_related_words_selection.json": "180816261bfc4be57a210f3665f4a2b63e63b353acd7482b48d819e8fa7f15f9",
    }
    record("check_hsk3_candidate_pool_unchanged", candidate_pool_hash_now == REFERENCE_HASHES["tools/hsk/hsk3_related_words_candidate_pool.json"],
           {"current": candidate_pool_hash_now, "reference": REFERENCE_HASHES["tools/hsk/hsk3_related_words_candidate_pool.json"]})
    record("check_hsk3_selection_unchanged", selection_hash_now == REFERENCE_HASHES["tools/hsk/hsk3_related_words_selection.json"],
           {"current": selection_hash_now, "reference": REFERENCE_HASHES["tools/hsk/hsk3_related_words_selection.json"]})

    # 21. HSK3 source-field preservation (same as check17, restated for the report item numbering)
    record("check21_hsk3_source_field_preservation", reconstructed_hash == before_snapshot["targetSha256"], "same as check17")

    # 22. app/src protection
    app_src_status = subprocess.run(
        ["git", "status", "--porcelain", "--", "app/src"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    record("check22_app_src_unchanged", app_src_status.strip() == "", app_src_status.strip() or "(clean)")

    # 23. refined artifact hash/provenance
    record("check23a_refined_selectionHash_matches_selection_file",
           source_doc.get("selectionArtifactHash") == sha256_of(selection_text),
           {"recorded": source_doc.get("selectionArtifactHash"), "actual": sha256_of(selection_text)})
    record("check23b_refined_poolHash_matches_pool_file",
           source_doc.get("candidatePoolHash") == sha256_of(candidate_pool_text),
           {"recorded": source_doc.get("candidatePoolHash"), "actual": sha256_of(candidate_pool_text)})

    # 24. idempotency
    dry_run = subprocess.run(
        ["python", str(MERGE_SCRIPT_PATH), "--dry-run"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    dry_run_output = dry_run.stdout
    idempotent_to_add_zero = "records that would change (add relatedWordIds): 0" in dry_run_output
    idempotent_conflicts_zero = "conflicts (existing relatedWordIds differs from source): 0" in dry_run_output
    record("check24_idempotent_dry_run", dry_run.returncode == 0 and idempotent_to_add_zero and idempotent_conflicts_zero,
           {"returncode": dry_run.returncode, "to_add_zero": idempotent_to_add_zero, "conflicts_zero": idempotent_conflicts_zero})

    # special-case verification
    special = {
        "huida_hui_absent": "hsk1_081" not in production_by_id["hsk3_182"]["relatedWordIds"],
        "renzhen_rende_absent": "hsk3_317" not in production_by_id["hsk3_315"]["relatedWordIds"],
        "renzhen_renwei_absent": "hsk3_317" not in production_by_id["hsk3_316"]["relatedWordIds"],
        "tigao_gao_present": "hsk2_041" in production_by_id["hsk3_352"]["relatedWordIds"],
        "guanji_isolated_from_guanxi_family": not any(
            t in production_by_id["hsk3_153"]["relatedWordIds"] for t in ("hsk3_154", "hsk3_155", "hsk3_156", "hsk3_157")
        ),
    }
    record("special_cases_all_correct", all(special.values()), special)

    # high-count verification
    high_count_actual = {sid: len(production_by_id[sid]["relatedWordIds"]) for sid in HIGH_COUNT_EXPECTED}
    record("high_count_matches", high_count_actual == HIGH_COUNT_EXPECTED, {"expected": HIGH_COUNT_EXPECTED, "actual": high_count_actual})

    # C-tier production verification: only promoted C-tier edges integrated
    c_tier_should_be_integrated = {("hsk3_234", "hsk2_138"), ("hsk3_347", "hsk1_098")}
    c_tier_should_be_excluded = {
        ("hsk3_030", "hsk3_210"), ("hsk3_210", "hsk3_030"),
        ("hsk3_115", "hsk3_139"), ("hsk3_139", "hsk3_115"), ("hsk3_139", "hsk1_183"),
        ("hsk3_159", "hsk3_403"), ("hsk3_403", "hsk3_159"),
    }
    c_tier_integrated_ok = all(t in production_by_id[s]["relatedWordIds"] for s, t in c_tier_should_be_integrated)
    c_tier_excluded_ok = all(t not in production_by_id[s]["relatedWordIds"] for s, t in c_tier_should_be_excluded)
    record("c_tier_production_safety", c_tier_integrated_ok and c_tier_excluded_ok,
           {"integrated_ok": c_tier_integrated_ok, "excluded_ok": c_tier_excluded_ok})

    print("=== P5.7.5 post-integration validation ===")
    for name, result in checks.items():
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {name}: {result['detail']}")
    print()
    print(f"allChecksPassed: {all_passed}")

    after_hash = sha256_of(production_text)

    report = {
        "reportLabel": "P5.7.5 HSK3 RELATED-WORD PRODUCTION INTEGRATION REPORT",
        "timestampUtc": datetime.now(timezone.utc).isoformat(),
        "baselineCommit": "2d44f627f96e53eb03e9193de92f56ce5322c476",
        "sourceArtifact": {
            "path": "tools/hsk/hsk3_related_words_refined_selection.json",
            "sha256": refined_hash_now,
            "modifiedByThisPhase": False,
        },
        "productionTarget": {
            "path": "data/hsk/hsk3/hsk3_vocabulary_production.json",
            "sha256Before": before_snapshot["targetSha256"],
            "sha256After": after_hash,
            "recordCountBefore": before_snapshot["recordCount"],
            "recordCountAfter": len(production_records),
        },
        "criticalAccounting": {
            "totalRefinedRelationships": total_refined,
            "selectedRelationships": selected_rel_count,
            "needsReviewRelationships": needs_review_rel_count,
            "eligibleProductionRelationships": selected_rel_count,
            "arithmeticReconciles": selected_rel_count + needs_review_rel_count == total_refined,
        },
        "mergeContract": {
            "rule": "For each source record where status == 'selected', set production_record.relatedWordIds = source_record.selectedRelatedWordIds, matched by production.id == source.sourceId. needs_review records receive no relatedWordIds. No other field on any record is modified.",
            "selectedRecordsIntegrated": len(selected_src_ids),
            "needsReviewRecordsIntegrated": 0,
            "relationshipsIntegrated": total_relationships_in_production,
        },
        "mergeResult": {
            "recordsWithNonEmptyRelatedWordIds": sum(1 for r in production_records if r.get("relatedWordIds")),
            "recordsChangedFromEmpty": 157,
            "recordsSelectedButLegitimatelyEmpty": 337,
            "recordsUnchangedNeedsReview": EXPECTED_NEEDS_REVIEW,
            "relationshipsAdded": total_relationships_in_production,
        },
        "targetHskDistribution": {
            "refined": refined_level_dist,
            "excludedNeedsReview": excluded_level_dist,
            "production": production_level_dist,
        },
        "specialCases": special,
        "highCount": high_count_actual,
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
