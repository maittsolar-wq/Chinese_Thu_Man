import fs from "node:fs";
import { memoizeOnce } from "./memoize";
import {
  RADICALS_PATH,
  RADICAL_DETAIL_PATH,
  RADICAL_VOCABULARY_MAPPING_PATH,
} from "./paths";
import {
  buildRadicalDetail,
  normalizeRadicalSummary,
  type RawRadicalDetail,
  type RawRadicalSummary,
  type RawRadicalVocabularyMapping,
} from "./radicalAdapter";
import { getVocabularyById } from "./vocabularyRepository";
import { filterRadicals } from "./radicalSearch";
import type { RadicalDetail, RadicalSummary } from "./types";

function readJson<T>(filePath: string): T {
  return JSON.parse(fs.readFileSync(filePath, "utf-8"));
}

const loadRadicalSummaries = memoizeOnce((): RadicalSummary[] => {
  const raw = readJson<RawRadicalSummary[]>(RADICALS_PATH);
  return raw.map(normalizeRadicalSummary);
});

const loadRadicalDetails = memoizeOnce((): Map<string, RawRadicalDetail> => {
  const raw = readJson<RawRadicalDetail[]>(RADICAL_DETAIL_PATH);
  return new Map(raw.map((entry) => [entry.radicalId, entry]));
});

const loadRadicalVocabularyMappings = memoizeOnce(
  (): Map<string, RawRadicalVocabularyMapping> => {
    const raw = readJson<RawRadicalVocabularyMapping[]>(
      RADICAL_VOCABULARY_MAPPING_PATH
    );
    return new Map(raw.map((entry) => [entry.radicalId, entry]));
  }
);

export function getAllRadicals(): RadicalSummary[] {
  return loadRadicalSummaries();
}

export function getRadicalSummaryById(id: string): RadicalSummary | null {
  return loadRadicalSummaries().find((radical) => radical.id === id) ?? null;
}

/**
 * Joins radicals_214.json (meaningVi/strokeCount live here) with
 * radical_detail_data.json (character list) and
 * radical_vocabulary_mapping.json (vocabulary grouped by HSK level) on
 * radicalId, then resolves each vocabulary reference's meaningVi through
 * the canonical vocabulary repository rather than trusting the mapping
 * file's own (always-null) meaning/strokes fields.
 */
export function getRadicalDetailById(id: string): RadicalDetail | null {
  const summary = getRadicalSummaryById(id);
  const detail = loadRadicalDetails().get(id);
  const vocabularyMapping = loadRadicalVocabularyMappings().get(id);

  if (!summary || !detail || !vocabularyMapping) return null;

  return buildRadicalDetail(summary, detail, vocabularyMapping, (vocabularyId) => {
    return getVocabularyById(vocabularyId)?.meaningVi ?? null;
  });
}

export function getRadicalsWithNoVocabulary(): RadicalSummary[] {
  const mappings = loadRadicalVocabularyMappings();
  return loadRadicalSummaries().filter(
    (radical) => (mappings.get(radical.id)?.vocabularyCount ?? 0) === 0
  );
}

export function getRadicalVocabularyCount(id: string): number {
  return loadRadicalVocabularyMappings().get(id)?.vocabularyCount ?? 0;
}

/** Every vocabulary id mapped to this radical, across all HSK levels,
 *  from the existing radical_vocabulary_mapping.json — no new mapping
 *  data, just flattening the per-level grouping already loaded above. */
export function getVocabularyIdsForRadical(radicalId: string): string[] {
  const mapping = loadRadicalVocabularyMappings().get(radicalId);
  if (!mapping) return [];
  return Object.values(mapping.vocabularyByLevel).flatMap((entries) =>
    entries.map((entry) => entry.vocabularyId)
  );
}

/**
 * Reverse index of the same radical_vocabulary_mapping.json already loaded
 * above (radicalId -> vocabulary entries), rebuilt as vocabularyId ->
 * radicalIds. A vocabulary word can contain more than one character (e.g.
 * "不客气" carries three, each under a different radical), and — confirmed
 * against the raw mapping data — the same radical can legitimately appear
 * more than once for a single word when two of its characters share a
 * radical (e.g. "一下"'s "一" and "下" both fall under radical_001), so
 * this dedups per word while iterating radicals in their existing
 * getAllRadicals()/kangxiIndex order for a stable, deterministic result.
 * No new file is read and no parsing logic is duplicated — this is a
 * pure in-memory reshaping of loadRadicalVocabularyMappings().
 */
const loadVocabularyRadicalIndex = memoizeOnce((): Map<string, string[]> => {
  const index = new Map<string, string[]>();
  for (const summary of loadRadicalSummaries()) {
    const mapping = loadRadicalVocabularyMappings().get(summary.id);
    if (!mapping) continue;
    for (const entries of Object.values(mapping.vocabularyByLevel)) {
      for (const entry of entries) {
        const radicalIds = index.get(entry.vocabularyId) ?? [];
        if (!radicalIds.includes(summary.id)) radicalIds.push(summary.id);
        index.set(entry.vocabularyId, radicalIds);
      }
    }
  }
  return index;
});

/**
 * All radicals associated with a vocabulary word, resolved through the
 * same radical_vocabulary_mapping.json / getRadicalSummaryById() already
 * used by Radical Detail — never a second/parallel data source. Returns
 * [] when the word has no mapping (none currently exists in production
 * data, but the function stays defensive for words added later).
 */
export function getRadicalsForVocabularyId(vocabularyId: string): RadicalSummary[] {
  const radicalIds = loadVocabularyRadicalIndex().get(vocabularyId) ?? [];
  return radicalIds
    .map((id) => getRadicalSummaryById(id))
    .filter((radical): radical is RadicalSummary => radical !== null);
}

/**
 * Resolves a query against the radical dataset's OWN identifying fields
 * only (glyph, variants, pinyin, Vietnamese name, Vietnamese meaning) —
 * never against vocabulary fields, which is what keeps an ordinary
 * vocabulary pinyin substring match from ever being misclassified as a
 * radical match. The actual matching/ranking logic lives in the
 * environment-agnostic radicalSearch.ts (`filterRadicals`), shared as-is
 * with /radicals's own client-side live search (RadicalIndexView) — this
 * function just supplies the `fs`-loaded data and preserves this module's
 * existing "empty query → []" contract for its callers (e.g.
 * dictionarySearch.ts's searchDictionary, which cross-searches radicals to
 * expand the Dictionary popup's results — unrelated to and unaffected by
 * the /dictionary page's own "Bộ thủ" teaser section).
 */
export function searchRadicals(query: string): RadicalSummary[] {
  if (!query.trim()) return [];
  return filterRadicals(loadRadicalSummaries(), query);
}
