#!/usr/bin/env python3
"""Build HSK 4 meaning confidence and review routing.

Input:
    data/hsk/hsk4/hsk4_meanings_candidates_input.json

Outputs:
    data/hsk/hsk4/hsk4_meanings_confidence.json
    data/hsk/hsk4/hsk4_meanings_review_queue.json
    data/hsk/hsk4/hsk4_meaning_review_routing.json

This is a routing/structural step only.
It does not auto-approve translation accuracy.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk4"

INPUT = DATA / "hsk4_meanings_candidates_input.json"
CONFIDENCE = DATA / "hsk4_meanings_confidence.json"
QUEUE = DATA / "hsk4_meanings_review_queue.json"
ROUTING = DATA / "hsk4_meaning_review_routing.json"

EXPECTED_COUNT = 1000


def load_json(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing input: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {exc}")


def classify(record: dict):
    meanings = record.get("candidateMeanings")

    if not isinstance(meanings, list):
        return "LOW", ["candidateMeanings is not a list."]

    valid = [
        str(x).strip()
        for x in meanings
        if isinstance(x, str) and str(x).strip()
    ]

    if not valid:
        return "LOW", ["No candidate meaning."]

    if any(
        value.startswith("[CẦN XÁC MINH]")
        for value in valid
    ):
        return "LOW", ["Candidate explicitly requires verification."]

    if len(valid) == 1 and len(valid[0]) <= 80:
        return "HIGH", ["Single concise candidate meaning."]

    return "MEDIUM", [
        f"{len(valid)} candidate meaning(s) require verification."
    ]


def main():
    print("=" * 72)
    print("HSK 4 MEANING CONFIDENCE / REVIEW ROUTING")
    print("=" * 72)
    print()

    records = load_json(INPUT)

    if not isinstance(records, list):
        raise SystemExit("Candidate root must be a JSON array.")

    if len(records) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} records, got {len(records)}."
        )

    confidence_records = []
    review_queue = []
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for record in records:
        if not isinstance(record, dict):
            raise SystemExit("Candidate record must be an object.")

        rid = record.get("id")
        if not rid:
            raise SystemExit("Candidate record missing id.")

        confidence, reasons = classify(record)
        counts[confidence] += 1

        review_mode = (
            "LIGHT_VERIFICATION"
            if confidence == "HIGH"
            else "FULL_REVIEW"
        )

        item = {
            "id": rid,
            "word": record.get("word"),
            "pinyin": record.get("pinyin"),
            "partOfSpeech": record.get("partOfSpeech", []),
            "candidateMeanings": record.get(
                "candidateMeanings", []
            ),
            "confidence": confidence,
            "confidenceReasons": reasons,
            "reviewMode": review_mode,
            "reviewed": False,
            "generationStatus": record.get("generationStatus"),
            "generationSource": record.get("generationSource"),
        }

        confidence_records.append(item)
        review_queue.append(item)

    DATA.mkdir(parents=True, exist_ok=True)

    CONFIDENCE.write_text(
        json.dumps(
            confidence_records,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    QUEUE.write_text(
        json.dumps(
            review_queue,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    routing = {
        "status": "SUCCESS",
        "level": 4,
        "candidateRecords": len(records),
        "confidence": counts,
        "reviewRouting": {
            "LIGHT_VERIFICATION": counts["HIGH"],
            "FULL_REVIEW": (
                counts["MEDIUM"] + counts["LOW"]
            ),
        },
        "aiApiCalled": False,
        "automaticApproval": False,
        "translationAccuracyVerified": False,
        "note": (
            "HIGH means light verification routing only; "
            "it does not mean translation accuracy was verified."
        ),
    }

    ROUTING.write_text(
        json.dumps(
            routing,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Candidate records:       {len(records)}/{EXPECTED_COUNT}")
    print(f"HIGH:                    {counts['HIGH']}")
    print(f"MEDIUM:                  {counts['MEDIUM']}")
    print(f"LOW:                     {counts['LOW']}")
    print()
    print(
        f"LIGHT VERIFICATION:      {counts['HIGH']}"
    )
    print(
        f"FULL REVIEW:             "
        f"{counts['MEDIUM'] + counts['LOW']}"
    )
    print()
    print(f"Confidence report:       {CONFIDENCE}")
    print(f"Review queue:            {QUEUE}")
    print(f"Routing report:          {ROUTING}")
    print()
    print("SUCCESS")
    print("Routing completed.")
    print()
    print("IMPORTANT:")
    print("- No meanings were auto-approved.")
    print("- Translation accuracy is not independently verified.")
    print("- No reviewed or production data was modified.")


if __name__ == "__main__":
    main()
