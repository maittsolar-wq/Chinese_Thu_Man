# Chinese Thu Man — Next Data Work

## Immediate order

1. Run `fetch_hsk_source.py`.
2. Run `normalize_hsk_source.py`.
3. Validate the resulting 5,400 HSK 1–6 records.
4. Add Vietnamese meanings.
5. Add character/stroke mapping.
6. Add related words.
7. Add 1–3 examples where practical.
8. Add optional audio.
9. Run final validation.
10. Copy the processed content into the web project's `data/content/`.

## Do not ask Claude Code to

- invent 5,400 meanings without a review pipeline
- scrape proprietary dictionary sites
- mix HSK 2.0 and HSK 3.0
- create separate HSK/Dictionary/Practice datasets
- create one video file per vocabulary word
- add user progress to canonical content

## Target app-ready record

```text
id
word
pinyin
pinyinNumeric
meaningVi[]
introducedLevel
hskLevels[]
partOfSpeech[]
strokeCount
characterIds[]
relatedWordIds[]
exampleIds[]
audio
```

## HSK UI interpretation

For the current product:
- HSK 1 = 300 cumulative words
- HSK 2 = 500 cumulative words
- HSK 3 = 1,000 cumulative words
- HSK 4 = 2,000 cumulative words
- HSK 5 = 3,600 cumulative words
- HSK 6 = 5,400 cumulative words

If the UI later needs "new words only", use `introducedLevel`.
