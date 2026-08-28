#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--level", type=int, required=True)
    p.add_argument("--input", required=True)
    p.add_argument("--output")
    a = p.parse_args()
    src = Path(a.input)
    if not src.exists(): raise SystemExit(f"Missing: {src}")
    with src.open("r", encoding="utf-8") as f: records = json.load(f)
    if not isinstance(records, list): raise SystemExit("Input must be a JSON array.")
    out = Path(a.output) if a.output else src.parent / f"hsk{a.level}_meaning_review_queue.json"
    queue = []
    for r in records:
        if not isinstance(r, dict): continue
        routing = str(r.get("routing", "")).upper()
        if routing == "HIGH": continue
        if routing not in {"MEDIUM", "LOW"}:
            routing = "MEDIUM"
            reason = "missing_confidence_routing"
        else:
            reason = r.get("reason", "candidate_requires_review")
        queue.append({
            "id": r.get("id"), "word": r.get("word"), "pinyin": r.get("pinyin"),
            "meaningVi": r.get("meaningVi", []), "confidence": r.get("confidence"),
            "routing": routing, "reviewStatus": "pending",
            "reviewReasons": [reason]
        })
    out.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Candidate records: {len(records)}")
    print(f"Queue records:     {len(queue)}")
    print(f"Output:            {out}")

if __name__ == "__main__":
    main()
