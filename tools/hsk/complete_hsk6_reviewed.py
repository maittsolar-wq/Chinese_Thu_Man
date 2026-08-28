#!/usr/bin/env python3
"""Complete the HSK 6 reviewed dataset from candidates.

This is a validation-stage completion step only.
It preserves existing reviewed records and fills missing reviewed records
from the candidate package. All AI-assisted meanings remain explicitly
unverified. No production data is created.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk6"
BASE = DATA / "hsk6_vocabulary_base.json"
CANDIDATES = DATA / "hsk6_meanings_candidates_input.json"
REVIEWED = DATA / "hsk6_vocabulary_reviewed.json"
REPORT = DATA / "hsk6_reviewed_completion_report.json"

EXPECTED = 1800


def candidate_meanings(record):
    values = record.get("candidateMeanings")
    if not isinstance(values, list):
        values = []
    values = [str(x).strip() for x in values if str(x).strip()]

    if not values and str(record.get("meaningVi") or "").strip():
        values = [str(record["meaningVi"]).strip()]

    return values


def main():
    print("=" * 72)
    print("HSK 6 REVIEWED DATA COMPLETION")
    print("=" * 72)
    print()

    for path in (BASE, CANDIDATES):
        if not path.exists():
            raise SystemExit(f"Missing required file: {path}")

    base = json.loads(BASE.read_text(encoding="utf-8"))
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))

    if len(base) != EXPECTED:
        raise SystemExit(f"Base records must be {EXPECTED}; got {len(base)}.")
    if len(candidates) != EXPECTED:
        raise SystemExit(
            f"Candidate records must be {EXPECTED}; got {len(candidates)}."
        )

    existing = {}
    if REVIEWED.exists():
        raw = json.loads(REVIEWED.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise SystemExit("Existing reviewed file must be a JSON array.")
        existing = {str(r.get("id")): r for r in raw if r.get("id")}

    candidate_by_id = {str(r.get("id")): r for r in candidates}
    output = []
    filled = 0
    preserved = 0
    missing = []

    for base_record in base:
        rid = str(base_record.get("id"))
        if rid in existing:
            output.append(existing[rid])
            preserved += 1
            continue

        candidate = candidate_by_id.get(rid)
        if not candidate:
            missing.append(rid)
            continue

        meanings = candidate_meanings(candidate)
        if not meanings:
            missing.append(rid)
            continue

        meaning = meanings[0]

        reviewed = dict(base_record)
        reviewed.update({
            "candidateMeanings": meanings,
            "meaningVi": meaning,
            "selectedMeaningVi": meaning,
            "generationSource": candidate.get(
                "generationSource", "AI-assisted"
            ),
            "generationStatus": candidate.get(
                "generationStatus", "ai_assisted"
            ),
            "verificationStatus": "unverified",
            "humanVerified": False,
            "groundTruth": False,
            "reviewStatus": "pending_validation",
        })

        output.append(reviewed)
        filled += 1

    DATA.mkdir(parents=True, exist_ok=True)
    REVIEWED.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report = {
        "baseRecords": len(base),
        "candidateRecords": len(candidates),
        "existingReviewedPreserved": preserved,
        "filledFromCandidates": filled,
        "finalReviewedFileRecords": len(output),
        "humanVerified": sum(
            1 for r in output if r.get("humanVerified") is True
        ),
        "aiAssistedUnverified": sum(
            1 for r in output
            if r.get("verificationStatus") == "unverified"
        ),
        "needsManualVerification": sum(
            1 for r in output
            if r.get("verificationStatus") == "unverified"
        ),
        "unresolvedIds": missing,
        "productionCreated": False,
    }

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Base records:                 {len(base)}/{EXPECTED}")
    print(f"Candidate records:            {len(candidates)}/{EXPECTED}")
    print(f"Existing reviewed preserved:  {preserved}")
    print(f"Filled from candidates:        {filled}")
    print(f"Final reviewed file records:   {len(output)}/{EXPECTED}")
    print(f"Human verified:                {report['humanVerified']}")
    print(f"AI-assisted unverified:        {report['aiAssistedUnverified']}")
    print(f"Needs manual verification:     {report['needsManualVerification']}")
    print(f"Output:                        {REVIEWED}")
    print(f"Report:                        {REPORT}")
    print()

    if missing or len(output) != EXPECTED:
        print("STATUS: FAIL")
        print("Unresolved IDs:")
        print(", ".join(missing[:50]))
        if len(missing) > 50:
            print(f"... and {len(missing) - 50} more")
        raise SystemExit(1)

    print("SUCCESS")
    print("HSK 6 reviewed dataset completed for validation.")
    print("No production data was created.")
    print("AI-assisted meanings remain explicitly unverified.")


if __name__ == "__main__":
    main()
