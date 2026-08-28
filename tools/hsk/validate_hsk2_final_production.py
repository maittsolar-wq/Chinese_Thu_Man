#!/usr/bin/env python3
"""Final validation gate for HSK 2 production build.

Input:
    data/hsk/hsk2/hsk2_vocabulary_reviewed.json

Output:
    data/hsk/hsk2/hsk2_final_production_validation.json

Important:
- Validates structure and completeness.
- AI-assisted/unverified meanings are allowed but explicitly reported.
- Human verification is NOT claimed.
- Does not modify the reviewed dataset.
- Does not create production data.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk2"
INPUT = DATA_DIR / "hsk2_vocabulary_reviewed.json"
OUTPUT = DATA_DIR / "hsk2_final_production_validation.json"

EXPECTED_COUNT = 200


def load_json(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing input: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {exc}")


def main():
    print("=" * 72)
    print("HSK 2 FINAL PRODUCTION VALIDATION")
    print("=" * 72)
    print()

    records = load_json(INPUT)
    errors = []
    warnings = []

    if not isinstance(records, list):
        raise SystemExit("Root value must be a JSON array.")

    if len(records) != EXPECTED_COUNT:
        errors.append(
            f"Expected {EXPECTED_COUNT} records, got {len(records)}."
        )

    seen_ids = set()

    for record in records:
        if not isinstance(record, dict):
            errors.append("Found non-object record.")
            continue

        rid = record.get("id")
        if not rid:
            errors.append("Record missing id.")
            continue

        if rid in seen_ids:
            errors.append(f"Duplicate ID: {rid}")
        seen_ids.add(rid)

        for field in ("word", "pinyin"):
            if not record.get(field):
                errors.append(f"{rid}: missing {field}.")

        if record.get("introducedLevel") != 2:
            errors.append(f"{rid}: introducedLevel must be 2.")

        meanings = record.get("meaningVi")
        selected = record.get("selectedMeaningVi")

        if not isinstance(meanings, list) or not meanings:
            errors.append(f"{rid}: meaningVi is empty.")
        elif any(not isinstance(x, str) or not x.strip() for x in meanings):
            errors.append(f"{rid}: meaningVi contains invalid values.")

        if not isinstance(selected, list) or not selected:
            errors.append(f"{rid}: selectedMeaningVi is empty.")

        human = record.get("reviewed") is True
        ai_unverified = (
            record.get("reviewed") is False
            and record.get("reviewRequired") is True
            and record.get("verificationMode") == "ai_assisted_unverified"
            and record.get("status") == "ai_assisted_unverified"
        )

        if not human and not ai_unverified:
            errors.append(f"{rid}: invalid verification state.")

    expected_ids = {f"hsk2_{i:03d}" for i in range(1, EXPECTED_COUNT + 1)}

    missing = expected_ids - seen_ids
    extra = seen_ids - expected_ids

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
        and r.get("verificationMode") == "ai_assisted_unverified"
        for r in records
    )

    if ai_count:
        warnings.append(
            f"{ai_count} records are AI-assisted and not human-verified."
        )

    report = {
        "status": "PASS" if not errors else "FAIL",
        "level": 2,
        "recordCount": len(records),
        "expectedCount": EXPECTED_COUNT,
        "humanReviewedCount": human_count,
        "aiAssistedUnverifiedCount": ai_count,
        "errors": errors,
        "warnings": warnings,
        "productionBuildAllowed": not errors,
        "translationAccuracyIndependentlyVerified": human_count == EXPECTED_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Records:                    {len(records)}/{EXPECTED_COUNT}")
    print(f"Human reviewed:             {human_count}")
    print(f"AI-assisted unverified:     {ai_count}")
    print(f"Errors:                     {len(errors)}")
    print(f"Warnings:                   {len(warnings)}")
    print(f"Production build allowed:  {'YES' if not errors else 'NO'}")
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
