"""
Stroke Count Pass 03 — step 1: pre-integration manifest.

Read-only. Records a full, machine-readable snapshot of the 6 production
files BEFORE any strokeCount write, so the integration script and the
post-integration validator can prove exactly what changed.
"""
import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent
LEVELS = [1, 2, 3, 4, 5, 6]

TRACKED_FIELDS = [
    "id", "word", "pinyin", "meaningVi", "examples", "relatedWordIds",
    "humanVerified", "groundTruth", "verificationStatus", "characterIds",
    "strokeCount",
]

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest = {"levels": {}}
    total = 0
    strokecount_key_present = 0
    strokecount_nonnull = 0

    for lvl in LEVELS:
        path = REPO_ROOT / "data" / "hsk" / f"hsk{lvl}" / f"hsk{lvl}_vocabulary_production.json"
        raw_bytes = path.read_bytes()
        records = json.loads(raw_bytes.decode("utf-8"))
        total += len(records)

        record_snapshots = []
        for r in records:
            snap = {f: r.get(f, "__ABSENT__") for f in TRACKED_FIELDS}
            record_snapshots.append(snap)
            if "strokeCount" in r:
                strokecount_key_present += 1
                if r["strokeCount"] is not None:
                    strokecount_nonnull += 1

        manifest["levels"][str(lvl)] = {
            "path": str(path.relative_to(REPO_ROOT)),
            "sha256": hashlib.sha256(raw_bytes).hexdigest(),
            "byteLength": len(raw_bytes),
            "recordCount": len(records),
            "records": record_snapshots,
        }

    manifest["totalRecords"] = total
    manifest["strokeCountKeyPresentCount"] = strokecount_key_present
    manifest["strokeCountNonNullCount"] = strokecount_nonnull

    (OUT_DIR / "pre_integration_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"totalRecords={total}")
    for lvl in LEVELS:
        m = manifest["levels"][str(lvl)]
        print(f"HSK{lvl}: records={m['recordCount']} sha256={m['sha256']}")
    print(f"strokeCountKeyPresentCount={strokecount_key_present} (out of {total})")
    print(f"strokeCountNonNullCount={strokecount_nonnull}")

if __name__ == "__main__":
    main()
