# Chinese Thu Man — HSK Data Source Audit v1.0

## A. Primary vocabulary source

Source: profesorm/hsk30

Observed CSV header:

```text
type,word,pinyin,cixing,sort,levelName
```

Example records include:

```text
1,爱,ài,动,1,一级
1,学习,xuéxí,动,249,一级
1,啊,a,助,301,二级
...
1,作业,zuòyè,名,1000,三级
...
1,作者,zuòzhě,名,2000,四级
...
1,作出,zuòchū,动,3600,五级
...
1,罪,zuì,名,5400,六级
```

The source is therefore directly usable for:
- word
- pinyin
- source part of speech
- introduction level
- source ordering

## B. Data that is NOT supplied

The CSV does not provide the Vietnamese learner-facing meaning required by the UI.

It also does not provide the complete app-ready:
- relatedWordIds
- exampleIds
- audio references
- stroke-order references

Therefore these fields must be enriched separately.

## C. HSK level parsing

`levelName` can contain cross-level annotations such as:

`一级（四级）`

For the canonical app model:
- primary/introduced level = the first level
- parenthetical levels are stored separately as `sourceAdditionalLevels` for audit only
- do not automatically treat parenthetical annotations as introduction levels

## D. Character source

For stroke-order UI, use Make Me a Hanzi graphics data as a separate source.

Project:
https://github.com/skishore/makemeahanzi

The project states it provides stroke-order vector graphics for 9,000+ common simplified/traditional characters.

Important: its `dictionary.txt` and `graphics.txt` have different licenses.

- `dictionary.txt`: LGPL v3-or-later
- `graphics.txt`: Arphic Public License

Therefore the project must keep the source/license notices separate.

## E. Recommended character implementation

Use:
- Make Me a Hanzi `graphics.txt` / compatible stroke data for stroke rendering
- project VocabularyWord for word/HSK/meaning
- character IDs to connect words to characters

Do NOT copy Make Me a Hanzi definitions into the Vietnamese vocabulary layer.

## F. Audio

No audio source is locked in this audit.

For MVP, audio may remain optional.

If browser TTS is used, it is runtime-generated and is not treated as a content asset.

If static audio is later added, it needs its own source/license record.

## G. Examples

No external example-sentence dataset is locked as the primary source in this package.

Examples should be added through:
1. project-created/editorial sentences, or
2. a separately audited open dataset with a compatible license.

Do not copy sentences from commercial/proprietary dictionary websites.

## H. Vietnamese

Vietnamese meanings are an editorial layer.

Recommended workflow:

source Chinese/Pinyin/HSK
→ draft Vietnamese meaning
→ human/editorial review
→ app content

Do not blindly copy an English dictionary and machine-translate thousands of records without validation.

## I. License conclusion

The primary HSK source is technically suitable for the MVP under the repository's stated CC BY 4.0 terms, including commercial use, provided attribution and change indication requirements are met.

The original HSK syllabus remains attributed to its original publisher/source; the repository itself states that it does not claim ownership of the original content.

For a future public/commercial release, re-check the exact source revision and license notices before shipping.
