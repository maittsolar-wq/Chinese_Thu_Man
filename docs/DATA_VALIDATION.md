# Chinese Thu Man — Data Validation v1.0

## Fatal checks
- valid JSON
- unique IDs
- required fields present
- HSK levels only 1–6
- required references resolve
- no unusable records

## Vocabulary
Every record must have:
- unique `id`
- non-empty `word`
- non-empty `pinyin` where required
- non-empty `meaningVi`
- non-empty `hskLevels`

Reject placeholders such as `TBD`, `test`, `undefined`, `null`.

## HSK
Allowed:
`1, 2, 3, 4, 5, 6`

Do not silently accept HSK 7+.

## Pinyin
Check consistency of display Pinyin and numeric Pinyin when both exist. Flag uncertain syllables for review rather than blindly deleting them.

## Vietnamese
Check:
- non-empty
- Vietnamese learner-facing wording
- no accidental markup
- reasonable length
- no English-only placeholder

Do not auto-overwrite editorial meanings during validation.

## Relationships
Every `relatedWordId`, `exampleId` and `characterId` must resolve. Flag self-references unless intentionally allowed.

## Examples
Each example requires:
- vocabularyId
- Chinese
- Pinyin
- Vietnamese meaning

Check that the target word appears in the Chinese sentence where practical.

## Characters
Check:
- valid Chinese character
- positive stroke count when present
- valid stroke-data reference when present

## Audio
If supplied, reference must be valid and asset must exist in the final build/package. Missing optional audio is a warning.

## Duplicate detection
Detect duplicate Chinese/Pinyin/source mappings. Duplicates may require editorial review because homographs can be legitimate.

## Practice readiness
For each HSK level, verify available vocabulary for:
- 10 questions
- 20 questions
- 50 questions

If insufficient, the app uses the available number and must not fabricate vocabulary.

## Cross-module
Verify:
- HSK retrieves records
- Dictionary searches records
- Word Detail resolves IDs
- Practice can generate questions

## Release gate
Fatal errors = 0.

Warnings may remain for optional missing audio, examples, related words or stroke data.

## Output
Generate:
- `validation-report.json`
- `validation-report.md`
