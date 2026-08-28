#!/usr/bin/env python3
"""Build HSK 4 vocabulary base from the HSK 3.0 source CSV.

Run from project root:
    python tools/hsk/build_hsk4_vocabulary_base.py

Input:
    data/raw/hsk/hsk_vocabulary.csv

Output:
    data/hsk/hsk4/hsk4_vocabulary_base.json
    data/hsk/hsk4/hsk4_vocabulary_base.csv
    data/hsk/hsk4/hsk4_normalization_report.json

Only records whose PRIMARY level is 四级 are included.
Duplicate visible Chinese words are allowed when source entries differ.
No meanings or production data are invented.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

SRC = ROOT / "data" / "raw" / "hsk" / "hsk_vocabulary.csv"
OUT = ROOT / "data" / "hsk" / "hsk4"

CHINESE_RE = re.compile(r"[\u3400-\u9fff]")


def parse_primary_level(level_name: str) -> int | None:
    level_name = (level_name or "").strip()

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
        if level_name.startswith(label):
            return level

    return None


def parse_all_hsk_levels(level_name: str) -> list[int]:
    mapping = {
        "一级": 1,
        "二级": 2,
        "三级": 3,
        "四级": 4,
        "五级": 5,
        "六级": 6,
        "七-九级": 7,
    }

    return sorted({
        level
        for label, level in mapping.items()
        if label in level_name
    })


def cumulative_levels(introduced_level: int) -> list[int]:
    return list(range(1, introduced_level + 1))


def normalize_word(source_word: str) -> str:
    source_word = source_word.strip()

    match = re.match(r"^(.*?)([1-9])$", source_word)

    if not match:
        return source_word

    base_word = match.group(1)

    if CHINESE_RE.search(base_word):
        return base_word

    return source_word


def normalize_pos(cixing: str) -> list[str]:
    return [
        value.strip()
        for value in re.split(
            r"[、,，;；/]+",
            cixing or "",
        )
        if value.strip()
    ]


def main():
    print("=" * 72)
    print("HSK 4 VOCABULARY BASE BUILD")
    print("=" * 72)
    print()

    if not SRC.exists():
        raise SystemExit(
            f"Missing source: {SRC}\n"
            "Run: python tools/hsk/fetch_hsk_source.py"
        )

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
        row
        for row in rows
        if row.get("type", "").strip() == "1"
        and parse_primary_level(
            row.get("levelName", "").strip()
        ) == 4
    ]

    print(
        f"HSK 4 introduced source rows found: "
        f"{len(source_rows)}"
    )

    if not source_rows:
        raise SystemExit(
            "No HSK 4 introduced records found. "
            "Check source encoding/levelName values."
        )

    records = []
    changes = []
    seen_ids = set()
    seen_source_entries = set()

    for index, row in enumerate(source_rows, start=1):
        source_word = row.get("word", "").strip()
        pinyin = row.get("pinyin", "").strip()
        level_name = row.get("levelName", "").strip()
        pos_source = row.get("cixing", "").strip()

        if not source_word:
            raise SystemExit(
                f"Empty word at HSK 4 source row {index}."
            )

        if not pinyin:
            raise SystemExit(
                f"Empty Pinyin for {source_word}."
            )

        source_sort = int(row["sort"])

        source_entry_key = (
            source_word,
            pinyin,
            pos_source,
            source_sort,
        )

        if source_entry_key in seen_source_entries:
            raise SystemExit(
                f"Duplicate source entry: {source_entry_key}"
            )

        seen_source_entries.add(source_entry_key)

        word = normalize_word(source_word)

        if word != source_word:
            changes.append({
                "sourceWord": source_word,
                "normalizedWord": word,
                "sourceSort": source_sort,
            })

        if parse_primary_level(level_name) != 4:
            raise SystemExit(
                f"Invalid introduced level for "
                f"{source_word}: {level_name!r}"
            )

        levels = parse_all_hsk_levels(level_name)

        if 4 not in levels:
            raise SystemExit(
                f"Could not map HSK 4 for "
                f"{source_word}: {level_name!r}"
            )

        record_id = f"hsk4_{index:03d}"

        if record_id in seen_ids:
            raise SystemExit(
                f"Duplicate ID: {record_id}"
            )

        seen_ids.add(record_id)

        records.append({
            "id": record_id,
            "word": word,
            "sourceWord": source_word,
            "pinyin": pinyin,
            "pinyinNumeric": None,
            "meaningVi": [],
            "introducedLevel": 4,
            "hskLevels": cumulative_levels(4),
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

    expected_ids = [
        f"hsk4_{i:03d}"
        for i in range(1, len(records) + 1)
    ]

    if [r["id"] for r in records] != expected_ids:
        raise SystemExit("IDs are not sequential.")

    source_sorts = [r["sourceSort"] for r in records]

    if source_sorts != sorted(source_sorts):
        raise SystemExit(
            "Source ordering is not ascending."
        )

    duplicate_words = {}

    for record in records:
        duplicate_words.setdefault(
            record["word"],
            [],
        ).append(record["id"])

    duplicate_word_groups = {
        word: ids
        for word, ids in duplicate_words.items()
        if len(ids) > 1
    }

    OUT.mkdir(parents=True, exist_ok=True)

    json_path = OUT / "hsk4_vocabulary_base.json"

    json_path.write_text(
        json.dumps(
            records,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    csv_path = OUT / "hsk4_vocabulary_base.csv"

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

        for record in records:
            writer.writerow([
                record["id"],
                record["word"],
                record["sourceWord"],
                record["pinyin"],
                record["introducedLevel"],
                ",".join(
                    map(str, record["hskLevels"])
                ),
                record["partOfSpeechSource"],
                record["sourceSort"],
                record["sourceLevelName"],
            ])

    report_path = OUT / "hsk4_normalization_report.json"

    report_path.write_text(
        json.dumps({
            "status": "SUCCESS",
            "level": 4,
            "recordCount": len(records),
            "normalizedCount": len(changes),
            "duplicateVisibleWordGroups": len(
                duplicate_word_groups
            ),
            "duplicateVisibleWords": duplicate_word_groups,
            "changes": changes,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print("=" * 72)
    print("SUCCESS")
    print("=" * 72)
    print(
        f"HSK 4 introduced records: {len(records)}"
    )
    print(
        f"Normalized source entries: {len(changes)}"
    )
    print(
        f"Duplicate visible word groups: "
        f"{len(duplicate_word_groups)}"
    )
    print(
        f"Output folder: {OUT}"
    )
    print()
    print("Generated files:")
    print(f"  - {json_path.name}")
    print(f"  - {csv_path.name}")
    print(f"  - {report_path.name}")
    print()
    print("Validation:")
    print("  [PASS] HSK 4 introduced records extracted")
    print("  [PASS] Unique source entries")
    print("  [PASS] Non-empty Chinese words")
    print("  [PASS] Non-empty Pinyin")
    print("  [PASS] HSK 4 level mapping")
    print("  [PASS] Source ordering")
    print("  [PASS] Sequential IDs")
    print("  [PASS] Source entry markers normalized")
    print("  [PASS] Duplicate visible words allowed")
    print()
    print("Status: HSK 4 SOURCE BASE ONLY - NOT PRODUCTION")
    print("=" * 72)


if __name__ == "__main__":
    main()
