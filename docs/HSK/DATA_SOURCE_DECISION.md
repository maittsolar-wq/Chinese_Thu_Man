# Chinese Thu Man — HSK Data Source Decision v1.0

## Decision

Primary vocabulary source for the current WEB MVP:

`profesorm/hsk30` — HSK 3.0 2026 Syllabus Dataset.

Repository:
https://github.com/profesorm/hsk30

Vocabulary file:
https://raw.githubusercontent.com/profesorm/hsk30/main/data/hsk_vocabulary.csv

License stated by the repository:
Creative Commons Attribution 4.0 International (CC BY 4.0).

The repository states that its data was extracted from the publicly available HSK syllabus published by Chinese Testing International and reorganized into machine-readable datasets. It also explicitly permits use for educational tools and language-learning apps, subject to attribution.

## Why this source

It is currently the best fit for the project because it provides:
- HSK 3.0 2026 vocabulary
- HSK 1–6 level boundaries
- Chinese vocabulary
- Pinyin
- Chinese part of speech
- deterministic sort/order
- CSV + JSON
- a clearly stated CC BY 4.0 license at the repository level

## Important limitation

This source does NOT provide the complete learner-facing content required by Chinese Thu Man.

It provides the vocabulary backbone, but the app still needs:
- Vietnamese meanings
- related words
- example sentences
- stroke-order data
- optional audio

Those must be added through separate, documented sources or project-created/editorial content.

## HSK 3.0 2026 counts

The 2026 structure is cumulative:

| Level | Cumulative words | New words at level |
|---|---:|---:|
| HSK 1 | 300 | 300 |
| HSK 2 | 500 | 200 |
| HSK 3 | 1,000 | 500 |
| HSK 4 | 2,000 | 1,000 |
| HSK 5 | 3,600 | 1,600 |
| HSK 6 | 5,400 | 1,800 |
| HSK 7–9 | 11,000 | 5,600 |

The source CSV confirms boundaries at 300, 500, 1,000, 2,000, 3,600 and 5,400. Therefore the application must distinguish:

`introducedLevel` = level where a word is introduced

from

`hskLevels` = cumulative levels where the word is available.

Example:
A word introduced in HSK 1 has:
`introducedLevel: 1`
`hskLevels: [1,2,3,4,5,6]`

This lets the UI support both:
- "new words in HSK 2" = introducedLevel 2
- "all vocabulary required by HSK 2" = hskLevels contains 2

## Recommended product behavior

For the current HSK Word List UI, show the cumulative vocabulary for the selected level.

Example:
`HSK 2 → 500 words`

If the UI later needs "new words only", filter by `introducedLevel`.

## Do not use

Do not use the older HSK 2.0 5,000-word list as the primary dataset.

Do not use the 2021 HSK 3.0 11,092-word list as the current primary dataset.

The project target is HSK 3.0 2026.
