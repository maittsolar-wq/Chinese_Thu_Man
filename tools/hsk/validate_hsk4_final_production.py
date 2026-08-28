#!/usr/bin/env python3
"""Final structural production gate for HSK 4."""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk4"
INPUT = DATA / "hsk4_vocabulary_reviewed.json"
OUTPUT = DATA / "hsk4_final_production_validation.json"
EXPECTED_COUNT = 1000


def load(path):
    if not path.exists():
        raise SystemExit(f"Missing input: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {exc}")


def main():
    print("=" * 72)
    print("HSK 4 FINAL PRODUCTION VALIDATION")
    print("=" * 72)
    print()

    records = load(INPUT)
    errors, warnings, seen = [], [], set()

    if not isinstance(records, list):
        raise SystemExit("Reviewed dataset root must be a JSON array.")

    for r in records:
        if not isinstance(r, dict):
            errors.append("Found non-object record.")
            continue

        rid = r.get("id")
        if not rid:
            errors.append("Record missing id.")
            continue
        if rid in seen:
            errors.append(f"Duplicate ID: {rid}")
        seen.add(rid)

        if r.get("introducedLevel") != 4:
            errors.append(f"{rid}: introducedLevel must be 4.")
        if not r.get("word"):
            errors.append(f"{rid}: missing word.")
        if not r.get("pinyin"):
            errors.append(f"{rid}: missing pinyin.")

        meanings = r.get("meaningVi")
        selected = r.get("selectedMeaningVi")
        if not isinstance(meanings, list) or not meanings:
            errors.append(f"{rid}: meaningVi is empty.")
        if not isinstance(selected, list) or not selected:
            errors.append(f"{rid}: selectedMeaningVi is empty.")

        human = r.get("reviewed") is True
        ai = (
            r.get("reviewed") is False
            and r.get("reviewRequired") is True
            and r.get("verificationMode")
            in {
                "ai_assisted_unverified",
                "needs_manual_verification",
            }
        )
        if not human and not ai:
            errors.append(f"{rid}: invalid verification state.")

        if r.get("verificationMode") == "needs_manual_verification":
            warnings.append(f"{rid}: manual verification required.")

    if len(records) != EXPECTED_COUNT:
        errors.append(
            f"Expected {EXPECTED_COUNT} records, got {len(records)}."
        )

    expected = {f"hsk4_{i:03d}" for i in range(1, EXPECTED_COUNT + 1)}
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
        and r.get("verificationMode") == "ai_assisted_unverified"
        for r in records
    )
    manual_count = sum(
        isinstance(r, dict)
        and r.get("verificationMode") == "needs_manual_verification"
        for r in records
    )

    warnings.append(
        f"{ai_count} AI-assisted records remain unverified."
    )

    report = {
        "status": "PASS" if not errors else "FAIL",
        "level": 4,
        "recordCount": len(records),
        "expectedCount": EXPECTED_COUNT,
        "humanReviewedCount": human_count,
        "aiAssistedUnverifiedCount": ai_count,
        "needsManualVerificationCount": manual_count,
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
    print(f"Manual verification:        {manual_count}")
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
        for e in errors:
            print(f"  [FAIL] {e}")
        raise SystemExit(1)

    print("Status: PASS")
    print("Final structural production gate passed.")
    print("AI-assisted meanings remain explicitly unverified.")
    print("No production data was created.")


if __name__ == "__main__":
    main()
