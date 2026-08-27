#!/usr/bin/env python3
"""
Validate the HSK 1 production dataset.

This is the final read-only gate after:
    source -> normalization -> pinyin QA -> meaning review
    -> final validation -> production build

Run from the project root:
    python tools/hsk/validate_hsk1_production.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk1"

PRODUCTION_FILE = DATA_DIR / "hsk1_vocabulary_production.json"
BASE_FILE = DATA_DIR / "hsk1_vocabulary_base.json"
FINAL_REPORT_FILE = DATA_DIR / "hsk1_final_validation.json"

REPORT_FILE = DATA_DIR / "hsk1_production_validation.json"

EXPECTED_COUNT = 300

PINYIN_ALLOWED_RE = re.compile(
    r"^[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü"
    r"ĀÁǍÀĒÉĚÈĪÍǏÌŌÓǑÒŪÚǓÙǕǗǙǛÜ"
    r"\s'’/\-·]+$"
)

FORBIDDEN_WORKFLOW_FIELDS = {
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


def main():
    errors = []
    warnings = []

    # ------------------------------------------------------------
    # 1. Load files
    # ------------------------------------------------------------
    try:
        production = load_json(PRODUCTION_FILE)
    except Exception as exc:
        errors.append(str(exc))
        return finish(errors, warnings, 0)

    try:
        base = load_json(BASE_FILE)
    except Exception as exc:
        errors.append(str(exc))
        return finish(errors, warnings, len(production) if isinstance(production, list) else 0)

    # ------------------------------------------------------------
    # 2. Top-level structure
    # ------------------------------------------------------------
    if not isinstance(production, list):
        errors.append("Production dataset phải là JSON array.")
        return finish(errors, warnings, 0)

    if not isinstance(base, list):
        errors.append("Base dataset phải là JSON array.")
        return finish(errors, warnings, len(production))

    # ------------------------------------------------------------
    # 3. Record count
    # ------------------------------------------------------------
    if len(production) != EXPECTED_COUNT:
        errors.append(
            f"Production record count = {len(production)}, expected {EXPECTED_COUNT}."
        )

    if len(base) != EXPECTED_COUNT:
        errors.append(
            f"Base record count = {len(base)}, expected {EXPECTED_COUNT}."
        )

    # ------------------------------------------------------------
    # 4. Index base records
    # ------------------------------------------------------------
    base_by_id = {}
    for record in base:
        if not isinstance(record, dict):
            errors.append("Base contains a non-object record.")
            continue

        record_id = record.get("id")
        if not record_id:
            errors.append("Base contains a record without id.")
            continue

        if record_id in base_by_id:
            errors.append(f"Base duplicate ID: {record_id}")
        base_by_id[record_id] = record

    # ------------------------------------------------------------
    # 5. Production records
    # ------------------------------------------------------------
    seen_ids = set()
    seen_words = set()

    for index, record in enumerate(production, start=1):
        if not isinstance(record, dict):
            errors.append(f"Production record #{index} is not an object.")
            continue

        record_id = record.get("id")
        word = str(record.get("word", "")).strip()
        pinyin = str(record.get("pinyin", "")).strip()
        meanings = record.get("meaningVi")

        # ID
        if not record_id:
            errors.append(f"Record #{index}: missing id.")
            continue

        if record_id in seen_ids:
            errors.append(f"Duplicate production ID: {record_id}")
        seen_ids.add(record_id)

        # Identity must match base
        base_record = base_by_id.get(record_id)
        if base_record is None:
            errors.append(f"{record_id}: ID not present in base dataset.")
        else:
            base_word = str(base_record.get("word", "")).strip()
            base_pinyin = str(base_record.get("pinyin", "")).strip()

            if word != base_word:
                errors.append(
                    f"{record_id}: word mismatch "
                    f"(base={base_word!r}, production={word!r})."
                )

            if pinyin != base_pinyin:
                errors.append(
                    f"{record_id}: Pinyin mismatch "
                    f"(base={base_pinyin!r}, production={pinyin!r})."
                )

            for field in ("introducedLevel", "hskLevels"):
                if field in base_record and record.get(field) != base_record.get(field):
                    errors.append(
                        f"{record_id}: {field} mismatch between base and production."
                    )

        # Word
        if not word:
            errors.append(f"{record_id}: empty Chinese word.")

        if word in seen_words:
            errors.append(f"Duplicate Chinese word: {word!r}")
        seen_words.add(word)

        # Pinyin
        if not pinyin:
            errors.append(f"{record_id}: empty Pinyin.")
        elif not PINYIN_ALLOWED_RE.match(pinyin):
            errors.append(
                f"{record_id}: invalid Pinyin characters/format: {pinyin!r}"
            )

        # Vietnamese meanings
        if not isinstance(meanings, list):
            errors.append(f"{record_id}: meaningVi must be an array.")
        elif not meanings:
            errors.append(f"{record_id}: meaningVi is empty.")
        else:
            cleaned = []
            for meaning in meanings:
                if not isinstance(meaning, str) or not meaning.strip():
                    errors.append(
                        f"{record_id}: meaningVi contains empty/non-string value."
                    )
                else:
                    cleaned.append(meaning.strip())

            if len(cleaned) != len(set(cleaned)):
                errors.append(f"{record_id}: duplicate Vietnamese meanings.")

        # Production must not contain review workflow state.
        forbidden_present = sorted(
            field for field in FORBIDDEN_WORKFLOW_FIELDS if field in record
        )
        if forbidden_present:
            errors.append(
                f"{record_id}: workflow-only fields present: "
                + ", ".join(forbidden_present)
            )

        # Basic production schema checks.
        required_fields = (
            "id",
            "word",
            "pinyin",
            "meaningVi",
            "introducedLevel",
            "hskLevels",
            "partOfSpeech",
            "sourceSort",
            "audio",
        )

        for field in required_fields:
            if field not in record:
                errors.append(f"{record_id}: missing required production field: {field}")

        if "partOfSpeech" in record and not isinstance(record["partOfSpeech"], list):
            errors.append(f"{record_id}: partOfSpeech must be an array.")

        if "hskLevels" in record and not isinstance(record["hskLevels"], list):
            errors.append(f"{record_id}: hskLevels must be an array.")

        if "audio" in record and not isinstance(record["audio"], dict):
            errors.append(f"{record_id}: audio must be an object.")

        if "sourceSort" in record and not isinstance(record["sourceSort"], int):
            errors.append(f"{record_id}: sourceSort must be an integer.")

    # ------------------------------------------------------------
    # 6. Exact ID set comparison
    # ------------------------------------------------------------
    production_ids = {r.get("id") for r in production if isinstance(r, dict)}
    base_ids = set(base_by_id)

    missing_ids = sorted(base_ids - production_ids)
    extra_ids = sorted(production_ids - base_ids)

    if missing_ids:
        errors.append(
            "Production missing IDs: " + ", ".join(missing_ids[:20])
        )

    if extra_ids:
        errors.append(
            "Production contains IDs outside base: " + ", ".join(extra_ids[:20])
        )

    # ------------------------------------------------------------
    # 7. Check final validation prerequisite
    # ------------------------------------------------------------
    if FINAL_REPORT_FILE.exists():
        try:
            final_report = load_json(FINAL_REPORT_FILE)
            if final_report.get("status") != "PASS":
                errors.append(
                    "hsk1_final_validation.json is not PASS."
                )
        except Exception as exc:
            warnings.append(f"Could not read final validation report: {exc}")
    else:
        warnings.append("hsk1_final_validation.json not found.")

    # ------------------------------------------------------------
    # 8. Final status
    # ------------------------------------------------------------
    return finish(errors, warnings, len(production))


def finish(errors, warnings, record_count):
    status = "PASS" if not errors else "FAIL"

    report = {
        "datasetName": "Chinese Thu Man HSK 1",
        "validationType": "PRODUCTION_VALIDATION",
        "status": status,
        "expectedRecordCount": EXPECTED_COUNT,
        "productionRecordCount": record_count,
        "errorCount": len(errors),
        "warningCount": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "productionFile": str(PRODUCTION_FILE),
    }

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=" * 64)
    print("HSK 1 PRODUCTION VALIDATION")
    print("=" * 64)
    print()
    print(f"Production records:   {record_count}/{EXPECTED_COUNT}")
    print(f"Errors:               {len(errors)}")
    print(f"Warnings:             {len(warnings)}")
    print(f"Status:               {status}")
    print(f"Report:               {REPORT_FILE}")
    print()

    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  ✗ {error}")
        print()

    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"  ! {warning}")
        print()

    if status == "PASS":
        print("PASS: Production dataset is ready for app integration.")
    else:
        print("FAIL: Production dataset is NOT ready.")

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
