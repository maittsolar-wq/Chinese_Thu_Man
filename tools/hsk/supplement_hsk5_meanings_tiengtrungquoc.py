#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape
from urllib.parse import urljoin
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "hsk" / "hsk5"
INPUT = DATA / "hsk5_meanings_candidates_input.json"
CATEGORY = "https://tiengtrungquoc.net/danh-muc/hsk-5/"
EXPECTED = 1600
WORKERS = 10

def fetch(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "vi,en;q=0.9"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")

def clean_html(value):
    value = re.sub(r"(?is)<script.*?</script>", " ", value)
    value = re.sub(r"(?is)<style.*?</style>", " ", value)
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()

def norm_word(value):
    return re.sub(r"\s+", "", value.strip())

def norm_pinyin(value):
    value = value.strip().lower().replace("’", "'")
    return re.sub(r"\s+", "", value)

def links_from_page(html):
    links = set()
    for href in re.findall(r'''href=["']([^"']+)["']''', html, re.I):
        url = urljoin(CATEGORY, href)
        if "/hsk-5/" in url and "/page/" not in url:
            links.add(url)
    return links

def extract_record(html):
    visible = clean_html(html)

    title = re.search(
        r"(?:Từ|Hán tự)\s*[:：]?\s*([\u3400-\u9fff]{1,20})",
        visible, re.I
    )
    pinyin = re.search(
        r"(?:Phiên âm|Pinyin)\s*[:：]?\s*"
        r"([A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü'·\s]+)",
        visible, re.I
    )
    meaning = re.search(
        r"(?:Nghĩa tiếng Việt|Nghĩa Việt|Nghĩa)\s*[:：]?\s*"
        r"(.{1,500}?)(?=\s+(?:Ví dụ|Câu ví dụ|Example|Tiếng Anh|Nghĩa tiếng Anh)\b|$)",
        visible, re.I
    )

    if not title or not pinyin or not meaning:
        return None

    word = norm_word(title.group(1))
    py = norm_pinyin(pinyin.group(1))
    vi = re.sub(r"\s+", " ", meaning.group(1)).strip(" :;-")

    if not word or not py or not vi or not re.search(r"[À-ỹĐđ]", vi):
        return None

    return word, py, vi

def main():
    print("=" * 72)
    print("HSK 5 MEANING CANDIDATES — TIENGTRUNGQUOC")
    print("=" * 72)
    print()

    if not INPUT.exists():
        raise SystemExit(f"Missing input: {INPUT}")

    records = json.loads(INPUT.read_text(encoding="utf-8"))
    if not isinstance(records, list) or len(records) != EXPECTED:
        raise SystemExit(f"Expected {EXPECTED} records.")

    first = fetch(CATEGORY)
    pages = [CATEGORY]
    m = re.search(r"Trang 1 của (\d+)", clean_html(first), re.I)
    count = min(int(m.group(1)), 107) if m else 107

    for page in range(2, count + 1):
        pages.append(
            f"https://tiengtrungquoc.net/danh-muc/hsk-5/page/{page}/"
        )

    print(f"Category pages: {len(pages)}")

    word_links = set()
    for i, page in enumerate(pages, 1):
        try:
            html = first if i == 1 else fetch(page)
            word_links.update(links_from_page(html))
        except Exception as exc:
            print(f"Page {i} failed: {exc}")

        if i % 10 == 0 or i == len(pages):
            print(f"  page {i}/{len(pages)} -> {len(word_links)} links")

    print(f"Unique word pages: {len(word_links)}")

    reference = {}

    def load_one(url):
        try:
            return extract_record(fetch(url))
        except Exception:
            return None

    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = [pool.submit(load_one, u) for u in word_links]
        for future in as_completed(futures):
            item = future.result()
            if item:
                word, py, vi = item
                key = (word, py)
                reference.setdefault(key, [])
                if vi not in reference[key]:
                    reference[key].append(vi)
            done += 1
            if done % 100 == 0:
                print(f"  word pages fetched: {done}/{len(futures)}")

    print(f"Vietnamese mappings: {len(reference)}")

    before = 0
    newly = 0
    resolved = 0
    unresolved = []

    for record in records:
        existing = record.get("candidateMeanings", [])
        if not isinstance(existing, list):
            existing = []
        existing = [x.strip() for x in existing if isinstance(x, str) and x.strip()]

        if existing:
            before += 1

        key = (
            norm_word(record.get("word", "")),
            norm_pinyin(record.get("pinyin", "")),
        )

        merged = list(existing)
        seen = {x.casefold() for x in merged}

        for vi in reference.get(key, []):
            if vi.casefold() not in seen:
                merged.append(vi)
                seen.add(vi.casefold())

        if not existing and merged:
            newly += 1

        record["candidateMeanings"] = merged

        if merged:
            record["generationStatus"] = "generated_reference_assisted_unverified"
            record["generationSource"] = "tiengtrungquoc_hsk30_vietnamese_reference"
            resolved += 1
        else:
            record["generationStatus"] = "needs_manual_verification"
            record["generationSource"] = "no_vietnamese_reference_match"
            unresolved.append(record["id"])

    INPUT.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print("SUCCESS")
    print(f"Previously resolved: {before}/{EXPECTED}")
    print(f"Newly resolved:       {newly}")
    print(f"Total resolved:       {resolved}/{EXPECTED}")
    print(f"Still unresolved:     {len(unresolved)}")
    print(f"Output:               {INPUT}")
    print()
    print("No meaning was invented.")
    print("Base/reviewed/production data was not modified.")

    if unresolved:
        print()
        print("First unresolved IDs:")
        print(", ".join(unresolved[:50]))
        if len(unresolved) > 50:
            print(f"... and {len(unresolved) - 50} more.")

if __name__ == "__main__":
    main()
