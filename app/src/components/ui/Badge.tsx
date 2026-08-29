import Link from "next/link";
import clsx from "clsx";

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
