"""P5.4.2 -- HSK1 Related-Word FINAL SELECTION, built from the P5.4.1
candidate pool only. Selection-only: never writes relatedWordIds to
production, never touches the candidate pool or any production file.

METHODOLOGY: every P5.4.1 candidate carries one of 9 rule categories.
This script maps those categories onto the P5.4.2 A/B/C quality
hierarchy, then applies additional, individually-reasoned scrutiny to
every C-tier (FUNCTIONAL_CONTEXT) candidate -- the tier the phase
brief explicitly says to "use sparingly" and never promote merely
because the candidate pool retained it.

Tier mapping (A > B > C):
    A: ANTONYM, NEAR_SYNONYM, MORPHOLOGICAL_SUFFIX,
       COMPOSITIONAL_COMPOUND, CLOSED_PARADIGM, GENDER_PAIR, CONTRAST
       -- these are either direct word-formation, canonical closed
       grammatical paradigms, or well-established antonym/near-synonym
       pairs; already high-precision by construction in P5.4.1.
    B: COMPOUND_FAMILY -- shares a productive root but is not itself a
       direct derivation of the specific paired word; solid lexical
       family relation, one notch below A.
    C: FUNCTIONAL_CONTEXT -- collocational/discourse/real-world-script
       relationships. Every one of the 20 unordered C-tier pairs from
       P5.4.1 was individually re-reviewed against the stricter final-
       selection bar ("strong, useful, recurring, not merely same
       topic"); FUNCTIONAL_CONTEXT_ACCEPT below is the explicit result
       of that review -- 13 pairs kept, 7 pairs rejected. See the
       P5.4.2 report for the reasoning behind each.

Rejected specifically because closer scrutiny showed them to be topical
co-membership rather than a genuine recurring lexical relationship (not
because P5.4.1 was "wrong" to retain them as candidates -- a candidate
pool is deliberately broader than a final selection):
    mao1/gou3 (cat/dog -- only two animal nouns in HSK1, no
        derivational/collocational link)
    yi3zi/zhuo1zi (chair/table -- furniture co-occurrence, no
        derivational/collocational link)
    xue3/yu3, xue3/tian1qi4, yu3/tian1qi4 (weather-phenomenon topic
        co-membership, not a fixed collocation)
    zao3fan4/zao3shang4, wan3fan4/wan3shang4 (near-tautological
        "meal is eaten at that time of day" -- no added lexical value
        beyond what the words' own glosses already say)

Special per-record override: hsk1_248 (xue2sheng1) had 6 candidates in
the pool (3x COMPOUND_FAMILY, 1x COMPOSITIONAL_COMPOUND, 1x
NEAR_SYNONYM, 1x FUNCTIONAL_CONTEXT). Per the "do not exceed 5 without
a compelling reason" rule, the weakest (single C-tier: xue2xiao4) is
dropped from xue2sheng1's own selection specifically, keeping the 5
strongest (A/B tier). This is NOT applied symmetrically: from
xue2xiao4's own side, xue2sheng1 remains selected, because it is one of
only two candidates xue2xiao4 has at all and is independently
defensible on xue2xiao4's terms. Per-source asymmetric selection is a
deliberate, documented choice -- see the P5.4.2 report.

status policy: "needs_review" if and only if the record's final
selected set contains at least one C-tier (FUNCTIONAL_CONTEXT)
relationship (the one tier this phase treats as requiring human
confirmation); otherwise "selected" -- including confidently-empty
records (0 candidates existed, or all candidates were confidently
rejected) which are "selected" with selectedCount 0, not needs_review,
because there was no residual ambiguity in reaching that empty result.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HSK1_PATH = REPO_ROOT / "data" / "hsk" / "hsk1" / "hsk1_vocabulary_production.json"
POOL_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_candidate_pool.json"
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_selection.json"

SELECTION_VERSION = "p542-v1"
RULES_VERSION = "hsk1-selection-rules-v1"
MAX_SELECTED_PER_RECORD = 5

CATEGORY_TIER = {
    "ANTONYM": "A",
    "NEAR_SYNONYM": "A",
    "MORPHOLOGICAL_SUFFIX": "A",
    "COMPOSITIONAL_COMPOUND": "A",
    "CLOSED_PARADIGM": "A",
    "GENDER_PAIR": "A",
    "CONTRAST": "A",
    "COMPOUND_FAMILY": "B",
    "FUNCTIONAL_CONTEXT": "C",
}

# The 13 FUNCTIONAL_CONTEXT (C-tier) unordered pairs that survive the
# stricter final-selection review. Every other FUNCTIONAL_CONTEXT pair
# in the candidate pool is rejected. Order-independent (frozenset pairs).
FUNCTIONAL_CONTEXT_ACCEPT = {
    frozenset({"hsk1_035", "hsk1_189"}),  # dian4hua4 / shou3ji1
    frozenset({"hsk1_290", "hsk1_070"}),  # zhong1wen2 / han4zi4
    frozenset({"hsk1_250", "hsk1_248"}),  # xue2xiao4 / xue2sheng1
    frozenset({"hsk1_256", "hsk1_100"}),  # yi1sheng1 / kan4bing4
    frozenset({"hsk1_257", "hsk1_100"}),  # yi1yuan4 / kan4bing4
    frozenset({"hsk1_063", "hsk1_176"}),  # gong1zuo4 / shang4ban1
    frozenset({"hsk1_063", "hsk1_228"}),  # gong1zuo4 / xia4ban1
    frozenset({"hsk1_241", "hsk1_014"}),  # xie4xie / bu2ke4qi
    frozenset({"hsk1_045", "hsk1_120"}),  # dui4buqi3 / mei2guan1xi
    frozenset({"hsk1_147", "hsk1_272"}),  # ni3hao3 / zai4jian4
    frozenset({"hsk1_058", "hsk1_018"}),  # ge1 / chang4
    frozenset({"hsk1_023", "hsk1_255"}),  # chuan1 / yi1fu
    frozenset({"hsk1_240", "hsk1_296"}),  # xie3 / zi4
}

# Explicitly rejected C-tier pairs (kept here, not silently omitted, so
# the rejection is auditable against the P5.4.1 candidate pool).
FUNCTIONAL_CONTEXT_REJECT = {
    frozenset({"hsk1_119", "hsk1_064"}): "mao1/gou3: only-two-animal-nouns co-membership, no derivational/collocational link -- topical, not lexical",
    frozenset({"hsk1_260", "hsk1_295"}): "yi3zi/zhuo1zi: furniture co-occurrence, no derivational/collocational link -- topical, not lexical",
    frozenset({"hsk1_251", "hsk1_267"}): "xue3/yu3: precipitation-type topic co-membership, not a fixed collocation",
    frozenset({"hsk1_251", "hsk1_208"}): "xue3/tian1qi4: weather-phenomenon-under-hypernym topic relation, not a fixed collocation",
    frozenset({"hsk1_267", "hsk1_208"}): "yu3/tian1qi4: weather-phenomenon-under-hypernym topic relation, not a fixed collocation",
    frozenset({"hsk1_274", "hsk1_275"}): "zao3fan4/zao3shang4: near-tautological 'meal eaten at that time', no added lexical value",
    frozenset({"hsk1_216", "hsk1_217"}): "wan3fan4/wan3shang4: near-tautological 'meal eaten at that time', no added lexical value",
}

# Per-record override: (source_id, dropped_candidate_id) pairs excluded
# from that ONE record's own selection despite being accepted candidates
# in general, applied for count-management / relative-strength reasons
# specific to that record. See hsk1_248 special case in the module
# docstring. This is intentionally asymmetric (does not remove the
# relationship from the other side's own record).
PER_RECORD_DROP = {
    ("hsk1_248", "hsk1_250"),  # xue2sheng1: drop xue2xiao4 (weakest of 6, count-management)
}


def load_json_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def classify(source_id: str, candidate_id: str, category: str) -> tuple[bool, str]:
    """Returns (accepted, tier). tier is always the category's natural
    tier even when rejected, for audit purposes."""
    tier = CATEGORY_TIER.get(category)
    if tier is None:
        fail(f"unknown category '{category}' for {source_id}->{candidate_id}")
    if category != "FUNCTIONAL_CONTEXT":
        return True, tier
    pair = frozenset({source_id, candidate_id})
    if pair in FUNCTIONAL_CONTEXT_ACCEPT:
        return True, tier
    if pair in FUNCTIONAL_CONTEXT_REJECT:
        return False, tier
    # A FUNCTIONAL_CONTEXT pair not present in either explicit list is a
    # script-authoring gap, not something to silently accept or reject.
    fail(f"FUNCTIONAL_CONTEXT pair {sorted(pair)} not classified in either accept or reject list")


def main() -> None:
    if OUTPUT_PATH.exists():
        fail(f"{OUTPUT_PATH} already exists -- refusing to overwrite an existing selection artifact.")

    hsk1_text = load_json_text(HSK1_PATH)
    hsk1_records = json.loads(hsk1_text)
    if len(hsk1_records) != 300:
        fail(f"HSK1 production record count {len(hsk1_records)} != expected 300")
    hsk1_ids = {r["id"] for r in hsk1_records}

    pool_text = load_json_text(POOL_PATH)
    pool = json.loads(pool_text)
    pool_records = {r["sourceId"]: r for r in pool["records"]}

    if set(pool_records.keys()) != hsk1_ids:
        fail("candidate pool source IDs do not exactly match HSK1 production IDs")

    all_pool_candidate_ids = set()
    for r in pool_records.values():
        for c in r["candidates"]:
            all_pool_candidate_ids.add(c["wordId"])

    output_records = []
    stats_rejected_functional = 0
    stats_accepted_functional = 0

    for source_id in sorted(hsk1_ids, key=lambda i: pool_records[i]["sourceId"]):
        pass  # placeholder to keep deterministic iteration below

    # Deterministic iteration order: same as the HSK1 production file order.
    for hsk1_r in hsk1_records:
        source_id = hsk1_r["id"]
        pool_r = pool_records[source_id]

        selected = []
        reasons = []
        for c in pool_r["candidates"]:
            cand_id = c["wordId"]
            category = c["category"]

            if (source_id, cand_id) in PER_RECORD_DROP:
                continue

            accepted, tier = classify(source_id, cand_id, category)
            if category == "FUNCTIONAL_CONTEXT":
                if accepted:
                    stats_accepted_functional += 1
                else:
                    stats_rejected_functional += 1
            if not accepted:
                continue

            selected.append((cand_id, tier, c["word"], category))

        # Deterministic ordering: tier (A,B,C) then wordId.
        tier_order = {"A": 0, "B": 1, "C": 2}
        selected.sort(key=lambda t: (tier_order[t[1]], t[0]))

        if len(selected) > MAX_SELECTED_PER_RECORD:
            fail(
                f"{source_id} has {len(selected)} selected relationships after tiering, "
                f"exceeds max {MAX_SELECTED_PER_RECORD} -- needs an explicit PER_RECORD_DROP entry"
            )

        selected_ids = [s[0] for s in selected]
        status = "needs_review" if any(s[1] == "C" for s in selected) else "selected"

        selection_reasons = [
            {
                "relatedWordId": cand_id,
                "category": tier,
                "reason": f"P5.4.1 category {orig_category} ({word}); tier {tier} per P5.4.2 hierarchy.",
            }
            for cand_id, tier, word, orig_category in selected
        ]

        output_records.append(
            {
                "sourceId": source_id,
                "selectedRelatedWordIds": selected_ids,
                "status": status,
                "selectedCount": len(selected_ids),
                "selectionReasons": selection_reasons,
            }
        )

    generated_at = datetime.now(timezone.utc).isoformat()

    artifact = {
        "selectionVersion": SELECTION_VERSION,
        "candidatePoolPath": "tools/hsk/hsk1_related_words_candidate_pool.json",
        "candidatePoolVersion": pool.get("poolVersion"),
        "candidatePoolHash": sha256_of(pool_text),
        "sourceDatasetHash": sha256_of(hsk1_text),
        "rulesVersion": RULES_VERSION,
        "tierPolicy": {
            "A": "Strong semantic relation (synonym/near-synonym, antonym, direct lexical family, strong derivation, established compound family) -- auto-accepted from P5.4.1 categories ANTONYM, NEAR_SYNONYM, MORPHOLOGICAL_SUFFIX, COMPOSITIONAL_COMPOUND, CLOSED_PARADIGM, GENDER_PAIR, CONTRAST.",
            "B": "Strong collocation / lexical relation -- auto-accepted from P5.4.1 category COMPOUND_FAMILY.",
            "C": "Contextual/functional relation, used sparingly -- from P5.4.1 category FUNCTIONAL_CONTEXT; each of the 20 unordered candidate pairs individually re-reviewed, 13 accepted / 7 explicitly rejected (see FUNCTIONAL_CONTEXT_REJECT in this script).",
        },
        "statusPolicy": "needs_review iff the final selected set contains >=1 C-tier relationship; otherwise selected (including confidently-empty 0-selection records).",
        "maxSelectedPerRecord": MAX_SELECTED_PER_RECORD,
        "generatedAt": generated_at,
        "generatorScript": "tools/hsk/select_hsk1_related_words_p542.py",
        "recordCount": len(output_records),
        "records": output_records,
    }

    OUTPUT_PATH.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    total_selected = sum(r["selectedCount"] for r in output_records)
    dist = {}
    for r in output_records:
        dist[r["selectedCount"]] = dist.get(r["selectedCount"], 0) + 1
    selected_status = sum(1 for r in output_records if r["status"] == "selected")
    needs_review_status = sum(1 for r in output_records if r["status"] == "needs_review")

    print(f"Wrote {OUTPUT_PATH}")
    print(f"records: {len(output_records)}  total selected relationships: {total_selected}")
    print(f"distribution by count: {dict(sorted(dist.items()))}")
    print(f"status: selected={selected_status} needs_review={needs_review_status}")
    print(f"FUNCTIONAL_CONTEXT accepted edges: {stats_accepted_functional}  rejected edges: {stats_rejected_functional}")


if __name__ == "__main__":
    main()
