import type { Metadata } from "next";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { SearchBox } from "@/components/search/SearchBox";
import { VocabularyCard } from "@/components/vocabulary/VocabularyCard";
import { EmptyState } from "@/components/ui/EmptyState";
import { DictionaryRadicalSection } from "@/components/dictionary/DictionaryRadicalSection";
import { searchVocabulary } from "@/lib/data/vocabularyRepository";
import { getAllRadicals, getRadicalVocabularyCount } from "@/lib/data/radicalRepository";

export const metadata: Metadata = { title: "Từ điển — Chinese Thu Man" };

export default async function DictionaryPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const { q } = await searchParams;
  const query = q?.trim() ?? "";
  const hasQuery = query.length > 0;
  const results = hasQuery ? searchVocabulary(query) : [];

  const radicals = getAllRadicals();
  const radicalVocabularyCounts = Object.fromEntries(
    radicals.map((radical) => [radical.id, getRadicalVocabularyCount(radical.id)])
  );

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb items={[{ label: "Trang chủ", href: "/" }, { label: "Từ điển" }]} />

      <div className="flex flex-col gap-2">
        <h1 className="text-2xl font-bold text-primary">Từ điển</h1>
        <p className="text-sm text-neutral-600">
          Tra cứu từ vựng HSK theo chữ Hán, pinyin hoặc nghĩa tiếng Việt.
        </p>
      </div>

      <SearchBox defaultValue={query} />

      {hasQuery ? (
        results.length > 0 ? (
          <div className="flex flex-col gap-3">
            <p className="text-sm text-neutral-600">
              Tìm thấy {results.length.toLocaleString("vi-VN")} kết quả
            </p>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {results.map((word) => (
                <VocabularyCard
                  key={word.id}
                  word={word}
                  href={`/vocabulary/${word.id}?from=dictionary`}
                  showAllLevels
                />
              ))}
            </div>
          </div>
        ) : (
          <EmptyState
            title="Không tìm thấy từ phù hợp"
            description="Hãy thử chữ Hán, pinyin hoặc nghĩa tiếng Việt khác."
          />
        )
      ) : (
        <EmptyState title="Nhập từ khóa để bắt đầu tra cứu." />
      )}

      <DictionaryRadicalSection radicals={radicals} vocabularyCounts={radicalVocabularyCounts} />
    </div>
  );
}
