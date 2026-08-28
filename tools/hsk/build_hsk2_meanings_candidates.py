#!/usr/bin/env python3
"""Prepare HSK 2 records for AI-assisted Vietnamese meaning generation.

Run from project root:
    python tools/hsk/build_hsk2_meanings_candidates.py

Input:
    data/hsk/hsk2/hsk2_vocabulary_base.json

Output:
    data/hsk/hsk2/hsk2_meanings_candidates_input.json

This script does NOT call an AI API and does NOT invent meanings.
It creates a clean, provider-neutral input package that can be processed
in batches by an AI assistant without requiring an API key.

The output contains the information needed to generate Vietnamese
meaning candidates:
    - id
    - Chinese word
    - Pinyin
    - part of speech
    - HSK level
    - source order

No reviewed or production data is modified.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

INPUT = (
    ROOT
    / "data"
    / "hsk"
    / "hsk2"
    / "hsk2_vocabulary_base.json"
)

OUTPUT = (
    ROOT
    / "data"
    / "hsk"
    / "hsk2"
    / "hsk2_meanings_candidates_input.json"
)

EXPECTED_COUNT = 200


def main():
    print("=" * 64)
    print("HSK 2 MEANING CANDIDATES INPUT BUILD")
    print("=" * 64)
    print()

    if not INPUT.exists():
        raise SystemExit(
            f"Missing input: {INPUT}\n"
            "Run build_hsk2_vocabulary_base.py first."
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

        if record["introducedLevel"] != 2:
            raise SystemExit(
                f"Record {record['id']} has "
                f"introducedLevel={record['introducedLevel']}, "
                "expected 2."
            )

        candidate_inputs.append(
            {
                "id": record["id"],
                "word": record["word"],
                "pinyin": record["pinyin"],
                "partOfSpeech": record["partOfSpeech"],
                "partOfSpeechSource": record.get(
                    "partOfSpeechSource"
                ),
                "introducedLevel": 2,
                "hskLevels": record.get(
                    "hskLevels",
                    [2],
                ),
                "sourceSort": record["sourceSort"],
                "sourceLevelName": record.get(
                    "sourceLevelName"
                ),

                # AI output slots.
                # These remain empty until an AI-assisted generation step
                # is actually performed.
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

    print(
        f"Input records:       {len(records)}"
    )
    print(
        f"Candidate inputs:    {len(candidate_inputs)}"
    )
    print(
        "Generation status:   pending"
    )
    print(
        "AI API called:       NO"
    )
    print(
        "Ground truth:        NOT INCLUDED"
    )
    print(
        "Reviewed data:       NOT INCLUDED"
    )
    print(
        "Production data:     NOT INCLUDED"
    )
    print(
        f"Output:              {OUTPUT}"
    )
    print()
    print("SUCCESS")
    print(
        "HSK 2 AI meaning candidate input package created."
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
