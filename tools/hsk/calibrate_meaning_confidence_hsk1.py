#!/usr/bin/env python3
"""
HSK 1 meaning confidence calibration pilot.

Compares the pre-review meaning candidates with the final reviewed meanings.
This is a calibration experiment only.

It supports the actual project structure where:
    hsk1_meanings_draft_v2.json
is an object containing:
    {
        "datasetName": ...,
        "recordCount": 300,
        "records": [...]
    }

It does NOT modify the reviewed or production datasets.

Run from the project root:
    python tools/hsk/calibrate_meaning_confidence_hsk1.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk1"

CANDIDATE_FILE = DATA_DIR / "hsk1_meanings_draft_v2.json"
REFERENCE_FILE = DATA_DIR / "hsk1_vocabulary_reviewed.json"
OUTPUT_FILE = DATA_DIR / "hsk1_meaning_confidence_calibration.json"

EXPECTED_COUNT = 300


def load_json(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def extract_records(data, label: str):
    """
    Accept either:
      - a direct JSON array
      - an object containing a 'records' array

    This makes the calibration tool compatible with the project's
    actual draft-v2 wrapper structure.
    """
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict) and isinstance(data.get("records"), list):
        records = data["records"]
    else:
        raise SystemExit(
            f"{label} must be a JSON array or an object containing "
            f"a 'records' array."
        )

    return records


def normalize_text(value: str) -> str:
    value = str(value).lower().strip()

    # Normalize common punctuation used in Vietnamese meanings.
    value = re.sub(
        r"[，。！？、；：,.!?;:()\[\]（）\"“”‘’]",
        " ",
        value,
    )

    return re.sub(r"\s+", " ", value).strip()


def meaning_set(record):
    values = record.get("meaningVi", [])

    if isinstance(values, str):
        values = [values]

    if not isinstance(values, list):
        return set()

    return {
        normalize_text(value)
        for value in values
        if isinstance(value, str) and value.strip()
    }


def score_candidate(candidate, reference):
    candidate_meanings = meaning_set(candidate)
    reference_meanings = meaning_set(reference)

    if not candidate_meanings:
        return 0.0, "missing_candidate_meaning"

    if not reference_meanings:
        return 0.0, "missing_reference_meaning"

    # Exact set agreement.
    if candidate_meanings == reference_meanings:
        return 1.0, "exact_match"

    # Explainable overlap score.
    intersection = len(candidate_meanings & reference_meanings)
    union = len(candidate_meanings | reference_meanings)
    jaccard = intersection / union if union else 0.0

    if jaccard >= 0.5:
        return 0.80, "partial_meaning_overlap"

    # One meaning may be a textual expansion/contraction of another.
    for candidate_value in candidate_meanings:
        for reference_value in reference_meanings:
            if (
                candidate_value in reference_value
                or reference_value in candidate_value
            ):
                return 0.65, "textual_meaning_overlap"

    return 0.40, "meaning_disagreement"


def route(score: float) -> str:
    if score >= 0.90:
        return "HIGH"

    if score >= 0.70:
        return "MEDIUM"

    return "LOW"


def main():
    print("=" * 64)
    print("HSK 1 MEANING CONFIDENCE CALIBRATION PILOT")
    print("=" * 64)
    print()

    candidate_data = load_json(CANDIDATE_FILE)
    reference_data = load_json(REFERENCE_FILE)

    candidates = extract_records(candidate_data, "Candidate file")
    references = extract_records(reference_data, "Reference file")

    if len(candidates) != EXPECTED_COUNT:
        raise SystemExit(
            f"Candidate records = {len(candidates)}, "
            f"expected {EXPECTED_COUNT}."
        )

    if len(references) != EXPECTED_COUNT:
        raise SystemExit(
            f"Reference records = {len(references)}, "
            f"expected {EXPECTED_COUNT}."
        )

    reference_by_id = {
        record.get("id"): record
        for record in references
        if isinstance(record, dict) and record.get("id")
    }

    results = []

    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue

        record_id = candidate.get("id")
        reference = reference_by_id.get(record_id)

        if reference is None:
            confidence = 0.0
            reason = "missing_reference_record"
        else:
            confidence, reason = score_candidate(candidate, reference)

        results.append(
            {
                "id": record_id,
                "word": candidate.get("word"),
                "pinyin": candidate.get("pinyin"),
                "candidateMeaningVi": candidate.get("meaningVi", []),
                "reviewedMeaningVi": (
                    reference.get("meaningVi", [])
                    if reference
                    else []
                ),
                "confidence": confidence,
                "routing": route(confidence),
                "reason": reason,
            }
        )

    total = len(results)

    if total != EXPECTED_COUNT:
        raise SystemExit(
            f"Calibration results = {total}, expected {EXPECTED_COUNT}."
        )

    high = sum(item["routing"] == "HIGH" for item in results)
    medium = sum(item["routing"] == "MEDIUM" for item in results)
    low = sum(item["routing"] == "LOW" for item in results)

    exact = sum(
        item["reason"] == "exact_match"
        for item in results
    )

    high_precision = exact / high if high else None

    report = {
        "dataset": "HSK 1",
        "type": "MEANING_CONFIDENCE_CALIBRATION_PILOT",
        "status": "PASS",
        "records": total,
        "routing": {
            "HIGH": high,
            "MEDIUM": medium,
            "LOW": low,
        },
        "exactMatches": exact,
        "highPrecision": high_precision,
        "thresholds": {
            "HIGH": ">= 0.90",
            "MEDIUM": "0.70-0.89",
            "LOW": "< 0.70",
        },
        "inputCandidateFile": str(CANDIDATE_FILE),
        "inputReferenceFile": str(REFERENCE_FILE),
        "results": results,
        "note": (
            "This is a calibration experiment using HSK 1 reviewed data. "
            "The heuristic score is not an AI confidence guarantee and "
            "must not be treated as production calibration."
        ),
    }

    OUTPUT_FILE.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Candidate records: {len(candidates)}/{EXPECTED_COUNT}")
    print(f"Reference records: {len(references)}/{EXPECTED_COUNT}")
    print(f"Records compared:  {total}/{EXPECTED_COUNT}")
    print(f"Exact matches:     {exact}")
    print(f"HIGH:              {high}")
    print(f"MEDIUM:            {medium}")
    print(f"LOW:               {low}")

    if high_precision is None:
        print("HIGH precision:    n/a")
    else:
        print(f"HIGH precision:    {high_precision:.2%}")

    print(f"Output:            {OUTPUT_FILE}")
    print()
    print("SUCCESS")
    print("No reviewed or production data was modified.")


if __name__ == "__main__":
    main()
