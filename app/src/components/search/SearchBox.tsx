import { SearchIcon } from "@/components/ui/icons";

/**
 * Phase 06 redesign: same GET form → /dictionary?q=... submission as
 * before (server-rendered search, zero logic change) — restyled to be the
 * visual focus of the page rather than a small bar above the results, per
 * this phase's "the search field should feel like the primary action of
 * the page" instruction. /dictionary-exclusive (verified consumer).
 */
export function SearchBox({
  defaultValue,
  placeholder = "Nhập chữ Hán, pinyin hoặc nghĩa tiếng Việt...",
}: {
  defaultValue?: string;
  placeholder?: string;
}) {
  return (
    <form action="/dictionary" method="get" className="relative w-full">
      <SearchIcon className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-neutral-500 dark:text-night-muted" />
      <input
        type="text"
        name="q"
        defaultValue={defaultValue}
        placeholder={placeholder}
        className="w-full rounded-md border border-neutral-300 bg-white py-4 pl-12 pr-28 text-lg text-neutral-900 outline-none placeholder:text-neutral-500 focus:border-primary focus:ring-1 focus:ring-primary dark:border-night-border dark:bg-night-input dark:text-night-text dark:placeholder:text-night-muted"
        aria-label="Tìm kiếm từ vựng"
      />
      <button
        type="submit"
        className="absolute right-2 top-1/2 -translate-y-1/2 rounded-md bg-primary px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-primary-dark"
      >
        Tìm kiếm
      </button>
    </form>
  );
}
