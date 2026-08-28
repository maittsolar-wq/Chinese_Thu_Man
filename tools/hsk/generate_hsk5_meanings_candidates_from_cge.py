#!/usr/bin/env python3
"""Generate HSK 5 Vietnamese meaning candidates from CGE's HSK 3.0 list.

The CGE page contains the cumulative HSK 1-5 vocabulary (4316 records)
and Vietnamese meanings. This script matches the project's 1600 HSK 5
records by Chinese word + normalized Pinyin.

Input:
    data/hsk/hsk5/hsk5_meanings_candidates_input.json

Output:
    data/hsk/hsk5/hsk5_meanings_candidates_input.json

Safety:
- Existing candidate meanings are preserved.
- Only reference-derived Vietnamese meanings are added.
- No meaning is invented.
- Base/reviewed/production data is not modified.
"""

from __future__ import annotations

import html
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk5"
INPUT = DATA / "hsk5_meanings_candidates_input.json"

URL = "https://cge.edu.vn/tieng-trung-hsk/tu-vung-hsk-5.html"
EXPECTED = 1600


class TableParser(HTMLParser):
    """Collect table rows/cells from the CGE HTML."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_row = False
        self.in_cell = False
        self.cell_text = []
        self.row = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()

        if tag == "tr":
            self.in_row = True
            self.row = []

        elif tag in {"td", "th"} and self.in_row:
            self.in_cell = True
            self.cell_text = []

        elif tag == "br" and self.in_cell:
            self.cell_text.append(" ")

    def handle_data(self, data):
        if self.in_cell:
            self.cell_text.append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag in {"td", "th"} and self.in_cell:
            value = html.unescape(
                "".join(self.cell_text)
            )
            value = re.sub(r"\s+", " ", value).strip()
            self.row.append(value)
            self.in_cell = False
            self.cell_text = []

        elif tag == "tr" and self.in_row:
            if self.row:
                self.rows.append(self.row)
            self.row = []
            self.in_row = False


def fetch(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/139 Safari/537.36"
            ),
            "Accept-Language": "vi,en;q=0.9",
        },
    )

    with urllib.request.urlopen(
        request,
        timeout=60,
    ) as response:
        return response.read().decode(
            "utf-8",
            errors="replace",
        )


def norm_word(value: str) -> str:
    return re.sub(
        r"\s+",
        "",
        value.strip(),
    )


def norm_pinyin(value: str) -> str:
    value = value.strip().strip("/")
    value = value.replace("’", "'")
    value = re.sub(r"\s+", "", value)
    return value.casefold()


def looks_chinese(value: str) -> bool:
    return bool(
        re.search(
            r"[\u3400-\u9fff]",
            value,
        )
    )


def clean_meaning(value: str) -> str:
    value = re.sub(
        r"\s+",
        " ",
        value,
    ).strip()

    # CGE sometimes includes surrounding punctuation.
    value = value.strip(" ;；|")

    return value


def build_reference(html_text: str):
    parser = TableParser()
    parser.feed(html_text)

    reference = {}
    usable_rows = 0

    for row in parser.rows:
        if len(row) < 5:
            continue

        # Expected CGE columns:
        # STT | Từ tiếng Trung | Phiên âm | Loại từ | Nghĩa tiếng Việt | ...
        word = norm_word(row[1])
        pinyin = norm_pinyin(row[2])
        meaning = clean_meaning(row[4])

        if not word or not pinyin or not meaning:
            continue

        if not looks_chinese(word):
            continue

        # Avoid header rows.
        if word in {
            "Từ tiếng Trung",
            "Hán tự",
            "TỪ VỰNG HSK5",
        }:
            continue

        key = (
            word,
            pinyin,
        )

        reference.setdefault(key, [])

        if meaning not in reference[key]:
            reference[key].append(meaning)

        usable_rows += 1

    return reference, usable_rows


def main():
    print("=" * 72)
    print("HSK 5 MEANING CANDIDATES — CGE VIETNAMESE REFERENCE")
    print("=" * 72)
    print()

    if not INPUT.exists():
        raise SystemExit(
            f"Missing input: {INPUT}"
        )

    records = json.loads(
        INPUT.read_text(
            encoding="utf-8"
        )
    )

    if not isinstance(records, list):
        raise SystemExit(
            "Candidate input root must be a JSON array."
        )

    if len(records) != EXPECTED:
        raise SystemExit(
            f"Expected {EXPECTED} records, "
            f"got {len(records)}."
        )

    print(
        f"Candidate records:       "
        f"{len(records)}/{EXPECTED}"
    )
    print(f"Reference:               {URL}")
    print()

    try:
        source = fetch(URL)
    except Exception as exc:
        raise SystemExit(
            "Could not fetch CGE reference.\n"
            f"Error: {exc}"
        )

    reference, usable_rows = build_reference(source)

    print(
        f"Reference rows parsed:   "
        f"{usable_rows}"
    )
    print(
        f"Reference mappings:      "
        f"{len(reference)}"
    )

    before_resolved = 0
    after_resolved = 0
    newly_resolved = 0
    unresolved = []

    for record in records:
        existing = record.get(
            "candidateMeanings",
            [],
        )

        if not isinstance(existing, list):
            existing = []

        existing_clean = []
        seen = set()

        for meaning in existing:
            if not isinstance(meaning, str):
                continue

            meaning = meaning.strip()

            if not meaning:
                continue

            key = meaning.casefold()

            if key not in seen:
                seen.add(key)
                existing_clean.append(meaning)

        if existing_clean:
            before_resolved += 1

        key = (
            norm_word(record.get("word", "")),
            norm_pinyin(record.get("pinyin", "")),
        )

        reference_meanings = reference.get(
            key,
            [],
        )

        merged = list(existing_clean)

        for meaning in reference_meanings:
            key_meaning = meaning.casefold()

            if key_meaning not in {
                x.casefold()
                for x in merged
            }:
                merged.append(meaning)

        if not existing_clean and merged:
            newly_resolved += 1

        record["candidateMeanings"] = merged

        if merged:
            record["generationStatus"] = (
                "generated_reference_assisted_unverified"
            )
            record["generationSource"] = (
                "cge_hsk30_vietnamese_reference"
            )
            after_resolved += 1
        else:
            record["generationStatus"] = (
                "needs_manual_verification"
            )
            record["generationSource"] = (
                "no_vietnamese_reference_match"
            )
            unresolved.append(
                record.get("id")
            )

    INPUT.write_text(
        json.dumps(
            records,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print("SUCCESS")
    print(
        f"Previously resolved:        "
        f"{before_resolved}/{EXPECTED}"
    )
    print(
        f"Newly resolved from CGE:    "
        f"{newly_resolved}"
    )
    print(
        f"Total resolved:             "
        f"{after_resolved}/{EXPECTED}"
    )
    print(
        f"Still unresolved:           "
        f"{len(unresolved)}"
    )
    print(
        f"Output:                     {INPUT}"
    )
    print()
    print("IMPORTANT:")
    print("- Existing candidates were preserved.")
    print("- CGE Vietnamese meanings were added by exact word+pinyin match.")
    print("- No meaning was invented.")
    print("- Base/reviewed/production data was not modified.")

    if unresolved:
        print()
        print("First unresolved IDs:")
        print(
            ", ".join(unresolved[:50])
        )
        if len(unresolved) > 50:
            print(
                f"... and {len(unresolved) - 50} more."
            )


if __name__ == "__main__":
    main()
