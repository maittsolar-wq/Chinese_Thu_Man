import Link from "next/link";
import type { RadicalSummary } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";

export function RadicalCard({
  radical,
  vocabularyCount,
  hrefSuffix = "",
}: {
  radical: RadicalSummary;
  vocabularyCount: number;
  /** Optional query string (e.g. "?from=hsk") appended to the Radical
   *  Detail link, so the header can tell which entry point the visitor
   *  came from. Defaults to "" — every existing caller (the standalone
   *  /radicals page, and Dictionary's own use of this card) is
   *  unaffected unless it opts in. */
  hrefSuffix?: string;
}) {
  return (
    <Link href={`/radicals/${radical.id}${hrefSuffix}`} className="block">
      <Card className="flex h-full flex-col gap-1 transition-shadow hover:shadow-md">
        <div className="flex items-start justify-between gap-2">
          <p className="text-3xl font-bold text-neutral-900 dark:text-night-text">{radical.radical}</p>
          <span className="shrink-0 rounded-full bg-neutral-100 px-2 py-0.5 text-xs font-medium text-neutral-600 dark:bg-night-input dark:text-night-muted">
            #{radical.kangxiIndex}
          </span>
        </div>
        <p className="text-sm text-neutral-600 dark:text-night-muted">{radical.pinyin}</p>
        <p className="text-sm text-neutral-800 dark:text-night-text">
          {radical.nameVi} · {radical.meaningVi}
        </p>
        <p className="mt-auto pt-2 text-xs font-medium text-neutral-500 dark:text-night-muted">
          {vocabularyCount > 0
            ? `${vocabularyCount} từ vựng liên quan`
            : "Chưa có từ vựng liên quan"}
        </p>
      </Card>
    </Link>
  );
}
