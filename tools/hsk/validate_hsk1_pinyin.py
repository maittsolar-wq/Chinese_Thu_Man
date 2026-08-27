import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    ROOT
    / "data"
    / "hsk"
    / "hsk1"
    / "hsk1_vocabulary_with_meanings_draft.json"
)

REPORT_FILE = (
    ROOT
    / "data"
    / "hsk"
    / "hsk1"
    / "hsk1_pinyin_validation.json"
)


# ============================================================
# CONFIG
# ============================================================

VALID_CHARS = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "üÜ"
    "āáǎàēéěèīíǐìōóǒòūúǔù"
    "ǖǘǚǜ"
    " "
    "'’/"
    "-"
)

TONE_MARKS = set(
    "āáǎàēéěèīíǐìōóǒòūúǔù"
    "ǖǘǚǜ"
)


# Basic Pinyin syllable pattern.
SYLLABLE_RE = re.compile(
    r"^[a-züÜ"
    r"āáǎàēéěèīíǐìōóǒòūúǔù"
    r"ǖǘǚǜ"
    r"]+"
    r"(?:[1-5])?$",
    re.IGNORECASE,
)


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_apostrophe(text):
    """
    Normalize curly apostrophe to ASCII apostrophe
    for validation only.

    Example:
        nǚ’ér -> nǚ'ér

    Dataset itself is NOT modified.
    """

    return text.replace("’", "'")


# ============================================================
# PINYIN VALIDATION
# ============================================================

def is_valid_syllable(syllable):
    """
    Validate ONE Pinyin syllable.

    Examples:
        nǚ
        ér
        bù
        ba
        de
    """

    if not syllable:
        return False

    syllable = normalize_apostrophe(
        syllable.strip()
    )

    if not syllable:
        return False

    # Numeric tone support:
    # ma1, ma2, ma3, ma4, ma5
    if syllable[-1:].isdigit():

        if syllable[-1] not in "12345":
            return False

        syllable = syllable[:-1]

    return bool(
        SYLLABLE_RE.match(syllable)
    )


def validate_pinyin_token(token):
    """
    Validate one Pinyin token.

    Supports:

        bàba
        nǚ'ér
        nǚ’ér
        shéi/shuí

    Important:
    Apostrophe separates syllables.
    Slash separates pronunciation alternatives.
    """

    token = normalize_apostrophe(
        token.strip()
    )

    if not token:
        return False, []


    invalid = []


    # --------------------------------------------------------
    # Pronunciation alternatives
    #
    # shéi/shuí
    # --------------------------------------------------------

    alternatives = [
        x.strip()
        for x in token.split("/")
        if x.strip()
    ]


    if not alternatives:
        return False, [token]


    # --------------------------------------------------------
    # Validate every pronunciation alternative
    # --------------------------------------------------------

    for alternative in alternatives:

        # ----------------------------------------------------
        # Apostrophe separates syllables.
        #
        # nǚ'ér
        # ↓
        # nǚ
        # ér
        # ----------------------------------------------------

        syllables = [
            x.strip()
            for x in alternative.split("'")
            if x.strip()
        ]


        if not syllables:
            invalid.append(alternative)
            continue


        for syllable in syllables:

            if not is_valid_syllable(
                syllable
            ):
                invalid.append(
                    syllable
                )


    return (
        len(invalid) == 0,
        invalid
    )


# ============================================================
# NEUTRAL TONE
# ============================================================

