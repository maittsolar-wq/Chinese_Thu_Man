"""P5.10.3 -- Build the persistent special-review queue.

Deterministic, mechanical classification only -- no content authoring.
Scans the full HSK1-6 universe, excludes the P5.10.2 pilot's 100 IDs,
and places every remaining tier-3 (homograph, different reading) and
tier-4 (same-level same-pinyin duplicate) record into a persistent
special-review artifact. These records are permanently excluded from
the normal 100-record batch queue (see build_examples_queue_p103.py) --
they must never receive a blind-generated example.

Never modifies production. Never overwrites an existing special-review
artifact (rerun is a no-op once written, matching every other
generator in this project's fail-closed / refuse-to-overwrite pattern).

Usage:
    python build_examples_special_review_p103.py
"""

import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
PILOT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "hsk_examples_p102_pilot_01.json"
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "examples" / "hsk_examples_special_review_p103.json"


def load_json_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def load_universe() -> dict:
    universe = {}
    for n in range(1, 7):
        path = REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
        for r in json.loads(load_json_text(path)):
            universe[r["id"]] = {**r, "_level": n}
    return universe


def get_pos(r: dict) -> list:
    if r.get("partOfSpeech"):
        return r["partOfSpeech"]
    if r.get("cixing"):
        return [r["cixing"]]
    return []


def classify_risk_tiers(universe: dict) -> tuple[dict, dict]:
    word_pinyin = defaultdict(set)
    for r in universe.values():
        word_pinyin[r["word"]].add(r["pinyin"])
    homograph_words = {w for w, p in word_pinyin.items() if len(p) > 1}

    by_level_word_pinyin = defaultdict(list)
    for r in universe.values():
        by_level_word_pinyin[(r["_level"], r["word"], r["pinyin"])].append(r["id"])
    tier4_ids = {rid for ids in by_level_word_pinyin.values() if len(ids) > 1 for rid in ids}
    tier3_ids = {rid for rid, r in universe.items() if r["word"] in homograph_words} - tier4_ids

    tiers = {}
    reasons = {}
    for rid, r in universe.items():
        if rid in tier4_ids:
            tiers[rid] = 4
            siblings = [i for i in by_level_word_pinyin[(r["_level"], r["word"], r["pinyin"])] if i != rid]
            reasons[rid] = f"Tier 4: same word+pinyin '{r['word']}'/{r['pinyin']}' duplicated within HSK{r['_level']} by record(s) {siblings} -- cannot safely disambiguate sense without manual review."
        elif rid in tier3_ids:
            tiers[rid] = 3
            other_readings = sorted(word_pinyin[r["word"]] - {r["pinyin"]})
            reasons[rid] = f"Tier 3: '{r['word']}' also appears elsewhere in HSK1-6 under different reading(s) {other_readings} -- example could accidentally read naturally under the wrong tone/reading."
        else:
            pos = get_pos(r)
            cm = len(r.get("candidateMeanings") or [])
            tiers[rid] = 2 if (len(pos) > 1 or cm > 1) else 1
    return tiers, reasons


def main() -> None:
    if OUTPUT_PATH.exists():
        print(f"NOTE: {OUTPUT_PATH} already exists -- refusing to overwrite. No changes made.")
        return

    universe = load_universe()
    pilot = json.loads(load_json_text(PILOT_PATH))
    pilot_ids = {r["sourceId"] for r in pilot["records"]}

    remaining = sorted(set(universe) - pilot_ids)
    assert len(remaining) == 5300, f"expected 5300 remaining, got {len(remaining)}"

    tiers, reasons = classify_risk_tiers(universe)

    special_review_records = []
    for rid in remaining:
        if tiers[rid] in (3, 4):
            r = universe[rid]
            special_review_records.append({
                "sourceId": rid,
                "word": r["word"],
                "pinyin": r["pinyin"],
                "hskLevel": r["_level"],
                "riskTier": tiers[rid],
                "reason": reasons[rid],
                "sourceIssue": "homograph_different_reading" if tiers[rid] == 3 else "same_level_same_pinyin_duplicate",
                "status": "pending_review",
            })

    source_hashes = {}
    for n in range(1, 7):
        path = REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
        source_hashes[f"hsk{n}"] = hashlib.sha256(load_json_text(path).encode("utf-8")).hexdigest()

    artifact = {
        "queueLabel": "P5.10.3 -- Persistent Special-Review Queue (Tier 3 + Tier 4)",
        "queueVersion": "p103-v1",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "generatorScript": "tools/hsk/examples/build_examples_special_review_p103.py",
        "sourceProductionHashes": source_hashes,
        "pilotArtifactExcluded": "tools/hsk/examples/hsk_examples_p102_pilot_01.json (100 IDs excluded from this scan)",
        "totalRemainingScanned": len(remaining),
        "tier3Count": sum(1 for r in special_review_records if r["riskTier"] == 3),
        "tier4Count": sum(1 for r in special_review_records if r["riskTier"] == 4),
        "totalSpecialReviewCount": len(special_review_records),
        "records": special_review_records,
    }

    text = json.dumps(artifact, indent=2, ensure_ascii=False) + "\n"
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)

    print(f"Wrote {OUTPUT_PATH}")
    print(f"tier3={artifact['tier3Count']} tier4={artifact['tier4Count']} total={artifact['totalSpecialReviewCount']}")


if __name__ == "__main__":
    main()
