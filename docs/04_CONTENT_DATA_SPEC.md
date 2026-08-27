# Chinese Thu Man — Content Data Specification v1.0

## Goal
Prepare HSK 1–6 vocabulary data for the approved web UI.

Required core content:
- Chinese
- Pinyin
- Vietnamese meaning
- HSK level

Additional content:
- related words
- example sentences
- stroke count
- stroke-order data
- optional audio

## Recommended record
```json
{
  "id": "hsk1_001",
  "chinese": "学习",
  "pinyin": "xuéxí",
  "meaningVi": "học, học tập",
  "hskLevels": [1],
  "partOfSpeech": ["động từ"],
  "strokeCount": 16,
  "relatedWordIds": [],
  "examples": [
    {
      "chinese": "我学习中文。",
      "pinyin": "Wǒ xuéxí Zhōngwén.",
      "meaningVi": "Tôi học tiếng Trung."
    }
  ],
  "audio": {
    "wordUrl": null,
    "exampleUrl": null
  },
  "strokeData": {
    "characterIds": ["学", "习"]
  }
}
```

Adapt the exact structure to the selected source and existing project conventions.

## Required field definitions
### id
Stable unique ID.

### chinese
Chinese word/phrase.

### pinyin
Standard Pinyin.

### meaningVi
Concise, natural Vietnamese learner-facing meaning.

### hskLevels
Array of HSK levels. Do not force a multi-level word into one level when the authoritative data says otherwise.

## Part of speech
Use consistent Vietnamese labels such as:
- danh từ
- động từ
- tính từ
- đại từ
- phó từ
- lượng từ

## Related words
Prefer meaningful relationships:
- shared character
- common compound
- semantic relationship
- learner-relevant association

Example:
`学习 → 学生 → 学校 → 大学`
Only include genuinely useful relationships.

## Examples
Each example should:
- be grammatically correct
- naturally use the target word
- suit the learner level
- have matching Pinyin
- have accurate Vietnamese translation

MVP recommendation: 1–3 strong examples per word. One good example is better than several poor ones.

## Stroke order
Use structured stroke data rendered in the browser. Do not require a manually produced video for every word.

## Audio
Optional. Browser TTS may be used as a fallback, but should not be treated as canonical audio data.

## Dictionary search
The same records support Chinese, Pinyin and Vietnamese search.

## Practice distractors
Multiple-choice distractors should preferably come from the same HSK scope and must not duplicate the correct answer.

## HSK source
Use one clearly identified HSK 3.0 source for the selected standard. Before import, record:
- source
- URL/repository
- version
- license
- extraction date
- transformations

Do not silently mix HSK 2.0 and HSK 3.0.

## External data and copyright
Internal/non-commercial use does not automatically eliminate copyright or license obligations.

For every external dataset:
1. inspect the actual data license
2. record attribution requirements
3. comply with share-alike requirements where applicable
4. do not copy proprietary website content without permission

## Preparation pipeline
```text
External source
→ raw import
→ normalize Chinese/Pinyin/HSK
→ normalize Vietnamese meanings
→ validate
→ add related-word references
→ add examples
→ attach stroke references
→ attach optional audio
→ processed JSON
→ web app
```

## Raw vs processed
Keep external raw data separate:
```text
data/
├── raw/
└── processed/
```
Do not treat manually edited raw source data as the canonical application dataset.

## Metadata
Processed dataset should record:
```text
datasetName
standard
levels
version
source
license
preparedAt
```

## Quality gate
A dataset is ready only when:
- required fields are complete
- HSK mapping is validated
- Pinyin is valid
- Vietnamese meaning is reviewed
- duplicates are handled
- related references resolve
- examples match the target word
- stroke references resolve where provided
- source/license metadata is recorded

## MVP priority
Priority 1:
Chinese + Pinyin + Vietnamese meaning + HSK level

Priority 2:
stroke count + stroke order + related words

Priority 3:
examples + audio

If content preparation becomes too large, ship Priority 1 first while keeping the schema ready for Priority 2/3.
