"""
Stroke Count Pass 03 -- Production Integration merge script.

Mirrors the established integration pattern from
tools/hsk/examples/merge_hsk_examples_p104.py: fail-closed,
deterministic-by-ID, dry-run/apply modes, never silently overwrites,
never touches anything outside its declared write target.

Source artifact (READ-ONLY, never written by this script):
    tools/hsk/stroke_count/vocabulary_stroke_draft.json
    (the Pass 02 draft, already reviewed and approved -- 5400/5400
    records resolved, 100% coverage, 0 review-queue items)

Production targets (the ONLY files this script may write, and the ONLY
field within them this script may change -- `strokeCount`):
    data/hsk/hsk{1..6}/hsk{1..6}_vocabulary_production.json

Schema note: unlike `examples` (P5.10.4), `strokeCount` already EXISTS
as a key (always `null`) on every HSK1-5 record; it is ABSENT entirely
on every HSK6 record (confirmed in Pass 01/02 inspection). This script
therefore UPDATES the key on HSK1-5 and ADDS it on HSK6 -- both are
"this record's strokeCount goes from not-yet-populated to populated",
just represented differently in the two schema variants already present
in production, exactly as-is; this script does not unify or reshape
that pre-existing schema difference.

ID mapping: every draft record's `id` is used verbatim as the
production `id` to update -- never by word text, never by array
position.

Usage:
    python merge_stroke_count_p03.py --dry-run
    python merge_stroke_count_p03.py --apply
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
STROKE_COUNT_DIR = REPO_ROOT / "tools" / "hsk" / "stroke_count"
DRAFT_PATH = STROKE_COUNT_DIR / "vocabulary_stroke_draft.json"

PRODUCTION_PATHS = {
    n: REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
    for n in (1, 2, 3, 4, 5, 6)
}

EXPECTED_PRODUCTION_COUNTS = {1: 300, 2: 200, 3: 500, 4: 1000, 5: 1600, 6: 1800}
EXPECTED_TOTAL = 5400


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


def load_draft() -> dict:
    if not DRAFT_PATH.exists():
        fail(f"approved draft artifact not found: {DRAFT_PATH}")
    doc = json.loads(load_json_text(DRAFT_PATH))
    summary = doc["summary"]
    records = doc["records"]

    if summary["totalRecords"] != EXPECTED_TOTAL:
        fail(f"draft totalRecords {summary['totalRecords']} != expected {EXPECTED_TOTAL}")
    if summary["resolvedCount"] != EXPECTED_TOTAL or summary["unresolvedCount"] != 0:
        fail(f"draft is not fully resolved: resolved={summary['resolvedCount']} "
             f"unresolved={summary['unresolvedCount']} -- refusing to integrate a partial draft")
    if summary["coveragePercent"] != 100.0:
        fail(f"draft coverage {summary['coveragePercent']}% != 100% -- refusing to integrate")

    by_id = {}
    seen = set()
    for r in records:
        rid = r["id"]
        if rid in seen:
            fail(f"duplicate id '{rid}' found within the draft artifact -- refusing to proceed")
        seen.add(rid)
        if r["status"] != "resolved":
            fail(f"record {rid} has status '{r['status']}', expected 'resolved'")
        stroke_count = r["strokeCount"]
        if not isinstance(stroke_count, int) or isinstance(stroke_count, bool) or stroke_count <= 0:
            fail(f"record {rid} has invalid draft strokeCount value: {stroke_count!r}")
        by_id[rid] = stroke_count

    if len(by_id) != EXPECTED_TOTAL:
        fail(f"internal inconsistency: {len(by_id)} unique draft ids vs {EXPECTED_TOTAL} expected")

    return by_id


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


def compute_plan(production_by_level: dict, draft_by_id: dict) -> dict:
    to_update = []
    unexpected_prepopulated = []
    missing_from_draft = []

    all_production_ids = set()
    for n, records in production_by_level.items():
        for r in records:
            rid = r["id"]
            all_production_ids.add(rid)
            if rid not in draft_by_id:
                missing_from_draft.append(rid)
                continue

            existing = r.get("strokeCount", None)
            if existing is not None:
                unexpected_prepopulated.append({"id": rid, "existing": existing, "incoming": draft_by_id[rid]})
                continue

            to_update.append((r, draft_by_id[rid]))

    unknown_in_draft = set(draft_by_id.keys()) - all_production_ids
    return {
        "to_update": to_update,
        "unexpected_prepopulated": unexpected_prepopulated,
        "missing_from_draft": missing_from_draft,
        "unknown_in_draft": sorted(unknown_in_draft),
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

    draft_by_id = load_draft()
    production_by_level = load_production()

    plan = compute_plan(production_by_level, draft_by_id)

    print("=== Stroke Count Pass 03 merge plan ===")
    print(f"total draft records (approved, resolved): {len(draft_by_id)}")
    print(f"records that would change (populate strokeCount): {len(plan['to_update'])}")
    print(f"records missing from draft (would remain unpopulated): {len(plan['missing_from_draft'])}")
    print(f"draft ids not found in any production file: {len(plan['unknown_in_draft'])}")
    print(f"records already unexpectedly pre-populated: {len(plan['unexpected_prepopulated'])}")

    if plan["missing_from_draft"]:
        fail(f"{len(plan['missing_from_draft'])} production id(s) have no corresponding draft entry "
             f"-- refusing to proceed with a partial mapping: {plan['missing_from_draft'][:10]}")

    if plan["unknown_in_draft"]:
        fail(f"{len(plan['unknown_in_draft'])} draft id(s) do not correspond to any production record: "
             f"{plan['unknown_in_draft'][:10]}")

    if plan["unexpected_prepopulated"]:
        print("UNEXPECTED PRE-POPULATED RECORDS (reported per instruction, not overwritten):")
        for c in plan["unexpected_prepopulated"][:10]:
            print(f"  id={c['id']} existing={c['existing']} incoming(draft)={c['incoming']}")
        fail(f"refusing to overwrite {len(plan['unexpected_prepopulated'])} record(s) that already carry "
             f"a non-null strokeCount -- this pass's baseline assumed 0 pre-populated records")

    if len(plan["to_update"]) != EXPECTED_TOTAL:
        fail(f"plan would update {len(plan['to_update'])} record(s), expected exactly {EXPECTED_TOTAL}")

    if args.dry_run:
        print("=== DRY RUN: no files written ===")
        return

    changed_by_level = {n: 0 for n in PRODUCTION_PATHS}
    for prod_r, stroke_count in plan["to_update"]:
        prod_r["strokeCount"] = stroke_count
        changed_by_level[level_from_id(prod_r["id"])] += 1

    for n, path in PRODUCTION_PATHS.items():
        output_text = serialize_like_source(production_by_level[n])
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(output_text)
        print(f"HSK{n}: {changed_by_level[n]} record(s) updated, file rewritten")

    print(f"=== APPLIED: {len(plan['to_update'])} production record(s) updated across "
          f"{sum(1 for c in changed_by_level.values() if c > 0)} file(s) ===")
    print("Draft artifact was not written to.")


if __name__ == "__main__":
    main()
