# Chinese Thu Man — Content Data Schema v1.0

## Purpose
Define the canonical content model shared by HSK, Dictionary, Word Detail and Practice.

## Rule
Use one canonical `VocabularyWord`. Do not create separate HSK/Dictionary/Practice copies.

## Recommended structure
```text
data/
├── raw/
├── normalized/
└── content/
    ├── vocabulary.json
    ├── examples.json
    ├── characters.json
    └── metadata.json
```

## VocabularyWord
```json
{
  "id": "hsk1_001",
  "word": "学习",
  "pinyin": "xuéxí",
  "pinyinNumeric": "xue2xi2",
  "meaningVi": ["học", "học tập"],
  "hskLevels": [1],
  "partOfSpeech": ["động từ"],
  "strokeCount": 16,
  "characterIds": ["char_xue", "char_xi"],
  "relatedWordIds": [],
  "exampleIds": [],
  "audio": {"wordUrl": null, "exampleUrl": null}
}
```

### Required
- `id`: unique, stable, not based on display text
- `word`: Chinese word/phrase
- `pinyin`: learner-facing Pinyin
- `meaningVi`: Vietnamese meaning(s)
- `hskLevels`: integer array, values 1–6

### Optional
- `pinyinNumeric`
- `partOfSpeech`
- `strokeCount`
- `characterIds`
- `relatedWordIds`
- `exampleIds`
- `audio`

## Example
```json
{
  "id": "example_001",
  "vocabularyId": "hsk1_001",
  "chinese": "我学习中文。",
  "pinyin": "Wǒ xuéxí Zhōngwén.",
  "meaningVi": "Tôi học tiếng Trung.",
  "level": 1,
  "audioUrl": null
}
```

## Character
```json
{
  "id": "char_xue",
  "character": "学",
  "pinyin": "xué",
  "strokeCount": 8,
  "radical": "子",
  "strokeData": null
}
```

Stroke data should be structured data rendered by the web app, not a video per vocabulary word.

## Relationships
```text
VocabularyWord
├── characterIds → Character
├── relatedWordIds → VocabularyWord
└── exampleIds → Example
```

## Practice
Practice questions are generated at runtime from VocabularyWord. Do not permanently duplicate practice questions in content files.

## User state
Current MVP has no cloud user data. Do not put favorites, progress, streaks or learning status into canonical content.

## Priority
P1: Chinese + Pinyin + Vietnamese + HSK
P2: POS + stroke count + character/stroke data
P3: related words + examples + audio
