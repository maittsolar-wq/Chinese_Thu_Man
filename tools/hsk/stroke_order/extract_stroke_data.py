"""
STROKE ORDER PASS 02 -- character-level stroke-data asset extraction.

Builds the exact 1940-character inventory required by the current 5400 HSK
vocabulary records (normalizing the 12 known digit-suffix records to their
real underlying Han character), extracts ONLY those characters from Make Me
a Hanzi's graphics.txt, and writes one minimal JSON asset per character to
app/public/stroke-data/<codepoint-hex>.json.

Does NOT touch any vocabulary JSON file, the adapter, strokeCount, audio,
relatedWordIds, examples, or characterIds. Read-only against production data.

Usage:
  python extract_stroke_data.py --dry-run   (report only, no file writes)
  python extract_stroke_data.py --apply     (writes app/public/stroke-data/)
"""
import json, re, os, argparse, sys

REPO = "d:/Chinese_Thu_Man"
GRAPHICS_TXT = ("C:/Users/User/AppData/Local/Temp/claude/d--Chinese-Thu-Man/"
                "29337d40-44ea-4211-819d-b8322527f958/scratchpad/stroke_order_research/graphics.txt")
OUT_DIR = f"{REPO}/app/public/stroke-data"
LEVELS = [1, 2, 3, 4, 5, 6]

DIGIT_SUFFIX_RE = re.compile(r"^([\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+)([1-9])$")


def build_character_inventory():
    """Returns (distinct_chars: set[str], per_char_records: dict[str, list[str]])."""
    distinct_chars = set()
    char_to_record_ids = {}
    for lvl in LEVELS:
        path = f"{REPO}/data/hsk/hsk{lvl}/hsk{lvl}_vocabulary_production.json"
        records = json.load(open(path, encoding="utf-8"))
        for r in records:
            word = r["word"]
            m = DIGIT_SUFFIX_RE.match(word)
            lookup = m.group(1) if m else word
            for ch in lookup:
                distinct_chars.add(ch)
                char_to_record_ids.setdefault(ch, []).append(r["id"])
    return distinct_chars, char_to_record_ids


def codepoint_hex(ch: str) -> str:
    return format(ord(ch), "x")


def parse_graphics_txt(needed: set):
    """Returns dict[char] = {"character":..., "strokes":[...], "medians":[...]}."""
    found = {}
    with open(GRAPHICS_TXT, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            ch = obj["character"]
            if ch in needed:
                found[ch] = {
                    "character": ch,
                    "strokes": obj["strokes"],
                    "medians": obj["medians"],
                }
    return found


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    inventory, char_to_ids = build_character_inventory()
    print(f"required character inventory: {len(inventory)} (expected 1940)")
    if len(inventory) != 1940:
        print("FATAL: inventory count does not match expected 1940. Aborting.")
        sys.exit(1)

    extracted = parse_graphics_txt(inventory)
    print(f"extracted from graphics.txt: {len(extracted)} / {len(inventory)}")

    missing = inventory - set(extracted.keys())
    if missing:
        print(f"FATAL: {len(missing)} characters missing from source data. Aborting.")
        print("missing:", sorted(missing))
        sys.exit(1)

    # validate structural integrity before writing anything
    bad = []
    for ch, obj in extracted.items():
        strokes = obj.get("strokes") or []
        medians = obj.get("medians") or []
        if not strokes or not medians or len(strokes) != len(medians):
            bad.append((ch, len(strokes), len(medians)))
    if bad:
        print(f"FATAL: {len(bad)} characters have malformed strokes/medians. Aborting.")
        print(bad[:20])
        sys.exit(1)
    print("structural validation: all 1940 characters have non-empty, length-matched strokes/medians.")

    # check for codepoint filename collisions (should be impossible -- one char per codepoint)
    filenames = {}
    for ch in extracted:
        fname = codepoint_hex(ch) + ".json"
        if fname in filenames:
            print(f"FATAL: codepoint collision {fname} for {ch!r} and {filenames[fname]!r}")
            sys.exit(1)
        filenames[fname] = ch
    print(f"filename mapping: {len(filenames)} unique codepoint-based filenames, zero collisions.")

    if args.apply:
        os.makedirs(OUT_DIR, exist_ok=True)
        for ch, obj in extracted.items():
            fname = codepoint_hex(ch) + ".json"
            path = os.path.join(OUT_DIR, fname)
            # Use compact-but-readable JSON; ensure_ascii=False keeps the
            # character itself human-readable, and CRLF is NOT applied here
            # (these are new binary-adjacent static assets, not part of the
            # repo's existing CRLF-convention source-controlled JSON files).
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
        print(f"WROTE {len(extracted)} files to {OUT_DIR}")
    else:
        print("DRY RUN -- no files written")

    # save inventory + mapping for the validator / manifest to reuse
    manifest_helper = {
        "requiredCharacterCount": len(inventory),
        "extractedCount": len(extracted),
        "characters": sorted(inventory),
        "codepointFilenames": {ch: codepoint_hex(ch) + ".json" for ch in sorted(inventory)},
    }
    helper_path = f"{REPO}/tools/hsk/stroke_order/character_inventory.json"
    if args.apply:
        with open(helper_path, "w", encoding="utf-8", newline="\r\n") as f:
            f.write(json.dumps(manifest_helper, ensure_ascii=False, indent=2))
        print(f"saved inventory helper to {helper_path}")


if __name__ == "__main__":
    main()
