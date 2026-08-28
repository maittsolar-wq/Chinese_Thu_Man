import type {
  HskLevel,
  RadicalCharacterRef,
  RadicalDetail,
  RadicalSummary,
  RadicalVocabularyRef,
} from "./types";

export interface RawRadicalSummary {
  id: string;
  kangxiIndex: number;
  radical: string;
  pinyin: string;
  nameVi: string;
  meaningVi: string;
  strokeCount: number;
  variants: string[];
  groupKey: string;
}

export interface RawRadicalCharacterEntry {
  character: string;
  unicode: string;
  sourceVocabularyLevels: number[];
}

export interface RawRadicalDetail {
  radicalId: string;
  characterCount: number;
  characters: RawRadicalCharacterEntry[];
}

export interface RawRadicalVocabularyEntry {
  vocabularyId: string;
  word: string;
  pinyin: string;
  level: number;
  character: string;
}

export interface RawRadicalVocabularyMapping {
  radicalId: string;
  vocabularyCount: number;
  vocabularyByLevel: Record<string, RawRadicalVocabularyEntry[]>;
}

export function normalizeRadicalSummary(raw: RawRadicalSummary): RadicalSummary {
  return {
    id: raw.id,
    kangxiIndex: raw.kangxiIndex,
    radical: raw.radical,
    pinyin: raw.pinyin,
    nameVi: raw.nameVi,
    meaningVi: raw.meaningVi,
    strokeCount: raw.strokeCount,
    variants: raw.variants ?? [],
    groupKey: raw.groupKey,
  };
}

function isHskLevel(value: number): value is HskLevel {
  return value >= 1 && value <= 6;
}

export function buildRadicalDetail(
  summary: RadicalSummary,
  detail: RawRadicalDetail,
  vocabularyMapping: RawRadicalVocabularyMapping,
  resolveMeaning: (vocabularyId: string) => string | null
): RadicalDetail {
  const characters: RadicalCharacterRef[] = detail.characters.map((entry) => ({
    character: entry.character,
    unicode: entry.unicode,
    hskLevels: entry.sourceVocabularyLevels,
  }));

  const vocabularyByLevel: Partial<Record<HskLevel, RadicalVocabularyRef[]>> = {};
  for (const [levelKey, entries] of Object.entries(
    vocabularyMapping.vocabularyByLevel
  )) {
    const level = Number(levelKey);
    if (!isHskLevel(level) || entries.length === 0) continue;
    vocabularyByLevel[level] = entries.map((entry) => ({
      vocabularyId: entry.vocabularyId,
      word: entry.word,
      pinyin: entry.pinyin,
      level: level,
      character: entry.character,
      meaningVi: resolveMeaning(entry.vocabularyId),
    }));
  }

  return {
    ...summary,
    characterCount: detail.characterCount,
    characters,
    vocabularyCount: vocabularyMapping.vocabularyCount,
    vocabularyByLevel,
  };
}
