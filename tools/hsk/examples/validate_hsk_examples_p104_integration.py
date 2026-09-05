"""P5.10.4 -- Independent validator for the HSK Examples production
integration. Mirrors `validate_hsk5_related_words_p595_integration.py`:
read-only against every file it inspects, re-derives every number
directly rather than trusting the merge script's own report, exits
non-zero on any failure.

Baseline for "what changed" comparisons is `git show <BASELINE_COMMIT>`
against the commit that was HEAD immediately before this integration's
merge script ran (i.e. before any of the six production files were
rewritten) -- not a separate snapshot file.

Usage:
    python validate_hsk_examples_p104_integration.py
"""

import hashlib
import json
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
EXAMPLES_DIR = REPO_ROOT / "tools" / "hsk" / "examples"
PILOT_PATH = EXAMPLES_DIR / "hsk_examples_p102_pilot_01.json"
SPECIAL_REVIEW_PATH = EXAMPLES_DIR / "hsk_examples_special_review_p103.json"

PRODUCTION_PATHS = {
    n: REPO_ROOT / "data" / "hsk" / f"hsk{n}" / f"hsk{n}_vocabulary_production.json"
    for n in (1, 2, 3, 4, 5, 6)
}

# HEAD immediately before this integration's merge script wrote anything.
BASELINE_COMMIT = "cd02b46118809800ab04f59f66a0be90ad88c258"

EXPECTED_PRODUCTION_COUNTS = {1: 300, 2: 200, 3: 500, 4: 1000, 5: 1600, 6: 1800}
EXPECTED_CHANGED_COUNTS = {1: 296, 2: 190, 3: 488, 4: 980, 5: 1575, 6: 1783}
EXPECTED_TOTAL_UNIVERSE = 5400
EXPECTED_SPECIAL_REVIEW = 88
EXPECTED_TOTAL_SOURCE_RECORDS = 5312
EXPECTED_TOTAL_EXAMPLE_SENTENCES = 5406
EXPECTED_NEEDS_REVIEW_EMPTY = 13


def load_json_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def git_show(commit: str, path: str) -> str:
    out = subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=REPO_ROOT)
    return out.decode("utf-8")


def git_hash_object(path: Path) -> str:
    out = subprocess.check_output(["git", "hash-object", str(path)], cwd=REPO_ROOT)
    return out.decode("utf-8").strip()


def level_from_id(rid: str) -> int:
    m = re.match(r"^hsk([1-6])_", rid)
    return int(m.group(1)) if m else -1


