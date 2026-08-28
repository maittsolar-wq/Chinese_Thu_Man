#!/usr/bin/env python3
from __future__ import annotations
import json, re, urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk5"
INPUT = DATA / "hsk5_meanings_candidates_input.json"
URL = "https://hsk.hoctudat.com/tu-vung-hsk-3-0/5"
EXPECTED = 1600

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Accept-Language":"vi,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", errors="replace")

def strip_html(v):
    v = re.sub(r"(?is)<script.*?</script>", " ", v)
    v = re.sub(r"(?is)<style.*?</style>", " ", v)
    v = re.sub(r"<[^>]+>", " ", v)
    return re.sub(r"\s+", " ", unescape(v)).strip()

def nw(v): return re.sub(r"\s+", "", v.strip())
def np(v):
    v = re.sub(r"\s+", "", v.strip().lower())
    return re.sub(r"[1-9]+$", "", v)

def parse(text):
    ref = {}
    pattern = re.compile(
        r"(?P<word>[\u3400-\u9fff]{1,12})\s*\|\s*"
        r"(?P<pinyin>[A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü'·\s]+)"
        r"\s*\|\s*(?:[^|]+\s*\|\s*)?(?P<meaning>[^|\n]{2,300})"
    )
    for m in pattern.finditer(text):
        word, py = nw(m.group("word")), np(m.group("pinyin"))
        meaning = re.sub(r"\s+", " ", m.group("meaning")).strip()
        if word and py and meaning and re.search(r"[À-ỹĐđ]", meaning):
            ref.setdefault((word, py), [])
            if meaning not in ref[(word, py)]:
                ref[(word, py)].append(meaning)
    return ref

def main():
    print("="*72)
    print("HSK 5 MEANING CANDIDATES — HỌC TƯ ĐẠT")
    print("="*72)
    print()
    if not INPUT.exists(): raise SystemExit(f"Missing input: {INPUT}")
    records = json.loads(INPUT.read_text(encoding="utf-8"))
    if not isinstance(records, list) or len(records) != EXPECTED:
        raise SystemExit(f"Expected {EXPECTED} records.")
    ref = parse(strip_html(fetch(URL)))
    print(f"Candidate records:       {len(records)}/{EXPECTED}")
    print(f"Reference mappings:      {len(ref)}")
    before = newly = resolved = 0
    unresolved = []
    for r in records:
        existing = r.get("candidateMeanings", [])
        if not isinstance(existing, list): existing = []
        existing = [x.strip() for x in existing if isinstance(x,str) and x.strip()]
        if existing: before += 1
        key = (nw(r.get("word","")), np(r.get("pinyin","")))
        merged = list(existing)
        seen = {x.casefold() for x in merged}
        for meaning in ref.get(key, []):
            if meaning.casefold() not in seen:
                merged.append(meaning); seen.add(meaning.casefold())
        if not existing and merged: newly += 1
        r["candidateMeanings"] = merged
        if merged:
            r["generationStatus"] = "generated_reference_assisted_unverified"
            r["generationSource"] = "hoctudat_hsk30_vietnamese_reference"
            resolved += 1
        else:
            r["generationStatus"] = "needs_manual_verification"
            r["generationSource"] = "no_vietnamese_reference_match"
            unresolved.append(r["id"])
    INPUT.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print()
    print("SUCCESS")
    print(f"Previously resolved:     {before}/{EXPECTED}")
    print(f"Newly resolved:          {newly}")
    print(f"Total resolved:          {resolved}/{EXPECTED}")
    print(f"Still unresolved:        {len(unresolved)}")
    print(f"Output:                  {INPUT}")
    print("No meaning was invented.")
    print("Base/reviewed/production data was not modified.")
    if unresolved:
        print("First unresolved IDs:")
        print(", ".join(unresolved[:50]))
        if len(unresolved)>50: print(f"... and {len(unresolved)-50} more.")

if __name__ == "__main__":
    main()
