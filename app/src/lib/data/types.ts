export type HskLevel = 1 | 2 | 3 | 4 | 5 | 6;

export interface VocabularyAudio {
  wordUrl: string | null;
  exampleUrl: string | null;
}

export interface VocabularyExample {
  chinese: string;
  pinyin: string;
  meaningVi: string;
}

/**
 * Canonical vocabulary shape used everywhere in the UI (HSK, Dictionary,
 * Word Detail, Radicals). Produced by normalizing whichever raw shape a
 * given HSK level's production JSON happens to use — see
 * lib/data/vocabularyAdapter.ts. The source production files are never
 * modified; this is a read-time projection only.
 */
export interface VocabularyWord {
  id: string;
  word: string;
  pinyin: string;
  /** Vietnamese meaning, senses joined with "; " when the source has more than one. */
  meaningVi: string;
  hskLevels: HskLevel[];
  partOfSpeech: string[];
  strokeCount: number | null;
  relatedWordIds: string[];
  examples: VocabularyExample[];
  audio: VocabularyAudio;
}

export interface RadicalSummary {
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

export interface RadicalCharacterRef {
  character: string;
  unicode: string;
  hskLevels: number[];
}

export interface RadicalVocabularyRef {
  vocabularyId: string;
  word: string;
  pinyin: string;
  level: HskLevel;
  character: string;
  /** Resolved from the vocabulary repository; null if the id can't be found. */
  meaningVi: string | null;
}

export interface RadicalDetail extends RadicalSummary {
  characterCount: number;
  characters: RadicalCharacterRef[];
  vocabularyCount: number;
  vocabularyByLevel: Partial<Record<HskLevel, RadicalVocabularyRef[]>>;
}
