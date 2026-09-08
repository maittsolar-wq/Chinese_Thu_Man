import { ChevronRightIcon } from "@/components/ui/icons";
import { buildPageTokens } from "@/lib/pagination";

/**
 * Extracted verbatim from HomeSearch.tsx's own inline pagination block
 * (same markup, same classes, same colors) so DictionarySearchPopup can
 * reuse the exact already-approved control instead of a second copy.
 * HomeSearch now renders this component too — zero visual change there,
 * just relocated.
 */
export function SearchPagination({
  page,
  totalPages,
  onPageChange,
}: {
  page: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}) {
  if (totalPages <= 1) return null;

  const pageTokens = buildPageTokens(page, totalPages);

  return (
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
            onClick={() => onPageChange(token)}
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
        onClick={() => onPageChange(Math.min(totalPages, page + 1))}
        className="flex h-10 w-10 items-center justify-center rounded-lg border border-[#E2E8F0] text-neutral-700 transition-colors hover:bg-neutral-50 disabled:cursor-not-allowed disabled:opacity-40 dark:border-[#3A3A3A] dark:text-[#F8FAFC] dark:hover:bg-white/10"
      >
        <ChevronRightIcon className="h-4 w-4" />
      </button>
    </div>
  );
}
