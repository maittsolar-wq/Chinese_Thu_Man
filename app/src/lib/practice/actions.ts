"use server";

import { getVocabularyByLevel } from "@/lib/data/vocabularyRepository";
import type { HskLevel } from "@/lib/data/types";
import type { PracticeVocabularyItem } from "./session";

/**
 * The Practice session state lives in a client component, but vocabulary
 * data is only readable server-side (vocabularyRepository reads the
 * production JSON files from disk via `fs`). This Server Action is the
 * bridge: it reuses the exact same `getVocabularyByLevel` used by the
 * existing /hsk/[level] page — same pool, same data, nothing invented or
 * duplicated — and returns only the fields a session needs.
 */
export async function fetchPracticeVocabulary(
  hskLevel: HskLevel
): Promise<PracticeVocabularyItem[]> {
  return getVocabularyByLevel(hskLevel).map((word) => ({
    id: word.id,
    word: word.word,
    pinyin: word.pinyin,
    meaningVi: word.meaningVi,
  }));
}
