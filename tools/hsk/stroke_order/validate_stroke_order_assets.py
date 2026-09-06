"""
Stroke Order Pass 02 -- dedicated asset validator.

Validates the extracted app/public/stroke-data/ assets against the current
5400-record production vocabulary inventory. Read-only.
"""
import json, os, re, sys
from collections import Counter

REPO = "d:/Chinese_Thu_Man"
LEVELS = [1, 2, 3, 4, 5, 6]
STROKE_DATA_DIR = f"{REPO}/app/public/stroke-data"
DIGIT_SUFFIX_RE = re.compile(r"^([\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+)([1-9])$")

failures = []
def check(label, cond, detail=""):
    print(f"[{'PASS' if cond else 'FAIL'}] {label}" + (f" -- {detail}" if detail and not cond else ""))
    if not cond:
        failures.append((label, detail))

# ---------- rebuild required inventory fresh from production ----------
inventory = set()
for lvl in LEVELS:
    d = json.load(open(f"{REPO}/data/hsk/hsk{lvl}/hsk{lvl}_vocabulary_production.json", encoding="utf-8"))
    for r in d:
        m = DIGIT_SUFFIX_RE.match(r["word"])
        lookup = m.group(1) if m else r["word"]
        inventory |= set(lookup)

check("required character inventory = 1940", len(inventory) == 1940, f"got {len(inventory)}")

def codepoint_hex(ch):
    return format(ord(ch), "x")

expected_files = {codepoint_hex(ch) + ".json": ch for ch in inventory}

print("\n=== ASSET FILES ===")
all_files = [f for f in os.listdir(STROKE_DATA_DIR) if f.endswith(".json")]
check("file count = 1940", len(all_files) == 1940, f"got {len(all_files)}")

missing_files = set(expected_files) - set(all_files)
extra_files = set(all_files) - set(expected_files)
check("every required character has one JSON file", len(missing_files) == 0, f"missing: {missing_files}")
check("no unexpected extra JSON files", len(extra_files) == 0, f"extra: {extra_files}")

print("\n=== PER-FILE STRUCTURAL VALIDATION ===")
parse_errors = []
char_mismatch = []
missing_strokes = []
missing_medians = []
empty_strokes = []
empty_medians = []
length_mismatch = []
malformed_paths = []
seen_characters = Counter()

for fname, expected_char in expected_files.items():
    path = os.path.join(STROKE_DATA_DIR, fname)
    try:
        with open(path, encoding="utf-8") as f:
            obj = json.load(f)
    except Exception as e:
        parse_errors.append((fname, str(e)))
        continue

    if obj.get("character") != expected_char:
        char_mismatch.append((fname, expected_char, obj.get("character")))

    seen_characters[obj.get("character")] += 1

    strokes = obj.get("strokes")
    medians = obj.get("medians")
    if strokes is None:
        missing_strokes.append(fname)
    elif len(strokes) == 0:
        empty_strokes.append(fname)
    if medians is None:
        missing_medians.append(fname)
    elif len(medians) == 0:
        empty_medians.append(fname)
    if strokes is not None and medians is not None and len(strokes) != len(medians):
        length_mismatch.append((fname, len(strokes), len(medians)))

    if strokes:
        for i, s in enumerate(strokes):
            if not isinstance(s, str) or not s.strip().upper().startswith("M"):
                malformed_paths.append((fname, i))

check("every JSON parses", len(parse_errors) == 0, str(parse_errors[:10]))
check("character field matches filename/codepoint", len(char_mismatch) == 0, str(char_mismatch[:10]))
check("strokes field exists on every asset", len(missing_strokes) == 0, str(missing_strokes[:10]))
check("medians field exists on every asset", len(missing_medians) == 0, str(missing_medians[:10]))
check("strokes.length > 0 for every asset", len(empty_strokes) == 0, str(empty_strokes[:10]))
check("medians.length > 0 for every asset", len(empty_medians) == 0, str(empty_medians[:10]))
check("strokes.length === medians.length for every asset", len(length_mismatch) == 0, str(length_mismatch[:10]))
check("no malformed stroke paths (must start with SVG moveto 'M')", len(malformed_paths) == 0, str(malformed_paths[:10]))

dup_chars = {c: n for c, n in seen_characters.items() if n > 1}
check("no duplicate character assets", len(dup_chars) == 0, str(dup_chars))

print("\n=== REPRESENTATIVE CHARACTER SPOT CHECKS ===")
for ch in ["学", "习", "人", "爱", "中", "国", "你", "好"]:
    fname = codepoint_hex(ch) + ".json"
    path = os.path.join(STROKE_DATA_DIR, fname)
    ok = os.path.exists(path)
    if ok:
        obj = json.load(open(path, encoding="utf-8"))
        ok = obj["character"] == ch and len(obj["strokes"]) == len(obj["medians"]) > 0
    check(f"{ch} ({fname})", ok)

print("\n=== MULTI-CHARACTER WORD RESOLUTION ===")
for word in ["学习", "学生", "爱情", "可爱"]:
    for ch in word:
        fname = codepoint_hex(ch) + ".json"
        check(f"'{word}' -> character '{ch}' asset exists", os.path.exists(os.path.join(STROKE_DATA_DIR, fname)))

print("\n=== DIGIT-SUFFIX RECORD RESOLUTION ===")
digit_suffix_words = {
    "乘2": "乘", "局1": "局", "局2": "局", "料1": "料", "料2": "料", "露1": "露",
    "所2": "所", "该2": "该", "副2": "副", "升2": "升", "则1": "则", "支2": "支",
}
for word, expected_char in digit_suffix_words.items():
    m = DIGIT_SUFFIX_RE.match(word)
    resolved = m.group(1) if m else word
    check(f"{word} -> resolves to {expected_char}", resolved == expected_char)
    fname = codepoint_hex(resolved) + ".json"
    check(f"{word} -> asset {fname} exists", os.path.exists(os.path.join(STROKE_DATA_DIR, fname)))

print("\n" + "=" * 50)
if failures:
    print(f"RESULT: {len(failures)} FAILURE(S)")
    sys.exit(1)
else:
    print("RESULT: ALL CHECKS PASSED (1940/1940 valid)")
    sys.exit(0)
