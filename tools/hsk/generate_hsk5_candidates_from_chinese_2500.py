#!/usr/bin/env python3
"""Supplement HSK 5 Vietnamese candidates from a public 2500-word HSK 5 table.

Reference:
https://chinese.edu.vn/tu-vung-hsk-5.html

The page exposes a large table with:
STT | Chinese | Pinyin | Vietnamese meaning.

This script keeps the existing candidate meanings and fills only records
that match by Chinese + normalized Pinyin.

It does NOT modify base/reviewed/production data.
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

URL = "https://chinese.edu.vn/tu-vung-hsk-5.html"
EXPECTED = 1600


def fetch(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "vi,en;q=0.9",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def strip_html(value: str) -> str:
    value = re.sub(r"(?is)<script.*?</script>", "\n", value)
    value = re.sub(r"(?is)<style.*?</style>", "\n", value)
    value = re.sub(r"<br\s*/?>", " | ", value, flags=re.I)
    value = re.sub(r"</(?:p|div|li|tr|td|th)>", "\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def norm_word(value: str) -> str:
    return re.sub(r"\s+", "", str(value or "").strip())


def norm_pinyin(value: str) -> str:
    value = str(value or "").strip().lower()
    value = value.replace("’", "").replace("'", "")
    value = re.sub(r"[0-9]", "", value)
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        ch for ch in value
        if unicodedata.category(ch) != "Mn"
    )
    value = value.replace("ü", "v")
    return re.sub(r"[^a-zv]", "", value)


def clean_meaning(value: str) -> str:
    value = re.sub(r"\s+", " ", str(value or "")).strip()
    value = re.sub(
        r"\s*\([^)]*\)\s*$",
        "",
        value,
    ).strip()
    return value.strip(" |;；")


def parse_table(html: str):
    reference = {}
    rows = re.findall(
        r"(?is)<tr\b[^>]*>(.*?)</tr>",
        html,
    )

    parsed_rows = 0

    for row in rows:
        cells = re.findall(
            r"(?is)<t[dh]\b[^>]*>(.*?)</t[dh]>",
            row,
        )

        values = []
        for cell in cells:
            value = re.sub(
                r"<br\s*/?>",
                " ",
                cell,
                flags=re.I,
            )
            value = re.sub(
                r"<[^>]+>",
                " ",
                value,
            )
            value = unescape(value)
            value = re.sub(r"\s+", " ", value).strip()
            values.append(value)

        if len(values) < 4:
            continue

        # Locate Chinese / pinyin / Vietnamese columns without relying
        # on an exact fixed column count.
        word_i = next(
            (
                i for i, value in enumerate(values)
                if re.search(r"[\u3400-\u9fff]", value)
                and len(value) <= 20
            ),
            None,
        )

        if word_i is None:
            continue

        py_i = None
        for i, value in enumerate(values):
            if i == word_i:
                continue
            if re.fullmatch(
                r"[A-Za-zĀ-žā-ž'’üÜ·\s0-9…]+",
                value,
            ) and 1 <= len(value) <= 60:
                py_i = i
                break

        if py_i is None:
            continue

        meaning_i = None
        for i, value in enumerate(values):
            if i in {word_i, py_i}:
                continue
            if re.search(r"[À-ỹĐđ]", value):
                meaning_i = i
                break

        if meaning_i is None:
            continue

        word = norm_word(values[word_i])
        pinyin = norm_pinyin(values[py_i])
        meaning = clean_meaning(values[meaning_i])

        if not word or not pinyin or not meaning:
            continue

        # Avoid headers and long example sentences.
        if word in {"Chữ Hán", "Từ vựng", "STT"}:
            continue
        if len(meaning) > 250:
            continue

        key = (word, pinyin)
        reference.setdefault(key, [])

        if meaning not in reference[key]:
            reference[key].append(meaning)

        parsed_rows += 1

    return reference, parsed_rows


def main():
    print("=" * 72)
    print("HSK 5 VIETNAMESE CANDIDATES — 2500 WORD REFERENCE")
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

    print("Downloading reference...")
    html = fetch(URL)

    reference, parsed_rows = parse_table(html)

    print(f"Candidate records:       {len(records)}/{EXPECTED}")
    print(f"Reference rows parsed:   {parsed_rows}")
    print(f"Reference mappings:      {len(reference)}")

    before = 0
    newly = 0
    resolved = 0
    unresolved = []

    for record in records:
        existing = record.get(
            "candidateMeanings",
            [],
        )

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
                "chinese_edu_vietnamese_hsk5_reference"
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
