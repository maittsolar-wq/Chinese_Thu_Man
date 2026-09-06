# Audio Pass 01 — Source Research + License + Coverage + Mapping Audit

**Status: RESEARCH ONLY. Nothing here is integrated into production.**
No production vocabulary file, UI component, or type has been modified by this pass.
This directory is intentionally left **uncommitted** (untracked) per the task's explicit
"do not commit" instruction — it exists so the analysis is reproducible and reviewable,
not as a merge-ready deliverable.

## Contents

- `coverage_analysis.py` — the mapping-generation script. Re-run twice back-to-back
  produces byte-identical output (verified). Requires a local copy of
  `cedict_ts.u8` (see Source below) at the path configured at the top of the file.
- `mapping_draft.json` — READ-ONLY draft mapping artifact, one entry per current
  production vocabulary record (5400 total), each with `id`, `word`, `hskLevel`,
  `pinyin`, `source`, `audioKeyPath`, `mappingStatus` (`matched` / `needs_review` /
  `missing`), `matchTier`, and `normalizedFrom` (for the 12 digit-suffix records).

## Recommended source: `cjhoward/cedict-tts`

- Audio: Baidu Speech TTS-synthesized MP3s, one per distinct CC-CEDICT pronunciation,
  **CC0** (public domain).
  License source: https://github.com/cjhoward/cedict-tts (repo's own `LICENSE`/header
  comments in `tts.py`, read in full — MIT-style permissive on the generation code,
  explicit CC0 dedication on the generated audio output).
- Filenames are keyed by **numeric-tone pinyin** (e.g. `hao3.mp3`, `hao4.mp3`), not by
  hanzi — this is what allows correct disambiguation of homographs (好 hǎo "good" vs
  好 hào "to like" get *different* files), unlike a hanzi-keyed source.
- Underlying dictionary: CC-CEDICT (`cedict_ts.u8`), separately CC BY-SA 3.0 for the
  *text*, but per the source repo's own documentation this does not extend to the
  derived TTS audio, which is dedicated CC0.

## Coverage against current 5400-record production vocabulary (this pass's own count)

| | Count | % |
|---|---|---|
| Matched | 5377 | 99.57% |
| Needs review | 4 | 0.07% |
| Missing (no safe CEDICT entry) | 19 | 0.35% |

Per-level: HSK1 299/300, HSK2 199/200, HSK3 498/500, HSK4 994/1000, HSK5 1597/1600,
HSK6 1790/1800.

Matching strategy (see `coverage_analysis.py` for full logic):
1. **Single-character words**: convert the word's own tone-marked pinyin to an exact
   numeric tone (reliable for one syllable — no segmentation risk) and require an
   *exact* tone match against CEDICT. This is what correctly separates 好/看/还/长
   and all other single-character homographs by actual stored pronunciation, not by
   filename heuristic.
2. **Multi-character words**: since our pinyin field is a fused, unspaced string that
   cannot be safely re-segmented into per-syllable tones, first match on the
   **toneless** (tone-mark-stripped) full string against CEDICT candidates of equal
   syllable count. Where more than one CEDICT candidate ties, resolve by
   reconstructing each candidate's full tone-marked pinyin from its numeric form and
   comparing it directly against our own tone-marked string (uses real tone data
   without needing to segment it). Remaining ties fall back to preferring
   all-lowercase CEDICT entries (CEDICT capitalizes some proper-noun-context
   duplicates). Anything still ambiguous after all of that is left as
   `needs_review` — never silently guessed.
3. Two records (谁 "shéi/shuí", 熟 "shú/shóu") store two alternate pronunciations
   joined by `/` in the source pinyin field itself; these are explicitly flagged
   `needs_review` rather than picking one arbitrarily.

Determinism: `coverage_analysis.py` was run twice with independent output files;
`cmp` confirmed byte-identical results.

## Homograph/sense safety (why cedict-tts over audio-cmn)

39 word-forms in the 5400-record dataset are genuine cross-pronunciation homographs
(same hanzi, different pinyin/sense) — e.g. 好 hǎo/hào, 看 kàn/kān, 还 hái/huán,
长 cháng/zhǎng, 结果 jiéguǒ/jiēguǒ. Of these, **38 have coverage in `audio-cmn`**
(the hanzi-keyed alternative source), meaning a naive hanzi-filename mapping would
serve the exact same recording for every sense — silently wrong audio for at least
one sense in 38 of 39 cases. `cedict-tts`'s pinyin-keyed filenames resolved every one
of these correctly against the word's actual stored tone (verified directly for
好/看/还/长/了/的 above).

## Filename generation fidelity (found during Pass 02 integration)

`cjhoward/cedict-tts`'s own `tts.py` does not simply concatenate CEDICT's raw
numeric-tone syllables into a filename. Before slugifying, it (a) expands a
standalone `r5` erhua syllable to `er5` (e.g. 哪 "na3 r5" → `na3er5.mp3`, not
`na3r5.mp3`), and (b) applies real Mandarin tone-sandhi rules to 一/不 based on
the tone of the immediately following syllable (e.g. 不错 "bu4 cuo4" →
`bu2cuo4.mp3`; 一定 "yi1 ding4" → `yi2ding4.mp3`; 一般 "yi1 ban1" →
`yi4ban1.mp3`). `coverage_analysis.py` v4 replicates both transformations
exactly (`standardize_pinyin_syllables` / `sandhi_correct_tones`); this
affected the *filename* only, never which CEDICT dictionary entry a word
matched (that matching is tone-mark/toneless-based and unaffected by sandhi).
Verified directly against the real upstream repo: 72 filenames that were
initially 404 (naive concatenation) all resolved to `200` once corrected, and
zero previously-"working" filenames changed. All 4969 unique files (covering
5377 matched records) were confirmed present via direct HTTP existence checks
before import.

## 12 digit-suffix records (HSK6 same-hanzi sense splits)

All 12 resolved via Tier-1 exact-tone matching. 局1/局2 and 料1/料2 are
same-pronunciation/different-sense pairs — they correctly map to the *same* audio
file (`ju2.mp3`, `liao4.mp3` respectively), which is phonetically correct even
though the two production records represent different senses.
