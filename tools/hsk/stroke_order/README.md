# Stroke Order — Production Data

**Source:** [Make Me a Hanzi](https://github.com/skishore/makemeahanzi), `graphics.txt`
(commit `bddc96d41bef78427ed0e034e9f7e31d71fd1b92`, 2026-03-08), 9574 characters total.

**Data license: Arphic Public License** — see [ARPHICPL.TXT](ARPHICPL.TXT) in this
directory (also co-located at `app/public/stroke-data/ARPHICPL.TXT` alongside the
distributed data itself, satisfying the license's requirement to retain the license
file unaltered with any copy). This is **DATA licensing**, entirely separate from
and not to be confused with the MIT code license used by unrelated third-party
rendering libraries such as Hanzi Writer — no Hanzi Writer code or license is used
anywhere in this project; the stroke viewer is original code.

## What was extracted

Exactly the **1940 distinct Han characters** required by the current 5400-record HSK
vocabulary inventory (not the full 9574-character source). The 12 known digit-suffix
records (乘2, 局1, 局2, 料1, 料2, 露1, 所2, 该2, 副2, 升2, 则1, 支2) are normalized to
their real underlying character before lookup — stroke data is stored once per real
character, never as a separate "digit-suffix" entry.

Each extracted character keeps only `character`, `strokes` (SVG path data, one per
stroke), and `medians` (per-stroke centerline point arrays, preserved for future
Trace/Write/Quiz features — not used by this pass's viewer, but not discarded).
All other Make Me a Hanzi fields (e.g. `radStrokes`) were dropped as unnecessary.

## License compliance — this IS a "modification" under the Arphic Public License

Subsetting and reformatting 9574 characters' worth of one large text file into 1940
individual per-character JSON files is a modification under APL §2. Per §2(a)/(b):
- **How/when changed**: documented in [production_manifest.json](production_manifest.json)
  (extraction method, date, source commit).
- **Kept Freely Available**: the modified subset is served as a public static asset
  from `app/public/stroke-data/<codepoint>.json` — fetchable by anyone who visits the
  site, exactly as the original `graphics.txt` was itself freely available. No stroke
  geometry was altered; only which characters are included and which fields are kept.

Commercial use, redistribution, and modification are all permitted by the license
text; there is no prohibition on bundling in a commercial web or (later) Flutter
product, provided the above conditions are met.

## Storage

`app/public/stroke-data/<codepoint-hex>.json` — lowercase hex Unicode codepoint,
no `U+` prefix (e.g. `5b66.json` for 学, U+5B66). Chosen specifically to avoid
URL-encoding and filesystem edge cases that raw CJK filenames would introduce.

1940 files, 4,901,063 bytes total (~4.7 MB), average ~2.5 KB/character. Never loaded
in bulk — see `app/src/lib/data/strokeOrderLoader.ts` for the on-demand fetch used by
the Stroke Order viewer, which derives the needed characters directly from
`VocabularyWord.word` at render time (no vocabulary JSON schema change).

## Relationship to existing `strokeCount`

Completely separate concern. Production `VocabularyWord.strokeCount` (word-level sum,
Unihan `kTotalStrokes`-derived, integrated in the Stroke Count pass) is never read,
written, or reconciled by this pass. Two characters (范, 骨) have a well-known,
1-stroke cross-source discrepancy between Unihan's count and Make Me a Hanzi's stroke
array length — documented in the manifest, left as-is on both sides intentionally.

## Determinism

`extract_stroke_data.py` produces byte-identical output across independent runs
(verified for this pass).
