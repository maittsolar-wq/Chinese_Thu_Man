#!/usr/bin/env python3
"""Generate HSK 4 Vietnamese meaning candidates from a public reference.

Input:
    data/hsk/hsk4/hsk4_meanings_candidates_input.json

Reference:
    Public Google Sheet containing the HSK 3.0 HSK 4 vocabulary and
    Vietnamese meanings.

Output:
    data/hsk/hsk4/hsk4_meanings_candidates_input.json

This step only fills candidateMeanings. It does NOT approve meanings,
modify reviewed data, or create production data.
"""

from __future__ import annotations

import csv
import io
import json
import re
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk4"
INPUT = DATA / "hsk4_meanings_candidates_input.json"
OUTPUT = INPUT

SHEET_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "15F4d1XVroehGluwvUaBAExWiUkQaIIirnQ-NsbTQglw/"
    "export?format=csv"
)

EXPECTED_COUNT = 1000


def fetch_csv() -> str:
    req = urllib.request.Request(
        SHEET_CSV_URL,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8-sig", errors="replace")


def normalize_pinyin(value: str) -> str:
    value = value.strip().strip("/")
    value = value.replace("’", "'")
    value = re.sub(r"\s+", "", value)
    return value.casefold()


def normalize_word(value: str) -> str:
    value = value.strip()
    # Source markers such as 乘1 / 重2 are normalized by the base build.
    value = re.sub(r"[1-9]+$", "", value)
    return value


def load_reference() -> dict[tuple[str, str], list[str]]:
    text = fetch_csv()
    rows = list(csv.reader(io.StringIO(text)))

    header_index = None
    for i, row in enumerate(rows):
        normalized = [str(x).strip().casefold() for x in row]
        if "từ tiếng trung" in normalized:
            header_index = i
            break

    if header_index is None:
        raise RuntimeError(
            "Could not locate the vocabulary header in the Google Sheet."
        )

    header = [
        str(x).strip().casefold()
        for x in rows[header_index]
    ]

    word_col = header.index("từ tiếng trung")
    pinyin_col = header.index("phiên âm")
    meaning_col = header.index("nghĩa tiếng việt")

    result: dict[tuple[str, str], list[str]] = {}

    for row in rows[header_index + 1:]:
        if len(row) <= max(word_col, pinyin_col, meaning_col):
            continue

        word = normalize_word(row[word_col])
        pinyin = normalize_pinyin(row[pinyin_col])
        meaning = row[meaning_col].strip()

        if not word or not pinyin or not meaning:
            continue

        # Remove duplicated POS fragments if the source has multi-row
        # meanings. Keep the Vietnamese wording as a candidate.
        meaning = re.sub(r"\s+", " ", meaning).strip()

        key = (word, pinyin)
        result.setdefault(key, [])

        if meaning not in result[key]:
            result[key].append(meaning)

    return result


def main():
    print("=" * 72)
    print("HSK 4 MEANING CANDIDATES GENERATION")
    print("=" * 72)
    print()

    if not INPUT.exists():
        raise SystemExit(f"Missing input: {INPUT}")

    records = json.loads(
        INPUT.read_text(encoding="utf-8")
    )

    if not isinstance(records, list):
        raise SystemExit("Candidate input root must be a JSON array.")

    if len(records) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} records, got {len(records)}."
        )

    print(
        f"Candidate records:       "
        f"{len(records)}/{EXPECTED_COUNT}"
    )
    print("Reference: public HSK 4 Vietnamese vocabulary sheet")
    print("AI API called: NO")
    print()

    try:
        reference = load_reference()
    except Exception as exc:
        raise SystemExit(
            "Could not load the Vietnamese reference.\n"
            f"Error: {exc}"
        )

    print(
        f"Reference entries loaded: {len(reference)}"
    )

    enriched = []
    missing = []

    for record in records:
        key = (
            normalize_word(record["word"]),
            normalize_pinyin(record["pinyin"]),
        )

        candidates = reference.get(key, [])

        if not candidates:
            missing.append(record["id"])
            # Explicitly keep unresolved records visible to downstream
            # validation instead of inventing a meaning.
            candidates = [
                f"[CẦN XÁC MINH] {record['word']}"
            ]

        item = dict(record)
        item["candidateMeanings"] = candidates
        item["generationStatus"] = (
            "generated_ai_assisted_unverified"
        )
        item["generationSource"] = (
            "vietnamese_reference_candidate"
        )
        enriched.append(item)

    OUTPUT.write_text(
        json.dumps(
            enriched,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    generated = EXPECTED_COUNT - len(missing)

    print()
    print("SUCCESS")
    print(
        f"Generated candidate records: "
        f"{len(enriched)}/{EXPECTED_COUNT}"
    )
    print(
        f"Resolved from reference:     "
        f"{generated}/{EXPECTED_COUNT}"
    )
    print(
        f"Needs manual verification:   "
        f"{len(missing)}"
    )
    print(f"Output:                       {OUTPUT}")
    print()
    print("IMPORTANT:")
    print("- Meanings are candidates, not ground truth.")
    print("- No automatic production approval.")
    print("- Reviewed data was not modified.")
    print("- Production data was not modified.")

    if missing:
        print()
        print("Missing IDs:")
        print(", ".join(missing[:100]))
        if len(missing) > 100:
            print(f"... and {len(missing) - 100} more.")


if __name__ == "__main__":
    main()
