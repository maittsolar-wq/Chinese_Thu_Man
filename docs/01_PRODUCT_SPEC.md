# Chinese Thu Man — Product Specification v1.0

## Information architecture
```text
Chinese Thu Man
├── Trang chủ
├── HSK
│   ├── HSK Overview
│   ├── HSK 1–6
│   │   └── Word List
│   │       └── Word Detail
├── Từ điển
│   ├── Dictionary
│   ├── Search Result
│   ├── No Result
│   └── Word Detail
└── Luyện tập
    ├── Practice Home
    ├── Configuration
    ├── Chọn nghĩa
    ├── Chọn chữ Hán
    ├── Flashcard
    ├── Luyện viết
    └── Result
```

## Home
Entry point to HSK, Dictionary and Practice. Keep it simple; no complex personal dashboard.

## HSK
Users select HSK 1–6, open a Word List and then Word Detail. Vocabulary counts come from data; never hard-code them.

Word List approved filters:
- Tất cả
- Chưa học
- Đang học
- Đã thuộc
- Ôn tập

Current MVP has no persistent user learning profile. Do not invent server-side status storage.

## Word Detail
Shows:
- breadcrumb
- Chinese
- Pinyin
- Vietnamese meaning
- HSK level
- stroke count
- audio action when available
- stroke-order section
- related words
- example sentences

Favorite/save and learning-status behavior only when explicitly supported by the current MVP state model.

## Dictionary
Search the same canonical vocabulary dataset used by HSK. Search may support Chinese, Pinyin and Vietnamese meaning. Results open Word Detail. Do not create a duplicate dictionary database.

## Practice
Four types:
- Chọn nghĩa: Chinese/Pinyin → Vietnamese
- Chọn chữ Hán: Vietnamese → Chinese
- Flashcard: reveal meaning → Đã nhớ/Không nhớ
- Luyện viết: Vietnamese → user enters Chinese

Configuration:
- HSK 1–6
- Tất cả / 50 / 20 / 10

All use a shared Result screen.

## Result
Show:
- completion message
- total
- correct
- wrong
- accuracy
- Ôn lại X câu sai when errors exist
- Luyện tập tiếp
- Về trang chủ

Accuracy = correct / total × 100. Example: 18/20 = 90%.

## Navigation
Main navigation:
Trang chủ | HSK | Từ điển | Luyện tập

Word Detail can be reached from HSK Word List and Dictionary results.

## Non-goals
No accounts, payment, subscription, social features, teacher/admin management, complex analytics, or mobile application in MVP.
