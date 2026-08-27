# Practice Prototype Specification v1.0

## Goal
Validate the complete Practice user journey on WEB before coding is considered final.

## Required prototype screens/states
P01 Practice Home
P02 Meaning Configuration
P03 Character Configuration
P04 Flashcard Configuration
P05 Writing Configuration
P06 Meaning Question — default
P07 Meaning Question — correct
P08 Meaning Question — wrong
P09 Character Question
P10 Character Correct
P11 Character Wrong
P12 Flashcard Front
P13 Flashcard Back
P14 Writing Default
P15 Writing Hint
P16 Writing Correct
P17 Writing Wrong
P18 Shared Result

## Required flows

### Correct path
Home → exercise → configuration → start → answer → next → final question → Result

### Wrong + retry
Question → wrong → feedback → Thử lại → same question → answer → next

### Wrong + next
Question → wrong → feedback → Tiếp theo → next question

### Flashcard
Configuration → front → click card → back → Đã nhớ/Không nhớ → next

### Writing
Configuration → writing question → Gợi ý → Pinyin → input → Kiểm tra đáp án → feedback → next

### Review wrong
Result → Ôn lại câu sai → incorrect questions only → Result

### Continue
Result → Luyện tập tiếp → NEW session

## Acceptance
Prototype is complete only when:
- all four exercise types have complete journeys
- every answer state is represented
- Result is reachable
- Review Wrong works
- Continue starts a new session
- Home navigation works
- there are no dead ends
