import type { StrokeOrderCharacterData } from "./types";

/**
 * Client-side loader for Stroke Order data. Characters are derived directly
 * from VocabularyWord.word at render time — no vocabulary JSON field is used
 * or required. See tools/hsk/stroke_order/README.md for the extraction
 * pipeline that produced app/public/stroke-data/<codepoint-hex>.json.
 */

// CJK Unified Ideographs + Ext-A + Compatibility Ideographs, matching the
// exact ranges used by the Python extraction/validation tooling.
const DIGIT_SUFFIX_RE = /^([㐀-䶿一-鿿豈-﫿]+)([1-9])$/;
const HAN_RE = /[㐀-䶿一-鿿豈-﫿]/;

/**
 * Splits a vocabulary word into the individual Han characters it needs
 * stroke data for, normalizing the 12 known digit-suffix records (e.g.
 * "局2" -> "局") to their real underlying character first. Any non-Han
 * character (should not occur in current production data) is dropped
 * rather than causing a lookup error.
 */
export function getCharactersForWord(word: string): string[] {
  const match = DIGIT_SUFFIX_RE.exec(word);
  const normalized = match ? match[1] ?? word : word;
  return Array.from(normalized).filter((ch) => HAN_RE.test(ch));
}

export function codepointFilename(character: string): string {
  const codePoint = character.codePointAt(0);
  return `${(codePoint ?? 0).toString(16)}.json`;
}

/**
 * Fetches one character's stroke data from the public static asset.
 * Throws on a missing/invalid asset — callers must catch and fall back to
 * an EmptyState rather than crash (current coverage is 1940/1940, but the
 * loader must still degrade gracefully for any future gap).
 */
export async function fetchStrokeOrderData(
  character: string
): Promise<StrokeOrderCharacterData> {
  const response = await fetch(`/stroke-data/${codepointFilename(character)}`);
  if (!response.ok) {
    throw new Error(`Stroke data not found for "${character}"`);
  }
  const data = (await response.json()) as StrokeOrderCharacterData;
  if (!Array.isArray(data.strokes) || data.strokes.length === 0) {
    throw new Error(`Malformed stroke data for "${character}"`);
  }
  return data;
}
