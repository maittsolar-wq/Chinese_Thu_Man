# Chinese Thu Man — DICTIONARY QA Specification v1.0

## Basic

### DICT-001
Open Dictionary.

Expected:
- page loads
- Từ điển is active in navigation
- search is visible

## Chinese Search

### DICT-010
Search:
`学习`

Expected:
- 学习 appears
- Pinyin appears
- Vietnamese meaning appears

### DICT-011
Search exact Chinese character/word.

Expected:
- matching result appears

## Pinyin Search

### DICT-020
Search:
`xuexi`

Expected:
- 学习 appears

### DICT-021
Search:
`xuéxí`

Expected:
- 学习 appears

## Vietnamese Search

### DICT-030
Search:
`học`

Expected:
- relevant vocabulary appears where the dataset supports it

### DICT-031
Search with different capitalization.

Expected:
- matching behavior is case-insensitive for Vietnamese/Latin text

## Empty Query

### DICT-040
Open Dictionary with no query.

Expected:
- default state
- no false "no results" message

## No Result

### DICT-050
Search a nonexistent term.

Expected:
- `Không tìm thấy từ phù hợp`
- no broken layout

## Result

### DICT-060
Click a search result.

Expected:
- correct Word Detail opens

### DICT-061
Open the same word from HSK and Dictionary.

Expected:
- same canonical vocabulary data
- same Word Detail implementation

## Audio

### DICT-070
Audio available.

Expected:
- plays correctly

### DICT-071
Audio unavailable.

Expected:
- no broken control/page

## Data Integrity

### DICT-080
Modify canonical vocabulary data.

Expected:
- Dictionary reflects the change automatically
- no duplicated Dictionary record exists

## Error

### DICT-090
Simulate vocabulary repository failure.

Expected:
- friendly error state
- global navigation remains usable

## Keyboard / Accessibility

### DICT-100
Focus search using keyboard.

Expected:
- visible focus

### DICT-101
Press Enter with a query if submit-search behavior is used.

Expected:
- search executes

### DICT-102
Search action has accessible name.

## Visual QA

Check against approved UI:
- white background
- primary blue `#025291`
- search field
- cards
- borders
- radius
- spacing
- Chinese/Pinyin/meaning hierarchy
- active navigation

Do not add an unapproved sidebar.

## Responsive WEB

Test desktop, medium and narrow browser widths.

Expected:
- no horizontal overflow
- search remains usable
- results remain readable

## Build

- dev server starts
- production build succeeds
- no Dictionary console errors
- no broken routes
