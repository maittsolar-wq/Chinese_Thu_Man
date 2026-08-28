#!/usr/bin/env python3
"""
Generate a clean AI-meaning-candidate INPUT package for HSK 1.

IMPORTANT:
- This script does NOT call an AI API.
- It does NOT invent or translate meanings.
- It creates a machine-readable input package from the HSK 1 BASE dataset.
- The package is intentionally independent from reviewed/production data.
- It is the safe first stage before connecting an AI provider.

Run from project root:
    python tools/hsk/generate_hsk1_ai_meaning_candidates.py

Output:
    data/hsk/hsk1/hsk1_ai_meaning_candidates_input.json
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk1"

BASE_FILE = DATA_DIR / "hsk1_vocabulary_base.json"
OUTPUT_FILE = DATA_DIR / "hsk1_ai_meaning_candidates_input.json"

EXPECTED_COUNT = 300


def load_json(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def extract_records(data):
    if isinstance(data, list):
        return data

    if isinstance(data, dict) and isinstance(data.get("records"), list):
        return data["records"]

    raise SystemExit(
        "Base vocabulary must be a JSON array or an object containing "
        "a 'records' array."
    )


def main():
    print("=" * 64)
    print("HSK 1 AI MEANING CANDIDATE INPUT BUILD")
    print("=" * 64)
    print()

    base_data = load_json(BASE_FILE)
    base_records = extract_records(base_data)

    if len(base_records) != EXPECTED_COUNT:
        raise SystemExit(
            f"Base records = {len(base_records)}, expected {EXPECTED_COUNT}."
        )

    output_records = []
    seen_ids = set()

    for record in base_records:
        if not isinstance(record, dict):
            raise SystemExit("Base contains a non-object record.")

        record_id = record.get("id")
        word = str(record.get("word", "")).strip()
        pinyin = str(record.get("pinyin", "")).strip()

        if not record_id:
            raise SystemExit("Base record missing id.")

        if record_id in seen_ids:
            raise SystemExit(f"Duplicate base ID: {record_id}")
        seen_ids.add(record_id)

        if not word:
            raise SystemExit(f"{record_id}: empty word.")

        if not pinyin:
            raise SystemExit(f"{record_id}: empty Pinyin.")

        # Only source facts needed by the AI generation stage.
        # No reviewed meaning is copied here. This prevents accidental
        # leakage of the human-reviewed ground truth into the AI candidate.
        output_records.append(
            {
                "id": record_id,
                "word": word,
                "pinyin": pinyin,
                "introducedLevel": record.get("introducedLevel"),
                "hskLevels": record.get("hskLevels", []),
                "partOfSpeech": record.get("partOfSpeech", []),
                "partOfSpeechSource": record.get("partOfSpeechSource"),
                "sourceSort": record.get("sourceSort"),
                "aiCandidate": {
                    "meaningVi": [],
                    "source": "ai",
                    "model": None,
                    "modelVersion": None,
                    "generatedAt": None,
                    "confidence": None,
                    "reasoning": None,
                },
                "reviewStatus": "not_generated",
            }
        )

    payload = {
        "datasetName": "Chinese Thu Man HSK 1",
        "type": "AI_MEANING_CANDIDATE_INPUT",
        "version": 1,
        "recordCount": len(output_records),
        "groundTruthIncluded": False,
        "productionIncluded": False,
        "records": output_records,
    }

    OUTPUT_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Base records:       {len(base_records)}/{EXPECTED_COUNT}")
    print(f"Candidate inputs:   {len(output_records)}/{EXPECTED_COUNT}")
    print(f"Ground truth:       NOT INCLUDED")
    print(f"Production data:    NOT INCLUDED")
    print(f"Output:             {OUTPUT_FILE}")
    print()
    print("SUCCESS")
    print("AI candidate input package created.")
    print("No reviewed or production data was modified.")
    print()
    print("IMPORTANT:")
    print("This file contains EMPTY AI meaning slots by design.")
    print("The next step is the AI generation adapter, not manual editing.")


if __name__ == "__main__":
    main()
