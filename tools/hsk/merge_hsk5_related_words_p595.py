"""P5.9.5 -- HSK5 Related-Word Production Integration merge script.

Mirrors the established HSK1-4 integration pattern (most directly
merge_hsk4_related_words_p585.py), adapted for HSK5's approved P5.9.3
refined artifact.

Scope: merge `relatedWordIds` from the approved HSK5 refined-selection
artifact into HSK5 production vocabulary, for relationships whose
status permits production integration ONLY. needs_review-flagged
relationships (5 directed edges, corresponding to the 3 unique pairs
特殊/普遍, 定期/到期, 定期/过期) receive NO relatedWordIds in this
phase -- they are withheld regardless of which direction they are
listed from.

CRITICAL ACCOUNTING (never hardcoded, always computed directly from the
artifact): the refined artifact's total of 384 relationships is NOT the
eligible integration count -- 5 of those 384 directed edges are flagged
needs_review and must be excluded. The eligible count (379) is computed
directly from the artifact by this script.

Source artifact (READ-ONLY, never written by this script):
    tools/hsk/hsk5_related_words_refined_selection.json
    (a wrapped object: {..metadata.., "records": [...]}, each record
    shaped {"sourceId", "selectedRelatedWordIds", "status",
    "selectedCount", "selectionReasons"}; each entry in
    "selectionReasons" that carries a "needsReviewReason" key
    identifies a directed edge that must be WITHHELD from production
    even though it is present in "selectedRelatedWordIds" -- eligibility
    is determined per-relationship, not per-record, since a needs_review
    record can still have some non-flagged relationships in principle
    (not the case for HSK5's specific 4 needs_review records, but the
    script does not assume that).)

Production target (the ONLY file this script may write):
    data/hsk/hsk5/hsk5_vocabulary_production.json

Schema note (matches HSK1-4): every HSK5 production record already
carries a `relatedWordIds` key (as `[]`). An existing value of `[]` (or
a missing key) is treated as "not yet integrated" and may be written;
any existing NON-EMPTY value that differs from the incoming value is a
real conflict and aborts the run (fail-closed).

Usage:
    python merge_hsk5_related_words_p595.py --dry-run
    python merge_hsk5_related_words_p595.py --apply
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "tools" / "hsk" / "hsk5_related_words_refined_selection.json"
PRODUCTION_PATH = REPO_ROOT / "data" / "hsk" / "hsk5" / "hsk5_vocabulary_production.json"

EXPECTED_SOURCE_RECORDS = 1600
EXPECTED_TOTAL_RELATIONSHIPS = 384
EXPECTED_ELIGIBLE_RELATIONSHIPS = 379
EXPECTED_WITHHELD_RELATIONSHIPS = 5
EXPECTED_PRODUCTION_RECORDS = 1600

ALL_LEVEL_PRODUCTION_PATHS = [
    REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
    for n in (1, 2, 3, 4, 5, 6)
]


def load_json_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def build_valid_id_universe() -> set:
    ids = set()
    for p in ALL_LEVEL_PRODUCTION_PATHS:
        records = json.loads(load_json_text(p))
        for r in records:
            ids.add(r["id"])
    return ids


def validate_source(source_doc: dict) -> dict:
    records = source_doc["records"]
    if len(records) != EXPECTED_SOURCE_RECORDS:
        fail(f"source record count {len(records)} != expected {EXPECTED_SOURCE_RECORDS}")

    source_ids = [r["sourceId"] for r in records]
    if len(source_ids) != len(set(source_ids)):
        fail("duplicate sourceId(s) found in source artifact")

    total_relationships = sum(r.get("selectedCount", 0) for r in records)
    if total_relationships != EXPECTED_TOTAL_RELATIONSHIPS:
        fail(f"total relationships {total_relationships} != expected {EXPECTED_TOTAL_RELATIONSHIPS}")

    # ---- CRITICAL ACCOUNTING: eligibility determined per-relationship,
    # computed directly, never hardcoded ----
    eligible_by_source: dict[str, list[str]] = {}
    withheld_count = 0
    for r in records:
        sid = r["sourceId"]
        related = r.get("selectedRelatedWordIds") or []
        if sid in related:
            fail(f"self-reference found in source record {sid}")
        if len(related) != len(set(related)):
            fail(f"duplicate selectedRelatedWordIds within source record {sid}")
        if r.get("selectedCount") != len(related):
            fail(f"selectedCount mismatch in source record {sid}")

        reasons_by_target = {rr["relatedWordId"]: rr for rr in r.get("selectionReasons", [])}
        eligible_targets = []
        for tid in related:
            reason = reasons_by_target.get(tid)
            if reason is None:
                fail(f"relationship {sid}->{tid} has no matching selectionReasons entry -- malformed input")
            if "needsReviewReason" in reason:
                withheld_count += 1
            else:
                eligible_targets.append(tid)
        eligible_by_source[sid] = eligible_targets

    eligible_count = sum(len(v) for v in eligible_by_source.values())

    print("=== P5.9.5 critical accounting (computed directly from artifact) ===")
    print(f"total refined relationships:       {total_relationships}")
    print(f"eligible (non-needs_review) relationships: {eligible_count}")
    print(f"withheld (needs_review) relationships:      {withheld_count}")

    if eligible_count != EXPECTED_ELIGIBLE_RELATIONSHIPS:
        fail(f"eligible relationships {eligible_count} != expected {EXPECTED_ELIGIBLE_RELATIONSHIPS}")
    if withheld_count != EXPECTED_WITHHELD_RELATIONSHIPS:
        fail(f"withheld relationships {withheld_count} != expected {EXPECTED_WITHHELD_RELATIONSHIPS}")
    if eligible_count + withheld_count != total_relationships:
        fail(
            f"arithmetic inconsistency: eligible({eligible_count}) + "
            f"withheld({withheld_count}) != total({total_relationships})"
        )

    valid_ids = build_valid_id_universe()
    for sid, targets in eligible_by_source.items():
        for target in targets:
            if target not in valid_ids:
                fail(f"unknown target id '{target}' referenced by source record {sid} (not found in any HSK1-6 production file)")

    return {
        "eligible_by_source": eligible_by_source,
        "eligible_count": eligible_count,
        "withheld_count": withheld_count,
        "total_relationships": total_relationships,
        "valid_ids": valid_ids,
    }


def validate_production(production_records: list, eligible_by_source: dict) -> None:
    if len(production_records) != EXPECTED_PRODUCTION_RECORDS:
        fail(f"production record count {len(production_records)} != expected {EXPECTED_PRODUCTION_RECORDS}")

    prod_ids = [r["id"] for r in production_records]
    if len(prod_ids) != len(set(prod_ids)):
        fail("duplicate id(s) found in production file")

    prod_id_set = set(prod_ids)
    missing = [sid for sid in eligible_by_source if sid not in prod_id_set]
    if missing:
        fail(f"eligible sourceId(s) missing from production: {missing[:10]}")

    # NOTE: whether an existing non-empty relatedWordIds value is a real
    # conflict (differs from what the eligible set says) or a harmless
    # no-op (identical -- e.g. a legitimate idempotent re-run) is
    # determined per-record in compute_plan() below; a blanket fail here
    # on ANY non-empty value would incorrectly reject a legitimate
    # idempotent re-run.


def compute_plan(production_records: list, eligible_by_source: dict) -> dict:
    prod_by_id = {r["id"]: r for r in production_records}
    to_add = []
    unchanged = []
    conflicts = []

    for sid, targets in eligible_by_source.items():
        prod_r = prod_by_id[sid]
        existing_value = prod_r.get("relatedWordIds") or []
        if existing_value == targets:
            unchanged.append(sid)
        elif not existing_value:
            to_add.append((prod_r, targets))
        else:
            conflicts.append({"id": sid, "existing": existing_value, "incoming": targets})

    return {"to_add": to_add, "unchanged": unchanged, "conflicts": conflicts}


def serialize_like_source(records: list) -> str:
    text = json.dumps(records, indent=2, ensure_ascii=False)
    text = text.replace("\n", "\r\n")
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Report the plan, write nothing.")
    mode.add_argument("--apply", action="store_true", help="Apply the merge to production.")
    args = parser.parse_args()

    source_text = load_json_text(SOURCE_PATH)
    source_doc = json.loads(source_text)

    validated = validate_source(source_doc)
    eligible_by_source = validated["eligible_by_source"]

    production_text = load_json_text(PRODUCTION_PATH)
    production_records = json.loads(production_text)
    validate_production(production_records, eligible_by_source)

    plan = compute_plan(production_records, eligible_by_source)

    records_updated = len(plan["to_add"])
    eligible_zero_rel = len([sid for sid, t in eligible_by_source.items() if len(t) == 0])

    print()
    print("=== P5.9.5 merge plan ===")
    print(f"production records total: {len(production_records)}")
    print(f"source records scanned: {len(eligible_by_source)}")
    print(f"eligible relationships: {validated['eligible_count']}")
    print(f"needs_review relationships withheld: {validated['withheld_count']}")
    print(f"records with eligible-but-zero relationships (no production change expected): {eligible_zero_rel}")
    print(f"records that would change (add relatedWordIds): {records_updated}")
    print(f"records already identical (idempotent no-op): {len(plan['unchanged'])}")
    print(f"total relationships that would be added: {sum(len(v) for _, v in plan['to_add'])}")
    print(f"conflicts (existing relatedWordIds differs from eligible set): {len(plan['conflicts'])}")

    if plan["conflicts"]:
        print("CONFLICT DETAILS:")
        for c in plan["conflicts"]:
            print(f"  id={c['id']} existing={c['existing']} incoming={c['incoming']}")
        fail("refusing to overwrite existing relatedWordIds with conflicting values")

    if args.dry_run:
        print("=== DRY RUN: no files written ===")
        return

    changed_count = 0
    for prod_r, targets in plan["to_add"]:
        prod_r["relatedWordIds"] = targets
        changed_count += 1

    output_text = serialize_like_source(production_records)
    with open(PRODUCTION_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(output_text)

    print(f"=== APPLIED: {changed_count} production record(s) updated ===")
    print(f"Source artifact ({SOURCE_PATH}) was not written to.")


if __name__ == "__main__":
    main()
