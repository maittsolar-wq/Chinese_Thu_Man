#!/usr/bin/env python3
"""Validate the HSK 2 vocabulary base dataset.

Run from project root:
    python tools/hsk/validate_hsk2_base.py

Input:
    data/hsk/hsk2/hsk2_vocabulary_base.json

Output:
    data/hsk/hsk2/hsk2_base_validation.json

This validator checks the HSK 2 base layer only.
It does not modify vocabulary data or production data.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

INPUT = ROOT / "data" / "hsk" / "hsk2" / "hsk2_vocabulary_base.json"
OUTPUT = ROOT / "data" / "hsk" / "hsk2" / "hsk2_base_validation.json"

EXPECTED_COUNT = 200


def is_chinese_word(value: str) -> bool:
    return bool(value) and bool(
        re.search(r"[\u3400-\u9fff]", value)
    )


def main():
    print("=" * 64)
    print("HSK 2 BASE VALIDATION")
    print("=" * 64)
    print()

    if not INPUT.exists():
        raise SystemExit(
            f"Missing input: {INPUT}\n"
            "Run build_hsk2_vocabulary_base.py first."
        )

    try:
        records = json.loads(
            INPUT.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"Invalid JSON: {exc}"
        )

    if not isinstance(records, list):
        raise SystemExit(
            "Invalid dataset: root value must be a list."
        )

    errors = []
    warnings = []

    if len(records) != EXPECTED_COUNT:
        errors.append(
            f"Expected {EXPECTED_COUNT} records, got {len(records)}."
        )

    ids = []
    source_sorts = []

    for index, record in enumerate(records, start=1):

        if not isinstance(record, dict):
            errors.append(
                f"Record {index}: record is not an object."
            )
            continue

        record_id = record.get("id")
        word = record.get("word")
        source_word = record.get("sourceWord")
        pinyin = record.get("pinyin")
        introduced_level = record.get("introducedLevel")
        hsk_levels = record.get("hskLevels")
        source_sort = record.get("sourceSort")
        source_level_name = record.get("sourceLevelName")

        if not isinstance(record_id, str):
            errors.append(
                f"Record {index}: invalid id."
            )
        else:
            ids.append(record_id)

        if not isinstance(word, str) or not is_chinese_word(word):
            errors.append(
                f"{record_id or index}: invalid Chinese word "
                f"{word!r}."
            )

        if not isinstance(source_word, str) or not source_word:
            errors.append(
                f"{record_id or index}: missing sourceWord."
            )

        if not isinstance(pinyin, str) or not pinyin.strip():
            errors.append(
                f"{record_id or index}: missing Pinyin."
            )

        if introduced_level != 2:
            errors.append(
                f"{record_id or index}: "
                f"introducedLevel={introduced_level!r}, expected 2."
            )

        if not isinstance(hsk_levels, list) or 2 not in hsk_levels:
            errors.append(
                f"{record_id or index}: HSK 2 missing from hskLevels."
            )

        if not isinstance(source_sort, int):
            errors.append(
                f"{record_id or index}: invalid sourceSort."
            )
        else:
            source_sorts.append(source_sort)

        if not isinstance(source_level_name, str):
            errors.append(
                f"{record_id or index}: missing sourceLevelName."
            )
        elif not source_level_name.startswith("二级"):
            errors.append(
                f"{record_id or index}: sourceLevelName does not "
                f"start with 二级: {source_level_name!r}."
            )

        # meaningVi must remain empty at base stage.
        meaning_vi = record.get("meaningVi")
        if meaning_vi != []:
            errors.append(
                f"{record_id or index}: meaningVi is not empty "
                "in base dataset."
            )

    expected_ids = [
        f"hsk2_{i:03d}"
        for i in range(1, EXPECTED_COUNT + 1)
    ]

    if ids != expected_ids:
        errors.append(
            "IDs are not sequential from hsk2_001 to hsk2_200."
        )

    if len(ids) != len(set(ids)):
        errors.append("Duplicate IDs found.")

    if len(source_sorts) != len(set(source_sorts)):
        errors.append("Duplicate sourceSort values found.")

    if source_sorts != sorted(source_sorts):
        errors.append(
            "sourceSort values are not in ascending order."
        )

    # Duplicate visible Chinese words are allowed.
    # They can represent separate dictionary entries.
    word_entry_map = {}

    for record in records:
        word = record.get("word")
        if word:
            word_entry_map.setdefault(word, []).append(record)

    duplicate_word_count = sum(
        1
        for entries in word_entry_map.values()
        if len(entries) > 1
    )

    if duplicate_word_count:
        warnings.append(
            f"{duplicate_word_count} Chinese words have multiple "
            "source entries; this is allowed."
        )

    report = {
        "status": "PASS" if not errors else "FAIL",
        "level": 2,
        "expectedRecords": EXPECTED_COUNT,
        "actualRecords": len(records),
        "errors": errors,
        "warnings": warnings,
        "checks": {
            "recordCount": not any(
                "Expected 200 records" in e
                for e in errors
            ),
            "ids": not any(
                "IDs are not sequential" in e
                or "Duplicate IDs" in e
                for e in errors
            ),
            "sourceSort": not any(
                "sourceSort" in e
                for e in errors
            ),
            "words": not any(
                "invalid Chinese word" in e
                for e in errors
            ),
            "pinyin": not any(
                "missing Pinyin" in e
                for e in errors
            ),
            "introducedLevel": not any(
                "introducedLevel" in e
                for e in errors
            ),
            "hskLevels": not any(
                "HSK 2 missing" in e
                for e in errors
            ),
            "sourceLevelName": not any(
                "sourceLevelName" in e
                for e in errors
            ),
            "baseMeaningState": not any(
                "meaningVi is not empty" in e
                for e in errors
            ),
        },
    }

    OUTPUT.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Base records: {len(records)}/{EXPECTED_COUNT}")
    print(f"Errors:        {len(errors)}")
    print(f"Warnings:      {len(warnings)}")
    print(f"Report:        {OUTPUT}")
    print()

    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  [FAIL] {error}")
        print()
        print("Status: FAIL")
        raise SystemExit(1)

    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"  [WARN] {warning}")
        print()

    print("Status: PASS")
    print()
    print("PASS: HSK 2 base dataset is structurally valid.")
    print("No vocabulary or production data was modified.")


if __name__ == "__main__":
    main()
