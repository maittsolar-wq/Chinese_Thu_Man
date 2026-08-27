#!/usr/bin/env python3
"""
Build the HSK 1 production dataset from the fully reviewed dataset.

This script is intentionally conservative:
- Reads hsk1_vocabulary_reviewed.json.
- Verifies the reviewed dataset is complete before packaging.
- Does NOT translate or modify meanings.
- Does NOT modify Pinyin.
- Removes workflow-only fields that should not be exposed to the app.
- Writes hsk1_vocabulary_production.json.

Run from the project root:
    python tools/hsk/build_hsk1_production.py
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk1"

INPUT_FILE = DATA_DIR / "hsk1_vocabulary_reviewed.json"
FINAL_REPORT = DATA_DIR / "hsk1_final_validation.json"
OUTPUT_FILE = DATA_DIR / "hsk1_vocabulary_production.json"

EXPECTED_COUNT = 300

# Fields used during source/review workflow but not required by the app's
# vocabulary production record.
WORKFLOW_FIELDS = {
    "reviewed",
    "reviewNotes",
    "candidateMeanings",
    "selectedMeaningVi",
    "sourceIds",
}


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def fail(message: str):
    raise SystemExit(f"ERROR: {message}")


def main():
    print("=" * 64)
    print("HSK 1 PRODUCTION BUILD")
    print("=" * 64)
    print()

    # ------------------------------------------------------------
    # 1. Require final validation PASS.
    # ------------------------------------------------------------
    try:
        final_report = load_json(FINAL_REPORT)
    except Exception as exc:
        fail(str(exc))

    if final_report.get("status") != "PASS":
        fail(
            "hsk1_final_validation.json is not PASS. "
            "Run final validation successfully before production build."
        )

    if final_report.get("productionCreated") is True:
        fail("Final validation report already indicates production was created.")

    # ------------------------------------------------------------
    # 2. Load reviewed dataset.
    # ------------------------------------------------------------
    try:
        reviewed = load_json(INPUT_FILE)
    except Exception as exc:
        fail(str(exc))

    if not isinstance(reviewed, list):
        fail("Reviewed dataset must be a JSON array.")

    if len(reviewed) != EXPECTED_COUNT:
        fail(
            f"Expected exactly {EXPECTED_COUNT} reviewed records, "
            f"got {len(reviewed)}."
        )

    # ------------------------------------------------------------
    # 3. Verify every record is production-ready.
    # ------------------------------------------------------------
    production = []
    seen_ids = set()
    seen_words = set()

    for index, record in enumerate(reviewed, start=1):
        if not isinstance(record, dict):
            fail(f"Record #{index} is not a JSON object.")

        record_id = record.get("id")
        word = str(record.get("word", "")).strip()
        pinyin = str(record.get("pinyin", "")).strip()
        meanings = record.get("meaningVi")

        if not record_id:
            fail(f"Record #{index} has no id.")

        if record_id in seen_ids:
            fail(f"Duplicate id: {record_id}")
        seen_ids.add(record_id)

        if not word:
            fail(f"{record_id}: empty word.")

        if word in seen_words:
            fail(f"{record_id}: duplicate Chinese word: {word!r}")
        seen_words.add(word)

        if not pinyin:
            fail(f"{record_id}: empty Pinyin.")

        if not isinstance(meanings, list) or not meanings:
            fail(f"{record_id}: meaningVi must be a non-empty array.")

        cleaned_meanings = []
        for meaning in meanings:
            if not isinstance(meaning, str) or not meaning.strip():
                fail(f"{record_id}: meaningVi contains an empty/non-string value.")
            cleaned_meanings.append(meaning.strip())

        if len(cleaned_meanings) != len(set(cleaned_meanings)):
            fail(f"{record_id}: duplicate Vietnamese meanings.")

        if record.get("reviewed") is not True:
            fail(f"{record_id}: record is not reviewed=True.")

        # Preserve the app-facing vocabulary data and remove review-only fields.
        production_record = {
            key: value
            for key, value in record.items()
            if key not in WORKFLOW_FIELDS and not key.startswith("_")
        }

        production_record["word"] = word
        production_record["pinyin"] = pinyin
        production_record["meaningVi"] = cleaned_meanings

        production.append(production_record)

    # ------------------------------------------------------------
    # 4. Stable ordering: preserve HSK 1 source/review order.
    # ------------------------------------------------------------
    production.sort(
        key=lambda r: (
            int(r.get("sourceSort", 10**9)),
            str(r.get("id", "")),
        )
    )

    # ------------------------------------------------------------
    # 5. Write production dataset.
    # ------------------------------------------------------------
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(production, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # ------------------------------------------------------------
    # 6. Print summary.
    # ------------------------------------------------------------
    print(f"Input:       {INPUT_FILE}")
    print(f"Records:     {len(production)}/{EXPECTED_COUNT}")
    print(f"Output:      {OUTPUT_FILE}")
    print()
    print("Production fields:")
    print("  ✓ Chinese word")
    print("  ✓ Pinyin")
    print("  ✓ Vietnamese meanings")
    print("  ✓ HSK level metadata")
    print("  ✓ Part of speech")
    print("  ✓ Source ordering")
    print("  ✓ Audio/relationship fields")
    print()
    print("Workflow-only review fields removed:")
    for field in sorted(WORKFLOW_FIELDS):
        print(f"  - {field}")
    print()
    print("SUCCESS")
    print("HSK 1 production dataset created.")
    print()
    print("Next step: run production validation before using the file in the app.")


if __name__ == "__main__":
    main()
