# Chinese Thu Man — HSK 1 Pilot Tool v0.1

## Mục tiêu

Tạo dataset HSK 1 gồm đúng 300 từ từ source HSK 3.0 2026 đã chọn.

## Chạy

Yêu cầu Python 3.

```bash
python build_hsk1_base.py
```

Script sẽ tải:

`https://raw.githubusercontent.com/profesorm/hsk30/main/data/hsk_vocabulary.csv`

và tạo:

```text
output/
├── hsk1_vocabulary_base.json
├── hsk1_vocabulary_base.csv
├── hsk1_meaning_review_queue.json
└── hsk1_metadata.json
```

## Quan trọng

Đây mới là SOURCE BASE, chưa phải production data.

Đã có:
- Chinese
- Pinyin
- source POS
- HSK 1 mapping
- source ordering

Chưa có:
- Vietnamese meaning
- related words
- examples
- audio
- stroke data

Không đưa output vào app production trước khi hoàn tất validation và license/provenance review.

## Vì sao script kiểm tra đúng 300?

Nếu source thay đổi và không còn đúng 300 record cho `一级`, script sẽ dừng thay vì âm thầm tạo dataset sai.
