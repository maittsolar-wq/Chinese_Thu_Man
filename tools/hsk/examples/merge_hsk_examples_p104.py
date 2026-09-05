"""P5.10.4 -- HSK Examples Production Integration merge script.

Mirrors the established Related-Words integration pattern (most directly
`merge_hsk5_related_words_p595.py`): fail-closed, deterministic-by-ID,
dry-run/apply modes, never silently overwrites, never touches anything
outside its declared write targets.

Naming note (reported, not silently assumed): the original
`hsk_examples_pipeline_plan_p5101.md` sketched a slightly different
phase-number scheme for this step (its own text calls a later stage
"P5.10.5 integration" and an earlier one "P5.10.4 final validation").
This session's actual usage settled on "P5.10.3" for the batch
generation work (batches 002-032, already committed). This script is
therefore named "p104" pragmatically -- the next unused sequence number
-- for the integration step; it does not claim to match the original
plan doc's exact numbering, which was itself never binding (no `P5`
phase numbering exists anywhere in `docs/`, confirmed by direct
inspection).

Scope: merge generated example sentences from the pilot artifact
(`hsk_examples_pilot_p5102.json`, 100 records) and every normal-queue
batch file (`examples_batch_002.json` .. `examples_batch_032.json`,
5212 records; 5312 total) into the `examples` field of the matching
production vocabulary record, for all six HSK levels.

Source artifacts (READ-ONLY, never written by this script):
    tools/hsk/examples/hsk_examples_p102_pilot_01.json
    tools/hsk/examples/examples_batch_002.json .. examples_batch_032.json

Production targets (the ONLY files this script may write):
    data/hsk/hsk{1..6}/hsk{1..6}_vocabulary_production.json

Schema note (differs from Related Words): unlike `relatedWordIds`,
which already existed on every HSK1-5 record (as `[]`) before that
integration ran, **no production record on any level currently has an
`examples` key at all** (confirmed by direct inspection: HSK1-5 have
`exampleIds`, a legacy always-empty field intentionally left alone per
P5.10.1; HSK6 has neither). This script therefore ADDS a new
`examples` key -- but strictly only to records that have a
corresponding source entry (pilot or a batch). The 88 special-review
(tier 3/4) records, spread across all six levels (not just HSK6),
receive NO `examples` key at all -- they are not silently given `[]`
"to make accounting look complete"; they are left exactly as they are,
byte-for-byte, because this integration phase has no generated content
for them and they are explicitly out of scope.

A source record's `examples` array is copied verbatim, including the
13 records (1 in the pilot, 12 across batches -- the HSK6 numeric-
suffix homograph cases) whose array is legitimately `[]` because their
literal word text can never appear in natural Chinese text (established
`needs_review` treatment from the generation phase). These 13 DO
receive an `examples` key (an empty array) because they went through
the pipeline and are accounted for -- this is the deliberate,
documented distinction between "processed, legitimately empty" (key
present, `[]`) and "out of scope" (key absent entirely).

ID mapping: every source record's `sourceId` is used verbatim as the
production `id` to update -- never by word text, never by array
position. The target production file is selected by parsing the
`hsk{N}_` prefix directly from the ID (the same convention
`queue_lib_p103.load_universe()` uses), and cross-checked against the
source record's own declared `hskLevel` field.

Usage:
    python merge_hsk_examples_p104.py --dry-run
    python merge_hsk_examples_p104.py --apply
"""

import argparse
import glob
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
EXAMPLES_DIR = REPO_ROOT / "tools" / "hsk" / "examples"
PILOT_PATH = EXAMPLES_DIR / "hsk_examples_p102_pilot_01.json"
SPECIAL_REVIEW_PATH = EXAMPLES_DIR / "hsk_examples_special_review_p103.json"

PRODUCTION_PATHS = {
    n: REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
    for n in (1, 2, 3, 4, 5, 6)
}

