#!/usr/bin/env python3
"""Build HSK 5 production dataset after final validation."""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk5"
REVIEWED = DATA / "hsk5_vocabulary_reviewed.json"
FINAL_VALIDATION = DATA / "hsk5_final_production_validation.json"
OUTPUT = DATA / "hsk5_vocabulary_production.json"
EXPECTED = 1600


def main():
    print("=" * 72)
    print("HSK 5 PRODUCTION BUILD")
    print("=" * 72)
    print()

    if not REVIEWED.exists():
        raise SystemExit(f"Missing reviewed: {REVIEWED}")
    if not FINAL_VALIDATION.exists():
        raise SystemExit(
            f"Missing final validation report: {FINAL_VALIDATION}"
        )

    validation = json.loads(
        FINAL_VALIDATION.read_text(encoding="utf-8")
    )

    if validation.get("status") != "PASS":
        raise SystemExit(
            "Production build blocked: final validation is not PASS."
        )

    if not validation.get("productionBuildAllowed"):
        raise SystemExit(
            "Production build blocked: productionBuildAllowed is false."
        )

    reviewed = json.loads(
        REVIEWED.read_text(encoding="utf-8")
    )

    if len(reviewed) != EXPECTED:
        raise SystemExit(
            f"Expected {EXPECTED} reviewed records, got {len(reviewed)}"
        )

    production = []

    for r in reviewed:
        item = dict(r)

        # Preserve verification metadata exactly.
        item["production"] = True
        item["humanVerified"] = bool(
            item.get("humanVerified", False)
        )

        if not item["humanVerified"]:
            item["verificationStatus"] = "unverified"
            item["productionVerification"] = (
                "ai_assisted_unverified"
            )

        production.append(item)

    OUTPUT.write_text(
        json.dumps(
            production,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    human = sum(
        1 for r in production
        if r.get("humanVerified")
    )

    ai = len(production) - human

    print(f"Production records:         {len(production)}/{EXPECTED}")
    print(f"Human-verified records:     {human}")
    print(f"AI-assisted unverified:     {ai}")
    print(f"Output:                     {OUTPUT}")
    print()
    print("SUCCESS")
    print("HSK 5 production dataset created.")
    print("Verification metadata preserved.")
    print("AI-assisted meanings were NOT marked as human-verified.")


if __name__ == "__main__":
    main()
