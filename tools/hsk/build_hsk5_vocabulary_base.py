#!/usr/bin/env python3
"""Build HSK 5 vocabulary base from the HSK 3.0 source CSV.

Run from project root:
    python tools/hsk/build_hsk5_vocabulary_base.py

Input:
    data/raw/hsk/hsk_vocabulary.csv

Outputs:
    data/hsk/hsk5/hsk5_vocabulary_base.json
    data/hsk/hsk5/hsk5_vocabulary_base.csv
    data/hsk/hsk5/hsk5_normalization_report.json

Source-base only. No meanings or production data are invented.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data" / "raw" / "hsk" / "hsk_vocabulary.csv"
OUT = ROOT / "data" / "hsk" / "hsk5"

CHINESE_RE = re.compile(r"[\u3400-\u9fff]")


def parse_primary_level(value: str) -> int | None:
    value = (value or "").strip()
    mapping = {
        "一级": 1,
        "二级": 2,
        "三级": 3,
        "四级": 4,
        "五级": 5,
        "六级": 6,
        "七-九级": 7,
    }
    for label, level in mapping.items():
        if value.startswith(label):
            return level
    return None


def parse_all_levels(value: str) -> list[int]:
    mapping = {
        "一级": 1,
        "二级": 2,
        "三级": 3,
        "四级": 4,
        "五级": 5,
        "六级": 6,
        "七-九级": 7,
    }
    return sorted(
        level for label, level in mapping.items()
        if label in value
    )


def normalize_word(value: str) -> str:
    value = value.strip()
    match = re.match(r"^(.*?)([1-9])$", value)
    if match and CHINESE_RE.search(match.group(1)):
        return match.group(1)
    return value


def normalize_pos(value: str) -> list[str]:
    return [
        x.strip()
        for x in re.split(r"[、,，;；/]+", value or "")
        if x.strip()
    ]


def main():
    print("=" * 72)
    print("HSK 5 VOCABULARY BASE BUILD")
    print("=" * 72)
    print()

    if not SRC.exists():
        raise SystemExit(f"Missing source: {SRC}")

    with SRC.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as f:
        rows = list(csv.DictReader(f))

    print(f"Source rows loaded: {len(rows)}")

    if not rows:
        raise SystemExit("Source CSV contains no rows.")

    required = {
        "type",
        "levelName",
        "word",
        "pinyin",
        "cixing",
        "sort",
    }

    missing = required - set(rows[0].keys())
    if missing:
        raise SystemExit(
            "Source CSV is missing required columns: "
            + ", ".join(sorted(missing))
        )

    source_rows = [
        row for row in rows
        if row.get("type", "").strip() == "1"
        and parse_primary_level(
            row.get("levelName", "")
        ) == 5
    ]

    print(
        f"HSK 5 introduced source rows found: "
        f"{len(source_rows)}"
    )

    if not source_rows:
        raise SystemExit(
            "No HSK 5 introduced records found."
        )

    records = []
    changes = []
    seen_source = set()
    seen_ids = set()

    for index, row in enumerate(source_rows, 1):
        source_word = row.get("word", "").strip()
        pinyin = row.get("pinyin", "").strip()
        pos_source = row.get("cixing", "").strip()
        level_name = row.get("levelName", "").strip()

        if not source_word:
            raise SystemExit(
                f"Empty Chinese word at source row {index}."
            )

        if not pinyin:
            raise SystemExit(
                f"Empty Pinyin for {source_word}."
            )

        source_sort = int(row["sort"])

        key = (
            source_word,
            pinyin,
            pos_source,
            source_sort,
        )

        if key in seen_source:
            raise SystemExit(
                f"Duplicate source entry: {key}"
            )

        seen_source.add(key)

        word = normalize_word(source_word)

        if word != source_word:
            changes.append({
                "sourceWord": source_word,
                "normalizedWord": word,
                "sourceSort": source_sort,
            })

        if parse_primary_level(level_name) != 5:
            raise SystemExit(
                f"Invalid introduced level for {source_word}: "
                f"{level_name!r}"
            )

        levels = parse_all_levels(level_name)
        if 5 not in levels:
            raise SystemExit(
                f"Could not map HSK 5 for {source_word}."
            )

        rid = f"hsk5_{index:03d}"

        if rid in seen_ids:
            raise SystemExit(f"Duplicate ID: {rid}")
        seen_ids.add(rid)

        records.append({
            "id": rid,
            "word": word,
            "sourceWord": source_word,
            "pinyin": pinyin,
            "pinyinNumeric": None,
            "meaningVi": [],
            "introducedLevel": 5,
            "hskLevels": list(range(1, 6)),
            "partOfSpeechSource": pos_source,
            "partOfSpeech": normalize_pos(pos_source),
            "sourceSort": source_sort,
            "sourceLevelName": level_name,
            "sourceAdditionalLevels": re.findall(
                r"（([^）]+)）",
                level_name,
            ),
            "strokeCount": None,
            "characterIds": [],
            "relatedWordIds": [],
            "exampleIds": [],
            "audio": {
                "wordUrl": None,
                "exampleUrl": None,
            },
            "_source": {
                "sourceId": "profesorm/hsk30",
                "sourceFile": "data/hsk_vocabulary.csv",
                "sourceSort": source_sort,
                "sourceLevelName": level_name,
            },
        })

    if [r["id"] for r in records] != [
        f"hsk5_{i:03d}"
        for i in range(1, len(records) + 1)
    ]:
        raise SystemExit("IDs are not sequential.")

    if [r["sourceSort"] for r in records] != sorted(
        r["sourceSort"] for r in records
    ):
        raise SystemExit("Source ordering is not ascending.")

    words = {}
    for record in records:
        words.setdefault(record["word"], []).append(record["id"])

    duplicates = {
        word: ids
        for word, ids in words.items()
        if len(ids) > 1
    }

    OUT.mkdir(parents=True, exist_ok=True)

    json_path = OUT / "hsk5_vocabulary_base.json"
    json_path.write_text(
        json.dumps(
            records,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    csv_path = OUT / "hsk5_vocabulary_base.csv"
    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as f:
        writer = csv.writer(f)
        writer.writerow([
            "id",
            "word",
            "sourceWord",
            "pinyin",
            "introducedLevel",
            "hskLevels",
            "partOfSpeechSource",
            "sourceSort",
            "sourceLevelName",
        ])

        for r in records:
            writer.writerow([
                r["id"],
                r["word"],
                r["sourceWord"],
                r["pinyin"],
                r["introducedLevel"],
                ",".join(map(str, r["hskLevels"])),
                r["partOfSpeechSource"],
                r["sourceSort"],
                r["sourceLevelName"],
            ])

    report_path = OUT / "hsk5_normalization_report.json"
    report_path.write_text(
        json.dumps({
            "status": "SUCCESS",
            "level": 5,
            "recordCount": len(records),
            "normalizedCount": len(changes),
            "duplicateVisibleWordGroups": len(duplicates),
            "duplicateVisibleWords": duplicates,
            "changes": changes,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print("=" * 72)
    print("SUCCESS")
    print("=" * 72)
    print(
        f"HSK 5 introduced records: {len(records)}"
    )
    print(
        f"Normalized source entries: {len(changes)}"
    )
    print(
        f"Duplicate visible word groups: {len(duplicates)}"
    )
    print(f"Output folder: {OUT}")
    print()
    print("Generated files:")
    print(f"  - {json_path.name}")
    print(f"  - {csv_path.name}")
    print(f"  - {report_path.name}")
    print()
    print("Validation:")
    print("  [PASS] HSK 5 introduced records extracted")
    print("  [PASS] Unique source entries")
    print("  [PASS] Non-empty Chinese words")
    print("  [PASS] Non-empty Pinyin")
    print("  [PASS] HSK 5 level mapping")
    print("  [PASS] Source ordering")
    print("  [PASS] Sequential IDs")
    print("  [PASS] Source entry markers normalized")
    print("  [PASS] Duplicate visible words allowed")
    print()
    print("Status: HSK 5 SOURCE BASE ONLY - NOT PRODUCTION")
    print("=" * 72)


if __name__ == "__main__":
    main()
