#!/usr/bin/env python3
"""Final structural production gate for HSK 6.

Reads:
    data/hsk/hsk6/hsk6_vocabulary_base.json
    data/hsk/hsk6/hsk6_vocabulary_reviewed.json
    data/hsk/hsk6/hsk6_reviewed_validation.json

Writes:
    data/hsk/hsk6/hsk6_final_production_validation.json

This validates that the reviewed dataset is structurally safe to build into
production. It does NOT create or modify production data.
AI-assisted meanings are allowed but must remain explicitly unverified.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk6"
BASE = DATA / "hsk6_vocabulary_base.json"
REVIEWED = DATA / "hsk6_vocabulary_reviewed.json"
REVIEWED_REPORT = DATA / "hsk6_reviewed_validation.json"
REPORT = DATA / "hsk6_final_production_validation.json"

EXPECTED = 1800


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    print("=" * 72)
    print("HSK 6 FINAL PRODUCTION VALIDATION")
    print("=" * 72)
    print()

    for path in (BASE, REVIEWED, REVIEWED_REPORT):
        if not path.exists():
            raise SystemExit(f"Missing required file: {path}")

    base = load(BASE)
    reviewed = load(REVIEWED)
    reviewed_report = load(REVIEWED_REPORT)

    errors = []
    warnings = []

    if not isinstance(base, list) or len(base) != EXPECTED:
        errors.append(
            f"Base records must be {EXPECTED}; got "
            f"{len(base) if isinstance(base, list) else 'invalid'}."
        )

    if not isinstance(reviewed, list) or len(reviewed) != EXPECTED:
        errors.append(
            f"Reviewed records must be {EXPECTED}; got "
            f"{len(reviewed) if isinstance(reviewed, list) else 'invalid'}."
        )

    if reviewed_report.get("status") != "PASS":
        errors.append("Reviewed validation report is not PASS.")

    base_by_id = {str(r.get("id")): r for r in base if isinstance(r, dict)}
    reviewed_by_id = {
        str(r.get("id")): r for r in reviewed if isinstance(r, dict)
    }

    expected_ids = [f"hsk6_{i:04d}" for i in range(1, EXPECTED + 1)]

    if list(reviewed_by_id.keys()) != expected_ids:
        errors.append("Reviewed IDs are not exactly hsk6_0001..hsk6_1800.")

    human_verified = 0
    ai_unverified = 0

    for rid in expected_ids:
        b = base_by_id.get(rid)
        r = reviewed_by_id.get(rid)

        if b is None or r is None:
            errors.append(f"{rid}: missing from base or reviewed.")
            continue

        # Core vocabulary identity must match the immutable base.
        for field in ("word", "pinyin", "level"):
            if r.get(field) != b.get(field):
                errors.append(f"{rid}: {field} differs from base.")

        if r.get("level") != "HSK 6":
            errors.append(f"{rid}: invalid level.")

        if not str(r.get("word") or "").strip():
            errors.append(f"{rid}: word is empty.")

        if not str(r.get("pinyin") or "").strip():
            errors.append(f"{rid}: pinyin is empty.")

        meaning = str(r.get("meaningVi") or "").strip()
        selected = str(r.get("selectedMeaningVi") or "").strip()
        candidates = r.get("candidateMeanings")

        if not meaning:
            errors.append(f"{rid}: meaningVi is empty.")
        if not selected:
            errors.append(f"{rid}: selectedMeaningVi is empty.")
        if not isinstance(candidates, list) or not any(
            str(x).strip() for x in candidates
        ):
            errors.append(f"{rid}: candidateMeanings is empty.")

        if r.get("humanVerified") is True:
            human_verified += 1

        status = str(r.get("verificationStatus") or "").strip().lower()
        if status == "unverified":
            ai_unverified += 1
        elif r.get("humanVerified") is not True:
            errors.append(
                f"{rid}: non-human-verified record has invalid verificationStatus."
            )

        # Production gate: nothing may claim automatic approval.
        if r.get("autoApproved") is True:
            errors.append(f"{rid}: autoApproved must be false/missing.")

    # The reviewed validation itself must report zero structural errors.
    if reviewed_report.get("errors", 0) != 0:
        errors.append(
            f"Reviewed validation report contains "
            f"{reviewed_report.get('errors')} errors."
        )

    # AI-assisted/unverified records are permitted at this stage.
    if human_verified == 0:
        warnings.append(
            "No human-verified records; all meanings remain AI-assisted/unverified."
        )

    production_allowed = not errors

    report = {
        "records": len(reviewed),
        "humanReviewed": human_verified,
        "aiAssistedUnverified": ai_unverified,
        "errors": len(errors),
        "warnings": len(warnings),
        "productionBuildAllowed": production_allowed,
        "status": "PASS" if production_allowed else "FAIL",
        "productionDataCreated": False,
        "errorDetails": errors,
        "warningDetails": warnings,
    }

    DATA.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Records:                    {len(reviewed)}/{EXPECTED}")
    print(f"Human reviewed:             {human_verified}")
    print(f"AI-assisted unverified:     {ai_unverified}")
    print(f"Errors:                     {len(errors)}")
    print(f"Warnings:                   {len(warnings)}")
    print(f"Production build allowed:   {'YES' if production_allowed else 'NO'}")
    print(f"Report:                     {REPORT}")
    print()

    if not production_allowed:
        print("Status: FAIL")
        for e in errors[:30]:
            print(f"  [FAIL] {e}")
        if len(errors) > 30:
            print(f"  ... and {len(errors) - 30} more")
        raise SystemExit(1)

    print("Status: PASS")
    print("Final structural production gate passed.")
    print("AI-assisted meanings remain explicitly unverified.")
    print("No production data was created.")


if __name__ == "__main__":
    main()
