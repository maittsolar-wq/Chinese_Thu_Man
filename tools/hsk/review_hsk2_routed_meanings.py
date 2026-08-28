#!/usr/bin/env python3
"""Review HSK 2 Vietnamese meanings using the routed review queue.

Run from project root:
    python tools/hsk/review_hsk2_routed_meanings.py

Inputs:
    data/hsk/hsk2/hsk2_vocabulary_base.json
    data/hsk/hsk2/hsk2_meanings_candidates.json
    data/hsk/hsk2/hsk2_meaning_review_routing.json
    data/hsk/hsk2/hsk2_meaning_review_queue.json

Output:
    data/hsk/hsk2/hsk2_vocabulary_reviewed.json
    data/hsk/hsk2/hsk2_meaning_review_report.json

Review policy:
    HIGH    -> LIGHT VERIFICATION
    MEDIUM  -> FULL REVIEW
    LOW     -> FULL REVIEW

IMPORTANT:
- Nothing is auto-approved.
- This script does not create production data.
- It starts from the authoritative HSK 2 base record.
- HIGH still requires a human confirmation.
- MEDIUM/LOW require selecting/editing the meaning.
- The script supports resume.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk2"

BASE_FILE = DATA_DIR / "hsk2_vocabulary_base.json"
CANDIDATES_FILE = DATA_DIR / "hsk2_meanings_candidates.json"
ROUTING_FILE = DATA_DIR / "hsk2_meaning_review_routing.json"
QUEUE_FILE = DATA_DIR / "hsk2_meaning_review_queue.json"

OUTPUT_FILE = DATA_DIR / "hsk2_vocabulary_reviewed.json"
REPORT_FILE = DATA_DIR / "hsk2_meaning_review_report.json"

EXPECTED_COUNT = 200


def load_json(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {path}\n{exc}")


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


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


def normalize_meanings(values):
    result = []
    seen = set()

    for value in values:
        value = str(value).strip()

        if not value:
            continue

        key = value.casefold()

        if key not in seen:
            seen.add(key)
            result.append(value)

    return result


def show_record(item, position, total):
    print()
    print("=" * 76)
    print(f"HSK 2 ROUTED MEANING REVIEW [{position}/{total}]")
    print("=" * 76)
    print(f"ID:       {item['id']}")
    print(f"Chinese:  {item['word']}")
    print(f"Pinyin:   {item['pinyin']}")
    print(
        f"POS:      "
        f"{', '.join(item.get('partOfSpeech', []))}"
    )
    print(f"Routing:  {item['sourceRouting']}")
    print(f"Review:   {item['reviewType']}")
    print()
    print("Candidate meanings:")

    for index, meaning in enumerate(
        item.get("candidateMeanings", []),
        start=1,
    ):
        print(f"  {index}. {meaning}")

    print()

    if item["reviewType"] == "LIGHT_VERIFICATION":
        print("LIGHT VERIFICATION")
        print("  y       candidates look correct → approve")
        print("  n       candidates are not correct → edit")
        print("  c       enter corrected meaning(s)")
        print("  s       skip")
        print("  q       save and quit")
    else:
        print("FULL REVIEW")
        print("  1       select candidate 1")
        print("  1,2     select multiple candidates")
        print("  c       enter corrected meaning(s)")
        print("  s       skip")
        print("  q       save and quit")


def custom_meanings():
    print()
    print("Enter Vietnamese meanings separated by ';'.")
    print("Example: mua; mua sắm")

    while True:
        text = input("Meaning(s): ").strip()
        meanings = normalize_meanings(text.split(";"))

        if not meanings:
            print("Meaning cannot be empty.")
            continue

        print()
        for meaning in meanings:
            print(f"  - {meaning}")

        confirm = input("Confirm? [Y/n]: ").strip().casefold()

        if confirm in {"", "y", "yes"}:
            notes = input("Review note (optional): ").strip()
            return meanings, notes


def light_review(item):
    while True:
        choice = input("Your choice: ").strip().casefold()

        if choice in {"q", "quit", "exit"}:
            return "quit", None, ""

        if choice in {"s", "skip"}:
            return "skip", None, ""

        if choice in {"y", "yes"}:
            meanings = normalize_meanings(
                item.get("candidateMeanings", [])
            )

            if not meanings:
                print("No usable candidate meanings.")
                continue

            notes = input("Review note (optional): ").strip()
            return "approved", meanings, notes

        if choice in {"n", "no", "c", "custom"}:
            meanings, notes = custom_meanings()
            return "approved", meanings, notes

        print("Enter y, n, c, s, or q.")


def full_review(item):
    candidates = item.get("candidateMeanings", [])

    while True:
        choice = input("Your choice: ").strip().casefold()

        if choice in {"q", "quit", "exit"}:
            return "quit", None, ""

        if choice in {"s", "skip"}:
            return "skip", None, ""

        if choice in {"c", "custom"}:
            meanings, notes = custom_meanings()
            return "approved", meanings, notes

        parts = choice.replace(",", " ").split()

        if not parts:
            print("Enter a candidate number, c, s, or q.")
            continue

        indexes = []
        valid = True

        for part in parts:
            if not part.isdigit():
                valid = False
                break

            number = int(part)

            if number < 1 or number > len(candidates):
                valid = False
                break

            index = number - 1

            if index not in indexes:
                indexes.append(index)

        if not valid:
            print("Invalid candidate selection.")
            continue

        meanings = normalize_meanings(
            [candidates[index] for index in indexes]
        )

        print()
        print("Selected:")
        for meaning in meanings:
            print(f"  - {meaning}")

        confirm = input("Confirm? [Y/n]: ").strip().casefold()

        if confirm in {"", "y", "yes"}:
            notes = input("Review note (optional): ").strip()
            return "approved", meanings, notes


def build_reviewed_record(
    base_record,
    candidate_record,
    meanings,
    notes,
    review_type,
):
    # Base remains authoritative for vocabulary/source metadata.
    record = dict(base_record)

    record["meaningVi"] = meanings

    # Workflow fields intentionally retained until production build.
    record["candidateMeanings"] = list(
        candidate_record.get("candidateMeanings", [])
    )
    record["selectedMeaningVi"] = list(meanings)
    record["reviewNotes"] = notes
    record["reviewed"] = True
    record["reviewRequired"] = False
    record["status"] = "approved"
    record["reviewType"] = review_type

    return record


def build_report(reviewed, skipped, queue_count):
    light = sum(
        r.get("reviewType") == "LIGHT_VERIFICATION"
        for r in reviewed.values()
    )
    full = sum(
        r.get("reviewType") == "FULL_REVIEW"
        for r in reviewed.values()
    )

    return {
        "datasetName": "Chinese Thu Man HSK 2 Vietnamese Meanings",
        "status": (
            "REVIEW_COMPLETE"
            if len(reviewed) == EXPECTED_COUNT
            else "REVIEW_IN_PROGRESS"
        ),
        "level": 2,
        "recordCount": EXPECTED_COUNT,
        "reviewed": len(reviewed),
        "unreviewed": EXPECTED_COUNT - len(reviewed),
        "skipped": len(skipped),
        "queueRecords": queue_count,
        "reviewTypesCompleted": {
            "LIGHT_VERIFICATION": light,
            "FULL_REVIEW": full,
        },
        "productionCreated": False,
        "skippedIds": sorted(skipped),
    }


def main():
    print("=" * 76)
    print("HSK 2 ROUTED MEANING REVIEW")
    print("=" * 76)
    print()

    base = index_by_id(
        load_json(BASE_FILE),
        "HSK 2 base",
    )
    candidates = index_by_id(
        load_json(CANDIDATES_FILE),
        "HSK 2 candidates",
    )

    routing = load_json(ROUTING_FILE)
    queue = load_json(QUEUE_FILE)

    if routing.get("status") != "ROUTING_COMPLETE":
        raise SystemExit(
            "Routing report is not ROUTING_COMPLETE."
        )

    if queue.get("status") != "REVIEW_QUEUE_READY":
        raise SystemExit(
            "Review queue is not REVIEW_QUEUE_READY."
        )

    queue_records = queue.get("records")

    if not isinstance(queue_records, list):
        raise SystemExit(
            "Review queue is missing its records array."
        )

    if len(queue_records) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} queue records, "
            f"got {len(queue_records)}."
        )

    existing = {}

    if OUTPUT_FILE.exists():
        previous = load_json(OUTPUT_FILE)

        if isinstance(previous, list):
            existing = index_by_id(
                previous,
                "existing reviewed data",
            )

    # Only retain actually reviewed records with a non-empty meaning.
    reviewed = {
        record_id: record
        for record_id, record in existing.items()
        if record.get("reviewed") is True
        and record.get("meaningVi")
    }

    print(f"Queue records:    {len(queue_records)}/{EXPECTED_COUNT}")
    print(f"Already reviewed: {len(reviewed)}")
    print(f"Remaining:        {EXPECTED_COUNT - len(reviewed)}")
    print()
    print("Base data will NOT be modified.")
    print("Production data will NOT be created.")
    print()

    skipped = set()

    # Queue is already priority ordered by the routing script.
    for position, item in enumerate(queue_records, start=1):
        record_id = item["id"]

        if record_id in reviewed:
            continue

        candidate = candidates.get(record_id)
        base_record = base.get(record_id)

        if candidate is None:
            raise SystemExit(
                f"Missing candidate record for {record_id}."
            )

        if base_record is None:
            raise SystemExit(
                f"Missing base record for {record_id}."
            )

        show_record(
            item,
            position,
            EXPECTED_COUNT,
        )

        if item["reviewType"] == "LIGHT_VERIFICATION":
            result, meanings, notes = light_review(item)
        else:
            result, meanings, notes = full_review(item)

        if result == "quit":
            save_json(
                OUTPUT_FILE,
                sorted(
                    reviewed.values(),
                    key=lambda r: r["id"],
                ),
            )

            report = build_report(
                reviewed,
                skipped,
                len(queue_records),
            )
            report["quitEarly"] = True
            save_json(REPORT_FILE, report)

            print()
            print("Progress saved.")
            print(f"Reviewed: {len(reviewed)}/{EXPECTED_COUNT}")
            print(f"Output:   {OUTPUT_FILE}")
            print(f"Report:   {REPORT_FILE}")
            return

        if result == "skip":
            skipped.add(record_id)
            continue

        reviewed[record_id] = build_reviewed_record(
            base_record=base_record,
            candidate_record=candidate,
            meanings=meanings,
            notes=notes,
            review_type=item["reviewType"],
        )

        # Save after every approved record so progress is never lost.
        save_json(
            OUTPUT_FILE,
            sorted(
                reviewed.values(),
                key=lambda r: r["id"],
            ),
        )

        save_json(
            REPORT_FILE,
            build_report(
                reviewed,
                skipped,
                len(queue_records),
            ),
        )

    save_json(
        OUTPUT_FILE,
        sorted(
            reviewed.values(),
            key=lambda r: r["id"],
        ),
    )

    report = build_report(
        reviewed,
        skipped,
        len(queue_records),
    )
    report["quitEarly"] = False
    save_json(REPORT_FILE, report)

    print()
    print("=" * 76)
    print("HSK 2 ROUTED MEANING REVIEW FINISHED")
    print("=" * 76)
    print(f"Reviewed: {len(reviewed)}/{EXPECTED_COUNT}")
    print(f"Skipped:  {len(skipped)}")
    print(f"Output:   {OUTPUT_FILE}")
    print(f"Report:   {REPORT_FILE}")
    print()

    if len(reviewed) == EXPECTED_COUNT:
        print(
            "All 200 records have been human-verified."
        )
        print(
            "Next step: reviewed-data validation."
        )
    else:
        print(
            "Review is incomplete; resume by running the script again."
        )

    print("Production data was NOT created.")


if __name__ == "__main__":
    main()
