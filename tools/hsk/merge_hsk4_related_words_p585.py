"""P5.8.5 -- HSK4 Related-Word Production Integration merge script.

Mirrors the established HSK1/2/3 integration pattern (merge_hsk3_related_
words_p575.py etc.), adapted for HSK4's approved P5.8.4 artifact.

Scope: merge `relatedWordIds` from the approved HSK4 refined-selection
artifact into HSK4 production vocabulary, for `status == "selected"`
records ONLY. `needs_review` records (10 of them) receive NO
relatedWordIds in this phase -- their record is left byte-for-byte as-is.

CRITICAL ACCOUNTING (never hardcoded, always computed directly from the
artifact): the refined artifact's total of 698 relationships is NOT the
eligible integration count -- 29 of those 698 belong to the 10
needs_review records and must be excluded. The eligible count (669) is
computed directly from the artifact by this script.

Source artifact (READ-ONLY, never written by this script):
    tools/hsk/hsk4_related_words_refined_selection.json
    (a wrapped object: {..metadata.., "records": [...]}, each record
    shaped {"sourceId", "selectedRelatedWordIds", "status",
    "selectedCount", "selectionReasons"} -- source field is named
    `selectedRelatedWordIds`, renamed to `relatedWordIds` on the
    production record to match the production/app schema, exactly as
    the HSK1/2/3 merges did.)

Production target (the ONLY file this script may write):
    data/hsk/hsk4/hsk4_vocabulary_production.json

Schema note (matches HSK1/2/3): every HSK4 production record already
carries a `relatedWordIds` key (as `[]`). An existing value of `[]` (or
a missing key) is treated as "not yet integrated" and may be written;
any existing NON-EMPTY value is a real conflict and aborts the run
(fail-closed).

Usage:
    python merge_hsk4_related_words_p585.py --dry-run
    python merge_hsk4_related_words_p585.py --apply
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "tools" / "hsk" / "hsk4_related_words_refined_selection.json"
PRODUCTION_PATH = REPO_ROOT / "data" / "hsk" / "hsk4" / "hsk4_vocabulary_production.json"

EXPECTED_SOURCE_RECORDS = 1000
EXPECTED_SELECTED = 990
EXPECTED_NEEDS_REVIEW = 10
EXPECTED_TOTAL_RELATIONSHIPS = 698
EXPECTED_ELIGIBLE_RELATIONSHIPS = 669
EXPECTED_WITHHELD_RELATIONSHIPS = 29
EXPECTED_PRODUCTION_RECORDS = 1000

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

    selected = [r for r in records if r["status"] == "selected"]
    needs_review = [r for r in records if r["status"] == "needs_review"]
    other = [r for r in records if r["status"] not in ("selected", "needs_review")]
    if other:
        fail(f"unexpected status values found: {set(r['status'] for r in other)}")

    if len(selected) != EXPECTED_SELECTED:
        fail(f"selected count {len(selected)} != expected {EXPECTED_SELECTED}")
    if len(needs_review) != EXPECTED_NEEDS_REVIEW:
        fail(f"needs_review count {len(needs_review)} != expected {EXPECTED_NEEDS_REVIEW}")

    # ---- CRITICAL ACCOUNTING: computed directly, never hardcoded ----
    total_relationships = sum(len(r.get("selectedRelatedWordIds") or []) for r in records)
    selected_rel_count = sum(len(r.get("selectedRelatedWordIds") or []) for r in selected)
    needs_review_rel_count = sum(len(r.get("selectedRelatedWordIds") or []) for r in needs_review)

    print("=== P5.8.5 critical accounting (computed directly from artifact) ===")
    print(f"total refined relationships:       {total_relationships}")
    print(f"selected-status relationships:     {selected_rel_count}")
    print(f"needs_review relationships:        {needs_review_rel_count}")
    print(f"eligible production relationships: {selected_rel_count}")

    if total_relationships != EXPECTED_TOTAL_RELATIONSHIPS:
        fail(f"total relationships {total_relationships} != expected {EXPECTED_TOTAL_RELATIONSHIPS}")
    if selected_rel_count != EXPECTED_ELIGIBLE_RELATIONSHIPS:
        fail(f"eligible (selected) relationships {selected_rel_count} != expected {EXPECTED_ELIGIBLE_RELATIONSHIPS}")
    if needs_review_rel_count != EXPECTED_WITHHELD_RELATIONSHIPS:
        fail(f"withheld (needs_review) relationships {needs_review_rel_count} != expected {EXPECTED_WITHHELD_RELATIONSHIPS}")
    if selected_rel_count + needs_review_rel_count != total_relationships:
        fail(
            f"arithmetic inconsistency: selected({selected_rel_count}) + "
            f"needs_review({needs_review_rel_count}) != total({total_relationships})"
        )

    for r in records:
        related = r.get("selectedRelatedWordIds") or []
        if r["sourceId"] in related:
            fail(f"self-reference found in source record {r['sourceId']}")
        if len(related) != len(set(related)):
            fail(f"duplicate selectedRelatedWordIds within source record {r['sourceId']}")
        if r["selectedCount"] != len(related):
            fail(f"selectedCount mismatch in source record {r['sourceId']}")

    valid_ids = build_valid_id_universe()
    for r in records:
        for target in r.get("selectedRelatedWordIds") or []:
            if target not in valid_ids:
                fail(f"unknown target id '{target}' referenced by source record {r['sourceId']} (not found in any HSK1-6 production file)")
            if not target.startswith("hsk4_"):
                fail(f"non-HSK4 target id '{target}' referenced by source record {r['sourceId']} -- scope violation")

    return {
        "selected": selected,
        "needs_review": needs_review,
        "valid_ids": valid_ids,
        "selected_rel_count": selected_rel_count,
        "needs_review_rel_count": needs_review_rel_count,
        "total_relationships": total_relationships,
    }


def validate_production(production_records: list, selected: list) -> None:
    if len(production_records) != EXPECTED_PRODUCTION_RECORDS:
        fail(f"production record count {len(production_records)} != expected {EXPECTED_PRODUCTION_RECORDS}")

    prod_ids = [r["id"] for r in production_records]
    if len(prod_ids) != len(set(prod_ids)):
        fail("duplicate id(s) found in production file")

    prod_id_set = set(prod_ids)
    missing = [r["sourceId"] for r in selected if r["sourceId"] not in prod_id_set]
    if missing:
        fail(f"selected sourceId(s) missing from production: {missing[:10]}")

    # NOTE: whether any existing non-empty relatedWordIds value is a real
    # conflict (differs from what the approved source artifact says) or a
    # harmless no-op (identical to it, e.g. on a second run of this same
    # script -- the mandatory P5.8.5 idempotency test) is determined
    # per-record, precisely, in compute_plan() below, which already
    # distinguishes unchanged / to_add / conflicts. A blanket fail here on
    # ANY non-empty value would incorrectly reject a legitimate idempotent
    # re-run, so this function is intentionally left to structural checks
    # only; compute_plan() is the sole source of conflict-fail-closed
    # behavior for relatedWordIds content.


def compute_plan(production_records: list, selected: list, needs_review: list) -> dict:
    prod_by_id = {r["id"]: r for r in production_records}
    to_add = []
    unchanged = []
    conflicts = []

    for src_r in selected:
        target_id = src_r["sourceId"]
        prod_r = prod_by_id[target_id]
        new_value = src_r.get("selectedRelatedWordIds") or []
        existing_value = prod_r.get("relatedWordIds") or []
        if existing_value == new_value:
            unchanged.append(target_id)
        elif not existing_value:
            to_add.append((prod_r, new_value))
        else:
            conflicts.append({"id": target_id, "existing": existing_value, "incoming": new_value})

    # Explicit safety check: no needs_review record may appear in to_add.
    needs_review_ids = {r["sourceId"] for r in needs_review}
    leaking = [pid for pid, _ in to_add if pid["id"] in needs_review_ids]
    if leaking:
        fail(f"needs_review record(s) present in to_add plan -- integrity violation: {[p['id'] for p in leaking]}")

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
    selected = validated["selected"]
    needs_review = validated["needs_review"]

    production_text = load_json_text(PRODUCTION_PATH)
    production_records = json.loads(production_text)
    validate_production(production_records, selected)

    plan = compute_plan(production_records, selected, needs_review)

    records_updated = len(plan["to_add"])
    selected_zero_rel = len([r for r in selected if len(r.get("selectedRelatedWordIds") or []) == 0])

    print()
    print("=== P5.8.5 merge plan ===")
    print(f"production records total: {len(production_records)}")
    print(f"selected (source) records: {len(selected)}")
    print(f"needs_review (source) records: {len(needs_review)}")
    print(f"selected records with zero relationships (no production change expected): {selected_zero_rel}")
    print(f"records that would change (add relatedWordIds): {records_updated}")
    print(f"records already identical (idempotent no-op): {len(plan['unchanged'])}")
    print(f"total relationships that would be added: {sum(len(v) for _, v in plan['to_add'])}")
    print(f"conflicts (existing relatedWordIds differs from source): {len(plan['conflicts'])}")

    if plan["conflicts"]:
        print("CONFLICT DETAILS:")
        for c in plan["conflicts"]:
            print(f"  id={c['id']} existing={c['existing']} incoming={c['incoming']}")
        fail("refusing to overwrite existing relatedWordIds with conflicting values")

    if args.dry_run:
        print("=== DRY RUN: no files written ===")
        return

    changed_count = 0
    for prod_r, new_value in plan["to_add"]:
        prod_r["relatedWordIds"] = new_value
        changed_count += 1

    output_text = serialize_like_source(production_records)
    with open(PRODUCTION_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(output_text)

    print(f"=== APPLIED: {changed_count} production record(s) updated ===")
    print(f"Source artifact ({SOURCE_PATH}) was not written to.")


if __name__ == "__main__":
    main()
