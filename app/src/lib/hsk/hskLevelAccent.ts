import type { HskLevel } from "@/lib/data/types";

/**
 * The same six decorative per-level accent colors already used on Home's
 * level grid (app/page.tsx's own local `HSK_ACCENT`) and Practice's cards
 * (tailwind.config.ts `accent.*`, added 2026-08-29). Duplicated here rather
 * than importing from Home's page module — Home is out of scope for this
 * phase and must not be touched — but the underlying hex values remain
 * single-sourced in tailwind.config.ts; this is just the level->className
 * lookup, same six values Home already renders.
 */
export const HSK_LEVEL_ACCENT_TEXT: Record<HskLevel, string> = {
  1: "text-accent-blue",
  2: "text-accent-green",
  3: "text-accent-purple",
  4: "text-accent-orange",
  5: "text-accent-red",
  6: "text-accent-teal",
};

export const HSK_LEVEL_ACCENT_BG: Record<HskLevel, string> = {
  1: "bg-accent-blue",
  2: "bg-accent-green",
  3: "bg-accent-purple",
  4: "bg-accent-orange",
  5: "bg-accent-red",
  6: "bg-accent-teal",
};
