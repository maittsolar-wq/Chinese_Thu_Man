#!/usr/bin/env python3
"""Resolve the final four Character -> Kangxi Radical exceptions.

The four remaining HSK characters are:
    户, 房, 所, 扇

Authoritative dictionary/index evidence places all four under 戶/户部,
Kangxi radical no. 63:
    https://zh.wikipedia.org/wiki/戶部_(部首)

The script patches ONLY these four unresolved records and preserves all
previous CCD/MDBG mappings.

Inputs:
    data/radicals/radical_character_mapping.json
    data/radicals/radicals_214.json

Outputs:
    data/radicals/radical_character_mapping.json
    data/radicals/radical_character_mapping_validation.json
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RADICAL_ROOT = ROOT / "data" / "radicals"

MAPPING = RADICAL_ROOT / "radical_character_mapping.json"
RADICALS = RADICAL_ROOT / "radicals_214.json"
REPORT = RADICAL_ROOT / "radical_character_mapping_validation.json"

SOURCE = "Kangxi radical index / 戶部 (部首)"
SOURCE_URL = "https://zh.wikipedia.org/wiki/戶部_(部首)"

TARGETS = {"户", "房", "所", "扇"}


def main():
    print("=" * 72)
    print("FINAL CHARACTER → KANGXI RADICAL EXCEPTION RESOLUTION")
    print("=" * 72)
    print()

    for path in (MAPPING, RADICALS):
        if not path.exists():
            raise SystemExit(f"Missing required file: {path}")

    records = json.loads(MAPPING.read_text(encoding="utf-8"))
    radicals = json.loads(RADICALS.read_text(encoding="utf-8"))

    radical = next(
        (
            r for r in radicals
            if int(r.get("kangxiIndex", -1)) == 63
        ),
        None,
    )

    if radical is None:
        raise SystemExit("Kangxi radical index 63 was not found.")

    canonical_radical = radical["radical"]

    # The 214-radical dataset may store the simplified display form 户
    # while the traditional Kangxi index is traditionally written 戶.
    if canonical_radical not in {"户", "戶"}:
        raise SystemExit(
            f"Unexpected radical 63 character: {canonical_radical!r}"
        )

    found = set()
    changed = []

    for record in records:
        ch = record.get("character")

        if ch not in TARGETS:
            continue

        found.add(ch)

        # Only patch unresolved records. Never overwrite a prior resolved
        # source mapping.
        status = str(record.get("mappingStatus") or "")
        if status.startswith("resolved") and record.get("verified") is True:
            continue

        record["radicalId"] = radical["id"]
        record["radicalCharacter"] = canonical_radical
        record["kangxiIndex"] = 63
        record["mappingStatus"] = "resolved_fallback_dictionary"
        record["mappingSource"] = SOURCE
        record["sourceUrl"] = SOURCE_URL
        record["verified"] = True
        changed.append(ch)

    missing_targets = sorted(TARGETS - found)

    if missing_targets:
        raise SystemExit(
            "Expected exception characters not found in mapping: "
            + ", ".join(missing_targets)
        )

    MAPPING.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    unresolved = [
        r.get("character")
        for r in records
        if not (
            str(r.get("mappingStatus", "")).startswith("resolved")
            and r.get("verified") is True
        )
    ]

    invalid = [
        r.get("character")
        for r in records
        if r.get("mappingStatus") == "unresolved_invalid_ccd_section"
    ]

    report = {
        "records": len(records),
        "resolved": len(records) - len(unresolved),
        "unresolved": len(unresolved),
        "invalid": len(invalid),
        "finalExceptionCharacters": sorted(TARGETS),
        "finalExceptionResolved": sorted(changed),
        "radicalIndex": 63,
        "radicalCharacter": canonical_radical,
        "source": SOURCE,
        "sourceUrl": SOURCE_URL,
        "status": (
            "PASS"
            if len(records) == 1940 and not unresolved and not invalid
            else "FAIL"
        ),
        "note": (
            "The four remaining exceptions are explicitly documented as "
            "members of 戶部/户部, Kangxi radical 63. No AI inference was used."
        ),
    }

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Records:                     {len(records)}")
    print(f"Final exceptions patched:    {len(changed)}")
    print(f"Resolved:                    {len(records) - len(unresolved)}")
    print(f"Unresolved:                  {len(unresolved)}")
    print(f"Invalid:                     {len(invalid)}")
    print(f"Radical:                     {canonical_radical}")
    print(f"Kangxi index:                63")
    print(f"Output:                      {MAPPING}")
    print(f"Validation:                  {REPORT}")
    print()

    if len(records) != 1940 or unresolved or invalid:
        print("STATUS: FAIL")
        print("Final character → radical mapping is not complete.")
        raise SystemExit(1)

    print("STATUS: PASS")
    print("Character → Kangxi Radical mapping is complete: 1940/1940.")


if __name__ == "__main__":
    main()