EXPECTED_PRODUCTION_COUNTS = {1: 300, 2: 200, 3: 500, 4: 1000, 5: 1600, 6: 1800}
EXPECTED_TOTAL_UNIVERSE = 5400
EXPECTED_SPECIAL_REVIEW = 88
EXPECTED_PILOT_RECORDS = 100
EXPECTED_BATCH_FILE_COUNT = 31  # batches 002..032 inclusive
EXPECTED_BATCH_RECORDS_TOTAL = 5212
EXPECTED_TOTAL_SOURCE_RECORDS = 5312  # pilot(100) + batches(5212)

EXAMPLE_FIELDS = {"chinese", "pinyin", "meaningVi"}


def load_json_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def level_from_id(rid: str) -> int:
    m = re.match(r"^hsk([1-6])_", rid)
    if not m:
        fail(f"cannot parse HSK level from id '{rid}' -- unexpected id format")
    return int(m.group(1))


def validate_example_record(rid: str, examples: list) -> None:
    if not isinstance(examples, list):
        fail(f"record {rid}: 'examples' is not a list")
    for i, ex in enumerate(examples):
        if not isinstance(ex, dict):
            fail(f"record {rid}: example[{i}] is not an object")
        if set(ex.keys()) != EXAMPLE_FIELDS:
            fail(f"record {rid}: example[{i}] has unexpected field set {sorted(ex.keys())}, expected {sorted(EXAMPLE_FIELDS)}")
        for field in EXAMPLE_FIELDS:
            value = ex.get(field)
            if not isinstance(value, str) or not value.strip():
                fail(f"record {rid}: example[{i}].{field} is not a non-empty string")


def load_sources() -> dict[str, dict]:
    """Load pilot + every batch file, return {sourceId: examples_list}."""
    if not PILOT_PATH.exists():
        fail(f"pilot artifact not found: {PILOT_PATH}")
    pilot_doc = json.loads(load_json_text(PILOT_PATH))
    pilot_records = pilot_doc["records"]
    if len(pilot_records) != EXPECTED_PILOT_RECORDS:
        fail(f"pilot record count {len(pilot_records)} != expected {EXPECTED_PILOT_RECORDS}")

    batch_paths = sorted(EXAMPLES_DIR.glob("examples_batch_*.json"))
    if len(batch_paths) != EXPECTED_BATCH_FILE_COUNT:
        fail(f"batch file count {len(batch_paths)} != expected {EXPECTED_BATCH_FILE_COUNT} "
             f"(found: {[p.name for p in batch_paths]})")
    expected_batch_numbers = list(range(2, 33))
    actual_batch_numbers = []
    for p in batch_paths:
        m = re.search(r"examples_batch_(\d+)\.json$", p.name)
        if not m:
            fail(f"unexpected batch filename shape: {p.name}")
        actual_batch_numbers.append(int(m.group(1)))
    if actual_batch_numbers != expected_batch_numbers:
        fail(f"batch numbers {actual_batch_numbers} != expected contiguous {expected_batch_numbers}")

    all_records = [("pilot", r) for r in pilot_records]
    batch_record_total = 0
    for p in batch_paths:
        doc = json.loads(load_json_text(p))
        recs = doc["records"]
        batch_record_total += len(recs)
        all_records.extend((p.name, r) for r in recs)

    if batch_record_total != EXPECTED_BATCH_RECORDS_TOTAL:
        fail(f"total batch record count {batch_record_total} != expected {EXPECTED_BATCH_RECORDS_TOTAL}")

    total = len(all_records)
    if total != EXPECTED_TOTAL_SOURCE_RECORDS:
        fail(f"total source record count {total} != expected {EXPECTED_TOTAL_SOURCE_RECORDS}")

    by_id: dict[str, dict] = {}
    seen_ids: dict[str, str] = {}
    for origin, r in all_records:
        rid = r["sourceId"]
        if rid in seen_ids:
            fail(f"duplicate sourceId '{rid}' found in both {seen_ids[rid]} and {origin} -- refusing to proceed")
        seen_ids[rid] = origin

        risk_tier = r.get("riskTier")
        if risk_tier not in (1, 2):
            fail(f"record {rid} (from {origin}) has riskTier={risk_tier}, expected 1 or 2 "
                 f"(tier 3/4 must never appear in a normal-queue source file)")

        declared_level = r.get("hskLevel")
        id_level = level_from_id(rid)
        if declared_level != id_level:
            fail(f"record {rid} (from {origin}): declared hskLevel={declared_level} "
                 f"does not match level parsed from id prefix ({id_level})")

        examples = r["examples"]
        validate_example_record(rid, examples)

        by_id[rid] = examples

    if len(by_id) != EXPECTED_TOTAL_SOURCE_RECORDS:
        fail(f"internal inconsistency: {len(by_id)} unique ids vs {EXPECTED_TOTAL_SOURCE_RECORDS} expected")

    return by_id


