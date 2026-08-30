"use client";

import { SearchIcon } from "@/components/ui/icons";
import { useDictionarySearch } from "./DictionarySearchProvider";

/**
 * Home's "Tra từ điển nhanh" widget, replacing the old on-page SearchBox
 * (still used unchanged by the full /dictionary page itself). Visually
 * mimics that same input's border/padding/color so the widget doesn't
 * change shape — but it's a button: clicking it opens the shared
 * DictionarySearchPopup rather than performing a second, separate search
 * inline on Home.
 */
export function DictionarySearchTrigger({ placeholder }: { placeholder: string }) {
  const { open } = useDictionarySearch();

  return (
    <button
      type="button"
      onClick={open}
      className="flex w-full items-center gap-2 rounded-md border border-neutral-300 bg-white px-4 py-2.5 text-left text-base text-neutral-500 outline-none transition-colors hover:border-primary focus:border-primary focus:ring-1 focus:ring-primary dark:border-night-border dark:bg-night-input dark:text-night-muted"
    >
      <SearchIcon className="h-4 w-4 shrink-0" />
      {placeholder}
    </button>
  );
}
