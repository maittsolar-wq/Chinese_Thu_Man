import Link from "next/link";
import type { VocabularyWord } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { Breadcrumb, type BreadcrumbItem } from "@/components/ui/Breadcrumb";
import { HskLevelBadge } from "@/components/ui/Badge";
import { EmptyState } from "@/components/ui/EmptyState";
import { getVocabularyById } from "@/lib/data/vocabularyRepository";

/**
 * The single canonical Word Detail view. Used by /vocabulary/[id] and
 * rendered no matter where the visitor arrived from (HSK Word List,
 * Dictionary results, or a radical's related-vocabulary list) — per
 * docs/DICTIONARY/DICTIONARY_SPEC.md §15, there is exactly one
 * implementation, only the breadcrumb trail changes.
 */
export function VocabularyDetail({
  word,
  breadcrumb,
}: {
  word: VocabularyWord;
  breadcrumb: BreadcrumbItem[];
}) {
  const relatedWords = word.relatedWordIds
    .map((id) => getVocabularyById(id))
    .filter((related): related is VocabularyWord => related !== null);

  const hasAudio = Boolean(word.audio.wordUrl);

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb items={breadcrumb} />

      <Card className="flex flex-col gap-3 p-6 sm:p-8">
        <div className="flex flex-wrap items-center gap-2">
          {word.hskLevels.map((level) => (
            <HskLevelBadge key={level} level={level} href={`/hsk/${level}`} />
          ))}
          {word.partOfSpeech.map((pos) => (
            <span
              key={pos}
              className="rounded-full bg-neutral-100 px-2.5 py-0.5 text-xs font-medium text-neutral-600"
            >
              {pos}
            </span>
          ))}
        </div>

        <p className="text-5xl font-bold leading-tight text-neutral-900">{word.word}</p>
        <p className="text-xl text-neutral-600">{word.pinyin}</p>
        <p className="text-lg text-neutral-800">{word.meaningVi}</p>

        {hasAudio && (
          <button
            type="button"
            className="mt-1 inline-flex w-fit items-center gap-2 rounded-md border border-primary px-3 py-1.5 text-sm font-medium text-primary hover:bg-primary-light"
          >
            🔊 Nghe phát âm
          </button>
        )}
      </Card>

      <section className="grid gap-4 sm:grid-cols-2">
        <Card>
          <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-neutral-600">
            Số nét
          </h2>
          {word.strokeCount != null ? (
            <p className="text-2xl font-semibold text-neutral-900">{word.strokeCount}</p>
          ) : (
            <p className="text-sm text-neutral-500">Chưa có dữ liệu số nét.</p>
          )}
        </Card>

        <Card>
          <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-neutral-600">
            Thứ tự nét viết
          </h2>
          <p className="text-sm text-neutral-500">Chưa có dữ liệu thứ tự nét viết.</p>
        </Card>
      </section>

      <section>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-neutral-600">
          Từ liên quan
        </h2>
        {relatedWords.length > 0 ? (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {relatedWords.map((related) => (
              <Link
                key={related.id}
                href={`/vocabulary/${related.id}`}
                className="block"
              >
                <Card className="hover:shadow-md">
                  <p className="text-xl font-semibold text-neutral-900">{related.word}</p>
                  <p className="text-sm text-neutral-600">{related.pinyin}</p>
                  <p className="truncate text-sm text-neutral-800">{related.meaningVi}</p>
                </Card>
              </Link>
            ))}
          </div>
        ) : (
          <EmptyState title="Chưa có từ liên quan cho mục này." />
        )}
      </section>

      <section>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-neutral-600">
          Câu ví dụ
        </h2>
        {word.examples.length > 0 ? (
          <div className="flex flex-col gap-3">
            {word.examples.map((example, index) => (
              <Card key={index}>
                <p className="text-lg font-medium text-neutral-900">{example.chinese}</p>
                <p className="text-sm text-neutral-600">{example.pinyin}</p>
                <p className="text-sm text-neutral-800">{example.meaningVi}</p>
              </Card>
            ))}
          </div>
        ) : (
          <EmptyState title="Chưa có câu ví dụ cho từ này." />
        )}
      </section>
    </div>
  );
}
