# Claude Code Instructions — Chinese Thu Man

## Role
You are the implementation agent for the existing Chinese Thu Man **WEB application**.

## Critical constraint
This is currently WEB ONLY.

Do NOT:
- create Flutter code
- create native iOS/Android code
- migrate the project to a mobile framework
- replace the existing web stack without explicit approval

## Before coding
Read:
```text
00_PROJECT_CONTEXT.md
01_UI_DESIGN_SYSTEM.md
02_PRACTICE_SPEC.md
03_PROTOTYPE_SPEC.md
04_DEVELOPMENT_SPEC.md
05_QA_SPEC.md
```

Then inspect the repository and determine the actual framework, routing, styling, data and test architecture.

## Source of truth
The supplied UI screenshots and the Markdown specifications are the source of truth.

Follow them instead of inventing new UX.

## Coding rules
- Reuse existing components and design tokens.
- Separate UI from state and data.
- Do not hard-code scores or accuracy.
- Generate questions once per session.
- Prevent duplicate scoring and rapid multi-advance.
- Keep Result shared across all four exercise types.
- Review Wrong must use the actual incorrect questions.
- Continue Practice must create a new session.
- Keep the web architecture intact.

## Scope discipline
Do not rewrite unrelated modules.
Do not delete existing features.
Do not silently change product terminology or business rules.

If a repository conflict requires a product-level decision, stop and report:
1. conflict
2. affected files
3. smallest proposed solution

## Implementation order
1. Repository inspection
2. Shared Practice state/models
3. Configuration
4. Chọn nghĩa
5. Chọn chữ Hán
6. Flashcard
7. Luyện viết
8. Result
9. Review Wrong
10. Continue Practice
11. Edge cases
12. Tests
13. Build
14. Visual verification

## Completion report
After implementation report:
- files created
- files modified
- features implemented
- tests run
- build result
- known issues
- deviations from the supplied UI/spec
