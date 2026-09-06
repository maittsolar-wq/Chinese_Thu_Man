import json, re, unicodedata, os, sys
from collections import Counter

REPO = "d:/Chinese_Thu_Man"
SCRATCH = "C:/Users/User/AppData/Local/Temp/claude/d--Chinese-Thu-Man/29337d40-44ea-4211-819d-b8322527f958/scratchpad/audio_research"
LEVELS = [1, 2, 3, 4, 5, 6]

TONE_MAP = {
    'ā': ('a', 1), 'á': ('a', 2), 'ǎ': ('a', 3), 'à': ('a', 4),
    'ē': ('e', 1), 'é': ('e', 2), 'ě': ('e', 3), 'è': ('e', 4),
    'ī': ('i', 1), 'í': ('i', 2), 'ǐ': ('i', 3), 'ì': ('i', 4),
    'ō': ('o', 1), 'ó': ('o', 2), 'ǒ': ('o', 3), 'ò': ('o', 4),
    'ū': ('u', 1), 'ú': ('u', 2), 'ǔ': ('u', 3), 'ù': ('u', 4),
    'ǖ': ('v', 1), 'ǘ': ('v', 2), 'ǚ': ('v', 3), 'ǜ': ('v', 4),
    'ü': ('v', 0),
}
# Explicit umlaut-family map applied BEFORE NFD decomposition -- NFD-stripping
# combining marks from a precomposed ǚ/ǘ/etc. leaves plain 'u', silently
# losing the umlaut and breaking comparison against CEDICT's ASCII "u:" (v)
# convention. This was a real bug found in v2 (affected 女/绿/旅/律/率 family
# words, ~35 records misclassified as "missing").
UMLAUT_CHARS = {'ǖ': 'v', 'ǘ': 'v', 'ǚ': 'v', 'ǜ': 'v', 'ü': 'v', 'Ü': 'v',
                'Ǖ': 'v', 'Ǘ': 'v', 'Ǚ': 'v', 'Ǜ': 'v'}

TONE_MARK_TABLE = {'a': 'āáǎà', 'e': 'ēéěè', 'i': 'īíǐì', 'o': 'ōóǒò', 'u': 'ūúǔù', 'v': 'ǖǘǚǜ'}

def strip_tone_marks(s: str) -> str:
    for k, v in UMLAUT_CHARS.items():
        s = s.replace(k, v)
    nfd = unicodedata.normalize('NFD', s)
    return ''.join(c for c in nfd if not unicodedata.combining(c)).lower()

def our_pinyin_toneless(pinyin: str) -> str:
    cleaned = re.sub(r"[^A-Za-zÀ-ɏ]", "", pinyin)
    return strip_tone_marks(cleaned)

def clean_our_pinyin_diacritic(pinyin: str) -> str:
    """Lowercased, punctuation/space/apostrophe stripped, tone marks and ü PRESERVED."""
    cleaned = pinyin.replace("'", "").replace("’", "").replace("-", "").replace(" ", "")
    return cleaned.lower()

def single_syllable_to_numeric(syl: str):
    if not re.fullmatch(r"[A-Za-zĀāÁáǍǎÀàĒēÉéĚěÈèĪīÍíǏǐÌìŌōÓóǑǒÒòŪūÚúǓǔÙùǕǖǗǘǙǚǛǜÜü]+", syl):
        return None
    tone = 5
    out_chars = []
    for ch in syl:
        lower = ch.lower()
        if lower in UMLAUT_CHARS:
            out_chars.append('v')
            continue
        if lower in TONE_MAP:
            base, t = TONE_MAP[lower]
            if t != 0:
                tone = t
            out_chars.append(base)
        else:
            out_chars.append(lower)
    return ''.join(out_chars) + str(tone)

def syllable_num_to_diacritic(syl: str):
    m = re.match(r'^([a-z:]+)([0-9])$', syl.lower())
    if not m:
        return None
    letters, tone = m.group(1), int(m.group(2))
    letters = letters.replace('u:', 'v')
    if tone == 5 or tone == 0:
        return letters.replace('v', 'ü')
    if 'a' in letters:
        idx = letters.index('a')
    elif 'e' in letters:
        idx = letters.index('e')
    elif 'ou' in letters:
        idx = letters.index('o')
    else:
        vowels = [i for i, c in enumerate(letters) if c in 'aeiouv']
        if not vowels:
            return None
        idx = vowels[-1]
    ch = letters[idx]
    if ch not in TONE_MARK_TABLE:
        return None
    marked = TONE_MARK_TABLE[ch][tone - 1]
    return (letters[:idx] + marked + letters[idx+1:]).replace('v', 'ü')

def candidate_to_diacritic_string(syllables):
    parts = []
    for s in syllables:
        d = syllable_num_to_diacritic(s)
        if d is None:
            return None
        parts.append(d)
    return "".join(parts)

