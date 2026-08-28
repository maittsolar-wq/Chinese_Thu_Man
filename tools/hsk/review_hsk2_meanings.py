#!/usr/bin/env python3
"""
Review HSK 2 Vietnamese meaning candidates.

Workflow:
    hsk2_vocabulary_base.json
        -> hsk2_meanings_candidates.json
        -> THIS SCRIPT (human review)
        -> hsk2_vocabulary_reviewed.json

This script:
- Reads AI/generated candidate meanings only.
- Keeps the HSK 2 base dataset unchanged.
- Lets the reviewer select one or more candidates, edit them, or enter a custom meaning.
- Writes a separate reviewed dataset.
- Never writes production data.
- Supports resume: existing reviewed records are skipped unless --redo is used.

Run from project root:
    python tools/hsk/review_hsk2_meanings.py

Optional:
    python tools/hsk/review_hsk2_meanings.py --redo
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk2"

INPUT_FILE = DATA_DIR / "hsk2_meanings_candidates.json"
BASE_FILE = DATA_DIR / "hsk2_vocabulary_base.json"
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


def validate_input(records):
    if not isinstance(records, list):
        raise SystemExit("Input must be a JSON array.")

    if len(records) != EXPECTED_COUNT:
        raise SystemExit(
            f"Expected {EXPECTED_COUNT} candidate records, "
            f"got {len(records)}."
        )

    seen_ids = set()

    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise SystemExit(f"Record #{index} is not an object.")

        record_id = record.get("id")
        word = str(record.get("word", "")).strip()
        pinyin = str(record.get("pinyin", "")).strip()
        candidates = record.get("candidateMeanings")

        if not record_id:
            raise SystemExit(f"Record #{index}: missing id.")

        if record_id in seen_ids:
            raise SystemExit(f"Duplicate ID: {record_id}")

        seen_ids.add(record_id)

        if not word:
            raise SystemExit(f"{record_id}: empty word.")

        if not pinyin:
            raise SystemExit(f"{record_id}: empty Pinyin.")

        if not isinstance(candidates, list) or not candidates:
            raise SystemExit(
                f"{record_id}: candidateMeanings must be a non-empty list."
            )

        if any(
            not isinstance(item, str) or not item.strip()
            for item in candidates
        ):
            raise SystemExit(
                f"{record_id}: candidateMeanings contains an invalid item."
            )


def validate_base(base_records):
    if not isinstance(base_records, list):
        raise SystemExit("HSK 2 base must be a JSON array.")

    if len(base_records) != EXPECTED_COUNT:
        raise SystemExit(
            f"HSK 2 base has {len(base_records)} records; "
            f"expected {EXPECTED_COUNT}."
        )

    base_by_id = {}

    for record in base_records:
        if not isinstance(record, dict):
            raise SystemExit("HSK 2 base contains a non-object record.")

        record_id = record.get("id")

        if not record_id:
            raise SystemExit("HSK 2 base contains a record without id.")

        if record_id in base_by_id:
            raise SystemExit(f"Duplicate base ID: {record_id}")

        base_by_id[record_id] = record

    return base_by_id


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


def parse_selection(text, candidate_count):
    """
    Accept:
        1
        1,3
        1 3
        all
        c
        custom
        s
        skip
        q
        quit
    """
    normalized = text.strip().casefold()

    if normalized in {"q", "quit", "exit"}:
        return "quit"

    if normalized in {"s", "skip"}:
        return "skip"

    if normalized in {"c", "custom"}:
        return "custom"

    if normalized == "all":
        return list(range(candidate_count))

    raw_parts = normalized.replace(",", " ").split()

    if not raw_parts:
        return None

    indexes = []

    for part in raw_parts:
        if not part.isdigit():
            return None

        number = int(part)

        if number < 1 or number > candidate_count:
            return None

        index = number - 1

        if index not in indexes:
            indexes.append(index)

    return indexes


def review_record(record, position, total):
    word = record["word"]
    pinyin = record["pinyin"]
    pos = record.get("partOfSpeechSource") or ", ".join(
        record.get("partOfSpeech", [])
    )
    candidates = record["candidateMeanings"]

    print()
    print("=" * 72)
    print(f"HSK 2 MEANING REVIEW  [{position}/{total}]")
    print("=" * 72)
    print(f"ID:       {record['id']}")
    print(f"Chinese:  {word}")
    print(f"Pinyin:   {pinyin}")
    print(f"POS:      {pos}")
    print()
    print("Candidate meanings:")

    for index, meaning in enumerate(candidates, start=1):
        print(f"  {index}. {meaning}")

    print()
    print("Commands:")
    print("  1          select one candidate")
    print("  1,3        select multiple candidates")
    print("  all        select all candidates")
    print("  c          enter custom Vietnamese meaning(s)")
    print("  s          skip for now")
    print("  q          save and quit")

    while True:
        choice = input("\nYour choice: ").strip()

        selection = parse_selection(choice, len(candidates))

        if selection == "quit":
            return "quit", None, ""

        if selection == "skip":
            return "skip", None, ""

        if selection == "custom":
            return get_custom_meanings()

        if isinstance(selection, list):
            selected = [candidates[i] for i in selection]
            selected = normalize_meanings(selected)

            if not selected:
                print("No valid meaning selected.")
                continue

            print()
            print("Selected:")
            for meaning in selected:
                print(f"  - {meaning}")

            confirm = input("Confirm? [Y/n]: ").strip().casefold()

            if confirm in {"", "y", "yes"}:
                return "approved", selected, ""

            continue

        print("Invalid choice. Please enter a candidate number, c, s, or q.")


def get_custom_meanings():
    print()
    print("Enter Vietnamese meanings separated by ';'.")
    print("Example: giúp; giúp đỡ")

    while True:
        text = input("Custom meaning(s): ").strip()

        meanings = normalize_meanings(text.split(";"))

        if not meanings:
            print("Meaning cannot be empty.")
            continue

        print()
        print("Custom meanings:")
        for meaning in meanings:
            print(f"  - {meaning}")

        confirm = input("Confirm? [Y/n]: ").strip().casefold()

        if confirm in {"", "y", "yes"}:
            notes = input("Review note (optional): ").strip()
            return "approved", meanings, notes


def build_reviewed_record(candidate, base_record, meanings, notes):
    """
    Start from BASE so source vocabulary facts remain authoritative.
    Only meaning/review workflow fields are added.
    """
    record = dict(base_record)

    record["meaningVi"] = meanings
    record["candidateMeanings"] = list(candidate["candidateMeanings"])
    record["selectedMeaningVi"] = list(meanings)
    record["reviewNotes"] = notes
    record["reviewed"] = True
    record["reviewRequired"] = False
    record["status"] = "approved"

    return record


def build_report(reviewed_records, skipped_ids, quit_early=False):
    reviewed_count = len(reviewed_records)

    report = {
        "datasetName": "Chinese Thu Man HSK 2 Vietnamese Meanings",
        "status": (
            "REVIEW_IN_PROGRESS"
            if reviewed_count < EXPECTED_COUNT
            else "REVIEW_COMPLETE"
        ),
        "level": 2,
        "recordCount": EXPECTED_COUNT,
        "summary": {
            "reviewed": reviewed_count,
            "unreviewed": EXPECTED_COUNT - reviewed_count,
            "skipped": len(skipped_ids),
            "missingMeaning": sum(
                not r.get("meaningVi")
                for r in reviewed_records
            ),
        },
        "skippedIds": sorted(skipped_ids),
        "quitEarly": quit_early,
        "productionCreated": False,
    }

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Review HSK 2 Vietnamese meaning candidates."
    )
    parser.add_argument(
        "--redo",
        action="store_true",
        help="Review all records again instead of resuming.",
    )
    args = parser.parse_args()

    print("=" * 72)
    print("HSK 2 MEANING REVIEW")
    print("=" * 72)
    print()

    candidates = load_json(INPUT_FILE)
    base = load_json(BASE_FILE)

    validate_input(candidates)
    base_by_id = validate_base(base)

    candidate_ids = {record["id"] for record in candidates}
    base_ids = set(base_by_id)

    missing_in_base = candidate_ids - base_ids
    extra_in_base = base_ids - candidate_ids

    if missing_in_base:
        raise SystemExit(
            "Candidate IDs missing from base: "
            + ", ".join(sorted(missing_in_base))
        )

    if extra_in_base:
        raise SystemExit(
            "Base contains IDs missing from candidates: "
            + ", ".join(sorted(extra_in_base))
        )

    existing_reviewed = {}

    if OUTPUT_FILE.exists() and not args.redo:
        existing = load_json(OUTPUT_FILE)

        if isinstance(existing, list):
            for record in existing:
                if (
                    isinstance(record, dict)
                    and record.get("id")
                    and record.get("reviewed") is True
                    and record.get("meaningVi")
                ):
                    existing_reviewed[record["id"]] = record

    print(f"Candidates:       {len(candidates)}")
    print(f"Already reviewed: {len(existing_reviewed)}")
    print(f"Remaining:        {EXPECTED_COUNT - len(existing_reviewed)}")
    print()
    print("Base and production data will NOT be modified.")
    print()

    reviewed = dict(existing_reviewed)
    skipped_ids = set()

    for position, candidate in enumerate(candidates, start=1):
        record_id = candidate["id"]

        if record_id in reviewed and not args.redo:
            continue

        result, meanings, notes = review_record(
            candidate,
            position,
            EXPECTED_COUNT,
        )

        if result == "quit":
            report = build_report(
                list(reviewed.values()),
                skipped_ids,
                quit_early=True,
            )

            save_json(
                OUTPUT_FILE,
                sorted(reviewed.values(), key=lambda r: r["id"]),
            )
            save_json(REPORT_FILE, report)

            print()
            print("Saved current progress.")
            print(f"Reviewed: {len(reviewed)}/{EXPECTED_COUNT}")
            print(f"Output:   {OUTPUT_FILE}")
            print(f"Report:   {REPORT_FILE}")
            return

        if result == "skip":
            skipped_ids.add(record_id)
            continue

        if result == "approved":
            base_record = base_by_id[record_id]

            reviewed[record_id] = build_reviewed_record(
                candidate,
                base_record,
                meanings,
                notes,
            )

            save_json(
                OUTPUT_FILE,
                sorted(reviewed.values(), key=lambda r: r["id"]),
            )

            report = build_report(
                list(reviewed.values()),
                skipped_ids,
                quit_early=False,
            )
            save_json(REPORT_FILE, report)

    report = build_report(
        list(reviewed.values()),
        skipped_ids,
        quit_early=False,
    )

    save_json(
        OUTPUT_FILE,
        sorted(reviewed.values(), key=lambda r: r["id"]),
    )
    save_json(REPORT_FILE, report)

    print()
    print("=" * 72)
    print("HSK 2 MEANING REVIEW COMPLETE")
    print("=" * 72)
    print(f"Reviewed: {len(reviewed)}/{EXPECTED_COUNT}")
    print(f"Skipped:  {len(skipped_ids)}")
    print(f"Output:   {OUTPUT_FILE}")
    print(f"Report:   {REPORT_FILE}")
    print()
    print("Production data was NOT created.")


if __name__ == "__main__":
    main()
