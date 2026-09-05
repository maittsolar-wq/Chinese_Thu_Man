"""
Stroke Count Pass 02 — step 1: extract distinct characters from the 6
production vocabulary files.

Read-only against production data. Writes only into
tools/hsk/stroke_count/. Does not modify any production JSON.

Digit-suffix rule (explicit, auditable — NOT a blanket "strip all
non-Han" rule): a word matches the known disambiguation pattern only if
it is one-or-more Han characters followed by EXACTLY one trailing ASCII
digit 1-9. Anything else that contains a non-Han character is reported
as an unexpected case for the review queue, never silently stripped.
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent

HAN_RANGES = [
    (0x3400, 0x4DBF),   # CJK Extension A
    (0x4E00, 0x9FFF),   # CJK Unified Ideographs
    (0xF900, 0xFAFF),   # CJK Compatibility Ideographs
]

def is_han(ch: str) -> bool:
    cp = ord(ch)
    return any(lo <= cp <= hi for lo, hi in HAN_RANGES)

DIGIT_SUFFIX_RE = re.compile(r"^([㐀-䶿一-鿿豈-﫿]+)([1-9])$")

def normalize_word(word: str):
    """Returns (normalized_word, suffix_stripped: bool, suffix_digit: str|None)."""
    m = DIGIT_SUFFIX_RE.match(word)
    if m:
        return m.group(1), True, m.group(2)
    return word, False, None

def main():
    levels = [1, 2, 3, 4, 5, 6]
    all_chars = set()
    length_dist = {}
    digit_suffix_records = []
    unexpected_non_han = []
    per_record = []
    total = 0

    for lvl in levels:
        path = REPO_ROOT / "data" / "hsk" / f"hsk{lvl}" / f"hsk{lvl}_vocabulary_production.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for rec in data:
            total += 1
            word = rec["word"]
            rid = rec["id"]
            normalized, stripped, digit = normalize_word(word)
            length_dist[len(word)] = length_dist.get(len(word), 0) + 1

            if stripped:
                digit_suffix_records.append({
                    "id": rid, "word": word, "normalizedWord": normalized, "digit": digit,
                })

            # Any character in the NORMALIZED word that isn't Han is unexpected.
            for ch in normalized:
                if not is_han(ch):
                    unexpected_non_han.append({
                        "id": rid, "word": word, "character": ch,
                        "codepoint": f"U+{ord(ch):04X}",
                    })
                all_chars.add(ch)

            per_record.append({
                "id": rid, "hskLevel": lvl, "word": word, "normalizedWord": normalized,
                "digitSuffixStripped": stripped,
            })

    result = {
        "totalRecords": total,
        "wordLengthDistribution": {str(k): v for k, v in sorted(length_dist.items())},
        "distinctCharacterCount": len(all_chars),
        "distinctCharacters": sorted(all_chars),
        "digitSuffixRecordCount": len(digit_suffix_records),
        "digitSuffixRecords": digit_suffix_records,
        "unexpectedNonHanCount": len(unexpected_non_han),
        "unexpectedNonHan": unexpected_non_han,
    }

    out_path = OUT_DIR / "vocabulary_character_extraction.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    (OUT_DIR / "vocabulary_records_normalized.json").write_text(
        json.dumps(per_record, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"totalRecords={total}")
    print(f"wordLengthDistribution={result['wordLengthDistribution']}")
    print(f"distinctCharacterCount={len(all_chars)}")
    print(f"digitSuffixRecordCount={len(digit_suffix_records)}")
    print(f"unexpectedNonHanCount={len(unexpected_non_han)}")
    if unexpected_non_han:
        print("UNEXPECTED NON-HAN CHARACTERS FOUND:")
        for item in unexpected_non_han:
            print(f"  {item}")

if __name__ == "__main__":
    sys.exit(main())
