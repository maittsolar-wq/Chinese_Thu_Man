"use server";

import { searchDictionary } from "@/lib/data/dictionarySearch";
import type { VocabularyWord } from "@/lib/data/types";

/**
 * The Dictionary Search Popup is a client component, but vocabulary/radical
 * data is only readable server-side (the repositories read production JSON
 * from disk via `fs`). This Server Action is the same bridge pattern as
 * lib/practice/actions.ts's fetchPracticeVocabulary — it just forwards to
 * the real search logic, nothing is reimplemented here.
 */
export async function searchDictionaryAction(query: string): Promise<VocabularyWord[]> {
  return searchDictionary(query);
}
