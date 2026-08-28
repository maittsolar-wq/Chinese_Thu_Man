#!/usr/bin/env python3
"""Final production validation gate for HSK 3."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk3"
INPUT = DATA / "hsk3_vocabulary_reviewed.json"
OUTPUT = DATA / "hsk3_final_production_validation.json"

EXPECTED_COUNT = 500


def load(path):
    if not path.exists():
        raise SystemExit(f"Missing input: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {exc}")


def main():
    print("=" * 72)
    print("HSK 3 FINAL PRODUCTION VALIDATION")
    print("=" * 72)
    print()

    records = load(INPUT)
    errors = []
    warnings = []

    if not isinstance(records, list):
        raise SystemExit("Reviewed dataset root must be a JSON array.")

    if len(records) != EXPECTED_COUNT:
        errors.append(
            f"Expected {EXPECTED_COUNT} records, got {len(records)}."
        )

    seen = set()

    for record in records:
        if not isinstance(record, dict):
            errors.append("Found non-object record.")
            continue

        rid = record.get("id")
        if not rid:
            errors.append("Record missing id.")
            continue

        if rid in seen:
            errors.append(f"Duplicate ID: {rid}")
        seen.add(rid)

        if record.get("introducedLevel") != 3:
            errors.append(f"{rid}: introducedLevel must be 3.")

        if not record.get("word"):
            errors.append(f"{rid}: missing word.")

        if not record.get("pinyin"):
            errors.append(f"{rid}: missing pinyin.")

        meanings = record.get("meaningVi")
        selected = record.get("selectedMeaningVi")

        if not isinstance(meanings, list) or not meanings:
            errors.append(f"{rid}: meaningVi is empty.")
        elif any(
            not isinstance(x, str) or not x.strip()
            for x in meanings
        ):
            errors.append(f"{rid}: meaningVi contains invalid values.")

        if not isinstance(selected, list) or not selected:
            errors.append(f"{rid}: selectedMeaningVi is empty.")

        human = record.get("reviewed") is True
        ai = (
            record.get("reviewed") is False
            and record.get("reviewRequired") is True
            and record.get("verificationMode")
            == "ai_assisted_unverified"
            and record.get("status")
            == "ai_assisted_unverified"
        )

        if not human and not ai:
            errors.append(f"{rid}: invalid verification state.")

    expected = {
        f"hsk3_{i:03d}"
        for i in range(1, EXPECTED_COUNT + 1)
    }

    missing = expected - seen
    extra = seen - expected

    if missing:
        errors.append("Missing IDs: " + ", ".join(sorted(missing)))
    if extra:
        errors.append("Unexpected IDs: " + ", ".join(sorted(extra)))

    human_count = sum(
        isinstance(r, dict) and r.get("reviewed") is True
        for r in records
    )

    ai_count = sum(
        isinstance(r, dict)
        and r.get("verificationMode")
        == "ai_assisted_unverified"
        for r in records
    )

    if ai_count:
        warnings.append(
            f"{ai_count} records are AI-assisted and not human-verified."
        )

    report = {
        "status": "PASS" if not errors else "FAIL",
        "level": 3,
        "recordCount": len(records),
        "expectedCount": EXPECTED_COUNT,
        "humanReviewedCount": human_count,
        "aiAssistedUnverifiedCount": ai_count,
        "errors": errors,
        "warnings": warnings,
        "productionBuildAllowed": not errors,
        "translationAccuracyIndependentlyVerified": (
            human_count == EXPECTED_COUNT
        ),
    }

    OUTPUT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Records:                    {len(records)}/{EXPECTED_COUNT}")
    print(f"Human reviewed:             {human_count}")
    print(f"AI-assisted unverified:     {ai_count}")
    print(f"Errors:                     {len(errors)}")
    print(f"Warnings:                   {len(warnings)}")
    print(
        "Production build allowed:  "
        + ("YES" if not errors else "NO")
    )
    print(f"Report:                     {OUTPUT}")
    print()

    if errors:
        print("Status: FAIL")
        for error in errors:
            print(f"  [FAIL] {error}")
        raise SystemExit(1)

    print("Status: PASS")
    print("Final structural production gate passed.")
    print("AI-assisted meanings remain explicitly unverified.")
    print("No production data was created.")


if __name__ == "__main__":
    main()
