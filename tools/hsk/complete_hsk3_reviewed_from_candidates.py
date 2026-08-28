#!/usr/bin/env python3
"""Complete HSK 3 reviewed dataset from meaning candidates.

Input:
    data/hsk/hsk3/hsk3_vocabulary_base.json
    data/hsk/hsk3/hsk3_meanings_candidates.json
    data/hsk/hsk3/hsk3_vocabulary_reviewed.json (optional)

Output:
    data/hsk/hsk3/hsk3_vocabulary_reviewed.json
    data/hsk/hsk3/hsk3_reviewed_completion_report.json

Existing reviewed records are preserved.
Missing records are filled from candidate meanings and explicitly marked
AI-assisted/unverified. No production data is created.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk3"

BASE = DATA / "hsk3_vocabulary_base.json"
CANDIDATES = DATA / "hsk3_meanings_candidates.json"
REVIEWED = DATA / "hsk3_vocabulary_reviewed.json"
REPORT = DATA / "hsk3_reviewed_completion_report.json"

EXPECTED_COUNT = 500


def load(path: Path, required=True):
    if not path.exists():
        if required:
            raise SystemExit(f"Missing input: {path}")
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def by_id(records, label):
    if not isinstance(records, list):
        raise SystemExit(f"{label} must be a JSON array.")
    result = {}
    for record in records:
        if not isinstance(record, dict):
            raise SystemExit(f"{label} contains a non-object record.")
        rid = record.get("id")
        if not rid:
            raise SystemExit(f"{label} contains a record without id.")
        if rid in result:
            raise SystemExit(f"Duplicate ID in {label}: {rid}")
        result[rid] = record
    return result


def meanings_from_candidate(record):
    values = record.get("candidateMeanings", [])
    if not isinstance(values, list):
        return []

    result = []
    seen = set()

    for value in values:
        if not isinstance(value, str):
            continue
        value = value.strip()
        if not value:
            continue
        key = value.casefold()
        if key not in seen:
            seen.add(key)
            result.append(value)

    return result


def main():
    print("=" * 72)
    print("HSK 3 REVIEWED DATA COMPLETION")
    print("=" * 72)
    print()

    base = by_id(load(BASE), "HSK 3 base")
    candidates = by_id(load(CANDIDATES), "HSK 3 candidates")
    existing = by_id(
        load(REVIEWED, required=False),
        "existing HSK 3 reviewed data",
    )

    if len(base) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} base records, got {len(base)}."
        )

    if len(candidates) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} candidate records, "
            f"got {len(candidates)}."
        )

    expected_ids = set(base)

    if set(candidates) != expected_ids:
        raise SystemExit(
            "Candidate IDs do not exactly match HSK 3 base IDs."
        )

    reviewed = {}
    preserved = []
    added = []

    for rid, record in existing.items():
        if rid not in expected_ids:
            raise SystemExit(
                f"Existing reviewed record is not an HSK 3 base ID: {rid}"
            )
        reviewed[rid] = record
        preserved.append(rid)

    for i in range(1, EXPECTED_COUNT + 1):
        rid = f"hsk3_{i:03d}"

        if rid in reviewed:
            continue

        base_record = base[rid]
        candidate = candidates[rid]
        meanings = meanings_from_candidate(candidate)

        if not meanings:
            raise SystemExit(
                f"{rid} has no usable candidate meanings."
            )

        item = dict(base_record)
        item["meaningVi"] = meanings
        item["candidateMeanings"] = meanings
        item["selectedMeaningVi"] = meanings

        item["reviewed"] = False
        item["reviewRequired"] = True
        item["status"] = "ai_assisted_unverified"
        item["verificationMode"] = "ai_assisted_unverified"
        item["translationAccuracyVerified"] = False
        item["reviewNotes"] = (
            "Meaning populated from AI candidate package. "
            "Not independently human-verified."
        )

        reviewed[rid] = item
        added.append(rid)

    if len(reviewed) != EXPECTED_COUNT:
        raise SystemExit(
            f"Completion failed: expected {EXPECTED_COUNT}, "
            f"got {len(reviewed)}."
        )

    ordered = [
        reviewed[f"hsk3_{i:03d}"]
        for i in range(1, EXPECTED_COUNT + 1)
    ]

    REVIEWED.parent.mkdir(parents=True, exist_ok=True)
    REVIEWED.write_text(
        json.dumps(ordered, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    human_count = sum(
        r.get("reviewed") is True for r in ordered
    )
    ai_count = sum(
        r.get("verificationMode") == "ai_assisted_unverified"
        for r in ordered
    )

    report = {
        "status": "COMPLETE_FOR_VALIDATION",
        "level": 3,
        "totalRecords": len(ordered),
        "preservedExistingRecords": len(preserved),
        "filledFromCandidates": len(added),
        "humanVerifiedRecords": human_count,
        "aiAssistedUnverifiedRecords": ai_count,
        "productionCreated": False,
        "note": (
            "Dataset is complete for structural validation. "
            "AI-assisted meanings are not human-verified."
        ),
    }

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Base records:                 {len(base)}/{EXPECTED_COUNT}")
    print(f"Candidate records:            {len(candidates)}/{EXPECTED_COUNT}")
    print(f"Existing reviewed preserved:  {len(preserved)}")
    print(f"Filled from candidates:       {len(added)}")
    print(f"Final reviewed file records:  {len(ordered)}/{EXPECTED_COUNT}")
    print(f"Human verified:               {human_count}")
    print(f"AI-assisted unverified:       {ai_count}")
    print()
    print(f"Output: {REVIEWED}")
    print(f"Report: {REPORT}")
    print()
    print("SUCCESS")
    print("HSK 3 reviewed dataset completed for validation.")
    print("No production data was created.")
    print("AI-assisted meanings remain explicitly unverified.")


if __name__ == "__main__":
    main()
