import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    ROOT / "data" / "hsk" / "hsk1"
    / "hsk1_vocabulary_reviewed.json"
)

OUTPUT_FILE = INPUT_FILE


def load_records():
    if not INPUT_FILE.exists():
        raise SystemExit(
            f"Không tìm thấy dataset: {INPUT_FILE}"
        )

    data = json.loads(
        INPUT_FILE.read_text(encoding="utf-8")
    )

    if not isinstance(data, list):
        raise RuntimeError(
            "Dataset phải là JSON array."
        )

    if len(data) != 300:
        raise RuntimeError(
            f"Expected 300 records, got {len(data)}."
        )

    return data


def save_records(records):
    OUTPUT_FILE.write_text(
        json.dumps(
            records,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


def normalize_meanings(text):
    text = text.replace("；", ";")

    return [
        item.strip()
        for item in text.split(";")
        if item.strip()
    ]


def reviewed_count(records):
    return sum(
        1
        for record in records
        if record.get("reviewed") is True
    )


def show_record(record, position, total):
    print()
    print("=" * 64)
    print(
        f"HSK 1 MEANING REVIEW [{position}/{total}]"
    )
    print("=" * 64)

    print(
        f"ID:       {record.get('id', '')}"
    )

    print(
        f"中文:      {record.get('word', '')}"
    )

    print(
        f"Pinyin:   {record.get('pinyin', '')}"
    )

    print(
        f"Từ loại:  "
        f"{record.get('partOfSpeechSource', '')}"
    )

    print()
    print("Nghĩa hiện tại:")

    meanings = record.get(
        "meaningVi",
        []
    )

    if meanings:
        for i, meaning in enumerate(
            meanings,
            start=1
        ):
            print(
                f"  {i}. {meaning}"
            )
    else:
        print("  [CHƯA CÓ NGHĨA]")

    print()
    print("-" * 64)
    print("[1] PASS  - nghĩa đúng, giữ nguyên")
    print("[2] SỬA   - sửa toàn bộ nghĩa")
    print("[3] BỎ QUA - review sau")
    print("[4] THOÁT  - lưu tiến độ")
    print("-" * 64)


def review_record(record, position, total):

    show_record(
        record,
        position,
        total
    )

    while True:

        choice = input(
            "\nChọn [1/2/3/4]: "
        ).strip()

        if choice == "1":

            meanings = record.get(
                "meaningVi",
                []
            )

            if not isinstance(
                meanings,
                list
            ) or not meanings:

                print(
                    "⚠ Record chưa có nghĩa. "
                    "Không thể PASS."
                )

                continue

            record["reviewed"] = True

            record["reviewStatus"] = (
                "reviewed"
            )

            record["reviewNotes"] = (
                record.get(
                    "reviewNotes",
                    ""
                )
            )

            return "reviewed"


        if choice == "2":

            print()
            print(
                "Nhập nghĩa tiếng Việt."
            )

            print(
                "Nhiều nghĩa ngăn cách bằng ';'"
            )

            print(
                "Ví dụ: yêu; yêu thích"
            )

            new_text = input(
                "Nghĩa mới: "
            ).strip()

            new_meanings = (
                normalize_meanings(
                    new_text
                )
            )

            if not new_meanings:

                print(
                    "⚠ Nghĩa không được để trống."
                )

                continue

            record["meaningVi"] = (
                new_meanings
            )

            record["reviewed"] = True

            record["reviewStatus"] = (
                "reviewed"
            )

            record["reviewNotes"] = (
                "Meaning edited during manual review."
            )

            print(
                "✓ Đã cập nhật nghĩa."
            )

            return "reviewed"


        if choice == "3":

            record["reviewed"] = False

            record["reviewStatus"] = (
                "unreviewed"
            )

            return "skipped"


        if choice == "4":

            return "exit"


        print(
            "⚠ Lựa chọn không hợp lệ."
        )


def main():

    records = load_records()

    total = len(records)

    already_reviewed = reviewed_count(
        records
    )


    print("=" * 64)
    print("HSK 1 MANUAL MEANING REVIEW v2")
    print("=" * 64)

    print(
        f"Dataset:  {INPUT_FILE}"
    )

    print(
        f"Records:  {total}"
    )

    print(
        f"Reviewed: {already_reviewed}/{total}"
    )

    print()
    print(
        "Tool sẽ TỰ TÌM record đầu tiên "
        "có reviewed != True."
    )

    print(
        "Không review lại record đã reviewed=True."
    )

    print(
        "Tiến độ được lưu sau mỗi record."
    )

    print(
        "Chọn [4] để thoát an toàn."
    )


    # --------------------------------------------------------
    # IMPORTANT:
    # Find the first actual unreviewed record.
    # Do not assume the starting index.
    # --------------------------------------------------------

    while True:

        target_index = None

        for i, record in enumerate(
            records
        ):

            if record.get(
                "reviewed"
            ) is not True:

                target_index = i
                break


        # ----------------------------------------------------
        # All records reviewed.
        # ----------------------------------------------------

        if target_index is None:

            print()
            print("=" * 64)
            print("ALL 300 RECORDS REVIEWED")
            print("=" * 64)

            print(
                f"Reviewed: "
                f"{reviewed_count(records)}/{total}"
            )

            print(
                f"Output: {OUTPUT_FILE}"
            )

            print(
                "STATUS: READY_FOR_FINAL_VALIDATION"
            )

            return


        record = records[target_index]

        position = target_index + 1


        result = review_record(
            record,
            position,
            total
        )


        # ----------------------------------------------------
        # Save immediately after every action.
        # ----------------------------------------------------

        save_records(records)


        if result == "exit":

            current = reviewed_count(
                records
            )

            print()
            print("=" * 64)
            print("ĐÃ LƯU TIẾN ĐỘ")
            print("=" * 64)

            print(
                f"Reviewed: {current}/{total}"
            )

            print(
                f"Remaining: "
                f"{total - current}"
            )

            print(
                f"Output: {OUTPUT_FILE}"
            )

            return


if __name__ == "__main__":
    main()
