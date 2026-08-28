#!/usr/bin/env python3
"""Generate HSK 5 Vietnamese meaning candidates.

Matches the project's 1,600 HSK 5 records against Vietnamese HSK 3.0
reference pages. It uses Chinese + normalized Pinyin as the primary key.

Reference pages:
- LTL Chinese Vietnamese HSK 5 list
- Laoshi Vietnamese HSK 3.0 Level 5 list
- CGE Vietnamese HSK 5 3.0 list

Important:
- This script NEVER invents a meaning.
- Unmatched records remain explicitly unresolved.
- Candidate meanings are reference-assisted and unverified.
- Base/reviewed/production data are not modified.
"""

from __future__ import annotations

import json
import re
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk5"
INPUT = DATA / "hsk5_meanings_candidates_input.json"
OUTPUT = INPUT
EXPECTED = 1600

URLS = [
    "https://hsk-exam.com/vn/blog/hsk-5-vocabulary-list",
    "https://laoshi.io/characters/vi/hsk/new-level5/",
    "https://cge.edu.vn/tieng-trung-hsk/tu-vung-hsk-5.html",
]


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def strip_html(text: str) -> str:
    text = re.sub(r"(?is)<script.*?</script>", " ", text)
    text = re.sub(r"(?is)<style.*?</style>", " ", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def norm_pinyin(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("’", "'").replace(" ", "")
    value = re.sub(r"[^a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü'0-9]", "", value)
    return value


def norm_word(value: str) -> str:
    return re.sub(r"\s+", "", value.strip())


def extract_vietnamese_table(text: str):
    """Extract simple Chinese | Pinyin | Vietnamese rows from source text."""
    result = {}

    # Markdown/table-like extraction from rendered source.
    patterns = [
        re.compile(
            r"([一-鿿]{1,8})\s*\|\s*"
            r"([A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü' ]+)\s*\|\s*"
            r"([^|]{1,300})"
        ),
        re.compile(
            r"([一-鿿]{1,8})\s+"
            r"([A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü' ]+)\s+"
            r"((?:thán từ|động từ|danh từ|tính từ|phó từ|liên từ|"
            r"giới từ|lượng từ|trợ từ|đại từ|số từ|[A-ZÀ-Ỹa-zà-ỹ]).{1,250}?)"
            r"(?=\s+[一-鿿]{1,8}\s+|$)"
        ),
    ]

    for pattern in patterns:
        for m in pattern.finditer(text):
            word = norm_word(m.group(1))
            py = norm_pinyin(m.group(2))
            meaning = re.sub(r"\s+", " ", m.group(3)).strip()

            if not word or not py or not meaning:
                continue

            # Keep only Vietnamese-looking definitions.
            if not re.search(
                r"[À-ỹ]|(?:anh|chị|em|người|cái|việc|làm|có|động|danh|"
                r"tính|phó|trợ|thán|bằng|trên|dưới|đến|cho|về|với)\b",
                meaning,
                re.I,
            ):
                continue

            key = (word, py)
            result.setdefault(key, [])
            if meaning not in result[key]:
                result[key].append(meaning)

    return result


def main():
    print("=" * 72)
    print("HSK 5 MEANING CANDIDATES GENERATION")
    print("=" * 72)
    print()

    if not INPUT.exists():
        raise SystemExit(f"Missing input: {INPUT}")

    records = json.loads(INPUT.read_text(encoding="utf-8"))

    if not isinstance(records, list) or len(records) != EXPECTED:
        raise SystemExit(
            f"Expected {EXPECTED} candidate records."
        )

    reference = {}

    for url in URLS:
        try:
            raw = fetch(url)
            text = strip_html(raw)
            found = extract_vietnamese_table(text)

            for key, meanings in found.items():
                reference.setdefault(key, [])
                for meaning in meanings:
                    if meaning not in reference[key]:
                        reference[key].append(meaning)

            print(f"Reference loaded: {url}")
            print(f"  Candidate mappings found: {len(found)}")
        except Exception as exc:
            print(f"Reference unavailable: {url}")
            print(f"  Reason: {exc}")

    resolved = 0
    unresolved = []

    output = []

    for record in records:
        word = norm_word(record.get("word", ""))
        pinyin = norm_pinyin(record.get("pinyin", ""))
        key = (word, pinyin)

        meanings = reference.get(key, [])

        item = dict(record)

        if meanings:
            item["candidateMeanings"] = meanings
            item["generationStatus"] = "generated_reference_assisted_unverified"
            item["generationSource"] = "vietnamese_hsk30_reference"
            resolved += 1
        else:
            item["candidateMeanings"] = []
            item["generationStatus"] = "needs_manual_verification"
            item["generationSource"] = "no_vietnamese_reference_match"
            unresolved.append(record.get("id"))

        output.append(item)

    OUTPUT.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print("SUCCESS")
    print(f"Candidate records:          {len(output)}/{EXPECTED}")
    print(f"Resolved from references:   {resolved}/{EXPECTED}")
    print(f"Needs manual verification:  {len(unresolved)}")
    print(f"Output:                     {OUTPUT}")
    print()
    print("IMPORTANT:")
    print("- Meanings are reference-assisted candidates, not ground truth.")
    print("- No automatic production approval was performed.")
    print("- Base/reviewed/production data was not modified.")

    if unresolved:
        print()
        print("First unresolved IDs:")
        print(", ".join(unresolved[:50]))
        if len(unresolved) > 50:
            print(f"... and {len(unresolved) - 50} more.")


if __name__ == "__main__":
    main()
