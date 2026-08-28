#!/usr/bin/env python3
"""Build UI-ready detail data for all 214 Kangxi radicals.

Inputs:
    data/radicals/radicals_214.json
    data/radicals/radical_character_mapping.json
    data/radicals/radical_vocabulary_mapping.json

Output:
    data/radicals/radical_detail_data.json
    data/radicals/radical_detail_data_validation.json

This is a presentation/data-contract layer only. It does not invent meanings,
characters, or vocabulary. Character and vocabulary relationships come from
the completed source-derived mapping files.
"""

from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
RADICAL_ROOT = ROOT / "data" / "radicals"

RADICALS = RADICAL_ROOT / "radicals_214.json"
CHAR_MAPPING = RADICAL_ROOT / "radical_character_mapping.json"
VOCAB_MAPPING = RADICAL_ROOT / "radical_vocabulary_mapping.json"

OUTPUT = RADICAL_ROOT / "radical_detail_data.json"
REPORT = RADICAL_ROOT / "radical_detail_data_validation.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    print("=" * 72)
    print("RADICAL DETAIL DATA BUILD — 214 KANGXI RADICALS")
    print("=" * 72)
    print()
    print(f"Project root:                {ROOT}")

    for path in (RADICALS, CHAR_MAPPING, VOCAB_MAPPING):
        if not path.exists():
            raise SystemExit(f"Missing required file: {path}")

    radicals = load(RADICALS)
    characters = load(CHAR_MAPPING)
    vocab_mapping = load(VOCAB_MAPPING)

    if not isinstance(radicals, list) or len(radicals) != 214:
        raise SystemExit("radicals_214.json must contain exactly 214 records.")

    if not isinstance(characters, list) or len(characters) != 1940:
        raise SystemExit(
            "radical_character_mapping.json must contain exactly 1940 records."
        )

    if not isinstance(vocab_mapping, list) or len(vocab_mapping) != 214:
        raise SystemExit(
            "radical_vocabulary_mapping.json must contain exactly 214 records."
        )

    radical_by_id = {str(r["id"]): r for r in radicals}

    # Build radical -> characters from the authoritative completed character
    # mapping, preserving the mapping's source provenance.
    chars_by_radical = defaultdict(list)

    for item in characters:
        status = str(item.get("mappingStatus") or "")
        if not (
            item.get("verified") is True
            and status.startswith("resolved")
        ):
            raise SystemExit(
                "Character mapping contains a non-resolved/non-verified record: "
                + str(item.get("character"))
            )

        radical_id = str(item.get("radicalId") or "")
        if radical_id not in radical_by_id:
            raise SystemExit(
                f"Character {item.get('character')} has invalid radicalId "
                f"{radical_id!r}."
            )

        chars_by_radical[radical_id].append({
            "character": item["character"],
            "unicode": item.get("unicode"),
            "sourceVocabularyLevels": item.get("sourceVocabularyLevels", []),
            "kangxiIndex": item.get("kangxiIndex"),
            "mappingSource": item.get("mappingSource"),
        })

    vocab_by_radical = {
        str(item["radicalId"]): item
        for item in vocab_mapping
    }

    if len(vocab_by_radical) != 214:
        raise SystemExit("Vocabulary mapping does not contain 214 unique radicals.")

    details = []

    for radical in sorted(
        radicals,
        key=lambda r: int(r.get("kangxiIndex", 999))
    ):
        radical_id = str(radical["id"])
        related_chars = sorted(
            chars_by_radical.get(radical_id, []),
            key=lambda x: ord(x["character"])
        )

        vocab = vocab_by_radical[radical_id]

        vocabulary_by_level = {}
        total_vocabulary = 0

        for level in range(1, 7):
            entries = list(
                vocab.get("vocabularyByLevel", {}).get(str(level), [])
            )

            # UI-ready stable unique list.
            seen = set()
            unique = []

            for entry in entries:
                key = (
                    entry.get("vocabularyId"),
                    entry.get("word"),
                    entry.get("character"),
                )
                if key in seen:
                    continue
                seen.add(key)
                unique.append(entry)

            vocabulary_by_level[str(level)] = unique
            total_vocabulary += len(unique)

        details.append({
            "radicalId": radical_id,
            "radicalCharacter": radical.get("radical"),
            "kangxiIndex": radical.get("kangxiIndex"),
            "strokes": radical.get("strokes"),
            "pinyin": radical.get("pinyin"),
            "meaning": radical.get("meaning"),

            "characterCount": len(related_chars),
            "characters": related_chars,

            "vocabularyCount": total_vocabulary,
            "vocabularyByLevel": vocabulary_by_level,

            "dataStatus": "ready",
            "characterMappingSource": (
                "radical_character_mapping.json"
            ),
            "vocabularyMappingSource": (
                "radical_vocabulary_mapping.json"
            ),
        })

    OUTPUT.write_text(
        json.dumps(details, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    empty_character_radicals = [
        d["kangxiIndex"]
        for d in details
        if d["characterCount"] == 0
    ]

    empty_vocab_radicals = [
        d["kangxiIndex"]
        for d in details
        if d["vocabularyCount"] == 0
    ]

    total_char_links = sum(d["characterCount"] for d in details)
    total_vocab_links = sum(d["vocabularyCount"] for d in details)

    report = {
        "radicals": len(details),
        "expectedRadicals": 214,
        "totalCharacterLinks": total_char_links,
        "expectedCharacters": 1940,
        "totalVocabularyLinks": total_vocab_links,
        "radicalsWithoutCharacters": len(empty_character_radicals),
        "radicalsWithoutVocabulary": len(empty_vocab_radicals),
        "radicalsWithoutVocabularyKangxiIndices": empty_vocab_radicals,
        "errors": 0,
        "status": (
            "PASS"
            if (
                len(details) == 214
                and total_char_links == 1940
                and all(d["dataStatus"] == "ready" for d in details)
            )
            else "FAIL"
        ),
        "note": (
            "This package is a UI-ready projection of source-derived radical "
            "and HSK mappings. Empty vocabulary lists are valid when a radical "
            "does not occur in the HSK 1-6 character set."
        ),
    }

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Radical detail records:       {len(details)}/214")
    print(f"Character links:              {total_char_links}/1940")
    print(f"Vocabulary links:             {total_vocab_links}")
    print(f"Radicals without characters:  {len(empty_character_radicals)}")
    print(f"Radicals without vocabulary:  {len(empty_vocab_radicals)}")
    print(f"Output:                       {OUTPUT}")
    print(f"Validation:                   {REPORT}")
    print()

    if report["status"] != "PASS":
        print("STATUS: FAIL")
        raise SystemExit(1)

    print("STATUS: PASS")
    print("Radical detail data package is ready for UI integration.")


if __name__ == "__main__":
    main()
