"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { searchDictionaryAction } from "@/lib/dictionary/actions";
import { HSK_LEVEL_HEX } from "@/lib/hsk/homePalette";
import { SearchIcon, CloseIcon, ChevronRightIcon } from "@/components/ui/icons";
import type { HskLevel, VocabularyWord } from "@/lib/data/types";

const SEARCH_DEBOUNCE_MS = 150;
const RESULTS_PER_PAGE = 5;

/** Visual-refinement pass: exact 6 example words from the approved
 *  reference — a shortcut into the SAME search flow below (clicking one
 *  just calls `setQuery`, the existing debounced-search effect does the
 *  rest), not a second search path. */
const SEARCH_EXAMPLES = ["学习", "你好", "中国", "老师", "喜欢", "朋友"];

/**
 * Home Quick Search. Reuses the exact same `searchDictionaryAction`
 * server action DictionarySearchPopup already calls — no second search
 * engine.
 *
 * Pass 14: rebuilt as a titled feature card (icon + "Tra từ điển nhanh" +
 * subtitle + input), matching the approved Search reference's exact
 * copy — earlier passes (4, 8, 9, 11) had treated this as a bare compact
 * input with no title, based on a literal reading of those passes' own
 * text instructions ("remove the decorative header", "no title/subtitle
 * area"); Pass 14's text is now unambiguous and gives the literal copy,
 * so this supersedes that reading rather than fighting it again.
 *
 * The icon is the real supplied blue magnifying-glass asset
 * (app/public/icons/search-icon.png) — the reference shows it green, but
 * no green magnifying-glass asset was ever supplied (only white/dark/
 * blue variants extracted from the conversation); flagged in the pass
 * report rather than fabricating a recolored asset.
 *
 * Results still render as an OVERLAY (`position: absolute`, taken out of
 * normal flow) with a `position: fixed` dimming backdrop, not inline
 * content — the outer card's own box height (icon/title/subtitle/input)
 * never changes when a query is typed, so HSK/Radical/Practice never
 * shift.
 *
 * Pass 15: the results/empty panel is now nested inside the same
 * `max-w-[660px]` wrapper as the input (previously a sibling of the
 * whole card, sized to the card's full width) — it's a compact dropdown
 * anchored under the compact input, not a full-card-width box. See the
 * width comment further down for why.
 *
 * Visual fix pass (HOME VISUAL FIX PASS): the outer card itself used to
 * stretch to the full HOME_CONTENT_MAX_WIDTH column (1180px) even though
 * every bit of its content (icon/title/subtitle/input/chips/overlay) was
 * already capped at the inner 660px wrapper — leaving a large blank
 * white area to the right in both the empty and results states. The
 * card is now capped at 660px content + its own p-6 padding (708px
 * total), so it visually wraps its content instead of floating an
 * empty region next to it. The results overlay already measured itself
 * against the 660px inner wrapper (`inset-x-0` on that ancestor, not the
 * card), so narrowing the card also fixes the overlay's apparent
 * oversized feel with no change to overlay logic/positioning.
 */
