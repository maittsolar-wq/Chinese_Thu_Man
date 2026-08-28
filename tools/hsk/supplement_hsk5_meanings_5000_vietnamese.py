#!/usr/bin/env python3
"""Supplement HSK 5 Vietnamese candidates from a 5000-word Chinese-Vietnamese source.

Source:
https://www.scribd.com/document/866911695/5000-TU-VUNG-HSK-CO-VD

The indexed source contains Chinese, pinyin, Vietnamese meaning and examples.
This script preserves the existing 803 candidates and adds only source-derived
Vietnamese meanings matched by Chinese word + normalized pinyin.

No base/reviewed/production data is modified.
"""

from __future__ import annotations

import json
import re
import unicodedata
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk5"
INPUT = DATA / "hsk5_meanings_candidates_input.json"

URL = "https://www.scribd.com/document/866911695/5000-TU-VUNG-HSK-CO-VD"
EXPECTED = 1600


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "vi,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def clean_html(value: str) -> str:
    value = re.sub(r"(?is)<script.*?</script>", "\n", value)
    value = re.sub(r"(?is)<style.*?</style>", "\n", value)
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    value = unescape(value)
    return value


def norm_word(value: str) -> str:
    return re.sub(r"\s+", "", value.strip())


def norm_pinyin(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[0-9]", "", value)
    value = value.replace("’", "").replace("'", "")
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        c for c in value
        if unicodedata.category(c) != "Mn"
    )
    value = value.replace("ü", "v")
    return re.sub(r"[^a-zv]", "", value)


def parse_source(text: str):
    result = {}

    # Format in the indexed document:
    # Chinese / pinyin / Vietnamese meaning / example.
    #
    # We use the Chinese token as the strongest boundary and take the
    # immediately adjacent pinyin + Vietnamese text.
    pattern = re.compile(
        r"(?:^|\n)\s*"
        r"(?:\d+\s+)?"
        r"(?P<word>[\u3400-\u9fff]{1,12})"
        r"\s+"
        r"(?P<pinyin>"
        r"[A-Za-zĀ-žā-ž'’üÜ·\s]+?"
        r")"
        r"\s+"
        r"(?P<meaning>"
        r"[À-ỹĐđ][^\n]{1,180}?"
        r")"
        r"(?=\n|$)",
        flags=re.I,
    )

    for m in pattern.finditer(text):
        word = norm_word(m.group("word"))
        py = norm_pinyin(m.group("pinyin"))
        meaning = re.sub(
            r"\s+",
            " ",
            m.group("meaning"),
        ).strip()

        if not word or not py or not meaning:
            continue

        # Reject example sentences / metadata.
        if len(meaning) > 160:
            continue

        if not re.search(r"[À-ỹĐđ]", meaning):
            continue

        # Remove common source artifacts.
        meaning = re.sub(
            r"\s+(?:他|她|我们|他们|请|这个|这次|我|你|我们需要|"
            r"Anh ấy|Cô ấy|Chúng tôi|Chúng ta)\b.*$",
            "",
            meaning,
            flags=re.I,
        ).strip(" ;,.")

        if not meaning:
            continue

        key = (word, py)
        result.setdefault(key, [])

        if meaning not in result[key]:
            result[key].append(meaning)

    return result


def main():
    print("=" * 72)
    print("HSK 5 VIETNAMESE CANDIDATES — 5000 WORD SOURCE")
    print("=" * 72)
    print()

    if not INPUT.exists():
        raise SystemExit(f"Missing input: {INPUT}")

    records = json.loads(
        INPUT.read_text(encoding="utf-8")
    )

    if not isinstance(records, list) or len(records) != EXPECTED:
        raise SystemExit(
            f"Expected {EXPECTED} records, got {len(records)}."
        )

    print("Downloading source...")
    raw = fetch(URL)
    text = clean_html(raw)

    reference = parse_source(text)

    print(f"Candidate records:       {len(records)}/{EXPECTED}")
    print(f"Reference mappings:      {len(reference)}")

    before = 0
    newly = 0
    resolved = 0
    unresolved = []

    for record in records:
        existing = record.get("candidateMeanings", [])

        if not isinstance(existing, list):
            existing = []

        existing = [
            x.strip()
            for x in existing
            if isinstance(x, str) and x.strip()
        ]

        if existing:
            before += 1

        key = (
            norm_word(record.get("word", "")),
            norm_pinyin(record.get("pinyin", "")),
        )

        merged = list(existing)
        seen = {x.casefold() for x in merged}

        for meaning in reference.get(key, []):
            if meaning.casefold() not in seen:
                merged.append(meaning)
                seen.add(meaning.casefold())

        if not existing and merged:
            newly += 1

        record["candidateMeanings"] = merged

        if merged:
            record["generationStatus"] = (
                "generated_reference_assisted_unverified"
            )
            record["generationSource"] = (
                "5000_vietnamese_hsk_reference"
            )
            resolved += 1
        else:
            record["generationStatus"] = (
                "needs_manual_verification"
            )
            record["generationSource"] = (
                "no_vietnamese_reference_match"
            )
            unresolved.append(record["id"])

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
    print(f"Previously resolved:     {before}/{EXPECTED}")
    print(f"Newly resolved:          {newly}")
    print(f"Total resolved:          {resolved}/{EXPECTED}")
    print(f"Still unresolved:        {len(unresolved)}")
    print(f"Output:                  {INPUT}")
    print()
    print("Existing candidates were preserved.")
    print("Only source-derived Vietnamese meanings were added.")
    print("No meaning was invented.")
    print("Base/reviewed/production data was not modified.")

    if unresolved:
        print()
        print("First unresolved IDs:")
        print(", ".join(unresolved[:50]))
        if len(unresolved) > 50:
            print(
                f"... and {len(unresolved) - 50} more."
            )


if __name__ == "__main__":
    main()