def is_unmarked_syllable(syllable):

    syllable = syllable.strip()

    if not syllable:
        return False

    # Numeric tone is explicitly marked.
    if syllable[-1:].isdigit():
        return False

    # Tone mark exists.
    if any(
        ch in TONE_MARKS
        for ch in syllable
    ):
        return False

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    if not DATA_FILE.exists():

        raise SystemExit(
            f"Missing dataset: {DATA_FILE}"
        )


    data = json.loads(
        DATA_FILE.read_text(
            encoding="utf-8"
        )
    )


    if not isinstance(data, list):

        raise RuntimeError(
            "Expected merged dataset "
            "to be a JSON array."
        )


    errors = []

    neutral_candidates = []


    # ========================================================
    # RECORD VALIDATION
    # ========================================================

    for record in data:

        record_id = record.get(
            "id",
            ""
        )

        word = str(
            record.get(
                "word",
                ""
            ) or ""
        )

        pinyin = str(
            record.get(
                "pinyin",
                ""
            ) or ""
        ).strip()


        # ----------------------------------------------------
        # Missing Pinyin
        # ----------------------------------------------------

        if not pinyin:

            errors.append({
                "id": record_id,
                "word": word,
                "issue": "missing_pinyin"
            })

            continue


        # ----------------------------------------------------
        # Normalize only for validation
        # ----------------------------------------------------

        normalized_pinyin = (
            normalize_apostrophe(
                pinyin
            )
        )


        # ----------------------------------------------------
        # Character validation
        # ----------------------------------------------------

        bad_chars = sorted({
            ch
            for ch in normalized_pinyin
            if ch not in VALID_CHARS
        })


        if bad_chars:

            errors.append({
                "id": record_id,
                "word": word,
                "pinyin": pinyin,
                "issue": "invalid_pinyin_characters",
                "invalidCharacters": bad_chars
            })

            continue


        # ----------------------------------------------------
        # Validate each space-separated group
        # ----------------------------------------------------

        invalid_syllables = []


        for token in re.split(
            r"\s+",
            normalized_pinyin
        ):

            if not token:
                continue


            ok, invalid = (
                validate_pinyin_token(
                    token
                )
            )


            if not ok:

                invalid_syllables.extend(
                    invalid
                )


        if invalid_syllables:

            errors.append({
                "id": record_id,
                "word": word,
                "pinyin": pinyin,
                "issue": "invalid_pinyin_format",
                "invalidSyllables": invalid_syllables
            })

            continue


        # ====================================================
        # NEUTRAL / UNMARKED TONE CANDIDATES
        # ====================================================

        for token in re.split(
            r"\s+",
            normalized_pinyin
        ):

            if not token:
                continue


            # Check every pronunciation alternative.
            for alternative in token.split("/"):

                alternative = (
                    alternative.strip()
                )

                if not alternative:
                    continue


                # Apostrophe-separated syllables.
                syllables = [
                    x.strip()
                    for x in alternative.split("'")
                    if x.strip()
                ]


                for syllable in syllables:

                    if is_unmarked_syllable(
                        syllable
                    ):

                        neutral_candidates.append({
                            "id": record_id,
                            "word": word,
                            "pinyin": pinyin,
                            "candidate": syllable,
                            "issue": "neutral_or_unmarked_tone"
                        })


    # ========================================================
    # DUPLICATE WORDS
    # ========================================================

    words = [
        str(
            r.get(
                "word",
                ""
            ) or ""
        )
        for r in data
    ]


    duplicate_words = sorted({
        word
        for word in words
        if word
        and words.count(word) > 1
    })


    for word in duplicate_words:

        errors.append({
            "word": word,
            "issue": "duplicate_normalized_word"
        })


    # ========================================================
    # STATUS
    # ========================================================

    status = (
        "PASS"
        if not errors
        else "FAIL"
    )


    report = {

        "dataset": str(
            DATA_FILE
        ),

        "status": status,

        "recordCount": len(data),

        "summary": {

            "missingPinyin": sum(
                1
                for e in errors
                if e.get("issue")
                == "missing_pinyin"
            ),

            "invalidPinyin": sum(
                1
                for e in errors
                if e.get("issue")
                in {
                    "invalid_pinyin_characters",
                    "invalid_pinyin_format"
                }
            ),

            "neutralOrUnmarkedToneCandidates":
                len(
                    neutral_candidates
                ),

            "duplicateNormalizedWords":
                len(
                    duplicate_words
                )
        },

        "errors": errors,

        "neutralOrUnmarkedToneCandidates":
            neutral_candidates,

        "duplicateNormalizedWords":
            duplicate_words,

        "notes": [

            "Pinyin dataset was not modified.",

            "Compound Pinyin without spaces "
            "is accepted.",

            "Apostrophe-separated syllables "
            "such as nǚ'ér are accepted.",

            "Curly apostrophe nǚ’ér is accepted "
            "as a source spelling variation.",

            "Slash pronunciation alternatives "
            "such as shéi/shuí are accepted.",

            "Neutral/unmarked tones are "
            "informational candidates only."
        ]
    }


    # ========================================================
    # WRITE REPORT
    # ========================================================

    REPORT_FILE.write_text(

        json.dumps(
            report,
            ensure_ascii=False,
            indent=2
        ),

        encoding="utf-8"
    )


    # ========================================================
    # TERMINAL OUTPUT
    # ========================================================

    print("=" * 60)
    print(
        "HSK 1 PINYIN VALIDATION v4"
    )
    print("=" * 60)

    print(
        f"Records:              "
        f"{len(data)}/300"
    )

    print(
        f"Missing Pinyin:       "
        f"{report['summary']['missingPinyin']}"
    )

    print(
        f"Invalid Pinyin:       "
        f"{report['summary']['invalidPinyin']}"
    )

    print(
        f"Neutral/unmarked:     "
        f"{len(neutral_candidates)}"
    )

    print(
        f"Duplicate words:      "
        f"{len(duplicate_words)}"
    )

    print(
        f"Status:               "
        f"{status}"
    )

    print(
        f"Report:               "
        f"{REPORT_FILE}"
    )


    # ========================================================
    # ERRORS
    # ========================================================

    if errors:

        print("\nERRORS:")

        for item in errors[:30]:

            print(
                f"  ! "
                f"{item.get('id', '')} | "
                f"{item.get('word', '')} | "
                f"{item.get('pinyin', '')} | "
                f"{item.get('issue', '')}"
            )


    # ========================================================
    # NEUTRAL TONE
    # ========================================================

    if neutral_candidates:

        print(
            "\nNEUTRAL / UNMARKED "
            "TONE CANDIDATES:"
        )

        for item in neutral_candidates[:30]:

            print(
                f"  ? "
                f"{item['id']} | "
                f"{item['word']} | "
                f"{item['pinyin']} | "
                f"{item['candidate']}"
            )


    print(
        "\nPinyin data was NOT modified."
    )


if __name__ == "__main__":
    main()