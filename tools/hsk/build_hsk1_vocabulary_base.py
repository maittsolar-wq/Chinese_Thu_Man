import csv
import io
import json
import re
import urllib.request
from pathlib import Path

SOURCE_URL = (
    "https://raw.githubusercontent.com/profesorm/hsk30/"
    "main/data/hsk_vocabulary.csv"
)

SOURCE_REPOSITORY = "profesorm/hsk30"
SOURCE_FILE = "data/hsk_vocabulary.csv"

ROOT = Path(__file__).resolve().parents[2]

OUT = ROOT / "data" / "hsk" / "hsk1"

EXPECTED_HSK1_COUNT = 300


# ============================================================
# SOURCE
# ============================================================

def fetch():
    print("Downloading HSK 3.0 vocabulary source...")
    print(f"Source: {SOURCE_URL}")

    request = urllib.request.Request(
        SOURCE_URL,
        headers={
            "User-Agent": "Chinese-Thu-Man-HSK-Data-Builder/1.0"
        }
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read().decode("utf-8-sig")

    rows = list(csv.DictReader(io.StringIO(data)))

    if not rows:
        raise RuntimeError(
            "Source CSV is empty or could not be parsed."
        )

    required_columns = {
        "type",
        "levelName",
        "word",
        "pinyin",
        "cixing",
        "sort",
    }

    actual_columns = set(rows[0].keys())
    missing_columns = required_columns - actual_columns

    if missing_columns:
        raise RuntimeError(
            "Source CSV is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    print(f"Source rows loaded: {len(rows)}")

    return rows


# ============================================================
# HSK LEVELS
# ============================================================

def parse_hsk_levels(level_name):
    mapping = {
        "一级": 1,
        "二级": 2,
        "三级": 3,
        "四级": 4,
        "五级": 5,
        "六级": 6,
    }

    levels = []

    for label, number in mapping.items():
        if label in level_name:
            levels.append(number)

    return sorted(set(levels))


# ============================================================
# WORD NORMALIZATION
# ============================================================

def normalize_word(source_word):
    """
    Remove source entry markers such as:

        本1 -> 本
        本2 -> 本
        点1 -> 点
        和1 -> 和

    Only removes ONE trailing digit when the remaining
    content contains Chinese characters.

    The original source value is preserved as `sourceWord`.
    """

    source_word = source_word.strip()

    match = re.match(
        r"^(.*?)([1-9])$",
        source_word
    )

    if not match:
        return source_word

    base_word = match.group(1)

    if re.search(r"[\u3400-\u9fff]", base_word):
        return base_word

    return source_word


# ============================================================
# POS
# ============================================================

def normalize_pos(cixing):
    return [
        x.strip()
        for x in cixing.split("、")
        if x.strip() and not x.startswith("（")
    ]


# ============================================================
# BUILD HSK 1
# ============================================================

def build():

    rows = fetch()

    # --------------------------------------------------------
    # Select HSK 1
    # --------------------------------------------------------

    source_rows = [
        r
        for r in rows
        if r.get("type", "").strip() == "1"
        and r.get("levelName", "").strip().startswith("一级")
    ]

    print(f"HSK 1 source rows found: {len(source_rows)}")

    if len(source_rows) != EXPECTED_HSK1_COUNT:
        raise RuntimeError(
            f"Expected exactly {EXPECTED_HSK1_COUNT} HSK 1 records, "
            f"got {len(source_rows)}."
        )

    records = []
    normalization_changes = []

    # --------------------------------------------------------
    # Build records
    # --------------------------------------------------------

    for index, row in enumerate(source_rows, start=1):

        source_word = row.get("word", "").strip()
        pinyin = row.get("pinyin", "").strip()
        level_name = row.get("levelName", "").strip()
        part_of_speech = row.get("cixing", "").strip()

        if not source_word:
            raise RuntimeError(
                f"Empty word at source row {index}"
            )

        if not pinyin:
            raise RuntimeError(
                f"Empty Pinyin for word {source_word}"
            )

        word = normalize_word(source_word)

        if word != source_word:
            normalization_changes.append({
                "sourceWord": source_word,
                "normalizedWord": word,
                "sourceSort": int(row["sort"])
            })

        hsk_levels = parse_hsk_levels(level_name)

        if not hsk_levels:
            raise RuntimeError(
                f"Could not parse HSK levels for word: {source_word}"
            )

        introduced_level = min(hsk_levels)

        source_sort = int(row["sort"])

        records.append({
            "id": f"hsk1_{index:03d}",

            # Clean user-facing word.
            "word": word,

            # Original source entry for audit.
            "sourceWord": source_word,

            "pinyin": pinyin,

            "pinyinNumeric": None,

            "meaningVi": [],

            "introducedLevel": introduced_level,

            "hskLevels": hsk_levels,

            "partOfSpeechSource": part_of_speech,

            "partOfSpeech": normalize_pos(part_of_speech),

            "sourceSort": source_sort,

            "sourceLevelName": level_name,

            "sourceAdditionalLevels": re.findall(
                r"（([^）]+)）",
                level_name
            ),

            "strokeCount": None,

            "characterIds": [],

            "relatedWordIds": [],

            "exampleIds": [],

            "audio": {
                "wordUrl": None,
                "exampleUrl": None
            },

            "_source": {
                "sourceId": SOURCE_REPOSITORY,
                "sourceFile": SOURCE_FILE,
                "sourceSort": source_sort,
                "sourceLevelName": level_name
            }
        })

    # ========================================================
    # VALIDATION
    # ========================================================

    errors = []

    ids = [r["id"] for r in records]
    words = [r["word"] for r in records]

    if len(records) != EXPECTED_HSK1_COUNT:
        errors.append(
            f"recordCount={len(records)}"
        )

    if len(ids) != len(set(ids)):
        errors.append("duplicate IDs")

    if len(words) != len(set(words)):
        duplicates = sorted(
            {
                word
                for word in words
                if words.count(word) > 1
            }
        )

        errors.append(
            "duplicate Chinese words: "
            + ", ".join(duplicates)
        )

    if any(not r["word"] for r in records):
        errors.append("empty Chinese word")

    if any(not r["pinyin"] for r in records):
        errors.append("empty Pinyin")

    if any(
        r["introducedLevel"] != 1
        for r in records
    ):
        errors.append(
            "one or more records have introducedLevel != 1"
        )

    expected_ids = [
        f"hsk1_{i:03d}"
        for i in range(
            1,
            EXPECTED_HSK1_COUNT + 1
        )
    ]

    if ids != expected_ids:
        errors.append(
            "IDs are not sequential from "
            "hsk1_001 to hsk1_300"
        )

    if errors:
        raise RuntimeError(
            "Validation failed:\n- "
            + "\n- ".join(errors)
        )

    # ========================================================
    # OUTPUT
    # ========================================================

    OUT.mkdir(
        parents=True,
        exist_ok=True
    )

    vocabulary_json = (
        OUT / "hsk1_vocabulary_base.json"
    )

    vocabulary_json.write_text(
        json.dumps(
            records,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    vocabulary_csv = (
        OUT / "hsk1_vocabulary_base.csv"
    )

    with vocabulary_csv.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "id",
            "word",
            "sourceWord",
            "pinyin",
            "introducedLevel",
            "hskLevels",
            "partOfSpeechSource",
            "sourceSort",
            "sourceLevelName"
        ])

        for r in records:

            writer.writerow([
                r["id"],
                r["word"],
                r["sourceWord"],
                r["pinyin"],
                r["introducedLevel"],
                ",".join(
                    map(str, r["hskLevels"])
                ),
                r["partOfSpeechSource"],
                r["sourceSort"],
                r["sourceLevelName"]
            ])

    # ========================================================
    # NORMALIZATION REPORT
    # ========================================================

    normalization_report = {
        "status": "SUCCESS",
        "recordCount": len(records),
        "normalizedCount": len(normalization_changes),
        "changes": normalization_changes
    }

    report_file = (
        OUT / "hsk1_normalization_report.json"
    )

    report_file.write_text(
        json.dumps(
            normalization_report,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    # ========================================================
    # SUCCESS
    # ========================================================

    print()
    print("=" * 60)
    print("SUCCESS")
    print("=" * 60)

    print(
        f"HSK 1 records: {len(records)}"
    )

    print(
        f"Normalized source entries: "
        f"{len(normalization_changes)}"
    )

    if normalization_changes:
        print()
        print("Normalization examples:")

        for item in normalization_changes[:20]:
            print(
                f"  {item['sourceWord']} "
                f"-> {item['normalizedWord']}"
            )

    print()
    print(f"Output folder: {OUT}")

    print()
    print("Generated files:")

    print(
        f"  - {vocabulary_json.name}"
    )

    print(
        f"  - {vocabulary_csv.name}"
    )

    print(
        f"  - {report_file.name}"
    )

    print()
    print("Validation:")
    print("  ✓ Exactly 300 HSK 1 records")
    print("  ✓ Unique IDs")
    print("  ✓ Unique normalized Chinese words")
    print("  ✓ Non-empty Chinese words")
    print("  ✓ Non-empty Pinyin")
    print("  ✓ HSK level mapping")
    print("  ✓ Source ordering")
    print("  ✓ Sequential IDs")
    print("  ✓ Source entry markers normalized")

    print()
    print(
        "Status: SOURCE BASE ONLY - NOT PRODUCTION"
    )

    print("=" * 60)


if __name__ == "__main__":
    build()