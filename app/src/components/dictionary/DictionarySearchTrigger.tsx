"use client";

import { SearchIcon } from "@/components/ui/icons";
import { useDictionarySearch } from "./DictionarySearchProvider";

/**
 * Home's secondary hero CTA (Phase 04) — opens the shared
 * DictionarySearchPopup rather than navigating anywhere, matching the
 * global nav's own "Từ điển" trigger. Home-exclusive component (nothing
 * else imports it), so it's free to be reshaped alongside Home itself.
 *
 * Previously rendered as a full-width fake search-input-shaped button in
 * its own dedicated "Tra từ điển nhanh" section; Home no longer has a
 * standalone Dictionary section (the popup is already one click away from
 * the persistent header nav on every page) — this is now just the hero's
 * secondary CTA button, sized and styled like Button.tsx's `secondary`
 * variant so hero primary/secondary CTAs read as a pair.
 */
export function DictionarySearchTrigger({ label }: { label: string }) {
  const { open } = useDictionarySearch();

  return (
    <button
      type="button"
      onClick={open}
      className="inline-flex w-fit items-center justify-center gap-2 rounded-md border border-primary bg-white px-4 py-2 text-sm font-semibold text-primary transition-colors hover:bg-primary-light dark:bg-night-surface dark:text-night-primary dark:hover:bg-night-input"
    >
      <SearchIcon className="h-4 w-4" />
      {label}
    </button>
  );
}
