import type { VocabularyWord } from "./types";

/**
 * Pure, environment-agnostic — no `fs`, safe to import from a "use client"
 * component. Replicates EXACTLY the matching behavior /hsk/[level] already
 * used (word/pinyin/meaning substring match, case-insensitive) before this
 * phase converted it to live client-side search — same behavior, just no
 * longer a server round-trip. This intentionally does NOT reuse
 * vocabularyRepository's `searchVocabulary` (exact→prefix→substring
 * ranking, tone-stripped pinyin): that's the Dictionary's global search,
 * a different, already-shipped experience with different behavior. Per
 * the audit and this phase's instructions, HSK level search keeps its
 * own existing, simpler, already-correct matching — not "upgraded" to
 * Dictionary's ranking just because the mechanism moved client-side.
 */
export function filterHskLevelVocabulary(
  words: VocabularyWord[],
  query: string
): VocabularyWord[] {
  const trimmed = query.trim().toLowerCase();
  if (!trimmed) return words;
  return words.filter(
    (word) =>
      word.word.includes(trimmed) ||
      word.pinyin.toLowerCase().includes(trimmed) ||
      word.meaningVi.toLowerCase().includes(trimmed)
  );
}
