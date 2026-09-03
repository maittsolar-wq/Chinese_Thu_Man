"""P5.4.1 -- HSK1 Related-Word CANDIDATE POOL generation (pilot).

This script produces a *candidate pool*, not a final selection. It never
assigns "selected"/"needs_review" status, never writes relatedWordIds to
production, and never invents vocabulary or IDs.

Design response to the HSK6 candidate-pool-provenance limitation (see
P5.2): HSK6's related-word artifact went straight from "relationship" to
"selection status" with no persisted intermediate candidate pool, so it
was impossible to later answer "what candidates were even considered for
word X?". This script's whole purpose is to make that question
answerable for HSK1, permanently, by persisting every candidate this
generation pass considered defensible, tagged with the explicit rule
category that justifies it.

METHODOLOGY NOTE (read before extending): every relationship below was
authored by direct linguistic review of the full, exact 300-word HSK1
production list (not inferred, not templated from a generic algorithm,
not guessed). Each entry cites one of a small, explicit set of rule
categories (RULE_CATEGORIES below) chosen specifically to exclude the
failure modes this project has already learned to avoid:
  - pure character-sharing with no synchronic compositional meaning
    (rejected explicitly for cases like a_dai/da-jia "everyone" vs
    "big+family" -- a false-friend character overlap, NOT included)
  - generic topic grouping (rejected for e.g. "all transportation
    words", "all time-unit words" as blanket sets)
  - numeral-family padding (the exact anti-pattern identified and
    removed during the HSK6 P3.5.5 refinement -- deliberately NOT
    repeated here; only one narrow, grammatically explicit numeral
    relationship is included: er4/liang3 register alternation)

SCOPE DECISION: this pilot's candidates are HSK1-internal only (every
candidate ID belongs to hsk1_vocabulary_production.json). Cross-level
candidates (HSK2-6) are explicitly in-scope per the project's approved
CROSS_LEVEL_HSK1_TO_HSK6 policy, but generating them defensibly requires
the same close, word-by-word review of the *target* level's exact word
list that this script gives HSK1 -- doing that carefully for five more
levels is out of scope for a pilot. This is a documented scope choice,
not a silently-dropped requirement; see the P5.4.1 report.

Usage:
    python generate_hsk1_related_word_candidates_p541.py
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HSK1_PATH = REPO_ROOT / "data" / "hsk" / "hsk1" / "hsk1_vocabulary_production.json"
OUTPUT_PATH = REPO_ROOT / "tools" / "hsk" / "hsk1_related_words_candidate_pool.json"

POOL_VERSION = "p541-v1"
RULES_VERSION = "hsk1-candidate-rules-v1"
MAX_CANDIDATES_PER_RECORD = 20

RULE_CATEGORIES = {
    "ANTONYM": "Canonical, unambiguous opposite-meaning pair (e.g. da4/xiao3).",
    "NEAR_SYNONYM": "Closely related meaning, commonly explicitly contrasted in HSK1 teaching (e.g. hui4/neng2/ke3yi3).",
    "MORPHOLOGICAL_SUFFIX": "Shares a productive bound grammatical suffix/allomorph (e.g. pronoun + men).",
    "COMPOSITIONAL_COMPOUND": "One word is directly formed by compounding with the other (e.g. du2 + shu1 = du2shu1).",
    "COMPOUND_FAMILY": "Shares a productive head/root morpheme forming a recognized HSK1 word-formation family (e.g. hao3+chi1/kan4/ting1/wan2r).",
    "CLOSED_PARADIGM": "Member of the same small, closed grammatical or semantic paradigm (e.g. zuo2tian1/jin1tian1/ming2tian1).",
    "FUNCTIONAL_CONTEXT": "Real-world functional, collocational, or discourse-adjacency relationship (e.g. xie4xie/bu2ke4qi, chuan1/yi1fu).",
    "GENDER_PAIR": "Male/female counterpart within a defined lexical pair (e.g. nan2peng2you/nu:3peng2you).",
    "CONTRAST": "Age/role contrast pair within a closed kinship set (e.g. ge1ge/di4di).",
}

# ---------------------------------------------------------------------------
# Curated relationship pairs: (id_a, id_b, category, note)
#
# `note` is a short human-authored justification kept for audit purposes;
# it is NOT copied verbatim into the artifact's per-candidate "reason"
# (that is templated from `category` + the paired word, see build_reason()
# below) -- `note` exists so a reviewer reading this script can see why
# each pair was judged defensible without re-deriving it from scratch.
#
# Every pair here was checked against the full HSK1 wordlist. IDs are
# hsk1_NNN as they appear in production; validated again at generation
# time against the loaded production ID set (fail-closed if any is wrong).
# ---------------------------------------------------------------------------
PAIRS = [
    # -- numerals: single narrow, grammatically explicit exception only --
    ("hsk1_049", "hsk1_111", "NEAR_SYNONYM", "er4 vs liang3: liang3 is the classifier-position allomorph of er4, an explicit HSK1 grammar point -- deliberately NOT a general numeral-family link (see HSK6 numeral-padding lesson)."),

    # -- personal pronouns: pluralizing suffix men --
    ("hsk1_221", "hsk1_222", "MORPHOLOGICAL_SUFFIX", "wo3 -> wo3men"),
    ("hsk1_146", "hsk1_148", "MORPHOLOGICAL_SUFFIX", "ni3 -> ni3men"),
    ("hsk1_200", "hsk1_203", "MORPHOLOGICAL_SUFFIX", "ta1 -> ta1men"),
    ("hsk1_202", "hsk1_205", "MORPHOLOGICAL_SUFFIX", "ta1(she) -> ta1men(she)"),
    ("hsk1_201", "hsk1_204", "MORPHOLOGICAL_SUFFIX", "ta1(it) -> ta1men(it)"),
    ("hsk1_124", "hsk1_222", "MORPHOLOGICAL_SUFFIX", "men is the suffix morpheme of wo3men"),
    ("hsk1_124", "hsk1_148", "MORPHOLOGICAL_SUFFIX", "men is the suffix morpheme of ni3men"),
    ("hsk1_124", "hsk1_203", "MORPHOLOGICAL_SUFFIX", "men is the suffix morpheme of ta1men"),
    ("hsk1_124", "hsk1_205", "MORPHOLOGICAL_SUFFIX", "men is the suffix morpheme of ta1men(she)"),
    ("hsk1_124", "hsk1_204", "MORPHOLOGICAL_SUFFIX", "men is the suffix morpheme of ta1men(it)"),
    ("hsk1_146", "hsk1_150", "NEAR_SYNONYM", "ni3 vs nin2: informal/formal register pair for 'you', explicit HSK1 teaching point"),
    ("hsk1_200", "hsk1_202", "CLOSED_PARADIGM", "third-person singular gender paradigm: ta1/ta1(she)"),
    ("hsk1_200", "hsk1_201", "CLOSED_PARADIGM", "third-person singular paradigm: ta1(he)/ta1(it)"),
    ("hsk1_202", "hsk1_201", "CLOSED_PARADIGM", "third-person singular paradigm: ta1(she)/ta1(it)"),
    ("hsk1_203", "hsk1_205", "CLOSED_PARADIGM", "third-person plural gender paradigm"),
    ("hsk1_203", "hsk1_204", "CLOSED_PARADIGM", "third-person plural paradigm"),
    ("hsk1_205", "hsk1_204", "CLOSED_PARADIGM", "third-person plural paradigm"),

    # -- demonstrative / interrogative closed paradigms (zhe4/na4/na3 family) --
    ("hsk1_279", "hsk1_136", "ANTONYM", "zhe4 (this) / na4 (that)"),
    ("hsk1_279", "hsk1_131", "CLOSED_PARADIGM", "zhe4 (this) / na3 (which) -- demonstrative/interrogative counterpart"),
    ("hsk1_136", "hsk1_131", "CLOSED_PARADIGM", "na4 (that) / na3 (which) -- demonstrative/interrogative counterpart"),
    ("hsk1_281", "hsk1_138", "CLOSED_PARADIGM", "zhe4ge / na4ge"),
    ("hsk1_281", "hsk1_132", "CLOSED_PARADIGM", "zhe4ge / na3ge"),
    ("hsk1_138", "hsk1_132", "CLOSED_PARADIGM", "na4ge / na3ge"),
    ("hsk1_282", "hsk1_139", "CLOSED_PARADIGM", "zhe4li3 / na4li3"),
    ("hsk1_282", "hsk1_133", "CLOSED_PARADIGM", "zhe4li3 / na3li3"),
    ("hsk1_139", "hsk1_133", "CLOSED_PARADIGM", "na4li3 / na3li3"),
    ("hsk1_283", "hsk1_140", "CLOSED_PARADIGM", "zhe4r / na4r"),
    ("hsk1_283", "hsk1_134", "CLOSED_PARADIGM", "zhe4r / na3r"),
    ("hsk1_140", "hsk1_134", "CLOSED_PARADIGM", "na4r / na3r"),
    ("hsk1_284", "hsk1_141", "CLOSED_PARADIGM", "zhe4xie1 / na4xie1"),
    ("hsk1_284", "hsk1_135", "CLOSED_PARADIGM", "zhe4xie1 / na3xie1"),
    ("hsk1_141", "hsk1_135", "CLOSED_PARADIGM", "na4xie1 / na3xie1"),
    ("hsk1_280", "hsk1_137", "CLOSED_PARADIGM", "zhe4bian1 / na4bian1 (no na3bian1 in HSK1)"),
    ("hsk1_282", "hsk1_283", "NEAR_SYNONYM", "zhe4li3 / zhe4r: near-total synonyms, both 'here'"),
    ("hsk1_139", "hsk1_140", "NEAR_SYNONYM", "na4li3 / na4r: near-total synonyms, both 'there'"),
    ("hsk1_133", "hsk1_134", "NEAR_SYNONYM", "na3li3 / na3r: near-total synonyms, both 'where'"),
    ("hsk1_262", "hsk1_266", "NEAR_SYNONYM", "yi4xie1 / you3xie1: both 'some/a few'"),
    ("hsk1_264", "hsk1_266", "NEAR_SYNONYM", "you3de / you3xie1: both 'some'"),
    ("hsk1_265", "hsk1_261", "NEAR_SYNONYM", "you3dian3r / yi4dian3r: both 'a little'"),
    ("hsk1_259", "hsk1_261", "NEAR_SYNONYM", "yi2xia4 / yi4dian3r: both express a small degree/brief duration in different syntactic slots"),

    # -- gender pairs --
    ("hsk1_142", "hsk1_152", "ANTONYM", "nan2 (male) / nu:3 (female)"),
    ("hsk1_143", "hsk1_154", "GENDER_PAIR", "nan2peng2you / nu:3peng2you"),
    ("hsk1_048", "hsk1_153", "GENDER_PAIR", "er2zi (son) / nu:3'er2 (daughter)"),
    ("hsk1_156", "hsk1_143", "COMPOSITIONAL_COMPOUND", "peng2you is the root of nan2peng2you"),
    ("hsk1_156", "hsk1_154", "COMPOSITIONAL_COMPOUND", "peng2you is the root of nu:3peng2you"),
    ("hsk1_231", "hsk1_155", "GENDER_PAIR", "xian1sheng (Mr.) / nu:3shi4 (Ms.) -- polite address terms"),

    # -- sibling contrast/gender paradigm --
    ("hsk1_059", "hsk1_032", "CONTRAST", "ge1ge (older brother) / di4di (younger brother)"),
    ("hsk1_092", "hsk1_123", "CONTRAST", "jie3jie (older sister) / mei4mei (younger sister)"),
    ("hsk1_059", "hsk1_092", "GENDER_PAIR", "older siblings: brother/sister"),
    ("hsk1_032", "hsk1_123", "GENDER_PAIR", "younger siblings: brother/sister"),

    # -- other antonyms --
    ("hsk1_025", "hsk1_234", "ANTONYM", "da4 (big) / xiao3 (small)"),
    ("hsk1_046", "hsk1_180", "ANTONYM", "duo1 (many) / shao3 (few)"),
    ("hsk1_109", "hsk1_169", "ANTONYM", "leng3 (cold) / re4 (hot)"),
    ("hsk1_116", "hsk1_117", "ANTONYM", "mai3 (buy) / mai4 (sell)"),
    ("hsk1_273", "hsk1_215", "ANTONYM", "zao3 (early) / wan3 (late)"),
    ("hsk1_175", "hsk1_226", "ANTONYM", "shang4 (up) / xia4 (down)"),
    ("hsk1_106", "hsk1_167", "ANTONYM", "lai2 (come) / qu4 (go)"),
    ("hsk1_163", "hsk1_080", "ANTONYM", "qian2 (front) / hou4 (back)"),
    ("hsk1_110", "hsk1_212", "ANTONYM", "li3 (inside) / wai4 (outside)"),
    ("hsk1_263", "hsk1_122", "ANTONYM", "you3 (have) / mei2you3 (not have)"),
    ("hsk1_065", "hsk1_157", "ANTONYM", "gui4 (expensive) / pian2yi (cheap)"),
    ("hsk1_275", "hsk1_217", "ANTONYM", "zao3shang (morning) / wan3shang (evening)"),

    # -- shang4/xia4 activity compounds --
    ("hsk1_176", "hsk1_177", "COMPOUND_FAMILY", "shang4ban1 / shang4ke4: shang4+activity family"),
    ("hsk1_176", "hsk1_179", "COMPOUND_FAMILY", "shang4ban1 / shang4xue2: shang4+activity family"),
    ("hsk1_177", "hsk1_179", "COMPOUND_FAMILY", "shang4ke4 / shang4xue2: shang4+activity family"),
    ("hsk1_228", "hsk1_229", "COMPOUND_FAMILY", "xia4ban1 / xia4ke4: xia4+activity-end family"),
    ("hsk1_176", "hsk1_228", "ANTONYM", "shang4ban1 (start work) / xia4ban1 (end work)"),
    ("hsk1_177", "hsk1_229", "ANTONYM", "shang4ke4 (start class) / xia4ke4 (end class)"),
    ("hsk1_227", "hsk1_267", "COMPOSITIONAL_COMPOUND", "xia4yu3 is directly compositional with yu3"),

    # -- hao3+X adjective compound family --
    ("hsk1_072", "hsk1_073", "COMPOUND_FAMILY", "hao3chi1 / hao3kan4"),
    ("hsk1_072", "hsk1_074", "COMPOUND_FAMILY", "hao3chi1 / hao3ting1"),
    ("hsk1_072", "hsk1_075", "COMPOUND_FAMILY", "hao3chi1 / hao3wan2r"),
    ("hsk1_073", "hsk1_074", "COMPOUND_FAMILY", "hao3kan4 / hao3ting1"),
    ("hsk1_073", "hsk1_075", "COMPOUND_FAMILY", "hao3kan4 / hao3wan2r"),
    ("hsk1_074", "hsk1_075", "COMPOUND_FAMILY", "hao3ting1 / hao3wan2r"),
    ("hsk1_071", "hsk1_072", "COMPOSITIONAL_COMPOUND", "hao3 is the root of hao3chi1"),
    ("hsk1_071", "hsk1_073", "COMPOSITIONAL_COMPOUND", "hao3 is the root of hao3kan4"),
    ("hsk1_071", "hsk1_074", "COMPOSITIONAL_COMPOUND", "hao3 is the root of hao3ting1"),
    ("hsk1_071", "hsk1_075", "COMPOSITIONAL_COMPOUND", "hao3 is the root of hao3wan2r"),
    ("hsk1_158", "hsk1_073", "NEAR_SYNONYM", "piao4liang / hao3kan4: both 'good-looking/pretty'"),

    # -- dian4+X electric-device compound family --
    ("hsk1_035", "hsk1_036", "COMPOUND_FAMILY", "dian4hua4 / dian4nao3"),
    ("hsk1_035", "hsk1_037", "COMPOUND_FAMILY", "dian4hua4 / dian4shi4"),
    ("hsk1_035", "hsk1_038", "COMPOUND_FAMILY", "dian4hua4 / dian4ying3"),
    ("hsk1_036", "hsk1_037", "COMPOUND_FAMILY", "dian4nao3 / dian4shi4"),
    ("hsk1_036", "hsk1_038", "COMPOUND_FAMILY", "dian4nao3 / dian4ying3"),
    ("hsk1_037", "hsk1_038", "COMPOUND_FAMILY", "dian4shi4 / dian4ying3"),
    ("hsk1_038", "hsk1_039", "COMPOSITIONAL_COMPOUND", "dian4ying3yuan4 is compositional with dian4ying3"),
    ("hsk1_035", "hsk1_024", "COMPOSITIONAL_COMPOUND", "da3dian4hua4 is compositional with dian4hua4"),
    ("hsk1_035", "hsk1_189", "FUNCTIONAL_CONTEXT", "shou3ji1 is the device commonly used to place dian4hua4 calls"),

    # -- zhong1guo/zhong1wen + han4yu3/han4zi -- language family --
    ("hsk1_289", "hsk1_290", "COMPOUND_FAMILY", "zhong1guo2 / zhong1wen2"),
    ("hsk1_069", "hsk1_290", "NEAR_SYNONYM", "han4yu3 / zhong1wen2: near-total synonyms, both 'Chinese language'"),
    ("hsk1_069", "hsk1_070", "COMPOUND_FAMILY", "han4yu3 / han4zi4"),
    ("hsk1_290", "hsk1_070", "FUNCTIONAL_CONTEXT", "han4zi4 is the writing system of zhong1wen2"),

    # -- education-level closed paradigm (da4xue2/zhong1xue2/xiao3xue2) --
    ("hsk1_027", "hsk1_292", "CLOSED_PARADIGM", "education-level paradigm: da4xue2 / zhong1xue2"),
    ("hsk1_027", "hsk1_237", "CLOSED_PARADIGM", "education-level paradigm: da4xue2 / xiao3xue2"),
    ("hsk1_292", "hsk1_237", "CLOSED_PARADIGM", "education-level paradigm: zhong1xue2 / xiao3xue2"),
    ("hsk1_028", "hsk1_293", "CLOSED_PARADIGM", "student-level paradigm: da4xue2sheng1 / zhong1xue2sheng1"),
    ("hsk1_028", "hsk1_238", "CLOSED_PARADIGM", "student-level paradigm: da4xue2sheng1 / xiao3xue2sheng1"),
    ("hsk1_293", "hsk1_238", "CLOSED_PARADIGM", "student-level paradigm: zhong1xue2sheng1 / xiao3xue2sheng1"),
    ("hsk1_027", "hsk1_028", "COMPOSITIONAL_COMPOUND", "da4xue2 -> da4xue2sheng1"),
    ("hsk1_292", "hsk1_293", "COMPOSITIONAL_COMPOUND", "zhong1xue2 -> zhong1xue2sheng1"),
    ("hsk1_237", "hsk1_238", "COMPOSITIONAL_COMPOUND", "xiao3xue2 -> xiao3xue2sheng1"),
    ("hsk1_248", "hsk1_028", "COMPOUND_FAMILY", "xue2sheng1 is the hypernym root shared with da4xue2sheng1"),
    ("hsk1_248", "hsk1_293", "COMPOUND_FAMILY", "xue2sheng1 is the hypernym root shared with zhong1xue2sheng1"),
    ("hsk1_248", "hsk1_238", "COMPOUND_FAMILY", "xue2sheng1 is the hypernym root shared with xiao3xue2sheng1"),
    ("hsk1_250", "hsk1_248", "FUNCTIONAL_CONTEXT", "xue2xiao4 (school) and xue2sheng1 (student): institution/role pair"),
    ("hsk1_247", "hsk1_249", "NEAR_SYNONYM", "xue2 / xue2xi2: near-synonym verb pair, classic HSK1 contrast"),
    ("hsk1_247", "hsk1_250", "COMPOSITIONAL_COMPOUND", "xue2 is the root of xue2xiao4"),
    ("hsk1_247", "hsk1_248", "COMPOSITIONAL_COMPOUND", "xue2 is the root of xue2sheng1"),
    ("hsk1_042", "hsk1_043", "COMPOSITIONAL_COMPOUND", "du2 is the root of du2shu1"),
    ("hsk1_043", "hsk1_249", "NEAR_SYNONYM", "du2shu1 can also mean 'to study', commonly contrasted with xue2xi2"),
    ("hsk1_211", "hsk1_248", "NEAR_SYNONYM", "tong2xue2 (classmate) / xue2sheng1 (student): close, commonly co-occurring"),

    # -- medical family --
    ("hsk1_256", "hsk1_257", "COMPOUND_FAMILY", "yi1sheng1 / yi1yuan4"),
    ("hsk1_256", "hsk1_100", "FUNCTIONAL_CONTEXT", "yi1sheng1 performs kan4bing4"),
    ("hsk1_257", "hsk1_100", "FUNCTIONAL_CONTEXT", "kan4bing4 takes place at yi1yuan4"),
    ("hsk1_012", "hsk1_100", "COMPOSITIONAL_COMPOUND", "bing4 is the object of kan4bing4"),
    ("hsk1_012", "hsk1_183", "COMPOSITIONAL_COMPOUND", "bing4 is the root of sheng1bing4; also near-synonymous 'be ill' as noun/verb vs verb"),

    # -- vehicle compounds --
    ("hsk1_020", "hsk1_083", "COMPOSITIONAL_COMPOUND", "che1 is the root of huo3che1"),
    ("hsk1_020", "hsk1_022", "COMPOSITIONAL_COMPOUND", "che1 is the root of chu1zu1che1"),
    ("hsk1_083", "hsk1_022", "COMPOUND_FAMILY", "huo3che1 / chu1zu1che1: X+che1 vehicle-type family"),
    ("hsk1_020", "hsk1_098", "COMPOSITIONAL_COMPOUND", "che1 is the object of kai1che1"),

    # -- shop compounds --
    ("hsk1_051", "hsk1_191", "COMPOUND_FAMILY", "fan4dian4 / shu1dian4: X+dian4 shop family"),
    ("hsk1_051", "hsk1_174", "COMPOUND_FAMILY", "fan4dian4 / shang1dian4: X+dian4 shop family"),
    ("hsk1_191", "hsk1_174", "COMPOUND_FAMILY", "shu1dian4 / shang1dian4: X+dian4 shop family"),
    ("hsk1_190", "hsk1_191", "COMPOSITIONAL_COMPOUND", "shu1 is the root of shu1dian4"),
    ("hsk1_050", "hsk1_051", "COMPOSITIONAL_COMPOUND", "fan4 is the root of fan4dian4"),
    ("hsk1_019", "hsk1_174", "NEAR_SYNONYM", "chao1shi4 (supermarket) / shang1dian4 (shop): closely related retail concepts"),

    # -- meal-time closed paradigm --
    ("hsk1_274", "hsk1_224", "CLOSED_PARADIGM", "meal-time paradigm: zao3fan4 / wu3fan4"),
    ("hsk1_274", "hsk1_216", "CLOSED_PARADIGM", "meal-time paradigm: zao3fan4 / wan3fan4"),
    ("hsk1_224", "hsk1_216", "CLOSED_PARADIGM", "meal-time paradigm: wu3fan4 / wan3fan4"),
    ("hsk1_125", "hsk1_050", "COMPOSITIONAL_COMPOUND", "mi3fan4 is directly compositional with fan4"),
    ("hsk1_273", "hsk1_275", "COMPOSITIONAL_COMPOUND", "zao3 is the root of zao3shang4"),
    ("hsk1_215", "hsk1_217", "COMPOSITIONAL_COMPOUND", "wan3 is the root of wan3shang4"),
    ("hsk1_274", "hsk1_275", "FUNCTIONAL_CONTEXT", "zao3fan4 is eaten during zao3shang4"),
    ("hsk1_216", "hsk1_217", "FUNCTIONAL_CONTEXT", "wan3fan4 is eaten during wan3shang4"),

    # -- day-part closed paradigm --
    ("hsk1_178", "hsk1_291", "CLOSED_PARADIGM", "day-part paradigm: shang4wu3 / zhong1wu3"),
    ("hsk1_178", "hsk1_230", "CLOSED_PARADIGM", "day-part paradigm: shang4wu3 / xia4wu3"),
    ("hsk1_291", "hsk1_230", "CLOSED_PARADIGM", "day-part paradigm: zhong1wu3 / xia4wu3"),
    ("hsk1_275", "hsk1_178", "NEAR_SYNONYM", "zao3shang4 / shang4wu3: overlapping 'morning' senses, standard HSK1 nuance contrast"),

    # -- duration units --
    ("hsk1_055", "hsk1_056", "COMPOSITIONAL_COMPOUND", "fen1 is the root of fen1zhong1"),
    ("hsk1_236", "hsk1_056", "CLOSED_PARADIGM", "duration-unit pair: xiao3shi2 / fen1zhong1"),

    # -- Sunday near-synonym + week compounds --
    ("hsk1_244", "hsk1_245", "NEAR_SYNONYM", "xing1qi1ri4 / xing1qi1tian1: near-total synonyms, both 'Sunday'"),
    ("hsk1_243", "hsk1_244", "COMPOSITIONAL_COMPOUND", "xing1qi1 is the root of xing1qi1ri4"),
    ("hsk1_243", "hsk1_245", "COMPOSITIONAL_COMPOUND", "xing1qi1 is the root of xing1qi1tian1"),

    # -- day/year deixis closed paradigms --
    ("hsk1_297", "hsk1_094", "CLOSED_PARADIGM", "day-deixis paradigm: zuo2tian1 / jin1tian1"),
    ("hsk1_297", "hsk1_129", "CLOSED_PARADIGM", "day-deixis paradigm: zuo2tian1 / ming2tian1"),
    ("hsk1_094", "hsk1_129", "CLOSED_PARADIGM", "day-deixis paradigm: jin1tian1 / ming2tian1"),
    ("hsk1_168", "hsk1_093", "CLOSED_PARADIGM", "year-deixis paradigm: qu4nian2 / jin1nian2"),
    ("hsk1_168", "hsk1_128", "CLOSED_PARADIGM", "year-deixis paradigm: qu4nian2 / ming2nian2"),
    ("hsk1_093", "hsk1_128", "CLOSED_PARADIGM", "year-deixis paradigm: jin1nian2 / ming2nian2"),
    ("hsk1_094", "hsk1_093", "COMPOUND_FAMILY", "jin1tian1 / jin1nian2: shared jin1- root"),
    ("hsk1_129", "hsk1_128", "COMPOUND_FAMILY", "ming2tian1 / ming2nian2: shared ming2- root"),
    ("hsk1_207", "hsk1_094", "COMPOSITIONAL_COMPOUND", "tian1 is the root of jin1tian1"),
    ("hsk1_207", "hsk1_129", "COMPOSITIONAL_COMPOUND", "tian1 is the root of ming2tian1"),
    ("hsk1_207", "hsk1_297", "COMPOSITIONAL_COMPOUND", "tian1 is the root of zuo2tian1"),
    ("hsk1_149", "hsk1_093", "COMPOSITIONAL_COMPOUND", "nian2 is the root of jin1nian2"),
    ("hsk1_149", "hsk1_128", "COMPOSITIONAL_COMPOUND", "nian2 is the root of ming2nian2"),
    ("hsk1_149", "hsk1_168", "COMPOSITIONAL_COMPOUND", "nian2 is the root of qu4nian2"),
    ("hsk1_207", "hsk1_005", "COMPOSITIONAL_COMPOUND", "tian1 is the root of bai2tian1"),
    ("hsk1_207", "hsk1_208", "COMPOSITIONAL_COMPOUND", "tian1's 'sky' sense is the etymological root of tian1qi4"),

    # -- work --
    ("hsk1_063", "hsk1_176", "FUNCTIONAL_CONTEXT", "gong1zuo4 (work) and shang4ban1 (start work)"),
    ("hsk1_063", "hsk1_228", "FUNCTIONAL_CONTEXT", "gong1zuo4 (work) and xia4ban1 (end work)"),

    # -- discourse-adjacency pairs --
    ("hsk1_241", "hsk1_014", "FUNCTIONAL_CONTEXT", "xie4xie / bu2ke4qi: canonical thanks/response adjacency pair"),
    ("hsk1_045", "hsk1_120", "FUNCTIONAL_CONTEXT", "dui4buqi3 / mei2guan1xi: canonical apology/response adjacency pair"),
    ("hsk1_121", "hsk1_120", "NEAR_SYNONYM", "mei2shi4 / mei2guan1xi: both 'it's okay/no problem'"),
    ("hsk1_147", "hsk1_272", "FUNCTIONAL_CONTEXT", "ni3hao3 / zai4jian4: canonical greeting-open/close pair"),
    ("hsk1_270", "hsk1_272", "COMPOSITIONAL_COMPOUND", "zai4 is the root of zai4jian4"),
    ("hsk1_088", "hsk1_272", "COMPOSITIONAL_COMPOUND", "jian4 is the root of zai4jian4"),
    ("hsk1_088", "hsk1_101", "COMPOSITIONAL_COMPOUND", "jian4 is the resultative-complement root of kan4jian4"),
    ("hsk1_088", "hsk1_210", "COMPOSITIONAL_COMPOUND", "jian4 is the resultative-complement root of ting1jian4"),
    ("hsk1_099", "hsk1_101", "COMPOSITIONAL_COMPOUND", "kan4 is the root of kan4jian4"),
    ("hsk1_209", "hsk1_210", "COMPOSITIONAL_COMPOUND", "ting1 is the root of ting1jian4"),
    ("hsk1_101", "hsk1_210", "COMPOUND_FAMILY", "kan4jian4 / ting1jian4: parallel V+jian4 resultative-complement family"),

    # -- compositional VO/verb-complement pairs --
    ("hsk1_194", "hsk1_195", "COMPOSITIONAL_COMPOUND", "shui4 is the root of shui4jiao4"),
    ("hsk1_196", "hsk1_197", "COMPOSITIONAL_COMPOUND", "shuo1 is the root of shuo1hua4"),
    ("hsk1_219", "hsk1_220", "COMPOSITIONAL_COMPOUND", "wen4 is the root of wen4ti2"),
    ("hsk1_165", "hsk1_166", "COMPOSITIONAL_COMPOUND", "qing3 is the root of qing3wen4"),
    ("hsk1_021", "hsk1_072", "COMPOSITIONAL_COMPOUND", "chi1 is the root of hao3chi1"),
    ("hsk1_021", "hsk1_077", "NEAR_SYNONYM", "chi1 (eat) / he1 (drink): basic-consumption verb pair, closely taught together"),
    ("hsk1_023", "hsk1_255", "FUNCTIONAL_CONTEXT", "chuan1 (wear) yi1fu (clothes): canonical verb-object collocation"),
    ("hsk1_058", "hsk1_018", "FUNCTIONAL_CONTEXT", "ge1 (song) is the canonical object of chang4 (sing)"),
    ("hsk1_240", "hsk1_296", "FUNCTIONAL_CONTEXT", "xie3 (write) zi4 (characters): canonical verb-object collocation"),
    ("hsk1_296", "hsk1_070", "COMPOSITIONAL_COMPOUND", "zi4 is the root of han4zi4"),

    # -- modal verb near-synonym cluster --
    ("hsk1_233", "hsk1_252", "NEAR_SYNONYM", "xiang3 / yao4: both express 'want to', standard HSK1 contrast"),
    ("hsk1_082", "hsk1_145", "NEAR_SYNONYM", "hui4 / neng2: both 'can', classic HSK1 modal-verb contrast"),
    ("hsk1_082", "hsk1_102", "NEAR_SYNONYM", "hui4 / ke3yi3: both 'can', classic HSK1 modal-verb contrast"),
    ("hsk1_145", "hsk1_102", "NEAR_SYNONYM", "neng2 / ke3yi3: both 'can', classic HSK1 modal-verb contrast"),
    ("hsk1_171", "hsk1_288", "NEAR_SYNONYM", "ren4shi (know a person/thing) / zhi1dao4 (know a fact): standard HSK1 contrast"),
    ("hsk1_096", "hsk1_233", "NEAR_SYNONYM", "jue2de (feel/think) / xiang3 (think/want): commonly contrasted"),
    ("hsk1_206", "hsk1_053", "NEAR_SYNONYM", "tai4 / fei1chang2: near-synonym intensifiers"),
    ("hsk1_053", "hsk1_079", "NEAR_SYNONYM", "fei1chang2 / hen3: both general intensifiers"),
    ("hsk1_067", "hsk1_270", "NEAR_SYNONYM", "hai2 (still) / zai4 (again): commonly contrasted continuation adverbs"),
    ("hsk1_047", "hsk1_085", "NEAR_SYNONYM", "duo1shao (how many/much) / ji3 (how many): standard HSK1 contrast"),

    # -- fruit/food family --
    ("hsk1_126", "hsk1_127", "COMPOUND_FAMILY", "mian4bao1 / mian4tiao2r: mian4+X flour-food family"),
    ("hsk1_193", "hsk1_159", "COMPOUND_FAMILY", "shui3guo3 / ping2guo3: X+guo3 fruit family"),

    # -- small, deliberately-flagged closed 2-item domain pairs (see semantic sanity review) --
    ("hsk1_119", "hsk1_064", "FUNCTIONAL_CONTEXT", "mao1 / gou3: the only two animal words in HSK1, canonical textbook pairing"),
    ("hsk1_260", "hsk1_295", "FUNCTIONAL_CONTEXT", "yi3zi / zhuo1zi: canonical HSK1 furniture pairing ('zhuo1zi he2 yi3zi')"),

    # -- misc compositional / functional singles --
    ("hsk1_007", "hsk1_258", "COMPOSITIONAL_COMPOUND", "ban4 is the root of yi2ban4"),
    ("hsk1_086", "hsk1_087", "COMPOSITIONAL_COMPOUND", "jia1 is the root of jia1ren2"),
    ("hsk1_068", "hsk1_235", "NEAR_SYNONYM", "hai2zi / xiao3peng2you: both can mean 'child'"),
    ("hsk1_251", "hsk1_267", "FUNCTIONAL_CONTEXT", "xue3 (snow) / yu3 (rain): narrow precipitation-type pair"),
    ("hsk1_251", "hsk1_208", "FUNCTIONAL_CONTEXT", "xue3 (snow) is a weather phenomenon reported via tian1qi4"),
    ("hsk1_267", "hsk1_208", "FUNCTIONAL_CONTEXT", "yu3 (rain) is a weather phenomenon reported via tian1qi4"),
]


def load_json_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_hsk1() -> tuple[list[dict], str]:
    text = load_json_text(HSK1_PATH)
    records = json.loads(text)
    if len(records) != 300:
        fail(f"HSK1 production record count {len(records)} != expected 300")
    return records, sha256_of(text)


def load_candidate_universe() -> tuple[dict, str]:
    """HSK1-6 production IDs -> {word, pinyin, level}. Also returns a
    combined hash of all six files (order-stable) for provenance."""
    universe: dict[str, dict] = {}
    combined = []
    for lvl in (1, 2, 3, 4, 5, 6):
        path = REPO_ROOT / "data" / "hsk" / f"hsk{lvl}" / f"hsk{lvl}_vocabulary_production.json"
        text = load_json_text(path)
        combined.append(text)
        records = json.loads(text)
        for r in records:
            universe[r["id"]] = {"word": r["word"], "pinyin": r["pinyin"], "hskLevel": lvl}
    universe_hash = sha256_of(" ".join(combined))
    return universe, universe_hash


def build_reason(category: str, other_word: str, other_pinyin: str) -> str:
    templates = {
        "ANTONYM": f"Antonym of {other_word} ({other_pinyin}).",
        "NEAR_SYNONYM": f"Near-synonym of {other_word} ({other_pinyin}); commonly contrasted in HSK1 usage.",
        "MORPHOLOGICAL_SUFFIX": f"Shares the pluralizing suffix relationship with {other_word} ({other_pinyin}).",
        "COMPOSITIONAL_COMPOUND": f"Directly compositional with {other_word} ({other_pinyin}) via shared root morpheme.",
        "COMPOUND_FAMILY": f"Shares a productive HSK1 word-formation root with {other_word} ({other_pinyin}).",
        "CLOSED_PARADIGM": f"Member of the same closed HSK1 paradigm as {other_word} ({other_pinyin}).",
        "FUNCTIONAL_CONTEXT": f"Functionally/collocationally linked to {other_word} ({other_pinyin}) in real-world usage.",
        "GENDER_PAIR": f"Gender-paired counterpart of {other_word} ({other_pinyin}).",
        "CONTRAST": f"Age/role contrast pair with {other_word} ({other_pinyin}) within a closed kinship set.",
    }
    return templates[category]


def main() -> None:
    if OUTPUT_PATH.exists():
        fail(
            f"{OUTPUT_PATH} already exists -- this script refuses to overwrite an "
            "existing candidate pool artifact. Inspect/validate it instead."
        )

    hsk1_records, source_hash = load_hsk1()
    hsk1_ids = {r["id"] for r in hsk1_records}
    id_to_record = {r["id"]: r for r in hsk1_records}

    universe, universe_hash = load_candidate_universe()

    # Validate every pair before building anything.
    seen_pairs = set()
    for a, b, category, _note in PAIRS:
        if a not in hsk1_ids:
            fail(f"source id '{a}' is not a real HSK1 production id")
        if b not in universe:
            fail(f"candidate id '{b}' is not a real HSK1-6 production id (referenced from {a})")
        if a == b:
            fail(f"self-reference: {a} paired with itself")
        if category not in RULE_CATEGORIES:
            fail(f"unknown category '{category}' on pair ({a}, {b})")
        key = tuple(sorted((a, b)))
        # Allow the same unordered pair to appear at most once in PAIRS;
        # duplicate authoring is a script-authoring bug, not something to
        # silently absorb.
        if key in seen_pairs:
            fail(f"duplicate pair authored: {a} <-> {b}")
        seen_pairs.add(key)

    # Expand to a per-source-id adjacency map (symmetric expansion).
    adjacency: dict[str, list[tuple[str, str]]] = {rid: [] for rid in hsk1_ids}
    for a, b, category, _note in PAIRS:
        adjacency[a].append((b, category))
        if b in adjacency:  # b may be HSK1 or a higher level
            adjacency[b].append((a, category))

    for rid, cands in adjacency.items():
        cand_ids = [c for c, _ in cands]
        if len(cand_ids) != len(set(cand_ids)):
            fail(f"duplicate candidate id(s) generated for source {rid}: {cand_ids}")
        if len(cand_ids) > MAX_CANDIDATES_PER_RECORD:
            fail(f"source {rid} has {len(cand_ids)} candidates, exceeds max {MAX_CANDIDATES_PER_RECORD}")

    generated_at = datetime.now(timezone.utc).isoformat()

    records_out = []
    for r in hsk1_records:
        rid = r["id"]
        cands = adjacency[rid]
        # Deterministic ordering: sort by candidate id (stable, reproducible).
        cands_sorted = sorted(cands, key=lambda t: t[0])
        candidate_entries = []
        for cand_id, category in cands_sorted:
            target = universe[cand_id]
            candidate_entries.append(
                {
                    "wordId": cand_id,
                    "word": target["word"],
                    "hskLevel": target["hskLevel"],
                    "category": category,
                    "reason": build_reason(category, target["word"], target["pinyin"]),
                }
            )
        records_out.append(
            {
                "sourceId": rid,
                "sourceWord": r["word"],
                "sourceHskLevel": 1,
                "candidateCount": len(candidate_entries),
                "candidates": candidate_entries,
            }
        )

    artifact = {
        "poolVersion": POOL_VERSION,
        "sourceDataset": "data/hsk/hsk1/hsk1_vocabulary_production.json",
        "sourceDatasetHash": source_hash,
        "candidateUniverse": "data/hsk/hsk{1..6}/hsk{1..6}_vocabulary_production.json (CROSS_LEVEL_HSK1_TO_HSK6)",
        "candidateUniverseHash": universe_hash,
        "candidateUniverseRecordCount": len(universe),
        "rulesVersion": RULES_VERSION,
        "ruleCategories": RULE_CATEGORIES,
        "maxCandidatesPerRecord": MAX_CANDIDATES_PER_RECORD,
        "scopeNote": (
            "Pilot scope: all candidates in this artifact are HSK1-internal "
            "(every wordId belongs to hsk1_vocabulary_production.json), even "
            "though the candidate universe spans HSK1-6 per the approved "
            "CROSS_LEVEL_HSK1_TO_HSK6 policy. This is a deliberate, documented "
            "scope decision for the pilot, not a silent limitation -- see the "
            "P5.4.1 report."
        ),
        "generatedAt": generated_at,
        "generatorScript": "tools/hsk/generate_hsk1_related_word_candidates_p541.py",
        "recordCount": len(records_out),
        "records": records_out,
    }

    OUTPUT_PATH.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    total_candidates = sum(r["candidateCount"] for r in records_out)
    zero_count = sum(1 for r in records_out if r["candidateCount"] == 0)
    max_count = max(r["candidateCount"] for r in records_out)
    print(f"Wrote {OUTPUT_PATH}")
    print(f"records: {len(records_out)}  total candidate edges: {total_candidates}  "
          f"zero-candidate records: {zero_count}  max per record: {max_count}")


if __name__ == "__main__":
    main()
