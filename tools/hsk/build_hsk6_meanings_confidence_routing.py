#!/usr/bin/env python3
"""HSK 6 meaning confidence / review routing.

Reads:
    data/hsk/hsk6/hsk6_meanings_candidates_input.json

Writes:
    hsk6_meanings_confidence.json
    hsk6_meanings_review_queue.json
    hsk6_meaning_review_routing.json

No meanings are auto-approved. No reviewed or production data is modified.
"""

from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk6"
INPUT = DATA / "hsk6_meanings_candidates_input.json"
CONFIDENCE = DATA / "hsk6_meanings_confidence.json"
QUEUE = DATA / "hsk6_meanings_review_queue.json"
ROUTING = DATA / "hsk6_meaning_review_routing.json"
EXPECTED = 1800

def meaning_list(r):
    vals = r.get("candidateMeanings")
    if not isinstance(vals, list):
        vals = []
    vals = [str(x).strip() for x in vals if str(x).strip()]
    if not vals and str(r.get("meaningVi") or "").strip():
        vals = [str(r["meaningVi"]).strip()]
    return vals

def score(r):
    meanings = meaning_list(r)
    score = 0
    reasons = []

    if meanings:
        score += 60
    else:
        reasons.append("no meaning candidate")

    if len(meanings) == 1:
        score += 20
    elif len(meanings) > 1:
        score += 10
        reasons.append("multiple meaning candidates")

    source = str(r.get("generationSource") or "").lower()
    status = str(r.get("generationStatus") or "").lower()

    if "reference" in source or status == "reference_assisted":
        score += 20
    elif "ai" in source or "ai" in status:
        score += 5
        reasons.append("AI-assisted meaning")
    else:
        reasons.append("unknown generation source")

    if r.get("humanVerified") is True:
        score += 20
    else:
        reasons.append("not human verified")

    # Structural confidence is deliberately conservative: AI-assisted
    # meanings remain unverified even when their structural score is high.
    if score >= 85:
        level = "HIGH"
        route = "LIGHT_VERIFICATION"
    elif score >= 60:
        level = "MEDIUM"
        route = "FULL_REVIEW"
    else:
        level = "LOW"
        route = "FULL_REVIEW"

    return score, level, route, reasons

def main():
    print("=" * 72)
    print("HSK 6 MEANING CONFIDENCE / REVIEW ROUTING")
    print("=" * 72)
    print()

    if not INPUT.exists():
        raise SystemExit(f"Missing input: {INPUT}")

    records = json.loads(INPUT.read_text(encoding="utf-8"))
    if not isinstance(records, list) or len(records) != EXPECTED:
        raise SystemExit(
            f"Expected {EXPECTED} candidate records, got {len(records) if isinstance(records,list) else 'invalid'}."
        )

    confidence = []
    queue = []
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    routes = {"LIGHT_VERIFICATION": 0, "FULL_REVIEW": 0}

    for r in records:
        score_value, level, route, reasons = score(r)
        item = {
            "id": r.get("id"),
            "word": r.get("word"),
            "pinyin": r.get("pinyin"),
            "confidenceScore": score_value,
            "confidence": level,
            "reviewRoute": route,
            "reasons": reasons,
            "humanVerified": False,
            "verificationStatus": "unverified",
            "autoApproved": False,
        }
        confidence.append(item)
        counts[level] += 1
        routes[route] += 1

        # Every unverified candidate is retained in the review queue.
        queue.append({
            **item,
            "meaningVi": r.get("meaningVi", ""),
            "candidateMeanings": meaning_list(r),
            "generationSource": r.get("generationSource", ""),
        })

    DATA.mkdir(parents=True, exist_ok=True)
    CONFIDENCE.write_text(
        json.dumps(confidence, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    QUEUE.write_text(
        json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    report = {
        "candidateRecords": len(records),
        "confidence": counts,
        "routing": routes,
        "humanVerified": 0,
        "autoApproved": 0,
        "productionCreated": False,
        "allMeaningsUnverified": True,
    }
    ROUTING.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Candidate records:       {len(records)}/{EXPECTED}")
    print(f"HIGH:                    {counts['HIGH']}")
    print(f"MEDIUM:                  {counts['MEDIUM']}")
    print(f"LOW:                     {counts['LOW']}")
    print()
    print(f"LIGHT VERIFICATION:      {routes['LIGHT_VERIFICATION']}")
    print(f"FULL REVIEW:             {routes['FULL_REVIEW']}")
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
    print("- AI-assisted meanings remain explicitly unverified.")
    print("- Human verified: 0.")
    print("- No reviewed or production data was modified.")

if __name__ == "__main__":
    main()
