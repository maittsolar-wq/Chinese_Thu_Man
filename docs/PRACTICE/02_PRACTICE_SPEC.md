# Practice Specification v1.0

## 1. Home
Title:
`LUYỆN TẬP`

Subtitle:
`Học từ vựng theo 6 cấp độ HSK từ cơ bản đến nâng cao.`

Cards:
- `Chọn nghĩa` — `Chọn nghĩa tiếng việt đúng với từ vựng`
- `Chọn chữ Hán` — `Chọn chữ Hán đúng với nghĩa`
- `Flashcard` — `Ôn tập từ vựng với thẻ ghi nhớ`
- `Luyện viết` — `Nhập tiếng Trung theo nghĩa tiếng việt`

## 2. Configuration
Shared by all four exercise types.

Fields:
- Phạm vi luyện tập: HSK 1–HSK 6
- Số lượng từ: Tất cả / 50 / 20 / 10
- CTA: `Bắt đầu luyện tập`

Default shown in supplied UI:
- HSK 2
- 20

If requested count exceeds available vocabulary, use the available count.

## 3. Session
Minimum session data:
```text
sessionId
exerciseType
hskLevel
requestedCount
actualCount
currentIndex
correctCount
wrongCount
startedAt
completedAt
questions[]
```

Each question:
```text
questionId
vocabularyId
questionType
correctAnswer
userAnswer
isCorrect
attemptCount
status
```

Statuses:
`unanswered`, `answered_correct`, `answered_wrong`, `skipped`

## 4. Chọn nghĩa
Prompt:
Chinese + Pinyin.

Example:
`学习`
`xuéxí`

Four Vietnamese options. Correct position must be randomized.

Correct feedback:
`✓ Chính xác!`
`Đáp án: Học, học tập`
`Tiếp theo`

Wrong feedback:
`✕ Chưa chính xác!`
`Bạn chọn: Giáo viên`
`Đáp án: Học, học tập`
`Thử lại` / `Tiếp theo`

## 5. Chọn chữ Hán
Prompt is Vietnamese meaning.

Example:
`Học, học tập`

Four Chinese options:
- 学习
- 学生
- 学校
- 老师

Use the same correct/wrong/retry/next logic.

## 6. Flashcard
Front:
- Chinese
- Pinyin
- Audio
- `Nhấn vào thẻ để xem nghĩa`

Back:
- Chinese
- Pinyin
- Vietnamese meaning

Actions:
- `Không nhớ` = wrong
- `Đã nhớ` = correct

A card can only be scored once.

## 7. Luyện viết
Prompt:
Vietnamese meaning.

Input placeholder:
`Nhập Tiếng Trung`

Hint:
`Gợi ý`

Hint reveals Pinyin only, not the Chinese answer.

Actions:
`Không nhớ`
`Kiểm tra đáp án`

Correct:
`✓ Chính xác!`
`Đáp án: 学习`
`Tiếp theo`

Wrong:
`✕ Chưa chính xác!`
`Bạn chọn: 学校`
`Đáp án: 学习`
`Thử lại` / `Tiếp theo`

Empty input is not valid.

## 8. Progress
Display `current/total`.
Progress is calculated from the actual session count.

## 9. Answer locking
After an answer is submitted:
- prevent changing the answer
- prevent duplicate scoring
- prevent multiple rapid advances

## 10. Retry
`Thử lại` keeps the same question and does not advance the index.

`Tiếp theo` advances once and preserves the recorded result.

## 11. Result
All four exercise types use one shared Result screen.

Display:
`Kết quả luyện tập`
celebration illustration
result message
`18/20 câu` style completion count
statistics:
- Đúng
- Sai
- Độ chính xác

Accuracy:
`correctCount / actualCount * 100`

Example:
18/20 = **90%**, not 80%.

If wrongCount > 0:
`Ôn lại {wrongCount} câu sai`

Always provide:
`Luyện tập tiếp`
`Về trang chủ`

If wrongCount == 0, hide Review Wrong.

## 12. Review Wrong
Use only questions answered incorrectly in the completed session.
Do not generate unrelated questions.

Flow:
`Result → Ôn lại câu sai → wrong questions → Result`

## 13. Continue Practice
Starts a NEW session.
Do not mutate the completed session.

Keep exercise type and HSK scope by default and select fresh questions when possible.

## 14. Exit
Leaving an unfinished session should show confirmation:
`Thoát luyện tập?`
`Tiến độ hiện tại sẽ không được lưu.`

Actions:
`Ở lại`
`Thoát`

Do not treat an unfinished session as a completed result.

## 15. Randomization
Generate the question set once at session creation.
Do not randomize again on every render.
Randomize option positions before the question is displayed.

## 16. Minimum vocabulary model
```text
id
hskLevel
chinese
pinyin
meaningVi
audioUrl
```

## 17. Edge cases
Handle:
- empty dataset
- fewer items than requested
- duplicate rapid clicks
- repeated submission
- empty writing input
- refresh during active session
- invalid practice route
- missing audio
- missing Pinyin
- malformed vocabulary data

Never show a blank/crashed Practice page.
