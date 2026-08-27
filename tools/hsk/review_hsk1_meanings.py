import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    ROOT / "data" / "hsk" / "hsk1"
    / "hsk1_vocabulary_reviewed.json"
)

TOTAL_EXPECTED = 300


def load_records():
    if not DATA_FILE.exists():
        raise SystemExit(f"Không tìm thấy dataset: {DATA_FILE}")

    records = json.loads(
        DATA_FILE.read_text(encoding="utf-8")
    )

    if not isinstance(records, list):
        raise RuntimeError("Dataset phải là JSON array.")

    if len(records) != TOTAL_EXPECTED:
        raise RuntimeError(
            f"Expected {TOTAL_EXPECTED} records, got {len(records)}."
        )

    return records


def save_records(records):
    DATA_FILE.write_text(
        json.dumps(
            records,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


def count_reviewed(records):
    return sum(
        1 for r in records
        if r.get("reviewed") is True
    )


def normalize_meanings(text):
    text = text.replace("；", ";")

    return [
        item.strip()
        for item in text.split(";")
        if item.strip()
    ]


def show_record(record, position, total, reviewed, skipped_this_session):
    print()
    print("=" * 64)
    print(f"HSK 1 MEANING REVIEW [{position}/{total}]")
    print("=" * 64)

    print(f"Tiến độ:  {reviewed}/{total} reviewed")
    print(f"Bỏ qua phiên này: {skipped_this_session}")
    print()

    print(f"ID:       {record.get('id', '')}")
    print(f"中文:      {record.get('word', '')}")
    print(f"Pinyin:   {record.get('pinyin', '')}")
    print(f"Từ loại:  {record.get('partOfSpeechSource', '')}")

    print()
    print("Nghĩa hiện tại:")

    meanings = record.get("meaningVi", [])

    if isinstance(meanings, list) and meanings:
        for i, meaning in enumerate(meanings, start=1):
            print(f"  {i}. {meaning}")
    else:
        print("  [CHƯA CÓ NGHĨA]")

    print()
    print("-" * 64)
    print("[1] PASS   - nghĩa đúng, giữ nguyên")
    print("[2] SỬA    - sửa toàn bộ nghĩa")
    print("[3] BỎ QUA - sang từ chưa review tiếp theo trong phiên này")
    print("[4] THOÁT  - lưu tiến độ và thoát")
    print("-" * 64)


def review_one(record, position, total, reviewed, skipped_this_session):

    show_record(
        record,
        position,
        total,
        reviewed,
        skipped_this_session
    )

    while True:

        choice = input("\nChọn [1/2/3/4]: ").strip()

        if choice == "1":

            meanings = record.get("meaningVi", [])

            if not isinstance(meanings, list) or not meanings:
                print("⚠ Record chưa có nghĩa. Không thể PASS.")
                continue

            record["reviewed"] = True
            record["reviewStatus"] = "reviewed"

            save_records(records_global)

            return "reviewed"

        if choice == "2":

            print()
            print("Nhập nghĩa tiếng Việt.")
            print("Nếu có nhiều nghĩa, ngăn cách bằng ';'")
            print("Ví dụ: yêu; yêu thích")

            new_text = input("Nghĩa mới: ").strip()

            new_meanings = normalize_meanings(new_text)

            if not new_meanings:
                print("⚠ Nghĩa không được để trống.")
                continue

            record["meaningVi"] = new_meanings
            record["reviewed"] = True
            record["reviewStatus"] = "reviewed"
            record["reviewNotes"] = (
                "Meaning edited during manual review."
            )

            save_records(records_global)

            print("✓ Đã cập nhật nghĩa.")

            return "reviewed"

        if choice == "3":
            # IMPORTANT:
            # Do NOT save a permanent state change here.
            # The record remains unreviewed and will be retried
            # in a future session.
            return "skipped"

        if choice == "4":
            return "exit"

        print("⚠ Lựa chọn không hợp lệ.")


def main():

    global records_global

    records = load_records()
    records_global = records

    total = len(records)

    reviewed = count_reviewed(records)

    print("=" * 64)
    print("HSK 1 MANUAL MEANING REVIEW v3")
    print("=" * 64)

    print(f"Dataset:  {DATA_FILE}")
    print(f"Records:  {total}")
    print(f"Reviewed: {reviewed}/{total}")
    print()

    print(
        "Tool sẽ tiếp tục từ record chưa review đầu tiên."
    )

    print(
        "[3] BỎ QUA chỉ bỏ qua trong PHIÊN HIỆN TẠI."
    )

    print(
        "Nếu bạn thoát và chạy lại, record bị bỏ qua "
        "sẽ được hiển thị lại."
    )

    print(
        "Đây là chủ ý để không đánh dấu một từ chưa review "
        "thành reviewed."
    )

    print(
        "[4] THOÁT để lưu tiến độ."
    )

    # --------------------------------------------------------
    # Session-local cursor.
    #
    # This is the key fix:
    # after SKIP, move to the next index in this session.
    # We do NOT persist skip as reviewed.
    # --------------------------------------------------------

    cursor = 0
    skipped_this_session = set()

    while cursor < total:

        record = records[cursor]

        # Already reviewed -> skip automatically.
        if record.get("reviewed") is True:
            cursor += 1
            continue

        # Already skipped during this session -> continue.
        if cursor in skipped_this_session:
            cursor += 1
            continue

        current_reviewed = count_reviewed(records)

        result = review_one(
            record,
            cursor + 1,
            total,
            current_reviewed,
            len(skipped_this_session)
        )

        if result == "reviewed":
            cursor += 1
            continue

        if result == "skipped":
            skipped_this_session.add(cursor)
            cursor += 1
            continue

        if result == "exit":
            current_reviewed = count_reviewed(records)

            print()
            print("=" * 64)
            print("ĐÃ LƯU TIẾN ĐỘ")
            print("=" * 64)

            print(f"Reviewed: {current_reviewed}/{total}")
            print(f"Skipped this session: {len(skipped_this_session)}")
            print(f"Remaining unreviewed: {total - current_reviewed}")
            print(f"Output: {DATA_FILE}")

            return

    current_reviewed = count_reviewed(records)

    print()
    print("=" * 64)
    print("SESSION COMPLETE")
    print("=" * 64)

    print(f"Reviewed: {current_reviewed}/{total}")
    print(
        f"Skipped this session: "
        f"{len(skipped_this_session)}"
    )
    print(
        f"Remaining unreviewed: "
        f"{total - current_reviewed}"
    )

    if current_reviewed == total:
        print("STATUS: READY_FOR_FINAL_VALIDATION")
    else:
        print(
            "STATUS: SESSION COMPLETE "
            "WITH UNREVIEWED RECORDS"
        )


if __name__ == "__main__":
    records_global = []
    main()
