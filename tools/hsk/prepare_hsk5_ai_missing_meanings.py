#!/usr/bin/env python3
"""Prepare HSK 5 missing meanings for AI-assisted batch generation.

This does NOT call an AI API and does NOT modify reviewed/production data.
It creates a clean batch input containing only records whose
candidateMeanings are still empty.

Input:
    data/hsk/hsk5/hsk5_meanings_candidates_input.json

Output:
    data/hsk/hsk5/hsk5_ai_missing_meanings_input.json

The generated batch file is intended for the same AI-assisted meaning
generation workflow used for HSK 3/4.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk5"

INPUT = DATA / "hsk5_meanings_candidates_input.json"
OUTPUT = DATA / "hsk5_ai_missing_meanings_input.json"

EXPECTED = 1600


def main():
    print("=" * 72)
    print("HSK 5 AI MISSING MEANINGS INPUT PREPARATION")
    print("=" * 72)
    print()

    if not INPUT.exists():
        raise SystemExit(f"Missing input: {INPUT}")

    records = json.loads(
        INPUT.read_text(encoding="utf-8")
    )

    if not isinstance(records, list):
        raise SystemExit(
            "Candidate input root must be a JSON array."
        )

    if len(records) != EXPECTED:
        raise SystemExit(
            f"Expected {EXPECTED} records, got {len(records)}."
        )

    missing = []

    for record in records:
        meanings = record.get(
            "candidateMeanings",
            [],
        )

        if not isinstance(meanings, list):
            meanings = []

        meanings = [
            value.strip()
            for value in meanings
            if isinstance(value, str)
            and value.strip()
        ]

        if meanings:
            continue

        missing.append(
            {
                "id": record.get("id"),
                "level": record.get(
                    "introducedLevel"
                ),
                "word": record.get(
                    "word"
                ),
                "pinyin": record.get(
                    "pinyin"
                ),
                "task": (
                    "Generate concise Vietnamese "
                    "dictionary meanings for this "
                    "Chinese HSK 5 vocabulary item. "
                    "Prefer 1-3 common meanings. "
                    "Do not invent context-specific "
                    "meanings. Mark result as "
                    "AI-assisted and unverified."
                ),
            }
        )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            missing,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Source records:          {len(records)}/{EXPECTED}"
    )
    print(
        f"Records already resolved: "
        f"{EXPECTED - len(missing)}/{EXPECTED}"
    )
    print(
        f"Missing meanings:         "
        f"{len(missing)}"
    )
    print(
        f"Output:                   {OUTPUT}"
    )
    print()
    print("SUCCESS")
    print()
    print(
        "AI API called:            NO"
    )
    print(
        "Reviewed data modified:   NO"
    )
    print(
        "Production data modified: NO"
    )
    print()
    print(
        "Next step: generate AI-assisted Vietnamese "
        "meaning candidates for this batch."
    )


if __name__ == "__main__":
    main()
