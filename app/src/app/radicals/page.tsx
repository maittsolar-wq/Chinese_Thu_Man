import type { Metadata } from "next";
import { RadicalIndexNav } from "@/components/radicals/RadicalIndexNav";
import { RadicalIndexView } from "@/components/radicals/RadicalIndexView";
import { getAllRadicals, getRadicalVocabularyCount } from "@/lib/data/radicalRepository";

export const metadata: Metadata = { title: "Bộ thủ — Chinese Thu Man" };

/**
 * The canonical full radical browser (UI-001/UI-004 polish pass) — search
 * and pagination now live in RadicalIndexView (client-side, mirrors
 * HskLevelVocabularyList's pattern), so this page just loads the full
 * dataset once and hands it down. Dictionary and HSK link here via a
 * teaser instead of duplicating this browser (see DictionaryRadicalSection).
 *
 * Navigation-completion pass: this page deliberately does NOT read
 * `searchParams` itself (tried and reverted — it de-opts this route from
 * static (○) to dynamic (ƒ) rendering, a real architecture/perf side
 * effect this pass never asked for). The `?from=`-aware Back-button-vs-
 * breadcrumb decision and the Radical Detail hrefSuffix chaining both
 * live client-side instead (RadicalIndexNav / RadicalIndexView reading
 * window.location.search on mount), the same already-established pattern
 * AppHeader itself uses for exactly this reason. This page stays a plain
 * static shell either way.
 */
export default async function RadicalsPage() {
  const radicals = getAllRadicals();
  const vocabularyCounts = Object.fromEntries(
    radicals.map((radical) => [radical.id, getRadicalVocabularyCount(radical.id)])
  );

  return (
    <div className="flex flex-col gap-6">
      <RadicalIndexNav />

      <div className="flex flex-col gap-2">
        <h1 className="font-ui text-2xl font-bold text-primary dark:text-night-primary">Bộ thủ</h1>
        <p className="font-ui text-sm text-neutral-600 dark:text-night-muted">
          Tra cứu 214 bộ thủ Khang Hy — nền tảng để hiểu cấu tạo chữ Hán và từ vựng HSK liên quan.
        </p>
      </div>

      <RadicalIndexView radicals={radicals} vocabularyCounts={vocabularyCounts} />
    </div>
  );
}
