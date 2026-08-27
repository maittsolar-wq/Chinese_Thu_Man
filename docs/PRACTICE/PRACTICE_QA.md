# Chinese Thu Man — PRACTICE QA Specification v1.0

## 1. Home

### PRA-QA-001
Open Practice.

Expected:
- four exercise types visible
- Practice active in navigation

### PRA-QA-002
Click each exercise card.

Expected:
- corresponding configuration opens

## 2. Configuration

### PRA-QA-010
Verify HSK 1–6.

### PRA-QA-011
Verify counts:
- Tất cả
- 50
- 20
- 10

### PRA-QA-012
Request more words than available.

Expected:
- actual session count equals available vocabulary count
- no invalid questions

## 3. Chọn nghĩa

### PRA-QA-020
Start session.

Expected:
- Chinese + Pinyin
- four Vietnamese options
- progress correct

### PRA-QA-021
Correct answer.

Expected:
- green state
- correct feedback
- score +1
- Next advances once

### PRA-QA-022
Wrong answer.

Expected:
- selected option red
- correct answer shown
- Retry and Next visible

### PRA-QA-023
Retry.

Expected:
- same question
- index unchanged
- no duplicate score

## 4. Chọn chữ Hán

### PRA-QA-030
Question shows Vietnamese meaning + four Chinese options.

### PRA-QA-031
Correct/wrong behavior matches specification.

### PRA-QA-032
Correct option position changes between generated questions but remains stable during the current question.

## 5. Flashcard

### PRA-QA-040
Front state:
- Chinese
- Pinyin
- audio when available

### PRA-QA-041
Click card.

Expected:
- back state
- Vietnamese meaning visible

### PRA-QA-042
Click Đã nhớ.

Expected:
- correct +1
- advance once

### PRA-QA-043
Click Không nhớ.

Expected:
- wrong +1
- advance once

### PRA-QA-044
Rapidly click both actions.

Expected:
- only one score
- only one advance

## 6. Luyện viết

### PRA-QA-050
Empty input.

Expected:
- cannot be accepted as correct

### PRA-QA-051
Correct Chinese input.

Expected:
- correct feedback
- correct +1

### PRA-QA-052
Wrong input.

Expected:
- wrong feedback
- user's answer shown
- correct answer shown

### PRA-QA-053
Click Gợi ý.

Expected:
- Pinyin appears
- Chinese answer remains hidden

### PRA-QA-054
Whitespace around correct answer.

Expected:
- harmless leading/trailing whitespace does not make a correct answer wrong

## 7. Progress

### PRA-QA-060
20-question session.

Expected:
`1/20`, `2/20`, ..., `20/20`

No skipped or duplicated indexes.

## 8. Result

### PRA-QA-070
20/20.

Expected:
```text
Đúng 20
Sai 0
100%
```
Review button hidden.

### PRA-QA-071
18/20.

Expected:
```text
Đúng 18
Sai 2
90%
Ôn lại 2 câu sai
```

### PRA-QA-072
10/20.

Expected:
```text
Đúng 10
Sai 10
50%
Ôn lại 10 câu sai
```

## 9. Review Wrong

### PRA-QA-080
Complete a session with 3 incorrect questions.

Click Review Wrong.

Expected:
- exactly 3 review questions
- all originated from incorrect questions
- no unrelated vocabulary

### PRA-QA-081
Complete review.

Expected:
- separate Result
- original session result remains unchanged

## 10. Continue

### PRA-QA-090
Click Luyện tập tiếp.

Expected:
- new session
- progress starts again
- old result is not mutated

## 11. Exit

### PRA-QA-100
Leave active session.

Expected:
- exit confirmation

### PRA-QA-101
Click Ở lại.

Expected:
- session remains

### PRA-QA-102
Click Thoát.

Expected:
- leaves session
- unfinished session is not counted as completed

## 12. Edge Cases

### PRA-QA-110
No vocabulary for selected HSK.

Expected:
- friendly empty state
- no crash

### PRA-QA-111
Missing audio.

Expected:
- no broken player

### PRA-QA-112
Missing Pinyin.

Expected:
- page remains usable

### PRA-QA-113
Invalid exercise route.

Expected:
- friendly not-found/redirect

### PRA-QA-114
Rapid clicks.

Expected:
- no double score
- no multi-step advance
- no corrupted result

## 13. Data Integrity

### PRA-QA-120
Compare Practice word data with HSK/Dictionary.

Expected:
- same canonical vocabulary record

### PRA-QA-121
Update canonical vocabulary.

Expected:
- Practice uses updated vocabulary without a separate duplicated dataset

## 14. Visual QA

Check approved UI:
- white background
- primary blue `#025291`
- active navigation
- cards
- buttons
- question hierarchy
- Chinese typography
- Pinyin
- answer options
- progress
- green/red feedback
- Result layout

Do not introduce an unapproved sidebar or additional dashboard UI.

## 15. Responsive WEB QA

Test desktop, medium and narrow browser widths.

Expected:
- no horizontal overflow
- questions remain readable
- answer options remain usable
- controls remain accessible

## 16. Build QA

- dev server starts
- production build succeeds
- no Practice console errors
- no broken Practice routes
- no missing critical assets
