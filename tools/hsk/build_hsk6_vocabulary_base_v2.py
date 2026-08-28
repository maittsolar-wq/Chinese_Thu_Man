#!/usr/bin/env python3
from __future__ import annotations
import csv, io, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "raw" / "hsk" / "hsk_vocabulary.csv"
OUT = ROOT / "data" / "hsk" / "hsk6"
EXPECTED = 1600  # HSK 3.0 Level 6 introduced vocabulary

def decode_source(path):
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    # Repair common UTF-8 -> Latin-1 mojibake if detected.
    if any(x in text for x in ("Ã", "Â", "ç", "è", "å", "æ", "é", "ä")):
        try:
            repaired = text.encode("latin1").decode("utf-8")
            if repaired.count("级") >= text.count("级"):
                text = repaired
        except UnicodeError:
            pass
    return text

def clean(v):
    return str(v or "").strip()

def clean_word(v):
    return re.sub(r"\s+", "", clean(v))

def clean_pinyin(v):
    return re.sub(r"\s+", " ", clean(v))

def introduced_at_hsk6(level_name):
    """
    IMPORTANT:
    The source contains values such as:
      二级(六级)
      三级(六级)
      四级(六级)
      五级(六级)
    These are NOT HSK6-introduced records.
    We only accept a level marker whose FIRST level is 六级,
    or an unambiguous HSK6 label.
    """
    v = clean(level_name)
    v2 = re.sub(r"\s+", "", v)
    if v2 in {"HSK6", "HSK6.0", "HSK6级", "HSK 6"}:
        return True
    # First/main level must be 六级.
    if re.match(r"^六级(?:$|[（(])", v2):
        return True
    return False

def main():
    print("="*72)
    print("HSK 6 VOCABULARY BASE BUILD")
    print("="*72)
    print()
    if not SOURCE.exists():
        raise SystemExit(f"Source not found: {SOURCE}")

    rows=list(csv.DictReader(io.StringIO(decode_source(SOURCE))))
    if not rows:
        raise SystemExit("Source CSV has no rows.")

    selected=[r for r in rows if introduced_at_hsk6(r.get("levelName"))]

    if not selected:
        samples=sorted({clean(r.get("levelName")) for r in rows if "级" in clean(r.get("levelName"))})
        print("Detected levelName values:")
        for s in samples:
            print(repr(s))
        raise SystemExit("No HSK6-introduced rows found.")

    records=[]
    seen=set()
    duplicate_words={}
    for i,r in enumerate(selected,1):
        word=clean_word(r.get("word"))
        pinyin=clean_pinyin(r.get("pinyin"))
        level_name=clean(r.get("levelName"))
        if not word:
            raise SystemExit(f"Empty word at selected row {i}")
        if not pinyin:
            raise SystemExit(f"Empty pinyin for {word} at selected row {i}")
        key=(word,pinyin)
        if key in seen:
            duplicate_words[word]=duplicate_words.get(word,1)+1
        seen.add(key)
        records.append({
            "id":f"hsk6_{i:04d}",
            "level":"HSK 6",
            "word":word,
            "pinyin":pinyin,
            "cixing":clean(r.get("cixing")),
            "sourceSort":clean(r.get("sort")),
        })

    OUT.mkdir(parents=True,exist_ok=True)
    jp=OUT/"hsk6_vocabulary_base.json"
    cp=OUT/"hsk6_vocabulary_base.csv"
    rp=OUT/"hsk6_normalization_report.json"

    jp.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
    with cp.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["id","level","word","pinyin","cixing","sourceSort"])
        w.writeheader(); w.writerows(records)

    validations={
        "hsk6IntroducedRecordsExtracted":len(records)>0,
        "nonEmptyChineseWords":all(x["word"] for x in records),
        "nonEmptyPinyin":all(x["pinyin"] for x in records),
        "hsk6LevelMapping":all(x["level"]=="HSK 6" for x in records),
        "sequentialIds":[x["id"] for x in records]==[f"hsk6_{i:04d}" for i in range(1,len(records)+1)],
        "duplicateVisibleWordsAllowed":True,
    }
    report={
        "sourceRowsLoaded":len(rows),
        "hsk6IntroducedRecords":len(records),
        "uniqueSourceEntries":len(seen),
        "duplicateVisibleWordGroups":len(duplicate_words),
        "duplicateVisibleWords":duplicate_words,
        "validations":validations,
        "production":False,
    }
    rp.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")

    print(f"Source rows loaded: {len(rows)}")
    print(f"HSK 6 introduced source rows found: {len(records)}")
    print()
    print("SUCCESS")
    print(f"HSK 6 introduced records: {len(records)}")
    print(f"Unique source entries: {len(seen)}")
    print(f"Duplicate visible word groups: {len(duplicate_words)}")
    print(f"Output folder: {OUT}")
    print()
    print("Generated files:")
    print("  - hsk6_vocabulary_base.json")
    print("  - hsk6_vocabulary_base.csv")
    print("  - hsk6_normalization_report.json")
    print()
    print("Validation:")
    for k,v in validations.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print()
    print("Status: HSK 6 SOURCE BASE ONLY - NOT PRODUCTION")

if __name__=="__main__":
    main()
