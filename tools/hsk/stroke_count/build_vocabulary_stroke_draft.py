"""
Stroke Count Pass 02 — step 3: draft word-level strokeCount.

Confirmed product rule: strokeCount = SUM of kTotalStrokes across every
character OCCURRENCE in the word (repeated characters count once per
occurrence, not deduplicated). The known 12 digit-suffix records use
their normalized (suffix-stripped) word for this calculation.

Reads only: vocabulary_records_normalized.json, character_stroke_map.json.
Writes only: vocabulary_stroke_draft.json, vocabulary_review_queue.json.
Touches NO production file. Does not write strokeCount back into any
data/hsk/*.json file.
"""
import json
import sys
import statistics
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent

# Soft plausibility bounds per character (not a hard reject) — used only
# to flag outliers for the review queue, never to fail a record.
MIN_PLAUSIBLE_PER_CHAR = 1
MAX_PLAUSIBLE_PER_CHAR = 30  # kTotalStrokes tops out well under this for all common Han characters

def main():
    records = json.loads((OUT_DIR / "vocabulary_records_normalized.json").read_text(encoding="utf-8"))
    char_map = json.loads((OUT_DIR / "character_stroke_map.json").read_text(encoding="utf-8"))["mapping"]

    draft = []
    review_queue = []
    warnings = []

    for rec in records:
        rid = rec["id"]
        word = rec["word"]
        normalized = rec["normalizedWord"]
        characters = list(normalized)

        char_entries = []
        unresolved_chars = []
        for ch in characters:
            entry = char_map.get(ch)
            if entry is None:
                unresolved_chars.append(ch)
                char_entries.append({"character": ch, "strokeCount": None})
            else:
                char_entries.append({"character": ch, "strokeCount": entry["strokeCount"]})

        if unresolved_chars:
            status = "unresolved"
            total = None
            review_queue.append({
                "id": rid, "word": word, "normalizedWord": normalized,
                "reason": "unresolved_character",
                "characters": sorted(set(unresolved_chars)),
                "proposedAction": "Resolve missing character(s) in character_review_queue.json first, then regenerate.",
            })
        else:
            status = "resolved"
            total = sum(c["strokeCount"] for c in char_entries)

            # Plausibility checks (warnings only, never a failure).
            per_char_avg = total / len(characters) if characters else 0
            if per_char_avg > MAX_PLAUSIBLE_PER_CHAR or per_char_avg < MIN_PLAUSIBLE_PER_CHAR:
                warnings.append({
                    "id": rid, "word": word, "total": total, "charCount": len(characters),
                    "reason": "outlier_average_strokes_per_character",
                    "detail": f"avg {per_char_avg:.1f} strokes/char across {len(characters)} char(s)",
                })

        draft.append({
            "id": rid,
            "hskLevel": rec["hskLevel"],
            "word": word,
            "normalizedWord": normalized,
            "digitSuffixStripped": rec["digitSuffixStripped"],
            "characters": char_entries,
            "strokeCount": total,
            "status": status,
        })

    resolved = [d for d in draft if d["status"] == "resolved"]
    unresolved = [d for d in draft if d["status"] != "resolved"]

    summary = {
        "totalRecords": len(draft),
        "resolvedCount": len(resolved),
        "unresolvedCount": len(unresolved),
        "coveragePercent": round(100.0 * len(resolved) / len(draft), 4) if draft else 0.0,
        "warningCount": len(warnings),
        "warnings": warnings,
    }

    (OUT_DIR / "vocabulary_stroke_draft.json").write_text(
        json.dumps({"summary": summary, "records": draft}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT_DIR / "vocabulary_review_queue.json").write_text(
        json.dumps(review_queue, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"totalRecords={summary['totalRecords']}")
    print(f"resolvedCount={summary['resolvedCount']}")
    print(f"unresolvedCount={summary['unresolvedCount']}")
    print(f"coveragePercent={summary['coveragePercent']}")
    print(f"warningCount={summary['warningCount']}")
    for w in warnings:
        print(f"  WARNING: {w}")

if __name__ == "__main__":
    sys.exit(main())
