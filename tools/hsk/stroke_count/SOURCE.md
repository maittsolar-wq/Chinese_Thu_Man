# Stroke Count Source — Unicode Unihan Database

## Source

- **Source name:** Unicode Han Database (Unihan)
- **Property used:** `kTotalStrokes` (total stroke count of the character's representative glyph, including the radical)
- **Release:** Unicode 17.0.0
- **Official source URL:** https://www.unicode.org/Public/17.0.0/ucd/Unihan.zip
- **Archive SHA-256:** `f7a48b2b545acfaa77b2d607ae28747404ce02baefee16396c5d2d7a8ef34b5e`
- **File containing `kTotalStrokes` in this release:** `Unihan_IRGSources.txt` (internal header: `Date: 2025-07-24 00:00:00 GMT [KL]`, `Unicode Version 17.0.0`) — verified directly against the pinned archive, not assumed from prior documentation.
- **Retrieved:** 2026-09-05

## License

Unicode License v3 (https://www.unicode.org/license.txt). Verified directly: permits use, copy, modify, merge, publish, distribute, and sell copies of Unicode Data Files, subject to two conditions:

1. The copyright notice (reproduced below) must accompany all copies, either directly in the files or in accompanying documentation.
2. Unicode, Inc.'s name may not be used in advertising/promotion of derivative products without prior written permission.

Copyright notice (from `Unihan_IRGSources.txt`):

```
© 2025 Unicode®, Inc.
Unicode and the Unicode Logo are registered trademarks of Unicode, Inc.
in the U.S. and other countries.
For terms of use and license, see https://www.unicode.org/terms_of_use.html
```

## How this source is used in this repository

Only the `kTotalStrokes` lines for the 1940 distinct Han characters actually
present in this project's HSK1–6 vocabulary (`data/hsk/hsk{1..6}/hsk{N}_vocabulary_production.json`,
`word` field, after stripping the 12 known digit-suffix disambiguation
artifacts) were extracted into `unihan_ktotalstrokes_17.0.0.tsv` — a
filtered subset, not the full ~8.1 MB `Unihan.zip` or the full
~13.3 MB `Unihan_IRGSources.txt`. The full original archive was not
committed to the repository.

To regenerate this extract against a different Unicode release, re-run
`extract_vocabulary_characters.py` against updated production data, then
re-filter a freshly downloaded `Unihan_IRGSources.txt` to the resulting
character list.

## Format notes (verified against this specific pinned release)

`kTotalStrokes` lines have the form `U+XXXX<TAB>kTotalStrokes<TAB>VALUE`.
In Unicode 17.0.0, **every one of the 102,999 `kTotalStrokes` entries in
the full file carries exactly one integer value** — no space-separated
multi-value or region-tagged (`G`/`T`/`J`/...) entries were found. A
separate, much rarer field, `kAlternateTotalStrokes` (105 entries in this
release, all in obscure CJK Extension A characters, format `N:J` etc.),
exists for cases where a regional source disagrees with the primary
value — none of this project's 1940 characters use it.

`build_character_stroke_map.py` still implements defensive parsing for a
hypothetical multi-value `kTotalStrokes` line (preferring a `G`-tagged
token, matching general Unihan documentation for older format
conventions) in case a future re-pin against a different Unicode version
encounters it — this code path is not exercised by the current pinned
release, and this should not be assumed to still be true if this pipeline
is ever re-run against a different Unihan version.

## Coverage achieved

100% (1940 / 1940 distinct characters resolved, 0 sent to review).
