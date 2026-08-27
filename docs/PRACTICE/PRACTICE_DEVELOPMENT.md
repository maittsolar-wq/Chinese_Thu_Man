# Chinese Thu Man — PRACTICE Development Specification v1.0

## 1. Target

Implement Practice in the existing Chinese Thu Man WEB application.

This is a WEB implementation only.

## 2. Before Coding

Inspect:
- existing framework
- router
- global layout/header
- design tokens
- reusable Card/Button/Input components
- Vocabulary Repository
- HSK implementation
- shared Word Detail
- test setup

Reuse existing architecture.

## 3. Suggested Architecture

Conceptual:

```text
PracticePage
PracticeConfig
PracticeSession
QuestionGenerator
AnswerValidator
ResultCalculator
ResultPage
ReviewWrong
```

Use repository naming conventions where appropriate.

## 4. Shared Components

Prefer reusable components:

```text
PracticeCard
PracticeConfig
HskSelector
QuestionProgress
QuestionOption
AnswerFeedback
Flashcard
WritingInput
HintButton
ResultStats
ResultActions
```

Do not create four unrelated implementations of shared behavior.

## 5. Data

Practice consumes canonical VocabularyWord records from the shared repository.

Conceptual repository calls:

```text
getVocabularyByHsk(level)
getVocabularyByIds(ids)
```

Do not import separate practice-specific vocabulary JSON.

## 6. Question Generation

Create a question set when a session starts.

Pseudo-flow:

```text
pool = getVocabularyByHsk(level)
selected = selectWords(pool, requestedCount)
questions = generateQuestions(selected, exerciseType)
session = createSession(questions)
```

Store the generated question set in session state.

Do not generate questions during render.

## 7. Distractors

For multiple choice:
- correct answer must exist in the selected vocabulary record
- distractors should preferably come from the same HSK scope
- no duplicate option
- correct option position randomized once
- options remain stable during the current question

## 8. Meaning Validation

Compare selected option against the question's correct answer.

Do not infer correctness from displayed text if a stable answer ID can be used.

## 9. Character Validation

Same principle:
- use vocabulary/question IDs
- do not depend solely on UI labels

## 10. Flashcard

Use a simple `front/back` state.

After `Đã nhớ` or `Không nhớ`:
- score exactly once
- advance exactly once

## 11. Writing Validation

Recommended:

```text
userInput
→ trim
→ compare with expected Chinese
```

For MVP, exact character/word equality after whitespace normalization is sufficient.

Do not build handwriting canvas or OCR.

## 12. Progress

Use:

```text
currentIndex + 1
actualCount
```

for user-facing progress.

Example:
first question of 20:
`1/20`

## 13. Result Calculation

Use session state:

```text
total = actualCount
correct = correctCount
wrong = total - correct
accuracy = total > 0 ? correct / total * 100 : 0
```

Do not hard-code values.

## 14. Result

One shared Result component receives calculated result data.

Conceptual props:

```text
total
correct
wrong
accuracy
exerciseType
hskLevel
```

Review Wrong receives the completed question results.

## 15. Review Wrong

Filter completed session questions:

```text
questions.filter(question => question.isCorrect === false)
```

Create a new review session from those vocabulary/question records.

Do not modify the original session.

## 16. Continue Practice

Create a new session.

Never reuse the completed session object as mutable state.

## 17. Persistence

No backend user account is required.

If session persistence is needed to survive a browser refresh, use the simplest approved browser-local mechanism. Do not introduce a server database for MVP solely for Practice.

If refresh recovery is not implemented, show a safe restart behavior rather than corrupted state.

## 18. Routing

Use existing web router.

Conceptual:
```text
/practice
/practice/meaning
/practice/character
/practice/flashcard
/practice/writing
```

A configuration/session route can be implemented according to existing router conventions.

Do not create a second router.

## 19. Rapid Interaction Protection

Disable/lock answer controls after submission.

Prevent:
- double scoring
- double navigation
- skipped questions
- duplicated result counts

## 20. Error Handling

If vocabulary pool is empty:
show:
`Chưa có dữ liệu từ vựng cho cấp độ này.`

If Pinyin is missing:
- preserve question
- hide/disable hint where applicable

If audio is missing:
- hide/disable audio action

If question generation fails:
- show friendly error
- allow returning to Practice Home

## 21. Responsive WEB

Desktop-first.
At narrower browser widths:
- question card remains readable
- answer options stack/wrap
- buttons remain accessible
- no horizontal overflow

Do not implement a mobile app.

## 22. Implementation Order

1. Inspect repository
2. Reuse global layout/design system
3. Implement Practice Home
4. Implement shared Configuration
5. Implement session state
6. Implement Chọn nghĩa
7. Implement Chọn chữ Hán
8. Implement Flashcard
9. Implement Luyện viết
10. Implement shared Result
11. Implement Review Wrong
12. Implement Continue
13. Handle edge cases
14. Tests
15. Build
16. Visual verification

## 23. Completion Report

Claude Code must report:
- files created
- files modified
- routes
- data source/repository used
- components reused
- tests run
- build result
- known issues
- deviations from approved UI/spec
