#!/usr/bin/env python3
"""Build Radical -> HSK vocabulary mapping.

Inputs:
    data/radicals/radicals_214.json
    data/radicals/radical_character_mapping.json
    data/hsk/hsk1..hsk6/*_vocabulary_base.json

Logic:
    1. Use the completed Character -> Kangxi Radical mapping.
    2. For each HSK vocabulary word, extract its Han characters.
    3. Connect the vocabulary record to every radical represented by a
       character in that word.
    4. Preserve the exact HSK vocabulary IDs and levels.
    5. Do not infer additional radical relationships.

Outputs:
    data/radicals/radical_vocabulary_mapping.json
    data/radicals/radical_vocabulary_mapping_validation.json
"""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
RADICAL_ROOT = ROOT / "data" / "radicals"
HSK_ROOT = ROOT / "data" / "hsk"

CHAR_MAPPING = RADICAL_ROOT / "radical_character_mapping.json"
RADICALS = RADICAL_ROOT / "radicals_214.json"

OUTPUT = RADICAL_ROOT / "radical_vocabulary_mapping.json"
REPORT = RADICAL_ROOT / "radical_vocabulary_mapping_validation.json"


def is_han(ch: str) -> bool:
    return "CJK UNIFIED IDEOGRAPH" in unicodedata.name(ch, "")


def han_chars(text: str) -> list[str]:
    return [ch for ch in text if is_han(ch)]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    print("=" * 72)
    print("RADICAL → HSK VOCABULARY MAPPING BUILD")
    print("=" * 72)
    print()
    print(f"Project root:                {ROOT}")

    for path in (CHAR_MAPPING, RADICALS):
        if not path.exists():
            raise SystemExit(f"Missing required file: {path}")

    char_mapping = load_json(CHAR_MAPPING)
    radicals = load_json(RADICALS)

    if not isinstance(char_mapping, list):
        raise SystemExit("radical_character_mapping.json must be a list.")

    if not isinstance(radicals, list) or len(radicals) != 214:
        raise SystemExit("radicals_214.json must contain exactly 214 records.")

    radical_by_id = {
        str(r["id"]): r for r in radicals
    }

    # Only completed, source-derived mappings are allowed into this layer.
    character_to_radical = {}

    for item in char_mapping:
        character = str(item.get("character") or "")
        radical_id = item.get("radicalId")
        status = str(item.get("mappingStatus") or "")
        verified = item.get("verified") is True

        if (
            character
            and radical_id
            and status.startswith("resolved")
            and verified
            and str(radical_id) in radical_by_id
        ):
            character_to_radical[character] = str(radical_id)

    if len(character_to_radical) != 1940:
        raise SystemExit(
            "Character mapping is not complete: "
            f"{len(character_to_radical)}/1940 usable mappings."
        )

    # radical_id -> levels -> vocabulary records
    buckets = defaultdict(lambda: defaultdict(list))
    total_vocab_records = 0
    total_han_character_occurrences = 0
    mapped_vocab_records = set()
    unmapped_chars = set()

    source_stats = {}

    for level in range(1, 7):
        path = (
            HSK_ROOT
            / f"hsk{level}"
            / f"hsk{level}_vocabulary_base.json"
        )

        if not path.exists():
            raise SystemExit(f"Missing HSK {level} base: {path}")

        records = load_json(path)

        if not isinstance(records, list):
            raise SystemExit(f"Invalid HSK {level} base: {path}")

        source_stats[f"HSK {level}"] = len(records)
        total_vocab_records += len(records)

        for record in records:
            if not isinstance(record, dict):
                continue

            word = str(record.get("word") or "")
            chars = list(dict.fromkeys(han_chars(word)))

            for character in chars:
                total_han_character_occurrences += 1

                radical_id = character_to_radical.get(character)

                if radical_id is None:
                    unmapped_chars.add(character)
                    continue

                radical = radical_by_id[radical_id]

                vocabulary_id = str(
                    record.get("id")
                    or f"hsk{level}_{record.get('sort', '')}"
                )

                entry = {
                    "vocabularyId": vocabulary_id,
                    "word": word,
                    "pinyin": record.get("pinyin"),
                    "level": level,
                    "character": character,
                }

                buckets[radical_id][level].append(entry)
                mapped_vocab_records.add((level, vocabulary_id))

    output = []

    for radical in sorted(
        radicals,
        key=lambda r: int(r.get("kangxiIndex", 999))
    ):
        radical_id = str(radical["id"])
        level_map = buckets.get(radical_id, {})

        levels = {}
        all_vocab = []

        for level in range(1, 7):
            entries = level_map.get(level, [])

            # Stable de-duplication.
            seen = set()
            unique_entries = []

            for entry in entries:
                key = (
                    entry["vocabularyId"],
                    entry["word"],
                    entry["character"],
                )
                if key in seen:
                    continue
                seen.add(key)
                unique_entries.append(entry)

            levels[str(level)] = unique_entries
            all_vocab.extend(unique_entries)

        output.append({
            "radicalId": radical_id,
            "radicalCharacter": radical["radical"],
            "kangxiIndex": radical["kangxiIndex"],
            "strokes": radical.get("strokes"),
            "pinyin": radical.get("pinyin"),
            "meaning": radical.get("meaning"),
            "vocabularyCount": len(all_vocab),
            "vocabularyByLevel": levels,
            "mappingSource": "Character → Kangxi Radical + HSK vocabulary base",
        })

    OUTPUT.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    radicals_with_vocab = sum(
        1 for r in output if r["vocabularyCount"] > 0
    )

    total_links = sum(r["vocabularyCount"] for r in output)

    report = {
        "radicals": len(output),
        "expectedRadicals": 214,
        "hskVocabularyRecords": total_vocab_records,
        "characterMappingRecords": len(char_mapping),
        "usableCharacterMappings": len(character_to_radical),
        "radicalsWithVocabulary": radicals_with_vocab,
        "radicalsWithoutVocabulary": 214 - radicals_with_vocab,
        "totalRadicalVocabularyLinks": total_links,
        "unmappedHanCharactersInVocabulary": sorted(unmapped_chars),
        "sourceStats": source_stats,
        "errors": 0,
        "status": (
            "PASS"
            if (
                len(output) == 214
                and len(character_to_radical) == 1940
                and not unmapped_chars
            )
            else "PASS_WITH_WARNINGS"
        ),
        "note": (
            "A vocabulary word is linked to every radical represented by "
            "its Han characters. This is a character-presence relationship, "
            "not a claim that the radical is the semantic component of the "
            "whole word."
        ),
    }

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Radicals:                    {len(output)}/214")
    print(f"Usable character mappings:   {len(character_to_radical)}/1940")
    print(f"HSK vocabulary records:      {total_vocab_records}")
    print(f"Radicals with vocabulary:     {radicals_with_vocab}/214")
    print(f"Radical-vocabulary links:     {total_links}")
    print(f"Unmapped Han characters:      {len(unmapped_chars)}")
    print(f"Output:                       {OUTPUT}")
    print(f"Validation:                   {REPORT}")
    print()

    if len(output) != 214 or len(character_to_radical) != 1940:
        print("STATUS: FAIL")
        raise SystemExit(1)

    if unmapped_chars:
        print("STATUS: PASS_WITH_WARNINGS")
        print("Some vocabulary characters are outside the completed 1940-character mapping.")
        print("No relationship was invented for those characters.")
    else:
        print("STATUS: PASS")
        print("Radical → HSK vocabulary mapping completed.")


if __name__ == "__main__":
    main()
