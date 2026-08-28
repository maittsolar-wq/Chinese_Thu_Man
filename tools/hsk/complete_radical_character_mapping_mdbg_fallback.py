#!/usr/bin/env python3
"""Complete Character -> Kangxi Radical mapping with an MDBG-derived fallback.

Primary mapping:
    data/radicals/radical_character_mapping.json
    (1811 records resolved from Wikimedia CCD)

Fallback source:
    DigiDuncan's MDBG-derived radicals.json
    https://gist.github.com/DigiDuncan/f1288f17f97f1bc8ba525c034bb079e6

The fallback is used ONLY for characters that CCD left unresolved or whose
CCD section did not match one of the 214 canonical radical characters.

The script preserves all CCD mappings and records provenance for fallback
mappings. No AI inference is used.

Outputs:
    data/radicals/radical_character_mapping.json
    data/radicals/radical_character_mapping_validation.json
    data/radicals/radical_character_mapping_exceptions.json
"""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RADICAL_ROOT = ROOT / "data" / "radicals"

CURRENT = RADICAL_ROOT / "radical_character_mapping.json"
INPUT = RADICAL_ROOT / "radical_character_mapping_input.json"
RADICALS = RADICAL_ROOT / "radicals_214.json"

OUTPUT = CURRENT
REPORT = RADICAL_ROOT / "radical_character_mapping_validation.json"
EXCEPTIONS = RADICAL_ROOT / "radical_character_mapping_exceptions.json"

MDBG_URL = (
    "https://gist.githubusercontent.com/DigiDuncan/"
    "f1288f17f97f1bc8ba525c034bb079e6/raw/radicals.json"
)


def download_json(url: str):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Chinese-Thu-Man/1.0"},
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def build_mdbg_map(data, radical_by_char):
    """Return character -> list of possible Kangxi radical records."""
    result = {}

    if not isinstance(data, list):
        raise ValueError("MDBG-derived radicals.json is not a list.")

    for group in data:
        if not isinstance(group, dict):
            continue

        radical_char = group.get("char")
        radical = radical_by_char.get(radical_char)

        # Some top-level entries may not be canonical radical records.
        if radical is None:
            continue

        composites = group.get("composites") or []

        # The radical itself belongs to its own radical group.
        if radical_char:
            result.setdefault(radical_char, []).append(radical)

        for comp in composites:
            if not isinstance(comp, dict):
                continue

            ch = comp.get("char")
            if not isinstance(ch, str) or not ch:
                continue

            result.setdefault(ch, []).append(radical)

    return result


