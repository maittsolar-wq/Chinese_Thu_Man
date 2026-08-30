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
 * Resolves a query against the radical dataset's OWN identifying fields
 * only (glyph, variants, pinyin, Vietnamese name, Vietnamese meaning) —
 * never against vocabulary fields, which is what keeps an ordinary
 * vocabulary pinyin substring match from ever being misclassified as a
 * radical match. The actual matching/ranking logic lives in the
 * environment-agnostic radicalSearch.ts (`filterRadicals`), shared as-is
 * with the client-side live "Bộ thủ (214)" search on the Dictionary main
 * screen — this function just supplies the `fs`-loaded data and preserves
 * this module's existing "empty query → []" contract for its callers
 * (e.g. dictionarySearch.ts's searchDictionary).
 */
export function searchRadicals(query: string): RadicalSummary[] {
  if (!query.trim()) return [];
  return filterRadicals(loadRadicalSummaries(), query);
}
