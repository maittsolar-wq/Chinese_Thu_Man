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
