#!/usr/bin/env python3
"""Build HSK 2 production dataset after final validation.

Input:
    data/hsk/hsk2/hsk2_vocabulary_reviewed.json
    data/hsk/hsk2/hsk2_final_production_validation.json

Output:
    data/hsk/hsk2/hsk2_vocabulary_production.json

The production file preserves verification metadata.
AI-assisted meanings are NOT relabeled as human-reviewed.
The build is blocked if final validation has not passed.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk2"

REVIEWED = DATA_DIR / "hsk2_vocabulary_reviewed.json"
VALIDATION = DATA_DIR / "hsk2_final_production_validation.json"
OUTPUT = DATA_DIR / "hsk2_vocabulary_production.json"

EXPECTED_COUNT = 200


def load_json(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def main():
    print("=" * 72)
    print("HSK 2 PRODUCTION BUILD")
    print("=" * 72)
    print()

    validation = load_json(VALIDATION)

    if validation.get("status") != "PASS":
        raise SystemExit(
            "Production build blocked: final validation is not PASS."
        )

    records = load_json(REVIEWED)

    if not isinstance(records, list) or len(records) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} reviewed records."
        )

    production = []

    for record in records:
        # Production is a clean copy, while preserving verification metadata.
        item = dict(record)

        item["dataStatus"] = "production"
        item["sourceDataset"] = "hsk2_vocabulary_reviewed.json"

        if item.get("verificationMode") == "ai_assisted_unverified":
            item["translationAccuracyVerified"] = False
        else:
            item["translationAccuracyVerified"] = (
                item.get("reviewed") is True
            )

        production.append(item)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(production, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    human = sum(
        r.get("translationAccuracyVerified") is True
        for r in production
    )
    ai_unverified = sum(
        r.get("verificationMode") == "ai_assisted_unverified"
        for r in production
    )

    print(f"Production records:         {len(production)}/{EXPECTED_COUNT}")
    print(f"Human-verified records:     {human}")
    print(f"AI-assisted unverified:     {ai_unverified}")
    print(f"Output:                     {OUTPUT}")
    print()
    print("SUCCESS")
    print("HSK 2 production dataset created.")
    print("Verification metadata preserved.")
    print("AI-assisted meanings were NOT marked as human-verified.")


if __name__ == "__main__":
    main()
