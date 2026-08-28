#!/usr/bin/env python3
"""Validate the HSK 6 reviewed dataset structurally.

This is a validation gate only:
- validates the 1,800-record reviewed dataset against the HSK 6 base;
- allows AI-assisted/unverified meanings;
- does NOT require human verification;
- does NOT modify reviewed or production data;
- does NOT auto-approve meanings.

Output:
    data/hsk/hsk6/hsk6_reviewed_validation.json
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk6"
BASE = DATA / "hsk6_vocabulary_base.json"
REVIEWED = DATA / "hsk6_vocabulary_reviewed.json"
REPORT = DATA / "hsk6_reviewed_validation.json"

EXPECTED = 1800


def nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def main():
    print("=" * 72)
    print("HSK 6 REVIEWED DATA VALIDATION")
    print("=" * 72)
    print()

    for path in (BASE, REVIEWED):
        if not path.exists():
            raise SystemExit(f"Missing required file: {path}")

    base = json.loads(BASE.read_text(encoding="utf-8"))
    reviewed = json.loads(REVIEWED.read_text(encoding="utf-8"))

    errors = []
    warnings = []

    if not isinstance(base, list):
        errors.append("Base file is not a JSON array.")
        base = []

    if not isinstance(reviewed, list):
        errors.append("Reviewed file is not a JSON array.")
        reviewed = []

    if len(base) != EXPECTED:
        errors.append(f"Base records: expected {EXPECTED}, got {len(base)}.")

    if len(reviewed) != EXPECTED:
        errors.append(
            f"Reviewed records: expected {EXPECTED}, got {len(reviewed)}."
        )

    base_by_id = {str(r.get("id")): r for r in base if isinstance(r, dict)}
    reviewed_by_id = {
        str(r.get("id")): r for r in reviewed if isinstance(r, dict)
    }

    expected_ids = [f"hsk6_{i:04d}" for i in range(1, EXPECTED + 1)]

    if list(reviewed_by_id.keys()) != expected_ids:
        errors.append("Reviewed IDs are not exactly hsk6_0001..hsk6_1800 in order.")

    human_verified = 0
    ai_unverified = 0
    manual_verification = 0

    for rid in expected_ids:
        b = base_by_id.get(rid)
        r = reviewed_by_id.get(rid)

        if b is None:
            errors.append(f"{rid}: missing from base.")
            continue
        if r is None:
            errors.append(f"{rid}: missing from reviewed.")
            continue

        # Base identity must not change.
        for field in ("word", "pinyin", "level"):
            if r.get(field) != b.get(field):
                errors.append(
                    f"{rid}: {field} differs from base "
                    f"({b.get(field)!r} != {r.get(field)!r})."
                )

        if r.get("level") != "HSK 6":
            errors.append(f"{rid}: level is not HSK 6.")

        if not nonempty(r.get("word")):
            errors.append(f"{rid}: word is empty.")

        if not nonempty(r.get("pinyin")):
            errors.append(f"{rid}: pinyin is empty.")

        meanings = r.get("candidateMeanings")
        if not isinstance(meanings, list):
            errors.append(f"{rid}: candidateMeanings is not a list.")
            meanings = []

        meanings = [str(x).strip() for x in meanings if str(x).strip()]

        meaning_vi = str(r.get("meaningVi") or "").strip()
        selected = str(r.get("selectedMeaningVi") or "").strip()

        if not meaning_vi:
            errors.append(f"{rid}: meaningVi is empty.")

        if not selected:
            errors.append(f"{rid}: selectedMeaningVi is empty.")

        if meanings and meaning_vi not in meanings:
            errors.append(
                f"{rid}: meaningVi is not present in candidateMeanings."
            )

        if selected and meaning_vi and selected != meaning_vi:
            errors.append(
                f"{rid}: selectedMeaningVi does not equal meaningVi."
            )

        hv = r.get("humanVerified")
        if hv is True:
            human_verified += 1
        elif hv is False:
            manual_verification += 1
        else:
            errors.append(f"{rid}: humanVerified must be boolean.")

        status = str(r.get("verificationStatus") or "").strip().lower()
        if status == "unverified":
            ai_unverified += 1
        elif hv is not True:
            warnings.append(
                f"{rid}: verificationStatus is {status!r} without human verification."
            )

        # Production must never be created by this validation step.
        if r.get("autoApproved") is True:
            errors.append(f"{rid}: autoApproved must not be true.")

    # Deduplicate warnings while preserving order.
    warnings = list(dict.fromkeys(warnings))

    report = {
        "reviewedRecords": len(reviewed),
        "humanReviewed": human_verified,
        "aiAssistedUnverified": ai_unverified,
        "manualVerification": manual_verification,
        "errors": len(errors),
        "warnings": len(warnings),
        "status": "PASS" if not errors else "FAIL",
        "productionCreated": False,
        "errorDetails": errors,
        "warningDetails": warnings[:20],
    }

    DATA.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Reviewed records:          {len(reviewed)}/{EXPECTED}")
    print(f"Human reviewed:            {human_verified}")
    print(f"AI-assisted unverified:    {ai_unverified}")
    print(f"Manual verification:       {manual_verification}")
    print(f"Errors:                    {len(errors)}")
    print(f"Warnings:                  {len(warnings)}")
    print(f"Report:                    {REPORT}")
    print()

    if errors:
        print("Status: FAIL")
        for e in errors[:30]:
            print(f"  [FAIL] {e}")
        if len(errors) > 30:
            print(f"  ... and {len(errors) - 30} more")
        raise SystemExit(1)

    print("Status: PASS")
    print()
    print("PASS: HSK 6 reviewed dataset is structurally valid.")
    print("AI-assisted meanings remain explicitly unverified.")
    print("No production data was created.")


if __name__ == "__main__":
    main()
