"""P5.9.5 -- Independent validator for the HSK5 production integration.

Read-only against every file it inspects. Never writes to production, the
before-snapshot, the refined artifact, the P5.9.2 selection, the
candidate pool, or any other prior-phase artifact. Exits non-zero if any
check fails.

Usage:
    python validate_hsk5_related_words_p595_integration.py
"""

import hashlib
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REFINED_PATH = REPO_ROOT / "tools" / "hsk" / "hsk5_related_words_refined_selection.json"
SELECTION_PATH = REPO_ROOT / "tools" / "hsk" / "hsk5_related_words_selection.json"
BEFORE_SNAPSHOT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk5_production_p595_before_snapshot.json"
PRODUCTION_PATH = REPO_ROOT / "data" / "hsk" / "hsk5" / "hsk5_vocabulary_production.json"
BASELINE_COMMIT = "9775f22f93cd1bd0467e6eb1318e6a42f3ffa6ea"

OTHER_LEVEL_PATHS = {
    n: REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
    for n in (1, 2, 3, 4, 6)
}
EXPECTED_OTHER_LEVEL_HASHES = {
    1: "371c8c5b16a5b7250433b4adffa419f4752fe4a2",
    2: "f468aeafeda1a32285b303dc2b37c284b9160d45",
    3: "0d21c124e2e11351b8f89fb62a1d9e2f613de7fd",
    4: "b85fc217da54d4796df951b19e32b1029dfb8feb",
    6: "77fad88d80caed515a1875aa296cc9d7c12011a0",
}

EXPECTED_TOTAL_RELATIONSHIPS = 384
EXPECTED_ELIGIBLE = 379
EXPECTED_WITHHELD = 5
EXPECTED_RECORDS_CHANGED = 131


def load_json_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def git_show(commit: str, path: str) -> str:
    out = subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=REPO_ROOT)
    return out.decode("utf-8")


def git_hash_object(path: Path) -> str:
    out = subprocess.check_output(["git", "hash-object", str(path)], cwd=REPO_ROOT)
    return out.decode("utf-8").strip()


