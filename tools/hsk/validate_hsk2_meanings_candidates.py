#!/usr/bin/env python3
"""Validate HSK 2 Vietnamese meaning candidates before review.

Run from project root:
    python tools/hsk/validate_hsk2_meanings_candidates.py

Inputs:
    data/hsk/hsk2/hsk2_vocabulary_base.json
    data/hsk/hsk2/hsk2_meanings_candidates.json
    data/hsk/hsk2/hsk2_meanings_confidence.json

Output:
    data/hsk/hsk2/hsk2_meanings_candidates_validation.json

This validates structural integrity and consistency only.
It does NOT verify translation accuracy and does NOT approve meanings
for production.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk2"

BASE_FILE = DATA_DIR / "hsk2_vocabulary_base.json"
CANDIDATES_FILE = DATA_DIR / "hsk2_meanings_candidates.json"
CONFIDENCE_FILE = DATA_DIR / "hsk2_meanings_confidence.json"
OUTPUT_FILE = DATA_DIR / "hsk2_meanings_candidates_validation.json"

EXPECTED_COUNT = 200
VALID_ROUTES = {"HIGH", "MEDIUM", "LOW"}

CHINESE_RE = re.compile(r"[\u3400-\u9fff]")


def load_json(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def index_by_id(records, label):
    if not isinstance(records, list):
        raise SystemExit(f"{label} must be a JSON array.")

    result = {}

    for record in records:
        if not isinstance(record, dict):
            raise SystemExit(f"{label} contains a non-object record.")

        record_id = record.get("id")

        if not record_id:
            raise SystemExit(f"{label} contains a record without id.")

        if record_id in result:
            raise SystemExit(
                f"Duplicate ID in {label}: {record_id}"
            )

        result[record_id] = record

    return result


def main():
    print("=" * 72)
    print("HSK 2 MEANING CANDIDATES VALIDATION")
    print("=" * 72)
    print()

    base = load_json(BASE_FILE)
    candidates = load_json(CANDIDATES_FILE)
    confidence = load_json(CONFIDENCE_FILE)

    base_by_id = index_by_id(base, "HSK 2 base")
    candidate_by_id = index_by_id(
        candidates,
        "HSK 2 meaning candidates",
    )

    confidence_records = confidence.get("records")

    if not isinstance(confidence_records, list):
        raise SystemExit(
            "Confidence report is missing a valid 'records' array."
        )

    confidence_by_id = index_by_id(
        confidence_records,
        "HSK 2 confidence records",
    )

    errors = []
    warnings = []

    expected_ids = {
        f"hsk2_{i:03d}"
        for i in range(1, EXPECTED_COUNT + 1)
    }

    for label, mapping in (
        ("base", base_by_id),
        ("candidates", candidate_by_id),
        ("confidence", confidence_by_id),
    ):
        if len(mapping) != EXPECTED_COUNT:
            errors.append(
                f"{label}: expected {EXPECTED_COUNT} records, "
                f"got {len(mapping)}."
            )

        missing = expected_ids - set(mapping)
        extra = set(mapping) - expected_ids

        if missing:
            errors.append(
                f"{label}: missing IDs: "
                + ", ".join(sorted(missing))
            )

        if extra:
            errors.append(
                f"{label}: unexpected IDs: "
                + ", ".join(sorted(extra))
            )

    for record_id in sorted(expected_ids):
        base_record = base_by_id.get(record_id)
        candidate = candidate_by_id.get(record_id)
        confidence_record = confidence_by_id.get(record_id)

        if not base_record or not candidate or not confidence_record:
            continue

        # Candidate identity must match the authoritative base.
        for field in (
            "word",
            "pinyin",
            "sourceSort",
            "introducedLevel",
        ):
            base_value = base_record.get(field)
            candidate_value = candidate.get(field)

            if candidate_value != base_value:
                errors.append(
                    f"{record_id}: candidate {field} does not match base "
                    f"({candidate_value!r} != {base_value!r})."
                )

        word = candidate.get("word", "")

        if not isinstance(word, str) or not word.strip():
            errors.append(
                f"{record_id}: empty Chinese word."
            )
        elif not CHINESE_RE.search(word):
            errors.append(
                f"{record_id}: word does not contain Chinese characters."
            )

        pinyin = candidate.get("pinyin")

        if not isinstance(pinyin, str) or not pinyin.strip():
            errors.append(
                f"{record_id}: empty Pinyin."
            )

        meanings = candidate.get("candidateMeanings")

        if not isinstance(meanings, list) or not meanings:
            errors.append(
                f"{record_id}: candidateMeanings is empty."
            )
            continue

        cleaned = []

        for meaning in meanings:
            if not isinstance(meaning, str):
                errors.append(
                    f"{record_id}: candidate meaning is not a string."
                )
                continue

            value = meaning.strip()

            if not value:
                errors.append(
                    f"{record_id}: candidate meaning is empty."
                )
                continue

            cleaned.append(value)

        if len(cleaned) != len(set(x.casefold() for x in cleaned)):
            errors.append(
                f"{record_id}: duplicate candidate meanings."
            )

        if candidate.get("generationStatus") != "generated":
            errors.append(
                f"{record_id}: generationStatus is not 'generated'."
            )

        # A candidate package must not contain reviewed/production state.
        forbidden_review_fields = (
            "selectedMeaningVi",
            "reviewed",
            "reviewNotes",
            "status",
            "meaningVi",
            "autoApproved",
        )

        for field in forbidden_review_fields:
            if field in candidate:
                errors.append(
                    f"{record_id}: forbidden review/production field "
                    f"present: {field}."
                )

        confidence_route = confidence_record.get("routing")

        if confidence_route not in VALID_ROUTES:
            errors.append(
                f"{record_id}: invalid routing: "
                f"{confidence_route!r}."
            )

        if confidence_record.get("autoApproved") is not False:
            errors.append(
                f"{record_id}: autoApproved must be false."
            )

        if confidence_record.get("word") != base_record.get("word"):
            errors.append(
                f"{record_id}: confidence word does not match base."
            )

        if confidence_record.get("pinyin") != base_record.get("pinyin"):
            errors.append(
                f"{record_id}: confidence Pinyin does not match base."
            )

        confidence_meanings = confidence_record.get(
            "candidateMeanings"
        )

        if confidence_meanings != meanings:
            errors.append(
                f"{record_id}: confidence candidates do not match "
                "candidate package."
            )

    route_counts = {
        route: sum(
            r.get("routing") == route
            for r in confidence_by_id.values()
        )
        for route in sorted(VALID_ROUTES)
    }

    if sum(route_counts.values()) != EXPECTED_COUNT:
        errors.append(
            "Confidence routing does not cover all 200 records."
        )

    if route_counts["LOW"] == 0:
        warnings.append(
            "No LOW records were routed. This is not an accuracy guarantee."
        )

    warnings.append(
        "Candidate validation checks structure/consistency only; "
        "translation accuracy is not independently verified."
    )

    report = {
        "status": "PASS" if not errors else "FAIL",
        "level": 2,
        "expectedRecords": EXPECTED_COUNT,
        "actualRecords": len(candidate_by_id),
        "errors": errors,
        "warnings": warnings,
        "routingCounts": route_counts,
        "translationAccuracyVerified": False,
        "productionApproved": False,
        "checks": {
            "recordCount": len(candidate_by_id) == EXPECTED_COUNT,
            "ids": not any(
                "IDs" in error or "missing IDs" in error
                or "unexpected IDs" in error
                for error in errors
            ),
            "baseConsistency": not any(
                "does not match base" in error
                for error in errors
            ),
            "candidateMeanings": not any(
                "candidateMeanings is empty" in error
                or "candidate meaning" in error
                or "duplicate candidate meanings" in error
                for error in errors
            ),
            "generationStatus": not any(
                "generationStatus" in error
                for error in errors
            ),
            "routing": not any(
                "routing" in error
                for error in errors
            ),
            "noAutoApproval": not any(
                "autoApproved" in error
                for error in errors
            ),
            "noReviewState": not any(
                "forbidden review/production field" in error
                for error in errors
            ),
        },
    }

    OUTPUT_FILE.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Candidate records: {len(candidate_by_id)}/{EXPECTED_COUNT}")
    print(f"Errors:             {len(errors)}")
    print(f"Warnings:           {len(warnings)}")
    print()
    print(
        "Routing: "
        f"HIGH={route_counts['HIGH']}  "
        f"MEDIUM={route_counts['MEDIUM']}  "
        f"LOW={route_counts['LOW']}"
    )
    print()
    print(f"Report: {OUTPUT_FILE}")
    print()

    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  [FAIL] {error}")
        print()
        print("Status: FAIL")
        raise SystemExit(1)

    print("Status: PASS")
    print()
    print(
        "PASS: HSK 2 meaning candidates are structurally consistent."
    )
    print(
        "Translation accuracy is NOT independently verified."
    )
    print(
        "No reviewed or production data was modified."
    )


if __name__ == "__main__":
    main()
