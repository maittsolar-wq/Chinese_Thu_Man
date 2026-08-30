"use client";

import { useMemo, useState } from "react";
import { RadicalCard } from "@/components/radicals/RadicalCard";
import { EmptyState } from "@/components/ui/EmptyState";
import { SearchIcon, CloseIcon } from "@/components/ui/icons";
import { filterRadicals, groupRadicalsByStrokeCount } from "@/lib/data/radicalSearch";
import type { RadicalSummary } from "@/lib/data/types";

/**
 * The Dictionary main screen's "Bộ thủ (214)" section — a radical-ONLY
 * live search (never touches vocabulary; see radicalSearch.ts's header
 * comment), grouped by stroke count, reusing the existing RadicalCard
 * (which already links to the untouched /radicals/[id] Radical Detail
 * route). All 214 radicals are handed down as props from the Server
 * Component page and filtered entirely client-side — no debounce needed,
 * no server round-trip, since 214 items is trivial to filter in-browser
 * and this keeps the interaction genuinely instant.
 */
export function DictionaryRadicalSection({
  radicals,
  vocabularyCounts,
}: {
  radicals: RadicalSummary[];
  vocabularyCounts: Record<string, number>;
}) {
  const [query, setQuery] = useState("");

  const visibleRadicals = useMemo(() => filterRadicals(radicals, query), [radicals, query]);
  const groups = useMemo(() => groupRadicalsByStrokeCount(visibleRadicals), [visibleRadicals]);
  const hasQuery = query.trim().length > 0;

  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-xl font-bold text-primary">Bộ thủ ({radicals.length})</h2>

      <div className="relative">
        <SearchIcon className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-500 dark:text-night-muted" />
        <input
          type="text"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Tìm bộ thủ"
          aria-label="Tìm kiếm bộ thủ"
          className="w-full rounded-md border border-neutral-300 bg-white py-2.5 pl-10 pr-10 text-base text-neutral-900 outline-none placeholder:text-neutral-500 focus:border-primary focus:ring-1 focus:ring-primary dark:border-night-border dark:bg-night-input dark:text-night-text dark:placeholder:text-night-muted"
        />
        {hasQuery && (
          <button
            type="button"
            aria-label="Xóa tìm kiếm"
            onClick={() => setQuery("")}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-500 hover:text-neutral-700 dark:text-night-muted dark:hover:text-night-text"
          >
            <CloseIcon className="h-4 w-4" />
          </button>
        )}
      </div>

      {hasQuery && (
        <p className="text-sm text-neutral-600 dark:text-night-muted">Kết quả tìm kiếm</p>
      )}

      {visibleRadicals.length === 0 ? (
        <EmptyState
          title="Không tìm thấy bộ thủ phù hợp"
          description="Hãy thử chữ, pinyin hoặc nghĩa khác."
        />
      ) : (
        <div className="flex flex-col gap-6">
          {groups.map((group) => (
            <div key={group.strokeCount} className="flex flex-col gap-3">
              {!hasQuery && (
                <h3 className="text-sm font-semibold text-neutral-600 dark:text-night-muted">
                  {group.strokeCount} nét ({group.radicals.length})
                </h3>
              )}
              <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
                {group.radicals.map((radical) => (
                  <RadicalCard
                    key={radical.id}
                    radical={radical}
                    vocabularyCount={vocabularyCounts[radical.id] ?? 0}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