def main() -> None:
    checks: dict[str, dict] = {}
    all_passed = True

    def record(name: str, passed: bool, detail: str) -> None:
        nonlocal all_passed
        checks[name] = {"passed": passed, "detail": detail}
        if not passed:
            all_passed = False

    refined_text = load_json_text(REFINED_PATH)
    refined = json.loads(refined_text)
    refined_records = refined["records"]

    selection = json.loads(load_json_text(SELECTION_PATH))
    rejected_pairs = {(e["sourceId"], e["targetId"]) for e in selection["rejectedRelationships"]}

    prod_text = load_json_text(PRODUCTION_PATH)
    prod_records = json.loads(prod_text)
    prod_by_id = {r["id"]: r for r in prod_records}

    before_text_from_git = git_show(BASELINE_COMMIT, "data/hsk/hsk5/hsk5_vocabulary_production.json")
    before_records = json.loads(before_text_from_git)
    before_by_id = {r["id"]: r for r in before_records}

    # ---------------- 1-4: source count / hashes ----------------
    record("source_record_count", len(refined_records) == 1600, f"{len(refined_records)}")

    def canon_hash(text):
        data = json.loads(text)
        data.pop("generatedAt", None)
        return sha256_of(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))

    refined_canon_hash = canon_hash(refined_text)
    record("refined_artifact_hash_present", bool(refined_canon_hash), f"{refined_canon_hash}")

    baseline_prod_hash = git_hash_object(Path(BEFORE_SNAPSHOT_PATH))  # sanity: snapshot exists
    record("production_baseline_snapshot_exists", BEFORE_SNAPSHOT_PATH.exists(), str(BEFORE_SNAPSHOT_PATH))

    # ---------------- eligible/withheld recomputation ----------------
    eligible_by_source: dict[str, list[str]] = {}
    withheld_count = 0
    eligible_count = 0
    for r in refined_records:
        sid = r["sourceId"]
        related = r.get("selectedRelatedWordIds") or []
        reasons_by_target = {rr["relatedWordId"]: rr for rr in r.get("selectionReasons", [])}
        targets = []
        for tid in related:
            reason = reasons_by_target.get(tid)
            if reason and "needsReviewReason" in reason:
                withheld_count += 1
            else:
                eligible_count += 1
                targets.append(tid)
        eligible_by_source[sid] = targets

    record("eligible_relationship_count_379", eligible_count == EXPECTED_ELIGIBLE, f"{eligible_count}")
    record("withheld_relationship_count_5", withheld_count == EXPECTED_WITHHELD, f"{withheld_count}")
    record("eligible_plus_withheld_equals_total", eligible_count + withheld_count == EXPECTED_TOTAL_RELATIONSHIPS,
           f"{eligible_count}+{withheld_count} vs {EXPECTED_TOTAL_RELATIONSHIPS}")

    # ---------------- 5. exact source -> target mapping ----------------
    missing_from_production = []
    extra_in_production = []
    mismatched = []
    for sid, targets in eligible_by_source.items():
        prod_r = prod_by_id.get(sid)
        if prod_r is None:
            missing_from_production.append(sid)
            continue
        actual = prod_r.get("relatedWordIds") or []
        if sorted(actual) != sorted(targets):
            mismatched.append((sid, sorted(targets), sorted(actual)))
    record("no_missing_eligible_relationships", len(missing_from_production) == 0, f"{missing_from_production[:10]}")
    record("exact_mapping_no_mismatches", len(mismatched) == 0, f"{mismatched[:10]}")

    # extra: any production record with relatedWordIds not matching an eligible source
    for pid, prec in prod_by_id.items():
        rel = prec.get("relatedWordIds") or []
        if rel:
            expected = eligible_by_source.get(pid)
            if expected is None or sorted(rel) != sorted(expected):
                extra_in_production.append(pid)
    record("no_extra_relationships_in_production", len(extra_in_production) == 0, f"{extra_in_production[:10]}")

    # ---------------- 6-9. needs_review / rejection / self-link / duplicate leakage ----------------
    needs_review_leaked = []
    for r in refined_records:
        for rr in r.get("selectionReasons", []):
            if "needsReviewReason" in rr:
                sid, tid = r["sourceId"], rr["relatedWordId"]
                prod_r = prod_by_id.get(sid)
                if prod_r and tid in (prod_r.get("relatedWordIds") or []):
                    needs_review_leaked.append((sid, tid))
    record("no_needs_review_leakage", len(needs_review_leaked) == 0, f"{needs_review_leaked[:10]}")

    rejected_leaked = []
    for pid, prec in prod_by_id.items():
        rel = prec.get("relatedWordIds") or []
        for tid in rel:
            if (pid, tid) in rejected_pairs:
                rejected_leaked.append((pid, tid))
    record("no_rejected_leakage", len(rejected_leaked) == 0, f"{rejected_leaked[:10]}")

    self_links = []
    dup_targets = []
    for r in prod_records:
        rel = r.get("relatedWordIds") or []
        if r["id"] in rel:
            self_links.append(r["id"])
        if len(rel) != len(set(rel)):
            dup_targets.append(r["id"])
    record("no_self_links", len(self_links) == 0, f"{self_links[:10]}")
    record("no_duplicates", len(dup_targets) == 0, f"{dup_targets[:10]}")

    # ---------------- valid IDs / target levels ----------------
    universe = set()
    universe_level = {}
    for n in (1, 2, 3, 4, 5, 6):
        recs = json.loads(load_json_text(REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"))
        for rr in recs:
            universe.add(rr["id"])
            universe_level[rr["id"]] = n
    invalid_ids = []
    target_level_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for r in prod_records:
        for tid in (r.get("relatedWordIds") or []):
            if tid not in universe:
                invalid_ids.append((r["id"], tid))
            else:
                target_level_counts[universe_level[tid]] += 1
    record("valid_ids", len(invalid_ids) == 0, f"{invalid_ids[:10]}")
    record("target_levels_recorded", True, f"{target_level_counts}")

    # ---------------- field preservation ----------------
    field_diffs = []
    order_before = [r["id"] for r in before_records]
    order_after = [r["id"] for r in prod_records]
    for rid in before_by_id:
        b = before_by_id[rid]
        a = prod_by_id[rid]
        for field in set(b.keys()) | set(a.keys()):
            if field == "relatedWordIds":
                continue
            if b.get(field) != a.get(field):
                field_diffs.append((rid, field))
    record("only_relatedWordIds_changed", len(field_diffs) == 0, f"{field_diffs[:10]}")
    record("record_ordering_preserved", order_before == order_after, f"preserved={order_before == order_after}")

    changed_ids = [rid for rid in before_by_id if (before_by_id[rid].get("relatedWordIds") or []) != (prod_by_id[rid].get("relatedWordIds") or [])]
    record("records_changed_count_131", len(changed_ids) == EXPECTED_RECORDS_CHANGED, f"{len(changed_ids)}")

    # ---------------- HSK1/2/3/4/6 unchanged ----------------
    other_level_diffs = []
    for n, path in OTHER_LEVEL_PATHS.items():
        actual_hash = git_hash_object(path)
        expected_hash = EXPECTED_OTHER_LEVEL_HASHES[n]
        if actual_hash != expected_hash:
            other_level_diffs.append((n, expected_hash, actual_hash))
    record("hsk1_unchanged", not any(d[0] == 1 for d in other_level_diffs), f"{[d for d in other_level_diffs if d[0]==1]}")
    record("hsk2_unchanged", not any(d[0] == 2 for d in other_level_diffs), f"{[d for d in other_level_diffs if d[0]==2]}")
    record("hsk3_unchanged", not any(d[0] == 3 for d in other_level_diffs), f"{[d for d in other_level_diffs if d[0]==3]}")
    record("hsk4_unchanged", not any(d[0] == 4 for d in other_level_diffs), f"{[d for d in other_level_diffs if d[0]==4]}")
    record("hsk6_unchanged", not any(d[0] == 6 for d in other_level_diffs), f"{[d for d in other_level_diffs if d[0]==6]}")

    app_src_status = subprocess.check_output(
        ["git", "status", "--short", "--", "app/src"], cwd=REPO_ROOT
    ).decode("utf-8").strip()
    record("app_src_unchanged", app_src_status == "", f"git status: '{app_src_status}'")

    # ---------------- idempotency (re-derive plan, expect 0 to_add) ----------------
    prod_hash_now = git_hash_object(PRODUCTION_PATH)
    all_applied = all(
        sorted(prod_by_id[sid].get("relatedWordIds") or []) == sorted(targets)
        for sid, targets in eligible_by_source.items()
    )
    record("idempotency_all_eligible_already_applied", all_applied, f"production_hash={prod_hash_now}")

    # ---------------- counts reconcile ----------------
    non_empty_count = sum(1 for r in prod_records if (r.get("relatedWordIds") or []))
    total_related = sum(len(r.get("relatedWordIds") or []) for r in prod_records)
    record("records_with_relatedWordIds_matches_eligible_source_count",
           non_empty_count == sum(1 for t in eligible_by_source.values() if t),
           f"production={non_empty_count} eligible_nonzero_sources={sum(1 for t in eligible_by_source.values() if t)}")
    record("total_relatedWordIds_matches_eligible_count", total_related == eligible_count,
           f"production_total={total_related} eligible_count={eligible_count}")

    print("=== P5.9.5 integration validation ===")
    for name, result in checks.items():
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {name}: {result['detail']}")

    print()
    print(f"allChecksPassed: {all_passed}")
    print(f"checksTotal: {len(checks)}")
    print(f"checksPassed: {sum(1 for c in checks.values() if c['passed'])}")

    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
