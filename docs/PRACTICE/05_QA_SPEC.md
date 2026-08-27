# Practice QA Specification v1.0

## Configuration
- HSK selector contains HSK 1–6
- Count selector contains Tất cả / 50 / 20 / 10
- Requested count never exceeds available data

## Meaning
- four options appear
- correct answer works
- wrong answer works
- correct state is green
- wrong state is red
- Retry keeps current question
- Next advances once

## Character
Run the same tests as Meaning.

## Flashcard
- front displays Chinese + Pinyin
- audio works when available
- click card reveals meaning
- Đã nhớ increments correct once
- Không nhớ increments wrong once
- no duplicate scoring

## Writing
- empty input cannot pass
- correct input passes
- wrong input shows user's answer and correct answer
- Gợi ý reveals Pinyin only
- Retry keeps current question
- Next advances once

## Result
### 20/20
Đúng 20 / Sai 0 / 100%
Review button hidden.

### 18/20
Đúng 18 / Sai 2 / 90%
Review button says:
`Ôn lại 2 câu sai`

### 10/20
Đúng 10 / Sai 10 / 50%
Review button says:
`Ôn lại 10 câu sai`

## Review Wrong
Only incorrect questions from the completed session are reviewed.

## Continue
Starts a new session and resets progress.

## Navigation
- Home works
- Exit confirmation works
- no dead-end routes

## Rapid interactions
Rapid clicking must not:
- double-score
- skip multiple questions
- corrupt the session

## Visual QA
Compare against supplied screenshots:
- header
- content width
- typography
- cards
- borders
- shadows
- buttons
- Chinese/Pinyin hierarchy
- answer spacing
- progress
- correct/wrong feedback
- Result layout

## Build QA
- dev server starts
- production build succeeds
- no Practice console errors
- no broken Practice routes
- no missing assets
- no unexpected horizontal overflow
