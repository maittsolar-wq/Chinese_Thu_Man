# Chinese Thu Man — Project Context v1.0

## Platform
Chinese Thu Man is currently a **WEB-ONLY** Chinese vocabulary learning website for Vietnamese learners.
Do not build Flutter, React Native, native iOS, native Android, or a mobile app. Responsive behavior means responsive WEB only.

## MVP purpose
The product focuses on:
- learning HSK vocabulary
- reviewing vocabulary
- browsing vocabulary by HSK level
- searching vocabulary
- viewing word details
- practicing vocabulary

## Main areas
1. Trang chủ
2. HSK
3. Từ điển
4. Luyện tập

## Practice
Four exercise types:
- Chọn nghĩa
- Chọn chữ Hán
- Flashcard
- Luyện viết

## MVP exclusions
No login, registration, cloud user profile, payments, subscriptions, notifications, admin dashboard, social/community features, or mobile app unless explicitly requested later.

## Product language
Vietnamese UI. Vocabulary uses Chinese + Pinyin + Vietnamese meaning.

## Source of truth
Approved UI screenshots and approved Markdown specifications are the source of truth. Do not invent unrelated features.

## Architecture principle
Use one canonical vocabulary dataset shared by HSK, Dictionary, Word Detail, Practice and Home summaries.

## Workflow
UI Design → Specification → Data Specification → Prototype → Review → Development Specification → Claude Code → Build → QA → Fix → Regression.
