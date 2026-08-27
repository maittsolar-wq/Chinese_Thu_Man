# Chinese Thu Man — HOME Prototype Specification v1.0

## 1. Prototype Goal

Validate the Home information architecture and navigation before coding.

This prototype is for the WEB application.

## 2. Main Screen

### HOME-01 — Home Default

Must show:
- header/navigation
- welcome/hero area
- three core feature entries
- HSK quick access where present in the approved design

## 3. Interaction Map

```text
HOME
│
├── Click HSK
│   └── HSK Overview
│
├── Click Từ điển
│   └── Dictionary
│
├── Click Luyện tập
│   └── Practice Home
│
└── Click HSK Level
    └── Selected HSK Word List
```

## 4. Navigation States

### Active Home
`Trang chủ` highlighted.

### Navigate to HSK
Home remains the source page; HSK becomes active.

### Navigate to Dictionary
Dictionary becomes active.

### Navigate to Practice
Practice becomes active.

## 5. Dynamic Content State

If HSK counts are included:

Default:
```text
HSK 1
XXX từ
```

Loading:
```text
HSK 1
████
```

Error:
```text
Không thể tải dữ liệu
```

## 6. Prototype Acceptance

The prototype is accepted when:
- the three core feature destinations are obvious
- HSK levels are easy to discover
- every clickable element has a clear destination
- no dead-end CTA exists
- layout remains visually consistent with the approved UI
