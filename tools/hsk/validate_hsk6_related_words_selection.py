#!/usr/bin/env python3
"""Merge and validate the HSK 6 related-word selection batches.

Input:
    tools/hsk/hsk6_sel01.jsonl .. tools/hsk/hsk6_sel40.jsonl (read-only)
    data/hsk/hsk1..hsk6/hsk{N}_vocabulary_production.json (read-only)

Output:
    tools/hsk/hsk6_related_words_selection.json  (merged artifact)
    tools/hsk/hsk6_related_words_validation_report.json  (this script's findings)

This script does NOT modify the 40 batch files, the HSK6 candidate pool,
production vocabulary, or any other pipeline artifact. It only reads them
and writes the two output files listed above.

POOL SCOPE (approved decision): Related Vocabulary for HSK6 sources uses a
CROSS-LEVEL HSK1-6 scope, not an HSK6-only scope. A relatedWordId from any
of HSK1-6 is in-scope by design, provided it is genuinely useful and
semantically defensible (semantic quality is judged separately, in the QA
report - this script only checks structural/referential validity).

CANDIDATE-POOL PROVENANCE LIMITATION (documented, not silently assumed):
A dedicated "HSK6 related-word candidate pool" artifact was searched for
repository-wide (full git history via `git log --all --diff-filter=A`,
working tree, dangling objects via `git fsck`, reflog) and does not exist
anywhere accessible to this repository. The commit that added the 40
selection batches (50df530) references a checkpoint that validated "0 pool
violations," but never persisted the pool itself as a file.

Consequence: this script CANNOT verify that a given relatedWordId was
drawn from the *original* candidate pool used during selection - that pool
is unrecoverable. It CAN only verify the strictly weaker, mechanically
checkable property: does the relatedWordId exist as a real record
somewhere in the HSK1-6 production vocabulary? That is reported as
`existsInHsk1to6Production`. A separate, explicit field
(`confirmedInOriginalCandidatePool`) is always false for every relationship,
because no artifact exists against which that stronger claim could be
checked - this is a limitation of what can be validated, not a finding
that anything is wrong.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS_HSK = ROOT / "tools" / "hsk"
DATA_HSK = ROOT / "data" / "hsk"

BATCH_GLOB = "hsk6_sel*.jsonl"
MERGED_OUT = TOOLS_HSK / "hsk6_related_words_selection.json"
REPORT_OUT = TOOLS_HSK / "hsk6_related_words_validation_report.json"

EXPECTED_TOTAL = 1800
ALLOWED_STATUS = {"selected", "needs_review"}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
SELECTED_MIN_COUNT = 4  # observed: "selected" == 4 or 5 relatedWordIds

CANDIDATE_POOL_PROVENANCE_NOTE = (
    "No HSK6 related-word candidate-pool artifact exists anywhere "
    "accessible to this repository (full git history, working tree, "
    "dangling objects, and reflog were all searched; see the P3.5.5 "
    "pool-scope investigation). This script therefore validates "
    "relatedWordIds against the mechanically checkable property "
    "'exists in HSK1-6 production vocabulary', which is a necessary but "
    "not sufficient proxy for 'was in the original candidate pool'. "
    "Membership in the true original pool cannot be confirmed for any "
    "relationship, cross-level or HSK6-native, because that pool was "
    "never persisted."
)


def load_production_ids(level: int) -> set[str]:
    path = DATA_HSK / f"hsk{level}" / f"hsk{level}_vocabulary_production.json"
    records = json.loads(path.read_text(encoding="utf-8"))
    return {r["id"] for r in records}


def load_hsk_levels(level: int) -> dict[str, list[int]]:
    path = DATA_HSK / f"hsk{level}" / f"hsk{level}_vocabulary_production.json"
    records = json.loads(path.read_text(encoding="utf-8"))
    return {r["id"]: r.get("hskLevels") for r in records}


def main() -> None:
    issues: dict[str, list] = {
        "duplicate_source_ids": [],
        "missing_hsk6_source_ids": [],
        "unexpected_source_ids": [],
        "wrong_level_source_ids": [],
        "self_references": [],
        "duplicate_related_word_ids": [],
        "unknown_related_word_ids": [],  # not in ANY hsk1-6 production - genuine defect
        "invalid_selection_status": [],
        "invalid_confidence": [],
        "reason_count_mismatch": [],
        "status_count_inconsistency": [],
        "batch_file_errors": [],
    }

    # Cross-level usage is NOT an issue under the approved CROSS-LEVEL
    # HSK1-6 pool scope. Reported separately, descriptively, below.
    cross_level_info: dict[str, list] = {
        "hsk6_to_hsk6": [],
        "cross_level_target_tagged_hsk6": [],  # target hskLevels includes 6
        "cross_level_target_lower_only": [],  # target hskLevels does not include 6
    }

    batch_files = sorted(TOOLS_HSK.glob(BATCH_GLOB))
    print(f"Batch files found: {len(batch_files)}")
    if len(batch_files) != 40:
        issues["batch_file_errors"].append(
            f"Expected 40 batch files, found {len(batch_files)}"
        )

    # batch_merged is derived ONLY from the 40 immutable source batches, and
    # is used ONLY for batch-integrity checks (duplicate sourceId within the
    # batches, per-file JSON validity/counts). It is NEVER what gets
    # validated for relationship-level content, and it is NEVER written to
    # MERGED_OUT if that file already exists - see `working_set` below.
    batch_merged: list[dict] = []
    per_file_counts: dict[str, int] = {}
    seen_source_ids: set[str] = set()

    for path in batch_files:
        count = 0
        with path.open("r", encoding="utf-8") as fh:
            for line_no, line in enumerate(fh, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    issues["batch_file_errors"].append(
                        f"{path.name}:{line_no} invalid JSON: {exc}"
                    )
                    continue

                sid = record.get("sourceId")
                if sid in seen_source_ids:
                    issues["duplicate_source_ids"].append(sid)
                seen_source_ids.add(sid)

                batch_merged.append(record)
                count += 1
        per_file_counts[path.name] = count

    print(f"Total records in batches (in batch order): {len(batch_merged)}")

    # --- structural counts -------------------------------------------------
    if len(batch_merged) != EXPECTED_TOTAL:
        issues["batch_file_errors"].append(
            f"Expected {EXPECTED_TOTAL} total records in batches, got {len(batch_merged)}"
        )

    # merged_already_exists: if hsk6_related_words_selection.json is already
    # present (e.g. after targeted semantic refinement), this script MUST
    # NOT overwrite it by re-deriving from the immutable batches - it
    # validates the file AS IT CURRENTLY STANDS. It is only created fresh
    # from the batches the first time this script ever runs.
    merged_already_exists = MERGED_OUT.exists()
    if merged_already_exists:
        merged: list[dict] = json.loads(MERGED_OUT.read_text(encoding="utf-8"))
        print(f"Validating EXISTING merged/refined artifact ({len(merged)} records) - not re-derived from batches.")
    else:
        merged = batch_merged
        print("No existing merged artifact found - this run creates it fresh from the batches.")

    # --- HSK6 production id cross-check ------------------------------------
    production_ids_by_level = {n: load_production_ids(n) for n in range(1, 7)}
    hsk6_ids = production_ids_by_level[6]
    all_production_ids = set().union(*production_ids_by_level.values())

    # hskLevels for every id across HSK1-5 (HSK6-native targets are trivially
    # "hsk6_to_hsk6", so they don't need this lookup).
    hsk_levels_by_id: dict[str, list[int] | None] = {}
    for n in range(1, 6):
        hsk_levels_by_id.update(load_hsk_levels(n))

    merged_source_ids = {r.get("sourceId") for r in merged}
    missing = sorted(hsk6_ids - merged_source_ids)
    unexpected = sorted(merged_source_ids - hsk6_ids)
    issues["missing_hsk6_source_ids"] = missing
    issues["unexpected_source_ids"] = unexpected

    hsk6_id_pattern = re.compile(r"^hsk6_\d{4}$")
    for r in merged:
        sid = r.get("sourceId")
        if sid and not hsk6_id_pattern.match(sid):
            issues["wrong_level_source_ids"].append(sid)

    # --- per-record checks ---------------------------------------------------
    for r in merged:
        sid = r.get("sourceId")
        related = r.get("relatedWordIds", [])
        status = r.get("selectionStatus")
        confidence = r.get("confidence")
        reasons = r.get("selectionReasons", [])

        if status not in ALLOWED_STATUS:
            issues["invalid_selection_status"].append({"sourceId": sid, "value": status})
        if confidence not in ALLOWED_CONFIDENCE:
            issues["invalid_confidence"].append({"sourceId": sid, "value": confidence})

        if len(reasons) != len(related):
            issues["reason_count_mismatch"].append(
                {"sourceId": sid, "relatedCount": len(related), "reasonCount": len(reasons)}
            )

        if sid in related:
            issues["self_references"].append(sid)

        if len(related) != len(set(related)):
            dupes = sorted({x for x in related if related.count(x) > 1})
            issues["duplicate_related_word_ids"].append({"sourceId": sid, "duplicates": dupes})

        for rel in related:
            if rel not in all_production_ids:
                # Genuinely fabricated/unknown - not in ANY HSK1-6
                # production file. This remains a real defect regardless
                # of pool scope.
                issues["unknown_related_word_ids"].append({"sourceId": sid, "relatedWordId": rel})
                continue

            # Not an issue under the approved CROSS-LEVEL HSK1-6 scope -
            # descriptive categorization only.
            entry = {"sourceId": sid, "relatedWordId": rel}
            if rel in hsk6_ids:
                cross_level_info["hsk6_to_hsk6"].append(entry)
            else:
                target_levels = hsk_levels_by_id.get(rel)
                if target_levels and 6 in target_levels:
                    cross_level_info["cross_level_target_tagged_hsk6"].append(entry)
                else:
                    cross_level_info["cross_level_target_lower_only"].append(entry)

        count = len(related)
        if status == "selected" and count < SELECTED_MIN_COUNT:
            issues["status_count_inconsistency"].append(
                {"sourceId": sid, "status": status, "relatedCount": count, "expected": ">=4"}
            )
        if status == "needs_review" and count >= SELECTED_MIN_COUNT:
            issues["status_count_inconsistency"].append(
                {"sourceId": sid, "status": status, "relatedCount": count, "expected": "<4"}
            )

    # --- write merged artifact ONLY on first creation -----------------------
    # If MERGED_OUT already existed (post-refinement or otherwise), this
    # script must not touch it - it only validates. Writing here would
    # silently discard any refinement applied on top of the original merge.
    if not merged_already_exists:
        MERGED_OUT.write_text(
            json.dumps(merged, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # --- summary -------------------------------------------------------------
    total_relationships = sum(len(r.get("relatedWordIds", [])) for r in merged)
    records_with_relationships = sum(1 for r in merged if r.get("relatedWordIds"))
    needs_review_count = sum(1 for r in merged if r.get("selectionStatus") == "needs_review")
    selected_count = sum(1 for r in merged if r.get("selectionStatus") == "selected")

    report = {
        "mergedSourceMode": "existing_refined_artifact" if merged_already_exists else "fresh_from_batches",
        "poolScope": "CROSS_LEVEL_HSK1_TO_HSK6",
        "candidatePoolProvenanceLimitation": CANDIDATE_POOL_PROVENANCE_NOTE,
        "batchFilesFound": len(batch_files),
        "perFileCounts": per_file_counts,
        "totalRecordsMerged": len(merged),
        "expectedTotal": EXPECTED_TOTAL,
        "uniqueSourceIds": len(seen_source_ids),
        "totalRelationships": total_relationships,
        "recordsWithRelationships": records_with_relationships,
        "recordsWithZeroRelationships": len(merged) - records_with_relationships,
        "selectedStatusCount": selected_count,
        "needsReviewStatusCount": needs_review_count,
        "crossLevelUsage": {
            "note": (
                "Descriptive only, not a validation issue, per the approved "
                "CROSS_LEVEL_HSK1_TO_HSK6 pool scope decision."
            ),
            "hsk6ToHsk6Count": len(cross_level_info["hsk6_to_hsk6"]),
            "crossLevelTargetTaggedHsk6Count": len(
                cross_level_info["cross_level_target_tagged_hsk6"]
            ),
            "crossLevelTargetLowerOnlyCount": len(
                cross_level_info["cross_level_target_lower_only"]
            ),
            "crossLevelTargetTaggedHsk6Examples": cross_level_info[
                "cross_level_target_tagged_hsk6"
            ][:10],
            "crossLevelTargetLowerOnlyExamples": cross_level_info[
                "cross_level_target_lower_only"
            ][:10],
        },
        "candidatePoolConfirmation": {
            "existsInHsk1to6ProductionCount": total_relationships
            - len(issues["unknown_related_word_ids"]),
            "confirmedInOriginalCandidatePoolCount": 0,
            "note": (
                "confirmedInOriginalCandidatePoolCount is 0 for all "
                "relationships (not just cross-level ones) because the "
                "original candidate-pool artifact does not exist. See "
                "candidatePoolProvenanceLimitation."
            ),
        },
        "issues": issues,
        "issueCounts": {k: len(v) for k, v in issues.items()},
        "allChecksPassed": all(len(v) == 0 for v in issues.values()),
    }

    REPORT_OUT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"Pool scope: {report['poolScope']}")
    print()
    print("Issues (genuine defects):")
    for k, v in report["issueCounts"].items():
        print(f"  {k}: {v}")
    print()
    print("Cross-level usage (descriptive, not an issue):")
    cl = report["crossLevelUsage"]
    print(f"  HSK6 -> HSK6: {cl['hsk6ToHsk6Count']}")
    print(f"  Cross-level, target tagged hskLevels includes 6: {cl['crossLevelTargetTaggedHsk6Count']}")
    print(f"  Cross-level, target lower-level only: {cl['crossLevelTargetLowerOnlyCount']}")
    print()
    print("Candidate-pool confirmation:")
    cp = report["candidatePoolConfirmation"]
    print(f"  Exists in HSK1-6 production: {cp['existsInHsk1to6ProductionCount']} / {total_relationships}")
    print(f"  Confirmed in original candidate pool: {cp['confirmedInOriginalCandidatePoolCount']} / {total_relationships} (artifact unrecoverable - see note)")
    print()
    print(f"allChecksPassed: {report['allChecksPassed']}")
    print(f"Merged artifact {'preserved as-is (already existed)' if merged_already_exists else 'created fresh'}: {MERGED_OUT}")
    print(f"Report output: {REPORT_OUT}")


if __name__ == "__main__":
    main()
