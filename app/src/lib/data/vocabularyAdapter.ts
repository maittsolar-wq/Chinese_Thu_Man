import type { HskLevel, VocabularyExample, VocabularyWord } from "./types";

/**
 * The six hsk{N}_vocabulary_production.json files do not share one schema:
 *  - HSK 1: meaningVi is string[]; hskLevels/partOfSpeech/strokeCount/
 *    characterIds/exampleIds/audio/relatedWordIds all present (the latter
 *    group always empty/null in the current data).
 *  - HSK 2–5: same field set as HSK 1, but meaningVi is a single string,
 *    plus extra pipeline bookkeeping fields (candidateMeanings,
 *    selectedMeaningVi, reviewStatus, etc.) that the UI does not need.
 *  - HSK 6: reduced shape — no hskLevels (uses `level: "HSK 6"`), no
 *    partOfSpeech (uses `cixing`), no characterIds/exampleIds/audio/
 *    strokeCount/relatedWordIds at all.
 *  - `examples` (P5.10.4 integration): present only on records covered
 *    by the HSK Examples generation pipeline (pilot + batches 002-032,
 *    5312 records across all six levels); absent entirely on the 88
 *    special-review records that pipeline intentionally excluded. The
 *    legacy `exampleIds` field (always empty) is unrelated and untouched.
 *
 * This adapter normalizes every level to the single canonical
 * VocabularyWord shape at read time. It never edits the source files.
 */
export interface RawVocabularyRecord {
  id: string;
  word: string;
  pinyin: string;
  meaningVi?: string | string[] | null;
  selectedMeaningVi?: string | null;
  candidateMeanings?: string[] | null;
  hskLevels?: number[] | null;
  level?: string | null;
  partOfSpeech?: string[] | null;
  cixing?: string | null;
  strokeCount?: number | null;
  relatedWordIds?: string[] | null;
  examples?: VocabularyExample[] | null;
  audio?: { wordUrl?: string | null; exampleUrl?: string | null } | null;
}

function parseLevelFromLabel(label: string | null | undefined): HskLevel | null {
  if (!label) return null;
  const match = /(\d)/.exec(label);
  if (!match) return null;
  const value = Number(match[1]);
  return value >= 1 && value <= 6 ? (value as HskLevel) : null;
}

function resolveMeaningVi(raw: RawVocabularyRecord): string {
  if (Array.isArray(raw.meaningVi)) {
    return raw.meaningVi.filter(Boolean).join("; ");
  }
  return (
    raw.selectedMeaningVi ||
    raw.meaningVi ||
    raw.candidateMeanings?.[0] ||
    ""
  );
}

function resolveHskLevels(
  raw: RawVocabularyRecord,
  fallbackLevel: HskLevel
): HskLevel[] {
  if (Array.isArray(raw.hskLevels) && raw.hskLevels.length > 0) {
    return raw.hskLevels.filter(
      (level): level is HskLevel => level >= 1 && level <= 6
    );
  }
  const fromLabel = parseLevelFromLabel(raw.level);
  return [fromLabel ?? fallbackLevel];
}

function resolvePartOfSpeech(raw: RawVocabularyRecord): string[] {
  if (Array.isArray(raw.partOfSpeech) && raw.partOfSpeech.length > 0) {
    return raw.partOfSpeech;
  }
  return raw.cixing ? [raw.cixing] : [];
}

export function normalizeVocabularyRecord(
  raw: RawVocabularyRecord,
  fallbackLevel: HskLevel
): VocabularyWord {
  return {
    id: raw.id,
    word: raw.word,
    pinyin: raw.pinyin,
    meaningVi: resolveMeaningVi(raw),
    hskLevels: resolveHskLevels(raw, fallbackLevel),
    partOfSpeech: resolvePartOfSpeech(raw),
    strokeCount: raw.strokeCount ?? null,
    relatedWordIds: raw.relatedWordIds ?? [],
    // Populated by the P5.10.4 integration for pipeline-covered records
    // (pilot + batches 002-032); absent on the special-review records,
    // which correctly fall back to an empty array here.
    examples: raw.examples ?? [],
    audio: {
      wordUrl: raw.audio?.wordUrl ?? null,
      exampleUrl: raw.audio?.exampleUrl ?? null,
    },
  };
}
