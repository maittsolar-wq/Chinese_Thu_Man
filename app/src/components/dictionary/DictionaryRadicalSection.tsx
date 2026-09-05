import { RadicalCard } from "@/components/radicals/RadicalCard";
import { LinkButton } from "@/components/ui/Button";
import { ArrowRightIcon } from "@/components/ui/icons";
import type { RadicalSummary } from "@/lib/data/types";

/** A single row at the widest grid breakpoint (`xl:grid-cols-6`) — enough
 *  to give a real sense of the feature without reproducing the full
 *  index. */
const TEASER_COUNT = 6;

/**
 * Dictionary's (and HSK's — this component is shared, see hsk/page.tsx)
 * "Bộ thủ" section, reduced from a full second copy of the 214-radical
 * browser to a compact teaser + "Xem tất cả" link (UI-004 polish pass).
 *
 * Before this change, this component rendered a live-searchable, full
 * 214-radical grid grouped by stroke count — a near-complete duplicate of
 * /radicals's own browser, and the reason /dictionary and /hsk measured
 * at 35,000+px tall on mobile (UI-001/UI-004 in the UI/UX audit). /radicals
 * is now the canonical place to search and browse every radical (see
 * RadicalIndexView, added in the same pass) with its own pagination —
 * neither Dictionary nor HSK had a product-specific reason to keep an
 * independent full copy, so both now link out to it instead.
 *
 * The teaser shows the highest-vocabularyCount radicals (the most likely
 * to be useful at a glance) rather than an arbitrary slice — reuses the
 * existing RadicalCard unchanged, no new visual design.
 */
export function DictionaryRadicalSection({
  radicals,
  vocabularyCounts,
  radicalHrefSuffix,
}: {
  radicals: RadicalSummary[];
  vocabularyCounts: Record<string, number>;
  /** Passed straight through to each teaser RadicalCard (e.g. "?from=hsk"
   *  when this section is reused on /hsk) so the header can keep the
   *  right tab active on Radical Detail — same contract as before this
   *  pass, unaffected by the teaser/full-grid change. */
  radicalHrefSuffix?: string;
}) {
  const teaserRadicals = [...radicals]
    .sort((a, b) => (vocabularyCounts[b.id] ?? 0) - (vocabularyCounts[a.id] ?? 0))
    .slice(0, TEASER_COUNT);

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-1">
        <h2 className="text-xl font-bold text-primary">Bộ thủ ({radicals.length})</h2>
        <p className="text-sm text-neutral-600 dark:text-night-muted">
          214 bộ thủ Khang Hy và từ vựng HSK liên quan.
        </p>
      </div>

      <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
        {teaserRadicals.map((radical) => (
          <RadicalCard
            key={radical.id}
            radical={radical}
            vocabularyCount={vocabularyCounts[radical.id] ?? 0}
            hrefSuffix={radicalHrefSuffix}
          />
        ))}
      </div>

      <LinkButton href="/radicals" variant="secondary" className="w-fit">
        Xem tất cả {radicals.length.toLocaleString("vi-VN")} bộ thủ
        <ArrowRightIcon className="h-4 w-4" />
      </LinkButton>
    </div>
  );
}
