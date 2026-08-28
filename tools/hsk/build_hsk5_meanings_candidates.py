#!/usr/bin/env python3
"""Prepare HSK 5 records for AI-assisted Vietnamese meaning generation.

Input:
    data/hsk/hsk5/hsk5_vocabulary_base.json

Output:
    data/hsk/hsk5/hsk5_meanings_candidates_input.json

No AI API is called and no meanings are invented.
No base, reviewed, or production data is modified.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk5"

INPUT = DATA / "hsk5_vocabulary_base.json"
OUTPUT = DATA / "hsk5_meanings_candidates_input.json"

EXPECTED_COUNT = 1600


def main():
    print("=" * 72)
    print("HSK 5 MEANING CANDIDATES INPUT BUILD")
    print("=" * 72)
    print()

    if not INPUT.exists():
        raise SystemExit(
            f"Missing input: {INPUT}\n"
            "Run build_hsk5_vocabulary_base.py first."
        )

    try:
        records = json.loads(
            INPUT.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON input: {exc}")

    if not isinstance(records, list):
        raise SystemExit("Input root must be a JSON array.")

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
            field for field in required
            if field not in record
        ]

        if missing:
            raise SystemExit(
                f"Record {record.get('id', '<unknown>')} "
                f"missing fields: {', '.join(missing)}"
            )

        if record["introducedLevel"] != 5:
            raise SystemExit(
                f"Record {record['id']} has "
                f"introducedLevel={record['introducedLevel']}, "
                "expected 5."
            )

        candidate_inputs.append({
            "id": record["id"],
            "word": record["word"],
            "sourceWord": record.get("sourceWord"),
            "pinyin": record["pinyin"],
            "partOfSpeech": record["partOfSpeech"],
            "partOfSpeechSource": record.get(
                "partOfSpeechSource"
            ),
            "introducedLevel": 5,
            "hskLevels": record.get(
                "hskLevels",
                [1, 2, 3, 4, 5],
            ),
            "sourceSort": record["sourceSort"],
            "sourceLevelName": record.get(
                "sourceLevelName"
            ),
            "candidateMeanings": [],
            "generationStatus": "pending",
        })

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
    print("HSK 5 AI meaning candidate input package created.")
    print()
    print(
        "Next step: generate Vietnamese meaning candidates "
        "with AI/reference in batches."
    )
    print("No base, reviewed, or production data was modified.")


if __name__ == "__main__":
    main()
