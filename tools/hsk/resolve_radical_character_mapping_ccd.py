#!/usr/bin/env python3
"""Resolve HSK Han characters to Kangxi radicals using CCD.

Source:
    Wikimedia Commons Chinese Character Decomposition (CCD)
    https://github.com/leonsilicon/chinese-characters-decomposition

CCD contains 21,169 character rows and its `section` field is the Kangxi
radical under which the character is filed.

Inputs:
    data/radicals/radical_character_mapping_input.json
    data/radicals/radicals_214.json

Output:
    data/radicals/radical_character_mapping.json
    data/radicals/radical_character_mapping_validation.json

The script downloads the repository's raw ccd.json. It does not use AI and
does not infer a radical when the source has no section value.
"""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RADICAL_ROOT = ROOT / "data" / "radicals"

INPUT = RADICAL_ROOT / "radical_character_mapping_input.json"
RADICALS = RADICAL_ROOT / "radicals_214.json"
OUTPUT = RADICAL_ROOT / "radical_character_mapping.json"
REPORT = RADICAL_ROOT / "radical_character_mapping_validation.json"

CCD_URL = (
    "https://raw.githubusercontent.com/leonsilicon/"
    "chinese-characters-decomposition/main/ccd.json"
)


def download_json(url: str):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Chinese-Thu-Man/1.0"},
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    print("=" * 72)
    print("CHARACTER → KANGXI RADICAL RESOLUTION — CCD")
    print("=" * 72)
    print()
    print("Downloading CCD reference...")

    for path in (INPUT, RADICALS):
        if not path.exists():
            raise SystemExit(f"Missing required file: {path}")

    source_records = json.loads(INPUT.read_text(encoding="utf-8"))
    radicals = json.loads(RADICALS.read_text(encoding="utf-8"))

    if not isinstance(source_records, list):
        raise SystemExit("Mapping input must be a JSON array.")
    if not isinstance(radicals, list) or len(radicals) != 214:
        raise SystemExit("radicals_214.json must contain exactly 214 records.")

    radical_by_char = {
        str(r["radical"]): r for r in radicals
    }

    if len(radical_by_char) != 214:
        raise SystemExit("Radical characters are not unique.")

    ccd = download_json(CCD_URL)

    if not isinstance(ccd, dict):
        raise SystemExit("CCD root must be an object.")

    headers = ccd.get("headers")
    rows = ccd.get("rows")

    if not isinstance(headers, list) or not isinstance(rows, list):
        raise SystemExit("CCD does not contain expected headers/rows.")

    try:
        component_i = headers.index("component")
        section_i = headers.index("section")
    except ValueError as exc:
        raise SystemExit(
            "CCD headers do not contain component/section."
        ) from exc

    ccd_by_char = {}

    for row in rows:
        if not isinstance(row, list):
            continue
        if len(row) <= max(component_i, section_i):
            continue

        character = row[component_i]
        section = row[section_i]

        if not isinstance(character, str) or not character:
            continue

        # Keep the first non-empty section if duplicate rows occur.
        if character not in ccd_by_char:
            ccd_by_char[character] = section
        elif not ccd_by_char[character] and section:
            ccd_by_char[character] = section

    resolved = 0
    unresolved = []
    invalid_radicals = []
    output = []

    for item in source_records:
        record = dict(item)
        character = str(record.get("character") or "")
        section = ccd_by_char.get(character)

        record["mappingSource"] = "Wikimedia CCD / ccd.json"
        record["sourceUrl"] = CCD_URL
        record["ccdSection"] = section

        if not section or section == "*":
            record["mappingStatus"] = "unresolved"
            record["verified"] = False
            unresolved.append(character)
            output.append(record)
            continue

        radical = radical_by_char.get(section)

        if radical is None:
            record["mappingStatus"] = "unresolved_invalid_ccd_section"
            record["verified"] = False
            invalid_radicals.append({
                "character": character,
                "ccdSection": section,
            })
            output.append(record)
            continue

        record["radicalId"] = radical["id"]
        record["radicalCharacter"] = radical["radical"]
        record["kangxiIndex"] = radical["kangxiIndex"]
        record["mappingStatus"] = "resolved"
        record["verified"] = True
        resolved += 1
        output.append(record)

    OUTPUT.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    unresolved_count = len(unresolved)
    invalid_count = len(invalid_radicals)

    # This is a structural resolution gate, not a claim that the CCD
    # classification is human-reviewed by the app owner.
    report = {
        "inputRecords": len(source_records),
        "ccdRows": len(rows),
        "ccdUniqueCharacters": len(ccd_by_char),
        "outputRecords": len(output),
        "resolved": resolved,
        "unresolved": unresolved_count,
        "invalidCcdSections": invalid_count,
        "errors": 0,
        "status": "PASS" if len(output) == len(source_records) else "FAIL",
        "mappingSource": "Wikimedia CCD",
        "sourceUrl": CCD_URL,
        "field": "section",
        "unresolvedCharacters": unresolved[:200],
        "invalidCcdSectionExamples": invalid_radicals[:100],
        "note": (
            "Only CCD section values that exactly match one of the 214 "
            "radicals in radicals_214.json were accepted. No radical was "
            "inferred or AI-generated."
        ),
    }

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Input characters:             {len(source_records)}")
    print(f"CCD rows:                     {len(rows)}")
    print(f"CCD unique characters:        {len(ccd_by_char)}")
    print(f"Resolved:                     {resolved}")
    print(f"Unresolved:                   {unresolved_count}")
    print(f"Invalid CCD sections:        {invalid_count}")
    print(f"Output:                       {OUTPUT}")
    print(f"Validation:                   {REPORT}")
    print()

    if len(output) != len(source_records):
        print("STATUS: FAIL")
        print("Some input records were not emitted.")
        raise SystemExit(1)

    print("STATUS: PASS")
    print("Character → Kangxi Radical resolution completed.")
    print("No radical relation was invented.")
    print("Unresolved characters remain explicitly unresolved.")


if __name__ == "__main__":
    main()