def main() -> None:
    checks: dict[str, dict] = {}
    all_passed = True

    def record(name: str, passed: bool, detail: str) -> None:
        nonlocal all_passed
        checks[name] = {"passed": passed, "detail": detail}
        if not passed:
            all_passed = False

    # ---------------- load sources ----------------
    pilot_doc = json.loads(load_json_text(PILOT_PATH))
    pilot_records = pilot_doc["records"]
    batch_paths = sorted(EXAMPLES_DIR.glob("examples_batch_*.json"))
    record("batch_file_count_31", len(batch_paths) == 31, f"{len(batch_paths)}")

    source_by_id: dict[str, list] = {}
    dup_ids = []
    for origin_records in [pilot_records] + [json.loads(load_json_text(p))["records"] for p in batch_paths]:
        for r in origin_records:
            rid = r["sourceId"]
            if rid in source_by_id:
                dup_ids.append(rid)
            source_by_id[rid] = r["examples"]
    record("no_duplicate_source_ids", len(dup_ids) == 0, f"{dup_ids[:10]}")
    record("source_total_5312", len(source_by_id) == EXPECTED_TOTAL_SOURCE_RECORDS, f"{len(source_by_id)}")

    total_sentences = sum(len(v) for v in source_by_id.values())
    record("total_example_sentences_5406", total_sentences == EXPECTED_TOTAL_EXAMPLE_SENTENCES, f"{total_sentences}")

    empty_source = [rid for rid, v in source_by_id.items() if len(v) == 0]
    record("needs_review_empty_count_13", len(empty_source) == EXPECTED_NEEDS_REVIEW_EMPTY, f"{len(empty_source)}")

    # ---------------- special review ----------------
    sr_doc = json.loads(load_json_text(SPECIAL_REVIEW_PATH))
    sr_records = sr_doc["records"] if isinstance(sr_doc, dict) else sr_doc
    special_review_ids = {r.get("sourceId") or r.get("id") for r in sr_records}
    record("special_review_count_88", len(special_review_ids) == EXPECTED_SPECIAL_REVIEW, f"{len(special_review_ids)}")

    overlap = set(source_by_id.keys()) & special_review_ids
    record("no_overlap_source_vs_special_review", len(overlap) == 0, f"{sorted(overlap)[:10]}")

    # ---------------- load current (post-merge) production ----------------
    prod_by_id: dict[str, dict] = {}
    prod_records_by_level: dict[int, list] = {}
    for n, path in PRODUCTION_PATHS.items():
        recs = json.loads(load_json_text(path))
        record(f"hsk{n}_production_count", len(recs) == EXPECTED_PRODUCTION_COUNTS[n], f"{len(recs)}")
        prod_records_by_level[n] = recs
        for r in recs:
            prod_by_id[r["id"]] = r

    prod_ids = list(prod_by_id.keys())
    record("no_duplicate_production_ids", len(prod_ids) == len(set(prod_ids)), f"{len(prod_ids)} vs {len(set(prod_ids))}")
    record("universe_size_5400", len(prod_ids) == EXPECTED_TOTAL_UNIVERSE, f"{len(prod_ids)}")

    union = set(source_by_id.keys()) | special_review_ids
    record("union_equals_universe", union == set(prod_ids), f"union={len(union)} universe={len(prod_ids)}")

    # ---------------- B: every eligible record has examples populated ----------------
    missing_examples = []
    mismatched_examples = []
    for rid, expected in source_by_id.items():
        prod_r = prod_by_id.get(rid)
        if prod_r is None:
            missing_examples.append(rid)
            continue
        if "examples" not in prod_r:
            missing_examples.append(rid)
            continue
        if prod_r["examples"] != expected:
            mismatched_examples.append(rid)
    record("all_eligible_have_examples_key", len(missing_examples) == 0, f"{missing_examples[:10]}")
    record("all_eligible_examples_match_source_exactly", len(mismatched_examples) == 0, f"{mismatched_examples[:10]}")

    # ---------------- C: special-review untouched (no examples key at all) ----------------
    special_review_with_examples = [rid for rid in special_review_ids if "examples" in prod_by_id.get(rid, {})]
    record("special_review_has_no_examples_key", len(special_review_with_examples) == 0,
           f"{special_review_with_examples[:10]}")

    # ---------------- D: no example source id maps to more than one production record ----------------
    # (equivalent to no_duplicate_source_ids above, re-stated as its own named check per the report spec)
    record("no_duplicate_source_to_production_mapping", len(dup_ids) == 0, f"{dup_ids[:10]}")

    # ---------------- E: no production record duplicated ----------------
    # (equivalent to no_duplicate_production_ids above, re-stated as its own named check)
    record("no_duplicate_production_records", len(prod_ids) == len(set(prod_ids)), "see above")

    # ---------------- F: field preservation (everything except 'examples') ----------------
    field_diffs = []
    order_diffs = []
    changed_examples_ids = []
    for n, path in PRODUCTION_PATHS.items():
        before_text = git_show(BASELINE_COMMIT, f"data/hsk/hsk{n}/hsk{n}_vocabulary_production.json")
        before_records = json.loads(before_text)
        before_by_id = {r["id"]: r for r in before_records}
        after_records = prod_records_by_level[n]
        after_by_id = {r["id"]: r for r in after_records}

        order_before = [r["id"] for r in before_records]
        order_after = [r["id"] for r in after_records]
        if order_before != order_after:
            order_diffs.append(n)

        for rid, b in before_by_id.items():
            a = after_by_id[rid]
            for field in set(b.keys()) | set(a.keys()):
                if field == "examples":
                    continue
                if b.get(field) != a.get(field):
                    field_diffs.append((rid, field))
            if b.get("examples") != a.get("examples"):
                changed_examples_ids.append(rid)

    record("only_examples_field_changed", len(field_diffs) == 0, f"{field_diffs[:10]}")
    record("record_ordering_preserved_all_levels", len(order_diffs) == 0, f"levels_reordered={order_diffs}")

    changed_by_level: dict[int, int] = {n: 0 for n in PRODUCTION_PATHS}
    for rid in changed_examples_ids:
        changed_by_level[level_from_id(rid)] += 1
    for n in PRODUCTION_PATHS:
        record(f"hsk{n}_changed_count_matches_expected",
               changed_by_level[n] == EXPECTED_CHANGED_COUNTS[n],
               f"{changed_by_level[n]} vs expected {EXPECTED_CHANGED_COUNTS[n]}")

    # ---------------- G: Related Words regression -- relatedWordIds byte-identical ----------------
    related_words_diffs = []
    for n, path in PRODUCTION_PATHS.items():
        before_text = git_show(BASELINE_COMMIT, f"data/hsk/hsk{n}/hsk{n}_vocabulary_production.json")
        before_records = json.loads(before_text)
        before_by_id = {r["id"]: r for r in before_records}
        for r in prod_records_by_level[n]:
            rid = r["id"]
            b = before_by_id[rid]
            if b.get("relatedWordIds") != r.get("relatedWordIds"):
                related_words_diffs.append(rid)
    record("related_words_unchanged", len(related_words_diffs) == 0, f"{related_words_diffs[:10]}")

    # ---------------- H: examples integrity ----------------
    example_field_shape_errors = []
    for rid, prod_r in prod_by_id.items():
        if "examples" not in prod_r:
            continue
        for i, ex in enumerate(prod_r["examples"]):
            if set(ex.keys()) != {"chinese", "pinyin", "meaningVi"}:
                example_field_shape_errors.append((rid, i))
    record("examples_have_expected_schema", len(example_field_shape_errors) == 0, f"{example_field_shape_errors[:10]}")

    non_eligible_with_content = [
        rid for rid in special_review_ids
        if "examples" in prod_by_id.get(rid, {}) and len(prod_by_id[rid]["examples"]) > 0
    ]
    record("no_unexpected_examples_on_special_review", len(non_eligible_with_content) == 0,
           f"{non_eligible_with_content[:10]}")

    # ---------------- adapter check ----------------
    adapter_path = REPO_ROOT / "app" / "src" / "lib" / "data" / "vocabularyAdapter.ts"
    adapter_text = adapter_path.read_text(encoding="utf-8")
    reads_raw_examples = "raw.examples" in adapter_text
    hardcodes_empty = "examples: []," in adapter_text.replace(" ", "").replace("\n", "")
    record("adapter_reads_raw_examples", reads_raw_examples, f"'raw.examples' present: {reads_raw_examples}")
    record("adapter_no_longer_hardcodes_empty", not hardcodes_empty, f"hardcoded '[]' still present: {hardcodes_empty}")

    # ---------------- app/src untouched except the adapter ----------------
    app_src_status = subprocess.check_output(
        ["git", "status", "--short", "--", "app/src"], cwd=REPO_ROOT
    ).decode("utf-8").strip()
    lines = [l for l in app_src_status.splitlines() if l.strip()]
    non_adapter_lines = [l for l in lines if "vocabularyAdapter.ts" not in l]
    record("app_src_only_adapter_modified", len(non_adapter_lines) == 0, f"{non_adapter_lines}")

    print("=== P5.10.4 integration validation ===")
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
