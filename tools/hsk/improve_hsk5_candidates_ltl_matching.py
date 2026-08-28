#!/usr/bin/env python3

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

URL = "https://hsk-exam.com/vn/blog/hsk-5-vocabulary-list"
EXPECTED = 1600


def fetch(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "vi,en;q=0.9",
        },
    )

    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read().decode(
            "utf-8",
            errors="replace",
        )


def strip_html(value: str) -> str:
    value = re.sub(
        r"(?is)<script.*?</script>",
        " ",
        value,
    )

    value = re.sub(
        r"(?is)<style.*?</style>",
        " ",
        value,
    )

    value = re.sub(
        r"<br\s*/?>",
        "\n",
        value,
        flags=re.I,
    )

    value = re.sub(
        r"<[^>]+>",
        " ",
        value,
    )

    return re.sub(
        r"\s+",
        " ",
        unescape(value),
    ).strip()


def norm_word(value: str) -> str:
    return re.sub(
        r"\s+",
        "",
        value.strip(),
    )


def norm_pinyin(value: str) -> str:
    """
    Normalize Pinyin without str.maketrans().

    Examples:
        ānwèi
        anwei
        an1wei4

    -> anwei
    """

    value = value.strip().lower()

    value = value.replace("’", "")
    value = value.replace("'", "")

    # Remove numeric tone marks.
    value = re.sub(
        r"[0-9]",
        "",
        value,
    )

    # Separate Unicode tone marks from letters.
    value = unicodedata.normalize(
        "NFD",
        value,
    )

    # Remove combining marks.
    value = "".join(
        char
        for char in value
        if unicodedata.category(char) != "Mn"
    )

    # ü -> v for matching.
    value = value.replace(
        "ü",
        "v",
    )

    # Keep only matching characters.
    value = re.sub(
        r"[^a-zv]",
        "",
        value,
    )

    return value


def parse_reference(text: str):
    reference = {}

    pattern = re.compile(
        r"(?P<word>[\u3400-\u9fff]{1,12})\s+"
        r"(?P<pinyin>"
        r"[A-Za-zĀ-žā-ž'’·\s0-9]+?"
        r")\s+"
        r"(?P<meaning>"
        r"[À-ỹĐđ][^\n]{1,400}?"
        r")"
        r"(?=\s+[\u3400-\u9fff]{1,12}\s+|$)",
        flags=re.I,
    )

    for match in pattern.finditer(text):

        word = norm_word(
            match.group("word")
        )

        pinyin = norm_pinyin(
            match.group("pinyin")
        )

        meaning = re.sub(
            r"\s+",
            " ",
            match.group("meaning"),
        ).strip()

        if not word:
            continue

        if not pinyin:
            continue

        if not meaning:
            continue

        meaning = re.split(
            r"\s+(?:Ví dụ|Đừng lẫn|Cùng âm|Lưu ý)\b",
            meaning,
            maxsplit=1,
            flags=re.I,
        )[0].strip()

        if not meaning:
            continue

        key = (
            word,
            pinyin,
        )

        reference.setdefault(
            key,
            [],
        )

        if meaning not in reference[key]:
            reference[key].append(
                meaning
            )

    return reference


def main():

    print("=" * 72)
    print("HSK 5 CANDIDATE MATCHING — IMPROVED LTL")
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
            "Input must be a JSON array."
        )

    if len(records) != EXPECTED:
        raise SystemExit(
            f"Expected {EXPECTED} records, "
            f"got {len(records)}."
        )

    print(
        "Downloading Vietnamese reference..."
    )

    source = strip_html(
        fetch(URL)
    )

    reference = parse_reference(
        source
    )

    print(
        f"Candidate records:       "
        f"{len(records)}/{EXPECTED}"
    )

    print(
        f"Reference mappings:      "
        f"{len(reference)}"
    )

    before = 0
    newly = 0
    resolved = 0
    unresolved = []

    for record in records:

        existing = record.get(
            "candidateMeanings",
            [],
        )

        if not isinstance(
            existing,
            list,
        ):
            existing = []

        existing = [
            value.strip()
            for value in existing
            if isinstance(
                value,
                str,
            )
            and value.strip()
        ]

        if existing:
            before += 1

        key = (
            norm_word(
                record.get(
                    "word",
                    "",
                )
            ),
            norm_pinyin(
                record.get(
                    "pinyin",
                    "",
                )
            ),
        )

        merged = list(
            existing
        )

        seen = {
            value.casefold()
            for value in merged
        }

        for meaning in reference.get(
            key,
            [],
        ):

            normalized = (
                meaning.casefold()
            )

            if normalized not in seen:

                merged.append(
                    meaning
                )

                seen.add(
                    normalized
                )

        if (
            not existing
            and merged
        ):
            newly += 1

        record[
            "candidateMeanings"
        ] = merged

        if merged:

            record[
                "generationStatus"
            ] = (
                "generated_reference_assisted_unverified"
            )

            record[
                "generationSource"
            ] = (
                "ltl_vietnamese_reference_tone_normalized"
            )

            resolved += 1

        else:

            record[
                "generationStatus"
            ] = (
                "needs_manual_verification"
            )

            record[
                "generationSource"
            ] = (
                "no_vietnamese_reference_match"
            )

            unresolved.append(
                record["id"]
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
        f"Previously resolved:     "
        f"{before}/{EXPECTED}"
    )

    print(
        f"Newly resolved:          "
        f"{newly}"
    )

    print(
        f"Total resolved:          "
        f"{resolved}/{EXPECTED}"
    )

    print(
        f"Still unresolved:        "
        f"{len(unresolved)}"
    )

    print(
        f"Output:                  "
        f"{INPUT}"
    )

    print()
    print(
        "Existing candidates were preserved."
    )

    print(
        "No meaning was invented."
    )

    print(
        "Base/reviewed/production data "
        "was not modified."
    )

    if unresolved:

        print()
        print(
            "First unresolved IDs:"
        )

        print(
            ", ".join(
                unresolved[:50]
            )
        )

        if len(unresolved) > 50:
            print(
                f"... and "
                f"{len(unresolved) - 50} more."
            )


if __name__ == "__main__":
    main()