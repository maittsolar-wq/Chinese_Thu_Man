#!/usr/bin/env python3
"""Validate HSK 5 reviewed dataset before production gate."""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk5"
BASE = DATA / "hsk5_vocabulary_base.json"
REVIEWED = DATA / "hsk5_vocabulary_reviewed.json"
REPORT = DATA / "hsk5_reviewed_validation.json"
EXPECTED = 1600


def main():
    print("=" * 72)
    print("HSK 5 REVIEWED DATA VALIDATION")
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
            f"reviewed record count is {len(reviewed)}/{EXPECTED}"
        )

    base_ids = [r.get("id") for r in base]
    reviewed_ids = [r.get("id") for r in reviewed]

    if base_ids != reviewed_ids:
        errors.append("reviewed IDs/order do not exactly match base")

    human = 0
    ai = 0
    manual = 0

    for r in reviewed:
        rid = r.get("id", "<missing>")
        word = str(r.get("word") or "").strip()
        pinyin = str(r.get("pinyin") or "").strip()
        meaning = str(r.get("meaningVi") or "").strip()
        selected = str(r.get("selectedMeaningVi") or "").strip()
        meanings = r.get("candidateMeanings", [])

        if not word:
            errors.append(f"{rid}: word is empty")
        if not pinyin:
            errors.append(f"{rid}: pinyin is empty")
        if not meaning:
            errors.append(f"{rid}: meaningVi is empty")
        if not selected:
            errors.append(f"{rid}: selectedMeaningVi is empty")
        if not isinstance(meanings, list) or not any(
            isinstance(x, str) and x.strip() for x in meanings
        ):
            errors.append(f"{rid}: candidateMeanings is empty")

        if bool(r.get("humanVerified")):
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
        warnings.append(
            "No human-verified records are present."
        )

    status = "PASS" if not errors else "FAIL"

    report = {
        "reviewedRecords": len(reviewed),
        "humanReviewed": human,
        "aiAssistedUnverified": ai,
        "manualVerification": manual,
        "errors": len(errors),
        "warnings": len(warnings),
        "status": status,
        "productionDataCreated": False,
        "errorDetails": errors,
        "warningDetails": warnings,
    }

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Reviewed records:          {len(reviewed)}/{EXPECTED}")
    print(f"Human reviewed:            {human}")
    print(f"AI-assisted unverified:    {ai}")
    print(f"Manual verification:       {manual}")
    print(f"Errors:                    {len(errors)}")
    print(f"Warnings:                  {len(warnings)}")
    print(f"Report:                    {REPORT}")
    print()
    print(f"Status: {status}")
    print()

    if errors:
        for error in errors:
            print(f"  [FAIL] {error}")
        raise SystemExit(1)

    print("PASS: HSK 5 reviewed dataset is structurally valid.")
    print("AI-assisted meanings remain explicitly unverified.")
    print("No production data was created.")


if __name__ == "__main__":
    main()
