# Chinese Thu Man — Data Architecture v1.0

## Core principle
Use **one canonical vocabulary dataset** for:
- Home
- HSK
- Word List
- Word Detail
- Dictionary
- Practice

Do not create separate duplicated HSK, Dictionary and Practice word databases.

## MVP storage
No backend is required for the canonical vocabulary content.

Recommended:
```text
data/
└── vocabulary/
    ├── hsk1.json
    ├── hsk2.json
    ├── hsk3.json
    ├── hsk4.json
    ├── hsk5.json
    └── hsk6.json
```
A single processed JSON is also acceptable if the existing web architecture benefits from it.

## Canonical VocabularyWord
```text
id
chinese
pinyin
meaningVi
hskLevels[]
partOfSpeech[]
strokeCount
relatedWordIds[]
examples[]
audio
strokeData
```

## HSK
Do not assume a word belongs to exactly one level. Preserve multiple level associations when the authoritative source requires them.

## Word Detail
Resolve one canonical VocabularyWord and display its available details.

## Dictionary
Search the canonical repository. Return vocabulary IDs, then open Word Detail.

Searchable fields:
- Chinese
- Pinyin
- Vietnamese meaning

## Practice
Question generators consume VocabularyWord records.

Meaning:
`Chinese + Pinyin → meaningVi`

Character:
`meaningVi → Chinese`

Flashcard:
`front = Chinese + Pinyin; back = meaningVi`

Writing:
`prompt = meaningVi; expected = Chinese; hint = Pinyin`

## Practice Session
```text
sessionId
exerciseType
hskLevel
requestedCount
actualCount
currentIndex
correctCount
wrongCount
questions[]
startedAt
completedAt
```

Question:
```text
questionId
vocabularyId
questionType
correctAnswer
userAnswer
isCorrect
attemptCount
status
```

## User data
Current MVP does not require a server-side user profile or cloud persistence.
Temporary practice state can live in application state.

Future favorites/progress can be added without changing VocabularyWord.

## Audio
Optional:
```text
audio:
  wordUrl
  exampleUrl
```
Missing audio must not crash the UI.

## Stroke order
Prefer structured stroke data rendered in the browser instead of storing a video for every word.

## Related words
Prefer canonical IDs:
`relatedWordIds[]`
Do not duplicate entire vocabulary records.

## Examples
Store:
```text
chinese
pinyin
meaningVi
```

## Data validation
Validate:
- unique IDs
- non-empty Chinese/Pinyin/meaning
- valid HSK levels
- valid related-word references
- valid examples
- valid stroke references

## Source/license
Record source, source version, license and preparation date. A repository software license does not automatically mean every dataset inside it has the same license.

## Data flow
```text
Processed vocabulary
        ↓
Vocabulary Repository
   ┌────┼─────┬─────┐
   ↓    ↓     ↓     ↓
  HSK  Dict  Word  Practice
       ↓     Detail   ↓
       └──────┬───────┘
              ↓
        shared vocabulary
```
