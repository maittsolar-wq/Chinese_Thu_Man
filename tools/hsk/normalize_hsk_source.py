#!/usr/bin/env python3
"""Normalize HSK 3.0 source CSV into the app vocabulary schema.

Run after fetch_hsk_source.py.

Important:
- Removes source entry-disambiguation suffixes such as 本1 -> 本.
- Keeps the original source word in metadata for traceability.
- Does not remove arbitrary digits from the middle of a word.
- Vietnamese meanings/examples/strokes remain enrichment layers.
"""

from pathlib import Path
import csv
import json
import re

SRC = Path("data/raw/hsk/hsk_vocabulary.csv")
OUT = Path("data/normalized/hsk_vocabulary_base.json")

LEVEL_MAP = {
    "一级": 1,
    "二级": 2,
    "三级": 3,
    "四级": 4,
    "五级": 5,
    "六级": 6,
    "七-九级": 7,
}


def parse_primary_level(level_name: str):
    m = re.match(
        r"^(一级|二级|三级|四级|五级|六级|七-九级)",
        level_name.strip(),
    )

    if not m:
        raise ValueError(f"Unknown levelName: {level_name!r}")

    return LEVEL_MAP[m.group(1)]


def cumulative_levels(introduced_level: int):
    if introduced_level >= 7:
        return []

    return list(range(introduced_level, 7))


def normalize_pos(cixing: str):
    return [
        x.strip()
        for x in cixing.split("、")
        if x.strip() and not x.startswith("（")
    ]


def normalize_word(source_word: str):
    """Normalize source entry labels such as 本1 -> 本.

    The HSK source may append a trailing numeric entry marker to
    distinguish multiple dictionary entries for the same visible word.

    Examples:
        本1 -> 本
        本2 -> 本
        点1 -> 点
        和1 -> 和

    Only a trailing 1-9 marker is removed.
    Digits elsewhere are preserved.

    Returns:
        (normalized_word, source_word)
    """

    source_word = source_word.strip()

    # Chinese vocabulary entries in this source are normally Chinese
    # characters, optionally followed by a single entry marker 1-9.
    #
    # We intentionally only remove ONE trailing digit.
    # This avoids broad digit stripping.
    match = re.match(r"^(.*?)([1-9])$", source_word)

    if not match:
        return source_word, source_word

    base_word = match.group(1)

    # Safety check:
    # Only normalize if the remaining part contains Chinese characters.
    if re.search(r"[\u3400-\u9fff]", base_word):
        return base_word, source_word

    return source_word, source_word


def main():
    if not SRC.exists():
        raise SystemExit(
            f"Missing {SRC}. Run fetch_hsk_source.py first."
        )

    records = []
    seen = set()
    normalization_changes = []

    with SRC.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as f:

        for row in csv.DictReader(f):

            source_word = row["word"].strip()

            if not source_word:
                continue

            word, original_word = normalize_word(source_word)

            if word != original_word:
                normalization_changes.append({
                    "sourceWord": original_word,
                    "normalizedWord": word,
                    "sourceSort": int(row["sort"]),
                })

            level = parse_primary_level(row["levelName"])

            if level > 6:
                continue

            # The source's `sort` is the stable source order.
            source_id = f"hsk{level}_{int(row['sort']):04d}"

            if source_id in seen:
                raise ValueError(
                    f"Duplicate source id: {source_id}"
                )

            seen.add(source_id)

            records.append({
                "id": source_id,

                # Clean word used by the application.
                "word": word,

                # Original source value kept for auditability.
                "sourceWord": original_word,

                "pinyin": row["pinyin"].strip(),
                "pinyinNumeric": None,

                "meaningVi": [],

                "introducedLevel": level,
                "hskLevels": cumulative_levels(level),

                "partOfSpeechSource": row["cixing"].strip(),
                "partOfSpeech": normalize_pos(row["cixing"]),

                "sourceSort": int(row["sort"]),
                "sourceLevelName": row["levelName"].strip(),

                "sourceAdditionalLevels": re.findall(
                    r"（([^）]+)）",
                    row["levelName"]
                ),

                "strokeCount": None,
                "characterIds": [],
                "relatedWordIds": [],
                "exampleIds": [],

                "audio": {
                    "wordUrl": None,
                    "exampleUrl": None
                }
            })

    OUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUT.write_text(
        json.dumps(
            records,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print("=" * 60)
    print("HSK SOURCE NORMALIZATION")
    print("=" * 60)

    print(f"Records written: {len(records):,}")
    print(f"Output: {OUT}")

    print()
    print(
        f"Normalized entry markers: "
        f"{len(normalization_changes):,}"
    )

    if normalization_changes:
        print()
        print("Examples:")

        for item in normalization_changes[:20]:
            print(
                f"  {item['sourceWord']} "
                f"-> {item['normalizedWord']}"
            )

    print()
    print("STATUS: NORMALIZATION SUCCESS")


if __name__ == "__main__":
    main()