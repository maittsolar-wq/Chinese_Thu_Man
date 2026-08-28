#!/usr/bin/env python3
"""HSK 6 Vietnamese meaning candidates — multi-source generation.

Reads:
    data/hsk/hsk6/hsk6_meanings_candidates_input.json

Writes back the same candidate package, preserving existing candidates.

Reference sources:
- CGE HSK 6 Vietnamese vocabulary page
- Laoshi New HSK 6 Vietnamese vocabulary
- HSK Atlas New HSK 3.0 vocabulary pages
- Hanzistroke HSK 6 3.0 page (fallback; English meanings only)

Important:
- Reference-derived Vietnamese meanings are candidates, not ground truth.
- Existing candidates are never overwritten.
- Unresolved records are explicitly marked for later AI-assisted generation.
- No reviewed or production data is modified.
"""

from __future__ import annotations
import csv
import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"data"/"hsk"/"hsk6"
INPUT=DATA/"hsk6_meanings_candidates_input.json"
AI_INPUT=DATA/"hsk6_ai_missing_meanings_input.json"
EXPECTED=1800

URLS=[
    "https://cge.edu.vn/tieng-trung-hsk/tu-vung-hsk-6.html",
    "https://laoshi.io/characters/vi/hsk/new-level6/",
    "https://hskatlas.com/vi/hsk3.0-level6/vocabulary/",
]

def fetch(url):
    req=urllib.request.Request(url,headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36"
    })
    with urllib.request.urlopen(req,timeout=60) as r:
        raw=r.read()
    for enc in ("utf-8","utf-8-sig","cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8","replace")

def norm(s):
    s=html.unescape(str(s or ""))
    s=re.sub(r"<[^>]+>"," ",s)
    s=s.replace("\xa0"," ")
    return re.sub(r"\s+"," ",s).strip()

def strip_pinyin(s):
    # Keep tone-bearing letters; remove slashes/brackets and whitespace.
    s=norm(s).lower()
    s=re.sub(r"[/\[\](){}]", " ", s)
    return re.sub(r"\s+"," ",s).strip()

def add(mapping, word, pinyin, meaning, source):
    word=norm(word)
    pinyin=strip_pinyin(pinyin)
    meaning=norm(meaning)
    if not word or not meaning:
        return
    # Reject obvious headers/labels.
    if word.lower() in {"汉字","汉字","词","từ","hán tự","pinyin","nghĩa tiếng việt"}:
        return
    key=(word,pinyin)
    if key not in mapping:
        mapping[key]={"meaningVi":meaning,"source":source}

def parse_cge(text,mapping):
    # Markdown/HTML tables commonly expose: Hán tự | Pinyin | Nghĩa tiếng Việt.
    clean=re.sub(r"<br\s*/?>"," ",text,flags=re.I)
    rows=re.findall(r"<tr[^>]*>(.*?)</tr>",clean,flags=re.I|re.S)
    for row in rows:
        cells=re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>",row,flags=re.I|re.S)
        vals=[norm(x) for x in cells]
        if len(vals)>=3:
            add(mapping,vals[0],vals[1],vals[2],"CGE")
    # Markdown fallback
    for line in text.splitlines():
        if "|" not in line: continue
        vals=[norm(x) for x in line.split("|") if norm(x)]
        if len(vals)>=3:
            add(mapping,vals[0],vals[1],vals[2],"CGE")

def parse_laoshi(text,mapping):
    # Laoshi pages render vocabulary cards/table with Chinese, pinyin, translation.
    # Try table rows first.
    rows=re.findall(r"<tr[^>]*>(.*?)</tr>",text,flags=re.I|re.S)
    for row in rows:
        cells=re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>",row,flags=re.I|re.S)
        vals=[norm(x) for x in cells]
        if len(vals)>=3:
            add(mapping,vals[0],vals[1],vals[2],"Laoshi")
    # Search compact card patterns: Chinese ... pinyin ... Vietnamese text.
    for m in re.finditer(
        r'<[^>]*>([\u3400-\u9fff]{1,12})</[^>]*>.*?'
        r'([a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü\s/]+).*?'
        r'<[^>]*>([^<]{2,80})</[^>]*>',
        text, re.I|re.S):
        add(mapping,m.group(1),m.group(2),m.group(3),"Laoshi")

