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
