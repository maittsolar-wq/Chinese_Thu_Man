#!/usr/bin/env python3
"""Build HSK 2 Vietnamese meaning candidates from the HSK 2 base dataset.

Run from project root:
    python tools/hsk/build_hsk2_meanings_draft.py

Input:
    data/hsk/hsk2/hsk2_vocabulary_base.json

Output:
    data/hsk/hsk2/hsk2_meanings_draft.json

This script prepares the meanings-review layer only.
It does not modify HSK 2 base data, reviewed data, or production data.

Important:
- meaningVi is kept empty until meanings are reviewed.
- candidateMeanings is populated from source metadata only when
  a Vietnamese meaning source is already available in the base record.
- No AI API is called.
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
    / "hsk2_meanings_draft.json"
)

EXPECTED_COUNT = 200


def main():
    print("=" * 64)
    print("HSK 2 MEANINGS DRAFT BUILD")
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
            f"Expected {EXPECTED_COUNT} base records, "
            f"got {len(records)}."
        )

    draft_records = []

    for record in records:
        if not isinstance(record, dict):
            raise SystemExit(
                "Invalid base record: expected object."
            )

        record_id = record.get("id")

        # Candidate meanings are intentionally empty here.
        # The actual Vietnamese meaning generation/review layer
        # will populate them later.
        draft_records.append(
            {
                "id": record_id,
                "word": record.get("word"),
                "sourceWord": record.get("sourceWord"),
                "pinyin": record.get("pinyin"),
                "introducedLevel": record.get(
                    "introducedLevel"
                ),
                "hskLevels": record.get(
                    "hskLevels",
                    [],
                ),
                "partOfSpeechSource": record.get(
                    "partOfSpeechSource"
                ),
                "partOfSpeech": record.get(
                    "partOfSpeech",
                    [],
                ),
                "sourceSort": record.get(
                    "sourceSort"
                ),
                "sourceLevelName": record.get(
                    "sourceLevelName"
                ),

                # Meaning workflow fields.
                "candidateMeanings": [],
                "selectedMeaningVi": None,
                "reviewNotes": "",
                "reviewed": False,
            }
        )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            draft_records,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Input records:      {len(records)}"
    )
    print(
        f"Draft records:      {len(draft_records)}"
    )
    print(
        "Candidate meanings: 0"
    )
    print(
        "Reviewed:           0"
    )
    print(
        "Production data:    NOT INCLUDED"
    )
    print(
        f"Output:             {OUTPUT}"
    )
    print()
    print("SUCCESS")
    print("HSK 2 meaning draft package created.")
    print()
    print("No AI API was called.")
    print(
        "No HSK 2 base, reviewed, or production data "
        "was modified."
    )


if __name__ == "__main__":
    main()
