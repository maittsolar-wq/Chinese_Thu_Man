"use client";

import { useEffect, useMemo, useState } from "react";
import { EmptyState } from "@/components/ui/EmptyState";
import { Pagination } from "@/components/ui/Pagination";
import { SearchIcon, ChevronDownIcon } from "@/components/ui/icons";
import { ListeningLessonCard } from "./ListeningLessonCard";
import type { ListeningLesson } from "@/lib/listening/types";

const PAGE_SIZE = 8;

type SortOption = "newest" | "oldest" | "az";

const SORT_LABELS: Record<SortOption, string> = {
  newest: "Mới nhất",
  oldest: "Cũ nhất",
  az: "Tên A-Z",
};

function sortLessons(lessons: ListeningLesson[], sort: SortOption): ListeningLesson[] {
  const sorted = [...lessons];
  if (sort === "newest") return sorted.reverse();
  if (sort === "az") return sorted.sort((a, b) => a.chineseTitle.localeCompare(b.chineseTitle, "zh"));
  return sorted; // "oldest" = catalog order, already ascending by code
}

function matchesQuery(lesson: ListeningLesson, query: string): boolean {
  const q = query.trim().toLowerCase();
  if (!q) return true;
  return (
    lesson.id.toLowerCase().includes(q) ||
    lesson.code.includes(q) ||
    lesson.label.toLowerCase().includes(q) ||
    lesson.chineseTitle.toLowerCase().includes(q) ||
    lesson.vietnameseTitle.toLowerCase().includes(q)
  );
}

/**
 * Owns search + sort + pagination for one level's lesson list — client-
 * side only, mirroring the same client-owned-state pattern as
 * HskLevelVocabularyList. `lessons` is that level's full mock catalog;
 * nothing here fetches or mutates it.
 */
export function ListeningLessonGrid({ lessons }: { lessons: ListeningLesson[] }) {
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState<SortOption>("newest");
  const [page, setPage] = useState(1);

  const filtered = useMemo(() => {
    const matched = lessons.filter((lesson) => matchesQuery(lesson, query));
    return sortLessons(matched, sort);
  }, [lessons, query, sort]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const pageItems = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);
  const rangeStart = filtered.length === 0 ? 0 : (page - 1) * PAGE_SIZE + 1;
  const rangeEnd = Math.min(page * PAGE_SIZE, filtered.length);

  useEffect(() => {
    setPage(1);
  }, [query, sort]);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative sm:max-w-md sm:flex-1">
          <SearchIcon className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-500 dark:text-night-muted" />
          <input
            type="text"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Tìm kiếm bài nghe (ví dụ: 502, chào hỏi...)"
            aria-label="Tìm kiếm bài nghe"
            className="font-ui w-full rounded-2xl border border-[#E2E8F0] bg-white py-3 pl-11 pr-4 text-base text-neutral-900 outline-none placeholder:text-neutral-500 focus:border-primary focus:ring-1 focus:ring-primary dark:border-night-border dark:bg-night-input dark:text-night-text dark:placeholder:text-night-muted"
          />
        </div>

        <div className="relative shrink-0">
          <select
            value={sort}
            onChange={(event) => setSort(event.target.value as SortOption)}
            aria-label="Sắp xếp bài nghe"
            className="font-ui w-full appearance-none rounded-xl border border-[#E2E8F0] bg-white py-2.5 pl-4 pr-10 text-base font-semibold text-neutral-800 outline-none focus:border-primary focus:ring-1 focus:ring-primary dark:border-night-border dark:bg-night-input dark:text-night-text sm:w-auto"
          >
            {(Object.keys(SORT_LABELS) as SortOption[]).map((option) => (
              <option key={option} value={option}>
                {SORT_LABELS[option]}
              </option>
            ))}
          </select>
          <ChevronDownIcon className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-500 dark:text-night-muted" />
        </div>
      </div>

      {filtered.length === 0 ? (
        <EmptyState
          title="Không tìm thấy bài nghe phù hợp"
          description="Hãy thử số bài hoặc từ khóa khác."
        />
      ) : (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          {pageItems.map((lesson) => (
            <ListeningLessonCard key={lesson.id} lesson={lesson} />
          ))}
        </div>
      )}

      {filtered.length > 0 && (
        <div className="flex flex-col items-center gap-3">
          <Pagination currentPage={page} totalPages={totalPages} onPageChange={setPage} />
          <p className="font-ui text-sm text-neutral-600 dark:text-night-muted">
            Hiển thị {rangeStart} - {rangeEnd} trong {filtered.length} bài
          </p>
        </div>
      )}
    </div>
  );
}
