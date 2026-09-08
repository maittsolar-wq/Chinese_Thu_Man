/**
 * Extracted from HomeSearch.tsx (Pass 04+) so DictionarySearchPopup can
 * reuse the exact same windowing logic instead of a second copy — a
 * broad single-letter query can match thousands of records (~900+
 * pages), and rendering one button per page in that case would mean
 * hundreds of DOM nodes plus literal horizontal overflow. Windowed to
 * first/last + current±1 with "…" gaps, same fixed-size buttons either
 * surface renders.
 */
export type PageToken = number | "ellipsis";

export function buildPageTokens(current: number, total: number): PageToken[] {
  const windowStart = Math.max(2, current - 1);
  const windowEnd = Math.min(total - 1, current + 1);

  const tokens: PageToken[] = [1];
  if (windowStart > 2) tokens.push("ellipsis");
  for (let p = windowStart; p <= windowEnd; p++) tokens.push(p);
  if (windowEnd < total - 1) tokens.push("ellipsis");
  if (total > 1) tokens.push(total);
  return tokens;
}
