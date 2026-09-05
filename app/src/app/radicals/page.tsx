import type { Metadata } from "next";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { RadicalIndexView } from "@/components/radicals/RadicalIndexView";
import { getAllRadicals, getRadicalVocabularyCount } from "@/lib/data/radicalRepository";

export const metadata: Metadata = { title: "Bộ thủ — Chinese Thu Man" };

/**
 * The canonical full radical browser (UI-001/UI-004 polish pass) — search
 * and pagination now live in RadicalIndexView (client-side, mirrors
 * HskLevelVocabularyList's pattern), so this page just loads the full
 * dataset once and hands it down. Dictionary and HSK link here via a
 * teaser instead of duplicating this browser (see DictionaryRadicalSection).
 */
export default async function RadicalsPage() {
  const radicals = getAllRadicals();
  const vocabularyCounts = Object.fromEntries(
    radicals.map((radical) => [radical.id, getRadicalVocabularyCount(radical.id)])
  );

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb items={[{ label: "Trang chủ", href: "/" }, { label: "Bộ thủ" }]} />

      <div className="flex flex-col gap-2">
        <h1 className="text-2xl font-bold text-primary">Bộ thủ</h1>
        <p className="text-sm text-neutral-600">
          214 bộ thủ Khang Hy và từ vựng HSK liên quan.
        </p>
      </div>

      <RadicalIndexView radicals={radicals} vocabularyCounts={vocabularyCounts} />
    </div>
  );
}
