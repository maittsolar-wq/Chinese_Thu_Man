"""P5.4.3 -- HSK1 Related-Word Semantic QA + Refinement.

Takes the P5.4.2 selection artifact as IMMUTABLE input and produces a
refined artifact. Never modifies the P5.4.1 candidate pool, the P5.4.2
selection, or any production file.

METHODOLOGY: this phase re-reviews every C-tier (FUNCTIONAL_CONTEXT)
relationship that survived P5.4.2's own review, under a stricter bar
(Step 7 of the P5.4.3 brief): "strongly recurring in ordinary Chinese,
lexically meaningful, useful for a learner, specific rather than
broad-topic, not replaceable by a stronger A/B relationship, not merely
'these words often appear in the same situation'." A/B-tier
relationships are not re-litigated here -- they were already the
strongest categories in P5.4.1/P5.4.2 and nothing in this deeper pass
found reason to remove any of them.

REMOVE decisions (both directions removed symmetrically -- these are
genuine relationship-level rejections, not asymmetric edits):

  gong1zuo4 <-> shang4ban1 (hsk1_063 <-> hsk1_176)
  gong1zuo4 <-> xia4ban1   (hsk1_063 <-> hsk1_228)
      On deeper review: 工作 is a general/abstract activity noun,
      上班/下班 are specific temporal-boundary verbs for starting/ending
      it. Unlike the surviving VO-collocation pairs (chuan1/yi1fu,
      chang4/ge1, xie3/zi4 -- which are fixed two-word phrases a
      learner would say verbatim), "工作上班" is not itself a
      collocation; the relationship is closer to topical/entailment
      than a tight recurring lexical pairing. Does not clear the
      stricter bar's "not merely same situation" test.

  ni3hao3 <-> zai4jian4 (hsk1_147 <-> hsk1_272)
      Explicitly flagged in the P5.4.2 report as the weakest of the
      three adjacency-style C-tier pairs, and explicitly NOT to be
      preserved automatically here. Unlike xie4xie/bu2ke4qi and
      dui4buqi3/mei2guan1xi (genuine question-response adjacency
      pairs -- one utterance directly prompts the other), ni3hao3 and
      zai4jian4 do not co-occur in the same exchange; they are both
      "greeting-category" words used at opposite ends of an
      interaction, which is closer to topical category membership than
      a recurring lexical pair. Removed.

status refinement: P5.4.2 mechanically flagged every record containing
ANY C-tier relationship as needs_review. This phase applies the
judgment Step 11 explicitly calls for: the tightest, most canonical
C-tier survivors -- true fixed adjacency-response pairs and canonical
verb-object collocations -- are, after this second full review, judged
fully safe and promoted to status=selected even though the relationship
itself is still recorded as tier C. The remaining C-tier survivors
(device-category, institution-role, medical-frame, script-language
relationships) retain genuine interpretive texture and keep
needs_review.

CONFIDENT_C_TIER (promoted to selected):
    xie4xie <-> bu2ke4qi           (fixed response-adjacency pair)
    dui4buqi3 <-> mei2guan1xi      (fixed response-adjacency pair)
    chang4 <-> ge1                 (canonical VO collocation: chang4ge1)
    chuan1 <-> yi1fu               (canonical VO collocation: chuan1 yi1fu)
    xie3 <-> zi4                   (canonical VO collocation: xie3zi4)

Still needs_review (genuine residual judgment call, kept but flagged):
    dian4hua4 <-> shou3ji1         (device-category relationship)
    xue2xiao4 <-> xue2sheng1       (institution/role -- asymmetric, see below)
    yi1sheng1 <-> kan4bing4        (medical-frame relationship)
    yi1yuan4 <-> kan4bing4         (medical-frame relationship)
    han4zi4 <-> zhong1wen2         (script/language relationship)

The xue2xiao4 -> xue2sheng1 relationship remains deliberately
asymmetric, unchanged from P5.4.2: xue2sheng1's own record does not
list xue2xiao4 (dropped there for count-management among 6 candidates,
see P5.4.2), but xue2xiao4's own record legitimately keeps xue2sheng1
as one of only two candidates it has. This asymmetry is intentional,
not a curation mistake -- see the P5.4.3 report's bidirectional
consistency review.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HSK1_PATH = REPO_ROOT / "data" / "hsk" / "hsk1" / "hsk1_vocabulary_production.json"
POOL_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_candidate_pool.json"
SELECTION_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_selection.json"
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_refined_selection.json"
REPORT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_refinement_report.json"

REFINEMENT_VERSION = "p543-v1"
RULES_VERSION = "hsk1-refinement-rules-v1"
MAX_SELECTED_PER_RECORD = 5

# Directed (source, target) pairs to remove from the P5.4.2 selection.
# Written out symmetrically where the underlying relationship judgment
# is symmetric (all three of these are).
REMOVE_EDGES = {
    ("hsk1_063", "hsk1_176"), ("hsk1_176", "hsk1_063"),  # gong1zuo4 <-> shang4ban1
    ("hsk1_063", "hsk1_228"), ("hsk1_228", "hsk1_063"),  # gong1zuo4 <-> xia4ban1
    ("hsk1_147", "hsk1_272"), ("hsk1_272", "hsk1_147"),  # ni3hao3 <-> zai4jian4
}

REMOVE_REASONS = {
    frozenset({"hsk1_063", "hsk1_176"}): "工作/上班: topical/entailment relationship (上班 marks the start of 工作) rather than a tight recurring lexical pairing; not a fixed collocation the way the surviving VO pairs are. Fails the stricter 'not merely same situation' bar.",
    frozenset({"hsk1_063", "hsk1_228"}): "工作/下班: same reasoning as 工作/上班 (topical/entailment, not a fixed collocation).",
    frozenset({"hsk1_147", "hsk1_272"}): "你好/再见: both greeting-category words but not a direct response-adjacency pair (unlike 谢谢/不客气, 对不起/没关系) -- they don't co-occur in the same exchange. Closer to topical category membership than a recurring lexical pair. Explicitly flagged as the weakest of the three adjacency-style pairs and not preserved.",
}

# Relationships that remain C-tier in the artifact but, after this
# deeper review, are judged fully safe and promoted to status=selected
# rather than needs_review.
CONFIDENT_C_TIER = {
    frozenset({"hsk1_241", "hsk1_014"}),  # xie4xie / bu2ke4qi
    frozenset({"hsk1_045", "hsk1_120"}),  # dui4buqi3 / mei2guan1xi
    frozenset({"hsk1_058", "hsk1_018"}),  # ge1 / chang4
    frozenset({"hsk1_023", "hsk1_255"}),  # chuan1 / yi1fu
    frozenset({"hsk1_240", "hsk1_296"}),  # xie3 / zi4
}


def load_json_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    if OUTPUT_PATH.exists():
        fail(f"{OUTPUT_PATH} already exists -- refusing to overwrite an existing refined artifact.")
    if REPORT_PATH.exists():
        fail(f"{REPORT_PATH} already exists -- refusing to overwrite an existing refinement report.")

    hsk1_text = load_json_text(HSK1_PATH)
    hsk1_records = json.loads(hsk1_text)
    if len(hsk1_records) != 300:
        fail(f"HSK1 production record count {len(hsk1_records)} != expected 300")
    hsk1_ids = {r["id"] for r in hsk1_records}

    pool_text = load_json_text(POOL_PATH)
    pool = json.loads(pool_text)
    pool_candidate_ids = {r["sourceId"]: {c["wordId"] for c in r["candidates"]} for r in pool["records"]}

    selection_text = load_json_text(SELECTION_PATH)
    selection = json.loads(selection_text)
    selection_records = {r["sourceId"]: r for r in selection["records"]}

    if set(selection_records.keys()) != hsk1_ids:
        fail("P5.4.2 selection source IDs do not exactly match HSK1 production IDs")

    # Validate every REMOVE edge actually exists in the P5.4.2 selection
    # before applying it -- fail closed if the input has drifted from
    # what this script assumes.
    removed_log = []
    for src_id, tgt_id in sorted(REMOVE_EDGES):
        sel_ids = set(selection_records[src_id]["selectedRelatedWordIds"])
        if tgt_id not in sel_ids:
            fail(f"expected to remove {src_id}->{tgt_id} but it is not present in the P5.4.2 selection")

    output_records = []
    status_before = {"selected": 0, "needs_review": 0}
    status_after = {"selected": 0, "needs_review": 0}

    for hsk1_r in hsk1_records:
        source_id = hsk1_r["id"]
        sel_r = selection_records[source_id]
        status_before[sel_r["status"]] += 1

        kept_reasons = []
        for reason in sel_r["selectionReasons"]:
            tgt_id = reason["relatedWordId"]
            pair_key = frozenset({source_id, tgt_id})

            if (source_id, tgt_id) in REMOVE_EDGES:
                removed_log.append(
                    {
                        "sourceId": source_id,
                        "sourceWord": hsk1_r["word"],
                        "relatedWordId": tgt_id,
                        "relatedWord": next(
                            (h["word"] for h in hsk1_records if h["id"] == tgt_id), "?"
                        ),
                        "originalCategory": reason["category"],
                        "reasonForRemoval": REMOVE_REASONS.get(pair_key, "removed"),
                    }
                )
                continue

            kept_reasons.append(reason)

        # Fail-closed integrity: every kept id must still resolve inside
        # both the P5.4.2 selection (trivially true, it came from there)
        # and the P5.4.1 candidate pool.
        for reason in kept_reasons:
            if reason["relatedWordId"] not in pool_candidate_ids.get(source_id, set()):
                fail(
                    f"{source_id}: kept relatedWordId {reason['relatedWordId']} is not in the "
                    "P5.4.1 candidate pool for this source -- integrity violation"
                )

        if len(kept_reasons) > MAX_SELECTED_PER_RECORD:
            fail(f"{source_id} has {len(kept_reasons)} relationships after refinement, exceeds max {MAX_SELECTED_PER_RECORD}")

        # Status recomputation: needs_review iff a retained C-tier
        # relationship is NOT in CONFIDENT_C_TIER.
        has_uncertain_c = any(
            r["category"] == "C" and frozenset({source_id, r["relatedWordId"]}) not in CONFIDENT_C_TIER
            for r in kept_reasons
        )
        new_status = "needs_review" if has_uncertain_c else "selected"
        status_after[new_status] += 1

        output_records.append(
            {
                "sourceId": source_id,
                "selectedRelatedWordIds": [r["relatedWordId"] for r in kept_reasons],
                "status": new_status,
                "selectedCount": len(kept_reasons),
                "selectionReasons": kept_reasons,
            }
        )

    generated_at = datetime.now(timezone.utc).isoformat()

    refined_artifact = {
        "refinementVersion": REFINEMENT_VERSION,
        "selectionArtifact": "tools/hsk/hsk1_related_words_selection.json",
        "selectionArtifactHash": sha256_of(selection_text),
        "candidatePoolVersion": pool.get("poolVersion"),
        "candidatePoolHash": sha256_of(pool_text),
        "sourceDatasetHash": sha256_of(hsk1_text),
        "rulesVersion": RULES_VERSION,
        "maxSelectedPerRecord": MAX_SELECTED_PER_RECORD,
        "generatedAt": generated_at,
        "generatorScript": "tools/hsk/refine_hsk1_related_words_p543.py",
        "recordCount": len(output_records),
        "records": output_records,
    }
    output_text = json.dumps(refined_artifact, indent=2, ensure_ascii=False) + "\n"
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(output_text)
    # Re-read with newline="" (no translation) so the hash used below is
    # computed from the exact bytes that end up on disk -- matching how
    # every validator in this pipeline (and every other hash in this
    # project) reads files. Writing text on Windows would otherwise
    # translate "\n" -> "\r\n" while a naive read_text() would translate
    # it back, silently hashing a different string than what's on disk.
    output_text = load_json_text(OUTPUT_PATH)

    total_in = sum(r["selectedCount"] for r in selection["records"])
    total_out = sum(r["selectedCount"] for r in output_records)

    removal_by_category = {}
    for item in removed_log:
        removal_by_category[item["originalCategory"]] = removal_by_category.get(item["originalCategory"], 0) + 1

    report = {
        "reportLabel": "P5.4.3 HSK1 RELATED-WORD REFINEMENT REPORT",
        "refinementVersion": REFINEMENT_VERSION,
        "rulesVersion": RULES_VERSION,
        "generatedAt": generated_at,
        "inputSelectionArtifactHash": sha256_of(selection_text),
        "outputRefinedArtifactHash": sha256_of(output_text),
        "totalInputRelationships": total_in,
        "totalOutputRelationships": total_out,
        "numberKept": total_out,
        "numberRemoved": total_in - total_out,
        "removalReasonsByCategory": removal_by_category,
        "removedRelationships": removed_log,
        "needsReviewBefore": status_before["needs_review"],
        "needsReviewAfter": status_after["needs_review"],
        "statusDistributionBefore": status_before,
        "statusDistributionAfter": status_after,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote {OUTPUT_PATH}")
    print(f"Wrote {REPORT_PATH}")
    print(f"input relationships: {total_in}  output relationships: {total_out}  removed: {total_in - total_out}")
    print(f"status before: {status_before}  status after: {status_after}")


if __name__ == "__main__":
    main()
