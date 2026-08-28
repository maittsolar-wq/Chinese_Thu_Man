#!/usr/bin/env python3
"""Build HSK 6 production data after the final validation gate.

Inputs:
    data/hsk/hsk6/hsk6_vocabulary_reviewed.json
    data/hsk/hsk6/hsk6_final_production_validation.json

Output:
    data/hsk/hsk6/hsk6_vocabulary_production.json

This build preserves verification metadata exactly as supplied by the
reviewed dataset. AI-assisted/unverified meanings are NOT converted into
human-verified meanings.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk6"

REVIEWED = DATA / "hsk6_vocabulary_reviewed.json"
VALIDATION = DATA / "hsk6_final_production_validation.json"
OUTPUT = DATA / "hsk6_vocabulary_production.json"

EXPECTED = 1800


def main():
    print("=" * 72)
    print("HSK 6 PRODUCTION BUILD")
    print("=" * 72)
    print()

    if not REVIEWED.exists():
        raise SystemExit(f"Missing reviewed dataset: {REVIEWED}")

    if not VALIDATION.exists():
        raise SystemExit(
            f"Missing final production validation report: {VALIDATION}"
        )

    reviewed = json.loads(REVIEWED.read_text(encoding="utf-8"))
    validation = json.loads(VALIDATION.read_text(encoding="utf-8"))

    if not isinstance(reviewed, list):
        raise SystemExit("Reviewed dataset must be a JSON array.")

    if len(reviewed) != EXPECTED:
        raise SystemExit(
            f"Reviewed records must be {EXPECTED}; got {len(reviewed)}."
        )

    if validation.get("status") != "PASS":
        raise SystemExit(
            "Final production validation is not PASS. "
            "Production build is blocked."
        )

    if validation.get("productionBuildAllowed") is not True:
        raise SystemExit(
            "Production build is not allowed by the final validation gate."
        )

    # Verify the exact ID sequence before writing production.
    expected_ids = [f"hsk6_{i:04d}" for i in range(1, EXPECTED + 1)]
    ids = [str(r.get("id")) for r in reviewed]

    if ids != expected_ids:
        raise SystemExit(
            "Reviewed IDs are not exactly hsk6_0001..hsk6_1800."
        )

    # Final safety checks: production must not manufacture verification.
    for r in reviewed:
        if r.get("humanVerified") is True:
            # This is allowed if it genuinely exists in reviewed data.
            # We preserve it rather than changing it.
            continue

        if str(r.get("verificationStatus") or "").strip().lower() != "unverified":
            raise SystemExit(
                f"{r.get('id')}: non-human-verified record has an invalid "
                "verificationStatus."
            )

        if r.get("autoApproved") is True:
            raise SystemExit(
                f"{r.get('id')}: autoApproved must not be true."
            )

    # Copy records without changing verification metadata.
    production = [dict(r) for r in reviewed]

    OUTPUT.write_text(
        json.dumps(production, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    human_verified = sum(
        1 for r in production if r.get("humanVerified") is True
    )
    ai_unverified = sum(
        1 for r in production
        if str(r.get("verificationStatus") or "").strip().lower()
        == "unverified"
    )

    print(f"Production records:         {len(production)}/{EXPECTED}")
    print(f"Human-verified records:     {human_verified}")
    print(f"AI-assisted unverified:     {ai_unverified}")
    print(f"Output:                     {OUTPUT}")
    print()
    print("SUCCESS")
    print("HSK 6 production dataset created.")
    print("Verification metadata preserved.")
    print("AI-assisted meanings were NOT marked as human-verified.")


if __name__ == "__main__":
    main()
