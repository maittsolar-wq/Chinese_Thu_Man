#!/usr/bin/env python3
"""Validate the HSK 2 reviewed/AI-assisted vocabulary dataset.

Two verification states are supported:

1. Human reviewed:
   reviewed=true

2. AI-assisted but unverified:
   reviewed=false
   reviewRequired=true
   verificationMode="ai_assisted_unverified"
   status="ai_assisted_unverified"

AI-assisted records are structurally valid but remain WARNINGs.
They are NOT treated as human-reviewed.

This script does NOT create production data.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = (
    ROOT
    / "data"
    / "hsk"
    / "hsk2"
)

INPUT = (
    DATA_DIR
    / "hsk2_vocabulary_reviewed.json"
)

OUTPUT = (
    DATA_DIR
    / "hsk2_reviewed_validation.json"
)

EXPECTED_COUNT = 200


def load_json(path: Path):
    if not path.exists():
        raise SystemExit(
            f"Missing input: {path}"
        )

    try:
        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"Invalid JSON: {exc}"
        )


def main():
    print("=" * 72)
    print("HSK 2 REVIEWED DATA VALIDATION")
    print("=" * 72)
    print()

    records = load_json(INPUT)

    if not isinstance(records, list):
        raise SystemExit(
            "Reviewed dataset root must be a JSON array."
        )

    errors = []
    warnings = []
    seen_ids = set()

    for index, record in enumerate(
        records,
        start=1,
    ):
        if not isinstance(record, dict):
            errors.append(
                f"Record #{index} is not an object."
            )
            continue

        record_id = record.get("id")

        if not record_id:
            errors.append(
                f"Record #{index}: missing id."
            )
            continue

        if record_id in seen_ids:
            errors.append(
                f"Duplicate ID: {record_id}"
            )

        seen_ids.add(record_id)

        # ----------------------------------------------------------
        # Core vocabulary validation
        # ----------------------------------------------------------

        if record.get(
            "introducedLevel"
        ) != 2:
            errors.append(
                f"{record_id}: "
                "introducedLevel must be 2."
            )

        if not record.get("word"):
            errors.append(
                f"{record_id}: missing word."
            )

        if not record.get("pinyin"):
            errors.append(
                f"{record_id}: missing pinyin."
            )

        # ----------------------------------------------------------
        # Vietnamese meaning validation
        # ----------------------------------------------------------

        meanings = record.get(
            "meaningVi"
        )

        if (
            not isinstance(
                meanings,
                list,
            )
            or not meanings
        ):
            errors.append(
                f"{record_id}: meaningVi is empty."
            )
        else:
            for meaning in meanings:
                if (
                    not isinstance(
                        meaning,
                        str,
                    )
                    or not meaning.strip()
                ):
                    errors.append(
                        f"{record_id}: "
                        "meaningVi contains "
                        "an invalid value."
                    )

            cleaned = [
                meaning.strip()
                for meaning in meanings
                if isinstance(
                    meaning,
                    str,
                )
                and meaning.strip()
            ]

            normalized = [
                meaning.casefold()
                for meaning in cleaned
            ]

            if len(normalized) != len(
                set(normalized)
            ):
                warnings.append(
                    f"{record_id}: "
                    "duplicate Vietnamese meanings."
                )

        # ----------------------------------------------------------
        # Selected meanings
        # ----------------------------------------------------------

        selected = record.get(
            "selectedMeaningVi"
        )

        if (
            not isinstance(
                selected,
                list,
            )
            or not selected
        ):
            errors.append(
                f"{record_id}: "
                "selectedMeaningVi is empty."
            )

        # ----------------------------------------------------------
        # Verification state
        # ----------------------------------------------------------

        human_reviewed = (
            record.get("reviewed")
            is True
        )

        ai_assisted_unverified = (
            record.get("reviewed")
            is False
            and record.get(
                "reviewRequired"
            )
            is True
            and record.get(
                "verificationMode"
            )
            == "ai_assisted_unverified"
            and record.get(
                "status"
            )
            == "ai_assisted_unverified"
        )

        if not human_reviewed and not ai_assisted_unverified:
            errors.append(
                f"{record_id}: "
                "invalid verification state."
            )

    # --------------------------------------------------------------
    # Record count
    # --------------------------------------------------------------

    if len(records) != EXPECTED_COUNT:
        errors.append(
            f"Expected {EXPECTED_COUNT} "
            f"records, got {len(records)}."
        )

    # --------------------------------------------------------------
    # Sequential IDs
    # --------------------------------------------------------------

    expected_ids = {
        f"hsk2_{i:03d}"
        for i in range(
            1,
            EXPECTED_COUNT + 1,
        )
    }

    missing_ids = (
        expected_ids
        - seen_ids
    )

    extra_ids = (
        seen_ids
        - expected_ids
    )

    if missing_ids:
        errors.append(
            "Missing IDs: "
            + ", ".join(
                sorted(missing_ids)
            )
        )

    if extra_ids:
        errors.append(
            "Unexpected IDs: "
            + ", ".join(
                sorted(extra_ids)
            )
        )

    # --------------------------------------------------------------
    # Verification statistics
    # --------------------------------------------------------------

    human_reviewed_count = sum(
        isinstance(
            record,
            dict,
        )
        and record.get(
            "reviewed"
        )
        is True
        for record in records
    )

    ai_assisted_count = sum(
        isinstance(
            record,
            dict,
        )
        and record.get(
            "verificationMode"
        )
        == "ai_assisted_unverified"
        for record in records
    )

    if ai_assisted_count > 0:
        warnings.append(
            f"{ai_assisted_count} records are "
            "AI-assisted and not human-verified."
        )

    if human_reviewed_count < EXPECTED_COUNT:
        warnings.append(
            "Translation accuracy has not been "
            "independently verified for the "
            "complete HSK 2 dataset."
        )

    # --------------------------------------------------------------
    # Report
    # --------------------------------------------------------------

    report = {
        "status": (
            "PASS"
            if not errors
            else "FAIL"
        ),
        "level": 2,
        "recordCount": len(records),
        "expectedCount": EXPECTED_COUNT,
        "humanReviewedCount": (
            human_reviewed_count
        ),
        "aiAssistedUnverifiedCount": (
            ai_assisted_count
        ),
        "errors": errors,
        "warnings": warnings,
        "productionCreated": False,
        "translationAccuracyIndependentlyVerified": (
            human_reviewed_count
            == EXPECTED_COUNT
        ),
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # --------------------------------------------------------------
    # Console output
    # --------------------------------------------------------------

    print(
        f"Reviewed records:          "
        f"{len(records)}/{EXPECTED_COUNT}"
    )

    print(
        f"Human reviewed:            "
        f"{human_reviewed_count}"
    )

    print(
        f"AI-assisted unverified:    "
        f"{ai_assisted_count}"
    )

    print(
        f"Errors:                    "
        f"{len(errors)}"
    )

    print(
        f"Warnings:                  "
        f"{len(warnings)}"
    )

    print(
        f"Report:                    "
        f"{OUTPUT}"
    )

    print()

    if errors:
        print("Status: FAIL")
        print()

        for error in errors:
            print(
                f"  [FAIL] {error}"
            )

        raise SystemExit(1)

    print("Status: PASS")
    print()

    print(
        "PASS: HSK 2 reviewed dataset "
        "is structurally valid."
    )

    print(
        "AI-assisted meanings remain "
        "explicitly unverified."
    )

    print(
        "No production data was created."
    )


if __name__ == "__main__":
    main()