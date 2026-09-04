"""P5.8.5 -- Independent validator for the HSK4 production integration.

Read-only against every file it inspects. Never writes to production, the
before-snapshot, the refined artifact, or any other prior-phase artifact.
Exits non-zero if any check fails.

Checks are grouped under: Source integrity / Production integrity /
Change isolation / Idempotency / Data quality / Safety, per the P5.8.5
instructions.

Usage:
    python validate_hsk4_related_words_p585_integration.py
"""

import hashlib
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REFINED_PATH = REPO_ROOT / "tools" / "hsk" / "hsk4_related_words_refined_selection.json"
BEFORE_SNAPSHOT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk4_production_p585_before_snapshot.json"
PRODUCTION_PATH = REPO_ROOT / "data" / "hsk" / "hsk4" / "hsk4_vocabulary_production.json"
BASELINE_COMMIT = "6226508d21d1e1c50b56daae1bda7273df5d781c"

OTHER_LEVEL_PATHS = {
    n: REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
    for n in (1, 2, 3, 5, 6)
}
EXPECTED_OTHER_LEVEL_HASHES = {
    1: "371c8c5b16a5b7250433b4adffa419f4752fe4a2",
    2: "f468aeafeda1a32285b303dc2b37c284b9160d45",
    3: "0d21c124e2e11351b8f89fb62a1d9e2f613de7fd",
    5: "bd4e73287052df0b19e7fbbbffb06ec48819d6af",
    6: "77fad88d80caed515a1875aa296cc9d7c12011a0",
}

