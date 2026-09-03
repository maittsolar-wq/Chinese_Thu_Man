#!/usr/bin/env python3
"""P3.5.5 targeted semantic refinement.

Applies ONLY the explicitly-approved, individually-judged removals and
status changes documented below to the merged artifact
(tools/hsk/hsk6_related_words_selection.json). Does NOT touch the 40
original hsk6_sel*.jsonl batch files, the HSK6 candidate pool, HSK1-5
artifacts, production vocabulary, or app/src.

Every change is recorded with its reason in the refinement report. No
relationship was invented or auto-replaced; where a removal was proposed,
this script only reports possible replacements already present in the
existing data (there is none in most cases, since no separate candidate
list exists beyond what was already selected).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS_HSK = ROOT / "tools" / "hsk"
DATA_HSK = ROOT / "data" / "hsk"

MERGED_PATH = TOOLS_HSK / "hsk6_related_words_selection.json"
BASELINE_REPORT_PATH = TOOLS_HSK / "hsk6_related_words_validation_report.baseline.json"
REFINEMENT_REPORT_PATH = TOOLS_HSK / "hsk6_related_words_refinement_report.json"

SELECTED_MIN_COUNT = 4

# ---------------------------------------------------------------------------
# PHASE 2 - the 9 individually reviewed clear semantic errors.
# (sourceId, relatedWordId, reason for removal)
# ---------------------------------------------------------------------------
PHASE2_REMOVALS = [
    ("hsk6_0031", "hsk6_0861",
     "Reading mismatch: 暴露 (bàolù) uses the lù reading of 露 ('to reveal'); "
     "hsk6_0861 is specifically the lòu reading ('to show/appear'). The "
     "correct lù-reading sibling (hsk6_0863, 露1) is already present in "
     "this record, so removal loses no coverage."),
    ("hsk6_0387", "hsk6_1126",
     "Reading mismatch: 分散 (fēnsàn, 'to disperse') uses the sàn reading "
     "of 散; hsk6_1126 is specifically the sǎn reading ('scattered', "
     "adjective). The correct sàn-reading sibling (hsk6_1128) is already "
     "present in this record, so removal loses no coverage."),
    ("hsk6_0820", "hsk1_119",
     "Reason cited only '犭-radical animal category' - no lexical/semantic "
     "link between 狼 (wolf) and 猫 (cat) beyond shared radical + broad "
     "animal category, both explicitly named reject criteria."),
    ("hsk6_0820", "hsk5_484",
     "Reason cited only 'general animal category' - wolf and monkey share "
     "no lexical/semantic link beyond broad category, an explicitly named "
     "reject criterion."),
    ("hsk6_0885", "hsk5_969",
     "Reason self-describes as 'a weaker small-creature category' - snake "
     "is not an insect; the justification itself admits the relationship "
     "is weak/overreaching."),
    ("hsk6_0904", "hsk5_969",
     "Same issue as hsk6_0885->hsk5_969: reason self-describes as a "
     "'weaker small-creature category'; bee and snake share no defensible "
     "lexical link."),
    ("hsk6_1741", "hsk6_0316",
     "Reason cited only 'measure-word category' - 株 (measure word for "
     "plants) and 栋 (measure word for buildings) measure entirely "
     "unrelated noun classes; zero semantic overlap beyond both being "
     "measure words in general, an explicitly named reject criterion."),
    ("hsk6_1349", "hsk6_1586",
     "Sense mismatch: this dataset's own meaningVi for hsk6_1349 娃娃 is "
     "'búp bê' (doll), not 'baby/young child'. The relationship treats it "
     "as synonymous with 婴儿 (baby), contradicting the word's own "
     "recorded sense in this dataset."),
    ("hsk6_1577", "hsk6_1309",
     "Sense mismatch: hsk6_1577 银牌 means 'silver medal' (an award/"
     "ranking), not the raw metal. Relating it to 铜 (plain copper) via "
     "'metal category' conflates the medal sense with the metal sense. "
     "The record already has 铜牌 (hsk6_1314, 'bronze medal') as the "
     "correct medal-family sibling, so removal loses no coverage."),
]

# ---------------------------------------------------------------------------
# PHASE 3 - the 一-leading-character / numeral-padding cluster, evaluated
# relationship by relationship. Only relationships whose stated reason
# attributes the link to the shared 一 character (not some other shared
# character in the same record) were considered for removal; relationships
# justified by a different shared character (同, 系, 身, 律, 辈, 风, 时,
# 阵) or an explicit synonym claim were left untouched unless the synonym
# claim itself did not hold up (none were found to fail on close reading).
# ---------------------------------------------------------------------------
PHASE3_REMOVALS = [
    # hsk6_1541 一一 (one by one) - loses all 5: "one by one" (itemizing
    # separately/sequentially) shares no real meaning with togetherness,
    # constancy, uniformity, or repetition; only the leading 一 is shared.
    ("hsk6_1541", "hsk6_1547", "一-only: 一一 (one by one) vs 一道 (together) - no independent semantic link; opposing nuance if anything (itemized vs unified)."),
    ("hsk6_1541", "hsk6_1571", "一-only: 一一 (one by one) vs 一同 (together) - no independent semantic link."),
    ("hsk6_1541", "hsk6_1556", "一-only: 一一 (one by one, itemization) vs 一再 (repeatedly, action recurrence) - different concepts, no independent link."),
    ("hsk6_1541", "hsk6_1554", "一-only: 一一 (one by one) vs 一向 (always) - no independent semantic link."),
    ("hsk6_1541", "hsk6_1550", "一-only: 一一 (individually) vs 一律 (uniformly, without exception) - contrasting nuance, no independent link."),

    # hsk6_1556 一再 (repeatedly) - keeps 再三 (true synonym), loses the
    # rest: "repeatedly" (episodic frequency) is not synonymous with
    # consistency/constancy/togetherness.
    ("hsk6_1556", "hsk6_1548", "一-only: 一再 (repeatedly, frequency) vs 一贯 (consistent, steady state) - different semantic function, no independent link."),
    ("hsk6_1556", "hsk6_1554", "一-only: 一再 (repeatedly) vs 一向 (always) - different nuance, no independent link."),
    ("hsk6_1556", "hsk6_1550", "一-only: 一再 (repeatedly) vs 一律 (uniformly/no exception) - no independent link."),
    ("hsk6_1556", "hsk6_1571", "一-only: 一再 (repeatedly) vs 一同 (together) - no independent link."),

    # hsk6_1565 一口气 (in one breath/continuously, without stopping) -
    # loses all 5: describes MANNER of doing something in one uninterrupted
    # go, arguably opposite of "repeatedly"; no link to togetherness/
    # constancy/uniformity either.
    ("hsk6_1565", "hsk6_1547", "一-only: 一口气 (in one continuous go) vs 一道 (together) - no independent link."),
    ("hsk6_1565", "hsk6_1571", "一-only: 一口气 vs 一同 (together) - no independent link."),
    ("hsk6_1565", "hsk6_1554", "一-only: 一口气 vs 一向 (always) - no independent link."),
    ("hsk6_1565", "hsk6_1556", "一-only: 一口气 (all at once, not repeated) vs 一再 (repeatedly) - arguably contrasting, no independent link."),
    ("hsk6_1565", "hsk6_1550", "一-only: 一口气 vs 一律 (uniformly) - no independent link."),

    # hsk6_1571 一同 (together) - keeps 一道 (true synonym) + 陪同/同伴/
    # 同行 (genuine 同-based links, out of 一-scope), loses only 一再.
    ("hsk6_1571", "hsk6_1556", "一-only: 一同 (together) vs 一再 (repeatedly) - no independent link."),

    # hsk6_1554 一向 (always/habitually) - keeps 一贯 (true synonym), loses
    # the rest, including 一律 (related domain but distinct nuance:
    # personal habitual constancy vs universal without-exception rule).
    ("hsk6_1554", "hsk6_1550", "一-only: 一向 (personal habitual constancy) vs 一律 (uniform application across a group) - related domain but distinct nuance, not a defensible near-synonym pair on close reading."),
    ("hsk6_1554", "hsk6_1571", "一-only: 一向 vs 一同 (together) - no independent link."),
    ("hsk6_1554", "hsk6_1556", "一-only: 一向 vs 一再 (repeatedly) - no independent link."),
    ("hsk6_1554", "hsk6_1547", "一-only: 一向 vs 一道 (together) - no independent link."),

    # hsk6_1564 一帆风顺 (smooth sailing, idiom) - keeps 风力/风雨 (genuine
    # literal-etymology link via 风, out of 一-scope), loses the 3 一-only
    # picks (idiom's figurative meaning has no relation to consistency).
    ("hsk6_1564", "hsk6_1548", "一-only: idiom 一帆风顺 (everything going smoothly) vs 一贯 (consistent) - no independent link beyond shared 一."),
    ("hsk6_1564", "hsk6_1554", "一-only: 一帆风顺 vs 一向 (always) - no independent link."),
    ("hsk6_1564", "hsk6_1550", "一-only: 一帆风顺 vs 一律 (uniformly) - no independent link."),

    # hsk6_1546 一带 (a region/zone) - loses all 5: "a region" shares no
    # meaning with first-rate/lifetime/whole-body/together/consistent.
    ("hsk6_1546", "hsk6_1543", "一-only: 一带 (a region) vs 一辈子 (a lifetime) - no independent link."),
    ("hsk6_1546", "hsk6_1569", "一-only: 一带 (a region) vs 一身 (whole body) - no independent link."),
    ("hsk6_1546", "hsk6_1538", "一-only: 一带 (a region) vs 一流 (first-rate) - no independent link."),
    ("hsk6_1546", "hsk6_1547", "一-only: 一带 (a region) vs 一道 (together) - no independent link."),
    ("hsk6_1546", "hsk6_1548", "一-only: 一带 (a region) vs 一贯 (consistent) - no independent link."),

    # hsk6_1550 一律 (uniformly) - keeps 一贯 (consistency-domain, explicit
    # near-synonym claim) + 自律 (genuine 律-based link, out of 一-scope),
    # loses 一向 (distinct nuance, see above) and the unrelated pair.
    ("hsk6_1550", "hsk6_1554", "一-only: 一律 (uniform across a group) vs 一向 (personal habitual constancy) - distinct nuance, not a defensible near-synonym pair on close reading."),
    ("hsk6_1550", "hsk6_1571", "一-only: 一律 vs 一同 (together) - no independent link."),
    ("hsk6_1550", "hsk6_1556", "一-only: 一律 vs 一再 (repeatedly) - no independent link."),

    # hsk6_1570 一时 (temporarily/for a moment) - keeps the genuine 时-based
    # time-domain relationships (out of 一-scope), loses only the one
    # 一-only cross-domain pick.
    ("hsk6_1570", "hsk6_1538", "一-only: 一时 (brief time) vs 一流 (first-rate/quality) - no independent link."),

    # hsk6_1538 一流 (first-rate/top-notch) - loses all 5: a quality
    # rating shares no meaning with consistency/series/uniformity/
    # repetition.
    ("hsk6_1538", "hsk6_1548", "一-only: 一流 (first-rate) vs 一贯 (consistent) - no independent link."),
    ("hsk6_1538", "hsk6_1555", "一-only: 一流 (first-rate) vs 一系列 (a series) - no independent link."),
    ("hsk6_1538", "hsk6_1554", "一-only: 一流 (first-rate) vs 一向 (always) - no independent link."),
    ("hsk6_1538", "hsk6_1550", "一-only: 一流 (first-rate) vs 一律 (uniformly) - no independent link."),
    ("hsk6_1538", "hsk6_1556", "一-only: 一流 (first-rate) vs 一再 (repeatedly) - no independent link."),

    # hsk6_1555 一系列 (a series of) - keeps 系列/体系 (genuine 系-based
    # links, out of 一-scope), loses the 3 一-only cross-domain picks.
    ("hsk6_1555", "hsk6_1538", "一-only: 一系列 (a series) vs 一流 (first-rate) - no independent link."),
    ("hsk6_1555", "hsk6_1548", "一-only: 一系列 (a series) vs 一贯 (consistent) - no independent link."),
    ("hsk6_1555", "hsk6_1554", "一-only: 一系列 (a series) vs 一向 (always) - no independent link."),

    # hsk6_1548 一贯 (consistent) - keeps 一向/一律 (consistency-domain,
    # symmetric with the KEEP decisions above), loses the 3 unrelated ones.
    ("hsk6_1548", "hsk6_1555", "一-only: 一贯 (consistent) vs 一系列 (a series) - no independent link."),
    ("hsk6_1548", "hsk6_1538", "一-only: 一贯 (consistent) vs 一流 (first-rate) - no independent link."),
    ("hsk6_1548", "hsk6_1556", "一-only: 一贯 (consistent) vs 一再 (repeatedly) - no independent link (mirrors the hsk6_1556->hsk6_1548 removal)."),

    # hsk6_1569 一身 (whole body / occasionally 'a lifetime') - keeps all
    # 身-based relationships (genuine, out of 一-scope; 一辈子 kept because
    # its own reason asserts a real shared 'lifespan' sense, not just
    # shared 一), loses only the 一-only cross-domain pick.
    ("hsk6_1569", "hsk6_1546", "一-only: 一身 (body/lifetime) vs 一带 (a region) - no independent link."),

    # hsk6_1547 一道 (together) - keeps 一同 (true synonym), loses the 4
    # 一-only cross-domain picks.
    ("hsk6_1547", "hsk6_1541", "一-only: 一道 (together) vs 一一 (one by one) - no independent link; opposing nuance if anything."),
    ("hsk6_1547", "hsk6_1554", "一-only: 一道 (together) vs 一向 (always) - no independent link."),
    ("hsk6_1547", "hsk6_1556", "一-only: 一道 (together) vs 一再 (repeatedly) - no independent link."),
    ("hsk6_1547", "hsk6_1550", "一-only: 一道 (together) vs 一律 (uniformly) - no independent link."),

    # hsk6_1557 一阵 (a burst/spell) - keeps 阵雨 (genuine 阵-based link,
    # out of 一-scope), loses the 4 一-only cross-domain picks.
    ("hsk6_1557", "hsk6_1548", "一-only: 一阵 (a short burst) vs 一贯 (consistent) - no independent link."),
    ("hsk6_1557", "hsk6_1554", "一-only: 一阵 (a short burst) vs 一向 (always) - no independent link."),
    ("hsk6_1557", "hsk6_1556", "一-only: 一阵 (a short burst) vs 一再 (repeatedly) - no independent link."),
    ("hsk6_1557", "hsk6_1571", "一-only: 一阵 (a short burst) vs 一同 (together) - no independent link."),

    # hsk6_1643 再三 (again and again) - keeps 一再 (true synonym), loses
    # the rest, including the two framed as "repetitive/consistency theme"
    # which do not hold up as a defensible near-synonym pair on close
    # reading (repetition-of-instances vs universality/constancy).
    ("hsk6_1643", "hsk6_1550", "Weak cross-domain: 再三 (repeatedly) vs 一律 (uniformly/no exception) - related abstract 'pattern over time' super-category but distinct specific meaning; not a defensible near-synonym pair."),
    ("hsk6_1643", "hsk6_1554", "Weak cross-domain: 再三 (repeatedly) vs 一向 (always/constancy) - distinct specific meaning, not a defensible near-synonym pair."),
    ("hsk6_1643", "hsk6_1571", "一-only: 再三 (repeatedly) vs 一同 (together) - no independent link."),
    ("hsk6_1643", "hsk6_1547", "一-only: 再三 (repeatedly) vs 一道 (together) - no independent link."),
]

ALL_REMOVALS = PHASE2_REMOVALS + PHASE3_REMOVALS

# ---------------------------------------------------------------------------
# PHASE 4 - hsk6_1220 status-only correction (no relationship change).
# ---------------------------------------------------------------------------
PHASE4_STATUS_CHANGES = [
    ("hsk6_1220", "needs_review", "selected",
     "All 4 relationships (书画, 念书, 书面, 书写) re-verified as "
     "defensible shared-character relationships to 书籍 with no D/E/F "
     "issue found; per the stated rule ('needs_review when fewer than 4 "
     "defensible relationships exist'), 4 defensible relationships means "
     "this should be 'selected', matching the pattern of every other "
     "record in the dataset. No relationship was changed."),
]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    baseline_checksum = sha256_of(MERGED_PATH)
    baseline_report = json.loads(BASELINE_REPORT_PATH.read_text(encoding="utf-8"))

    merged = json.loads(MERGED_PATH.read_text(encoding="utf-8"))
    by_id = {r["sourceId"]: r for r in merged}

    total_relationships_before = sum(len(r.get("relatedWordIds", [])) for r in merged)

    removed_log = []
    not_found_log = []

    # Group removals by sourceId for efficient application.
    removals_by_source: dict[str, list[tuple[str, str]]] = {}
    for sid, rel_id, reason in ALL_REMOVALS:
        removals_by_source.setdefault(sid, []).append((rel_id, reason))

    status_changes_log = []

    for sid, removals in removals_by_source.items():
        record = by_id.get(sid)
        if record is None:
            for rel_id, reason in removals:
                not_found_log.append({"sourceId": sid, "relatedWordId": rel_id, "issue": "sourceId not found in merged data"})
            continue

        before_related = list(record["relatedWordIds"])
        before_status = record["selectionStatus"]

        for rel_id, reason in removals:
            if rel_id not in record["relatedWordIds"]:
                not_found_log.append({"sourceId": sid, "relatedWordId": rel_id, "issue": "relatedWordId not present (already absent)"})
                continue

            idx = record["relatedWordIds"].index(rel_id)
            removed_word_id = record["relatedWordIds"].pop(idx)
            removed_reason_entry = None
            for i, rr in enumerate(record["selectionReasons"]):
                if rr["candidateId"] == rel_id:
                    removed_reason_entry = record["selectionReasons"].pop(i)
                    break

            removed_log.append({
                "sourceId": sid,
                "relatedWordId": removed_word_id,
                "originalReason": removed_reason_entry["reason"] if removed_reason_entry else None,
                "removalJustification": reason,
            })

        after_count = len(record["relatedWordIds"])
        new_status = record["selectionStatus"]
        if before_status == "selected" and after_count < SELECTED_MIN_COUNT:
            new_status = "needs_review"
        elif before_status == "needs_review" and after_count >= SELECTED_MIN_COUNT:
            # Should not occur from removals alone, but guard anyway.
            new_status = "selected"

        if new_status != before_status:
            record["selectionStatus"] = new_status
            status_changes_log.append({
                "sourceId": sid,
                "trigger": "relationship_count_dropped_below_threshold",
                "from": before_status,
                "to": new_status,
                "relatedCountBefore": len(before_related),
                "relatedCountAfter": after_count,
            })

    # --- Phase 4: hsk6_1220 status-only change ------------------------------
    phase4_log = []
    for sid, from_status, to_status, reason in PHASE4_STATUS_CHANGES:
        record = by_id.get(sid)
        if record is None:
            phase4_log.append({"sourceId": sid, "applied": False, "issue": "sourceId not found"})
            continue
        actual_from = record["selectionStatus"]
        if actual_from != from_status:
            phase4_log.append({
                "sourceId": sid, "applied": False,
                "issue": f"expected current status {from_status!r}, found {actual_from!r} - not applying blindly",
            })
            continue
        record["selectionStatus"] = to_status
        phase4_log.append({
            "sourceId": sid, "applied": True,
            "from": from_status, "to": to_status, "reason": reason,
        })

    total_relationships_after = sum(len(r.get("relatedWordIds", [])) for r in merged)

    # --- write refined merged artifact --------------------------------------
    MERGED_PATH.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    refined_checksum = sha256_of(MERGED_PATH)

    report = {
        "baselineChecksumSha256": baseline_checksum,
        "refinedChecksumSha256": refined_checksum,
        "baselineTotalRelationships": total_relationships_before,
        "refinedTotalRelationships": total_relationships_after,
        "relationshipsRemoved": len(removed_log),
        "statusChangesFromRemovals": len(status_changes_log),
        "phase4StatusChanges": phase4_log,
        "removed": removed_log,
        "notFound": not_found_log,
        "statusChangesFromRemovals_detail": status_changes_log,
        "proposedButNotAppliedReplacements": [
            {
                "sourceId": "hsk6_0031",
                "note": "No replacement proposed - the two remaining relationships (hsk6_0863 露1, hsk6_1324 透露) already correctly cover the lù sense; no additional candidate exists in the record's own data.",
            },
            {
                "sourceId": "hsk6_0387",
                "note": "No new replacement needed - hsk6_1128 (correct sàn-reading 散) was already present in this record before refinement.",
            },
            {
                "sourceId": "hsk6_1741",
                "note": "Record now has 0 relationships; no replacement candidate exists in the record's own data (it only ever had the one, now-removed, relationship).",
            },
            {
                "sourceId": "hsk6_1349",
                "note": "Record now has 0 relationships; no replacement candidate exists in the record's own data.",
            },
        ],
        "remainingUnresolvedIssues": [
            "落 (hsk6_0810) là-vs-luò upstream production-data labeling question - not touched, deferred per instructions.",
            "眼光 (hsk6_1515) -> 眉毛/盲人 borderline sense concern - not touched, deferred per instructions (not in the Phase 2 explicit list).",
            "狼 (hsk6_0820) -> 狗 (hsk1_064) borderline radical-only concern - not touched, deferred (not in the Phase 2 explicit list; only 猫 and 猴子 were explicitly listed for removal).",
            "狼 (hsk6_0820) -> 狮子 (hsk6_1180) category-based reasoning retained - not touched, deferred (not in the Phase 2 explicit list).",
        ],
    }

    REFINEMENT_REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Baseline checksum:  {baseline_checksum}")
    print(f"Refined checksum:   {refined_checksum}")
    print(f"Relationships before: {total_relationships_before}")
    print(f"Relationships after:  {total_relationships_after}")
    print(f"Removed:              {len(removed_log)}")
    print(f"Status changes (from removals): {len(status_changes_log)}")
    print(f"Phase 4 status changes applied: {sum(1 for x in phase4_log if x.get('applied'))}")
    print(f"Not-found anomalies: {len(not_found_log)}")
    print(f"Refinement report: {REFINEMENT_REPORT_PATH}")


if __name__ == "__main__":
    main()
