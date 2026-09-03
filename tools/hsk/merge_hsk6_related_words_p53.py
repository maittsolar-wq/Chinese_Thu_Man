"""P5.3 -- HSK6 Related-Word Production Integration merge script.

Scope (approved P5.2 decision, Option B): merge `relatedWordIds` from the
approved HSK6 related-word selection artifact into HSK6 production
vocabulary, for `selectionStatus == "selected"` records ONLY.
`needs_review` records (737 of them) receive NO relatedWordIds field in
this phase -- their record shape is left exactly as-is.

Source artifact (READ-ONLY, never written by this script):
    tools/hsk/hsk6_related_words_selection.json

Production target (the ONLY file this script may write):
    data/hsk/hsk6/hsk6_vocabulary_production.json

The merge contract is intentionally narrow:
  - For each source record where selectionStatus == "selected", set
    production_record["relatedWordIds"] = source_record["relatedWordIds"]
    on the production record whose "id" equals the source record's
    "sourceId".
  - No other field on any production record is read, touched, or
    reordered. All 5,300 HSK1-5 production records and all HSK6 records
    that are NOT "selected" are byte-for-byte untouched.
  - The script fails closed: any precondition mismatch (unexpected
    counts, missing IDs, unknown IDs, an existing relatedWordIds value
    that conflicts with the source) aborts before any write happens.
  - Deterministic: given the same two input files, always produces the
    same output bytes.
  - Idempotent: running it again against an already-merged production
    file is a no-op (every target value already matches the source).

Usage:
    python merge_hsk6_related_words_p53.py --dry-run
    python merge_hsk6_related_words_p53.py --apply
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "tools" / "hsk" / "hsk6_related_words_selection.json"
PRODUCTION_PATH = REPO_ROOT / "data" / "hsk" / "hsk6" / "hsk6_vocabulary_production.json"

EXPECTED_SOURCE_RECORDS = 1800
EXPECTED_SELECTED = 1063
EXPECTED_NEEDS_REVIEW = 737
EXPECTED_SELECTED_RELATIONSHIPS = 5119
EXPECTED_PRODUCTION_RECORDS = 1800

ALL_LEVEL_PRODUCTION_PATHS = [
    REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
    for n in (1, 2, 3, 4, 5, 6)
]


def load_json_text(path: Path) -> str:
    # Source/production files are stored with CRLF line endings and no
    # trailing newline; read in binary-safe text mode without translating
    # line endings so we can reproduce the exact byte layout on write.
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


def validate_source(source_records: list) -> dict:
    if len(source_records) != EXPECTED_SOURCE_RECORDS:
        fail(
            f"source record count {len(source_records)} != expected "
            f"{EXPECTED_SOURCE_RECORDS}"
        )

    source_ids = [r["sourceId"] for r in source_records]
    if len(source_ids) != len(set(source_ids)):
        fail("duplicate sourceId(s) found in source artifact")

    selected = [r for r in source_records if r["selectionStatus"] == "selected"]
    needs_review = [
        r for r in source_records if r["selectionStatus"] == "needs_review"
    ]
    other = [
        r
        for r in source_records
        if r["selectionStatus"] not in ("selected", "needs_review")
    ]
    if other:
        fail(f"unexpected selectionStatus values found: {set(r['selectionStatus'] for r in other)}")

    if len(selected) != EXPECTED_SELECTED:
        fail(f"selected count {len(selected)} != expected {EXPECTED_SELECTED}")
    if len(needs_review) != EXPECTED_NEEDS_REVIEW:
        fail(
            f"needs_review count {len(needs_review)} != expected "
            f"{EXPECTED_NEEDS_REVIEW}"
        )

    selected_rel_count = sum(len(r.get("relatedWordIds") or []) for r in selected)
    if selected_rel_count != EXPECTED_SELECTED_RELATIONSHIPS:
        fail(
            f"selected relationship count {selected_rel_count} != expected "
            f"{EXPECTED_SELECTED_RELATIONSHIPS}"
        )

    for r in source_records:
        related = r.get("relatedWordIds") or []
        if r["sourceId"] in related:
            fail(f"self-reference found in source record {r['sourceId']}")
        if len(related) != len(set(related)):
            fail(f"duplicate relatedWordIds within source record {r['sourceId']}")

    valid_ids = build_valid_id_universe()
    for r in source_records:
        for target in r.get("relatedWordIds") or []:
            if target not in valid_ids:
                fail(
                    f"unknown target id '{target}' referenced by source record "
                    f"{r['sourceId']} (not found in any HSK1-6 production file)"
                )

    return {
        "selected": selected,
        "needs_review": needs_review,
        "valid_ids": valid_ids,
    }


def validate_production(production_records: list, selected: list) -> None:
    if len(production_records) != EXPECTED_PRODUCTION_RECORDS:
        fail(
            f"production record count {len(production_records)} != expected "
            f"{EXPECTED_PRODUCTION_RECORDS}"
        )

    prod_ids = [r["id"] for r in production_records]
    if len(prod_ids) != len(set(prod_ids)):
        fail("duplicate id(s) found in production file")

    prod_id_set = set(prod_ids)
    missing = [r["sourceId"] for r in selected if r["sourceId"] not in prod_id_set]
    if missing:
        fail(f"selected sourceId(s) missing from production: {missing[:10]}")


def compute_plan(production_records: list, selected: list) -> dict:
    """Determine, per selected record, whether this run would ADD,
    leave UNCHANGED (idempotent no-op), or CONFLICT with an existing
    value. Never mutates the input lists."""
    prod_by_id = {r["id"]: r for r in production_records}
    to_add = []
    unchanged = []
    conflicts = []

    for src_r in selected:
        target_id = src_r["sourceId"]
        prod_r = prod_by_id[target_id]
        new_value = src_r.get("relatedWordIds") or []
        if "relatedWordIds" in prod_r:
            existing_value = prod_r["relatedWordIds"]
            if existing_value == new_value:
                unchanged.append(target_id)
            else:
                conflicts.append(
                    {
                        "id": target_id,
                        "existing": existing_value,
                        "incoming": new_value,
                    }
                )
        else:
            to_add.append((prod_r, new_value))

    return {"to_add": to_add, "unchanged": unchanged, "conflicts": conflicts}


def serialize_like_source(records: list) -> str:
    """Serialize the record list with the exact formatting convention
    already used by hsk6_vocabulary_production.json: 2-space indent,
    non-ASCII characters left unescaped, CRLF line endings, no trailing
    newline after the closing bracket."""
    text = json.dumps(records, indent=2, ensure_ascii=False)
    # json.dumps always emits bare "\n"; convert to the file's CRLF
    # convention. There is no other "\r" in the input to worry about.
    text = text.replace("\n", "\r\n")
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Report the plan, write nothing.")
    mode.add_argument("--apply", action="store_true", help="Apply the merge to production.")
    args = parser.parse_args()

    source_text = load_json_text(SOURCE_PATH)
    source_records = json.loads(source_text)

    validated = validate_source(source_records)
    selected = validated["selected"]
    needs_review = validated["needs_review"]

    production_text = load_json_text(PRODUCTION_PATH)
    production_records = json.loads(production_text)
    validate_production(production_records, selected)

    plan = compute_plan(production_records, selected)

    unexpected_ids = []  # no unexpected-id concept beyond "not in production", already checked as `missing`

    print("=== P5.3 merge plan ===")
    print(f"production records total: {len(production_records)}")
    print(f"selected (source) records: {len(selected)}")
    print(f"needs_review (source) records: {len(needs_review)}")
    print(f"records that would change (add relatedWordIds): {len(plan['to_add'])}")
    print(f"records already identical (idempotent no-op): {len(plan['unchanged'])}")
    print(
        f"total relationships that would be added: "
        f"{sum(len(v) for _, v in plan['to_add'])}"
    )
    print(f"conflicts (existing relatedWordIds differs from source): {len(plan['conflicts'])}")
    print(f"missing source IDs (checked in validate_production): 0")
    print(f"unexpected IDs: {len(unexpected_ids)}")

    if plan["conflicts"]:
        print("CONFLICT DETAILS:")
        for c in plan["conflicts"]:
            print(f"  id={c['id']} existing={c['existing']} incoming={c['incoming']}")
        fail("refusing to overwrite existing relatedWordIds with conflicting values")

    if args.dry_run:
        print("=== DRY RUN: no files written ===")
        return

    # --apply: perform the additive merge in-place on the in-memory
    # production_records list (order/identity preserved), write once.
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
