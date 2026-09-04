"""P5.10.3 -- Shared deterministic queue-building logic, imported by every
batch generator script (generate_examples_batch_p103.py and future
batches). Not a standalone entry point.

Resume rule: scans the pilot artifact, the special-review queue, and
every existing `examples_batch_*.json` file in this directory to build
the set of already-processed IDs, then returns the next N unprocessed
IDs from the deterministic tier1/2 queue (sorted ascending by id).
"""

import json
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
EXAMPLES_DIR = REPO_ROOT / "tools" / "hsk" / "examples"
PILOT_PATH = EXAMPLES_DIR / "hsk_examples_p102_pilot_01.json"
SPECIAL_REVIEW_PATH = EXAMPLES_DIR / "hsk_examples_special_review_p103.json"


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


def classify_risk_tiers(universe: dict) -> dict:
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
    for rid, r in universe.items():
        if rid in tier4_ids:
            tiers[rid] = 4
        elif rid in tier3_ids:
            tiers[rid] = 3
        else:
            pos = get_pos(r)
            cm = len(r.get("candidateMeanings") or [])
            tiers[rid] = 2 if (len(pos) > 1 or cm > 1) else 1
    return tiers


def get_completed_ids() -> set:
    """IDs already covered by the pilot, the special-review queue, or any
    existing completed batch artifact. Used for resume-safety."""
    completed = set()

    pilot = json.loads(load_json_text(PILOT_PATH))
    completed.update(r["sourceId"] for r in pilot["records"])

    if SPECIAL_REVIEW_PATH.exists():
        sr = json.loads(load_json_text(SPECIAL_REVIEW_PATH))
        completed.update(r["sourceId"] for r in sr["records"])

    for batch_file in sorted(EXAMPLES_DIR.glob("examples_batch_*.json")):
        batch = json.loads(load_json_text(batch_file))
        completed.update(r["sourceId"] for r in batch["records"])

    return completed


def get_next_batch_ids(batch_size: int = 100) -> tuple[list, dict, dict]:
    """Returns (next_ids, universe, tiers) -- the next `batch_size`
    unprocessed tier1/2 IDs in deterministic (tier, id) order."""
    universe = load_universe()
    tiers = classify_risk_tiers(universe)
    completed = get_completed_ids()

    eligible = sorted(
        (rid for rid, r in universe.items() if rid not in completed and tiers[rid] in (1, 2)),
        key=lambda rid: (tiers[rid], rid),
    )
    return eligible[:batch_size], universe, tiers


def next_batch_number() -> int:
    """Pilot is batch 001. Next sequential batch number based on existing
    examples_batch_*.json files."""
    existing = sorted(EXAMPLES_DIR.glob("examples_batch_*.json"))
    if not existing:
        return 2
    numbers = [int(p.stem.split("_")[-1]) for p in existing]
    return max(numbers) + 1
