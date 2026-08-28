#!/usr/bin/env python3
"""Build HSK 3 AI meaning candidate input package.

Run from project root:
    python tools/hsk/build_hsk3_meanings_candidates.py

Input:
    data/hsk/hsk3/hsk3_vocabulary_base.json

Output:
    data/hsk/hsk3/hsk3_meanings_candidates_input.json

This script does NOT call an AI API and does NOT invent meanings.
It prepares provider-neutral records for AI-assisted Vietnamese
meaning generation.

No base, reviewed, or production data is modified.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

INPUT = (
    ROOT
    / "data"
    / "hsk"
    / "hsk3"
    / "hsk3_vocabulary_base.json"
)

OUTPUT = (
    ROOT
    / "data"
    / "hsk"
    / "hsk3"
    / "hsk3_meanings_candidates_input.json"
)

EXPECTED_COUNT = 500


def main():
    print("=" * 72)
    print("HSK 3 MEANING CANDIDATES INPUT BUILD")
    print("=" * 72)
    print()

    if not INPUT.exists():
        raise SystemExit(
            f"Missing input: {INPUT}\n"
            "Run build_hsk3_vocabulary_base.py first."
        )

    try:
        records = json.loads(
            INPUT.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"Invalid JSON input: {exc}"
        )

    if not isinstance(records, list):
        raise SystemExit(
            "Invalid input: root value must be a list."
        )

    if len(records) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} records, "
            f"got {len(records)}."
        )

    candidate_inputs = []

    for record in records:
        if not isinstance(record, dict):
            raise SystemExit(
                "Invalid base record: expected object."
            )

        required = [
            "id",
            "word",
            "pinyin",
            "partOfSpeech",
            "introducedLevel",
            "sourceSort",
        ]

        missing = [
            field
            for field in required
            if field not in record
        ]

        if missing:
            raise SystemExit(
                f"Record {record.get('id', '<unknown>')} "
                f"missing fields: {', '.join(missing)}"
            )

        if record["introducedLevel"] != 3:
            raise SystemExit(
                f"Record {record['id']} has "
                f"introducedLevel={record['introducedLevel']}, "
                "expected 3."
            )

        candidate_inputs.append(
            {
                "id": record["id"],
                "word": record["word"],
                "sourceWord": record.get("sourceWord"),
                "pinyin": record["pinyin"],
                "partOfSpeech": record["partOfSpeech"],
                "partOfSpeechSource": record.get(
                    "partOfSpeechSource"
                ),
                "introducedLevel": 3,
                "hskLevels": record.get(
                    "hskLevels",
                    [1, 2, 3],
                ),
                "sourceSort": record["sourceSort"],
                "sourceLevelName": record.get(
                    "sourceLevelName"
                ),

                # AI output slots.
                "candidateMeanings": [],
                "generationStatus": "pending",
            }
        )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            candidate_inputs,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Input records:       {len(records)}")
    print(f"Candidate inputs:    {len(candidate_inputs)}")
    print("Generation status:   pending")
    print("AI API called:       NO")
    print("Ground truth:        NOT INCLUDED")
    print("Reviewed data:       NOT INCLUDED")
    print("Production data:     NOT INCLUDED")
    print(f"Output:              {OUTPUT}")
    print()
    print("SUCCESS")
    print(
        "HSK 3 AI meaning candidate input package created."
    )
    print()
    print(
        "Next step: generate Vietnamese meaning candidates "
        "with AI in batches."
    )
    print(
        "No base, reviewed, or production data was modified."
    )


if __name__ == "__main__":
    main()
