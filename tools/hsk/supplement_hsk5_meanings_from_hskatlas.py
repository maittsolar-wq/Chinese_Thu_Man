#!/usr/bin/env python3
"""Supplement HSK 5 Vietnamese meaning candidates from HSK Atlas.

The current HSK 5 candidate package may have unresolved records because
the earlier references contain only subsets of HSK 5 3.0.

HSK Atlas publishes the HSK 3.0 Level 5 vocabulary list with:
Chinese word + pinyin + Vietnamese meaning.

Input:
    data/hsk/hsk5/hsk5_meanings_candidates_input.json

Output:
    same file, with additional candidateMeanings where matched.

This script:
- preserves existing candidates;
- only adds meanings from the HSK Atlas reference;
- never invents a meaning;
- leaves genuinely unmatched records unresolved;
- does not modify base/reviewed/production data.
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

URL = "https://hskatlas.com/vi/hsk3.0-level5/vocabulary/"
EXPECTED = 1600


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "vi,en;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read().decode(
            "utf-8",
            errors="replace",
        )


def clean_html(html: str) -> str:
    html = re.sub(
        r"(?is)<script.*?</script>",
        " ",
        html,
    )
    html = re.sub(
        r"(?is)<style.*?</style>",
        " ",
        html,
    )
    html = re.sub(
        r"(?is)<!--.*?-->",
        " ",
        html,
    )
    html = re.sub(
        r"<br\s*/?>",
        "\n",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"</(?:p|div|li|tr|td|th|h[1-6])>",
        "\n",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"<[^>]+>",
        " ",
        html,
    )
    return unescape(html)


def norm_word(value: str) -> str:
    return re.sub(r"\s+", "", value.strip())


def norm_pinyin(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("’", "'")
    value = re.sub(r"\s+", "", value)
    return value


def is_chinese(value: str) -> bool:
    return bool(
        re.search(r"[\u3400-\u9fff]", value)
    )


def looks_vietnamese(value: str) -> bool:
    # Vietnamese diacritics + common Vietnamese letters.
    return bool(
        re.search(
            r"[À-ỹĐđ]",
            value,
        )
    )


def extract_rows(html: str):
    """Extract likely Chinese/pinyin/Vietnamese triples.

    HSK Atlas may render the vocabulary as HTML or embedded JSON.
    We deliberately use conservative patterns and never synthesize text.
    """
    result = {}

    # First, inspect table rows with 3+ cells.
    rows = re.findall(
        r"(?is)<tr\b[^>]*>(.*?)</tr>",
        html,
    )

    for row in rows:
        cells = re.findall(
            r"(?is)<t[dh]\b[^>]*>(.*?)</t[dh]>",
            row,
        )

        values = []
        for cell in cells:
            cell = re.sub(r"<[^>]+>", " ", cell)
            cell = unescape(cell)
            cell = re.sub(r"\s+", " ", cell).strip()
            values.append(cell)

        if len(values) < 3:
            continue

        # Find Chinese, pinyin and Vietnamese cells without assuming
        # a fixed column order.
        word = next(
            (x for x in values if is_chinese(x) and len(x) <= 20),
            None,
        )

        if not word:
            continue

        pinyin = next(
            (
                x for x in values
                if re.fullmatch(
                    r"[A-Za-zĀ-žā-ž'·\s0-9]+",
                    x,
                )
                and len(x) <= 60
                and not is_chinese(x)
            ),
            None,
        )

        if not pinyin:
            continue

        meaning = next(
            (
                x for x in values
                if x not in {word, pinyin}
                and looks_vietnamese(x)
                and len(x) <= 500
            ),
            None,
        )

        if not meaning:
            continue

        key = (
            norm_word(word),
            norm_pinyin(pinyin),
        )

        result.setdefault(key, [])

        if meaning not in result[key]:
            result[key].append(meaning)

    # Fallback: scan visible text lines.
    text = clean_html(html)

    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()

        if not line:
            continue

        # Chinese + pinyin + Vietnamese.
        match = re.search(
            r"(?P<word>[\u3400-\u9fff]{1,12})\s+"
            r"(?P<pinyin>[A-Za-zĀ-žā-ž'·\s]+?)\s+"
            r"(?P<meaning>[A-Za-zÀ-ỹĐđ0-9 ,;:/()'\".-]{2,300})$",
            line,
        )

        if not match:
            continue

        word = norm_word(match.group("word"))
        pinyin = norm_pinyin(match.group("pinyin"))
        meaning = re.sub(
            r"\s+",
            " ",
            match.group("meaning"),
        ).strip()

        if not looks_vietnamese(meaning):
            continue

        key = (word, pinyin)
        result.setdefault(key, [])

        if meaning not in result[key]:
            result[key].append(meaning)

    return result


def main():
    print("=" * 72)
    print("HSK 5 MEANING CANDIDATES — HSK ATLAS SUPPLEMENT")
    print("=" * 72)
    print()

    if not INPUT.exists():
        raise SystemExit(f"Missing input: {INPUT}")

    records = json.loads(
        INPUT.read_text(encoding="utf-8")
    )

    if not isinstance(records, list):
        raise SystemExit("Input must be a JSON array.")

    if len(records) != EXPECTED:
        raise SystemExit(
            f"Expected {EXPECTED} records, got {len(records)}."
        )

    print(f"Candidate records: {len(records)}/{EXPECTED}")
    print(f"Reference: {URL}")
    print()

    try:
        html = fetch(URL)
    except Exception as exc:
        raise SystemExit(
            "Could not fetch HSK Atlas.\n"
            f"Error: {exc}"
        )

    reference = extract_rows(html)

    print(
        f"Reference mappings extracted: {len(reference)}"
    )

    before = sum(
        bool(
            isinstance(r.get("candidateMeanings"), list)
            and r.get("candidateMeanings")
        )
        for r in records
    )

    added = 0
    unresolved = []

    for record in records:
        key = (
            norm_word(record.get("word", "")),
            norm_pinyin(record.get("pinyin", "")),
        )

        meanings = reference.get(key, [])

        existing = record.get(
            "candidateMeanings",
            [],
        )

        if not isinstance(existing, list):
            existing = []

        merged = []
        seen = set()

        for value in existing + meanings:
            if not isinstance(value, str):
                continue

            value = value.strip()

            if not value:
                continue

            k = value.casefold()

            if k not in seen:
                seen.add(k)
                merged.append(value)

        if len(merged) > len(existing):
            added += 1

        record["candidateMeanings"] = merged

        if merged:
            record["generationStatus"] = (
                "generated_reference_assisted_unverified"
            )
            record["generationSource"] = (
                "vietnamese_hsk30_reference"
            )
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

    resolved = EXPECTED - len(unresolved)

    print()
    print("SUCCESS")
    print(
        f"Resolved candidate records:   "
        f"{resolved}/{EXPECTED}"
    )
    print(
        f"Newly resolved by supplement: "
        f"{added}"
    )
    print(
        f"Still unresolved:             "
        f"{len(unresolved)}"
    )
    print(f"Output:                       {INPUT}")
    print()
    print("IMPORTANT:")
    print("- Existing candidates were preserved.")
    print("- Only reference-derived meanings were added.")
    print("- No meaning was invented.")
    print("- Base/reviewed/production data was not modified.")

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
