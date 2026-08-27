# Chinese Thu Man — Data Pipeline v1.0

## Goal
Convert external/open datasets into clean, validated application content.

```text
External Sources
→ Raw
→ Normalize
→ Deduplicate
→ Merge
→ Vietnamese Editorial
→ Related Words
→ Examples
→ Character/Stroke Mapping
→ Validate
→ Processed Content
→ Web App
```

## 1. Acquire
Store source files unchanged under `data/raw/`.

Record:
- source
- URL
- exact version/date
- license
- retrieval date

## 2. Normalize
Normalize:
- Chinese whitespace
- Pinyin
- HSK level
- part of speech
- source IDs

Create stable application IDs.

## 3. Deduplicate
Detect duplicate Chinese words, IDs and conflicting mappings. Do not silently discard conflicts; produce a review report.

## 4. Merge
Recommended authority:
1. selected HSK 3.0 source → level mapping
2. approved dictionary source → Pinyin/POS/definitions where licensed
3. project Vietnamese editorial layer → learner-facing Vietnamese
4. approved stroke source → character/stroke data

Do not silently mix HSK 2.0 and HSK 3.0.

## 5. Vietnamese Editorial
Meanings should be concise and natural for Vietnamese learners.

Example:
`学习 → học; học tập`

Do not blindly ship machine-translated definitions.

## 6. Related Words
Create relationships only when genuinely useful. Prefer IDs rather than duplicated records.

## 7. Examples
Target 1–3 strong examples per word where practical. Every example needs Chinese + matching Pinyin + Vietnamese translation.

## 8. Stroke Data
Map characters to structured stroke-order data. Do not create a separate video file for every vocabulary word.

## 9. Audio
Optional. Store references, not binary audio inside vocabulary JSON.

## 10. Validate
Run `DATA_VALIDATION.md` before release.

## 11. Output
```text
data/content/
├── vocabulary.json
├── examples.json
├── characters.json
└── metadata.json
```

## 12. Reproducibility
Same raw source + same pipeline version should produce the same processed data. Record dataset and pipeline versions.

## 13. Updates
`new source → pipeline → validation → diff → review → release`

Diff should report added/removed/changed words, meanings, Pinyin, HSK mapping, examples and stroke references.

## 14. MVP
Phase 1: Chinese/Pinyin/Vietnamese/HSK
Phase 2: character/stroke/POS
Phase 3: related words/examples/audio
