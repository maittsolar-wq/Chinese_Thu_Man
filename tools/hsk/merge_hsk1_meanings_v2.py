import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hsk" / "hsk1"

BASE_FILE = DATA_DIR / "hsk1_vocabulary_base.json"
MEANING_FILE = DATA_DIR / "hsk1_meanings_draft_v2.json"
OUT_FILE = DATA_DIR / "hsk1_vocabulary_with_meanings_draft.json"

base = json.loads(BASE_FILE.read_text(encoding="utf-8"))
meaning_payload = json.loads(MEANING_FILE.read_text(encoding="utf-8"))
meaning_by_id = {r["id"]: r for r in meaning_payload["records"]}

if len(base) != 300:
    raise RuntimeError(f"Base must contain 300 records, got {len(base)}")

merged = []
for record in base:
    item = dict(record)
    meaning = meaning_by_id.get(record["id"])
    if meaning is None:
        raise RuntimeError(f"Missing meaning for {record['id']}")

    item["meaningVi"] = meaning["meaningVi"]
    item["contentStatus"] = "draft"
    item["reviewed"] = False
    item["reviewRequired"] = True
    merged.append(item)

OUT_FILE.write_text(
    json.dumps(merged, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("SUCCESS")
print("Merged records:", len(merged))
print("Output:", OUT_FILE)
print("Note: Pinyin remains sourced from the base vocabulary file.")