# ---------- parse CEDICT ----------
cedict_by_simplified = {}
with open(f"{SCRATCH}/cedict_ts.u8", encoding="utf-8") as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        m = re.match(r"^(\S+)\s+(\S+)\s+\[([^\]]+)\]\s+/", line)
        if not m:
            continue
        trad, simp, pinyin_bracket = m.groups()
        syllables = pinyin_bracket.split(" ")
        cedict_by_simplified.setdefault(simp, []).append(syllables)

def cedict_toneless(syllables):
    return "".join(re.sub(r"[0-9]", "", s).lower().replace("u:", "v") for s in syllables)

def cedict_numeric_lower(syllables):
    return "".join(s.lower().replace("u:", "v") for s in syllables)

def is_all_lowercase_initial(syllables):
    return all(s[0:1].islower() for s in syllables if s)

# ---------- upstream filename-generation fidelity fix ----------
# cjhoward/cedict-tts's own tts.py does NOT simply concatenate CEDICT's raw
# numeric syllables into a filename. It first (a) expands a standalone 'r5'
# erhua syllable to 'er5', then (b) applies real Mandarin tone-sandhi rules to
# 一/不 based on the tone of the immediately following syllable. Skipping
# these means computing a filename that doesn't exist on disk even though the
# underlying dictionary-entry MATCH (word identity / sense) is correct --
# verified by direct HTTP existence checks against the real upstream repo
# (see tools/hsk/audio_research/README.md, "Filename generation fidelity").
def standardize_pinyin_syllables(syllables):
    return ['er5' if s.lower() == 'r5' else s.lower().replace('u:', 'v') for s in syllables]

def sandhi_correct_tones(word, syllables):
    out = list(syllables)
    for i, ch in enumerate(word):
        if ch in ('一', '不'):  # 一 or 不
            if i + 1 < len(syllables):
                next_tone = int(re.sub(r'[^0-9]', '', syllables[i + 1]) or 0)
                tone = int(re.sub(r'[^0-9]', '', syllables[i]) or 0)
                if next_tone == 4:
                    tone = 2
                elif next_tone != 5:
                    tone = 4
                out[i] = re.sub(r'[0-9]+$', str(tone), syllables[i])
    return out

def generate_audio_filename(lookup_word, syllables):
    std = standardize_pinyin_syllables(syllables)
    corrected = sandhi_correct_tones(lookup_word, std)
    return ''.join(corrected) + '.mp3'

# ---------- load production (fresh, sorted for determinism) ----------
all_records = []
for lvl in LEVELS:
    d = json.load(open(f"{REPO}/data/hsk/hsk{lvl}/hsk{lvl}_vocabulary_production.json", encoding="utf-8"))
    all_records.extend(d)
all_records.sort(key=lambda r: r["id"])

DIGIT_SUFFIX_RE = re.compile(r"^([\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+)([1-9])$")

matched = []
missing = []
needs_review = []  # ambiguous even after all tie-breaks, OR special-format (slash dual-pronunciation)

