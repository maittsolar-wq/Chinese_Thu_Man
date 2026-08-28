#!/usr/bin/env python3
"""Merge the 797 AI-assisted HSK 5 meanings into the existing 1600 candidates.

Run from:
    D:\Chinese_Thu_Man

Expected files:
    data/hsk/hsk5/hsk5_meanings_candidates_input.json
    hsk5_ai_missing_meanings_candidates.json

The second file is the generated batch from this step.

Only currently-empty candidate records are filled. Existing 803 candidates
are preserved. No reviewed/production file is touched.
"""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk5"
MAIN = DATA / "hsk5_meanings_candidates_input.json"

# Put the generated JSON in D:\Chinese_Thu_Man\data\hsk\hsk5\
BATCH = DATA / "hsk5_ai_missing_meanings_candidates.json"

EXPECTED_MAIN = 1600
EXPECTED_BATCH = 797


def main():
    print("=" * 72)
    print("HSK 5 AI MEANING CANDIDATES — MERGE 797")
    print("=" * 72)
    print()

    if not MAIN.exists():
        raise SystemExit(f"Missing main candidates file: {MAIN}")
    if not BATCH.exists():
        raise SystemExit(f"Missing AI batch file: {BATCH}")

    main_records = json.loads(MAIN.read_text(encoding="utf-8"))
    batch_records = json.loads(BATCH.read_text(encoding="utf-8"))

    if len(main_records) != EXPECTED_MAIN:
        raise SystemExit(
            f"Expected main {EXPECTED_MAIN}, got {len(main_records)}"
        )
    if len(batch_records) != EXPECTED_BATCH:
        raise SystemExit(
            f"Expected batch {EXPECTED_BATCH}, got {len(batch_records)}"
        )

    by_id = {r["id"]: r for r in batch_records}

    before = 0
    filled = 0
    already_nonempty = 0

    for r in main_records:
        meanings = r.get("candidateMeanings", [])
        if isinstance(meanings, list) and any(
            isinstance(x, str) and x.strip() for x in meanings
        ):
            before += 1
            continue

        item = by_id.get(r["id"])
        if not item:
            continue

        meaning = item["meaningVi"].strip()
        r["candidateMeanings"] = [meaning]
        r["selectedMeaningVi"] = meaning
        r["meaningVi"] = meaning
        r["generationStatus"] = "ai_assisted_unverified"
        r["generationSource"] = (
            "ChatGPT_AI_assisted_candidate_generation"
        )
        r["verificationStatus"] = "unverified"
        r["humanVerified"] = False
        filled += 1

    after = sum(
        1 for r in main_records
        if isinstance(r.get("candidateMeanings"), list)
        and any(
            isinstance(x, str) and x.strip()
            for x in r["candidateMeanings"]
        )
    )

    MAIN.write_text(
        json.dumps(main_records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Main records:             {len(main_records)}/{EXPECTED_MAIN}")
    print(f"Existing candidates:      {before}/{EXPECTED_MAIN}")
    print(f"Filled from AI batch:     {filled}/{EXPECTED_BATCH}")
    print(f"Final candidate records:  {after}/{EXPECTED_MAIN}")
    print(f"Still missing:            {EXPECTED_MAIN - after}")
    print(f"Updated:                  {MAIN}")
    print()
    print("SUCCESS" if after == EXPECTED_MAIN else "INCOMPLETE")
    print("Existing candidates were preserved.")
    print("All newly filled meanings remain AI-assisted / unverified.")
    print("Reviewed and production data were not modified.")


if __name__ == "__main__":
    main()
