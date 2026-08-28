#!/usr/bin/env python3
"""Route HSK 2 meaning candidates into a focused human-review queue.

Run from project root:
    python tools/hsk/route_hsk2_meaning_review.py

Inputs:
    data/hsk/hsk2/hsk2_meanings_candidates.json
    data/hsk/hsk2/hsk2_meanings_confidence.json
    data/hsk/hsk2/hsk2_meanings_candidates_validation.json

Optional calibration input:
    data/hsk/hsk1/hsk1_meaning_confidence_calibration.json

Outputs:
    data/hsk/hsk2/hsk2_meaning_review_routing.json
    data/hsk/hsk2/hsk2_meaning_review_queue.json

Important:
- This script does NOT approve any meaning.
- It does NOT create production data.
- It does NOT claim that HIGH means translation accuracy is verified.
- HSK 1 calibration is used only as supporting evidence when present.
- Because the current HSK 2 confidence score is structural, the routing
  remains conservative.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
H2_DIR = ROOT / "data" / "hsk" / "hsk2"
H1_DIR = ROOT / "data" / "hsk" / "hsk1"

CANDIDATES_FILE = H2_DIR / "hsk2_meanings_candidates.json"
CONFIDENCE_FILE = H2_DIR / "hsk2_meanings_confidence.json"
VALIDATION_FILE = H2_DIR / "hsk2_meanings_candidates_validation.json"
CALIBRATION_FILE = H1_DIR / "hsk1_meaning_confidence_calibration.json"

ROUTING_FILE = H2_DIR / "hsk2_meaning_review_routing.json"
QUEUE_FILE = H2_DIR / "hsk2_meaning_review_queue.json"

EXPECTED_COUNT = 200


def load_json(path: Path, required: bool = True):
    if not path.exists():
        if required:
            raise SystemExit(f"Missing required file: {path}")
        return None

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def by_id(records, label):
    if not isinstance(records, list):
        raise SystemExit(f"{label} must contain a JSON array.")

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


def calibration_summary(calibration):
    """Extract HSK 1 calibration evidence without inventing new evidence."""
    if not isinstance(calibration, dict):
        return {
            "available": False,
            "highPrecision": None,
            "recordsCompared": 0,
        }

    return {
        "available": True,
        "highPrecision": calibration.get("highPrecision"),
        "recordsCompared": calibration.get(
            "recordsCompared",
            calibration.get("recordCount", 0),
        ),
        "exactMatches": calibration.get("exactMatches"),
        "high": calibration.get("high"),
    }


def main():
    print("=" * 72)
    print("HSK 2 MEANING REVIEW ROUTING")
    print("=" * 72)
    print()

    candidates = load_json(CANDIDATES_FILE)
    confidence = load_json(CONFIDENCE_FILE)
    validation = load_json(VALIDATION_FILE)
    calibration = load_json(CALIBRATION_FILE, required=False)

    candidate_by_id = by_id(
        candidates,
        "HSK 2 candidates",
    )

    confidence_records = confidence.get("records")
    confidence_by_id = by_id(
        confidence_records,
        "HSK 2 confidence",
    )

    if validation.get("status") != "PASS":
        raise SystemExit(
            "Candidate validation is not PASS. "
            "Fix validation before routing."
        )

    if len(candidate_by_id) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} HSK 2 candidates, "
            f"got {len(candidate_by_id)}."
        )

    expected_ids = set(candidate_by_id)

    if set(confidence_by_id) != expected_ids:
        raise SystemExit(
            "Candidate and confidence IDs do not match."
        )

    calibration_info = calibration_summary(calibration)

    routed = []
    review_queue = []

    for record_id in sorted(expected_ids):
        candidate = candidate_by_id[record_id]
        confidence_record = confidence_by_id[record_id]

        route = confidence_record.get("routing")
        structural_score = confidence_record.get(
            "structuralScore"
        )

        # IMPORTANT:
        # Current HSK 2 HIGH is only a structural signal. Therefore:
        # - HIGH: "light verification" queue
        # - MEDIUM/LOW: "full verification" queue
        # Nothing is auto-approved.
        if route == "HIGH":
            review_type = "LIGHT_VERIFICATION"
            priority = 3
            reason = (
                "Structural candidate passed clean checks, but "
                "translation accuracy is not independently verified."
            )
        elif route == "MEDIUM":
            review_type = "FULL_REVIEW"
            priority = 2
            reason = (
                "Candidate has weaker structural confidence and "
                "requires human verification."
            )
        else:
            review_type = "FULL_REVIEW"
            priority = 1
            reason = (
                "Candidate has LOW structural confidence and "
                "requires human verification."
            )

        item = {
            "id": record_id,
            "word": candidate.get("word"),
            "pinyin": candidate.get("pinyin"),
            "partOfSpeech": candidate.get("partOfSpeech", []),
            "candidateMeanings": candidate.get(
                "candidateMeanings",
                [],
            ),
            "structuralScore": structural_score,
            "sourceRouting": route,
            "reviewType": review_type,
            "priority": priority,
            "reason": reason,
            "approved": False,
            "reviewed": False,
        }

        routed.append(item)

        # The queue intentionally contains ALL records.
        # HIGH records are lighter review, not auto-approved.
        review_queue.append(item)

    review_queue.sort(
        key=lambda x: (x["priority"], x["id"])
    )

    counts = {
        "LIGHT_VERIFICATION": sum(
            x["reviewType"] == "LIGHT_VERIFICATION"
            for x in routed
        ),
        "FULL_REVIEW": sum(
            x["reviewType"] == "FULL_REVIEW"
            for x in routed
        ),
    }

    source_routing = {
        "HIGH": sum(x["sourceRouting"] == "HIGH" for x in routed),
        "MEDIUM": sum(x["sourceRouting"] == "MEDIUM" for x in routed),
        "LOW": sum(x["sourceRouting"] == "LOW" for x in routed),
    }

    routing_report = {
        "status": "ROUTING_COMPLETE",
        "level": 2,
        "recordCount": len(routed),
        "sourceRouting": source_routing,
        "reviewTypes": counts,
        "calibrationReference": {
            "used": calibration_info["available"],
            "data": calibration_info,
            "note": (
                "HSK 1 calibration is supporting evidence only. "
                "It does not independently verify HSK 2 translations."
            ),
        },
        "policy": {
            "autoApproval": False,
            "productionApproval": False,
            "highMeansAccuracyVerified": False,
            "highAction": "LIGHT_VERIFICATION",
            "mediumAction": "FULL_REVIEW",
            "lowAction": "FULL_REVIEW",
        },
        "records": routed,
    }

    queue_report = {
        "status": "REVIEW_QUEUE_READY",
        "level": 2,
        "recordCount": len(review_queue),
        "reviewTypes": counts,
        "records": review_queue,
    }

    ROUTING_FILE.write_text(
        json.dumps(
            routing_report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    QUEUE_FILE.write_text(
        json.dumps(
            queue_report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Candidate records: {len(routed)}/{EXPECTED_COUNT}")
    print()
    print("Source routing:")
    print(f"  HIGH:   {source_routing['HIGH']}")
    print(f"  MEDIUM: {source_routing['MEDIUM']}")
    print(f"  LOW:    {source_routing['LOW']}")
    print()
    print("Review routing:")
    print(
        "  LIGHT VERIFICATION:",
        counts["LIGHT_VERIFICATION"],
    )
    print(
        "  FULL REVIEW:       ",
        counts["FULL_REVIEW"],
    )
    print()
    print(
        "HSK 1 calibration available:",
        "YES" if calibration_info["available"] else "NO",
    )
    print()
    print(f"Routing report: {ROUTING_FILE}")
    print(f"Review queue:   {QUEUE_FILE}")
    print()
    print("SUCCESS")
    print()
    print("IMPORTANT:")
    print("- No meanings were auto-approved.")
    print("- No reviewed data was modified.")
    print("- No production data was created.")
    print(
        "- HIGH means light verification only, "
        "not translation accuracy verified."
    )


if __name__ == "__main__":
    main()
