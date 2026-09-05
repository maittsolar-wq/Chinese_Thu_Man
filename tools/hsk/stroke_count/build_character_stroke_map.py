"""
Stroke Count Pass 02 — step 2: build the character -> strokeCount mapping.

Source: Unicode Unihan Database, `kTotalStrokes` field, from the pinned
Unihan.zip release recorded in SOURCE.md (Unicode 17.0.0, retrieved
2026-09-05 from https://www.unicode.org/Public/17.0.0/ucd/Unihan.zip,
sha256 f7a48b2b545acfaa77b2d607ae28747404ce02baefee16396c5d2d7a8ef34b5e).

kTotalStrokes lives in Unihan_IRGSources.txt in this release (verified
directly against the pinned zip — NOT assumed from prior research).
Format confirmed empirically: `U+XXXX<TAB>kTotalStrokes<TAB>VALUE`,
where VALUE was a single unsigned integer for all 102,999 entries in
this release (zero multi-value/region-tagged entries found). The
G-tag-preference logic below is implemented defensively per spec, in
case a future re-pin of this pipeline against a different Unicode
version encounters the historical multi-value format
(e.g. "10 12" or "10:G 12:T") — it is NOT exercised by this run.

Reads only: vocabulary_character_extraction.json (produced by
extract_vocabulary_characters.py) and the pinned raw Unihan extract.
Writes only: character_stroke_map.json, character_review_queue.json.
Touches no production file.
"""
import json
import re
import sys
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
RAW_UNIHAN_EXTRACT = OUT_DIR / "unihan_ktotalstrokes_17.0.0.tsv"

def parse_kTotalStrokes_line(raw_value: str, codepoint: str):
    """
    Returns (strokeCount:int|None, sourceTag:str|None, status:str).
    status is one of: "resolved", "no_g_tag", "invalid_value".
    Defensive multi-value handling per spec; not exercised in this
    pinned release (see module docstring).
    """
    tokens = raw_value.split()
    if len(tokens) == 1:
        token = tokens[0]
        # Defensive: a single token MAY still carry a ":G" style tag in
        # some historical Unihan releases; this pinned release does not,
        # but parse defensively rather than assuming.
        if ":" in token:
            num, tag = token.split(":", 1)
        else:
            num, tag = token, None
        if not re.fullmatch(r"\d+", num):
            return None, None, "invalid_value"
        value = int(num)
        if value <= 0:
            return None, None, "invalid_value"
        return value, tag, "resolved"

    # Multiple space-separated tokens (not observed in this release, but
    # handled per the Pass 01 spec): prefer a G-tagged token.
    parsed = []
    for token in tokens:
        if ":" in token:
            num, tag = token.split(":", 1)
        else:
            num, tag = token, None
        if re.fullmatch(r"\d+", num):
            parsed.append((int(num), tag))
    g_values = [v for v, tag in parsed if tag and "G" in tag]
    if len(g_values) == 1:
        return g_values[0], "G", "resolved"
    return None, None, "no_g_tag"

def load_unihan_map():
    """codepoint (e.g. 'U+5B66') -> raw kTotalStrokes value string."""
    mapping = {}
    with RAW_UNIHAN_EXTRACT.open(encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 3 or parts[1] != "kTotalStrokes":
                continue
            mapping[parts[0]] = parts[2]
    return mapping

def main():
    extraction = json.loads((OUT_DIR / "vocabulary_character_extraction.json").read_text(encoding="utf-8"))
    characters = extraction["distinctCharacters"]
    unihan_raw = load_unihan_map()

    resolved = {}
    review_queue = []

    for ch in characters:
        codepoint = f"U+{ord(ch):04X}"
        raw_value = unihan_raw.get(codepoint)
        if raw_value is None:
            review_queue.append({
                "character": ch, "codepoint": codepoint,
                "reason": "missing_kTotalStrokes",
                "detail": "No kTotalStrokes entry found in the pinned Unihan_IRGSources.txt extract.",
            })
            continue

        stroke_count, source_tag, status = parse_kTotalStrokes_line(raw_value, codepoint)
        if status != "resolved":
            review_queue.append({
                "character": ch, "codepoint": codepoint,
                "reason": status,
                "detail": f"raw kTotalStrokes value was '{raw_value}'",
            })
            continue

        resolved[ch] = {
            "character": ch,
            "codepoint": codepoint,
            "strokeCount": stroke_count,
            "sourceTag": source_tag,
            "sourceVersion": "Unicode 17.0.0 Unihan_IRGSources.txt kTotalStrokes",
        }

    result = {
        "distinctCharactersRequired": len(characters),
        "resolvedCount": len(resolved),
        "unresolvedCount": len(review_queue),
        "coveragePercent": round(100.0 * len(resolved) / len(characters), 4) if characters else 0.0,
        "mapping": resolved,
    }

    (OUT_DIR / "character_stroke_map.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT_DIR / "character_review_queue.json").write_text(
        json.dumps(review_queue, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"distinctCharactersRequired={len(characters)}")
    print(f"resolvedCount={len(resolved)}")
    print(f"unresolvedCount={len(review_queue)}")
    print(f"coveragePercent={result['coveragePercent']}")
    if review_queue:
        print("REVIEW QUEUE:")
        for item in review_queue:
            print(f"  {item}")

if __name__ == "__main__":
    sys.exit(main())
