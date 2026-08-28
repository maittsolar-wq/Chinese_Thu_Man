#!/usr/bin/env python3
"""Build the HSK 6 meaning-candidate input package.

Input:
    data/hsk/hsk6/hsk6_vocabulary_base.json

Output:
    data/hsk/hsk6/hsk6_meanings_candidates_input.json

This step ONLY packages the 1,800 HSK 6 vocabulary records for the later
Vietnamese meaning-candidate generation step. It does not invent meanings,
call an AI API, modify reviewed data, or create production data.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk6"
BASE = DATA / "hsk6_vocabulary_base.json"
OUTPUT = DATA / "hsk6_meanings_candidates_input.json"

EXPECTED = 1800


def main():
    print("=" * 72)
    print("HSK 6 MEANING CANDIDATES INPUT BUILD")
    print("=" * 72)
    print()

    if not BASE.exists():
        raise SystemExit(f"Missing HSK 6 base file: {BASE}")

    base = json.loads(BASE.read_text(encoding="utf-8"))

    if not isinstance(base, list):
        raise SystemExit("HSK 6 base must be a JSON array.")

    if len(base) != EXPECTED:
        raise SystemExit(
            f"Expected {EXPECTED} base records, got {len(base)}."
        )

    candidate_inputs = []

    for record in base:
        rid = str(record.get("id") or "").strip()
        word = str(record.get("word") or "").strip()
        pinyin = str(record.get("pinyin") or "").strip()
        level = str(record.get("level") or "").strip()

        if not rid:
            raise SystemExit("A base record has an empty id.")
        if not word:
            raise SystemExit(f"{rid}: Chinese word is empty.")
        if not pinyin:
            raise SystemExit(f"{rid}: Pinyin is empty.")
        if level != "HSK 6":
            raise SystemExit(
                f"{rid}: unexpected level {level!r}; expected 'HSK 6'."
            )

        candidate_inputs.append({
            "id": rid,
            "level": "HSK 6",
            "word": word,
            "pinyin": pinyin,
            "cixing": record.get("cixing", ""),
            "sourceSort": record.get("sourceSort", ""),
            "candidateMeanings": [],
            "selectedMeaningVi": "",
            "meaningVi": "",
            "generationStatus": "pending",
            "verificationStatus": "unverified",
            "humanVerified": False,
        })

    ids = [r["id"] for r in candidate_inputs]
    expected_ids = [f"hsk6_{i:04d}" for i in range(1, EXPECTED + 1)]

    if ids != expected_ids:
        raise SystemExit(
            "HSK 6 IDs are not sequential from hsk6_0001 to hsk6_1800."
        )

    DATA.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(candidate_inputs, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Input records:       {len(base)}")
    print(f"Candidate inputs:    {len(candidate_inputs)}")
    print("Generation status:   pending")
    print("AI API called:       NO")
    print("Ground truth:        NOT INCLUDED")
    print("Reviewed data:       NOT INCLUDED")
    print("Production data:     NOT INCLUDED")
    print(f"Output:              {OUTPUT}")
    print()
    print("SUCCESS")
    print("HSK 6 AI meaning candidate input package created.")
    print()
    print("Next step: generate Vietnamese meaning candidates with AI/reference.")
    print("No base, reviewed, or production data was modified.")


if __name__ == "__main__":
    main()
