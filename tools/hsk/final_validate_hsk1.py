#!/usr/bin/env python3
"""
Final validation v2 for the HSK 1 reviewed dataset.

This script is READ-ONLY:
- It does NOT modify the reviewed dataset.
- It does NOT create the production dataset.
- It compares the reviewed data against the HSK 1 base vocabulary.
- It also checks the latest Pinyin validation report.

Run from the project root:
    python tools/hsk/final_validate_hsk1.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data" / "hsk" / "hsk1"

BASE_FILE = DATA_DIR / "hsk1_vocabulary_base.json"
REVIEWED_FILE = DATA_DIR / "hsk1_vocabulary_reviewed.json"
MEANING_REPORT_FILE = DATA_DIR / "hsk1_meaning_validation.json"
PINYIN_REPORT_FILE = DATA_DIR / "hsk1_pinyin_validation.json"

REPORT_FILE = DATA_DIR / "hsk1_final_validation.json"

EXPECTED_COUNT = 300

# Chinese source-entry markers that were normalized earlier.
MARKER_SUFFIX_RE = re.compile(r"^[\u4e00-\u9fff]+[1-9]$")

# Basic pinyin character validation.
# Keep this format check aligned with validate_hsk1_pinyin.py v4.
# The source contains:
# - curly apostrophe in forms such as nǚ’ér
# - slash for accepted pronunciation alternatives such as shéi/shuí
PINYIN_ALLOWED_RE = re.compile(
    r"^[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü"
    r"ĀÁǍÀĒÉĚÈĪÍǏÌŌÓǑÒŪÚǓÙǕǗǙǛÜ"
    r"\s'’/\-·]+$"
)


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def add_error(errors, message):
    errors.append(message)


def add_warning(warnings, message):
    warnings.append(message)


def validate_list_of_strings(value, field_name, record_id, errors):
    if not isinstance(value, list):
        add_error(errors, f"{record_id}: {field_name} phải là array")
        return

    for item in value:
        if not isinstance(item, str) or not item.strip():
            add_error(errors, f"{record_id}: {field_name} chứa giá trị rỗng/không phải string")


def main():
    errors = []
    warnings = []

    # ------------------------------------------------------------
    # 1. Load datasets/reports
    # ------------------------------------------------------------
    try:
        base = load_json(BASE_FILE)
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1

    try:
        reviewed = load_json(REVIEWED_FILE)
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1

    meaning_report = None
    pinyin_report = None

    if MEANING_REPORT_FILE.exists():
        try:
            meaning_report = load_json(MEANING_REPORT_FILE)
        except Exception as exc:
            add_warning(warnings, f"Không đọc được meaning validation report: {exc}")
    else:
        add_warning(warnings, "Thiếu hsk1_meaning_validation.json")

    if PINYIN_REPORT_FILE.exists():
        try:
            pinyin_report = load_json(PINYIN_REPORT_FILE)
        except Exception as exc:
            add_warning(warnings, f"Không đọc được pinyin validation report: {exc}")
    else:
        add_warning(warnings, "Thiếu hsk1_pinyin_validation.json")

    # ------------------------------------------------------------
    # 2. Top-level structure
    # ------------------------------------------------------------
    if not isinstance(base, list):
        add_error(errors, "Base dataset phải là JSON array")

    if not isinstance(reviewed, list):
        add_error(errors, "Reviewed dataset phải là JSON array")

    if errors:
        return write_report(errors, warnings, 0, 0)

    # ------------------------------------------------------------
    # 3. Record count
    # ------------------------------------------------------------
    if len(base) != EXPECTED_COUNT:
        add_error(errors, f"Base record count = {len(base)}, expected {EXPECTED_COUNT}")

    if len(reviewed) != EXPECTED_COUNT:
        add_error(
            errors,
            f"Reviewed record count = {len(reviewed)}, expected {EXPECTED_COUNT}",
        )

    if len(base) != len(reviewed):
        add_error(
            errors,
            f"Base/reviewed count mismatch: {len(base)} vs {len(reviewed)}",
        )

    # ------------------------------------------------------------
    # 4. Index records by ID
    # ------------------------------------------------------------
    base_by_id = {}
    reviewed_by_id = {}

    for record in base:
        if not isinstance(record, dict):
            add_error(errors, "Base chứa record không phải object")
            continue

        record_id = record.get("id")
        if not record_id:
            add_error(errors, "Base có record thiếu id")
            continue

        if record_id in base_by_id:
            add_error(errors, f"Base duplicate ID: {record_id}")
        base_by_id[record_id] = record

    for record in reviewed:
        if not isinstance(record, dict):
            add_error(errors, "Reviewed chứa record không phải object")
            continue

        record_id = record.get("id")
        if not record_id:
            add_error(errors, "Reviewed có record thiếu id")
            continue

        if record_id in reviewed_by_id:
            add_error(errors, f"Reviewed duplicate ID: {record_id}")
        reviewed_by_id[record_id] = record

    # ------------------------------------------------------------
    # 5. Exact base/reviewed alignment
    # ------------------------------------------------------------
    if set(base_by_id) != set(reviewed_by_id):
        missing = sorted(set(base_by_id) - set(reviewed_by_id))
        extra = sorted(set(reviewed_by_id) - set(base_by_id))

        if missing:
            add_error(errors, f"Reviewed thiếu IDs: {', '.join(missing[:20])}")
        if extra:
            add_error(errors, f"Reviewed có IDs ngoài base: {', '.join(extra[:20])}")

    # ------------------------------------------------------------
    # 6. Per-record production-readiness checks
    # ------------------------------------------------------------
    reviewed_count = 0
    seen_words = set()
    seen_pinyin = {}

    for record_id, base_record in base_by_id.items():
        record = reviewed_by_id.get(record_id)
        if record is None:
            continue

        # Core identity must not change during meaning review.
        base_word = str(base_record.get("word", "")).strip()
        review_word = str(record.get("word", "")).strip()

        if not review_word:
            add_error(errors, f"{record_id}: word rỗng")
        elif review_word != base_word:
            add_error(
                errors,
                f"{record_id}: word mismatch (base={base_word!r}, reviewed={review_word!r})",
            )

        # Source-entry markers such as 本1 must not remain.
        if MARKER_SUFFIX_RE.match(review_word):
            add_error(errors, f"{record_id}: word còn marker số cuối: {review_word!r}")

        # Pinyin must remain unchanged by meaning review.
        base_pinyin = str(base_record.get("pinyin", "")).strip()
        review_pinyin = str(record.get("pinyin", "")).strip()

        if not review_pinyin:
            add_error(errors, f"{record_id}: Pinyin rỗng")
        elif review_pinyin != base_pinyin:
            add_error(
                errors,
                f"{record_id}: Pinyin mismatch (base={base_pinyin!r}, reviewed={review_pinyin!r})",
            )

        if review_pinyin:
            if not PINYIN_ALLOWED_RE.match(review_pinyin):
                add_error(
                    errors,
                    f"{record_id}: Pinyin chứa ký tự ngoài format cho phép: {review_pinyin!r}",
                )

            if review_pinyin in seen_pinyin:
                add_warning(
                    warnings,
                    f"{record_id}: Pinyin trùng với {seen_pinyin[review_pinyin]} "
                    f"({review_pinyin!r}); có thể hợp lệ.",
                )
            else:
                seen_pinyin[review_pinyin] = record_id

        if review_word:
            if review_word in seen_words:
                add_error(errors, f"Duplicate Chinese word: {review_word!r}")
            seen_words.add(review_word)

        # Vietnamese meanings.
        meanings = record.get("meaningVi")

        if meanings is None:
            add_error(errors, f"{record_id}: thiếu meaningVi")
        else:
            validate_list_of_strings(meanings, "meaningVi", record_id, errors)

            if isinstance(meanings, list):
                cleaned = [x.strip() for x in meanings if isinstance(x, str) and x.strip()]

                if not cleaned:
                    add_error(errors, f"{record_id}: meaningVi rỗng")

                if len(cleaned) != len(set(cleaned)):
                    add_error(errors, f"{record_id}: meaningVi có nghĩa trùng lặp")

        # Manual review must be complete for production.
        if record.get("reviewed") is True:
            reviewed_count += 1
        else:
            add_error(errors, f"{record_id}: reviewed không phải True")

        # Basic HSK identity consistency.
        if record.get("introducedLevel") is not None:
            if record.get("introducedLevel") != base_record.get("introducedLevel"):
                add_error(
                    errors,
                    f"{record_id}: introducedLevel thay đổi trong review",
                )

        if record.get("hskLevels") is not None:
            if record.get("hskLevels") != base_record.get("hskLevels"):
                add_error(
                    errors,
                    f"{record_id}: hskLevels thay đổi trong review",
                )

    # ------------------------------------------------------------
    # 7. Check validation reports
    # ------------------------------------------------------------
    if meaning_report:
        status = meaning_report.get("status")
        records = meaning_report.get("recordCount", meaning_report.get("records"))
        reviewed_in_report = meaning_report.get("reviewedCount", meaning_report.get("reviewed"))

        if status and "PASS" not in str(status):
            add_error(errors, f"Meaning validation report status không PASS: {status}")

        # Support both old and new report shapes.
        if isinstance(records, int) and records != EXPECTED_COUNT:
            add_error(errors, f"Meaning report record count = {records}")

        if isinstance(reviewed_in_report, int) and reviewed_in_report != EXPECTED_COUNT:
            add_error(errors, f"Meaning report reviewed count = {reviewed_in_report}")

        report_errors = meaning_report.get("errors")
        if isinstance(report_errors, int) and report_errors != 0:
            add_error(errors, f"Meaning validation report có {report_errors} errors")

    if pinyin_report:
        status = pinyin_report.get("status")
        if status and str(status).upper() != "PASS":
            add_error(errors, f"Pinyin validation report status không PASS: {status}")

        for field_name in ("recordCount", "records"):
            value = pinyin_report.get(field_name)
            if isinstance(value, int) and value != EXPECTED_COUNT:
                add_error(errors, f"Pinyin report {field_name} = {value}")
                break

        invalid = pinyin_report.get("invalidPinyin", pinyin_report.get("invalid"))
        if isinstance(invalid, int) and invalid != 0:
            add_error(errors, f"Pinyin validation report có {invalid} invalid Pinyin")

        missing = pinyin_report.get("missingPinyin", pinyin_report.get("missing"))
        if isinstance(missing, int) and missing != 0:
            add_error(errors, f"Pinyin validation report có {missing} missing Pinyin")

    # ------------------------------------------------------------
    # 8. Final status
    # ------------------------------------------------------------
    status = "PASS" if not errors and reviewed_count == EXPECTED_COUNT else "FAIL"

    print("=" * 64)
    print("HSK 1 FINAL DATA VALIDATION v2")
    print("=" * 64)
    print()
    print(f"Base records:          {len(base)}/{EXPECTED_COUNT}")
    print(f"Reviewed records:      {reviewed_count}/{EXPECTED_COUNT}")
    print(f"Unreviewed records:    {EXPECTED_COUNT - reviewed_count}")
    print(f"Errors:                {len(errors)}")
    print(f"Warnings:              {len(warnings)}")
    print(f"Status:                {status}")
    print(f"Report:                {REPORT_FILE}")
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
        print("PASS: HSK 1 reviewed dataset đạt final validation.")
        print("Chưa tạo production file. Production packaging là bước tiếp theo.")
    else:
        print("FAIL: Chưa đủ điều kiện tạo production.")
        print("Hãy sửa lỗi rồi chạy lại final validation.")

    return write_report(
        errors,
        warnings,
        len(base),
        reviewed_count,
        status=status,
    )


def write_report(
    errors,
    warnings,
    base_count,
    reviewed_count,
    status=None,
):
    if status is None:
        status = "PASS" if not errors else "FAIL"

    report = {
        "datasetName": "Chinese Thu Man HSK 1",
        "validationType": "FINAL_DATA_VALIDATION",
        "status": status,
        "expectedRecordCount": EXPECTED_COUNT,
        "baseRecordCount": base_count,
        "reviewedRecordCount": reviewed_count,
        "unreviewedRecordCount": max(EXPECTED_COUNT - reviewed_count, 0),
        "errorCount": len(errors),
        "warningCount": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "productionCreated": False,
    }

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
