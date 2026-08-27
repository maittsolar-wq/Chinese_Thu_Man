# Chinese Thu Man — PRACTICE Prototype Specification v1.0

## 1. Goal

Validate the complete four-exercise vocabulary practice flow on WEB before coding.

## 2. Screens

### PRA-01 — Practice Home
Four cards:
- Chọn nghĩa
- Chọn chữ Hán
- Flashcard
- Luyện viết

### PRA-02 — Configuration
- HSK selector
- question count
- Start button

### PRA-03 — Chọn nghĩa Default
- progress
- Chinese
- Pinyin
- four Vietnamese answers

### PRA-04 — Chọn nghĩa Correct
- selected answer green
- correct feedback
- Next

### PRA-05 — Chọn nghĩa Wrong
- selected answer red
- correct answer
- Retry
- Next

### PRA-06 — Chọn chữ Hán
- Vietnamese meaning
- four Chinese options

### PRA-07 — Chọn chữ Hán Correct/Wrong
Use the same feedback pattern.

### PRA-08 — Flashcard Front
- Chinese
- Pinyin
- audio
- tap/click card instruction

### PRA-09 — Flashcard Back
- Chinese
- Pinyin
- Vietnamese meaning
- Đã nhớ
- Không nhớ

### PRA-10 — Luyện viết Default
- Vietnamese meaning
- input
- Gợi ý
- Không nhớ
- Kiểm tra đáp án

### PRA-11 — Luyện viết Hint
Pinyin visible, Chinese answer hidden.

### PRA-12 — Luyện viết Correct
Correct feedback + Next.

### PRA-13 — Luyện viết Wrong
Wrong feedback + Retry + Next.

### PRA-14 — Result
Shared result screen for all four types.

Show:
- score
- accuracy
- review wrong when applicable
- continue
- home

## 3. Flows

### Meaning
```text
Home
→ Chọn nghĩa
→ Configuration
→ Start
→ Question
→ Answer
→ Next
→ ...
→ Result
```

### Character
```text
Home
→ Chọn chữ Hán
→ Configuration
→ Start
→ Question
→ Answer
→ Next
→ Result
```

### Flashcard
```text
Home
→ Flashcard
→ Configuration
→ Start
→ Front
→ Back
→ Đã nhớ/Không nhớ
→ Next
→ Result
```

### Writing
```text
Home
→ Luyện viết
→ Configuration
→ Start
→ Meaning
→ Gợi ý
→ Input
→ Kiểm tra
→ Feedback
→ Next
→ Result
```

### Review
```text
Result
→ Ôn lại câu sai
→ Incorrect questions
→ Result
```

### Continue
```text
Result
→ Luyện tập tiếp
→ New Configuration/Session
```

## 4. Prototype States

Must demonstrate:
- default
- selected answer
- correct
- wrong
- retry
- hint
- flashcard front
- flashcard back
- result
- no wrong answers
- wrong answers
- empty/no-data state

## 5. Acceptance

No dead-end interaction.
All four exercise types reach Result.
Review Wrong only appears when there are errors.
Continue starts a new session.