def load_special_review_ids() -> set[str]:
    if not SPECIAL_REVIEW_PATH.exists():
        fail(f"special-review artifact not found: {SPECIAL_REVIEW_PATH}")
    doc = json.loads(load_json_text(SPECIAL_REVIEW_PATH))
    records = doc["records"] if isinstance(doc, dict) else doc
    ids = set()
    for r in records:
        rid = r.get("sourceId") or r.get("id")
        if rid is None:
            fail("a special-review record has neither 'sourceId' nor 'id'")
        ids.add(rid)
    if len(ids) != EXPECTED_SPECIAL_REVIEW:
        fail(f"special-review record count {len(ids)} != expected {EXPECTED_SPECIAL_REVIEW}")
    return ids


def load_production() -> dict[int, list]:
    production_by_level = {}
    for n, path in PRODUCTION_PATHS.items():
        records = json.loads(load_json_text(path))
        if len(records) != EXPECTED_PRODUCTION_COUNTS[n]:
            fail(f"HSK{n} production record count {len(records)} != expected {EXPECTED_PRODUCTION_COUNTS[n]}")
        ids = [r["id"] for r in records]
        if len(ids) != len(set(ids)):
            fail(f"duplicate id(s) found in HSK{n} production file")
        for r in records:
            if level_from_id(r["id"]) != n:
                fail(f"HSK{n} production file contains id '{r['id']}' whose prefix does not match level {n}")
        production_by_level[n] = records
    return production_by_level


def validate_universe_partition(eligible_ids: set, special_review_ids: set, production_by_level: dict) -> None:
    universe_ids = set()
    for n, records in production_by_level.items():
        for r in records:
            universe_ids.add(r["id"])

    if len(universe_ids) != EXPECTED_TOTAL_UNIVERSE:
        fail(f"universe size {len(universe_ids)} != expected {EXPECTED_TOTAL_UNIVERSE}")

    overlap = eligible_ids & special_review_ids
    if overlap:
        fail(f"{len(overlap)} id(s) appear in BOTH the examples source data and the special-review "
             f"queue -- these sets must be disjoint: {sorted(overlap)[:10]}")

    unknown_eligible = eligible_ids - universe_ids
    if unknown_eligible:
        fail(f"{len(unknown_eligible)} sourceId(s) from examples data are not found in any production "
             f"file: {sorted(unknown_eligible)[:10]}")

    unknown_special = special_review_ids - universe_ids
    if unknown_special:
        fail(f"{len(unknown_special)} special-review id(s) are not found in any production file: "
             f"{sorted(unknown_special)[:10]}")

    union = eligible_ids | special_review_ids
    missing = universe_ids - union
    if missing:
        fail(f"{len(missing)} production id(s) are neither in the examples source data nor the "
             f"special-review queue -- unaccounted-for record(s): {sorted(missing)[:10]}")

    if union != universe_ids:
        fail("union of eligible + special-review ids does not exactly equal the full production universe")

    print("=== universe partition check ===")
    print(f"universe: {len(universe_ids)}  eligible: {len(eligible_ids)}  "
          f"special_review: {len(special_review_ids)}  "
          f"eligible+special_review==universe: {union == universe_ids}")


