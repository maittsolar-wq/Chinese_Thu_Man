# Chinese Thu Man — Project Context

## Scope
Chinese Thu Man is currently a **WEB-ONLY Chinese learning application** for Vietnamese learners.

**Critical constraint:** Do not convert this project to Flutter, React Native, native iOS, native Android, or another mobile application. Use the existing web stack in the repository.

## Product
Main navigation currently shown:
- Trang chủ
- HSK
- Từ điển
- Luyện tập

The current focus is the **Luyện tập** module.

## Practice types
1. Chọn nghĩa
2. Chọn chữ Hán
3. Flashcard
4. Luyện viết

The four types share configuration, session management, progress, Result, Review Wrong, Continue Practice and Home navigation.

## Source of truth
The supplied UI screenshots are the primary visual reference. Preserve:
- desktop web composition
- white background
- blue primary color
- rounded cards
- light borders/shadows
- Vietnamese UI
- clear Chinese/Pinyin typography
- green correct states
- red incorrect states
- yellow/orange hint states

Do not introduce unrelated UX patterns.

## Implementation principle
Separate UI, vocabulary data, practice state, question generation, validation and result calculation.

Do not hard-code scores or results.
