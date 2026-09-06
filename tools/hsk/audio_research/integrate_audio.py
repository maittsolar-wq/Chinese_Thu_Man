"""
AUDIO PASS 02 -- production integration.

Populates VocabularyWord.audio.wordUrl for the 5377 approved matched records
(from tools/hsk/audio_research/mapping_draft.json) using stable relative
paths of the form /audio/cedict-tts/<filename>.mp3, pointing at the verified
files already imported into app/public/audio/cedict-tts/.

Does NOT touch: audio.exampleUrl, examples, relatedWordIds, strokeCount,
characterIds, humanVerified, verification fields, IDs, ordering, or any other
field. The 19 "missing" and 4 "needs_review" records are left with
audio.wordUrl = null (HSK1-5: field already exists as null, untouched;
HSK6: gets an explicit {wordUrl: null, exampleUrl: null} object like every
other HSK6 record, since HSK6 previously had no `audio` key at all).

Usage:
  python integrate_audio.py --dry-run   (default; writes a report, no file changes)
  python integrate_audio.py --apply     (writes the 6 production JSON files)
"""
import json, argparse, sys, os

REPO = "d:/Chinese_Thu_Man"
LEVELS = [1, 2, 3, 4, 5, 6]

def serialize_like_source(records):
    text = json.dumps(records, indent=2, ensure_ascii=False)
    return text.replace("\n", "\r\n")

def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    mapping = json.load(open(f"{REPO}/tools/hsk/audio_research/mapping_draft.json", encoding="utf-8"))
    matched_by_id = {r["id"]: r for r in mapping["records"] if r["mappingStatus"] == "matched"}
    unresolved_ids = {r["id"] for r in mapping["records"] if r["mappingStatus"] != "matched"}

    print(f"mapping: {len(matched_by_id)} matched, {len(unresolved_ids)} unresolved (missing/needs_review)")

    # Fail-closed: every matched record's referenced asset must exist on disk.
    audio_dir = f"{REPO}/app/public/audio/cedict-tts"
    on_disk = set(os.listdir(audio_dir))
    broken = []
    for rid, rec in matched_by_id.items():
        fname = rec["audioKeyPath"].split("/")[-1]
        if fname not in on_disk:
            broken.append((rid, fname))
    if broken:
        print(f"FATAL: {len(broken)} matched records reference a missing asset file. Aborting.")
        for b in broken[:20]:
            print("  ", b)
        sys.exit(1)
    print(f"asset integrity OK: all {len(matched_by_id)} matched records' files exist on disk ({len(on_disk)} files total).")

    total_touched = 0
    total_null_confirmed = 0
    per_level_matched = {}

    for lvl in LEVELS:
        path = f"{REPO}/data/hsk/hsk{lvl}/hsk{lvl}_vocabulary_production.json"
        records = json.load(open(path, encoding="utf-8"))
        level_matched = 0
        for rec in records:
            rid = rec["id"]
            if rid in matched_by_id:
                fname = matched_by_id[rid]["audioKeyPath"].split("/")[-1]
                url = f"/audio/cedict-tts/{fname}"
                if "audio" not in rec or rec["audio"] is None:
                    rec["audio"] = {"wordUrl": None, "exampleUrl": None}
                rec["audio"]["wordUrl"] = url
                level_matched += 1
                total_touched += 1
            elif rid in unresolved_ids:
                if "audio" not in rec or rec["audio"] is None:
                    rec["audio"] = {"wordUrl": None, "exampleUrl": None}
                else:
                    rec["audio"]["wordUrl"] = None
                total_null_confirmed += 1
            else:
                # Should not happen -- every production ID must appear in the
                # mapping artifact (it was generated from these exact files).
                print(f"FATAL: production id {rid} not found in mapping artifact. Aborting.")
                sys.exit(1)
        per_level_matched[lvl] = level_matched
        print(f"HSK{lvl}: {level_matched} records given wordUrl (of {len(records)} total)")

        if args.apply:
            out_text = serialize_like_source(records)
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(out_text)

    print(f"\nTOTAL matched-and-written: {total_touched}")
    print(f"TOTAL confirmed-null (missing/needs_review): {total_null_confirmed}")
    print("APPLIED" if args.apply else "DRY RUN -- no files written")

if __name__ == "__main__":
    main()
