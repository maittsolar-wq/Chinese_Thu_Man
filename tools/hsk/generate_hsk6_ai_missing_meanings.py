#!/usr/bin/env python3
"""Generate AI-assisted Vietnamese meaning candidates for unresolved HSK 6 records.

Input:
    data/hsk/hsk6/hsk6_ai_missing_meanings_input.json

Output:
    data/hsk/hsk6/hsk6_ai_missing_meanings_candidates.json

This script is intentionally deterministic/offline: it does NOT call an AI API.
It prepares a strict generation package with one request per unresolved word.
Use it as the input for the project's AI generation step, then merge the
returned candidates. It never modifies reviewed or production data.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk6"
INPUT = DATA / "hsk6_ai_missing_meanings_input.json"
OUTPUT = DATA / "hsk6_ai_missing_meanings_candidates.json"
EXPECTED_MISSING = 1292


def main():
    print("=" * 72)
    print("HSK 6 AI MISSING MEANINGS — GENERATION INPUT")
    print("=" * 72)
    print()

    if not INPUT.exists():
        raise SystemExit(f"Missing input: {INPUT}")

    records = json.loads(INPUT.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise SystemExit("AI missing input must be a JSON array.")

    if len(records) != EXPECTED_MISSING:
        raise SystemExit(
            f"Expected {EXPECTED_MISSING} unresolved records, got {len(records)}."
        )

    requests = []
    for r in records:
        rid = str(r.get("id") or "").strip()
        word = str(r.get("word") or "").strip()
        pinyin = str(r.get("pinyin") or "").strip()

        if not rid or not word or not pinyin:
            raise SystemExit(
                f"Invalid unresolved record: id={rid!r}, word={word!r}, "
                f"pinyin={pinyin!r}"
            )

        requests.append({
            "id": rid,
            "word": word,
            "pinyin": pinyin,
            "task": "Generate Vietnamese meaning candidate",
            "constraints": [
                "Return concise natural Vietnamese meaning(s).",
                "Prefer the most common HSK 6 learner-facing sense.",
                "Respect the word's part of speech and pinyin.",
                "Do not invent cultural or contextual information.",
                "Candidate only; not ground truth.",
            ],
            "generationStatus": "pending",
            "verificationStatus": "unverified",
            "humanVerified": False,
        })

    OUTPUT.write_text(
        json.dumps(requests, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Input unresolved records:  {len(records)}/{EXPECTED_MISSING}")
    print(f"AI generation requests:     {len(requests)}/{EXPECTED_MISSING}")
    print("AI API called:              NO")
    print("Ground truth:               NOT INCLUDED")
    print("Reviewed data modified:     NO")
    print("Production data modified:   NO")
    print(f"Output:                     {OUTPUT}")
    print()
    print("SUCCESS")
    print("HSK 6 AI-assisted meaning generation package prepared.")
    print()
    print("Next step: generate candidates for these 1292 records,")
    print("then merge them into hsk6_meanings_candidates_input.json.")
    print("All AI-assisted meanings must remain explicitly unverified.")


if __name__ == "__main__":
    main()
