#!/usr/bin/env python3
"""Score HSK 2 Vietnamese meaning candidates for review routing.

Run from project root:
    python tools/hsk/score_hsk2_meaning_candidates.py

Input:
    data/hsk/hsk2/hsk2_meanings_candidates.json

Output:
    data/hsk/hsk2/hsk2_meanings_confidence.json
    data/hsk/hsk2/hsk2_meanings_review_queue.json

Important:
- This is a DETERMINISTIC routing aid, not a truth detector.
- It does not call an AI API.
- It does not modify base, reviewed, or production data.
- It does not auto-approve meanings.
- HIGH/MEDIUM/LOW are routing labels only.
- Because HSK 2 candidates in the current workflow were generated without
  an external reference source, the scorer is deliberately conservative:
  records are routed using structural quality signals, not treated as verified
  Vietnamese translations.

The output is designed so a later calibrated model/reference source can replace
or augment these signals without changing the review/production contract.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk2"

INPUT_FILE = DATA_DIR / "hsk2_meanings_candidates.json"
CONFIDENCE_FILE = DATA_DIR / "hsk2_meanings_confidence.json"
QUEUE_FILE = DATA_DIR / "hsk2_meanings_review_queue.json"

EXPECTED_COUNT = 200

VIETNAMESE_RE = re.compile(
    r"[A-Za-zÀ-ỹĐđ]"
)

# Common signs that a candidate is more than a simple Vietnamese meaning,
# or contains meta/explanatory text that should not be treated as a clean
# dictionary gloss.
META_TERMS = (
    "trợ từ",
    "lượng từ",
    "biểu thị",
    "dùng để",
    "thành phần",
)


def load_json(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {path}\n{exc}")


def score_candidate(meanings):
    """
    Structural quality score only.

    Signals:
      + valid non-empty list
      + each meaning is a Vietnamese-looking string
      + duplicate removal
      + reasonable number of meanings
      - meta/explanatory wording

    This MUST NOT be interpreted as translation accuracy.
    """
    reasons = []
    score = 0.0

    if not isinstance(meanings, list) or not meanings:
        return 0.0, ["candidateMeanings is empty or invalid"]

    cleaned = [
        str(x).strip()
        for x in meanings
        if isinstance(x, str) and x.strip()
    ]

    if not cleaned:
        return 0.0, ["no usable meaning strings"]

    if len(cleaned) == len(meanings):
        score += 0.20
    else:
        reasons.append("contains empty/non-string candidates")

    lowered = [x.casefold() for x in cleaned]

    if len(lowered) == len(set(lowered)):
        score += 0.15
    else:
        reasons.append("duplicate candidate meaning")

    if 1 <= len(cleaned) <= 5:
        score += 0.15
    else:
        reasons.append("unusually many candidate meanings")

    vietnamese_like = 0
    for meaning in cleaned:
        if VIETNAMESE_RE.search(meaning):
            vietnamese_like += 1

    if vietnamese_like == len(cleaned):
        score += 0.20
    else:
        reasons.append("one or more candidates do not look textual")

    meta_count = sum(
        any(term in meaning.casefold() for term in META_TERMS)
        for meaning in cleaned
    )

    if meta_count == 0:
        score += 0.15
    else:
        reasons.append(
            "contains grammatical/meta explanation rather than a clean gloss"
        )

    avg_length = sum(len(x) for x in cleaned) / len(cleaned)

    if 1 <= avg_length <= 40:
        score += 0.15
    else:
        reasons.append("candidate text is unusually long")

    return round(min(score, 1.0), 2), reasons


def route(score, reasons):
    """
    Conservative routing.

    No record is considered production-safe from this structural score alone.
    HIGH means structurally clean and suitable for a lighter review route,
    not automatically correct.
    """
    if score >= 0.90 and not reasons:
        return "HIGH"

    if score >= 0.70:
        return "MEDIUM"

    return "LOW"


def main():
    print("=" * 72)
    print("HSK 2 MEANING CONFIDENCE / REVIEW ROUTING")
    print("=" * 72)
    print()

    candidates = load_json(INPUT_FILE)

    if not isinstance(candidates, list):
        raise SystemExit("Candidate dataset must be a JSON array.")

    if len(candidates) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} candidate records, "
            f"got {len(candidates)}."
        )

    seen_ids = set()
    scored = []
    queue = []

    for record in candidates:
        if not isinstance(record, dict):
            raise SystemExit("Candidate dataset contains a non-object record.")

        record_id = record.get("id")

        if not record_id:
            raise SystemExit("Candidate record missing id.")

        if record_id in seen_ids:
            raise SystemExit(f"Duplicate candidate ID: {record_id}")

        seen_ids.add(record_id)

        meanings = record.get("candidateMeanings", [])

        score, reasons = score_candidate(meanings)
        level = route(score, reasons)

        scored_record = {
            "id": record_id,
            "word": record.get("word"),
            "pinyin": record.get("pinyin"),
            "partOfSpeech": record.get("partOfSpeech", []),
            "candidateMeanings": meanings,
            "structuralScore": score,
            "routing": level,
            "reasons": reasons,
            "autoApproved": False,
        }

        scored.append(scored_record)

        # All records remain review-eligible. HIGH only means the record
        # passed structural checks; it is NOT production approval.
        queue.append(
            {
                "id": record_id,
                "routing": level,
                "priority": (
                    1 if level == "LOW"
                    else 2 if level == "MEDIUM"
                    else 3
                ),
                "reason": (
                    " / ".join(reasons)
                    if reasons
                    else "Structurally clean candidate; translation accuracy still requires verification."
                ),
            }
        )

    counts = {
        "HIGH": sum(r["routing"] == "HIGH" for r in scored),
        "MEDIUM": sum(r["routing"] == "MEDIUM" for r in scored),
        "LOW": sum(r["routing"] == "LOW" for r in scored),
    }

    report = {
        "datasetName": "Chinese Thu Man HSK 2 Meaning Candidate Routing",
        "status": "ROUTING_COMPLETE",
        "level": 2,
        "recordCount": len(scored),
        "routing": counts,
        "method": {
            "type": "deterministic_structural_scoring",
            "translationAccuracyVerified": False,
            "autoApprovalAllowed": False,
            "notes": (
                "Scores are routing aids only. They are not evidence that "
                "a Vietnamese meaning is correct."
            ),
        },
        "records": scored,
    }

    queue.sort(key=lambda item: (item["priority"], item["id"]))

    queue_report = {
        "datasetName": "Chinese Thu Man HSK 2 Meaning Review Queue",
        "status": "REVIEW_QUEUE_READY",
        "level": 2,
        "recordCount": len(queue),
        "counts": counts,
        "records": queue,
    }

    CONFIDENCE_FILE.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    QUEUE_FILE.write_text(
        json.dumps(queue_report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Candidate records: {len(scored)}/{EXPECTED_COUNT}")
    print(f"HIGH:               {counts['HIGH']}")
    print(f"MEDIUM:             {counts['MEDIUM']}")
    print(f"LOW:                {counts['LOW']}")
    print()
    print(f"Confidence report:  {CONFIDENCE_FILE}")
    print(f"Review queue:       {QUEUE_FILE}")
    print()
    print("SUCCESS")
    print("Routing completed.")
    print()
    print("IMPORTANT:")
    print("- No AI API was called.")
    print("- No automatic production approval was performed.")
    print("- Base, reviewed, and production data were not modified.")


if __name__ == "__main__":
    main()
