#!/usr/bin/env python3
"""Build HSK 3 vocabulary base from the HSK 3.0 source CSV.

Run from project root:
    python tools/hsk/build_hsk3_vocabulary_base.py

Input:
    data/raw/hsk/hsk_vocabulary.csv

Output:
    data/hsk/hsk3/hsk3_vocabulary_base.json
    data/hsk/hsk3/hsk3_vocabulary_base.csv
    data/hsk/hsk3/hsk3_normalization_report.json

Rules:
- HSK 3.0 source entries containing 二级 and/or 三级 are handled by level mapping.
- Only records introduced at HSK 3 are included.
- Source entry suffixes such as word1 -> word are normalized.
- Duplicate visible Chinese words are allowed when source entries differ.
- Meaning, examples, strokes, and audio remain enrichment layers.
- No AI API is called.
- No reviewed or production data is modified.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

SRC = (
    ROOT
    / "data"
    / "raw"
    / "hsk"
    / "hsk_vocabulary.csv"
)

OUT = (
    ROOT
    / "data"
    / "hsk"
    / "hsk3"
)

# HSK 3.0 source uses levelName such as:
#   三级
#   三级（四级）
#   三级（五级）
# We select records whose PRIMARY level is 三级.
PRIMARY_HSK3_PATTERN = re.compile(
    r"^三级(?:（[^）]+）)*$"
)

CHINESE_RE = re.compile(
    r"[\u3400-\u9fff]"
)


def parse_primary_level(level_name: str) -> int | None:
    """Return the primary HSK level from levelName.

    The first level marker determines the introduced level.
    """
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
    """Extract all HSK levels explicitly represented in levelName."""
    mapping = {
        "一级": 1,
        "二级": 2,
        "三级": 3,
        "四级": 4,
        "五级": 5,
        "六级": 6,
        "七-九级": 7,
    }

    levels = []

    for label, level in mapping.items():
        if label in level_name:
            levels.append(level)

    return sorted(set(levels))


def cumulative_levels(introduced_level: int) -> list[int]:
    """HSK cumulative availability through the introduced level."""
    if introduced_level <= 0:
        return []

    if introduced_level <= 6:
        return list(range(1, introduced_level + 1))

    return list(range(1, 7)) + [7]


def normalize_word(source_word: str) -> str:
    """Remove only a trailing source entry marker 1-9.

    Examples:
        过去1 -> 过去
        本1 -> 本
        和1 -> 和

    Digits elsewhere are preserved.
    """
    source_word = source_word.strip()

    match = re.match(
        r"^(.*?)([1-9])$",
        source_word,
    )

    if not match:
        return source_word

    base_word = match.group(1)

    if CHINESE_RE.search(base_word):
        return base_word

    return source_word


def normalize_pos(cixing: str) -> list[str]:
    """Normalize source POS field without inventing POS labels."""
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
    print("HSK 3 VOCABULARY BASE BUILD")
    print("=" * 72)
    print()

    if not SRC.exists():
        raise SystemExit(
            f"Missing source: {SRC}\n"
            "Run:\n"
            "  python tools/hsk/fetch_hsk_source.py"
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

    # Only entries whose PRIMARY introduced level is HSK 3.
    source_rows = [
        row
        for row in rows
        if row.get("type", "").strip() == "1"
        and parse_primary_level(
            row.get("levelName", "").strip()
        ) == 3
    ]

    print(
        f"HSK 3 introduced source rows found: "
        f"{len(source_rows)}"
    )

    if not source_rows:
        raise SystemExit(
            "No HSK 3 introduced records found. "
            "Check source encoding/levelName values."
        )

    records = []
    changes = []
    seen_ids = set()
    seen_source_entries = set()

    for index, row in enumerate(
        source_rows,
        start=1,
    ):
        source_word = row.get(
            "word",
            "",
        ).strip()

        pinyin = row.get(
            "pinyin",
            "",
        ).strip()

        level_name = row.get(
            "levelName",
            "",
        ).strip()

        pos_source = row.get(
            "cixing",
            "",
        ).strip()

        if not source_word:
            raise SystemExit(
                f"Empty word at HSK 3 source row {index}."
            )

        if not pinyin:
            raise SystemExit(
                f"Empty Pinyin for {source_word}."
            )

        source_sort = int(
            row.get("sort", "")
        )

        source_entry_key = (
            source_word,
            pinyin,
            pos_source,
            source_sort,
        )

        if source_entry_key in seen_source_entries:
            raise SystemExit(
                "Duplicate source entry: "
                f"{source_entry_key}"
            )

        seen_source_entries.add(
            source_entry_key
        )

        word = normalize_word(
            source_word
        )

        if word != source_word:
            changes.append(
                {
                    "sourceWord": source_word,
                    "normalizedWord": word,
                    "sourceSort": source_sort,
                }
            )

        introduced_level = parse_primary_level(
            level_name
        )

        if introduced_level != 3:
            raise SystemExit(
                f"Invalid introduced level for "
                f"{source_word}: {level_name!r}"
            )

        all_levels = parse_all_hsk_levels(
            level_name
        )

        if 3 not in all_levels:
            raise SystemExit(
                f"Could not map HSK 3 for "
                f"{source_word}: {level_name!r}"
            )

        record_id = f"hsk3_{index:03d}"

        if record_id in seen_ids:
            raise SystemExit(
                f"Duplicate ID: {record_id}"
            )

        seen_ids.add(record_id)

        records.append(
            {
                "id": record_id,
                "word": word,
                "sourceWord": source_word,
                "pinyin": pinyin,
                "pinyinNumeric": None,
                "meaningVi": [],
                "introducedLevel": 3,
                "hskLevels": cumulative_levels(3),
                "partOfSpeechSource": pos_source,
                "partOfSpeech": normalize_pos(
                    pos_source
                ),
                "sourceSort": source_sort,
                "sourceLevelName": level_name,
                "sourceAdditionalLevels": [
                    value
                    for value in re.findall(
                        r"（([^）]+)）",
                        level_name,
                    )
                ],
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
                        "data/hsk_vocabulary.csv"
                    ),
                    "sourceSort": source_sort,
                    "sourceLevelName": level_name,
                },
            }
        )

    # Validate sequential IDs.
    expected_ids = [
        f"hsk3_{i:03d}"
        for i in range(
            1,
            len(records) + 1,
        )
    ]

    actual_ids = [
        record["id"]
        for record in records
    ]

    if actual_ids != expected_ids:
        raise SystemExit(
            "IDs are not sequential."
        )

    # Validate source order.
    source_sorts = [
        record["sourceSort"]
        for record in records
    ]

    if source_sorts != sorted(
        source_sorts
    ):
        raise SystemExit(
            "Source ordering is not ascending."
        )

    # Duplicate visible words are intentionally allowed.
    duplicate_words = {}

    for record in records:
        duplicate_words.setdefault(
            record["word"],
            [],
        ).append(
            record["id"]
        )

    duplicate_word_groups = {
        word: ids
        for word, ids in duplicate_words.items()
        if len(ids) > 1
    }

    OUT.mkdir(
        parents=True,
        exist_ok=True,
    )

    json_path = (
        OUT
        / "hsk3_vocabulary_base.json"
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
        OUT
        / "hsk3_vocabulary_base.csv"
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
                    record[
                        "sourceLevelName"
                    ],
                ]
            )

    report_path = (
        OUT
        / "hsk3_normalization_report.json"
    )

    report = {
        "status": "SUCCESS",
        "level": 3,
        "recordCount": len(records),
        "normalizedCount": len(changes),
        "duplicateVisibleWordGroups": len(
            duplicate_word_groups
        ),
        "duplicateVisibleWords": (
            duplicate_word_groups
        ),
        "changes": changes,
    }

    report_path.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print("=" * 72)
    print("SUCCESS")
    print("=" * 72)
    print(
        f"HSK 3 introduced records: "
        f"{len(records)}"
    )
    print(
        f"Normalized source entries: "
        f"{len(changes)}"
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
    print("  [PASS] HSK 3 introduced records extracted")
    print("  [PASS] Unique source entries")
    print("  [PASS] Non-empty Chinese words")
    print("  [PASS] Non-empty Pinyin")
    print("  [PASS] HSK 3 level mapping")
    print("  [PASS] Source ordering")
    print("  [PASS] Sequential IDs")
    print("  [PASS] Source entry markers normalized")
    print("  [PASS] Duplicate visible words allowed")
    print()
    print(
        "Status: HSK 3 SOURCE BASE ONLY - NOT PRODUCTION"
    )
    print("=" * 72)


if __name__ == "__main__":
    main()
