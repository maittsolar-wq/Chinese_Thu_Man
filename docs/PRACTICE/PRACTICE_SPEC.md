# Chinese Thu Man — PRACTICE Specification v1.0

## 1. Purpose

Practice is the vocabulary review area of Chinese Thu Man.

The MVP contains exactly four exercise types:

1. Chọn nghĩa
2. Chọn chữ Hán
3. Flashcard
4. Luyện viết

The goal is to practice vocabulary from the canonical HSK dataset without introducing unnecessary LMS features.

## 2. Main Flow

```text
Practice Home
    ↓
Select Exercise Type
    ↓
Practice Configuration
    ↓
Practice Session
    ↓
Result
```

## 3. Practice Home

Title:
`LUYỆN TẬP`

Four main cards:

### Chọn nghĩa
`Chọn nghĩa tiếng Việt đúng với từ vựng`

### Chọn chữ Hán
`Chọn chữ Hán đúng với nghĩa`

### Flashcard
`Ôn tập từ vựng với thẻ ghi nhớ`

### Luyện viết
`Nhập tiếng Trung theo nghĩa tiếng Việt`

Each card opens the corresponding configuration/session flow.

## 4. Configuration

Shared configuration for all four exercise types.

### HSK

Options:
- HSK 1
- HSK 2
- HSK 3
- HSK 4
- HSK 5
- HSK 6

### Number of words

Options:
- Tất cả
- 50
- 20
- 10

CTA:
`Bắt đầu luyện tập`

The actual question count cannot exceed available vocabulary.

Example:

```text
Requested: 50
Available: 32
Actual: 32
```

Keep `requestedCount` and `actualCount` separately in session state.

## 5. Question Set

At session creation:
1. get vocabulary for selected HSK scope
2. choose the requested number
3. generate the question set
4. store it in the session

Do not generate a new random question on every React/render cycle.

## 6. Chọn nghĩa

### Prompt

Show:
```text
学习
xuéxí
```

Question:
`Chọn nghĩa đúng`

Show four Vietnamese options.

Example:
```text
A. Trường học
B. Học, học tập
C. Học sinh
D. Giáo viên
```

The correct option position is randomized.

### Correct

Selected option becomes green.

Show:
`✓ Chính xác!`

Show:
`Đáp án: Học, học tập`

CTA:
`Tiếp theo`

### Wrong

Selected option becomes red.

Show:
`✕ Chưa chính xác!`

Show:
`Bạn chọn: Giáo viên`
`Đáp án: Học, học tập`

Actions:
`Thử lại`
`Tiếp theo`

## 7. Chọn chữ Hán

### Prompt

Show Vietnamese meaning:

`Học, học tập`

Show four Chinese options.

Example:
```text
A. 学习
B. 学生
C. 学校
D. 老师
```

The correct position is randomized.

Correct/wrong states follow the same feedback rules as Chọn nghĩa.

## 8. Flashcard

### Front

Show:
```text
学习
xuéxí
```

Audio action if available.

Instruction:
`Nhấn vào thẻ để xem nghĩa`

### Back

Show:
```text
学习
xuéxí
Học, học tập
```

Actions:
- `Không nhớ`
- `Đã nhớ`

Rules:
- `Đã nhớ` = correct
- `Không nhớ` = wrong
- either action scores the card once and advances

Do not allow duplicate scoring.

## 9. Luyện viết

This exercise is intentionally simple.

It is NOT a freehand/canvas handwriting recognition system.

### Prompt

Show Vietnamese meaning:

`Học, học tập`

Input:
`Nhập Tiếng Trung`

Actions:
- `Gợi ý`
- `Không nhớ`
- `Kiểm tra đáp án`

### Hint

`Gợi ý` reveals Pinyin only:

`xuéxí`

It does not reveal the Chinese answer.

### Correct

Show:
`✓ Chính xác!`

`Đáp án: 学习`

CTA:
`Tiếp theo`

### Wrong

Show:
`✕ Chưa chính xác!`

`Bạn chọn: 学校`
`Đáp án: 学习`

Actions:
`Thử lại`
`Tiếp theo`

## 10. Writing Validation

Minimum rules:
- empty input is invalid
- trim leading/trailing whitespace
- compare normalized user input with expected Chinese answer
- do not silently modify user input
- do not accept the Pinyin as a correct Chinese answer

For MVP, exact Chinese character/word matching after harmless whitespace normalization is sufficient.

## 11. Progress

Every session shows:

```text
3/20
```

and a progress bar.

Progress is based on `actualCount`.

Do not calculate from requested count when requested > available.

## 12. Answer Lock

Once the current question is scored:
- prevent duplicate scoring
- prevent changing the submitted answer
- prevent rapid multiple navigation
- `Tiếp theo` advances only once

## 13. Retry

`Thử lại` keeps the same question.

It does not increase the question index.

The session's original question result should remain logically consistent.

## 14. Next

`Tiếp theo` advances to exactly one next question.

If the current question is the last question:
```text
Last Question
→ Complete Session
→ Result
```

Do not create an extra question.

## 15. Result

All four exercise types use the same Result UI.

Show:

```text
Kết quả luyện tập

Bạn đã hoàn thành bài tập luyện tập

18/20 câu

Đúng: 18
Sai: 2
Độ chính xác: 90%
```

Accuracy formula:

```text
accuracy = correctCount / actualCount × 100
```

Never hard-code result numbers.

### Actions

If wrongCount > 0:
`Ôn lại 2 câu sai`

Always:
`Luyện tập tiếp`
`Về trang chủ`

If wrongCount = 0:
hide the Review Wrong button.

## 16. Review Wrong

Review contains only incorrectly answered questions from the completed session.

Flow:

```text
Result
→ Ôn lại X câu sai
→ Incorrect questions only
→ Result
```

Review is a new session.

It must not modify the original completed session.

## 17. Continue Practice

Starts a new practice session.

Default:
- same exercise type
- same HSK level
- same requested count

Generate a fresh question selection where possible.

## 18. Exit Active Session

If the user attempts to leave before completion:

```text
Thoát luyện tập?

Tiến độ hiện tại sẽ không được lưu.
```

Actions:
- `Ở lại`
- `Thoát`

Do not record an abandoned session as completed.

## 19. Session Model

Conceptual:

```text
PracticeSession {
  sessionId
  exerciseType
  hskLevel
  requestedCount
  actualCount
  currentIndex
  correctCount
  wrongCount
  questions[]
  startedAt
  completedAt
}
```

Question:

```text
PracticeQuestion {
  questionId
  vocabularyId
  questionType
  correctAnswer
  userAnswer
  isCorrect
  attemptCount
  status
}
```

## 20. Question Status

Allowed values:

```text
unanswered
answered_correct
answered_wrong
```

Optional:
`skipped` only if an explicit skip feature is later approved.

Do not invent a skip button for the MVP.

## 21. Business Rules

1. Practice uses canonical VocabularyWord data.
2. Practice never owns a separate vocabulary database.
3. Four exercise types are fixed for MVP.
4. Question count cannot exceed available data.
5. Questions are generated once per session.
6. Correct/wrong scoring occurs once per question.
7. Result is shared across exercise types.
8. Review uses only incorrect questions.
9. Continue starts a new session.
10. No login is required.
11. No server-side user profile is required.
12. No commercial/subscription behavior is required.

## 22. Edge Cases

Handle:
- no vocabulary for selected HSK
- fewer words than requested
- empty writing input
- missing Pinyin
- missing audio
- duplicate rapid clicks
- browser refresh
- invalid practice type route
- invalid HSK route
- malformed vocabulary record

No edge case should cause a blank/crashed page.
