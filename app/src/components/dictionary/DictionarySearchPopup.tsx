"use client";

import { useEffect, useRef, useState } from "react";
import { useDictionarySearch } from "./DictionarySearchProvider";
import { searchDictionaryAction } from "@/lib/dictionary/actions";
import { VocabularyCard } from "@/components/vocabulary/VocabularyCard";
import { EmptyState } from "@/components/ui/EmptyState";
import { SearchPagination } from "@/components/search/SearchPagination";
import { SearchIcon, CloseIcon } from "@/components/ui/icons";
import type { VocabularyWord } from "@/lib/data/types";

const SEARCH_DEBOUNCE_MS = 150;
/**
 * In-popup pagination pass: previously the popup showed only the first
 * `DISPLAY_LIMIT` (20) results with a "Xem tất cả... trên trang Tra cứu"
 * link handing off to /dictionary — a second, separate full-page search
 * screen. That hand-off is gone; results now paginate *inside* this same
 * popup (reusing HomeSearch's own pagination control/logic, see
 * `SearchPagination`/`buildPageTokens`), so the popup never navigates
 * away. `RESULTS_PER_PAGE` keeps the exact same per-page count (20) the
 * popup already showed, per the "preserve current visible cards per
 * page" requirement — only the constant's name changed to reflect its
 * new role.
 */
const RESULTS_PER_PAGE = 20;

