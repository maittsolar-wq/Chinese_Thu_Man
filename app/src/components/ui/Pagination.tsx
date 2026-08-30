"use client";

import clsx from "clsx";
import { Button } from "./Button";
import { ChevronLeftIcon, ChevronRightIcon } from "./icons";

/**
 * The project's first (and only) pagination component — no prior pattern
 * existed to reuse, per the HSK audit. Purely presentational: the caller
 * owns `currentPage`/`totalPages` and does the actual slicing, so this
 * has no idea what it's paginating (vocabulary today, anything later).
 */
type PageToken = number | "ellipsis";

const MAX_VISIBLE_WITHOUT_COLLAPSING = 7;

/** 1, ..., current-1, current, current+1, ..., total — collapsing
 *  whichever ellipsis would otherwise be a single skipped page. Small
 *  page counts (the common case — most HSK levels paginate to well
 *  under 7 pages at PAGE_SIZE=50) show every page, uncollapsed. */
function getPageTokens(current: number, total: number): PageToken[] {
  if (total <= MAX_VISIBLE_WITHOUT_COLLAPSING) {
    return Array.from({ length: total }, (_, index) => index + 1);
  }

  const tokens: PageToken[] = [];
  const window = new Set([1, total, current - 1, current, current + 1]);
  let previous = 0;
  for (let page = 1; page <= total; page++) {
    if (!window.has(page)) continue;
    if (previous && page - previous > 1) tokens.push("ellipsis");
    tokens.push(page);
    previous = page;
  }
  return tokens;
}

export function Pagination({
  currentPage,
  totalPages,
  onPageChange,
}: {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}) {
  if (totalPages <= 1) return null;

  const tokens = getPageTokens(currentPage, totalPages);

  return (
    <nav aria-label="Phân trang" className="flex flex-wrap items-center justify-center gap-2">
      <Button
        type="button"
        variant="neutral"
        disabled={currentPage === 1}
        onClick={() => onPageChange(currentPage - 1)}
      >
        <ChevronLeftIcon className="h-4 w-4" />
        Trước
      </Button>

      {tokens.map((token, index) =>
        token === "ellipsis" ? (
          <span
            key={`ellipsis-${index}`}
            className="px-1 text-neutral-500 dark:text-night-muted"
            aria-hidden="true"
          >
            …
          </span>
        ) : (
          <button
            key={token}
            type="button"
            aria-current={token === currentPage ? "page" : undefined}
            onClick={() => onPageChange(token)}
            className={clsx(
              "flex h-9 min-w-9 items-center justify-center rounded-md border px-2 text-sm font-semibold transition-colors",
              token === currentPage
                ? "border-primary bg-primary text-white"
                : "border-neutral-300 bg-white text-neutral-900 hover:bg-neutral-50 dark:border-night-border dark:bg-night-input dark:text-night-text dark:hover:bg-night-surface"
            )}
          >
            {token}
          </button>
        )
      )}

      <Button
        type="button"
        variant="neutral"
        disabled={currentPage === totalPages}
        onClick={() => onPageChange(currentPage + 1)}
      >
        Sau
        <ChevronRightIcon className="h-4 w-4" />
      </Button>
    </nav>
  );
}
