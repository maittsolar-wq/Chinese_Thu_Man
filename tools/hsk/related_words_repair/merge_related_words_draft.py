"""
Related Words Pass 02 -- production integration merge script.

Mirrors the established integration pattern from
tools/hsk/examples/merge_hsk_examples_p104.py and
tools/hsk/stroke_count/merge_stroke_count_p03.py: fail-closed,
deterministic-by-ID, dry-run/apply modes, never silently overwrites,
never touches anything outside its declared write target.

Source artifact (READ-ONLY, never written by this script):
    tools/hsk/related_words_repair/related_words_draft.json
    (already validated: 11/11 checks pass, deterministic across two
    independent runs)

Production targets (the ONLY files this script may write, and the ONLY
field within them this script may change -- `relatedWordIds`):
    data/hsk/hsk{1..6}/hsk{1..6}_vocabulary_production.json

Only records whose production `relatedWordIds` is CURRENTLY EMPTY and
which appear in the draft's `changes` list are modified. HSK6 never
appears in the draft (see build_related_words_draft.py's docstring) and
is therefore never touched by this script either.

Usage:
    python merge_related_words_draft.py --dry-run
    python merge_related_words_draft.py --apply
"""
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DRAFT_PATH = Path(__file__).resolve().parent / "related_words_draft.json"

PRODUCTION_PATHS = {
    n: REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
    for n in (1, 2, 3, 4, 5, 6)
}
EXPECTED_PRODUCTION_COUNTS = {1: 300, 2: 200, 3: 500, 4: 1000, 5: 1600, 6: 1800}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def load_json_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def load_draft() -> dict[str, list[str]]:
    if not DRAFT_PATH.exists():
        fail(f"draft artifact not found: {DRAFT_PATH}")
    doc = json.loads(load_json_text(DRAFT_PATH))
    changes = doc["changes"]
    by_id = {}
    for c in changes:
        rid = c["id"]
        if rid in by_id:
            fail(f"duplicate id '{rid}' in draft changes -- refusing to proceed")
        if c["oldRelatedWordIds"]:
            fail(f"draft change for '{rid}' has non-empty oldRelatedWordIds -- refusing (must only fill empty records)")
        if c["hskLevel"] == 6:
            fail(f"draft contains an HSK6 change ('{rid}') -- HSK6 must never be touched by this pass")
        by_id[rid] = c["newRelatedWordIds"]
    return by_id


def load_production() -> dict[int, list]:
    production_by_level = {}
    for n, path in PRODUCTION_PATHS.items():
        records = json.loads(load_json_text(path))
        if len(records) != EXPECTED_PRODUCTION_COUNTS[n]:
            fail(f"HSK{n} production record count {len(records)} != expected {EXPECTED_PRODUCTION_COUNTS[n]}")
        production_by_level[n] = records
    return production_by_level


def compute_plan(production_by_level: dict, draft_by_id: dict) -> dict:
    to_update = []
    unexpected_nonempty = []
    missing_from_production = set(draft_by_id.keys())

    for n, records in production_by_level.items():
        for r in records:
            rid = r["id"]
            if rid not in draft_by_id:
                continue
            missing_from_production.discard(rid)
            existing = r.get("relatedWordIds")
            if existing:
                unexpected_nonempty.append({"id": rid, "existing": existing})
                continue
            to_update.append((r, draft_by_id[rid]))

    return {
        "to_update": to_update,
        "unexpected_nonempty": unexpected_nonempty,
        "missing_from_production": sorted(missing_from_production),
    }


def serialize_like_source(records: list) -> str:
    text = json.dumps(records, indent=2, ensure_ascii=False)
    text = text.replace("\n", "\r\n")
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    draft_by_id = load_draft()
    production_by_level = load_production()
    plan = compute_plan(production_by_level, draft_by_id)

    print("=== Related Words Pass 02 merge plan ===")
    print(f"total draft changes (approved, selected-only): {len(draft_by_id)}")
    print(f"records that would change: {len(plan['to_update'])}")
    print(f"draft ids not found in any production file: {len(plan['missing_from_production'])}")
    print(f"records already unexpectedly non-empty (would NOT be overwritten): {len(plan['unexpected_nonempty'])}")

    if plan["missing_from_production"]:
        fail(f"{len(plan['missing_from_production'])} draft id(s) not found in production: "
             f"{plan['missing_from_production'][:10]}")

    if plan["unexpected_nonempty"]:
        print("UNEXPECTED NON-EMPTY RECORDS (reported, not overwritten):")
        for c in plan["unexpected_nonempty"][:10]:
            print(f"  id={c['id']} existing={c['existing']}")
        fail(f"refusing to proceed: {len(plan['unexpected_nonempty'])} record(s) changed state since the draft "
             f"was built (now non-empty) -- regenerate the draft against current production before integrating")

    if len(plan["to_update"]) != len(draft_by_id):
        fail(f"plan would update {len(plan['to_update'])} record(s), expected exactly {len(draft_by_id)}")

    if args.dry_run:
        print("=== DRY RUN: no files written ===")
        return

    changed_by_level = {n: 0 for n in PRODUCTION_PATHS}
    for prod_r, new_related in plan["to_update"]:
        prod_r["relatedWordIds"] = new_related
        lvl = int(prod_r["id"].split("_")[0].replace("hsk", ""))
        changed_by_level[lvl] += 1

    for n, path in PRODUCTION_PATHS.items():
        if changed_by_level[n] == 0:
            print(f"HSK{n}: 0 records changed, file not rewritten")
            continue
        output_text = serialize_like_source(production_by_level[n])
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(output_text)
        print(f"HSK{n}: {changed_by_level[n]} record(s) updated, file rewritten")

    print(f"=== APPLIED: {len(plan['to_update'])} production record(s) updated ===")
    print("Draft artifact was not written to.")


if __name__ == "__main__":
    main()
