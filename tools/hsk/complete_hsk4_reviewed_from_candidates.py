#!/usr/bin/env python3
"""Complete HSK 4 reviewed dataset from meaning candidates.

Input:
    data/hsk/hsk4/hsk4_vocabulary_base.json
    data/hsk/hsk4/hsk4_meanings_candidates_input.json

Optional existing reviewed data:
    data/hsk/hsk4/hsk4_vocabulary_reviewed.json

Output:
    data/hsk/hsk4/hsk4_vocabulary_reviewed.json
    data/hsk/hsk4/hsk4_reviewed_completion_report.json

Existing reviewed records are preserved.
Missing records are filled from candidate meanings and explicitly marked
AI-assisted/unverified. No production data is created.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk4"

BASE = DATA / "hsk4_vocabulary_base.json"
CANDIDATES = DATA / "hsk4_meanings_candidates_input.json"
REVIEWED = DATA / "hsk4_vocabulary_reviewed.json"
REPORT = DATA / "hsk4_reviewed_completion_report.json"

EXPECTED_COUNT = 1000


def load(path: Path, required: bool = True):
    if not path.exists():
        if required:
            raise SystemExit(f"Missing input: {path}")
        return []

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"Invalid JSON in {path}: {exc}"
        )


def by_id(records, label: str):
    if not isinstance(records, list):
        raise SystemExit(
            f"{label} must be a JSON array."
        )

    result = {}

    for record in records:
        if not isinstance(record, dict):
            raise SystemExit(
                f"{label} contains a non-object record."
            )

        rid = record.get("id")

        if not rid:
            raise SystemExit(
                f"{label} contains a record without id."
            )

        if rid in result:
            raise SystemExit(
                f"Duplicate ID in {label}: {rid}"
            )

        result[rid] = record

    return result


def clean_meanings(record: dict):
    values = record.get(
        "candidateMeanings",
        [],
    )

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

        # Never promote the unresolved placeholder as a real meaning.
        if value.startswith("[CẦN XÁC MINH]"):
            continue

        key = value.casefold()

        if key not in seen:
            seen.add(key)
            result.append(value)

    return result


def main():
    print("=" * 72)
    print("HSK 4 REVIEWED DATA COMPLETION")
    print("=" * 72)
    print()

    base = by_id(
        load(BASE),
        "HSK 4 base",
    )

    candidates = by_id(
        load(CANDIDATES),
        "HSK 4 candidates",
    )

    existing = by_id(
        load(
            REVIEWED,
            required=False,
        ),
        "existing HSK 4 reviewed data",
    )

    if len(base) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} base records, "
            f"got {len(base)}."
        )

    if len(candidates) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} candidate records, "
            f"got {len(candidates)}."
        )

    expected_ids = set(base)

    if set(candidates) != expected_ids:
        raise SystemExit(
            "Candidate IDs do not exactly match HSK 4 base IDs."
        )

    reviewed = {}
    preserved = []
    added = []
    unresolved = []

    for rid, record in existing.items():
        if rid not in expected_ids:
            raise SystemExit(
                "Existing reviewed record is not an HSK 4 "
                f"base ID: {rid}"
            )

        reviewed[rid] = record
        preserved.append(rid)

    for i in range(
        1,
        EXPECTED_COUNT + 1,
    ):
        rid = f"hsk4_{i:03d}"

        if rid in reviewed:
            continue

        base_record = base[rid]
        candidate = candidates[rid]
        meanings = clean_meanings(candidate)

        item = dict(base_record)

        if meanings:
            item["meaningVi"] = meanings
            item["candidateMeanings"] = meanings
            item["selectedMeaningVi"] = meanings

            item["reviewed"] = False
            item["reviewRequired"] = True
            item["status"] = "ai_assisted_unverified"
            item["verificationMode"] = (
                "ai_assisted_unverified"
            )
            item["translationAccuracyVerified"] = False
            item["reviewNotes"] = (
                "Meaning populated from AI/reference candidate "
                "package. Not independently human-verified."
            )

        else:
            # Keep unresolved entries structurally explicit instead of
            # inventing a Vietnamese meaning.
            item["meaningVi"] = []
            item["candidateMeanings"] = []
            item["selectedMeaningVi"] = []

            item["reviewed"] = False
            item["reviewRequired"] = True
            item["status"] = "needs_manual_verification"
            item["verificationMode"] = (
                "needs_manual_verification"
            )
            item["translationAccuracyVerified"] = False
            item["reviewNotes"] = (
                "No usable candidate meaning was found. "
                "Manual verification required."
            )

            unresolved.append(rid)

        reviewed[rid] = item
        added.append(rid)

    if len(reviewed) != EXPECTED_COUNT:
        raise SystemExit(
            f"Completion failed: expected {EXPECTED_COUNT}, "
            f"got {len(reviewed)}."
        )

    ordered = [
        reviewed[f"hsk4_{i:03d}"]
        for i in range(
            1,
            EXPECTED_COUNT + 1,
        )
    ]

    REVIEWED.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REVIEWED.write_text(
        json.dumps(
            ordered,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    human_count = sum(
        record.get("reviewed") is True
        for record in ordered
    )

    ai_count = sum(
        record.get("verificationMode")
        == "ai_assisted_unverified"
        for record in ordered
    )

    unresolved_count = sum(
        record.get("verificationMode")
        == "needs_manual_verification"
        for record in ordered
    )

    report = {
        "status": "COMPLETE_FOR_VALIDATION",
        "level": 4,
        "totalRecords": len(ordered),
        "preservedExistingRecords": len(preserved),
        "filledFromCandidates": len(added),
        "humanVerifiedRecords": human_count,
        "aiAssistedUnverifiedRecords": ai_count,
        "needsManualVerificationRecords": unresolved_count,
        "unresolvedIds": unresolved,
        "productionCreated": False,
        "note": (
            "Dataset is complete for structural validation. "
            "AI-assisted meanings are not human-verified. "
            "Unresolved meanings remain explicitly flagged."
        ),
    }

    REPORT.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Base records:                 "
        f"{len(base)}/{EXPECTED_COUNT}"
    )
    print(
        f"Candidate records:            "
        f"{len(candidates)}/{EXPECTED_COUNT}"
    )
    print(
        f"Existing reviewed preserved:  "
        f"{len(preserved)}"
    )
    print(
        f"Filled from candidates:       "
        f"{len(added)}"
    )
    print(
        f"Final reviewed file records:  "
        f"{len(ordered)}/{EXPECTED_COUNT}"
    )
    print(
        f"Human verified:               "
        f"{human_count}"
    )
    print(
        f"AI-assisted unverified:       "
        f"{ai_count}"
    )
    print(
        f"Needs manual verification:    "
        f"{unresolved_count}"
    )
    print()
    print(f"Output: {REVIEWED}")
    print(f"Report: {REPORT}")
    print()
    print("SUCCESS")
    print(
        "HSK 4 reviewed dataset completed for validation."
    )
    print(
        "No production data was created."
    )
    print(
        "AI-assisted meanings remain explicitly unverified."
    )

    if unresolved:
        print()
        print("Unresolved IDs:")
        print(", ".join(unresolved))


if __name__ == "__main__":
    main()
