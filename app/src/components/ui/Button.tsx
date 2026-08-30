import Link from "next/link";
import type { AnchorHTMLAttributes, ButtonHTMLAttributes } from "react";
import clsx from "clsx";

type Variant = "primary" | "secondary" | "neutral";

const VARIANT_CLASSES: Record<Variant, string> = {
  primary: "bg-primary text-white hover:bg-primary-dark",
  secondary:
    "border border-primary bg-white text-primary hover:bg-primary-light dark:bg-night-surface dark:hover:bg-night-input",
  neutral:
    "border border-neutral-300 bg-white text-neutral-800 hover:bg-neutral-50 dark:border-night-border dark:bg-night-surface dark:text-night-text dark:hover:bg-night-input",
};

const BASE_CLASSES =
  "inline-flex items-center justify-center gap-2 rounded-md px-4 py-2 text-sm font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-50";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

export function Button({ variant = "primary", className, ...props }: ButtonProps) {
  return (
    <button
      className={clsx(BASE_CLASSES, VARIANT_CLASSES[variant], className)}
      {...props}
    />
  );
}

interface LinkButtonProps extends AnchorHTMLAttributes<HTMLAnchorElement> {
  href: string;
  variant?: Variant;
}

export function LinkButton({
  variant = "primary",
  className,
  href,
  ...props
}: LinkButtonProps) {
  return (
    <Link
      href={href}
      className={clsx(BASE_CLASSES, VARIANT_CLASSES[variant], className)}
      {...props}
    />
  );
}
