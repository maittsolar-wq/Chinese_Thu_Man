# AI-Assisted HSK Meaning Pipeline v1

## Goal
Scale Vietnamese meaning enrichment for HSK 2+ without manually reviewing every word.

HSK 1 (300 fully reviewed records) is the pilot ground truth.

## Pipeline
Source -> Normalize -> Pinyin QA -> POS QA -> Meaning candidates
-> Cross-source check -> Confidence scoring -> Review routing
-> Human/expert review -> Final validation -> Production

## Routing proposal
- HIGH: >= 0.90 -> auto-pass, subject to deterministic validation
- MEDIUM: 0.70-0.89 -> review queue
- LOW: < 0.70 -> expert review

These thresholds are pilot values and must be calibrated before production use.

## Confidence signals
- agreement with reviewed/reference meaning
- meaningful token overlap
- non-empty valid meaning list
- source agreement
- POS agreement
- source/model conflicts as penalties

AI proposes; deterministic validators check; confidence routes; humans review uncertainty.

## HSK 1 calibration
Compare:
- data/hsk/hsk1/hsk1_meanings_draft_v2.json
- data/hsk/hsk1/hsk1_vocabulary_reviewed.json

The calibration experiment must not modify production data.

## Production safety
1. Never overwrite reviewed or production datasets during scoring.
2. Keep candidates and review queue separate.
3. Store reasons for every routed review.
4. Production requires final deterministic validation.
5. Do not treat an AI confidence score as truth until calibrated against human-reviewed samples.
