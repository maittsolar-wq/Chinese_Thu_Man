#!/usr/bin/env python3
"""
Generic HSK AI meaning-generation adapter.

IMPORTANT:
- This version does NOT call an external AI API.
- It prepares a provider-neutral generation request package.
- It deliberately does not copy reviewed meanings / ground truth.
- It is the adapter boundary for the next AI provider integration.

Run from project root:
    python tools/hsk/generate_meaning_candidates.py --level 1

Input:
    data/hsk/hsk{level}/hsk{level}_ai_meaning_candidates_input.json

Output:
    data/hsk/hsk{level}/hsk{level}_meaning_generation_requests.json

The generated request package can later be consumed by an AI adapter.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_json(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def extract_records(data):
    if isinstance(data, list):
        return data

    if isinstance(data, dict) and isinstance(data.get("records"), list):
        return data["records"]

    raise SystemExit(
        "Input must be a JSON array or an object containing a 'records' array."
    )


def build_prompt(record, level):
    word = record["word"]
    pinyin = record["pinyin"]
    pos = record.get("partOfSpeech") or []

    pos_text = ", ".join(pos) if pos else "unknown"

    return (
        "Generate concise Vietnamese dictionary meanings for the Chinese "
        "vocabulary item below.\n\n"
        f"HSK level: {level}\n"
        f"Chinese: {word}\n"
        f"Pinyin: {pinyin}\n"
        f"Part of speech: {pos_text}\n\n"
        "Rules:\n"
        "1. Return only common Vietnamese meanings appropriate for this "
        "vocabulary item.\n"
        "2. Prefer 1-3 concise meanings.\n"
        "3. Do not invent meanings from context that are not standard "
        "dictionary senses.\n"
        "4. Preserve distinctions between parts of speech when relevant.\n"
        "5. Do not include Pinyin, Chinese characters, examples, explanations, "
        "or English.\n"
        "6. Output JSON only with this shape:\n"
        '{"meaningVi":["...","..."]}'
    )


def main():
    parser = argparse.ArgumentParser(
        description="Build provider-neutral AI meaning generation requests."
    )
    parser.add_argument("--level", type=int, required=True)
    parser.add_argument("--input")
    parser.add_argument("--output")
    args = parser.parse_args()

    if args.level < 1 or args.level > 6:
        raise SystemExit("--level must be between 1 and 6.")

    data_dir = ROOT / "data" / "hsk" / f"hsk{args.level}"

    input_path = (
        Path(args.input)
        if args.input
        else data_dir / f"hsk{args.level}_ai_meaning_candidates_input.json"
    )

    output_path = (
        Path(args.output)
        if args.output
        else data_dir / f"hsk{args.level}_meaning_generation_requests.json"
    )

    source_data = load_json(input_path)
    records = extract_records(source_data)

    requests = []
    seen_ids = set()

    for record in records:
        if not isinstance(record, dict):
            raise SystemExit("Input contains a non-object record.")

        record_id = record.get("id")
        word = str(record.get("word", "")).strip()
        pinyin = str(record.get("pinyin", "")).strip()

        if not record_id:
            raise SystemExit("Input record missing id.")

        if record_id in seen_ids:
            raise SystemExit(f"Duplicate input id: {record_id}")
        seen_ids.add(record_id)

        if not word:
            raise SystemExit(f"{record_id}: empty Chinese word.")

        if not pinyin:
            raise SystemExit(f"{record_id}: empty Pinyin.")

        requests.append(
            {
                "id": record_id,
                "word": word,
                "pinyin": pinyin,
                "introducedLevel": record.get("introducedLevel"),
                "hskLevels": record.get("hskLevels", []),
                "partOfSpeech": record.get("partOfSpeech", []),
                "prompt": build_prompt(record, args.level),
                "expectedOutputSchema": {
                    "meaningVi": ["string"]
                },
                "generationStatus": "pending",
                "provider": None,
                "model": None,
                "modelVersion": None,
                "generatedAt": None,
                "rawResponse": None,
            }
        )

    payload = {
        "datasetName": f"Chinese Thu Man HSK {args.level}",
        "type": "AI_MEANING_GENERATION_REQUESTS",
        "version": 1,
        "level": args.level,
        "recordCount": len(requests),
        "groundTruthIncluded": False,
        "productionIncluded": False,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "records": requests,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=" * 64)
    print(f"HSK {args.level} AI MEANING GENERATION REQUEST BUILD")
    print("=" * 64)
    print()
    print(f"Input records:      {len(records)}")
    print(f"Generation requests:{len(requests)}")
    print(f"Ground truth:       NOT INCLUDED")
    print(f"Production data:    NOT INCLUDED")
    print(f"Output:             {output_path}")
    print()
    print("SUCCESS")
    print("Provider-neutral AI generation request package created.")
    print()
    print("IMPORTANT:")
    print("No AI API was called.")
    print("No reviewed or production data was modified.")
    print("Next step: connect an AI provider adapter to these requests.")


if __name__ == "__main__":
    main()
