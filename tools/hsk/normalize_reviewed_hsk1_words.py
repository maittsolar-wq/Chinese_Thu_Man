import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FILE = (
    ROOT / "data" / "hsk" / "hsk1"
    / "hsk1_vocabulary_reviewed.json"
)

BACKUP = (
    ROOT / "data" / "hsk" / "hsk1"
    / "hsk1_vocabulary_reviewed.before_word_normalization.json"
)

# These are the six source-entry markers already confirmed by the
# normalization step:
# 本1 -> 本
# 点1 -> 点
# 和1 -> 和
# 会1 -> 会
# 两1 -> 两
# 喂1 -> 喂
WORD_MAP = {
    "本1": "本",
    "点1": "点",
    "和1": "和",
    "会1": "会",
    "两1": "两",
    "喂1": "喂",
}

def main():
    if not FILE.exists():
        raise SystemExit(f"Missing: {FILE}")

    records = json.loads(FILE.read_text(encoding="utf-8"))

    if not isinstance(records, list):
        raise RuntimeError("Expected JSON array.")

    # Preserve a backup before touching the reviewed dataset.
    if not BACKUP.exists():
        BACKUP.write_text(
            json.dumps(records, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    changed = []

    for record in records:
        old = record.get("word", "")
        if old in WORD_MAP:
            new = WORD_MAP[old]
            record["word"] = new
            changed.append({
                "id": record.get("id", ""),
                "old": old,
                "new": new
            })

    FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=" * 60)
    print("HSK 1 REVIEWED DATA WORD NORMALIZATION")
    print("=" * 60)
    print(f"Records: {len(records)}")
    print(f"Changed: {len(changed)}")
    print(f"Output:  {FILE}")
    print(f"Backup:  {BACKUP}")
    print()

    if changed:
        for item in changed:
            print(
                f"  ✓ {item['id']}: "
                f"{item['old']} -> {item['new']}"
            )
    else:
        print("No marker-suffixed words found.")

    print()
    print("Meanings, Pinyin and review status were NOT changed.")

if __name__ == "__main__":
    main()
