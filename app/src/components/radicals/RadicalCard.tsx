import Link from "next/link";
import type { RadicalSummary } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";

/**
 * Vocabulary Detail visual-refinement pass: sole live consumer is
 * VocabularyDetail's "Bộ thủ & chữ Hán" section (grep-verified —
 * DictionaryRadicalSection also imports this component but is itself
 * dead code, never imported by any route, so it's not a real consumer to
 * protect). Restyled in place rather than forked: bigger, medium-weight
 * (not bold) Noto Serif SC glyph (44-52px desktop / stock `text-5xl`=48px
 * covers both the desktop and mobile approved ranges), and the new
 * `ink`/`hairline` tokens already used by the rest of this screen. Same
 * data, same link target, same hrefSuffix contract.
 */
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
      <Card className="flex h-full flex-col gap-1 border-hairline transition-colors hover:border-primary dark:hover:border-night-primary">
        <div className="flex items-start justify-between gap-2">
          <p className="font-cjk text-5xl font-medium text-ink dark:text-night-text">{radical.radical}</p>
          <span className="shrink-0 rounded-full bg-neutral-100 px-2 py-0.5 text-xs font-medium text-ink-muted dark:bg-night-input dark:text-night-muted">
            #{radical.kangxiIndex}
          </span>
        </div>
        <p className="text-base text-ink-muted dark:text-night-muted">{radical.pinyin}</p>
        <p className="text-base font-medium text-ink dark:text-night-text">
          {radical.nameVi} · {radical.meaningVi}
        </p>
        <p className="mt-auto pt-2 text-sm font-medium text-ink-muted dark:text-night-muted">
          {vocabularyCount > 0
            ? `${vocabularyCount} từ vựng liên quan`
            : "Chưa có từ vựng liên quan"}
        </p>
      </Card>
    </Link>
  );
}
