import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { VocabularyCard } from "@/components/vocabulary/VocabularyCard";
import { EmptyState } from "@/components/ui/EmptyState";
import { getVocabularyByLevel } from "@/lib/data/vocabularyRepository";
import type { HskLevel } from "@/lib/data/types";

const VALID_LEVELS = [1, 2, 3, 4, 5, 6];

function parseLevel(param: string): HskLevel | null {
  const value = Number(param);
  return VALID_LEVELS.includes(value) ? (value as HskLevel) : null;
}

export function generateStaticParams() {
  return VALID_LEVELS.map((level) => ({ level: String(level) }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ level: string }>;
}): Promise<Metadata> {
  const { level: levelParam } = await params;
  const level = parseLevel(levelParam);
  return { title: level ? `HSK ${level} — Chinese Thu Man` : "HSK — Chinese Thu Man" };
}

export default async function HskLevelPage({
  params,
  searchParams,
}: {
  params: Promise<{ level: string }>;
  searchParams: Promise<{ q?: string }>;
}) {
  const { level: levelParam } = await params;
  const level = parseLevel(levelParam);
  if (!level) notFound();

  const { q } = await searchParams;
  const query = q?.trim().toLowerCase() ?? "";

  const words = getVocabularyByLevel(level).filter((word) => {
    if (!query) return true;
    return (
      word.word.includes(query) ||
      word.pinyin.toLowerCase().includes(query) ||
      word.meaningVi.toLowerCase().includes(query)
    );
  });

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb
        items={[
          { label: "Trang chủ", href: "/" },
          { label: "HSK", href: "/hsk" },
          { label: `HSK ${level}` },
        ]}
      />

      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold text-primary">HSK {level}</h1>
        <form action={`/hsk/${level}`} method="get" className="flex gap-2">
          <input
            type="text"
            name="q"
            defaultValue={q}
            placeholder={`Lọc trong HSK ${level}...`}
            className="w-full min-w-0 rounded-md border border-neutral-300 px-3 py-2 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary sm:w-64"
            aria-label={`Lọc từ vựng trong HSK ${level}`}
          />
          <button
            type="submit"
            className="shrink-0 rounded-md border border-primary px-3 py-2 text-sm font-medium text-primary hover:bg-primary-light"
          >
            Lọc
          </button>
        </form>
      </div>

      <p className="text-sm text-neutral-600">
        {words.length.toLocaleString("vi-VN")} từ vựng
      </p>

      {words.length > 0 ? (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {words.map((word) => (
            <VocabularyCard
              key={word.id}
              word={word}
              href={`/vocabulary/${word.id}?from=hsk&level=${level}`}
              currentLevel={level}
            />
          ))}
        </div>
      ) : (
        <EmptyState
          title="Không tìm thấy từ phù hợp"
          description="Hãy thử chữ Hán, pinyin hoặc nghĩa tiếng Việt khác."
        />
      )}
    </div>
  );
}
