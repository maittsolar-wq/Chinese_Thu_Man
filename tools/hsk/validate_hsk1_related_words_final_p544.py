"""P5.4.4 -- Final cross-stage validation gate for the HSK1 related-word
pipeline (candidate pool -> selection -> refinement). Read-only: never
writes to any P5.4.1/P5.4.2/P5.4.3 artifact or any production file.
Writes exactly one new file: tools/hsk/hsk1_related_words_final_validation_p544.json.

This does not re-implement the three per-stage validators (P5.4.1-3
already have their own, all confirmed passing separately) -- it
verifies the things only visible when looking across all four stages
at once: candidate->selection->refinement subset integrity, count
reconciliation, status reconciliation, the documented special cases,
the documented C-tier decisions, and the full source/target/production
universe hash chain.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HSK1_PATH = REPO_ROOT / "data" / "hsk" / "hsk1" / "hsk1_vocabulary_production.json"
POOL_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_candidate_pool.json"
SELECTION_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_selection.json"
REFINED_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_refined_selection.json"
REFINEMENT_REPORT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_refinement_report.json"
REPORT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_final_validation_p544.json"

VALIDATION_VERSION = "p544-v1"

PROD_PATHS = {
    lvl: REPO_ROOT / "data" / "hsk" / f"hsk{lvl}" / f"hsk{lvl}_vocabulary_production.json"
    for lvl in (1, 2, 3, 4, 5, 6)
}


def load_json_text(path: Path) -> str:
    # newline="" -- raw bytes, no translation. This is the ONLY correct
    # way to hash these files consistently with how they were written
    # and with how `sha256sum` / `git hash-object` see them; a naive
    # text-mode read on Windows silently normalizes CRLF -> LF and
    # produces a different hash than the file's actual on-disk bytes
    # (this exact class of bug was found and fixed in P5.4.3 §12).
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    if REPORT_PATH.exists():
        raise SystemExit(f"FAIL: {REPORT_PATH} already exists -- refusing to overwrite.")

    checks: dict[str, dict] = {}
    all_passed = True

    def record(name: str, passed: bool, detail: str) -> None:
        nonlocal all_passed
        checks[name] = {"passed": passed, "detail": detail}
        if not passed:
            all_passed = False

    hsk1_text = load_json_text(HSK1_PATH)
    hsk1_records = json.loads(hsk1_text)
    hsk1_ids = {r["id"] for r in hsk1_records}
    hsk1_word_by_id = {r["id"]: r["word"] for r in hsk1_records}
    hsk1_related_before = {r["id"]: r.get("relatedWordIds") for r in hsk1_records}

    pool_text = load_json_text(POOL_PATH)
    pool = json.loads(pool_text)
    pool_candidates = {r["sourceId"]: {c["wordId"] for c in r["candidates"]} for r in pool["records"]}

    selection_text = load_json_text(SELECTION_PATH)
    selection = json.loads(selection_text)
    selection_ids = {r["sourceId"]: set(r["selectedRelatedWordIds"]) for r in selection["records"]}

    refined_text = load_json_text(REFINED_PATH)
    refined = json.loads(refined_text)
    refined_records = {r["sourceId"]: r for r in refined["records"]}

    refinement_report_text = load_json_text(REFINEMENT_REPORT_PATH)
    refinement_report = json.loads(refinement_report_text)

    # Full HSK1-6 production universe.
    universe_ids = set()
    for p in PROD_PATHS.values():
        for r in json.loads(load_json_text(p)):
            universe_ids.add(r["id"])

    # ---- Step 5: cross-stage integrity A-H ----

    # A. Every P5.4.2 selected relationship exists in P5.4.1 candidate pool.
    a_violations = []
    for src, targets in selection_ids.items():
        allowed = pool_candidates.get(src, set())
        for t in targets:
            if t not in allowed:
                a_violations.append((src, t))
    record("A_selection_subset_of_pool", len(a_violations) == 0, f"violations: {a_violations[:10]}")

    # B. Every P5.4.3 retained relationship exists in P5.4.2.
    b_violations = []
    for src, r in refined_records.items():
        allowed = selection_ids.get(src, set())
        for t in r["selectedRelatedWordIds"]:
            if t not in allowed:
                b_violations.append((src, t))
    record("B_refinement_subset_of_selection", len(b_violations) == 0, f"violations: {b_violations[:10]}")

    # C. No P5.4.3 relationship was invented (i.e. also present in candidate pool, transitively covered by A+B, checked directly too).
    c_violations = []
    for src, r in refined_records.items():
        allowed = pool_candidates.get(src, set())
        for t in r["selectedRelatedWordIds"]:
            if t not in allowed:
                c_violations.append((src, t))
    record("C_refinement_subset_of_pool", len(c_violations) == 0, f"violations: {c_violations[:10]}")

    # D. Every sourceId exists in HSK1 production.
    d_violations = sorted(set(refined_records.keys()) - hsk1_ids)
    record("D_source_ids_in_hsk1", len(d_violations) == 0, f"unknown source ids: {d_violations[:10]}")

    # E. Every target ID resolves to a real vocabulary item.
    e_violations = []
    for src, r in refined_records.items():
        for t in r["selectedRelatedWordIds"]:
            if t not in universe_ids:
                e_violations.append((src, t))
    record("E_targets_resolve_to_real_items", len(e_violations) == 0, f"unresolved: {e_violations[:10]}")

    # F. No source references itself.
    f_violations = [src for src, r in refined_records.items() if src in r["selectedRelatedWordIds"]]
    record("F_no_self_references", len(f_violations) == 0, f"self-refs: {f_violations[:10]}")

    # G. No duplicate target per source.
    g_violations = []
    for src, r in refined_records.items():
        ids = r["selectedRelatedWordIds"]
        if len(ids) != len(set(ids)):
            g_violations.append(src)
    record("G_no_duplicate_targets", len(g_violations) == 0, f"dupes: {g_violations[:10]}")

    # H. No relationship points outside HSK1-6 production universe (same as E, phrased per brief).
    record("H_no_relationship_outside_universe", len(e_violations) == 0, f"outside universe: {e_violations[:10]}")

    # ---- Step 6: count reconciliation ----
    pool_total = sum(r["candidateCount"] for r in pool["records"])
    selection_total = sum(r["selectedCount"] for r in selection["records"])
    refined_total = sum(r["selectedCount"] for r in refined["records"])

    record("count_pool_408", pool_total == 408, f"actual={pool_total}")
    record("count_selection_393", selection_total == 393, f"actual={selection_total}")
    record("count_refined_387", refined_total == 387, f"actual={refined_total}")
    record("count_p542_removed_15", (pool_total - selection_total) == 15,
           f"actual={pool_total - selection_total}")
    record("count_p543_removed_6", (selection_total - refined_total) == 6,
           f"actual={selection_total - refined_total}")
    record("count_total_removed_21", (pool_total - refined_total) == 21,
           f"actual={pool_total - refined_total}")

    # Verify P5.4.3's own removal log accounts for exactly the P5.4.2->P5.4.3 delta.
    removed_log_count = len(refinement_report.get("removedRelationships", []))
    record("p543_removal_log_matches_delta", removed_log_count == (selection_total - refined_total),
           f"log={removed_log_count} delta={selection_total - refined_total}")

    # ---- Step 7: status reconciliation ----
    selected_count = sum(1 for r in refined["records"] if r["status"] == "selected")
    nr_count = sum(1 for r in refined["records"] if r["status"] == "needs_review")
    record("status_selected_292", selected_count == 292, f"actual={selected_count}")
    record("status_needs_review_8", nr_count == 8, f"actual={nr_count}")
    record("status_sums_to_300", (selected_count + nr_count) == 300,
           f"actual={selected_count + nr_count}")

    # ---- Step 8: special case revalidation ----
    def sel_ids(src):
        return refined_records[src]["selectedRelatedWordIds"]

    special = {}
    special["hsk1_248_xuesheng"] = {
        "selected": sel_ids("hsk1_248"),
        "excludes_xuexiao_hsk1_250": "hsk1_250" not in sel_ids("hsk1_248"),
    }
    special["hsk1_026_dajia"] = {"selected": sel_ids("hsk1_026"), "empty": sel_ids("hsk1_026") == []}
    special["hsk1_181_shei"] = {"selected": sel_ids("hsk1_181"), "empty": sel_ids("hsk1_181") == []}
    special["hsk1_182_shenme"] = {"selected": sel_ids("hsk1_182"), "empty": sel_ids("hsk1_182") == []}
    special["hsk1_049_er_liang"] = {
        "selected": sel_ids("hsk1_049"),
        "retains_hsk1_111": "hsk1_111" in sel_ids("hsk1_049"),
    }
    special["hsk1_119_mao_hsk1_064_gou"] = {
        "hsk1_119_selected": sel_ids("hsk1_119"),
        "hsk1_064_selected": sel_ids("hsk1_064"),
        "both_rejected": sel_ids("hsk1_119") == [] and sel_ids("hsk1_064") == [],
    }
    special["hsk1_260_yizi_hsk1_295_zhuozi"] = {
        "hsk1_260_selected": sel_ids("hsk1_260"),
        "hsk1_295_selected": sel_ids("hsk1_295"),
        "both_rejected": sel_ids("hsk1_260") == [] and sel_ids("hsk1_295") == [],
    }

    record("special_xuesheng_correct",
           special["hsk1_248_xuesheng"]["excludes_xuexiao_hsk1_250"] and len(special["hsk1_248_xuesheng"]["selected"]) == 5,
           json.dumps(special["hsk1_248_xuesheng"], ensure_ascii=False))
    record("special_dajia_empty", special["hsk1_026_dajia"]["empty"], json.dumps(special["hsk1_026_dajia"], ensure_ascii=False))
    record("special_shei_empty", special["hsk1_181_shei"]["empty"], json.dumps(special["hsk1_181_shei"], ensure_ascii=False))
    record("special_shenme_empty", special["hsk1_182_shenme"]["empty"], json.dumps(special["hsk1_182_shenme"], ensure_ascii=False))
    record("special_er_liang_retained", special["hsk1_049_er_liang"]["retains_hsk1_111"], json.dumps(special["hsk1_049_er_liang"], ensure_ascii=False))
    record("special_mao_gou_rejected", special["hsk1_119_mao_hsk1_064_gou"]["both_rejected"], json.dumps(special["hsk1_119_mao_hsk1_064_gou"], ensure_ascii=False))
    record("special_yizi_zhuozi_rejected", special["hsk1_260_yizi_hsk1_295_zhuozi"]["both_rejected"], json.dumps(special["hsk1_260_yizi_hsk1_295_zhuozi"], ensure_ascii=False))

    # ---- Step 9: C-tier revalidation ----
    c_tier_checks = {
        "gongzuo_shangban": ("hsk1_063", "hsk1_176", "removed"),
        "gongzuo_xiaban": ("hsk1_063", "hsk1_228", "removed"),
        "xiexie_bukeqi": ("hsk1_241", "hsk1_014", "kept_selected"),
        "duibuqi_meiguanxi": ("hsk1_045", "hsk1_120", "kept_selected"),
        "nihao_zaijian": ("hsk1_147", "hsk1_272", "removed"),
    }
    c_tier_results = {}
    for name, (src, tgt, expected) in c_tier_checks.items():
        present = tgt in sel_ids(src)
        if expected == "removed":
            ok = not present
            state = "removed" if not present else "still present (FAIL)"
        else:
            status = refined_records[src]["status"]
            ok = present and status == "selected"
            state = f"present, status={status}"
        c_tier_results[name] = {"expected": expected, "state": state, "matches": ok}
        record(f"ctier_{name}", ok, json.dumps(c_tier_results[name], ensure_ascii=False))

    # ---- Step 10/11: provenance chain + hash integrity (raw-byte) ----
    actual_pool_hash = sha256_of(pool_text)
    actual_selection_hash = sha256_of(selection_text)
    actual_refined_hash = sha256_of(refined_text)
    actual_source_hash = sha256_of(hsk1_text)

    record("hash_source_recorded_in_selection", selection.get("sourceDatasetHash") == actual_source_hash,
           f"recorded={selection.get('sourceDatasetHash')} actual={actual_source_hash}")
    record("hash_pool_recorded_in_selection", selection.get("candidatePoolHash") == actual_pool_hash,
           f"recorded={selection.get('candidatePoolHash')} actual={actual_pool_hash}")
    record("hash_source_recorded_in_refined", refined.get("sourceDatasetHash") == actual_source_hash,
           f"recorded={refined.get('sourceDatasetHash')} actual={actual_source_hash}")
    record("hash_pool_recorded_in_refined", refined.get("candidatePoolHash") == actual_pool_hash,
           f"recorded={refined.get('candidatePoolHash')} actual={actual_pool_hash}")
    record("hash_selection_recorded_in_refined", refined.get("selectionArtifactHash") == actual_selection_hash,
           f"recorded={refined.get('selectionArtifactHash')} actual={actual_selection_hash}")
    record("hash_refined_recorded_in_refinement_report",
           refinement_report.get("outputRefinedArtifactHash") == actual_refined_hash,
           f"recorded={refinement_report.get('outputRefinedArtifactHash')} actual={actual_refined_hash}")
    record("hash_selection_recorded_in_refinement_report",
           refinement_report.get("inputSelectionArtifactHash") == actual_selection_hash,
           f"recorded={refinement_report.get('inputSelectionArtifactHash')} actual={actual_selection_hash}")

    # ---- Step 13: production immutability ----
    non_empty = [rid for rid, v in hsk1_related_before.items() if v not in (None, [])]
    record("production_hsk1_relatedWordIds_empty", len(non_empty) == 0, f"non-empty: {non_empty[:10]}")

    print("=== P5.4.4 final cross-stage validation ===")
    for name, result in checks.items():
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {name}: {result['detail']}")
    print()
    print(f"allChecksPassed: {all_passed}")

    generated_at = datetime.now(timezone.utc).isoformat()
    final_report = {
        "validationVersion": VALIDATION_VERSION,
        "generatedAt": generated_at,
        "candidatePoolHash": actual_pool_hash,
        "selectionArtifactHash": actual_selection_hash,
        "refinedArtifactHash": actual_refined_hash,
        "refinementReportHash": sha256_of(refinement_report_text),
        "sourceDatasetHash": actual_source_hash,
        "pipelineCounts": {
            "candidatePoolRelationships": pool_total,
            "selectionRelationships": selection_total,
            "refinedRelationships": refined_total,
            "removedInSelection": pool_total - selection_total,
            "removedInRefinement": selection_total - refined_total,
            "totalRemoved": pool_total - refined_total,
        },
        "statusDistribution": {"selected": selected_count, "needs_review": nr_count, "total": selected_count + nr_count},
        "specialCases": special,
        "cTierResults": c_tier_results,
        "checks": checks,
        "allChecksPassed": all_passed,
    }
    with open(REPORT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(final_report, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWrote {REPORT_PATH}")

    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
