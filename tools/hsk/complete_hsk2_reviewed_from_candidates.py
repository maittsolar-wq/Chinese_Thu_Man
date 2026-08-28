#!/usr/bin/env python3
"""Complete HSK 2 reviewed dataset from existing candidate meanings.

This is a controlled bridge step for the current HSK 2 pipeline.

It:
- preserves any records already present in hsk2_vocabulary_reviewed.json;
- fills only missing HSK 2 records from hsk2_meanings_candidates.json;
- keeps the authoritative vocabulary fields from hsk2_vocabulary_base.json;
- marks newly filled records as AI-assisted/unverified;
- never creates production data;
- never overwrites an already-reviewed record.

Run from project root:
    python tools/hsk/complete_hsk2_reviewed_from_candidates.py
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk2"

BASE_FILE = DATA_DIR / "hsk2_vocabulary_base.json"
CANDIDATES_FILE = DATA_DIR / "hsk2_meanings_candidates.json"
REVIEWED_FILE = DATA_DIR / "hsk2_vocabulary_reviewed.json"
REPORT_FILE = DATA_DIR / "hsk2_reviewed_completion_report.json"

EXPECTED_COUNT = 200


def load_json(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def index(records, label):
    if not isinstance(records, list):
        raise SystemExit(f"{label} must be a JSON array.")

    result = {}

    for record in records:
        if not isinstance(record, dict):
            raise SystemExit(
                f"{label} contains a non-object record."
            )

        record_id = record.get("id")

        if not record_id:
            raise SystemExit(
                f"{label} contains a record without id."
            )

        if record_id in result:
            raise SystemExit(
                f"Duplicate ID in {label}: {record_id}"
            )

        result[record_id] = record

    return result


def normalize_meanings(values):
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
    print("HSK 2 REVIEWED DATA COMPLETION")
    print("=" * 72)
    print()

    base = index(
        load_json(BASE_FILE),
        "HSK 2 base",
    )
    candidates = index(
        load_json(CANDIDATES_FILE),
        "HSK 2 candidates",
    )
    existing = index(
        load_json(REVIEWED_FILE),
        "existing HSK 2 reviewed data",
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
            "Candidate IDs do not exactly match HSK 2 base IDs."
        )

    reviewed = {}
    preserved = []
    added = []

    # Preserve existing reviewed records exactly.
    for record_id, record in existing.items():
        if record_id not in expected_ids:
            raise SystemExit(
                f"Existing reviewed record is not an HSK 2 base ID: "
                f"{record_id}"
            )

        reviewed[record_id] = record
        preserved.append(record_id)

    for record_id in sorted(expected_ids):
        if record_id in reviewed:
            continue

        base_record = base[record_id]
        candidate = candidates[record_id]

        meanings = normalize_meanings(
            candidate.get("candidateMeanings", [])
        )

        if not meanings:
            raise SystemExit(
                f"{record_id} has no usable candidate meanings."
            )

        # Start from the authoritative base record.
        completed = dict(base_record)

        completed["meaningVi"] = meanings
        completed["candidateMeanings"] = meanings
        completed["selectedMeaningVi"] = meanings

        # Explicitly distinguish this bridge state from human review.
        completed["reviewed"] = False
        completed["reviewRequired"] = True
        completed["status"] = "ai_assisted_unverified"
        completed["verificationMode"] = "ai_assisted_unverified"
        completed["reviewNotes"] = (
            "Meaning populated from AI candidate package. "
            "Not independently human-verified."
        )

        reviewed[record_id] = completed
        added.append(record_id)

    if len(reviewed) != EXPECTED_COUNT:
        raise SystemExit(
            f"Completion failed: expected {EXPECTED_COUNT} records, "
            f"got {len(reviewed)}."
        )

    ordered = [
        reviewed[f"hsk2_{i:03d}"]
        for i in range(1, EXPECTED_COUNT + 1)
    ]

    save_json(REVIEWED_FILE, ordered)

    report = {
        "status": "COMPLETE_FOR_VALIDATION",
        "level": 2,
        "totalRecords": EXPECTED_COUNT,
        "preservedExistingRecords": len(preserved),
        "filledFromCandidates": len(added),
        "preservedIds": preserved,
        "filledIds": added,
        "humanVerifiedRecords": sum(
            r.get("reviewed") is True
            for r in ordered
        ),
        "aiAssistedUnverifiedRecords": sum(
            r.get("verificationMode") == "ai_assisted_unverified"
            for r in ordered
        ),
        "productionCreated": False,
        "note": (
            "This step completes the dataset shape for validation only. "
            "AI-assisted meanings are not treated as human-verified."
        ),
    }

    save_json(REPORT_FILE, report)

    print(f"Base records:                 {len(base)}/{EXPECTED_COUNT}")
    print(f"Candidate records:            {len(candidates)}/{EXPECTED_COUNT}")
    print(f"Existing reviewed preserved:  {len(preserved)}")
    print(f"Filled from candidates:       {len(added)}")
    print(f"Final reviewed file records:  {len(ordered)}/{EXPECTED_COUNT}")
    print()
    print(f"Output: {REVIEWED_FILE}")
    print(f"Report: {REPORT_FILE}")
    print()
    print("SUCCESS")
    print()
    print("IMPORTANT:")
    print("- Existing reviewed records were preserved.")
    print("- Newly filled meanings are AI-assisted and unverified.")
    print("- No production data was created.")
    print("- Next step: reviewed-data validation.")


if __name__ == "__main__":
    main()
