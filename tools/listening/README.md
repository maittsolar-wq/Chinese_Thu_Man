# Listening title-metadata preparation

This tool creates reviewable candidate records from video filenames. It is not a production `lesson.json` writer because this repository has no approved `lesson.json` contract.

```powershell
node tools/listening/prepare-lesson-title-metadata.mjs listening_batch_001_010 candidates.json
node tools/listening/prepare-lesson-title-metadata.test.mjs
```

The zero-padded filename number becomes `id`. A suffix becomes a Vietnamese-readable candidate with `vietnameseTitleSource: "filename"`; a number-only filename has no Vietnamese title candidate. The tool never derives Chinese: it emits `chineseTitle: null`, `chineseTitleSource: null`, and `needsReview: true`.

A future ingestion step may add Chinese only from verified metadata, an explicit creator title, or clear transcript/video extraction. OCR/AI inference must be `chineseTitleSource: "inferred"`, retain `needsReview: true`, and never overwrite verified data. The UI already consumes `chineseTitle` and `vietnameseTitle` from `ListeningLesson` through `listeningRepository`; it does not parse, translate, OCR, or call AI at runtime.
