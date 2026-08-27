# Chinese Thu Man — DICTIONARY Specification v1.0

## 1. Purpose

The Dictionary module provides a simple way for Vietnamese learners to quickly find Chinese vocabulary.

It is intentionally lightweight and focused on the vocabulary dataset already used by HSK.

The Dictionary is not a separate dictionary database and does not attempt to reproduce a full commercial dictionary platform.

## 2. Core Flow

```text
Từ điển
   ↓
Search
   ↓
Search Results
   ↓
Select Word
   ↓
Word Detail
```

No login or account is required.

## 3. Main Screen

The Dictionary page should contain:

- page title
- short supporting description where present in approved UI
- prominent search input
- search button/icon
- search result area

The page should remain visually clean and white-first.

Primary blue:
`#025291`

## 4. Search Input

Purpose:
Allow the user to search vocabulary quickly.

Recommended placeholder:

`Nhập chữ Hán, pinyin hoặc nghĩa tiếng Việt...`

Search should support:

1. Chinese
2. Pinyin
3. Vietnamese meaning

The exact matching/normalization behavior is defined in the Development specification.

## 5. Search Trigger

Support the interaction pattern approved by the existing UI.

Recommended:
- type query
- press Enter or click search
- display results

If the existing implementation already supports instant search, preserve that behavior.

Do not add both instant search and submit search unnecessarily.

## 6. Search Results

Each result should be compact and easy to scan.

Recommended hierarchy:

```text
学习
xuéxí
học, học tập
```

Optional:
- HSK level
- stroke count
- audio action

Do not overload result cards with the entire Word Detail dataset.

## 7. Result Count

If the UI shows result count, derive it from the actual search result.

Example:

`Tìm thấy 12 kết quả`

Never hard-code result counts.

## 8. Search Result Ordering

Recommended priority:

1. exact Chinese match
2. exact Pinyin match
3. exact Vietnamese meaning match
4. prefix/partial match
5. broader text match

If the existing UI has a different approved ordering, follow the approved UI.

The sorting implementation must be deterministic.

## 9. Search Normalization

The search system should normalize user input enough to make common searches work.

Examples:
- trim leading/trailing spaces
- normalize repeated spaces
- case-insensitive matching for Latin Pinyin/Vietnamese
- support Pinyin without tone marks where practical

Chinese matching should remain character-aware.

Do not implement overly complex fuzzy search for MVP unless needed.

## 10. Empty Search

When the page is first opened and the query is empty:

Show the default Dictionary state.

Do not display a misleading "Không tìm thấy" message.

## 11. No Results

When a non-empty query produces no results:

Show a friendly state such as:

`Không tìm thấy từ phù hợp`

Optional supporting text:

`Hãy thử chữ Hán, pinyin hoặc nghĩa tiếng Việt khác.`

Do not show a blank content area.

## 12. Loading

If the dictionary uses asynchronous data:

Show a lightweight loading/skeleton state.

If vocabulary data is bundled locally and search is synchronous, no artificial loading screen is required.

## 13. Error

If the vocabulary repository cannot be loaded:

Show a concise Vietnamese error state.

Example:

`Không thể tải dữ liệu từ điển.`

Keep global navigation functional.

Do not expose technical errors or stack traces.

## 14. Word Selection

Clicking a result opens the shared Word Detail.

Flow:

```text
Dictionary
→ Search Results
→ Word Detail
```

Use the canonical vocabulary ID.

Do not pass the entire vocabulary object through the URL.

## 15. Word Detail Reuse

Dictionary must use the same Word Detail experience as HSK.

Conceptually:

```text
HSK Word List ─────┐
                   ├──→ Word Detail
Dictionary Results ┘
```

Do not create:
- DictionaryWordDetail
- HSKWordDetail

as separate domain screens.

There should be one canonical Word Detail implementation.

## 16. Breadcrumb / Context

If the approved Word Detail UI uses breadcrumbs, the source context may be reflected.

Examples:

From HSK:
`Trang chủ > HSK 1 > 学习`

From Dictionary:
`Trang chủ > Từ điển > 学习`

The exact breadcrumb behavior should follow the approved prototype.

## 17. Search Scope

Default Dictionary search searches the full canonical HSK vocabulary dataset available in the application.

The Dictionary is not restricted to one HSK level unless the user explicitly enters from an HSK-scoped search experience.

## 18. HSK Filtering

A future enhancement may allow filtering by HSK level.

For MVP, do not add an HSK filter if it is not present in the approved UI.

If an HSK filter is later approved:

```text
Tất cả
HSK 1
HSK 2
...
HSK 6
```

It must filter the same canonical dataset.

## 19. Audio

If a result provides audio and the approved UI includes an audio action, clicking it plays the word.

Missing audio must not break the result.

## 20. Business Rules

1. Dictionary uses the canonical vocabulary dataset.
2. Dictionary has no duplicate vocabulary database.
3. Search covers Chinese/Pinyin/Vietnamese where data supports it.
4. Empty query is not a no-result state.
5. No-result state is explicit.
6. Selecting a result opens shared Word Detail.
7. No authentication is required.
8. No server-side user profile is required.
9. No payment/subscription functionality exists in MVP.

## 21. Acceptance Criteria

Dictionary is accepted when:
- page opens correctly
- search works
- Chinese search works
- Pinyin search works
- Vietnamese search works where supported
- results are deterministic
- no-result state works
- empty state works
- result opens correct Word Detail
- Word Detail is shared with HSK
- no duplicate dictionary dataset exists
- UI matches approved design
