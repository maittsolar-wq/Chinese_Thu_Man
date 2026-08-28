import type { Metadata } from "next";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { RadicalCard } from "@/components/radicals/RadicalCard";
import { EmptyState } from "@/components/ui/EmptyState";
import { getAllRadicals, getRadicalVocabularyCount } from "@/lib/data/radicalRepository";

export const metadata: Metadata = { title: "Bộ thủ — Chinese Thu Man" };

export default async function RadicalsPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const { q } = await searchParams;
  const query = q?.trim().toLowerCase() ?? "";

  const radicals = getAllRadicals().filter((radical) => {
    if (!query) return true;
    return (
      radical.radical.includes(query) ||
      radical.pinyin.toLowerCase().includes(query) ||
      radical.nameVi.toLowerCase().includes(query) ||
      radical.meaningVi.toLowerCase().includes(query)
    );
  });

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb items={[{ label: "Trang chủ", href: "/" }, { label: "Bộ thủ" }]} />

      <div className="flex flex-col gap-2">
        <h1 className="text-2xl font-bold text-primary">Bộ thủ</h1>
        <p className="text-sm text-neutral-600">
          214 bộ thủ Khang Hy và từ vựng HSK liên quan.
        </p>
      </div>

      <form action="/radicals" method="get" className="flex gap-2">
        <input
          type="text"
          name="q"
          defaultValue={q}
          placeholder="Tìm bộ thủ theo chữ, pinyin hoặc nghĩa..."
          className="w-full rounded-md border border-neutral-300 px-4 py-2.5 text-base outline-none focus:border-primary focus:ring-1 focus:ring-primary sm:max-w-md"
          aria-label="Tìm kiếm bộ thủ"
        />
        <button
          type="submit"
          className="shrink-0 rounded-md bg-primary px-4 py-2.5 text-sm font-semibold text-white hover:bg-primary-dark"
        >
          Tìm kiếm
        </button>
      </form>

      <p className="text-sm text-neutral-600">
        {radicals.length.toLocaleString("vi-VN")} bộ thủ
      </p>

      {radicals.length > 0 ? (
        <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
          {radicals.map((radical) => (
            <RadicalCard
              key={radical.id}
              radical={radical}
              vocabularyCount={getRadicalVocabularyCount(radical.id)}
            />
          ))}
        </div>
      ) : (
        <EmptyState
          title="Không tìm thấy bộ thủ phù hợp"
          description="Hãy thử chữ, pinyin hoặc nghĩa khác."
        />
      )}
    </div>
  );
}