def compute_plan(production_by_level: dict, eligible_by_id: dict) -> dict:
    to_add = []
    unchanged = []
    conflicts = []
    already_has_examples_key_unexpectedly = []

    for n, records in production_by_level.items():
        for r in records:
            rid = r["id"]
            if rid not in eligible_by_id:
                # Special-review or otherwise out of scope: must not carry
                # an 'examples' key at all. If one exists already (it
                # shouldn't, per inspection), that is a real conflict --
                # never silently overwritten or silently ignored.
                if "examples" in r:
                    already_has_examples_key_unexpectedly.append(rid)
                continue

            targets = eligible_by_id[rid]
            if "examples" in r:
                if r["examples"] == targets:
                    unchanged.append(rid)
                else:
                    conflicts.append({"id": rid, "existing": r["examples"], "incoming": targets})
            else:
                to_add.append((r, targets))

    return {
        "to_add": to_add,
        "unchanged": unchanged,
        "conflicts": conflicts,
        "unexpected_existing_key": already_has_examples_key_unexpectedly,
    }


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

    eligible_by_id = load_sources()
    special_review_ids = load_special_review_ids()
    production_by_level = load_production()

    validate_universe_partition(set(eligible_by_id.keys()), special_review_ids, production_by_level)

    plan = compute_plan(production_by_level, eligible_by_id)

    if plan["unexpected_existing_key"]:
        fail(f"{len(plan['unexpected_existing_key'])} out-of-scope record(s) unexpectedly already carry "
             f"an 'examples' key: {plan['unexpected_existing_key'][:10]}")

    print()
    print("=== P5.10.4 merge plan ===")
    print(f"total source records (pilot + batches 002-032): {len(eligible_by_id)}")
    print(f"special-review records (untouched, out of scope): {len(special_review_ids)}")
    print(f"records that would change (add examples): {len(plan['to_add'])}")
    print(f"records already identical (idempotent no-op): {len(plan['unchanged'])}")
    total_sentences = sum(len(t) for _, t in plan["to_add"])
    print(f"total example sentences that would be added: {total_sentences}")
    empty_added = sum(1 for _, t in plan["to_add"] if len(t) == 0)
    print(f"records added with an empty examples array (needs_review): {empty_added}")
    print(f"conflicts (existing 'examples' differs from source): {len(plan['conflicts'])}")

    if plan["conflicts"]:
        print("CONFLICT DETAILS:")
        for c in plan["conflicts"][:10]:
            print(f"  id={c['id']}")
        fail("refusing to overwrite existing 'examples' with conflicting values")

    if args.dry_run:
        print("=== DRY RUN: no files written ===")
        return

    changed_by_level = {n: 0 for n in PRODUCTION_PATHS}
    for prod_r, targets in plan["to_add"]:
        prod_r["examples"] = targets
        changed_by_level[level_from_id(prod_r["id"])] += 1

    for n, path in PRODUCTION_PATHS.items():
        if changed_by_level[n] == 0:
            print(f"HSK{n}: 0 records changed, file not rewritten")
            continue
        output_text = serialize_like_source(production_by_level[n])
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(output_text)
        print(f"HSK{n}: {changed_by_level[n]} record(s) updated, file rewritten")

    print(f"=== APPLIED: {len(plan['to_add'])} production record(s) updated across "
          f"{sum(1 for c in changed_by_level.values() if c > 0)} file(s) ===")
    print("Source artifacts (pilot + batch files) were not written to.")


if __name__ == "__main__":
    main()
