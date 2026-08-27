import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "data" / "hsk" / "hsk1" / "hsk1_vocabulary_base.json"
MEANINGS = ROOT / "data" / "hsk" / "hsk1" / "hsk1_meanings_draft.json"
OUT = ROOT / "data" / "hsk" / "hsk1" / "hsk1_vocabulary_merged_draft.json"

def main():
    base = json.loads(BASE.read_text(encoding="utf-8"))
    meanings_doc = json.loads(MEANINGS.read_text(encoding="utf-8"))
    meanings = meanings_doc["records"]

    if len(base) != 300 or len(meanings) != 300:
        raise RuntimeError(f"Expected 300 + 300 records; got {len(base)} + {len(meanings)}")

    by_id = {r["id"]: r for r in meanings}
    errors = []

    for r in base:
        m = by_id.get(r["id"])
        if not m:
            errors.append(f"Missing meaning: {r['id']}")
            continue
        if r["word"] != m["word"]:
            errors.append(f"Word mismatch: {r['id']}: {r['word']} != {m['word']}")

    if errors:
        raise RuntimeError("Merge validation failed:\n" + "\n".join(errors))

    merged = []
    for r in base:
        m = by_id[r["id"]]
        out = dict(r)
        out["meaningVi"] = m["meaningVi"]
        out["meaningStatus"] = m["status"]
        out["reviewRequired"] = m["reviewRequired"]
        merged.append(out)

    OUT.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print("SUCCESS")
    print("Merged records:", len(merged))
    print("Output:", OUT)
    print("Status: DRAFT - NOT PRODUCTION")

if __name__ == "__main__":
    main()