def parse_atlas(text,mapping):
    # Atlas may render JSON/HTML; capture explicit Chinese + Vietnamese pairs
    # where Vietnamese marker/translation fields are present.
    patterns=[
        r'"word"\s*:\s*"([^"]+)".{0,1200}?"pinyin"\s*:\s*"([^"]*)".{0,1200}?"(?:meaningVi|vietnamese|translation)"\s*:\s*"([^"]+)"',
        r'"chinese"\s*:\s*"([^"]+)".{0,1200}?"pinyin"\s*:\s*"([^"]*)".{0,1200}?"(?:meaningVi|vietnamese|translation)"\s*:\s*"([^"]+)"',
    ]
    for pat in patterns:
        for m in re.finditer(pat,text,re.I|re.S):
            add(mapping,m.group(1),m.group(2),m.group(3),"HSK Atlas")

def main():
    print("="*72)
    print("HSK 6 MEANING CANDIDATES GENERATION")
    print("="*72)
    print()

    if not INPUT.exists():
        raise SystemExit(f"Missing input: {INPUT}")
    records=json.loads(INPUT.read_text(encoding="utf-8"))
    if len(records)!=EXPECTED:
        raise SystemExit(f"Expected {EXPECTED} records, got {len(records)}")

    mapping={}
    source_counts={}
    for url in URLS:
        print("Reference:",url)
        try:
            text=fetch(url)
            before=len(mapping)
            if "cge.edu.vn" in url:
                parse_cge(text,mapping)
                source="CGE"
            elif "laoshi.io" in url:
                parse_laoshi(text,mapping)
                source="Laoshi"
            else:
                parse_atlas(text,mapping)
                source="HSK Atlas"
            added=len(mapping)-before
            source_counts[source]=source_counts.get(source,0)+added
            print("  Candidate mappings found:",added)
        except Exception as e:
            print("  WARNING:",type(e).__name__,str(e)[:180])
        time.sleep(1)

    resolved=0
    unresolved=[]
    for r in records:
        if r.get("candidateMeanings"):
            resolved+=1
            continue
        key=(norm(r.get("word")),strip_pinyin(r.get("pinyin")))
        hit=mapping.get(key)
        # Second pass: exact Chinese word when pinyin differs only in spacing/tones.
        if not hit:
            hits=[v for (w,p),v in mapping.items() if w==key[0]]
            if len(hits)==1:
                hit=hits[0]
        if hit:
            meaning=hit["meaningVi"]
            r["candidateMeanings"]=[meaning]
            r["selectedMeaningVi"]=meaning
            r["meaningVi"]=meaning
            r["generationStatus"]="reference_assisted"
            r["generationSource"]=hit["source"]
            r["verificationStatus"]="unverified"
            r["humanVerified"]=False
            resolved+=1
        else:
            r["generationStatus"]="needs_ai_assisted_generation"
            r["verificationStatus"]="unverified"
            r["humanVerified"]=False
            unresolved.append(r["id"])

    DATA.mkdir(parents=True,exist_ok=True)
    INPUT.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")

    missing=[r for r in records if r["id"] in set(unresolved)]
    AI_INPUT.write_text(json.dumps(missing,ensure_ascii=False,indent=2),encoding="utf-8")

    print()
    print("SUCCESS")
    print(f"Candidate records:          {len(records)}/{EXPECTED}")
    print(f"Resolved from references:   {resolved}/{EXPECTED}")
    print(f"Needs AI-assisted meaning:  {len(unresolved)}")
    print(f"Output:                      {INPUT}")
    print(f"AI missing input:            {AI_INPUT}")
    print()
    print("IMPORTANT:")
    print("- Reference meanings are candidates, not ground truth.")
    print("- Existing candidates were preserved.")
    print("- No human verification was claimed.")
    print("- Reviewed/production data was not modified.")
    if unresolved:
        print()
        print("Next step: generate AI-assisted Vietnamese meanings for the unresolved batch.")
    else:
        print()
        print("All 1800 records have candidate meanings; proceed to confidence routing.")

if __name__=="__main__":
    main()
