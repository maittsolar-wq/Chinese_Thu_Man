"use client";

import { useEffect, useMemo, useState } from "react";
import { VocabularyCard } from "@/components/vocabulary/VocabularyCard";
import { EmptyState } from "@/components/ui/EmptyState";
import { Pagination } from "@/components/ui/Pagination";
import { SearchIcon } from "@/components/ui/icons";
import { filterHskLevelVocabulary } from "@/lib/data/hskLevelFilter";
import type { VocabularyWord, HskLevel } from "@/lib/data/types";

/** Single constant, per the spec — change this to change every level's
 *  page size at once. */
const PAGE_SIZE = 50;

/**
 * Live search + pagination for one HSK level's vocabulary list. `words`
 * is that level's full pool (from `getVocabularyByLevel`, unchanged) —
 * search filters ONLY this array client-side, never touching the
 * Dictionary's global search or any other level's data, which is what
 * keeps this strictly level-scoped.
 *
 * The parent page renders this with `key={level}` so navigating between
 * HSK levels remounts it fresh (query cleared, page reset to 1) rather
 * than carrying state across a level change.
 */
export function HskLevelVocabularyList({
  words,
  level,
}: {
  words: VocabularyWord[];
  level: HskLevel;
}) {
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(1);

  const filtered = useMemo(() => filterHskLevelVocabulary(words, query), [words, query]);
  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const pageItems = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  // Any query change (including clearing it) restores page 1.
  useEffect(() => {
    setPage(1);
  }, [query]);

  return (
    <div className="flex flex-col gap-4">
      <div className="relative sm:max-w-md">
        <SearchIcon className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-500 dark:text-night-muted" />
        <input
          type="text"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder={`Tìm trong HSK ${level}...`}
          aria-label={`Tìm từ vựng trong HSK ${level}`}
          className="w-full rounded-md border border-neutral-300 bg-white py-2.5 pl-10 pr-4 text-base text-neutral-900 outline-none placeholder:text-neutral-500 focus:border-primary focus:ring-1 focus:ring-primary dark:border-night-border dark:bg-night-input dark:text-night-text dark:placeholder:text-night-muted"
        />
      </div>

      <p className="text-sm text-neutral-600 dark:text-night-muted">
        {filtered.length.toLocaleString("vi-VN")} từ vựng
      </p>

      {filtered.length === 0 ? (
        <EmptyState
          title="Không tìm thấy từ phù hợp"
          description="Hãy thử chữ Hán, pinyin hoặc nghĩa tiếng Việt khác."
        />
      ) : (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {pageItems.map((word) => (
            <VocabularyCard
              key={word.id}
              word={word}
              href={`/vocabulary/${word.id}?from=hsk&level=${level}`}
              currentLevel={level}
            />
          ))}
        </div>
      )}

      <Pagination currentPage={page} totalPages={totalPages} onPageChange={setPage} />
    </div>
  );
}
