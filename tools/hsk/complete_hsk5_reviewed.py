#!/usr/bin/env python3
"""Complete HSK 5 reviewed dataset from the 1600 candidate records.

Preserves existing reviewed records if present, fills missing reviewed records
from candidate meanings, and explicitly keeps AI-assisted meanings unverified.
Does not create production data.
"""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk5"
BASE = DATA / "hsk5_vocabulary_base.json"
CANDIDATES = DATA / "hsk5_meanings_candidates_input.json"
REVIEWED = DATA / "hsk5_vocabulary_reviewed.json"
REPORT = DATA / "hsk5_reviewed_completion_report.json"
EXPECTED = 1600


def main():
    print("=" * 72)
    print("HSK 5 REVIEWED DATA COMPLETION")
    print("=" * 72)
    print()

    if not BASE.exists():
        raise SystemExit(f"Missing base: {BASE}")
    if not CANDIDATES.exists():
        raise SystemExit(f"Missing candidates: {CANDIDATES}")

    base = json.loads(BASE.read_text(encoding="utf-8"))
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))

    if len(base) != EXPECTED:
        raise SystemExit(f"Base expected {EXPECTED}, got {len(base)}")
    if len(candidates) != EXPECTED:
        raise SystemExit(f"Candidates expected {EXPECTED}, got {len(candidates)}")

    existing = []
    if REVIEWED.exists():
        existing = json.loads(REVIEWED.read_text(encoding="utf-8"))
        if not isinstance(existing, list):
            raise SystemExit("Existing reviewed root must be a JSON array.")

    reviewed_by_id = {
        r.get("id"): r for r in existing if isinstance(r, dict) and r.get("id")
    }
    candidate_by_id = {r.get("id"): r for r in candidates}

    filled = 0
    preserved = 0
    human_verified = 0
    ai_unverified = 0
    unresolved = []

    final = []

    for b in base:
        rid = b["id"]
        r = reviewed_by_id.get(rid)

        if r is not None:
            preserved += 1
            item = dict(r)
        else:
            c = candidate_by_id.get(rid)
            if c is None:
                unresolved.append(rid)
                item = dict(b)
            else:
                item = dict(b)
                meanings = c.get("candidateMeanings", [])
                meanings = [
                    str(x).strip() for x in meanings
                    if isinstance(x, str) and x.strip()
                ]
                if not meanings:
                    unresolved.append(rid)
                else:
                    meaning = str(
                        c.get("selectedMeaningVi")
                        or c.get("meaningVi")
                        or meanings[0]
                    ).strip()
                    item["candidateMeanings"] = meanings
                    item["meaningVi"] = meaning
                    item["selectedMeaningVi"] = meaning
                    item["generationStatus"] = c.get(
                        "generationStatus",
                        "ai_assisted_unverified",
                    )
                    item["generationSource"] = c.get(
                        "generationSource",
                        "AI-assisted",
                    )
                    item["verificationStatus"] = "unverified"
                    item["humanVerified"] = False
                    filled += 1

        hv = bool(item.get("humanVerified"))
        if hv:
            human_verified += 1
        else:
            ai_unverified += 1

        final.append(item)

    REVIEWED.write_text(
        json.dumps(final, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report = {
        "baseRecords": len(base),
        "candidateRecords": len(candidates),
        "existingReviewedPreserved": preserved,
        "filledFromCandidates": filled,
        "finalReviewedFileRecords": len(final),
        "humanVerified": human_verified,
        "aiAssistedUnverified": ai_unverified,
        "unresolvedIds": unresolved,
        "productionCreated": False,
        "status": "SUCCESS" if len(final) == EXPECTED and not unresolved else "INCOMPLETE",
    }

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Base records:                 {len(base)}/{EXPECTED}")
    print(f"Candidate records:            {len(candidates)}/{EXPECTED}")
    print(f"Existing reviewed preserved:  {preserved}")
    print(f"Filled from candidates:       {filled}")
    print(f"Final reviewed file records:  {len(final)}/{EXPECTED}")
    print(f"Human verified:               {human_verified}")
    print(f"AI-assisted unverified:       {ai_unverified}")
    print(f"Output:                       {REVIEWED}")
    print(f"Report:                       {REPORT}")
    print()
    print("SUCCESS" if report["status"] == "SUCCESS" else "INCOMPLETE")
    print("HSK 5 reviewed dataset completed for validation.")
    print("No production data was created.")
    print("AI-assisted meanings remain explicitly unverified.")

    if unresolved:
        print()
        print("Unresolved IDs:")
        print(", ".join(unresolved))


if __name__ == "__main__":
    main()
