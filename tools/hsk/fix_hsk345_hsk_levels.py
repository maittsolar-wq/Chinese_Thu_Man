#!/usr/bin/env python3
"""Fix incorrect cumulative hskLevels on HSK3/4/5 reviewed data.

Root cause: build_hsk{3,4,5}_vocabulary_base.py previously overwrote the
correctly-parsed source levels with a synthetic cumulative range (e.g. HSK3
records always got [1,2,3] regardless of what the source actually said).
That bug is fixed in the base builders, but the already-populated
hsk{3,4,5}_vocabulary_reviewed.json files still carry the old cumulative
values (complete_hsk{N}_reviewed*.py never revisits an id that is already
present in the reviewed file).

This script recomputes hskLevels for every hsk3/4/5 reviewed record
directly from that same record's own `sourceLevelName` field (already
embedded, verbatim from the source CSV, on every record) using the exact
same level-name mapping the base builders use. No new data is invented and
no data is re-fetched.

Only the `hskLevels` field is modified. Every other field, and record
order, is left byte-identical.

Input / output (same file, in place):
    data/hsk/hsk3/hsk3_vocabulary_reviewed.json
    data/hsk/hsk4/hsk4_vocabulary_reviewed.json
    data/hsk/hsk5/hsk5_vocabulary_reviewed.json
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

LEVEL_MAPPING = {
    "一级": 1,
    "二级": 2,
    "三级": 3,
    "四级": 4,
    "五级": 5,
    "六级": 6,
    "七-九级": 7,
}

EXPECTED_COUNTS = {3: 500, 4: 1000, 5: 1600}


def parse_all_hsk_levels(level_name: str) -> list[int]:
    level_name = level_name or ""
    return sorted(
        {
            level
            for label, level in LEVEL_MAPPING.items()
            if label in level_name
        }
    )


def fix_level(level: int) -> dict:
    data_dir = ROOT / "data" / "hsk" / f"hsk{level}"
    path = data_dir / f"hsk{level}_vocabulary_reviewed.json"

    if not path.exists():
        raise SystemExit(f"Missing input: {path}")

    records = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(records, list):
        raise SystemExit(f"{path}: root must be a JSON array.")

    expected_count = EXPECTED_COUNTS[level]

    if len(records) != expected_count:
        raise SystemExit(
            f"{path}: expected {expected_count} records, got {len(records)}."
        )

    changed = 0
    unchanged = 0
    mismatches = []

    for record in records:
        if not isinstance(record, dict):
            raise SystemExit(f"{path}: found a non-object record.")

        rid = record.get("id")
        source_level_name = record.get("sourceLevelName")

        if not source_level_name:
            raise SystemExit(f"{rid}: missing sourceLevelName.")

        recomputed = parse_all_hsk_levels(source_level_name)

        if not recomputed:
            raise SystemExit(
                f"{rid}: could not recompute hskLevels from "
                f"sourceLevelName={source_level_name!r}."
            )

        if record.get("introducedLevel") not in recomputed:
            raise SystemExit(
                f"{rid}: recomputed hskLevels {recomputed} does not "
                f"contain introducedLevel={record.get('introducedLevel')}."
            )

        current = record.get("hskLevels")

        if current == recomputed:
            unchanged += 1
            continue

        record["hskLevels"] = recomputed
        changed += 1
        mismatches.append(
            {
                "id": rid,
                "sourceLevelName": source_level_name,
                "before": current,
                "after": recomputed,
            }
        )

    path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "level": level,
        "totalRecords": len(records),
        "changed": changed,
        "unchanged": unchanged,
        "sampleChanges": mismatches[:5],
    }


def main():
    print("=" * 72)
    print("HSK 3/4/5 hskLevels CORRECTION (reviewed data)")
    print("=" * 72)
    print()

    results = [fix_level(level) for level in (3, 4, 5)]

    for result in results:
        print(f"HSK{result['level']}:")
        print(f"  Total records:   {result['totalRecords']}")
        print(f"  hskLevels fixed: {result['changed']}")
        print(f"  Already correct: {result['unchanged']}")
        print()

    print("SUCCESS")
    print("Only the hskLevels field was modified on each reviewed record.")
    print("No production data was created.")


if __name__ == "__main__":
    main()
