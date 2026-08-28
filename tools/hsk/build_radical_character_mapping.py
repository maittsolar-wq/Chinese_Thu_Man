#!/usr/bin/env python3
"""Build a safe Character -> Kangxi Radical mapping package.

This first-stage tool extracts unique Han characters from the existing HSK
vocabulary base/production files and creates a mapping INPUT package. It does
not guess radicals from character appearance and does not create unverified
relations.

Input sources:
    data/hsk/hsk1..hsk6/*vocabulary_base.json
    (uses available base files only)

Output:
    data/radicals/radical_character_mapping_input.json
    data/radicals/radical_character_mapping_report.json

Each character is marked "pending" until a verified radical source is used.
"""

from __future__ import annotations

import json
from pathlib import Path
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
HSK_ROOT = ROOT / "data" / "hsk"
RADICAL_ROOT = ROOT / "data" / "radicals"

OUT = RADICAL_ROOT / "radical_character_mapping_input.json"
REPORT = RADICAL_ROOT / "radical_character_mapping_report.json"


def han_chars(text: str) -> list[str]:
    result = []
    for ch in text:
        name = unicodedata.name(ch, "")
        if "CJK UNIFIED IDEOGRAPH" in name:
            result.append(ch)
    return result


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    print("=" * 72)
    print("RADICAL â†’ CHARACTER MAPPING INPUT BUILD")
    print("=" * 72)
    print()

    RADICAL_ROOT.mkdir(parents=True, exist_ok=True)

    chars = {}
    source_stats = {}

    for level in range(1, 7):
        path = HSK_ROOT / f"hsk{level}" / f"hsk{level}_vocabulary_base.json"
        if not path.exists():
            continue

        records = load_json(path)
        source_stats[f"HSK {level}"] = len(records)

        for record in records:
            word = str(record.get("word") or "")
            for ch in han_chars(word):
                chars.setdefault(ch, {
                    "character": ch,
                    "unicode": f"U+{ord(ch):04X}",
                    "sourceVocabularyLevels": set(),
                    "sourceVocabularyIds": set(),
                })
                chars[ch]["sourceVocabularyLevels"].add(level)
                if record.get("id") is not None:
                    chars[ch]["sourceVocabularyIds"].add(str(record["id"]))

    records = []
    for ch in sorted(chars, key=lambda x: ord(x)):
        item = chars[ch]
        records.append({
            "id": f"char_{ord(ch):04X}",
            "character": ch,
            "unicode": item["unicode"],
            "sourceVocabularyLevels": sorted(item["sourceVocabularyLevels"]),
            "sourceVocabularyIds": sorted(item["sourceVocabularyIds"]),
            "radicalId": None,
            "radicalCharacter": None,
            "mappingStatus": "pending",
            "mappingSource": None,
            "verified": False,
        })

    OUT.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report = {
        "uniqueHanCharacters": len(records),
        "sourceStats": source_stats,
        "mapped": 0,
        "pending": len(records),
        "verified": 0,
        "status": "PASS" if records else "FAIL",
        "note": (
            "This is a mapping input package only. No character-to-radical "
            "relation was invented. Radical mapping remains pending until "
            "supported by a dedicated character-radical reference."
        ),
    }
    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Unique Han characters:       {len(records)}")
    for k, v in source_stats.items():
        print(f"{k} base records:             {v}")
    print("Mapped:                       0")
    print(f"Pending mapping:             {len(records)}")
    print("Verified:                    0")
    print(f"Input:                       {OUT}")
    print(f"Report:                      {REPORT}")
    print()
    print("SUCCESS")
    print("Character mapping input package created.")
    print("No radical relation was invented.")
    print("Next step: resolve Character â†’ Kangxi Radical from a dedicated reference.")


if __name__ == "__main__":
    main()

