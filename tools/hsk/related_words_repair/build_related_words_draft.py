"""
Related Words Pass 02 -- draft repair builder.

Reads only:
    data/hsk/hsk{1..6}/hsk{N}_vocabulary_production.json (read-only)
    data/hsk/hsk1/hsk1_related_words_selection_v2.json
    data/hsk/hsk{2,3,4,5}/hsk{N}_related_words_selection.json
    (HSK6 is intentionally NOT read as a repair source -- see module
    docstring in the final report: HSK6's own "selected" tier already
    matches current production exactly, i.e. it is already fully
    integrated under this exact same rule from a separate prior pass.
    Touching it here would risk double-applying or conflicting with
    that already-correct state.)

Writes only:
    tools/hsk/related_words_repair/*.json (this directory)

Never touches production. This script only proposes; a separate
integration step (run only after human review) applies the draft.

Rule (per approved product decision):
    IF production relatedWordIds is non-empty: leave completely unchanged.
    ELSE IF a "selected"-status source record exists with at least one
        valid (existing) target ID: populate with those valid target IDs,
        in the exact order the source lists them (the source's own order
        reflects its own generation-time ranking; no reordering is
        introduced here -- see ORDERING note below).
    ELSE: leave as [].
    NEVER integrate "needs_review".
    NEVER add an edge whose target ID does not exist in production.
    NEVER use "shares a character" as a rule -- only the source's own
        semantic selectionReasons-backed choices are used.

ORDERING: the source selection files do not document an explicit
"this is a relatedness ranking" contract (the sibling candidate-pool
file's own docstring explicitly disclaims that pool position is a
ranking); however every source record's relatedWordIds array is already
a finished, deliberate list produced by the selection step (not a
candidate pool), so it is treated as the intended order and preserved
verbatim, byte-for-byte, rather than re-sorting it by any other key.
This keeps the transformation the smallest possible change and keeps
the process trivially deterministic (same input -> same output, since
no new sort/tie-break logic is introduced at all).
"""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent

LEVELS = [1, 2, 3, 4, 5, 6]
SOURCE_PATHS = {
    1: REPO_ROOT / "data" / "hsk" / "hsk1" / "hsk1_related_words_selection_v2.json",
    2: REPO_ROOT / "data" / "hsk" / "hsk2" / "hsk2_related_words_selection.json",
    3: REPO_ROOT / "data" / "hsk" / "hsk3" / "hsk3_related_words_selection.json",
    4: REPO_ROOT / "data" / "hsk" / "hsk4" / "hsk4_related_words_selection.json",
    5: REPO_ROOT / "data" / "hsk" / "hsk5" / "hsk5_related_words_selection.json",
    # 6: intentionally absent -- see module docstring.
}


def load_production():
    per_level = {}
    all_by_id = {}
    for lvl in LEVELS:
        path = REPO_ROOT / "data" / "hsk" / f"hsk{lvl}" / f"hsk{lvl}_vocabulary_production.json"
        recs = json.loads(path.read_text(encoding="utf-8"))
        per_level[lvl] = recs
        for r in recs:
            all_by_id[r["id"]] = r
    return per_level, all_by_id


def main():
    per_level_production, all_production = load_production()

    changes = []  # proposed changes: records currently empty that gain data
    preserved_nonempty = []  # records already non-empty, explicitly not touched
    needs_review_excluded = []  # records whose only available source is needs_review
    invalid_target_excluded = []  # selected edges whose target id doesn't exist (would be dropped, but see check below)
    no_source_available = []  # records with no selection source at all (HSK6, or missing sourceId)

    for lvl in LEVELS:
        sel_by_id = {}
        if lvl in SOURCE_PATHS:
            sel = json.loads(SOURCE_PATHS[lvl].read_text(encoding="utf-8"))
            sel_by_id = {r["sourceId"]: r for r in sel}

        for rec in per_level_production[lvl]:
            rid = rec["id"]
            current = rec.get("relatedWordIds") or []

            if current:
                preserved_nonempty.append(rid)
                continue

            sel_rec = sel_by_id.get(rid)
            if sel_rec is None:
                no_source_available.append(rid)
                continue

            status = sel_rec.get("selectionStatus")
            if status != "selected":
                needs_review_excluded.append({"id": rid, "word": rec["word"], "status": status})
                continue

            proposed = sel_rec.get("relatedWordIds") or []
            valid_targets = [t for t in proposed if t in all_production]
            dropped = [t for t in proposed if t not in all_production]
            if dropped:
                invalid_target_excluded.append({"id": rid, "word": rec["word"], "droppedTargets": dropped})

            if not valid_targets:
                continue  # nothing valid to add; stays []

            # Look up reasons for the surviving valid targets only.
            reasons_by_target = {
                r["candidateId"]: r["reason"]
                for r in sel_rec.get("selectionReasons", [])
                if r.get("candidateId") in valid_targets
            }

            added_words = [all_production[t]["word"] for t in valid_targets]
            target_levels = [
                all_production[t].get("hskLevels") or [int(t.split("_")[0].replace("hsk", ""))]
                for t in valid_targets
            ]

            changes.append({
                "id": rid,
                "word": rec["word"],
                "hskLevel": lvl,
                "oldRelatedWordIds": current,
                "newRelatedWordIds": valid_targets,
                "addedIds": valid_targets,
                "addedWords": added_words,
                "addedHskLevels": target_levels,
                "selectionReasons": [
                    {"candidateId": t, "word": all_production[t]["word"], "reason": reasons_by_target.get(t, "")}
                    for t in valid_targets
                ],
                "sourceFile": str(SOURCE_PATHS[lvl].relative_to(REPO_ROOT)),
                "selectionStatus": status,
            })

    summary = {
        "recordsChanged": len(changes),
        "totalEdgesAdded": sum(len(c["addedIds"]) for c in changes),
        "recordsPreservedNonEmpty": len(preserved_nonempty),
        "recordsExcludedNeedsReview": len(needs_review_excluded),
        "recordsWithInvalidTargetDropped": len(invalid_target_excluded),
        "recordsWithNoSourceAvailable": len(no_source_available),
    }

    draft = {"summary": summary, "changes": changes}
    (OUT_DIR / "related_words_draft.json").write_text(
        json.dumps(draft, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    review = {
        "needsReviewExcluded": needs_review_excluded,
        "invalidTargetDropped": invalid_target_excluded,
        "noSourceAvailable": no_source_available,
        "preservedNonEmptyIds": preserved_nonempty,
    }
    (OUT_DIR / "related_words_review.json").write_text(
        json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
