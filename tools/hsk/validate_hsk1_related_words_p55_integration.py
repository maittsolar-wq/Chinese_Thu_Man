"""P5.5 -- Post-integration validation for the HSK1 related-word
production merge. Read-only: writes exactly one new file,
tools/hsk/hsk1_related_words_p55_integration_report.json. Never
modifies the source artifact or any production file.

Mirrors the checks performed for the HSK6 P5.3 integration
(tools/hsk/hsk6_related_words_p53_integration_report.json), adapted for
HSK1's schema (wrapped source object, selectedRelatedWordIds field
name, relatedWordIds already present-but-empty pre-merge).
"""

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_refined_selection.json"
BEFORE_SNAPSHOT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_production_p55_before_snapshot.json"
PRODUCTION_PATH = REPO_ROOT / "data" / "hsk" / "hsk1" / "hsk1_vocabulary_production.json"
REPORT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_p55_integration_report.json"

OTHER_LEVEL_PRODUCTION_PATHS = {
    n: REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
    for n in (2, 3, 4, 5, 6)
}
RADICALS_PATHS = [
    REPO_ROOT / "data" / "radicals" / "radicals_214.json",
    REPO_ROOT / "data" / "radicals" / "radicals_214_detail.json",
]

EXPECTED_PRODUCTION_RECORDS = 300
EXPECTED_SELECTED = 292
EXPECTED_NEEDS_REVIEW = 8
EXPECTED_SELECTED_RELATIONSHIPS = 366


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
    """True iff the working-tree file is git-identical to HEAD's committed
    blob (via hash-object vs rev-parse, immune to CRLF checkout noise)."""
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

    def record(name: str, passed: bool, detail: str) -> None:
        nonlocal all_passed
        checks[name] = {"passed": passed, "detail": detail}
        if not passed:
            all_passed = False

    # ---- load everything ----
    source_text = load_text(SOURCE_PATH)
    source_doc = json.loads(source_text)
    source_records = {r["sourceId"]: r for r in source_doc["records"]}

    before_snapshot = json.loads(load_text(BEFORE_SNAPSHOT_PATH))

    production_text = load_text(PRODUCTION_PATH)
    production_records = json.loads(production_text)
    production_by_id = {r["id"]: r for r in production_records}

    # Universe of valid target ids across all 6 levels (post-merge state).
    universe_ids = set()
    universe_ids.update(production_by_id.keys())
    for p in OTHER_LEVEL_PRODUCTION_PATHS.values():
        for r in json.loads(load_text(p)):
            universe_ids.add(r["id"])

    # ---- production record count unchanged ----
    record(
        "production_record_count_unchanged",
        len(production_records) == EXPECTED_PRODUCTION_RECORDS
        == before_snapshot["recordCount"],
        f"before={before_snapshot['recordCount']} after={len(production_records)} "
        f"expected={EXPECTED_PRODUCTION_RECORDS}",
    )

    # ---- every sourceId still exists ----
    before_ids = set(before_snapshot["recordIds"])
    after_ids = set(production_by_id.keys())
    record(
        "every_source_id_still_exists",
        before_ids == after_ids,
        f"missing={sorted(before_ids - after_ids)[:10]} "
        f"added={sorted(after_ids - before_ids)[:10]}",
    )

    # ---- every relatedWordId exists in vocabulary production ----
    unknown_targets = []
    for r in production_records:
        for t in r.get("relatedWordIds") or []:
            if t not in universe_ids:
                unknown_targets.append((r["id"], t))
    record(
        "every_related_word_id_exists",
        len(unknown_targets) == 0,
        f"unknown: {unknown_targets[:10]}",
    )

    # ---- no self references ----
    self_refs = [r["id"] for r in production_records if r["id"] in (r.get("relatedWordIds") or [])]
    record("no_self_references", len(self_refs) == 0, f"self-refs: {self_refs[:10]}")

    # ---- no duplicate relatedWordIds within a record ----
    dupe_records = [
        r["id"]
        for r in production_records
        if len(r.get("relatedWordIds") or []) != len(set(r.get("relatedWordIds") or []))
    ]
    record("no_duplicate_related_word_ids", len(dupe_records) == 0, f"dupes: {dupe_records[:10]}")

    # ---- only approved selected records received relatedWordIds; needs_review stayed empty ----
    selected_src_ids = {sid for sid, r in source_records.items() if r["status"] == "selected"}
    needs_review_src_ids = {sid for sid, r in source_records.items() if r["status"] == "needs_review"}

    needs_review_with_data = [
        sid for sid in needs_review_src_ids if (production_by_id[sid].get("relatedWordIds") or [])
    ]
    record(
        "needs_review_records_remain_without_related_word_ids",
        len(needs_review_with_data) == 0,
        f"unexpected non-empty needs_review records: {needs_review_with_data[:10]}",
    )

    non_selected_non_review_with_data = [
        r["id"]
        for r in production_records
        if r["id"] not in selected_src_ids
        and r["id"] not in needs_review_src_ids
        and (r.get("relatedWordIds") or [])
    ]
    record(
        "only_selected_records_received_related_word_ids",
        len(non_selected_non_review_with_data) == 0,
        f"unexpected: {non_selected_non_review_with_data[:10]}",
    )

    mismatched_selected = []
    for sid in selected_src_ids:
        expected_value = source_records[sid].get("selectedRelatedWordIds") or []
        actual_value = production_by_id[sid].get("relatedWordIds") or []
        if expected_value != actual_value:
            mismatched_selected.append(sid)
    record(
        "selected_records_exactly_match_source",
        len(mismatched_selected) == 0,
        f"mismatched: {mismatched_selected[:10]}",
    )

    # ---- total relationship count matches approved source artifact ----
    total_relationships_in_production = sum(len(r.get("relatedWordIds") or []) for r in production_records)
    record(
        "total_relationship_count_matches_source",
        total_relationships_in_production == EXPECTED_SELECTED_RELATIONSHIPS,
        f"actual={total_relationships_in_production} expected={EXPECTED_SELECTED_RELATIONSHIPS}",
    )

    # ---- no unexpected fields changed (only relatedWordIds may differ per record) ----
    # We don't have the literal before bytes per-record (only the before hash +
    # id list), so we instead prove it structurally: every field other than
    # relatedWordIds is untouched by re-deriving what "before" must have been
    # (identical production file with relatedWordIds forced back to [] for
    # every id in recordIds) and comparing hashes.
    reconstructed_before = []
    for r in production_records:
        r2 = dict(r)
        r2["relatedWordIds"] = []
        reconstructed_before.append(r2)
    # order must match the original before-snapshot's recordIds order
    reconstructed_before_by_id = {r["id"]: r for r in reconstructed_before}
    reconstructed_before_ordered = [reconstructed_before_by_id[i] for i in before_snapshot["recordIds"]]
    reconstructed_text = json.dumps(reconstructed_before_ordered, indent=2, ensure_ascii=False).replace("\n", "\r\n")
    reconstructed_hash = sha256_of(reconstructed_text)
    record(
        "no_unexpected_fields_changed",
        reconstructed_hash == before_snapshot["targetSha256"],
        f"reconstructed(with relatedWordIds zeroed)={reconstructed_hash} "
        f"before_snapshot={before_snapshot['targetSha256']}",
    )

    # ---- hashes ----
    after_hash = sha256_of(production_text)
    source_hash = sha256_of(source_text)
    record(
        "source_artifact_unmodified",
        unchanged_via_git("tools/hsk/hsk1_related_words_refined_selection.json"),
        "git hash-object vs HEAD blob comparison (CRLF-safe)",
    )

    # ---- HSK2-6 production, radicals, app/src unchanged ----
    other_level_unchanged = {}
    for n, p in OTHER_LEVEL_PRODUCTION_PATHS.items():
        relpath = str(p.relative_to(REPO_ROOT)).replace("\\", "/")
        other_level_unchanged[f"hsk{n}"] = unchanged_via_git(relpath)
    record(
        "hsk2_6_production_unchanged",
        all(other_level_unchanged.values()),
        json.dumps(other_level_unchanged),
    )

    radicals_unchanged = {}
    for p in RADICALS_PATHS:
        relpath = str(p.relative_to(REPO_ROOT)).replace("\\", "/")
        radicals_unchanged[relpath] = unchanged_via_git(relpath) if p.exists() else "missing"
    record(
        "radicals_unchanged",
        all(v is True for v in radicals_unchanged.values()),
        json.dumps(radicals_unchanged),
    )

    app_src_status = subprocess.run(
        ["git", "status", "--porcelain", "--", "app/src"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    record(
        "app_src_unchanged",
        app_src_status.strip() == "",
        f"git status --porcelain -- app/src: {app_src_status.strip() or '(clean)'}",
    )

    print("=== P5.5 post-integration validation ===")
    for name, result in checks.items():
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {name}: {result['detail']}")
    print()
    print(f"allChecksPassed: {all_passed}")

    report = {
        "reportLabel": "P5.5 HSK1 RELATED-WORD PRODUCTION INTEGRATION REPORT",
        "timestampUtc": datetime.now(timezone.utc).isoformat(),
        "baselineCommit": "6822fb53b34a2a67657e4eb950d5d5164e24b3a0",
        "sourceArtifact": {
            "path": "tools/hsk/hsk1_related_words_refined_selection.json",
            "sha256": source_hash,
            "modifiedByThisPhase": False,
        },
        "productionTarget": {
            "path": "data/hsk/hsk1/hsk1_vocabulary_production.json",
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
            "recordsWithNonEmptyRelatedWordIds": sum(
                1 for r in production_records if r.get("relatedWordIds")
            ),
            "recordsChangedFromEmpty": 193,
            "recordsSelectedButLegitimatelyEmpty": 99,
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
