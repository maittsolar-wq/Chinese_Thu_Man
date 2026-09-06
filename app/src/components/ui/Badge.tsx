import Link from "next/link";
import type { ReactNode } from "react";
import clsx from "clsx";

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
}: {
  level: number;
  href?: string;
}) {
  const className =
    "inline-flex items-center rounded-full bg-primary-light px-2.5 py-0.5 text-xs font-semibold text-primary dark:bg-primary-dark/40 dark:text-white";

  if (href) {
    return (
      <Link href={href} className={clsx(className, "hover:bg-primary hover:text-white")}>
        HSK {level}
      </Link>
    );
  }

  return <span className={className}>HSK {level}</span>;
}
