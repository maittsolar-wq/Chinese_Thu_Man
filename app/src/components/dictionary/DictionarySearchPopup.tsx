"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useDictionarySearch } from "./DictionarySearchProvider";
import { searchDictionaryAction } from "@/lib/dictionary/actions";
import { VocabularyCard } from "@/components/vocabulary/VocabularyCard";
import { EmptyState } from "@/components/ui/EmptyState";
import { SearchIcon, CloseIcon } from "@/components/ui/icons";
import type { VocabularyWord } from "@/lib/data/types";

const SEARCH_DEBOUNCE_MS = 150;
/** Popup stays compact; "Xem tất cả" hands off the full list to the
 *  existing /dictionary page rather than the popup growing unbounded. */
const DISPLAY_LIMIT = 20;

export function DictionarySearchPopup() {
  const { isOpen, close } = useDictionarySearch();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<VocabularyWord[]>([]);
  const [isSearching, setIsSearching] = useState(false);
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
    }
  }, [isOpen]);

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
  const showNoResults = hasQuery && !isSearching && results.length === 0;
  const showResults = hasQuery && results.length > 0;
  const visibleResults = results.slice(0, DISPLAY_LIMIT);

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
          <h2 className="text-xl font-bold text-primary">TỪ ĐIỂN</h2>
          <p className="text-sm text-neutral-600 dark:text-night-muted">
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
            className="w-full rounded-md border border-neutral-300 bg-white py-2.5 pl-10 pr-4 text-base text-neutral-900 outline-none placeholder:text-neutral-500 focus:border-primary focus:ring-1 focus:ring-primary dark:border-night-border dark:bg-night-input dark:text-night-text dark:placeholder:text-night-muted"
          />
        </div>

        <div className="max-h-[60vh] overflow-y-auto">
          {!hasQuery && (
            <EmptyState title="Nhập từ khóa để bắt đầu tra cứu." />
          )}

          {showNoResults && (
            <EmptyState
              title="Không tìm thấy từ phù hợp"
              description="Hãy thử chữ Hán, pinyin hoặc nghĩa tiếng Việt khác."
            />
          )}

          {showResults && (
            <div className="flex flex-col gap-3">
              <p className="text-sm text-neutral-600 dark:text-night-muted">
                Tìm thấy {results.length.toLocaleString("vi-VN")} kết quả
              </p>
              <div className="grid gap-3 sm:grid-cols-2">
                {visibleResults.map((word) => (
                  <div key={word.id} onClick={close}>
                    <VocabularyCard
                      word={word}
                      href={`/vocabulary/${word.id}?from=dictionary`}
                      showAllLevels
                    />
                  </div>
                ))}
              </div>
              {results.length > DISPLAY_LIMIT && (
                <Link
                  href={`/dictionary?q=${encodeURIComponent(trimmedQuery)}`}
                  onClick={close}
                  className="text-center text-sm font-medium text-primary hover:underline"
                >
                  Xem tất cả {results.length.toLocaleString("vi-VN")} kết quả trên trang Từ điển
                </Link>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
