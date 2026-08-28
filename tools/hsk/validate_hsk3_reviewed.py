#!/usr/bin/env python3
"""Validate HSK 3 reviewed/AI-assisted vocabulary dataset.

Human-reviewed records are valid.
AI-assisted/unverified records are also structurally valid, but remain warnings.
No record is promoted to human-verified by this validator.
No production data is created.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk3"

INPUT = DATA_DIR / "hsk3_vocabulary_reviewed.json"
OUTPUT = DATA_DIR / "hsk3_reviewed_validation.json"

EXPECTED_COUNT = 500


def load_json(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing input: {path}")

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {exc}")


def main():
    print("=" * 72)
    print("HSK 3 REVIEWED DATA VALIDATION")
    print("=" * 72)
    print()

    records = load_json(INPUT)

    if not isinstance(records, list):
        raise SystemExit("Reviewed dataset root must be a JSON array.")

    errors = []
    warnings = []
    seen_ids = set()

    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            errors.append(f"Record #{index} is not an object.")
            continue

        rid = record.get("id")

        if not rid:
            errors.append(f"Record #{index}: missing id.")
            continue

        if rid in seen_ids:
            errors.append(f"Duplicate ID: {rid}")
        seen_ids.add(rid)

        if record.get("introducedLevel") != 3:
            errors.append(f"{rid}: introducedLevel must be 3.")

        if not record.get("word"):
            errors.append(f"{rid}: missing word.")

        if not record.get("pinyin"):
            errors.append(f"{rid}: missing pinyin.")

        meanings = record.get("meaningVi")

        if not isinstance(meanings, list) or not meanings:
            errors.append(f"{rid}: meaningVi is empty.")
        else:
            for meaning in meanings:
                if not isinstance(meaning, str) or not meaning.strip():
                    errors.append(
                        f"{rid}: meaningVi contains an invalid value."
                    )

            normalized = [
                meaning.strip().casefold()
                for meaning in meanings
                if isinstance(meaning, str) and meaning.strip()
            ]

            if len(normalized) != len(set(normalized)):
                warnings.append(
                    f"{rid}: duplicate Vietnamese meanings."
                )

        selected = record.get("selectedMeaningVi")

        if not isinstance(selected, list) or not selected:
            errors.append(f"{rid}: selectedMeaningVi is empty.")

        human_reviewed = record.get("reviewed") is True

        ai_unverified = (
            record.get("reviewed") is False
            and record.get("reviewRequired") is True
            and record.get("verificationMode")
            == "ai_assisted_unverified"
            and record.get("status")
            == "ai_assisted_unverified"
        )

        if not human_reviewed and not ai_unverified:
            errors.append(
                f"{rid}: invalid verification state."
            )

    if len(records) != EXPECTED_COUNT:
        errors.append(
            f"Expected {EXPECTED_COUNT} records, got {len(records)}."
        )

    expected_ids = {
        f"hsk3_{i:03d}"
        for i in range(1, EXPECTED_COUNT + 1)
    }

    missing = expected_ids - seen_ids
    extra = seen_ids - expected_ids

    if missing:
        errors.append(
            "Missing IDs: " + ", ".join(sorted(missing))
        )

    if extra:
        errors.append(
            "Unexpected IDs: " + ", ".join(sorted(extra))
        )

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

    if human_count < EXPECTED_COUNT:
        warnings.append(
            "Translation accuracy has not been independently verified "
            "for the complete HSK 3 dataset."
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
        "productionCreated": False,
        "translationAccuracyIndependentlyVerified": (
            human_count == EXPECTED_COUNT
        ),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Reviewed records:          {len(records)}/{EXPECTED_COUNT}")
    print(f"Human reviewed:            {human_count}")
    print(f"AI-assisted unverified:    {ai_count}")
    print(f"Errors:                    {len(errors)}")
    print(f"Warnings:                  {len(warnings)}")
    print(f"Report:                    {OUTPUT}")
    print()

    if errors:
        print("Status: FAIL")
        for error in errors:
            print(f"  [FAIL] {error}")
        raise SystemExit(1)

    print("Status: PASS")
    print()
    print("PASS: HSK 3 reviewed dataset is structurally valid.")
    print("AI-assisted meanings remain explicitly unverified.")
    print("No production data was created.")


if __name__ == "__main__":
    main()
