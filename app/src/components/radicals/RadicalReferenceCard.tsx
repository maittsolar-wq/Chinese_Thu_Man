import Link from "next/link";
import type { RadicalSummary } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";

/**
 * Phase 07: `/radicals`-scoped, NOT a restyle of the shared `RadicalCard`.
 * That component is also rendered inside Vocabulary Detail's own "Bộ thủ &
 * chữ Hán" tab (an already-approved screen, Phase 02) — verified directly
 * via grep before touching anything — so it stays byte-for-byte untouched
 * and this dedicated component exists instead. Same underlying data, same
 * link target; only the presentation (font-cjk on the radical glyph,
 * matching the rest of the redesigned product) differs.
 */
export function RadicalReferenceCard({
  radical,
  vocabularyCount,
  hrefSuffix = "",
}: {
  radical: RadicalSummary;
  vocabularyCount: number;
  hrefSuffix?: string;
}) {
  return (
    <Link href={`/radicals/${radical.id}${hrefSuffix}`} className="block">
      <Card className="flex h-full flex-col gap-1 transition-shadow hover:shadow-md">
        <div className="flex items-start justify-between gap-2">
          <p className="font-cjk text-3xl font-semibold text-neutral-900 dark:text-night-text">
            {radical.radical}
          </p>
          <span className="font-ui shrink-0 rounded-full bg-neutral-100 px-2 py-0.5 text-xs font-medium text-neutral-600 dark:bg-night-input dark:text-night-muted">
            #{radical.kangxiIndex}
          </span>
        </div>
        <p className="font-ui text-sm italic text-primary dark:text-night-primary">{radical.pinyin}</p>
        <p className="font-ui text-sm text-neutral-800 dark:text-night-text">
          {radical.nameVi} · {radical.meaningVi}
        </p>
        <p className="font-ui mt-auto pt-2 text-xs font-medium text-neutral-500 dark:text-night-muted">
          {vocabularyCount > 0
            ? `${vocabularyCount} từ vựng liên quan`
            : "Chưa có từ vựng liên quan"}
        </p>
      </Card>
    </Link>
  );
}
