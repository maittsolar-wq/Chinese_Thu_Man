#!/usr/bin/env python3
"""HSK 5 meaning confidence / review routing.

Mirrors the HSK 3/4 confidence-routing contract:
- reads hsk5_meanings_candidates_input.json
- scores candidate quality using structural signals
- routes HIGH -> LIGHT VERIFICATION
- MEDIUM/LOW -> FULL REVIEW
- writes the three standard routing artifacts
- never auto-approves meanings
- never modifies reviewed/production data
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk5"

INPUT = DATA / "hsk5_meanings_candidates_input.json"
CONFIDENCE = DATA / "hsk5_meanings_confidence.json"
QUEUE = DATA / "hsk5_meanings_review_queue.json"
ROUTING = DATA / "hsk5_meaning_review_routing.json"

EXPECTED = 1600


def clean(value):
    return str(value or "").strip()


def score_record(record):
    meanings = record.get("candidateMeanings", [])
    if not isinstance(meanings, list):
        meanings = []

    meanings = [
        clean(x)
        for x in meanings
        if clean(x)
    ]

    word = clean(record.get("word"))
    pinyin = clean(record.get("pinyin"))
    selected = clean(record.get("selectedMeaningVi"))
    meaning = clean(record.get("meaningVi"))
    status = clean(record.get("generationStatus")).lower()
    source = clean(record.get("generationSource")).lower()

    score = 0
    reasons = []

    if word:
        score += 20
    else:
        reasons.append("missing Chinese word")

    if pinyin:
        score += 20
    else:
        reasons.append("missing pinyin")

    if meanings:
        score += 30
    else:
        reasons.append("no candidate meaning")

    if selected or meaning:
        score += 10
    else:
        reasons.append("missing selected/primary Vietnamese meaning")

    if len(meanings) <= 3:
        score += 5
    else:
        reasons.append("too many candidate meanings")

    if meaning and len(meaning) <= 120:
        score += 5
    elif meaning:
        reasons.append("Vietnamese meaning unusually long")

    # Reference-assisted candidates get a small structural confidence boost,
    # but are NEVER treated as verified ground truth.
    if "reference" in status or "reference" in source:
        score += 10
    elif "ai_assisted" in status or "ai-assisted" in status or "chatgpt" in source:
        score += 5

    if score >= 85:
        level = "HIGH"
        route = "LIGHT VERIFICATION"
    elif score >= 65:
        level = "MEDIUM"
        route = "FULL REVIEW"
    else:
        level = "LOW"
        route = "FULL REVIEW"

    if not reasons:
        reasons.append("candidate has complete structural meaning fields")

    return score, level, route, reasons


def main():
    print("=" * 72)
    print("HSK 5 MEANING CONFIDENCE / REVIEW ROUTING")
    print("=" * 72)
    print()

    if not INPUT.exists():
        raise SystemExit(f"Missing input: {INPUT}")

    records = json.loads(INPUT.read_text(encoding="utf-8"))

    if not isinstance(records, list) or len(records) != EXPECTED:
        raise SystemExit(
            f"Expected {EXPECTED} candidate records, got {len(records)}"
        )

    confidence = []
    review_queue = []

    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for record in records:
        score, level, route, reasons = score_record(record)
        counts[level] += 1

        item = {
            "id": record.get("id"),
            "word": record.get("word"),
            "pinyin": record.get("pinyin"),
            "confidenceScore": score,
            "confidenceLevel": level,
            "reviewRoute": route,
            "reasons": reasons,
            "autoApproved": False,
            "humanVerified": False,
            "verificationStatus": "unverified",
        }

        confidence.append(item)
        review_queue.append(item)

    routing = {
        "level": "HSK 5",
        "candidateRecords": len(records),
        "high": counts["HIGH"],
        "medium": counts["MEDIUM"],
        "low": counts["LOW"],
        "lightVerification": counts["HIGH"],
        "fullReview": counts["MEDIUM"] + counts["LOW"],
        "autoApproved": 0,
        "humanVerified": 0,
        "status": "completed",
        "important": [
            "No meanings were auto-approved.",
            "Translation accuracy is not independently verified.",
            "Reviewed and production data were not modified.",
        ],
    }

    DATA.mkdir(parents=True, exist_ok=True)

    CONFIDENCE.write_text(
        json.dumps(confidence, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    QUEUE.write_text(
        json.dumps(review_queue, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    ROUTING.write_text(
        json.dumps(routing, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Candidate records:       {len(records)}/{EXPECTED}")
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
