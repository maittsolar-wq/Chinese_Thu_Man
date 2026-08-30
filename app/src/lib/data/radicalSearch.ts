import type { RadicalSummary } from "./types";

/**
 * Pure, environment-agnostic radical filtering/grouping — no `fs`, no
 * server-only imports, safe to import from a "use client" component.
 *
 * This exists specifically so the live "Bộ thủ (214)" search on the
 * Dictionary main screen can filter client-side (all 214 radicals fit
 * trivially in memory, so there's no need for a server round-trip the way
 * vocabulary search needs one) WITHOUT reimplementing the matching logic —
 * `radicalRepository.ts`'s `searchRadicals` delegates to `filterRadicals`
 * below, so server and client share the exact same ranking, never two
 * divergent radical-search implementations.
 */

function normalizeSearchText(value: string): string {
  return value.trim().toLowerCase().replace(/\s+/g, " ");
}

/** Strips Pinyin tone marks so "shui" matches a radical whose pinyin is "shuǐ". */
function stripToneMarks(value: string): string {
  return value.normalize("NFD").replace(/[̀-ͯ]/g, "");
}

/**
 * Resolves a query against the radical dataset's OWN identifying fields
 * only (glyph, its written variants, pinyin, Vietnamese name, Vietnamese
 * meaning) — exact → prefix → substring ranking, same philosophy as
 * vocabularyRepository's searchVocabulary, scoped to radical fields.
 */
export function filterRadicals(all: RadicalSummary[], query: string): RadicalSummary[] {
  const trimmed = normalizeSearchText(query);
  if (!trimmed) return all;

  const trimmedNoTones = stripToneMarks(trimmed);

  const scored = all
    .map((radical) => {
      const glyphs = [radical.radical, ...radical.variants];
      const pinyin = normalizeSearchText(radical.pinyin);
      const pinyinNoTones = stripToneMarks(pinyin);
      const nameVi = normalizeSearchText(radical.nameVi);
      const meaningVi = normalizeSearchText(radical.meaningVi);

      let rank = -1;
      if (glyphs.includes(trimmed)) rank = 0;
      else if (pinyin === trimmed || pinyinNoTones === trimmedNoTones) rank = 1;
      else if (nameVi === trimmed || meaningVi === trimmed) rank = 2;
      else if (pinyin.startsWith(trimmed) || nameVi.startsWith(trimmed) || meaningVi.startsWith(trimmed))
        rank = 3;
      else if (
        glyphs.some((glyph) => glyph.includes(trimmed)) ||
        pinyin.includes(trimmed) ||
        pinyinNoTones.includes(trimmedNoTones) ||
        nameVi.includes(trimmed) ||
        meaningVi.includes(trimmed)
      )
        rank = 4;

      return { radical, rank };
    })
    .filter((entry) => entry.rank >= 0);

  scored.sort((a, b) => a.rank - b.rank || a.radical.id.localeCompare(b.radical.id));

  return scored.map((entry) => entry.radical);
}

export interface RadicalStrokeGroup {
  strokeCount: number;
  radicals: RadicalSummary[];
}

/** Groups radicals by stroke count, ascending — "1 nét (2)", "2 nét (14)", ... */
export function groupRadicalsByStrokeCount(radicals: RadicalSummary[]): RadicalStrokeGroup[] {
  const byStroke = new Map<number, RadicalSummary[]>();
  for (const radical of radicals) {
    const group = byStroke.get(radical.strokeCount);
    if (group) group.push(radical);
    else byStroke.set(radical.strokeCount, [radical]);
  }
  return Array.from(byStroke.entries())
    .sort(([a], [b]) => a - b)
    .map(([strokeCount, group]) => ({ strokeCount, radicals: group }));
}
