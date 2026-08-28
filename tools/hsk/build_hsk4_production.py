#!/usr/bin/env python3
"""Build HSK 4 production dataset after final validation."""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk4"
REVIEWED = DATA / "hsk4_vocabulary_reviewed.json"
VALIDATION = DATA / "hsk4_final_production_validation.json"
OUTPUT = DATA / "hsk4_vocabulary_production.json"
EXPECTED_COUNT = 1000


def load(path):
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def main():
    print("=" * 72)
    print("HSK 4 PRODUCTION BUILD")
    print("=" * 72)
    print()

    validation = load(VALIDATION)

    if validation.get("status") != "PASS":
        raise SystemExit(
            "Production build blocked: final validation is not PASS."
        )

    records = load(REVIEWED)

    if not isinstance(records, list) or len(records) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} reviewed records."
        )

    production = []

    for record in records:
        item = dict(record)
        item["dataStatus"] = "production"
        item["sourceDataset"] = "hsk4_vocabulary_reviewed.json"

        item["translationAccuracyVerified"] = (
            item.get("reviewed") is True
            and item.get("verificationMode")
            not in {
                "ai_assisted_unverified",
                "needs_manual_verification",
            }
        )

        production.append(item)

    OUTPUT.write_text(
        json.dumps(production, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    human = sum(
        r.get("translationAccuracyVerified") is True
        for r in production
    )
    ai = sum(
        r.get("verificationMode") == "ai_assisted_unverified"
        for r in production
    )
    manual = sum(
        r.get("verificationMode") == "needs_manual_verification"
        for r in production
    )

    print(f"Production records:         {len(production)}/{EXPECTED_COUNT}")
    print(f"Human-verified records:     {human}")
    print(f"AI-assisted unverified:     {ai}")
    print(f"Manual verification:        {manual}")
    print(f"Output:                     {OUTPUT}")
    print()
    print("SUCCESS")
    print("HSK 4 production dataset created.")
    print("Verification metadata preserved.")
    print("AI-assisted meanings were NOT marked as human-verified.")


if __name__ == "__main__":
    main()
