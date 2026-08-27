# Chinese Thu Man — HOME Specification v1.0

## 1. Purpose

Home is the main entry page of the Chinese Thu Man WEB application.

Its job is simple:
- orient the learner
- provide direct access to the three core learning areas
- surface HSK levels
- provide a clear path into vocabulary learning and practice

Home is NOT a complex personal dashboard.

## 2. Main Navigation

Header/navigation:
- Trang chủ
- HSK
- Từ điển
- Luyện tập

Home is the active item.

Navigation uses the shared Design System:
- white background
- primary blue `#025291`
- active state highlighted in blue

## 3. Page Structure

Conceptual structure:

```text
HOME
│
├── Header
│
├── Hero / Welcome
│
├── Main learning entry cards
│   ├── HSK
│   ├── Từ điển
│   └── Luyện tập
│
└── HSK overview / quick access
    ├── HSK 1
    ├── HSK 2
    ├── HSK 3
    ├── HSK 4
    ├── HSK 5
    └── HSK 6
```

The exact visual composition must follow the approved Home UI supplied by the product owner.

## 4. Hero

Purpose:
Give the user immediate context.

Recommended content:
- Chinese learning headline
- short Vietnamese description
- primary action to start learning
- optional supporting Chinese visual

Do not introduce:
- login
- account information
- notification center
- complicated statistics

## 5. Core Feature Cards

Home should expose three primary destinations.

### HSK

Title:
`HSK`

Description:
`Học từ vựng theo từng cấp độ HSK.`

Action:
`Xem HSK`

Navigation:
```text
Home → HSK Overview
```

### Từ điển

Title:
`Từ điển`

Description:
`Tra nhanh từ vựng tiếng Trung.`

Action:
`Tra từ`

Navigation:
```text
Home → Dictionary
```

### Luyện tập

Title:
`Luyện tập`

Description:
`Ôn tập từ vựng với nhiều dạng bài.`

Action:
`Luyện tập ngay`

Navigation:
```text
Home → Practice
```

## 6. HSK Quick Access

Home can show all six HSK levels as quick-access cards.

Each card displays:
- HSK level
- vocabulary count derived from the dataset
- action/entry affordance

Example:

```text
HSK 1
XXX từ
```

Click:
```text
Home → HSK Overview / HSK Level
```

Prefer direct navigation to the selected HSK level if the approved UI supports it.

Do not hard-code vocabulary counts.

## 7. Data Used by Home

Home consumes data from the shared vocabulary repository.

Possible derived values:
- total vocabulary count
- HSK 1 count
- HSK 2 count
- HSK 3 count
- HSK 4 count
- HSK 5 count
- HSK 6 count

Home must not maintain a second copy of vocabulary.

## 8. No User-Specific Data in MVP

Current MVP does not require:
- account
- saved user profile
- learning streak
- personal statistics
- personal progress
- favorite words
- cloud sync

Do not show fake progress such as:
`Bạn đã học 82%`
unless actual persistence is implemented and explicitly approved.

## 9. Navigation Rules

### HSK card
→ `/hsk` or the repository's equivalent HSK route.

### Dictionary card
→ `/dictionary` or equivalent.

### Practice card
→ `/practice` or equivalent.

### HSK level card
→ selected HSK level / Word List.

Use the project's existing routing conventions.

## 10. Loading State

Home should not display a blank page while vocabulary counts are loading.

If counts are loaded asynchronously:
- show skeleton/placeholder for count
- keep navigation usable

If vocabulary is bundled statically and available immediately, no special loading UI is necessary.

## 11. Empty State

If vocabulary data cannot be loaded:
- keep the general Home layout
- show a concise data-unavailable message where dynamic content would appear
- keep navigation available

Do not crash the entire page.

## 12. Error State

If a data request fails:
- show a small friendly error state
- do not expose technical stack traces
- allow navigation to other static pages

For a static-data MVP, data-loading errors should be handled at the repository/data layer.

## 13. Responsive WEB

Home is desktop-first WEB.

At narrower browser widths:
- feature cards may stack
- HSK cards may wrap
- text remains readable
- buttons remain usable
- no horizontal page overflow

Do not redesign this as a mobile application.

## 14. Business Rules

1. Home is always accessible.
2. Home does not require authentication.
3. All vocabulary counts are derived from canonical data.
4. Home does not own vocabulary records.
5. Every primary card must lead to a valid destination.
6. No CTA may lead to an unimplemented page.
7. No personal learning data is required for MVP.

## 15. Acceptance Criteria

Home is accepted when:
- all four main navigation items work
- HSK entry opens HSK
- Dictionary entry opens Dictionary
- Practice entry opens Practice
- six HSK levels are represented where approved
- dynamic counts are accurate
- no fake user statistics appear
- design matches the approved Home UI
- desktop layout has no overflow
- loading/error states do not break navigation
