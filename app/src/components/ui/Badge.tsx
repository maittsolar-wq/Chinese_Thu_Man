import Link from "next/link";
import type { ReactNode } from "react";
import clsx from "clsx";
import { HSK_LEVEL_HEX } from "@/lib/hsk/homePalette";
import type { HskLevel } from "@/lib/data/types";

/**
 * Generic tone-based badge — introduced for the Vocabulary Detail redesign
 * (Phase 02) to replace the "rounded-full bg-neutral-100 px-2.5 py-0.5
 * text-xs" pattern found hand-rolled independently in at least four files
 * during the Phase 01 audit (Radical Detail's stroke-count chip, its "Bộ
 * thủ số N" chip, Vocabulary Detail's part-of-speech chip, ...). Additive:
 * HskLevelBadge below is untouched and still used exactly as before by
 * every existing caller.
 */
export function Badge({
  tone = "neutral",
  children,
}: {
  tone?: "primary" | "neutral" | "success";
  children: ReactNode;
}) {
  const toneClasses = {
    primary: "bg-primary-light text-primary dark:bg-primary-dark/40 dark:text-night-primary",
    neutral: "bg-neutral-100 text-neutral-600 dark:bg-night-input dark:text-night-muted",
    success: "bg-success-bg text-success dark:bg-success/20 dark:text-success",
  }[tone];

  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
        toneClasses
      )}
    >
      {children}
    </span>
  );
}

export function HskLevelBadge({
  level,
  href,
  colored = false,
}: {
  level: number;
  href?: string;
  /**
   * Opt-in per-level HSK brand color (text = full `HSK_LEVEL_HEX` color,
   * background = the same color at ~10% opacity) instead of the flat
   * blue every caller has always used. Default `false` — every existing
   * caller (HskVocabularyRow, VocabularyDetail, RadicalDetailView,
   * RadicalVocabularyByLevel) is unaffected; only VocabularyCard's
   * search-result badges opt in, per the Search Results visual-fix pass.
   */
  colored?: boolean;
}) {
  const validLevel = level >= 1 && level <= 6 ? (level as HskLevel) : null;
  const tint = colored && validLevel ? HSK_LEVEL_HEX[validLevel] : null;

  const baseClassName = "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold";
  const flatClassName = "bg-primary-light text-primary dark:bg-primary-dark/40 dark:text-white";
  const style = tint ? { backgroundColor: `${tint}1A`, color: tint } : undefined;

  if (href) {
    return (
      <Link
        href={href}
        className={clsx(
          baseClassName,
          tint ? "transition-opacity hover:opacity-80" : clsx(flatClassName, "hover:bg-primary hover:text-white")
        )}
        style={style}
      >
        HSK {level}
      </Link>
    );
  }

  return (
    <span className={clsx(baseClassName, !tint && flatClassName)} style={style}>
      HSK {level}
    </span>
  );
}
