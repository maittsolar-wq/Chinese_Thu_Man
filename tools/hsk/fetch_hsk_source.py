#!/usr/bin/env python3
"""Fetch the pinned HSK vocabulary source for the Chinese Thu Man data pipeline."""

from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://raw.githubusercontent.com/profesorm/hsk30/main/data/hsk_vocabulary.csv"
OUT = Path("data/raw/hsk/hsk_vocabulary.csv")

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    req = Request(URL, headers={"User-Agent": "Chinese-Thu-Man-Data-Pipeline/1.0"})
    with urlopen(req, timeout=30) as response:
        data = response.read()
    OUT.write_bytes(data)
    print(f"Saved {len(data):,} bytes to {OUT}")

if __name__ == "__main__":
    main()