export function HomeSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<VocabularyWord[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [page, setPage] = useState(1);
  const requestIdRef = useRef(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const trimmedQuery = query.trim();
  const hasQuery = trimmedQuery.length > 0;

  const clear = () => setQuery("");

  /** Example-chip shortcut: fills the existing controlled input, which
   *  the debounced-search effect below already reacts to — same search
   *  path a manually-typed query takes, not a second one. */
  function selectExample(word: string) {
    setQuery(word);
    inputRef.current?.focus();
  }

  // Escape closes the overlay, same as the clear button / backdrop click.
  useEffect(() => {
    if (!hasQuery) return;
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") clear();
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [hasQuery]);

  useEffect(() => {
    if (!hasQuery) {
      setResults([]);
      setIsSearching(false);
      return;
    }

    setIsSearching(true);
    const requestId = ++requestIdRef.current;
    const timer = setTimeout(() => {
      searchDictionaryAction(trimmedQuery).then((found) => {
        if (requestIdRef.current === requestId) {
          setResults(found);
          setIsSearching(false);
        }
      });
    }, SEARCH_DEBOUNCE_MS);

    return () => clearTimeout(timer);
  }, [trimmedQuery, hasQuery]);

  // A new query always restarts pagination at page 1.
  useEffect(() => {
    setPage(1);
  }, [trimmedQuery]);

  const totalPages = Math.max(1, Math.ceil(results.length / RESULTS_PER_PAGE));
  const visibleResults = useMemo(() => {
    const start = (page - 1) * RESULTS_PER_PAGE;
    return results.slice(start, start + RESULTS_PER_PAGE);
  }, [results, page]);

  // A broad single-letter query can match thousands of records (~900+
  // pages). Windowed to first/last + current±1 with "…" gaps.
  const pageTokens = useMemo(() => buildPageTokens(page, totalPages), [page, totalPages]);

  const showEmpty = hasQuery && !isSearching && results.length === 0;
  const showResults = hasQuery && results.length > 0;
  const showOverlay = showEmpty || showResults;

  return (
    // Pass 15: the outer white card spans the full HOME_CONTENT_MAX_WIDTH
    // column, same as HSK/Radical/Practice's own HomeSectionCard shell —
    // already true structurally, confirmed by measuring the rendered DOM
    // (both were already 1180px @ left:130px). What actually read as
    // "too narrow" was the INPUT itself filling nearly the whole card
    // (1130px, i.e. card-width minus its own padding) with no visible
    // compact shape of its own. The input (and its results dropdown) is
    // now wrapped in its own `max-w-[660px]` box nested inside the
    // full-width card — matching §5's diagram exactly: a wide card
    // containing a visibly narrower, self-contained input.
    <div className="relative w-full">
      {hasQuery && (
        <div aria-hidden onClick={clear} className="fixed inset-0 z-40 bg-black/40" />
      )}

      <div className="relative z-50 w-full max-w-[708px] rounded-2xl border border-[#E2E8F0] bg-white p-6 shadow-[0_2px_0_#E2E8F0] dark:border-[#3A3A3A] dark:bg-[#242424] dark:shadow-[0_2px_0_#3a3a3a]">
        <div className="flex items-center gap-3">
          <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#0152911A]">
            <Image src="/icons/search-icon.png" alt="" width={22} height={22} aria-hidden />
          </span>
          <div>
            <h2 className="font-ui text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC]">
              Tra từ điển nhanh
            </h2>
            <p className="font-ui text-sm text-[#343536] dark:text-[#94A3B8]">
              Nhập chữ Hán để tra cứu từ vựng HSK.
            </p>
          </div>
        </div>

        <div className="relative mt-4 max-w-[660px]">
          {/* Icon/input/clear-button get their own positioning context so
              the clear button's vertical centering only ever measures
              against the input's own height — the example-chip row below
              is a normal-flow sibling of this wrapper, not inside it, so
              it can't shift that centering. */}
          <div className="relative">
            <SearchIcon className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-[#94A3B8]" />
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Nhập chữ Hán, pinyin, bộ thủ ..."
              aria-label="Tìm kiếm từ vựng"
              className="font-ui h-14 w-full rounded-2xl border border-[#E2E8F0] bg-white pl-12 pr-12 text-[16px] text-[#0F172A] outline-none placeholder:text-[#94A3B8] focus:border-[#025291] dark:border-[#3A3A3A] dark:bg-[#1a1a1a] dark:text-[#F8FAFC]"
            />
            {hasQuery && (
              <button
                type="button"
                aria-label="Xóa tìm kiếm"
                onClick={clear}
                className="absolute right-4 top-1/2 flex h-7 w-7 -translate-y-1/2 items-center justify-center rounded-full text-[#94A3B8] transition-colors hover:bg-neutral-100 dark:hover:bg-white/10"
              >
                <CloseIcon className="h-4 w-4" />
              </button>
            )}
          </div>

          {/* Example chips (visual-refinement pass) — a shortcut into the
              exact same controlled `query` state/debounced-search effect
              above, always visible (own normal-flow row, not part of the
              results overlay), so the card's own height above the overlay
              never changes based on search state. */}
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <span className="font-ui shrink-0 text-sm text-neutral-500 dark:text-[#94A3B8]">Ví dụ:</span>
            {SEARCH_EXAMPLES.map((example) => (
              <button
                key={example}
                type="button"
                onClick={() => selectExample(example)}
                className="font-cjk rounded-full bg-[#0152911A] px-3.5 py-1.5 text-sm text-[#025291] transition-colors hover:bg-[#01529133] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#025291] focus-visible:ring-offset-1 dark:bg-primary-dark/30 dark:text-night-primary dark:hover:bg-primary-dark/50"
              >
                {example}
              </button>
            ))}
          </div>

          {showOverlay && (
          <div className="absolute inset-x-0 top-full z-50 mt-3 max-h-[min(70vh,620px)] overflow-y-auto rounded-2xl border border-[#E2E8F0] bg-white p-5 text-left shadow-[0_2px_0_#E2E8F0] dark:border-[#3A3A3A] dark:bg-[#242424] dark:shadow-[0_2px_0_#3a3a3a]">
            {showEmpty && (
              <div className="flex flex-col items-center gap-2 py-6 text-center">
                <span className="flex h-12 w-12 items-center justify-center rounded-full bg-neutral-100 text-neutral-400 dark:bg-white/10 dark:text-[#94A3B8]">
                  <SearchIcon className="h-5 w-5" />
                </span>
                <p className="font-ui text-base font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  Không tìm thấy kết quả phù hợp
                </p>
                <p className="font-ui text-sm text-neutral-600 dark:text-[#94A3B8]">Hãy thử tìm với từ khóa khác</p>
              </div>
            )}

            {showResults && (
              <div className="flex flex-col gap-4">
                <p className="font-ui text-base font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  Kết quả tìm kiếm ({results.length.toLocaleString("vi-VN")})
                </p>

                <div className="flex flex-col gap-3">
                  {visibleResults.map((word, index) => (
                    <HomeSearchResultRow
                      key={`${word.id}-${index}`}
                      word={word}
                      level={word.hskLevels[0] as HskLevel | undefined}
                    />
                  ))}
                </div>

                {totalPages > 1 && (
                  <div className="flex flex-wrap items-center justify-center gap-2 pt-2">
                    {pageTokens.map((token, index) =>
                      token === "ellipsis" ? (
                        <span
                          key={`ellipsis-${index}`}
                          className="flex h-10 w-10 items-center justify-center text-sm text-neutral-400 dark:text-[#94A3B8]"
                        >
                          …
                        </span>
                      ) : (
                        <button
                          key={token}
                          type="button"
                          onClick={() => setPage(token)}
                          aria-current={token === page ? "page" : undefined}
                          className={
                            token === page
                              ? "flex h-10 w-10 items-center justify-center rounded-lg bg-[#015291] text-sm font-semibold text-white"
                              : "flex h-10 w-10 items-center justify-center rounded-lg border border-[#E2E8F0] text-sm font-medium text-neutral-700 transition-colors hover:bg-neutral-50 dark:border-[#3A3A3A] dark:text-[#F8FAFC] dark:hover:bg-white/10"
                          }
                        >
                          {token}
                        </button>
                      )
                    )}
                    <button
                      type="button"
                      aria-label="Trang sau"
                      disabled={page >= totalPages}
                      onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                      className="flex h-10 w-10 items-center justify-center rounded-lg border border-[#E2E8F0] text-neutral-700 transition-colors hover:bg-neutral-50 disabled:cursor-not-allowed disabled:opacity-40 dark:border-[#3A3A3A] dark:text-[#F8FAFC] dark:hover:bg-white/10"
                    >
                      <ChevronRightIcon className="h-4 w-4" />
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
          )}
        </div>
      </div>
    </div>
  );
}

function HomeSearchResultRow({ word, level }: { word: VocabularyWord; level?: HskLevel }) {
  return (
    <Link
      href={`/vocabulary/${word.id}?from=dictionary`}
      className="flex items-center justify-between gap-5 rounded-2xl border border-[#E2E8F0] px-6 py-5 transition-colors hover:bg-neutral-50 dark:border-[#3A3A3A] dark:hover:bg-white/5"
    >
      <span className="font-cjk shrink-0 text-[30px] font-semibold leading-none text-[#0F172A] dark:text-[#F8FAFC]">
        {word.word}
      </span>
      <span className="flex min-w-0 flex-1 flex-col gap-0.5">
        <span className="font-ui truncate text-base italic text-primary dark:text-night-primary">{word.pinyin}</span>
        <span className="font-ui truncate text-base text-neutral-800 dark:text-[#F8FAFC]">{word.meaningVi}</span>
      </span>
      {level !== undefined && (
        <span
          className="font-ui shrink-0 rounded-full px-4 py-1.5 text-sm font-semibold"
          style={{ backgroundColor: `${HSK_LEVEL_HEX[level]}1A`, color: HSK_LEVEL_HEX[level] }}
        >
          HSK{level}
        </span>
      )}
    </Link>
  );
}

type PageToken = number | "ellipsis";

/** First page, last page, and a small window around the current page —
 *  everything else collapses to a single "…" token. See the pageTokens
 *  comment above for why this exists. */
function buildPageTokens(current: number, total: number): PageToken[] {
  const windowStart = Math.max(2, current - 1);
  const windowEnd = Math.min(total - 1, current + 1);

  const tokens: PageToken[] = [1];
  if (windowStart > 2) tokens.push("ellipsis");
  for (let p = windowStart; p <= windowEnd; p++) tokens.push(p);
  if (windowEnd < total - 1) tokens.push("ellipsis");
  if (total > 1) tokens.push(total);
  return tokens;
}
