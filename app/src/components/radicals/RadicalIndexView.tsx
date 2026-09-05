"use client";

import { useEffect, useMemo, useState } from "react";
import { RadicalCard } from "@/components/radicals/RadicalCard";
import { EmptyState } from "@/components/ui/EmptyState";
import { Pagination } from "@/components/ui/Pagination";
import { SearchIcon } from "@/components/ui/icons";
import { filterRadicals } from "@/lib/data/radicalSearch";
import type { RadicalSummary } from "@/lib/data/types";

/** Same page size as HskLevelVocabularyList (UI-001) — no technical
 *  reason to diverge, and it keeps every paginated list in the app
 *  behaving identically. */
const PAGE_SIZE = 50;

/**
 * The canonical, full 214-radical browser (UI-001/UI-004). Live client-side
 * search + pagination, mirroring HskLevelVocabularyList's exact pattern
 * (PAGE_SIZE=50, useState query/page, useMemo filter, reset page on query
 * change) rather than the previous GET-form/`?q=` full-page-reload search —
 * this also makes the search interaction consistent with every other list
 * search in the app (HSK lists, Dictionary popup), none of which use a
 * submit button. All 214 radicals fit trivially in memory (already proven
 * by the Dictionary/HSK radical sections filtering the same array
 * client-side), so no server round-trip is needed.
 */
export function RadicalIndexView({
  radicals,
  vocabularyCounts,
}: {
  radicals: RadicalSummary[];
  vocabularyCounts: Record<string, number>;
}) {
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(1);

  const filtered = useMemo(() => filterRadicals(radicals, query), [radicals, query]);
  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const pageItems = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  // Any query change (including clearing it) restores page 1 — same rule
  // HskLevelVocabularyList uses.
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
          placeholder="Tìm bộ thủ theo chữ, pinyin hoặc nghĩa..."
          aria-label="Tìm kiếm bộ thủ"
          className="w-full rounded-md border border-neutral-300 bg-white py-2.5 pl-10 pr-4 text-base text-neutral-900 outline-none placeholder:text-neutral-500 focus:border-primary focus:ring-1 focus:ring-primary dark:border-night-border dark:bg-night-input dark:text-night-text dark:placeholder:text-night-muted"
        />
      </div>

      <p className="text-sm text-neutral-600 dark:text-night-muted">
        {filtered.length.toLocaleString("vi-VN")} bộ thủ
      </p>

      {filtered.length === 0 ? (
        <EmptyState
          title="Không tìm thấy bộ thủ phù hợp"
          description="Hãy thử chữ, pinyin hoặc nghĩa khác."
        />
      ) : (
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
          {pageItems.map((radical) => (
            <RadicalCard
              key={radical.id}
              radical={radical}
              vocabularyCount={vocabularyCounts[radical.id] ?? 0}
            />
          ))}
        </div>
      )}

      <Pagination currentPage={page} totalPages={totalPages} onPageChange={setPage} />
    </div>
  );
}
