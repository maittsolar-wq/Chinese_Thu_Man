# Practice Development Specification v1.0

## Target
Implement the Practice module in the existing **WEB application**.

Before coding, inspect the repository:
- framework
- package manager
- routing
- styling
- reusable components
- state management
- data layer
- tests

Reuse the existing architecture. Do not silently migrate frameworks.

## Responsibilities
Separate:
- Practice Home
- Configuration
- Session state
- Question generation
- Answer validation
- Result calculation
- Result UI
- Review Wrong

## Reusable components
Prefer shared components for:
```text
PracticeCard
PracticeConfig
HSKSelector
QuestionProgress
QuestionOption
AnswerFeedback
Flashcard
WritingInput
HintButton
ResultStats
ResultActions
```

Use repository naming conventions where they differ.

## Session lifecycle
```text
create session
→ generate questions
→ show current question
→ record answer
→ update score
→ advance
→ complete
→ calculate result
→ Result
```

## Integrity
Question data is generated once per session.
Do not randomize on every render.
Do not hard-code results.

## Result calculation
```text
total = actualCount
correct = correctCount
wrong = total - correct
accuracy = correct / total * 100
```

18/20 must display 90%.

## Review Wrong
Build the review session from the completed session's incorrect questions.

## Continue
Create a new session, not a mutation of the completed session.

## Routing
Use the existing web router. Conceptual routes may be:
```text
/practice
/practice/meaning
/practice/character
/practice/flashcard
/practice/writing
```
Follow the repository's actual conventions if different.

## Persistence
If persistence already exists, integrate with it.
Completed results should be representable by:
```text
exerciseType
hskLevel
total
correct
wrong
accuracy
completedAt
```

## Implementation order
1. Inspect repository
2. Shared models/state
3. Configuration
4. Chọn nghĩa
5. Chọn chữ Hán
6. Flashcard
7. Luyện viết
8. Shared Result
9. Review Wrong
10. Continue Practice
11. Edge cases
12. Tests
13. Build
14. Visual verification

## Do not change without approval
Do not independently change:
- product terminology
- exercise types
- Result structure
- navigation
- scoring rules
- HSK behavior
- question-count behavior
- visual hierarchy