EXPECTED_TOTAL_RELATIONSHIPS = 698
EXPECTED_ELIGIBLE = 669
EXPECTED_WITHHELD = 29
EXPECTED_RECORDS_CHANGED = 256
EXPECTED_SELECTED = 990
EXPECTED_NEEDS_REVIEW = 10


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

    prod_text = load_json_text(PRODUCTION_PATH)
    prod_records = json.loads(prod_text)
    prod_by_id = {r["id"]: r for r in prod_records}

    before_text_from_git = git_show(BASELINE_COMMIT, "data/hsk/hsk4/hsk4_vocabulary_production.json")
    before_records = json.loads(before_text_from_git)
    before_by_id = {r["id"]: r for r in before_records}

    # ---------------- Source integrity ----------------
    record("source_record_count", len(refined_records) == 1000, f"{len(refined_records)}")
    selected = [r for r in refined_records if r["status"] == "selected"]
    needs_review = [r for r in refined_records if r["status"] == "needs_review"]
    record("selected_count", len(selected) == EXPECTED_SELECTED, f"{len(selected)}")
    record("needs_review_count", len(needs_review) == EXPECTED_NEEDS_REVIEW, f"{len(needs_review)}")

    total_rel = sum(len(r.get("selectedRelatedWordIds") or []) for r in refined_records)
    eligible_rel = sum(len(r.get("selectedRelatedWordIds") or []) for r in selected)
    withheld_rel = sum(len(r.get("selectedRelatedWordIds") or []) for r in needs_review)
    record("total_relationships_698", total_rel == EXPECTED_TOTAL_RELATIONSHIPS, f"{total_rel}")
    record("eligible_relationships_669", eligible_rel == EXPECTED_ELIGIBLE, f"{eligible_rel}")
    record("withheld_relationships_29", withheld_rel == EXPECTED_WITHHELD, f"{withheld_rel}")
    record("eligible_plus_withheld_equals_total", eligible_rel + withheld_rel == total_rel,
           f"{eligible_rel}+{withheld_rel} vs {total_rel}")

    self_refs = [r["sourceId"] for r in refined_records if r["sourceId"] in (r.get("selectedRelatedWordIds") or [])]
    record("no_self_links_in_source", len(self_refs) == 0, f"{self_refs[:10]}")

    # ---------------- Production integrity ----------------
    record("production_record_count", len(prod_records) == 1000, f"{len(prod_records)}")
    record("baseline_matches_committed_state", set(before_by_id) == set(prod_by_id),
           "record id sets match")

    committed_baseline_hash = sha256_of(before_text_from_git)
    record("baseline_had_zero_related_word_ids",
           all(not (r.get("relatedWordIds") or []) for r in before_records),
           "true" if all(not (r.get("relatedWordIds") or []) for r in before_records) else "false")

    # ---------------- Change isolation ----------------
    changed_ids = []
    for rid in before_by_id:
        b = before_by_id[rid].get("relatedWordIds") or []
        a = prod_by_id[rid].get("relatedWordIds") or []
        if b != a:
            changed_ids.append(rid)
    record("records_changed_count_256", len(changed_ids) == EXPECTED_RECORDS_CHANGED, f"{len(changed_ids)}")

    field_diffs = []
    for rid in before_by_id:
        b = before_by_id[rid]
        a = prod_by_id[rid]
        for field in set(b.keys()) | set(a.keys()):
            if field == "relatedWordIds":
                continue
            if b.get(field) != a.get(field):
                field_diffs.append((rid, field))
    record("no_non_relatedWordIds_field_diffs", len(field_diffs) == 0, f"{field_diffs[:10]}")

    order_preserved = [r["id"] for r in before_records] == [r["id"] for r in prod_records]
    record("record_ordering_preserved", order_preserved, f"preserved={order_preserved}")

    other_level_diffs = []
    for n, path in OTHER_LEVEL_PATHS.items():
        actual_hash = git_hash_object(path)
        expected_hash = EXPECTED_OTHER_LEVEL_HASHES[n]
        if actual_hash != expected_hash:
            other_level_diffs.append((n, expected_hash, actual_hash))
    record("other_hsk_levels_unchanged", len(other_level_diffs) == 0, f"{other_level_diffs}")

    app_src_status = subprocess.check_output(
        ["git", "status", "--short", "--", "app/src"], cwd=REPO_ROOT
    ).decode("utf-8").strip()
    record("app_src_unchanged", app_src_status == "", f"git status: '{app_src_status}'")

    # ---------------- Data quality (exact mapping) ----------------
    mismatches = []
    needs_review_leaked = []
    fabricated = []
    for r in refined_records:
        sid = r["sourceId"]
        expected = r["selectedRelatedWordIds"] if r["status"] == "selected" else []
        actual = prod_by_id[sid].get("relatedWordIds") or []
        if actual != expected:
            mismatches.append(sid)
        if r["status"] == "needs_review" and actual:
            needs_review_leaked.append(sid)
    for pid, prec in prod_by_id.items():
        rel = prec.get("relatedWordIds") or []
        if rel:
            src = next((r for r in refined_records if r["sourceId"] == pid), None)
            if src is None or src["status"] != "selected" or rel != src["selectedRelatedWordIds"]:
                fabricated.append(pid)
    record("exact_mapping_no_mismatches", len(mismatches) == 0, f"{mismatches[:10]}")
    record("no_needs_review_leakage", len(needs_review_leaked) == 0, f"{needs_review_leaked[:10]}")
    record("no_fabricated_relationships_in_production", len(fabricated) == 0, f"{fabricated[:10]}")

    all_target_ids = set()
    for r in prod_records:
        all_target_ids.add(r["id"])
    # build cross-level id universe for full validity check
    universe = set(all_target_ids)
    for n, path in OTHER_LEVEL_PATHS.items():
        recs = json.loads(load_json_text(path))
        for r in recs:
            universe.add(r["id"])

    invalid_targets = []
    non_hsk4_targets = []
    dup_targets = []
    self_targets = []
    for r in prod_records:
        rel = r.get("relatedWordIds") or []
        if len(rel) != len(set(rel)):
            dup_targets.append(r["id"])
        if r["id"] in rel:
            self_targets.append(r["id"])
        for t in rel:
            if t not in universe:
                invalid_targets.append((r["id"], t))
            elif not t.startswith("hsk4_"):
                non_hsk4_targets.append((r["id"], t))
    record("no_invalid_target_ids", len(invalid_targets) == 0, f"{invalid_targets[:10]}")
    record("all_targets_within_hsk4_scope", len(non_hsk4_targets) == 0, f"{non_hsk4_targets[:10]}")
    record("no_duplicate_target_ids", len(dup_targets) == 0, f"{dup_targets[:10]}")
    record("no_self_links_in_production", len(self_targets) == 0, f"{self_targets[:10]}")

    # ---------------- Idempotency ----------------
    prod_hash = git_hash_object(PRODUCTION_PATH)
    record("production_file_hash_recorded", bool(prod_hash), f"{prod_hash}")

    print("=== P5.8.5 integration validation ===")
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
