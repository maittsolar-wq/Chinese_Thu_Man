import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

BASE_FILE = (
    ROOT / "data" / "hsk" / "hsk1"
    / "hsk1_vocabulary_base.json"
)

REVIEWED_FILE = (
    ROOT / "data" / "hsk" / "hsk1"
    / "hsk1_vocabulary_reviewed.json"
)

REPORT_FILE = (
    ROOT / "data" / "hsk" / "hsk1"
    / "hsk1_meaning_validation.json"
)

def load_json(path):
    if not path.exists():
        raise SystemExit(f"Missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    base = load_json(BASE_FILE)
    reviewed = load_json(REVIEWED_FILE)

    if not isinstance(base, list) or not isinstance(reviewed, list):
        raise RuntimeError("Datasets must be JSON arrays.")

    errors = []
    warnings = []

    if len(base) != 300:
        errors.append(f"Base record count is {len(base)}, expected 300.")

    if len(reviewed) != 300:
        errors.append(
            f"Reviewed record count is {len(reviewed)}, expected 300."
        )

    base_by_id = {r.get("id"): r for r in base}
    reviewed_by_id = {r.get("id"): r for r in reviewed}

    if len(base_by_id) != len(base):
        errors.append("Duplicate IDs in base dataset.")

    if len(reviewed_by_id) != len(reviewed):
        errors.append("Duplicate IDs in reviewed dataset.")

    # Check that the reviewed dataset still corresponds exactly to the
    # canonical normalized base dataset.
    for record_id, base_record in base_by_id.items():

        if record_id not in reviewed_by_id:
            errors.append(
                f"{record_id}: missing from reviewed dataset."
            )
            continue

        record = reviewed_by_id[record_id]

        base_word = str(base_record.get("word", "")).strip()
        reviewed_word = str(record.get("word", "")).strip()

        if base_word != reviewed_word:
            errors.append(
                f"{record_id}: word không khớp "
                f"(base='{base_word}', reviewed='{reviewed_word}')"
            )

        base_pinyin = str(
            base_record.get("pinyin", "")
        ).strip()

        reviewed_pinyin = str(
            record.get("pinyin", "")
        ).strip()

        if base_pinyin != reviewed_pinyin:
            errors.append(
                f"{record_id}: Pinyin không khớp "
                f"(base='{base_pinyin}', reviewed='{reviewed_pinyin}')"
            )

        meanings = record.get("meaningVi", [])

        if not isinstance(meanings, list):
            errors.append(
                f"{record_id}: meaningVi phải là list."
            )
            continue

        if record.get("reviewed") is True and len(meanings) == 0:
            errors.append(
                f"{record_id}: reviewed=True nhưng meaningVi trống."
            )

    reviewed_count = sum(
        1
        for r in reviewed
        if r.get("reviewed") is True
    )

    unreviewed_count = len(reviewed) - reviewed_count

    if reviewed_count < 300:
        warnings.append(
            f"Chưa đủ review: "
            f"{reviewed_count}/300 records đã reviewed."
        )

    # Canonical HSK 1 should not contain the six source-entry markers.
    marker_words = {
        "本1", "点1", "和1", "会1", "两1", "喂1"
    }

    remaining_markers = [
        {
            "id": r.get("id", ""),
            "word": r.get("word", "")
        }
        for r in reviewed
        if r.get("word") in marker_words
    ]

    if remaining_markers:
        for item in remaining_markers:
            errors.append(
                f"{item['id']}: vẫn còn source marker "
                f"'{item['word']}'."
            )

    status = (
        "PASS_READY_FOR_CONTINUED_REVIEW"
        if not errors and reviewed_count < 300
        else "PASS_READY_FOR_FINAL_VALIDATION"
        if not errors
        else "FAIL"
    )

    report = {
        "dataset": str(REVIEWED_FILE),
        "status": status,
        "recordCount": len(reviewed),
        "reviewed": reviewed_count,
        "unreviewed": unreviewed_count,
        "errors": errors,
        "warnings": warnings,
        "notes": [
            "Validator reads hsk1_vocabulary_reviewed.json, not the old draft file.",
            "Word and Pinyin are compared against the canonical normalized base.",
            "The six known source markers must not remain in reviewed production-bound data.",
            "Unreviewed records are warnings until all 300 meanings are reviewed."
        ]
    }

    REPORT_FILE.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=" * 60)
    print("HSK 1 MEANINGS VALIDATION v2")
    print("=" * 60)
    print(f"Records:          {len(reviewed)}/300")
    print(f"Reviewed:         {reviewed_count}/300")
    print(f"Unreviewed:       {unreviewed_count}/300")
    print(f"Errors:           {len(errors)}")
    print(f"Warnings:         {len(warnings)}")
    print(f"Status:           {status}")
    print(f"Report:           {REPORT_FILE}")

    if errors:
        print("\nERRORS:")
        for error in errors[:50]:
            print(f"  ✗ {error}")

    if warnings:
        print("\nWARNINGS:")
        for warning in warnings:
            print(f"  ! {warning}")

    print()
    if errors:
        print("STOP: Có lỗi. Chưa được tạo production.")
    elif reviewed_count < 300:
        print(
            "PASS: Dữ liệu reviewed hợp lệ, "
            "nhưng còn meanings chưa review."
        )
    else:
        print(
            "PASS: 300/300 meanings đã review. "
            "Có thể chuyển sang final validation."
        )

if __name__ == "__main__":
    main()
