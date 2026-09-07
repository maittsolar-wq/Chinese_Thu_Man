"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { searchDictionaryAction } from "@/lib/dictionary/actions";
import { HSK_LEVEL_HEX } from "@/lib/hsk/homePalette";
import { SearchIcon, CloseIcon, ChevronRightIcon } from "@/components/ui/icons";
import type { HskLevel, VocabularyWord } from "@/lib/data/types";

const SEARCH_DEBOUNCE_MS = 150;
const RESULTS_PER_PAGE = 5;

/**
 * Home Quick Search — Pass 04: its own section between Hero and HSK
 * (previously lived inside Hero), full content-grid width. Reuses the
 * exact same `searchDictionaryAction` server action DictionarySearchPopup
 * already calls — no second search engine.
 *
 * When active, results render as an OVERLAY (`position: absolute`, taken
 * out of normal flow) with a `position: fixed` dimming backdrop behind
 * it, rather than inline content that would grow this section's own
 * height. That's what keeps HSK/Radical/Practice from ever shifting when
 * a query is typed — this section's own box height is just the input
 * (56/64px), never the results panel, regardless of result count.
 */
export function HomeSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<VocabularyWord[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [page, setPage] = useState(1);
  const requestIdRef = useRef(0);

  const trimmedQuery = query.trim();
  const hasQuery = trimmedQuery.length > 0;

  const clear = () => setQuery("");

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
    // Width/alignment is deliberately NOT set here — the caller
    // (page.tsx) places this component directly inside the same
    // `HOME_CONTENT_MAX_WIDTH` column HSK/Radical/Practice use, so this
    // section takes on that exact width as an ordinary flex/block child
    // rather than duplicating (and risking double-padding) that layout
    // logic here. §8's "identical left/right alignment" requirement.
    <div className="relative w-full">
      {hasQuery && (
        <div
          aria-hidden
          onClick={clear}
          className="fixed inset-0 z-40 bg-black/40"
        />
      )}

      <div className="relative z-50">
        <div className="relative">
          <SearchIcon className="pointer-events-none absolute left-5 top-1/2 h-5 w-5 -translate-y-1/2 text-neutral-500" />
          <input
            type="text"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Nhập chữ Hán, pinyin, bộ thủ ..."
            aria-label="Tìm kiếm từ vựng"
            className="font-ui h-14 w-full rounded-2xl border-2 border-neutral-200 bg-white pl-14 pr-14 text-[16px] text-neutral-900 shadow-[0_10px_0_#E2E8F0] outline-none placeholder:text-neutral-500 focus:border-[#025291] sm:h-16"
          />
          {hasQuery && (
            <button
              type="button"
              aria-label="Xóa tìm kiếm"
              onClick={clear}
              className="absolute right-5 top-1/2 flex h-7 w-7 -translate-y-1/2 items-center justify-center rounded-full text-neutral-500 transition-colors hover:bg-neutral-100"
            >
              <CloseIcon className="h-4 w-4" />
            </button>
          )}
        </div>

        {showOverlay && (
          <div className="absolute inset-x-0 top-full z-50 mt-4 max-h-[min(70vh,620px)] overflow-y-auto rounded-2xl border border-neutral-200 bg-white p-7 text-left shadow-[0_10px_0_#E2E8F0]">
            {showEmpty && (
              <div className="flex flex-col items-center gap-3 py-12 text-center">
                <span className="flex h-16 w-16 items-center justify-center rounded-full bg-neutral-100 text-neutral-400">
                  <SearchIcon className="h-7 w-7" />
                </span>
                <p className="font-ui text-lg font-semibold text-neutral-900">
                  Không tìm thấy kết quả phù hợp
                </p>
                <p className="font-ui text-base text-neutral-600">Hãy thử tìm với từ khóa khác</p>
              </div>
            )}

            {showResults && (
              <div className="flex flex-col gap-4">
                <p className="font-ui text-base font-semibold text-neutral-900">
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
                          className="flex h-10 w-10 items-center justify-center text-sm text-neutral-400"
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
                              : "flex h-10 w-10 items-center justify-center rounded-lg border border-neutral-200 text-sm font-medium text-neutral-700 transition-colors hover:bg-neutral-50"
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
                      className="flex h-10 w-10 items-center justify-center rounded-lg border border-neutral-200 text-neutral-700 transition-colors hover:bg-neutral-50 disabled:cursor-not-allowed disabled:opacity-40"
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
  );
}

function HomeSearchResultRow({ word, level }: { word: VocabularyWord; level?: HskLevel }) {
  return (
    <Link
      href={`/vocabulary/${word.id}?from=dictionary`}
      className="flex items-center justify-between gap-5 rounded-2xl border border-neutral-200 px-6 py-5 transition-colors hover:bg-neutral-50"
    >
      <span className="font-cjk shrink-0 text-[30px] font-semibold leading-none text-neutral-900">
        {word.word}
      </span>
      <span className="flex min-w-0 flex-1 flex-col gap-0.5">
        <span className="font-ui truncate text-base italic text-primary">{word.pinyin}</span>
        <span className="font-ui truncate text-base text-neutral-800">{word.meaningVi}</span>
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
