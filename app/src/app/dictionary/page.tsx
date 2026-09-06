import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { SearchBox } from "@/components/search/SearchBox";
import { VocabularyCard } from "@/components/vocabulary/VocabularyCard";
import { EmptyState } from "@/components/ui/EmptyState";
import { Panel } from "@/components/ui/Card";
import { RadicalIcon, ArrowRightIcon } from "@/components/ui/icons";
import { searchVocabulary } from "@/lib/data/vocabularyRepository";

export const metadata: Metadata = { title: "Tra cứu — Chinese Thu Man" };

/**
 * Phase 06 redesign. Search behavior is completely unchanged: still a
 * server-rendered GET search against `searchVocabulary` only (the popup's
 * separately-combined radical-aware search, lib/data/dictionarySearch.ts,
 * was never used here before this pass and still isn't — that is a
 * pre-existing difference between the two surfaces, not something this
 * redesign introduces or corrects).
 *
 * The full 214-radical teaser grid (DictionaryRadicalSection) that used to
 * sit unconditionally below every search state — competing directly with
 * results — is replaced with one slim contextual panel, the same pattern
 * already established on Home and HSK (Phases 03-04): a single link out to
 * /radicals, not a second product destination fighting for attention.
 */
export default async function DictionaryPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const { q } = await searchParams;
  const query = q?.trim() ?? "";
  const hasQuery = query.length > 0;
  const results = hasQuery ? searchVocabulary(query) : [];

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb items={[{ label: "Trang chủ", href: "/" }, { label: "Tra cứu" }]} />

      <div className="flex flex-col gap-1">
        <h1 className="text-2xl font-bold text-primary dark:text-night-primary">
          Tra từ tiếng Trung
        </h1>
        <p className="text-sm text-neutral-600 dark:text-night-muted">
          Tra cứu từ vựng HSK theo chữ Hán, pinyin hoặc nghĩa tiếng Việt.
        </p>
      </div>

      <SearchBox defaultValue={query} />

      {hasQuery ? (
        results.length > 0 ? (
          <div className="flex flex-col gap-3">
            <p className="text-sm text-neutral-600 dark:text-night-muted">
              Tìm thấy {results.length.toLocaleString("vi-VN")} kết quả cho{" "}
              <span className="font-cjk font-semibold text-neutral-900 dark:text-night-text">
                &ldquo;{query}&rdquo;
              </span>
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

      <Panel className="flex flex-col items-start gap-3 p-6 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-start gap-3">
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary-light text-primary dark:bg-primary-dark/40 dark:text-night-primary">
            <RadicalIcon className="h-5 w-5" />
          </span>
          <div className="flex flex-col gap-0.5">
            <p className="text-sm font-semibold text-neutral-900 dark:text-night-text">
              Không tìm thấy? Thử tra theo bộ thủ
            </p>
            <p className="text-sm text-neutral-600 dark:text-night-muted">
              214 bộ thủ Khang Hy và chữ Hán liên quan.
            </p>
          </div>
        </div>
        <Link
          href="/radicals"
          className="inline-flex shrink-0 items-center gap-1.5 text-sm font-semibold text-primary hover:underline dark:text-night-primary"
        >
          Tra cứu bộ thủ
          <ArrowRightIcon className="h-4 w-4" />
        </Link>
      </Panel>
    </div>
  );
}