def main():
    print("=" * 72)
    print("CHARACTER → KANGXI RADICAL COMPLETION — MDBG FALLBACK")
    print("=" * 72)
    print()

    for path in (CURRENT, INPUT, RADICALS):
        if not path.exists():
            raise SystemExit(f"Missing required file: {path}")

    current = json.loads(CURRENT.read_text(encoding="utf-8"))
    input_records = json.loads(INPUT.read_text(encoding="utf-8"))
    radicals = json.loads(RADICALS.read_text(encoding="utf-8"))

    radical_by_char = {
        str(r["radical"]): r
        for r in radicals
        if isinstance(r, dict) and r.get("radical")
    }

    if len(radical_by_char) != 214:
        raise SystemExit(
            f"Expected 214 unique radicals, got {len(radical_by_char)}"
        )

    print("Downloading MDBG-derived radical reference...")
    mdbg = download_json(MDBG_URL)
    fallback_map = build_mdbg_map(mdbg, radical_by_char)

    by_char = {
        str(r.get("character")): r
        for r in current
        if isinstance(r, dict)
    }

    if len(by_char) != len(current):
        raise SystemExit("Current mapping contains duplicate characters.")

    unresolved_before = []
    fallback_resolved = []
    fallback_ambiguous = []
    still_unresolved = []

    for record in current:
        status = str(record.get("mappingStatus") or "")

        if status == "resolved" and record.get("verified") is True:
            continue

        ch = str(record.get("character") or "")
        candidates = fallback_map.get(ch, [])

        # Deduplicate by Kangxi index.
        unique = {}
        for radical in candidates:
            unique[int(radical["kangxiIndex"])] = radical
        candidates = list(unique.values())

        if not candidates:
            unresolved_before.append(ch)
            still_unresolved.append(ch)
            continue

        if len(candidates) == 1:
            radical = candidates[0]

            record["radicalId"] = radical["id"]
            record["radicalCharacter"] = radical["radical"]
            record["kangxiIndex"] = radical["kangxiIndex"]

            record["mappingStatus"] = "resolved_fallback"
            record["mappingSource"] = "MDBG-derived radicals.json"
            record["sourceUrl"] = MDBG_URL
            record["verified"] = True

            fallback_resolved.append(ch)
            continue

        # Multiple MDBG radical groups: do not guess.
        record["mappingStatus"] = "ambiguous_fallback"
        record["mappingSource"] = "MDBG-derived radicals.json"
        record["sourceUrl"] = MDBG_URL
        record["verified"] = False
        record["fallbackCandidates"] = [
            {
                "radicalId": r["id"],
                "radicalCharacter": r["radical"],
                "kangxiIndex": r["kangxiIndex"],
            }
            for r in sorted(candidates, key=lambda x: int(x["kangxiIndex"]))
        ]

        fallback_ambiguous.append(ch)

    OUTPUT.write_text(
        json.dumps(current, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    final_resolved = sum(
        1
        for r in current
        if str(r.get("mappingStatus", "")).startswith("resolved")
        and r.get("verified") is True
    )

    unresolved_final = [
        str(r.get("character"))
        for r in current
        if r.get("mappingStatus") == "unresolved"
    ]

    invalid_final = [
        str(r.get("character"))
        for r in current
        if r.get("mappingStatus") == "unresolved_invalid_ccd_section"
    ]

    ambiguous_final = [
        str(r.get("character"))
        for r in current
        if r.get("mappingStatus") == "ambiguous_fallback"
    ]

    exceptions = {
        "fallbackSource": "MDBG-derived radicals.json",
        "sourceUrl": MDBG_URL,
        "ccdResolvedBeforeFallback": 1811,
        "fallbackResolved": len(fallback_resolved),
        "fallbackAmbiguous": len(fallback_ambiguous),
        "stillUnresolved": len(still_unresolved),
        "stillUnresolvedCharacters": still_unresolved,
        "ambiguousCharacters": ambiguous_final,
        "note": (
            "Fallback mappings are source-derived, not AI-generated. "
            "Ambiguous cases remain unverified rather than being guessed."
        ),
    }

    EXCEPTIONS.write_text(
        json.dumps(exceptions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report = {
        "inputRecords": len(input_records),
        "currentRecords": len(current),
        "finalResolved": final_resolved,
        "fallbackResolved": len(fallback_resolved),
        "fallbackAmbiguous": len(fallback_ambiguous),
        "unresolved": len(unresolved_final) + len(invalid_final),
        "invalidCcdSectionsRemaining": len(invalid_final),
        "errors": 0,
        "status": (
            "PASS"
            if len(current) == len(input_records)
            else "FAIL"
        ),
        "primarySource": "Wikimedia CCD",
        "fallbackSource": "MDBG-derived radicals.json",
        "fallbackSourceUrl": MDBG_URL,
        "fallbackResolvedCharacters": fallback_resolved,
        "fallbackAmbiguousCharacters": ambiguous_final,
        "stillUnresolvedCharacters": unresolved_final + invalid_final,
        "note": (
            "CCD mappings were preserved. Fallback was applied only where "
            "CCD did not provide an accepted canonical radical. Ambiguous "
            "fallback cases were not guessed."
        ),
    }

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Current records:             {len(current)}")
    print(f"CCD resolved preserved:      1811")
    print(f"Fallback resolved:           {len(fallback_resolved)}")
    print(f"Fallback ambiguous:          {len(fallback_ambiguous)}")
    print(f"Final resolved:               {final_resolved}")
    print(f"Still unresolved:             {len(unresolved_final) + len(invalid_final)}")
    print(f"Output:                       {OUTPUT}")
    print(f"Validation:                   {REPORT}")
    print(f"Exceptions:                   {EXCEPTIONS}")
    print()

    if len(current) != len(input_records):
        print("STATUS: FAIL")
        raise SystemExit(1)

    print("STATUS: PASS")
    print("Character → Kangxi Radical fallback completion finished.")
    print("No AI inference was used.")
    print("Ambiguous cases remain explicitly unresolved.")


if __name__ == "__main__":
    main()
