#!/usr/bin/env python3
"""Build HSK 6 vocabulary base from the raw HSK vocabulary CSV.

The source CSV has been observed to be UTF-8 bytes displayed incorrectly by
some Windows/PowerShell code pages. This script reads bytes and repairs common
mojibake safely before parsing.

Source:
    data/raw/hsk/hsk_vocabulary.csv

Output:
    data/hsk/hsk6/hsk6_vocabulary_base.json
    data/hsk/hsk6/hsk6_vocabulary_base.csv
    data/hsk/hsk6/hsk6_normalization_report.json

No meanings, reviewed data, or production data are created/modified.
"""

from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "raw" / "hsk" / "hsk_vocabulary.csv"
OUT = ROOT / "data" / "hsk" / "hsk6"

EXPECTED_MIN = 1
TARGET_LEVELS = {"六级", "HSK 6", "HSK6", "6"}


def decode_source(path: Path) -> str:
    raw = path.read_bytes()

    # Prefer UTF-8. If it contains classic UTF-8-as-Windows-1252 mojibake,
    # repair only when the repaired text clearly improves the Chinese text.
    text = raw.decode("utf-8-sig")

    bad_markers = ("Ã", "Â", "ç", "è", "å", "æ", "é", "ä", "åŠ")
    if any(x in text for x in bad_markers):
        try:
            repaired = text.encode("latin1").decode("utf-8")
            if repaired.count("级") > text.count("级") or repaired.count("六") > text.count("六"):
                text = repaired
        except UnicodeError:
            pass

    return text


def normalize_level(value: str) -> str:
    v = str(value or "").strip()
    v = v.replace("（", "(").replace("）", ")")
    if v in {"六级", "HSK 6", "HSK6", "6"}:
        return "HSK 6"
    return v


def clean_word(value: str) -> str:
    return re.sub(r"\s+", "", str(value or "").strip())


def clean_pinyin(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def is_hsk6(level_name: str) -> bool:
    v = normalize_level(level_name)
    return v == "HSK 6" or "六级" in v


def main():
    print("=" * 72)
    print("HSK 6 VOCABULARY BASE BUILD")
    print("=" * 72)
    print()

    if not SOURCE.exists():
        raise SystemExit(f"Source file not found: {SOURCE}")

    text = decode_source(SOURCE)
    rows = list(csv.DictReader(io.StringIO(text)))

    if not rows:
        raise SystemExit("Source CSV contains no data rows.")

    selected = [r for r in rows if is_hsk6(r.get("levelName", ""))]

    if len(selected) < EXPECTED_MIN:
        # Give a diagnostic rather than silently creating an empty dataset.
        levels = sorted({
            str(r.get("levelName", "")).strip()
            for r in rows
            if str(r.get("levelName", "")).strip()
        })
        print("Detected levelName samples:")
        for x in levels:
            if "级" in x or "HSK" in x.upper():
                print(" ", repr(x))
        raise SystemExit("No HSK 6 rows were detected.")

    records = []
    seen_ids = set()
    seen_source_keys = set()
    duplicate_words = {}

    for idx, row in enumerate(selected, start=1):
        word = clean_word(row.get("word"))
        pinyin = clean_pinyin(row.get("pinyin"))
        level = normalize_level(row.get("levelName"))
        cixing = str(row.get("cixing") or "").strip()
        source_sort = str(row.get("sort") or "").strip()

        if not word:
            raise SystemExit(f"Empty Chinese word at selected row {idx}.")
        if not pinyin:
            raise SystemExit(f"Empty pinyin for {word} at selected row {idx}.")
        if level != "HSK 6":
            raise SystemExit(f"Unexpected level for {word}: {level!r}")

        rid = f"hsk6_{idx:04d}"
        if rid in seen_ids:
            raise SystemExit(f"Duplicate generated ID: {rid}")
        seen_ids.add(rid)

        key = (word, pinyin)
        if key in seen_source_keys:
            # Duplicate source entries are allowed by the established HSK
            # pipeline, but must be visible in the report.
            duplicate_words[word] = duplicate_words.get(word, 1) + 1
        else:
            seen_source_keys.add(key)

        records.append({
            "id": rid,
            "level": "HSK 6",
            "word": word,
            "pinyin": pinyin,
            "cixing": cixing,
            "sourceSort": source_sort,
        })

    # Validate source ordering by source sort where available.
    numeric_sorts = []
    for r in records:
        try:
            numeric_sorts.append(int(r["sourceSort"]))
        except (TypeError, ValueError):
            numeric_sorts.append(None)

    ordering_ok = all(
        numeric_sorts[i] is None
        or numeric_sorts[i - 1] is None
        or numeric_sorts[i] >= numeric_sorts[i - 1]
        for i in range(1, len(numeric_sorts))
    )

    if not ordering_ok:
        raise SystemExit("Selected HSK 6 rows are not in source order.")

    OUT.mkdir(parents=True, exist_ok=True)

    json_path = OUT / "hsk6_vocabulary_base.json"
    csv_path = OUT / "hsk6_vocabulary_base.csv"
    report_path = OUT / "hsk6_normalization_report.json"

    json_path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "level", "word", "pinyin", "cixing", "sourceSort"],
        )
        writer.writeheader()
        writer.writerows(records)

    report = {
        "sourceRowsLoaded": len(rows),
        "hsk6IntroducedRecords": len(records),
        "uniqueSourceEntries": len(seen_source_keys),
        "duplicateVisibleWordGroups": len(duplicate_words),
        "duplicateVisibleWords": duplicate_words,
        "encoding": "UTF-8 with mojibake repair when detected",
        "validations": {
            "hsk6IntroducedRecordsExtracted": len(records) > 0,
            "uniqueSourceEntries": len(seen_source_keys) > 0,
            "nonEmptyChineseWords": all(bool(r["word"]) for r in records),
            "nonEmptyPinyin": all(bool(r["pinyin"]) for r in records),
            "hsk6LevelMapping": all(r["level"] == "HSK 6" for r in records),
            "sourceOrdering": ordering_ok,
            "sequentialIds": [r["id"] for r in records]
            == [f"hsk6_{i:04d}" for i in range(1, len(records) + 1)],
            "duplicateVisibleWordsAllowed": True,
        },
        "production": False,
    }

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Source rows loaded: {len(rows)}")
    print(f"HSK 6 introduced source rows found: {len(records)}")
    print()
    print("=" * 72)
    print("SUCCESS")
    print("=" * 72)
    print(f"HSK 6 introduced records: {len(records)}")
    print(f"Unique source entries: {len(seen_source_keys)}")
    print(f"Duplicate visible word groups: {len(duplicate_words)}")
    print(f"Output folder: {OUT}")
    print()
    print("Generated files:")
    print("  - hsk6_vocabulary_base.json")
    print("  - hsk6_vocabulary_base.csv")
    print("  - hsk6_normalization_report.json")
    print()
    print("Validation:")
    for key, ok in report["validations"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {key}")
    print()
    print("Status: HSK 6 SOURCE BASE ONLY - NOT PRODUCTION")


if __name__ == "__main__":
    main()
