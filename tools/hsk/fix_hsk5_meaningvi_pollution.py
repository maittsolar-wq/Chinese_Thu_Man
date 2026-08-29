#!/usr/bin/env python3
"""Fix HSK5 meaningVi records polluted with an embedded example sentence.

Root cause: generate_hsk5_candidates_from_chinese_2500.py scraped
https://chinese.edu.vn/tu-vung-hsk-5.html and, for a subset of rows, the
detected "meaning" cell actually contained the Vietnamese meaning followed
by a Chinese example sentence and its Vietnamese translation concatenated
together, e.g.:

    "yeu thuong, giu gin 我们要爱护环境。 Chung ta phai bao ve moi truong."

That polluted string flowed unchanged into candidateMeanings / meaningVi /
selectedMeaningVi through complete_hsk5_reviewed.py and into production.

Fix rule (verified structurally against every currently affected record,
with zero split failures): locate the first CJK character (U+4E00-U+9FFF)
in the string and keep only the trimmed prefix before it. This is not an
arbitrary truncation -- it targets the exact script boundary the original
scraper's cleanup should have detected and did not.

Only records whose meaningVi/candidateMeanings actually contain a CJK
character are touched. Only the meaning fields are modified:
    meaningVi, candidateMeanings, selectedMeaningVi
No other field (id, word, pinyin, partOfSpeech, generationSource,
generationStatus, verificationStatus, humanVerified, ordering, ...) is
changed.

Input / output (same files, in place):
    data/hsk/hsk5/hsk5_meanings_candidates_input.json
    data/hsk/hsk5/hsk5_vocabulary_reviewed.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk5"

CANDIDATES = DATA / "hsk5_meanings_candidates_input.json"
REVIEWED = DATA / "hsk5_vocabulary_reviewed.json"

EXPECTED = 1600

CJK_RE = re.compile("[一-鿿]")


def clean_polluted(value: str) -> str | None:
    """Return the trimmed prefix before the first CJK character.

    Returns None if the value has no CJK pollution (nothing to do) or if
    the recovered prefix would be empty (would indicate a genuine failure
    that must stop the run rather than silently producing an empty
    meaning).
    """
    match = CJK_RE.search(value)

    if not match:
        return None

    prefix = value[: match.start()].strip(" ;,.　")

    return prefix


def load(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing input: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def fix_candidates() -> dict:
    records = load(CANDIDATES)

    if not isinstance(records, list) or len(records) != EXPECTED:
        raise SystemExit(
            f"{CANDIDATES}: expected {EXPECTED} records, got {len(records)}."
        )

    changed_ids = set()
    failures = []

    for record in records:
        rid = record.get("id")
        meanings = record.get("candidateMeanings")

        if not isinstance(meanings, list):
            continue

        new_meanings = []
        touched = False

        for value in meanings:
            if not isinstance(value, str):
                new_meanings.append(value)
                continue

            cleaned = clean_polluted(value)

            if cleaned is None:
                new_meanings.append(value)
                continue

            if not cleaned:
                failures.append(rid)
                continue

            new_meanings.append(cleaned)
            touched = True

        if touched:
            record["candidateMeanings"] = new_meanings
            changed_ids.add(rid)

    if failures:
        raise SystemExit(
            "Empty recovered candidateMeanings prefix for: "
            + ", ".join(failures)
        )

    CANDIDATES.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {"changedIds": changed_ids, "totalRecords": len(records)}


def fix_reviewed(expected_changed_ids: set) -> dict:
    records = load(REVIEWED)

    if not isinstance(records, list) or len(records) != EXPECTED:
        raise SystemExit(
            f"{REVIEWED}: expected {EXPECTED} records, got {len(records)}."
        )

    changed_ids = set()
    failures = []

    for record in records:
        rid = record.get("id")
        record_changed = False

        meaning_vi = record.get("meaningVi")

        if isinstance(meaning_vi, str):
            cleaned = clean_polluted(meaning_vi)

            if cleaned is not None:
                if not cleaned:
                    failures.append((rid, "meaningVi"))
                else:
                    record["meaningVi"] = cleaned
                    record_changed = True

        selected = record.get("selectedMeaningVi")

        if isinstance(selected, str):
            cleaned = clean_polluted(selected)

            if cleaned is not None:
                if not cleaned:
                    failures.append((rid, "selectedMeaningVi"))
                else:
                    record["selectedMeaningVi"] = cleaned
                    record_changed = True

        candidates = record.get("candidateMeanings")

        if isinstance(candidates, list):
            new_candidates = []
            candidates_touched = False

            for value in candidates:
                if not isinstance(value, str):
                    new_candidates.append(value)
                    continue

                cleaned = clean_polluted(value)

                if cleaned is None:
                    new_candidates.append(value)
                    continue

                if not cleaned:
                    failures.append((rid, "candidateMeanings"))
                    continue

                new_candidates.append(cleaned)
                candidates_touched = True

            if candidates_touched:
                record["candidateMeanings"] = new_candidates
                record_changed = True

        if record_changed:
            changed_ids.add(rid)

    if failures:
        raise SystemExit(
            "Empty recovered prefix for: "
            + ", ".join(f"{rid}:{field}" for rid, field in failures)
        )

    if changed_ids != expected_changed_ids:
        only_in_reviewed = changed_ids - expected_changed_ids
        only_in_candidates = expected_changed_ids - changed_ids
        raise SystemExit(
            "Mismatch between candidates-input and reviewed pollution "
            f"scope. Only in reviewed: {sorted(only_in_reviewed)}. "
            f"Only in candidates: {sorted(only_in_candidates)}."
        )

    REVIEWED.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {"changedIds": changed_ids, "totalRecords": len(records)}


def main():
    print("=" * 72)
    print("HSK 5 meaningVi POLLUTION FIX")
    print("=" * 72)
    print()

    candidates_result = fix_candidates()
    reviewed_result = fix_reviewed(candidates_result["changedIds"])

    print(f"Candidates input records: {candidates_result['totalRecords']}")
    print(f"Reviewed records:         {reviewed_result['totalRecords']}")
    print(f"Records corrected:        {len(reviewed_result['changedIds'])}")
    print()
    print("SUCCESS")
    print(
        "Only meaningVi/candidateMeanings/selectedMeaningVi were modified, "
        "and only on affected records."
    )
    print("No production data was created.")


if __name__ == "__main__":
    main()
