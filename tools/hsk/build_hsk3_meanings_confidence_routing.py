#!/usr/bin/env python3
"""Build HSK 3 meaning confidence and review routing.

Input:
    data/hsk/hsk3/hsk3_meanings_candidates.json

Outputs:
    data/hsk/hsk3/hsk3_meanings_confidence.json
    data/hsk/hsk3/hsk3_meanings_review_queue.json
    data/hsk/hsk3/hsk3_meaning_review_routing.json

This is a structural routing step only.
It does NOT verify translation accuracy and does NOT auto-approve meanings.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk3"
INPUT = DATA_DIR / "hsk3_meanings_candidates.json"
CONFIDENCE = DATA_DIR / "hsk3_meanings_confidence.json"
QUEUE = DATA_DIR / "hsk3_meanings_review_queue.json"
ROUTING = DATA_DIR / "hsk3_meaning_review_routing.json"

EXPECTED_COUNT = 500


def load_json(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing input: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {exc}")


def confidence_for(record: dict) -> tuple[str, list[str]]:
    reasons = []
    meanings = record.get("candidateMeanings", [])

    if not isinstance(meanings, list) or not meanings:
        return "LOW", ["No candidate meanings."]

    valid = [
        x.strip()
        for x in meanings
        if isinstance(x, str) and x.strip()
    ]

    if not valid:
        return "LOW", ["No usable candidate meanings."]

    # Conservative structural heuristic:
    # one concise candidate is usually LIGHT verification;
    # multiple candidates require FULL review because selection/context matters.
    if len(valid) == 1:
        text = valid[0]
        if len(text) <= 80:
            return "HIGH", ["Single concise candidate meaning."]
        return "MEDIUM", ["Single but relatively long candidate meaning."]

    reasons.append(f"{len(valid)} candidate meanings require selection.")
    return "MEDIUM", reasons


def main():
    print("=" * 72)
    print("HSK 3 MEANING CONFIDENCE / REVIEW ROUTING")
    print("=" * 72)
    print()

    records = load_json(INPUT)

    if not isinstance(records, list):
        raise SystemExit("Candidate root must be a JSON array.")

    if len(records) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} candidate records, got {len(records)}."
        )

    confidence_records = []
    queue = []

    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for record in records:
        if not isinstance(record, dict):
            raise SystemExit("Candidate record must be an object.")

        rid = record.get("id")
        if not rid:
            raise SystemExit("Candidate record missing id.")

        confidence, reasons = confidence_for(record)
        counts[confidence] += 1

        if confidence == "HIGH":
            review_mode = "LIGHT_VERIFICATION"
        elif confidence == "MEDIUM":
            review_mode = "FULL_REVIEW"
        else:
            review_mode = "FULL_REVIEW"

        item = {
            "id": rid,
            "word": record.get("word"),
            "pinyin": record.get("pinyin"),
            "partOfSpeech": record.get("partOfSpeech", []),
            "candidateMeanings": record.get("candidateMeanings", []),
            "confidence": confidence,
            "confidenceReasons": reasons,
            "reviewMode": review_mode,
            "reviewed": False,
            "generationStatus": record.get("generationStatus"),
            "verificationStatus": record.get("verificationStatus"),
        }

        confidence_records.append(item)
        queue.append(item)

    CONFIDENCE.parent.mkdir(parents=True, exist_ok=True)

    CONFIDENCE.write_text(
        json.dumps(confidence_records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    QUEUE.write_text(
        json.dumps(queue, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    routing_report = {
        "status": "SUCCESS",
        "level": 3,
        "candidateRecords": len(records),
        "confidence": counts,
        "reviewRouting": {
            "LIGHT_VERIFICATION": counts["HIGH"],
            "FULL_REVIEW": counts["MEDIUM"] + counts["LOW"],
        },
        "aiApiCalled": False,
        "automaticApproval": False,
        "translationAccuracyVerified": False,
    }

    ROUTING.write_text(
        json.dumps(routing_report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Candidate records:       {len(records)}/{EXPECTED_COUNT}")
    print(f"HIGH:                    {counts['HIGH']}")
    print(f"MEDIUM:                  {counts['MEDIUM']}")
    print(f"LOW:                     {counts['LOW']}")
    print()
    print(f"LIGHT VERIFICATION:      {counts['HIGH']}")
    print(f"FULL REVIEW:             {counts['MEDIUM'] + counts['LOW']}")
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
