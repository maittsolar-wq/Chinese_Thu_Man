import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk1"

INPUT_FILE = DATA_DIR / "hsk1_vocabulary_with_meanings_draft.json"
OUTPUT_FILE = DATA_DIR / "hsk1_vocabulary_reviewed.json"

def load_records():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Không tìm thấy: {INPUT_FILE}")
    return json.loads(INPUT_FILE.read_text(encoding="utf-8"))

def save_records(records):
    OUTPUT_FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def normalize_meanings(text):
    parts = [x.strip() for x in text.replace("；", ";").split(";")]
    return [x for x in parts if x]

def review_record(record, index, total):
    print("\n" + "=" * 64)
    print(f"HSK 1 VOCABULARY REVIEW  [{index}/{total}]")
    print("=" * 64)
    print(f"ID:       {record.get('id', '')}")
    print(f"中文:      {record.get('word', '')}")
    print(f"Pinyin:   {record.get('pinyin', '')}")

    meanings = record.get("meaningVi", [])
    print("Nghĩa hiện tại:")
    if meanings:
        for i, meaning in enumerate(meanings, 1):
            print(f"  {i}. {meaning}")
    else:
        print("  [CHƯA CÓ NGHĨA]")

    print("\n[1] PASS - nghĩa đúng, giữ nguyên")
    print("[2] SỬA - nhập lại nghĩa tiếng Việt")
    print("[3] BỎ QUA - chưa review, quay lại sau")
    print("[4] THOÁT - lưu tiến độ và thoát")

    while True:
        choice = input("\nChọn [1/2/3/4]: ").strip()

        if choice == "1":
            record["reviewStatus"] = "reviewed"
            record["reviewed"] = True
            record["reviewNotes"] = ""
            return "reviewed"

        if choice == "2":
            new_text = input(
                "Nhập nghĩa tiếng Việt, ngăn cách bằng dấu ';': "
            ).strip()
            new_meanings = normalize_meanings(new_text)

            if not new_meanings:
                print("⚠ Nghĩa không được để trống.")
                continue

            record["meaningVi"] = new_meanings
            record["reviewStatus"] = "reviewed"
            record["reviewed"] = True
            record["reviewNotes"] = "Meaning edited during manual review."
            return "reviewed"

        if choice == "3":
            record["reviewStatus"] = "unreviewed"
            record["reviewed"] = False
            return "skipped"

        if choice == "4":
            return "exit"

        print("Lựa chọn không hợp lệ.")

def main():
    records = load_records()

    # Backward-compatible defaults.
    for record in records:
        record.setdefault("reviewStatus", "unreviewed")
        record.setdefault("reviewed", False)
        record.setdefault("reviewNotes", "")

    total = len(records)
    reviewed_count = sum(1 for r in records if r.get("reviewed") is True)

    print("=" * 64)
    print("HSK 1 MANUAL MEANING REVIEW")
    print("=" * 64)
    print(f"Dataset:  {INPUT_FILE}")
    print(f"Records:  {total}")
    print(f"Reviewed: {reviewed_count}/{total}")
    print(f"Output:   {OUTPUT_FILE}")
    print()
    print("Mỗi lần chạy sẽ tiếp tục từ record chưa review đầu tiên.")
    print("Thoát bằng lựa chọn [4]; tiến độ được lưu ngay sau mỗi record.")

    for index, record in enumerate(records, 1):
        if record.get("reviewed") is True:
            continue

        result = review_record(record, index, total)

        # Save after every action so progress is not lost.
        save_records(records)

        if result == "exit":
            print("\nĐã lưu tiến độ. Thoát.")
            return

    reviewed_count = sum(1 for r in records if r.get("reviewed") is True)

    print("\n" + "=" * 64)
    print("REVIEW SESSION COMPLETE")
    print("=" * 64)
    print(f"Reviewed: {reviewed_count}/{total}")
    print(f"Remaining: {total - reviewed_count}")
    print(f"Output: {OUTPUT_FILE}")

    if reviewed_count == total:
        print("STATUS: READY_FOR_FINAL_VALIDATION")
    else:
        print("STATUS: REVIEW_INCOMPLETE")

if __name__ == "__main__":
    main()
