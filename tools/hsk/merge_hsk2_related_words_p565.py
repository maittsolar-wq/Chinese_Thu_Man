"""P5.6.5 -- HSK2 Related-Word Production Integration merge script.

Mirrors tools/hsk/merge_hsk1_related_words_p55.py exactly (the
established P5.5 HSK1 integration pattern), adapted for HSK2's
approved P5.6.4 artifact.

Scope: merge `relatedWordIds` from the approved HSK2 refined-selection
artifact into HSK2 production vocabulary, for `status == "selected"`
records ONLY. `needs_review` records (2 of them: hsk2_067/jiao1,
hsk2_044/ge4zi) receive NO relatedWordIds in this phase -- their
record is left byte-for-byte as-is.

Source artifact (READ-ONLY, never written by this script):
    tools/hsk/hsk2_related_words_refined_selection.json
    (a wrapped object: {..metadata.., "records": [...]}, each record
    shaped {"sourceId", "selectedRelatedWordIds", "status",
    "selectedCount", "selectionReasons"} -- source field is named
    `selectedRelatedWordIds`, renamed to `relatedWordIds` on the
    production record to match the production/app schema, exactly as
    the HSK1 P5.5 merge did.)

Production target (the ONLY file this script may write):
    data/hsk/hsk2/hsk2_vocabulary_production.json

Schema note (matches HSK1's P5.5 situation exactly, unlike HSK6's
P5.3): every HSK2 production record already carries a `relatedWordIds`
key (as `[]`), not an absent key. An existing value of `[]` (or a
missing key) is treated as "not yet integrated" and may be written;
any existing NON-EMPTY value is treated as a real conflict and aborts
the run (fail-closed).

The merge contract is intentionally narrow:
  - For each source record where status == "selected", set
    production_record["relatedWordIds"] = source_record["selectedRelatedWordIds"]
    on the production record whose "id" equals the source record's
    "sourceId".
  - No other field on any production record is read, touched, or
    reordered. All HSK1/3/4/5/6 production records and all HSK2
    records that are NOT "selected" are byte-for-byte untouched.
  - The script fails closed: any precondition mismatch (unexpected
    counts, missing IDs, unknown IDs, an existing non-empty
    relatedWordIds value that conflicts with the source) aborts before
    any write happens.
  - Deterministic: given the same two input files, always produces the
    same output bytes.
  - Idempotent: running it again against an already-merged production
    file is a no-op (every target value already matches the source).

Usage:
    python merge_hsk2_related_words_p565.py --dry-run
    python merge_hsk2_related_words_p565.py --apply
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "tools" / "hsk" / "hsk2_related_words_refined_selection.json"
PRODUCTION_PATH = REPO_ROOT / "data" / "hsk" / "hsk2" / "hsk2_vocabulary_production.json"

EXPECTED_SOURCE_RECORDS = 200
EXPECTED_SELECTED = 198
EXPECTED_NEEDS_REVIEW = 2
EXPECTED_SELECTED_RELATIONSHIPS = 327  # relationships belonging to status=="selected" records only.
# The refined artifact's grand total is 330 across all 200 records, but
# the 2 needs_review records (hsk2_067/jiao1: 2 relationships incl.
# jiao1->xue2; hsk2_044/ge4zi: 1 relationship, ge4zi->gao1) still carry
# their own (unintegrated) relationship data in the artifact -- 330 - 3
# = 327 is the correct count of relationships that actually belong to
# "selected" status and are therefore eligible for integration. Mirrors
# the identical HSK1 P5.5 situation (refinedRelationships=387 vs.
# selected-only=366).
EXPECTED_PRODUCTION_RECORDS = 200

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

    needs_review_ids = {r["sourceId"] for r in needs_review}
    expected_needs_review_ids = {"hsk2_067", "hsk2_044"}
    if needs_review_ids != expected_needs_review_ids:
        fail(f"needs_review sourceIds {needs_review_ids} != expected {expected_needs_review_ids} (jiao1/ge4zi)")

    selected_rel_count = sum(len(r.get("selectedRelatedWordIds") or []) for r in selected)
    if selected_rel_count != EXPECTED_SELECTED_RELATIONSHIPS:
        fail(f"selected relationship count {selected_rel_count} != expected {EXPECTED_SELECTED_RELATIONSHIPS}")

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

    return {"selected": selected, "needs_review": needs_review, "valid_ids": valid_ids}


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


def compute_plan(production_records: list, selected: list) -> dict:
    """Determine, per selected record, whether this run would ADD, leave
    UNCHANGED (idempotent no-op), or CONFLICT with an existing value. An
    existing value of [] (or a missing key) counts as "not yet
    integrated". Never mutates the input lists."""
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

    return {"to_add": to_add, "unchanged": unchanged, "conflicts": conflicts}


def serialize_like_source(records: list) -> str:
    """Serialize the record list with the exact formatting convention
    already used by hsk2_vocabulary_production.json: 2-space indent,
    non-ASCII characters left unescaped, CRLF line endings, no trailing
    newline after the closing bracket."""
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

    plan = compute_plan(production_records, selected)

    # Explicit needs_review safety assertion: neither hsk2_067 nor
    # hsk2_044 may ever appear on the "to_add" side of the plan.
    needs_review_ids = {r["sourceId"] for r in needs_review}
    leaking = [pid for pid, _ in plan["to_add"] if pid["id"] in needs_review_ids]
    if leaking:
        fail(f"needs_review record(s) present in to_add plan -- integrity violation: {leaking}")

    print("=== P5.6.5 merge plan ===")
    print(f"production records total: {len(production_records)}")
    print(f"selected (source) records: {len(selected)}")
    print(f"needs_review (source) records: {len(needs_review)}")
    print(f"records that would change (add relatedWordIds): {len(plan['to_add'])}")
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
