import { searchVocabulary, getVocabularyById } from "./vocabularyRepository";
import { searchRadicals, getVocabularyIdsForRadical } from "./radicalRepository";
import type { VocabularyWord } from "./types";

/**
 * The Dictionary Search Popup's combined search — used ONLY by the popup
 * (via dictionary/actions.ts), never by the existing /dictionary full page
 * (which keeps calling `searchVocabulary` directly, unchanged, so its
 * behavior is provably identical to before this file existed).
 *
 * Two independent, unmodified searches are combined here rather than
 * merged into either one:
 *   1. `searchVocabulary` (chinese/pinyin/meaning) — exact behavior
 *      preserved, first in the returned order.
 *   2. `searchRadicals` (radical glyph/pinyin/name/meaning) — resolved
 *      separately against the radical dataset's OWN fields, then expanded
 *      to that radical's mapped vocabulary via the existing
 *      radical_vocabulary_mapping.json (through getVocabularyIdsForRadical).
 *
 * This separation is what guarantees an ordinary vocabulary pinyin
 * substring match (e.g. many words happen to contain "shou") can never be
 * misclassified as a radical match: radical resolution never looks at
 * vocabulary fields, and vocabulary resolution never looks at radical
 * fields. Results are deduplicated by vocabulary id, direct matches first.
 */
export function searchDictionary(query: string): VocabularyWord[] {
  const trimmed = query.trim();
  if (!trimmed) return [];

  const direct = searchVocabulary(trimmed);
  const seen = new Set(direct.map((word) => word.id));

  const matchedRadicals = searchRadicals(trimmed);
  const radicalWords: VocabularyWord[] = [];
  for (const radical of matchedRadicals) {
    for (const vocabularyId of getVocabularyIdsForRadical(radical.id)) {
      if (seen.has(vocabularyId)) continue;
      seen.add(vocabularyId);
      const word = getVocabularyById(vocabularyId);
      if (word) radicalWords.push(word);
    }
  }

  return [...direct, ...radicalWords];
}
