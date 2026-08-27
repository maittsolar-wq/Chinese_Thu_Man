# Chinese Thu Man — DICTIONARY Prototype Specification v1.0

## 1. Goal

Validate the complete Dictionary interaction flow on WEB.

## 2. Required Screens

### DICT-01 — Dictionary Default

Show:
- header
- page title
- search field
- search action
- default empty/search state

### DICT-02 — Search Results

Example query:

`学习`

Show:

```text
学习
xuéxí
học, học tập
```

Optionally show HSK level/audio if approved.

### DICT-03 — No Results

Example query:

`abcdef`

Show:
`Không tìm thấy từ phù hợp`

### DICT-04 — Word Detail

Selecting `学习` opens the shared Word Detail.

## 3. Main Flow

```text
Từ điển
→ nhập 学习
→ Search
→ kết quả
→ click 学习
→ Word Detail
```

## 4. Pinyin Flow

```text
Từ điển
→ nhập xuexi
→ kết quả
→ 学习
```

## 5. Vietnamese Flow

```text
Từ điển
→ nhập học
→ kết quả
→ 学习
```

## 6. Empty State

```text
Từ điển
→ chưa nhập query
```

No no-result message.

## 7. No Result State

```text
Từ điển
→ query không tồn tại
→ Không tìm thấy từ phù hợp
```

## 8. Prototype Acceptance

- search is visually obvious
- result is easy to scan
- no-result state is clear
- result opens Word Detail
- Dictionary and HSK share the same Word Detail concept
- no extra sidebar or unrelated feature is introduced
