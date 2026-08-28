import fs from "node:fs";
import { hskProductionPath } from "./paths";
import { memoizeOnce } from "./memoize";
import {
  normalizeVocabularyRecord,
  type RawVocabularyRecord,
} from "./vocabularyAdapter";
import type { HskLevel, VocabularyWord } from "./types";

const ALL_LEVELS: HskLevel[] = [1, 2, 3, 4, 5, 6];

function loadLevel(level: HskLevel): VocabularyWord[] {
  const filePath = hskProductionPath(level);
  const raw = fs.readFileSync(filePath, "utf-8");
  const records: RawVocabularyRecord[] = JSON.parse(raw);
  return records.map((record) => normalizeVocabularyRecord(record, level));
}

const loadAllVocabulary = memoizeOnce((): VocabularyWord[] => {
  return ALL_LEVELS.flatMap(loadLevel);
});

const loadVocabularyIndex = memoizeOnce((): Map<string, VocabularyWord> => {
  const index = new Map<string, VocabularyWord>();
  for (const word of loadAllVocabulary()) {
    index.set(word.id, word);
  }
  return index;
});

export function getAllVocabulary(): VocabularyWord[] {
  return loadAllVocabulary();
}

export function getVocabularyById(id: string): VocabularyWord | null {
  return loadVocabularyIndex().get(id) ?? null;
}

export function getVocabularyByLevel(level: HskLevel): VocabularyWord[] {
  return loadAllVocabulary().filter((word) => word.hskLevels.includes(level));
}

export function getVocabularyCountByLevel(level: HskLevel): number {
  return getVocabularyByLevel(level).length;
}

export function getTotalVocabularyCount(): number {
  return loadAllVocabulary().length;
}

function normalizeSearchText(value: string): string {
  return value.trim().toLowerCase().replace(/\s+/g, " ");
}

/** Strips Pinyin tone marks so "xue2 xi2" / "xuexi" style queries still match. */
function stripToneMarks(value: string): string {
  return value.normalize("NFD").replace(/[̀-ͯ]/g, "");
}

export interface VocabularySearchResult {
  word: VocabularyWord;
  matchType: "chinese" | "pinyin" | "meaning";
}

/**
 * Search across Chinese / Pinyin / Vietnamese meaning per
 * docs/DICTIONARY/DICTIONARY_SPEC.md §8–9: exact Chinese, then exact
 * Pinyin, then exact meaning, then prefix, then broader substring match.
 * Deterministic — ties break on the underlying vocabulary id.
 */
export function searchVocabulary(query: string): VocabularyWord[] {
  const trimmed = normalizeSearchText(query);
  if (!trimmed) return [];

  const trimmedNoTones = stripToneMarks(trimmed);
  const all = loadAllVocabulary();

  const scored = all
    .map((word) => {
      const chinese = word.word;
      const pinyin = normalizeSearchText(word.pinyin);
      const pinyinNoTones = stripToneMarks(pinyin).replace(/\s+/g, "");
      const meaning = normalizeSearchText(word.meaningVi);
      const queryNoSpaces = trimmedNoTones.replace(/\s+/g, "");

      let rank = -1;
      if (chinese === trimmed) rank = 0;
      else if (pinyin === trimmed || pinyinNoTones === queryNoSpaces) rank = 1;
      else if (meaning === trimmed) rank = 2;
      else if (chinese.startsWith(trimmed) || pinyin.startsWith(trimmed)) rank = 3;
      else if (meaning.startsWith(trimmed)) rank = 4;
      else if (
        chinese.includes(trimmed) ||
        pinyin.includes(trimmed) ||
        pinyinNoTones.includes(queryNoSpaces) ||
        meaning.includes(trimmed)
      )
        rank = 5;

      return { word, rank };
    })
    .filter((entry) => entry.rank >= 0);

  scored.sort((a, b) => a.rank - b.rank || a.word.id.localeCompare(b.word.id));

  return scored.map((entry) => entry.word);
}
