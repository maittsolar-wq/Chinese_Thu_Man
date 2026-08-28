#!/usr/bin/env python3
"""Fix the single unresolved HSK 4 meaning: hsk4_908.

This patches only data/hsk/hsk4/hsk4_vocabulary_reviewed.json.
All other records are preserved unchanged.

hsk4_908:
    月饼
    yuèbing
    bánh trung thu
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk4"
REVIEWED = DATA / "hsk4_vocabulary_reviewed.json"

TARGET_ID = "hsk4_908"
MEANING = ["bánh trung thu"]


def main():
    if not REVIEWED.exists():
        raise SystemExit(f"Missing file: {REVIEWED}")

    try:
        records = json.loads(
            REVIEWED.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {exc}")

    if not isinstance(records, list):
        raise SystemExit("Reviewed dataset root must be a JSON array.")

    matches = [
        r for r in records
        if isinstance(r, dict) and r.get("id") == TARGET_ID
    ]

    if len(matches) != 1:
        raise SystemExit(
            f"Expected exactly one {TARGET_ID}, found {len(matches)}."
        )

    record = matches[0]

    if record.get("word") != "月饼":
        raise SystemExit(
            f"Unexpected word for {TARGET_ID}: "
            f"{record.get('word')!r}"
        )

    if record.get("pinyin") != "yuèbing":
        raise SystemExit(
            f"Unexpected pinyin for {TARGET_ID}: "
            f"{record.get('pinyin')!r}"
        )

    # Only fix the missing meaning fields and verification metadata.
    record["meaningVi"] = MEANING
    record["candidateMeanings"] = MEANING
    record["selectedMeaningVi"] = MEANING
    record["reviewed"] = False
    record["reviewRequired"] = True
    record["status"] = "ai_assisted_unverified"
    record["verificationMode"] = "ai_assisted_unverified"
    record["translationAccuracyVerified"] = False
    record["reviewNotes"] = (
        "Meaning manually supplied for the unresolved candidate: "
        "月饼 (yuèbing) = bánh trung thu. "
        "Not human-verified."
    )

    REVIEWED.write_text(
        json.dumps(
            records,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=" * 72)
    print("HSK 4 UNRESOLVED MEANING FIX")
    print("=" * 72)
    print()
    print("Fixed ID:       hsk4_908")
    print("Chinese:        月饼")
    print("Pinyin:         yuèbing")
    print("Meaning (VI):   bánh trung thu")
    print("Verification:   AI-assisted / unverified")
    print()
    print(f"Updated:        {REVIEWED}")
    print()
    print("SUCCESS")
    print("Only hsk4_908 was modified.")
    print("No production data was created.")


if __name__ == "__main__":
    main()
