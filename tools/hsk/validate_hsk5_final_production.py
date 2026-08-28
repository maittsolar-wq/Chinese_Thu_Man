#!/usr/bin/env python3
"""Final structural production gate for HSK 5."""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk5"
BASE = DATA / "hsk5_vocabulary_base.json"
REVIEWED = DATA / "hsk5_vocabulary_reviewed.json"
REPORT = DATA / "hsk5_final_production_validation.json"
EXPECTED = 1600


def main():
    print("=" * 72)
    print("HSK 5 FINAL PRODUCTION VALIDATION")
    print("=" * 72)
    print()

    if not BASE.exists():
        raise SystemExit(f"Missing base: {BASE}")
    if not REVIEWED.exists():
        raise SystemExit(f"Missing reviewed: {REVIEWED}")

    base = json.loads(BASE.read_text(encoding="utf-8"))
    reviewed = json.loads(REVIEWED.read_text(encoding="utf-8"))

    errors = []
    warnings = []

    if len(reviewed) != EXPECTED:
        errors.append(
            f"reviewed records {len(reviewed)}/{EXPECTED}"
        )

    base_ids = [r.get("id") for r in base]
    reviewed_ids = [r.get("id") for r in reviewed]

    if base_ids != reviewed_ids:
        errors.append("reviewed IDs/order do not match base")

    human = 0
    ai = 0
    manual = 0

    for r in reviewed:
        rid = r.get("id", "<missing>")
        if not str(r.get("word") or "").strip():
            errors.append(f"{rid}: word is empty")
        if not str(r.get("pinyin") or "").strip():
            errors.append(f"{rid}: pinyin is empty")
        if not str(r.get("meaningVi") or "").strip():
            errors.append(f"{rid}: meaningVi is empty")
        if not str(r.get("selectedMeaningVi") or "").strip():
            errors.append(f"{rid}: selectedMeaningVi is empty")

        meanings = r.get("candidateMeanings", [])
        if not isinstance(meanings, list) or not any(
            isinstance(x, str) and x.strip() for x in meanings
        ):
            errors.append(f"{rid}: candidateMeanings is empty")

        if r.get("humanVerified"):
            human += 1
        else:
            ai += 1

        if str(r.get("verificationStatus", "")).lower() in {
            "manual_verification",
            "needs_manual_verification",
        }:
            manual += 1

    if ai:
        warnings.append(
            "AI-assisted meanings remain explicitly unverified."
        )
    if human == 0:
        warnings.append("No human-verified records are present.")

    allowed = len(errors) == 0
    report = {
        "records": len(reviewed),
        "humanReviewed": human,
        "aiAssistedUnverified": ai,
        "manualVerification": manual,
        "errors": len(errors),
        "warnings": len(warnings),
        "productionBuildAllowed": allowed,
        "status": "PASS" if allowed else "FAIL",
        "productionDataCreated": False,
        "errorDetails": errors,
        "warningDetails": warnings,
    }

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Records:                    {len(reviewed)}/{EXPECTED}")
    print(f"Human reviewed:             {human}")
    print(f"AI-assisted unverified:     {ai}")
    print(f"Manual verification:        {manual}")
    print(f"Errors:                     {len(errors)}")
    print(f"Warnings:                   {len(warnings)}")
    print(f"Production build allowed:   {'YES' if allowed else 'NO'}")
    print(f"Report:                     {REPORT}")
    print()
    print(f"Status: {'PASS' if allowed else 'FAIL'}")

    if not allowed:
        print("Final structural production gate FAILED.")
        for e in errors:
            print(f"  [FAIL] {e}")
        raise SystemExit(1)

    print("Final structural production gate passed.")
    print("AI-assisted meanings remain explicitly unverified.")
    print("No production data was created.")


if __name__ == "__main__":
    main()
