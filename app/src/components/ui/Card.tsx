import type { HTMLAttributes } from "react";
import clsx from "clsx";

export function Card({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={clsx(
        "rounded-card border border-neutral-200 bg-white p-4 shadow-card dark:border-night-border dark:bg-night-surface",
        className
      )}
      {...props}
    />
  );
}

/**
 * Quiet, borderless grouping surface — distinct from Card by role, not just
 * by color. A Card means "this is a separate, often interactive item" (a
 * vocabulary row, a radical); a Panel means "this is reference information
 * sitting in its place" (Phase 01 design proposal §F). No shadow, no
 * border — the tonal shift from the page background is what separates it.
 */
export function Panel({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={clsx("rounded-card bg-surface-sunken p-4 dark:bg-night-input", className)}
      {...props}
    />
  );
}
