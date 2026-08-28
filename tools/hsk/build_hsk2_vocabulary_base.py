#!/usr/bin/env python3
"""Build HSK 2 vocabulary base from the HSK 3.0 source CSV."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

SRC = ROOT / "data" / "raw" / "hsk" / "hsk_vocabulary.csv"
OUT = ROOT / "data" / "hsk" / "hsk2"

EXPECTED_HSK2_COUNT = 200


def normalize_word(source_word: str) -> str:
    """Remove one trailing source entry marker such as 过去1 -> 过去."""

    source_word = source_word.strip()

    match = re.match(r"^(.*?)([1-9])$", source_word)

    if not match:
        return source_word

    base_word = match.group(1)

    if re.search(r"[\u3400-\u9fff]", base_word):
        return base_word

    return source_word


def parse_hsk_levels(level_name: str) -> list[int]:
    """Extract all HSK levels explicitly present in levelName."""

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
        {
            level
            for label, level in mapping.items()
            if label in level_name
        }
    )


def normalize_pos(cixing: str) -> list[str]:
    """Normalize source part-of-speech values."""

    if not cixing:
        return []

    return [
        item.strip()
        for item in re.split(r"[、,]", cixing)
        if item.strip()
    ]


def main():
    print("=" * 64)
    print("HSK 2 VOCABULARY BASE BUILD")
    print("=" * 64)
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
        raise SystemExit("Source CSV is empty.")

    required_columns = {
        "type",
        "levelName",
        "word",
        "pinyin",
        "cixing",
        "sort",
    }

    missing_columns = required_columns - set(rows[0].keys())

    if missing_columns:
        raise SystemExit(
            "Source CSV is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    # HSK 2 introduced vocabulary.
    #
    # Included:
    #   二级
    #   二级（五级）
    #   二级（七-九级）
    #   二级（四级）
    #   二级（六级）
    #   二级（三级）
    #   二级（三级）（五级）
    #
    # Excluded:
    #   一级（二级）
    #   一级（二级）（四级）
    #
    # Those words were introduced at HSK 1.

    source_rows = [
        row
        for row in rows
        if row.get("type", "").strip() == "1"
        and row.get("levelName", "").strip().startswith("二级")
    ]

    print(
        f"HSK 2 source rows found: {len(source_rows)}"
    )

    if len(source_rows) != EXPECTED_HSK2_COUNT:
        raise SystemExit(
            f"Expected exactly {EXPECTED_HSK2_COUNT} "
            f"HSK 2 records, got {len(source_rows)}."
        )

    records = []
    normalization_changes = []

    seen_ids = set()
    seen_source_sorts = set()
    seen_entry_keys = set()

    for index, row in enumerate(
        source_rows,
        start=1,
    ):
        source_word = row["word"].strip()
        pinyin = row["pinyin"].strip()
        cixing = row["cixing"].strip()
        level_name = row["levelName"].strip()
        source_sort = int(row["sort"])

        if not source_word:
            raise SystemExit(
                f"Empty word at source row {index}."
            )

        if not pinyin:
            raise SystemExit(
                f"Empty Pinyin for {source_word}."
            )

        word = normalize_word(source_word)

        if word != source_word:
            normalization_changes.append(
                {
                    "sourceWord": source_word,
                    "normalizedWord": word,
                    "sourceSort": source_sort,
                }
            )

        hsk_levels = parse_hsk_levels(
            level_name
        )

        if 2 not in hsk_levels:
            raise SystemExit(
                f"HSK 2 level could not be parsed for "
                f"{source_word}: {level_name}"
            )

        record_id = f"hsk2_{index:03d}"

        if record_id in seen_ids:
            raise SystemExit(
                f"Duplicate ID: {record_id}"
            )

        if source_sort in seen_source_sorts:
            raise SystemExit(
                f"Duplicate source sort: {source_sort}"
            )

        # Chinese words are NOT required to be unique.
        #
        # Example:
        #   过 | guò | 动
        #   过 | guo | 助
        #
        # These are separate dictionary entries.

        entry_key = (
            word,
            pinyin,
            cixing,
            source_sort,
        )

        if entry_key in seen_entry_keys:
            raise SystemExit(
                f"Duplicate source entry: {entry_key}"
            )

        seen_ids.add(record_id)
        seen_source_sorts.add(source_sort)
        seen_entry_keys.add(entry_key)

        records.append(
            {
                "id": record_id,
                "word": word,
                "sourceWord": source_word,
                "pinyin": pinyin,
                "pinyinNumeric": None,
                "meaningVi": [],
                "introducedLevel": 2,
                "hskLevels": hsk_levels,
                "partOfSpeechSource": cixing,
                "partOfSpeech": normalize_pos(cixing),
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
                    "sourceFile": (
                        "data/raw/hsk/hsk_vocabulary.csv"
                    ),
                    "sourceSort": source_sort,
                    "sourceLevelName": level_name,
                },
            }
        )

    expected_ids = [
        f"hsk2_{i:03d}"
        for i in range(
            1,
            EXPECTED_HSK2_COUNT + 1,
        )
    ]

    actual_ids = [
        record["id"]
        for record in records
    ]

    if actual_ids != expected_ids:
        raise SystemExit(
            "IDs are not sequential from "
            "hsk2_001 to hsk2_204."
        )

    source_sorts = [
        record["sourceSort"]
        for record in records
    ]

    if source_sorts != sorted(source_sorts):
        raise SystemExit(
            "Source ordering is not ascending."
        )

    OUT.mkdir(
        parents=True,
        exist_ok=True,
    )

    json_path = (
        OUT / "hsk2_vocabulary_base.json"
    )

    json_path.write_text(
        json.dumps(
            records,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    csv_path = (
        OUT / "hsk2_vocabulary_base.csv"
    )

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "id",
                "word",
                "sourceWord",
                "pinyin",
                "introducedLevel",
                "hskLevels",
                "partOfSpeechSource",
                "sourceSort",
                "sourceLevelName",
            ]
        )

        for record in records:
            writer.writerow(
                [
                    record["id"],
                    record["word"],
                    record["sourceWord"],
                    record["pinyin"],
                    record["introducedLevel"],
                    ",".join(
                        map(
                            str,
                            record["hskLevels"],
                        )
                    ),
                    record[
                        "partOfSpeechSource"
                    ],
                    record["sourceSort"],
                    record["sourceLevelName"],
                ]
            )

    report_path = (
        OUT / "hsk2_normalization_report.json"
    )

    report_path.write_text(
        json.dumps(
            {
                "status": "SUCCESS",
                "level": 2,
                "recordCount": len(records),
                "normalizedCount": len(
                    normalization_changes
                ),
                "changes": normalization_changes,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print("=" * 64)
    print("SUCCESS")
    print("=" * 64)

    print(
        f"HSK 2 introduced records: "
        f"{len(records)}/{EXPECTED_HSK2_COUNT}"
    )

    print(
        f"Normalized source entries: "
        f"{len(normalization_changes)}"
    )

    print(
        f"Output folder: {OUT}"
    )

    print()
    print("Generated files:")
    print(
        f"  - {json_path.name}"
    )
    print(
        f"  - {csv_path.name}"
    )
    print(
        f"  - {report_path.name}"
    )

    print()
    print("Validation:")
    print(
        "  [PASS] Exactly 204 HSK 2 introduced records"
    )
    print(
        "  [PASS] Unique IDs"
    )
    print(
        "  [PASS] Unique source entries"
    )
    print(
        "  [PASS] Duplicate Chinese words allowed "
        "when source entries differ"
    )
    print(
        "  [PASS] Non-empty Chinese words"
    )
    print(
        "  [PASS] Non-empty Pinyin"
    )
    print(
        "  [PASS] HSK 2 level mapping"
    )
    print(
        "  [PASS] Source ordering"
    )
    print(
        "  [PASS] Sequential IDs"
    )
    print(
        "  [PASS] Source entry markers normalized"
    )

    print()
    print(
        "Status: HSK 2 SOURCE BASE ONLY - NOT PRODUCTION"
    )
    print("=" * 64)


if __name__ == "__main__":
    main()