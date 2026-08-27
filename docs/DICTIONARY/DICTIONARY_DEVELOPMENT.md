# Chinese Thu Man — DICTIONARY Development Specification v1.0

## 1. Target

Implement Dictionary in the existing Chinese Thu Man WEB application.

Do not migrate the project to a mobile framework.

## 2. Before Coding

Inspect:
- existing framework
- router
- AppHeader
- design system
- vocabulary repository
- HSK Word List
- existing/shared Word Detail implementation

Reuse existing components.

## 3. Recommended Components

Conceptual structure:

```text
DictionaryPage
├── DictionaryHeader
├── SearchInput
├── SearchResults
├── SearchResultItem
├── EmptySearchState
└── NoResultsState
```

Do not create a second Word Detail component if HSK already provides one.

## 4. Data Access

Use the canonical Vocabulary Repository.

Conceptual method:

```text
searchVocabulary(query, options?)
```

Result:

```text
VocabularyWord[]
```

The repository should own search logic rather than each UI component implementing its own filtering.

## 5. Search Fields

Search:
- chinese
- pinyin
- meaningVi

Optional fields may be searchable later if explicitly approved.

## 6. Search Normalization

Suggested pipeline:

```text
raw query
→ trim
→ normalize spaces
→ normalize Latin case
→ normalize Pinyin comparison
→ search
→ rank
→ return results
```

Pinyin should ideally support:
- tone-marked Pinyin
- unaccented Pinyin

Example:

```text
xuéxí
xuexi
```

should be able to find:

`学习`

Vietnamese matching should be case-insensitive.

## 7. Search Ranking

Recommended scoring:

```text
exact Chinese       highest
Chinese prefix      high
exact Pinyin        high
Pinyin prefix       medium-high
exact Vietnamese    high
Vietnamese partial  medium
```

The exact scoring algorithm may be simple; consistency is more important than sophisticated fuzzy search.

## 8. Performance

For a static HSK dataset:
- load the dataset once
- keep a normalized search representation if useful
- avoid re-reading files on every keystroke
- avoid unnecessary external APIs

Do not introduce a search server for MVP.

If the dataset becomes large enough to require optimization, optimize the repository/search layer rather than the UI.

## 9. Result Item

A result should use:

```text
vocabulary.id
vocabulary.chinese
vocabulary.pinyin
vocabulary.meaningVi
```

Optional:
```text
hskLevels
strokeCount
audio
```

Do not duplicate these records in Dictionary-specific constants.

## 10. Navigation

Use canonical vocabulary ID:

```text
/dictionary/{wordId}
```

or the existing project's preferred Word Detail route.

If Word Detail is shared, route resolution should lead to the same Word Detail page.

## 11. Query State

Decide according to existing routing conventions whether query is represented in URL.

Recommended for a web application:

```text
/dictionary?q=学习
```

This allows:
- browser refresh
- back/forward
- sharing/search restoration

If the current project does not use URL query state, preserve its existing conventions.

## 12. Empty / No Result

Empty query:
- default state
- no error

Non-empty query + zero results:
- NoResultsState

## 13. Error Handling

Repository/data errors should be caught and translated into a friendly UI state.

Never render stack traces.

## 14. Accessibility

Search should support:
- keyboard focus
- Enter to submit if using submit search
- visible focus state
- accessible search label
- buttons with accessible names

## 15. Responsive WEB

At narrower browser widths:
- search field remains usable
- result cards stack naturally
- no horizontal overflow
- text wraps safely

No mobile app navigation.

## 16. Implementation Order

1. Inspect repository
2. Reuse shared layout/header
3. Connect Vocabulary Repository
4. Build search input
5. Build result rendering
6. Implement search normalization/ranking
7. Implement empty/no-result states
8. Connect Word Detail
9. Test Chinese/Pinyin/Vietnamese searches
10. Responsive WEB QA
11. Build

## 17. Completion Report

Report:
- files created/modified
- repository methods used
- routes added
- search behavior
- tests
- build result
- visual deviations
- known limitations
