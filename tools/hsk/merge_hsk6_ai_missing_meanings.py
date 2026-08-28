#!/usr/bin/env python3
"""Merge HSK 6 AI-assisted missing meanings into the full candidates input."""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk6"
MAIN = DATA / "hsk6_meanings_candidates_input.json"
AI = DATA / "hsk6_ai_missing_meanings_candidates.json"
EXPECTED = 1800


def main():
    print("=" * 72)
    print("HSK 6 AI MEANING CANDIDATES — MERGE 1292")
    print("=" * 72)
    print()

    if not MAIN.exists():
        raise SystemExit(f"Missing main candidates: {MAIN}")
    if not AI.exists():
        raise SystemExit(f"Missing AI candidates: {AI}")

    main_records = json.loads(MAIN.read_text(encoding="utf-8"))
    ai_records = json.loads(AI.read_text(encoding="utf-8"))

    if len(main_records) != EXPECTED:
        raise SystemExit(
            f"Main candidates must contain {EXPECTED} records, got {len(main_records)}."
        )

    if not isinstance(ai_records, list) or not ai_records:
        raise SystemExit("AI candidates file is empty or invalid.")

    by_id = {str(r.get("id")): r for r in ai_records}
    updated = 0
    missing = []

    for r in main_records:
        rid = str(r.get("id"))
        # Only fill records that are currently missing a candidate meaning.
        if r.get("candidateMeanings"):
            continue

        ai = by_id.get(rid)
        if not ai:
            missing.append(rid)
            continue

        meaning = str(ai.get("meaningVi") or "").strip()
        candidates = ai.get("candidateMeanings")

        if not meaning:
            if isinstance(candidates, list):
                candidates = [str(x).strip() for x in candidates if str(x).strip()]
                meaning = candidates[0] if candidates else ""

        if not meaning:
            missing.append(rid)
            continue

        r["candidateMeanings"] = [meaning]
        r["selectedMeaningVi"] = meaning
        r["meaningVi"] = meaning
        r["generationSource"] = "AI-assisted"
        r["generationStatus"] = "ai_assisted"
        r["verificationStatus"] = "unverified"
        r["humanVerified"] = False
        r["groundTruth"] = False
        updated += 1

    MAIN.write_text(
        json.dumps(main_records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    resolved = sum(
        1 for r in main_records
        if isinstance(r.get("candidateMeanings"), list)
        and any(str(x).strip() for x in r["candidateMeanings"])
    )

    print(f"Main records:             {len(main_records)}/{EXPECTED}")
    print(f"Existing candidates:      {EXPECTED - updated}/{EXPECTED}")
    print(f"Filled from AI batch:     {updated}/{len(ai_records)}")
    print(f"Final candidate records:  {resolved}/{EXPECTED}")
    print(f"Still missing:            {len(missing)}")
    print(f"Updated:                  {MAIN}")
    print()

    if missing:
        print("STATUS: FAIL")
        print("Unresolved IDs:")
        print(", ".join(missing[:50]))
        if len(missing) > 50:
            print(f"... and {len(missing)-50} more")
        raise SystemExit(1)

    if resolved != EXPECTED:
        raise SystemExit(
            f"Merge did not produce {EXPECTED}/{EXPECTED} resolved candidates."
        )

    print("SUCCESS")
    print("All HSK 6 meaning candidates are present.")
    print("AI-assisted meanings remain explicitly unverified.")
    print("Reviewed and production data were not modified.")


if __name__ == "__main__":
    main()
