"use client";

import { useState } from "react";
import Link from "next/link";
import { Card } from "@/components/ui/Card";
import { Pagination } from "@/components/ui/Pagination";
import { HskLevelBadge } from "@/components/ui/Badge";
import type { HskLevel, RadicalVocabularyRef } from "@/lib/data/types";

const ALL_LEVELS: HskLevel[] = [1, 2, 3, 4, 5, 6];

/**
 * Smaller than HskLevelVocabularyList/RadicalIndexView's PAGE_SIZE=50 —
 * a clear technical difference from those single-list contexts: this
 * screen can render up to 6 of these paginated lists at once (one per
 * HSK level), so 50/level would still let the page reach ~300 rendered
 * cards in the worst case (a radical present at high volume across every
 * level, e.g. 人). 20/level caps that same worst case at ~120 while still
 * keeping each level's own pagination click-count reasonable.
 */
const PAGE_SIZE = 20;

/**
 * A vocabulary word can contain multiple characters that map to the same
 * radical (e.g. both 一 and 下 in 一下 map to radical 一), so the same
 * vocabularyId can legitimately appear more than once within a level's
 * entries. Dedupe here at render time only — the source mapping JSON is
 * left untouched — keeping the first occurrence.
 */
function dedupeByVocabularyId(
  entries: RadicalVocabularyRef[]
): RadicalVocabularyRef[] {
  const seen = new Set<string>();
  const result: RadicalVocabularyRef[] = [];
  for (const entry of entries) {
    if (seen.has(entry.vocabularyId)) continue;
    seen.add(entry.vocabularyId);
    result.push(entry);
  }
  return result;
}

/**
 * Renders Radical Detail's "related vocabulary" grouped by HSK level
 * (UI-002 polish pass) — grouping is preserved exactly as before, only a
 * per-level page is added so a high-frequency radical no longer renders
 * hundreds of cards at once (radical_009 人 alone was measured at
 * 21,112px tall with all 545 words rendered together). Each level keeps
 * its own independent page state — paging through HSK 4 doesn't reset or
 * affect HSK 5's page, matching how unrelated lists shouldn't interfere.
 */
export function RadicalVocabularyByLevel({
  radicalId,
  vocabularyByLevel,
  vocabularyHrefSuffix = "",
}: {
  radicalId: string;
  vocabularyByLevel: Partial<Record<HskLevel, RadicalVocabularyRef[]>>;
  vocabularyHrefSuffix?: string;
}) {
  const [pageByLevel, setPageByLevel] = useState<Partial<Record<HskLevel, number>>>({});

  return (
    <div className="flex flex-col gap-5">
      {ALL_LEVELS.map((level) => {
        const entries = vocabularyByLevel[level];
        if (!entries || entries.length === 0) return null;
        const dedupedEntries = dedupeByVocabularyId(entries);
        const page = pageByLevel[level] ?? 1;
        const totalPages = Math.max(1, Math.ceil(dedupedEntries.length / PAGE_SIZE));
        const pageItems = dedupedEntries.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

        return (
          <div key={level}>
            <div className="mb-2 flex items-center gap-2">
              <HskLevelBadge level={level} />
              <span className="text-xs text-neutral-500 dark:text-night-muted">
                {dedupedEntries.length} từ
              </span>
            </div>
            <div className="grid grid-cols-2 gap-3 lg:grid-cols-3">
              {pageItems.map((entry) => (
                <Link
                  key={entry.vocabularyId}
                  href={`/vocabulary/${entry.vocabularyId}?from=radical&radicalId=${radicalId}${vocabularyHrefSuffix}`}
                  className="block min-w-0"
                >
                  <Card className="hover:shadow-md">
                    <p className="text-xl font-semibold text-neutral-900 dark:text-night-text">
                      {entry.word}
                    </p>
                    <p className="text-sm text-neutral-600 dark:text-night-muted">{entry.pinyin}</p>
                    {entry.meaningVi && (
                      <p className="truncate text-sm text-neutral-800 dark:text-night-text">
                        {entry.meaningVi}
                      </p>
                    )}
                  </Card>
                </Link>
              ))}
            </div>
            {totalPages > 1 && (
              <div className="mt-3">
                <Pagination
                  currentPage={page}
                  totalPages={totalPages}
                  onPageChange={(nextPage) =>
                    setPageByLevel((prev) => ({ ...prev, [level]: nextPage }))
                  }
                />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