export function DictionarySearchPopup() {
  const { isOpen, close } = useDictionarySearch();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<VocabularyWord[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [page, setPage] = useState(1);
  const inputRef = useRef<HTMLInputElement>(null);
  const requestIdRef = useRef(0);

  // Reset to a clean state every time the popup closes, so reopening (from
  // either entry point) always starts from the empty initial state rather
  // than a stale previous query/result list.
  useEffect(() => {
    if (!isOpen) {
      setQuery("");
      setResults([]);
      setIsSearching(false);
      setPage(1);
    }
  }, [isOpen]);

  // A new query always restarts pagination at page 1 (same as HomeSearch).
  useEffect(() => {
    setPage(1);
  }, [query]);

  // Focus the input as soon as the popup opens.
  useEffect(() => {
    if (isOpen) inputRef.current?.focus();
  }, [isOpen]);

  // Escape closes the popup.
  useEffect(() => {
    if (!isOpen) return;
    function handleKey(event: KeyboardEvent) {
      if (event.key === "Escape") close();
    }
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [isOpen, close]);

  // Prevent the page behind the popup from scrolling while it's open.
  useEffect(() => {
    if (!isOpen) return;
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previous;
    };
  }, [isOpen]);

  // Live search-as-you-type: debounced, with stale-response guarding so a
  // fast typer never has an earlier query's results clobber a later one.
  useEffect(() => {
    const trimmed = query.trim();
    if (!trimmed) {
      setResults([]);
      setIsSearching(false);
      return;
    }

    setIsSearching(true);
    const requestId = ++requestIdRef.current;
    const timer = setTimeout(() => {
      searchDictionaryAction(trimmed).then((found) => {
        if (requestIdRef.current === requestId) {
          setResults(found);
          setIsSearching(false);
        }
      });
    }, SEARCH_DEBOUNCE_MS);

    return () => clearTimeout(timer);
  }, [query]);

  if (!isOpen) return null;

  const trimmedQuery = query.trim();
  const hasQuery = trimmedQuery.length > 0;
  // Search Results visual-fix pass: matches Home Search's own `clear`
  // exactly (HomeSearch.tsx) — plain `setQuery("")`, no explicit refocus,
  // since that's what Home Search itself does.
  const clear = () => setQuery("");
  const showNoResults = hasQuery && !isSearching && results.length === 0;
  const showResults = hasQuery && results.length > 0;
  const totalPages = Math.max(1, Math.ceil(results.length / RESULTS_PER_PAGE));
  const visibleResults = results.slice((page - 1) * RESULTS_PER_PAGE, page * RESULTS_PER_PAGE);

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto p-4 sm:items-center sm:p-6">
      {/* Overlay — dims the page behind; clicking it closes the popup. */}
      <button
        type="button"
        aria-label="Đóng tìm kiếm"
        onClick={close}
        className="fixed inset-0 cursor-default bg-neutral-900/40 dark:bg-black/60"
      />

      {/* Panel — stopPropagation so clicks inside never bubble to the overlay. */}
      <div
        role="dialog"
        aria-modal="true"
        aria-label="Tìm kiếm từ điển"
        onClick={(event) => event.stopPropagation()}
        className="relative z-10 flex w-full max-w-xl flex-col gap-4 rounded-card border border-neutral-200 bg-white p-6 shadow-card dark:border-night-border dark:bg-night-surface sm:p-8"
      >
        <button
          type="button"
          aria-label="Đóng"
          onClick={close}
          className="absolute right-4 top-4 flex h-8 w-8 items-center justify-center rounded-full text-neutral-500 transition-colors hover:bg-neutral-100 dark:text-night-muted dark:hover:bg-night-input"
        >
          <CloseIcon className="h-4 w-4" />
        </button>

        <div className="flex flex-col gap-1 pr-8">
          <h2 className="font-ui text-xl font-bold text-primary dark:text-night-primary">
            Tra từ tiếng Trung
          </h2>
          <p className="font-ui text-sm text-neutral-600 dark:text-night-muted">
            Tra cứu chữ Hán, pinyin, từ vựng tiếng Trung hoặc 214 bộ thủ.
          </p>
        </div>

        <div className="relative">
          <SearchIcon className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-500 dark:text-night-muted" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Nhập chữ Hán, pinyin, bộ thủ ..."
            aria-label="Tìm kiếm từ vựng"
            className="font-ui w-full rounded-md border border-neutral-300 bg-white py-2.5 pl-10 pr-10 text-base text-neutral-900 outline-none placeholder:text-neutral-500 focus:border-primary focus:ring-1 focus:ring-primary dark:border-night-border dark:bg-night-input dark:text-night-text dark:placeholder:text-night-muted"
          />
          {hasQuery && (
            <button
              type="button"
              aria-label="Xóa tìm kiếm"
              onClick={clear}
              className="absolute right-3 top-1/2 flex h-6 w-6 -translate-y-1/2 items-center justify-center rounded-full text-neutral-500 transition-colors hover:bg-neutral-100 dark:text-night-muted dark:hover:bg-night-input"
            >
              <CloseIcon className="h-4 w-4" />
            </button>
          )}
        </div>

        <div className="max-h-[60vh] overflow-y-auto">
          {!hasQuery && (
            <EmptyState title="Nhập từ khóa để bắt đầu tra cứu." />
          )}

          {/* Phase 06: the ~150ms debounce window previously rendered
              nothing at all (isSearching was tracked but never displayed) —
              a real gap for this phase's required loading-state design. */}
          {hasQuery && isSearching && (
            <EmptyState title="Đang tìm..." />
          )}

          {showNoResults && (
            <EmptyState
              title="Không tìm thấy từ phù hợp"
              description="Hãy thử chữ Hán, pinyin hoặc nghĩa tiếng Việt khác."
            />
          )}

          {showResults && (
            <div className="flex flex-col gap-3">
              <p className="font-ui text-sm text-neutral-600 dark:text-night-muted">
                Tìm thấy {results.length.toLocaleString("vi-VN")} kết quả
              </p>
              <div className="grid gap-3 sm:grid-cols-2">
                {visibleResults.map((word) => (
                  <VocabularyCard
                    key={word.id}
                    word={word}
                    href={`/vocabulary/${word.id}?from=dictionary`}
                    showAllLevels
                    onClick={close}
                  />
                ))}
              </div>
              <SearchPagination page={page} totalPages={totalPages} onPageChange={setPage} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