for r in all_records:
    word = r["word"]
    rid = r["id"]
    lvl = int(rid.split("_")[0].replace("hsk", ""))
    our_pinyin = r["pinyin"]

    record_base = {"id": rid, "word": word, "hskLevel": lvl, "pinyin": our_pinyin, "normalizedFrom": None}

    if "/" in our_pinyin:
        needs_review.append({**record_base, "tier": "0-special-format-dual-pronunciation",
                              "reason": "source pinyin lists multiple alternate readings separated by '/'; "
                                        "cannot safely auto-select a single audio recording without an "
                                        "explicit editorial decision on which reading is primary"})
        continue

    our_toneless = our_pinyin_toneless(our_pinyin)
    our_diacritic_clean = clean_our_pinyin_diacritic(our_pinyin)

    lookup_word = word
    m = DIGIT_SUFFIX_RE.match(word)
    normalized_from = None
    if m:
        lookup_word = m.group(1)
        normalized_from = word
        record_base["normalizedFrom"] = normalized_from

    candidates = cedict_by_simplified.get(lookup_word, [])
    candidates = [c for c in candidates if len(c) == len(lookup_word)]

    if len(lookup_word) == 1:
        our_numeric = single_syllable_to_numeric(our_pinyin.strip())
        exact_tone_matches = []
        if our_numeric is not None:
            seen = {}
            for c in candidates:
                if cedict_numeric_lower(c) == our_numeric:
                    seen.setdefault(cedict_numeric_lower(c), c)
            exact_tone_matches = list(seen.values())

        if len(exact_tone_matches) == 1:
            syl = exact_tone_matches[0]
            matched.append({**record_base, "tier": "1-exact-tone",
                             "cedictPinyin": " ".join(syl), "audioFilename": generate_audio_filename(lookup_word, syl)})
            continue
        elif len(exact_tone_matches) > 1:
            needs_review.append({**record_base, "tier": "1-exact-tone-still-ambiguous",
                                  "candidates": exact_tone_matches})
            continue
        toneless_matches = [c for c in candidates if cedict_toneless(c) == our_toneless]
        if len(toneless_matches) == 1:
            syl = toneless_matches[0]
            matched.append({**record_base, "tier": "1-toneless-fallback",
                             "cedictPinyin": " ".join(syl), "audioFilename": generate_audio_filename(lookup_word, syl)})
        elif len(toneless_matches) > 1:
            needs_review.append({**record_base, "tier": "1-toneless-fallback-ambiguous",
                                  "candidates": toneless_matches})
        else:
            missing.append({**record_base, "cedictCandidates": candidates})
    else:
        toneless_matches = [c for c in candidates if cedict_toneless(c) == our_toneless]

        if len(toneless_matches) == 1:
            syl = toneless_matches[0]
            matched.append({**record_base, "tier": "2-toneless",
                             "cedictPinyin": " ".join(syl), "audioFilename": generate_audio_filename(lookup_word, syl)})
        elif len(toneless_matches) > 1:
            # Step 1: exact full diacritic reconstruction against our own
            # stored tone-marked pinyin (uses REAL tone info, not a heuristic)
            exact_recon = []
            for c in toneless_matches:
                recon = candidate_to_diacritic_string(c)
                if recon is not None and recon == our_diacritic_clean:
                    exact_recon.append(c)
            dedup_recon = {cedict_numeric_lower(c): c for c in exact_recon}
            if len(dedup_recon) == 1:
                syl = list(dedup_recon.values())[0]
                matched.append({**record_base, "tier": "2-diacritic-reconstruction",
                                 "cedictPinyin": " ".join(syl), "audioFilename": generate_audio_filename(lookup_word, syl),
                                 "rawCandidateCount": len(toneless_matches)})
                continue
            # Step 2: lowercase-initial tie-break (drops CEDICT proper-noun /
            # duplicate capitalized entries) -- only used when reconstruction
            # itself didn't already resolve it (i.e. dedup_recon was empty or
            # still >1, meaning tone info didn't disambiguate)
            lowercase_only = [c for c in toneless_matches if is_all_lowercase_initial(c)]
            dedup_lower = {cedict_numeric_lower(c) for c in lowercase_only}
            if len(dedup_lower) == 1 and len(dedup_recon) == 0:
                syl = next(c for c in lowercase_only if cedict_numeric_lower(c) in dedup_lower)
                matched.append({**record_base, "tier": "2-toneless-lowercase-tiebreak",
                                 "cedictPinyin": " ".join(syl), "audioFilename": generate_audio_filename(lookup_word, syl),
                                 "rawCandidateCount": len(toneless_matches)})
            else:
                needs_review.append({**record_base, "tier": "2-genuinely-ambiguous",
                                      "candidates": toneless_matches,
                                      "reconstructionMatches": exact_recon,
                                      "lowercaseCandidates": lowercase_only,
                                      "note": "0 exact-tone reconstruction matches (our stored tone pattern "
                                              "doesn't exactly match any CEDICT citation form)" if len(exact_recon) == 0
                                              else "reconstruction still ambiguous"})
        else:
            missing.append({**record_base, "cedictCandidates": candidates})

print(f"matched: {len(matched)}  missing: {len(missing)}  needs_review: {len(needs_review)}")
print(f"TOTAL: {len(matched)}/{len(all_records)} ({100*len(matched)/len(all_records):.2f}%)")

by_level = Counter(m["hskLevel"] for m in matched)
by_level_total = Counter(r["id"].split("_")[0].replace("hsk", "") for r in all_records)
totals = {1: 300, 2: 200, 3: 500, 4: 1000, 5: 1600, 6: 1800}
print()
for lvl in LEVELS:
    print(f"HSK{lvl}: {by_level.get(lvl,0)}/{totals[lvl]} ({100*by_level.get(lvl,0)/totals[lvl]:.2f}%)")

print("\nmatched by tier:", dict(Counter(m["tier"] for m in matched)))
print("needs_review by tier:", dict(Counter(n["tier"] for n in needs_review)))

os.makedirs(f"{SCRATCH}/output", exist_ok=True)
out = {
    "generatedFrom": "cedict_coverage_analysis_v4.py",
    "totalRecords": len(all_records),
    "matchedCount": len(matched),
    "missingCount": len(missing),
    "needsReviewCount": len(needs_review),
    "matched": matched,
    "missing": missing,
    "needsReview": needs_review,
}
outfile = sys.argv[1] if len(sys.argv) > 1 else f"{SCRATCH}/output/cedict_tts_coverage_v4.json"
with open(outfile, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=False)
print(f"\nsaved to {outfile}")
