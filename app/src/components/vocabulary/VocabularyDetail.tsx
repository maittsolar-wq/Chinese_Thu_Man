import Link from "next/link";
import type { VocabularyWord } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { Breadcrumb, type BreadcrumbItem } from "@/components/ui/Breadcrumb";
import { HskLevelBadge } from "@/components/ui/Badge";
import { EmptyState } from "@/components/ui/EmptyState";
import { RadicalCard } from "@/components/radicals/RadicalCard";
import { getVocabularyById } from "@/lib/data/vocabularyRepository";
import { getRadicalsForVocabularyId, getRadicalVocabularyCount } from "@/lib/data/radicalRepository";

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

  // Real data, resolved through the same radical_vocabulary_mapping.json /
  // getRadicalSummaryById() already used by Radical Detail (P3.1) — never
  // a second radical data source. [] here is defensive; every word in the
  // current production data resolves to at least one radical.
  const radicals = getRadicalsForVocabularyId(word.id);

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
              className="rounded-full bg-neutral-100 px-2.5 py-0.5 text-xs font-medium text-neutral-600 dark:bg-night-input dark:text-night-muted"
            >
              {pos}
            </span>
          ))}
        </div>

        <p className="text-5xl font-bold leading-tight text-neutral-900 dark:text-night-text">{word.word}</p>
        <p className="text-xl text-neutral-600 dark:text-night-muted">{word.pinyin}</p>
        <p className="text-lg text-neutral-800 dark:text-night-text">{word.meaningVi}</p>
      </Card>

      <section>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-neutral-600 dark:text-night-muted">
          Số nét
        </h2>
        {word.strokeCount != null ? (
          <Card className="sm:max-w-xs">
            <p className="text-2xl font-semibold text-neutral-900 dark:text-night-text">{word.strokeCount}</p>
          </Card>
        ) : (
          <EmptyState title="Chưa có dữ liệu số nét." />
        )}
      </section>

      {radicals.length > 0 && (
        <section>
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-neutral-600 dark:text-night-muted">
            Bộ thủ
          </h2>
          <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
            {radicals.map((radical) => (
              <RadicalCard
                key={radical.id}
                radical={radical}
                vocabularyCount={getRadicalVocabularyCount(radical.id)}
              />
            ))}
          </div>
        </section>
      )}

      <section>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-neutral-600 dark:text-night-muted">
          Từ liên quan
        </h2>
        {relatedWords.length > 0 ? (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {relatedWords.map((related) => (
              <Link
                key={related.id}
                href={`/vocabulary/${related.id}`}
                className="block min-w-0"
              >
                <Card className="hover:shadow-md">
                  <p className="text-xl font-semibold text-neutral-900 dark:text-night-text">{related.word}</p>
                  <p className="text-sm text-neutral-600 dark:text-night-muted">{related.pinyin}</p>
                  <p className="truncate text-sm text-neutral-800 dark:text-night-text">{related.meaningVi}</p>
                </Card>
              </Link>
            ))}
          </div>
        ) : (
          <EmptyState title="Chưa có từ liên quan cho mục này." />
        )}
      </section>

      <section>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-neutral-600 dark:text-night-muted">
          Câu ví dụ
        </h2>
        {word.examples.length > 0 ? (
          <div className="flex flex-col gap-3">
            {word.examples.map((example, index) => (
              <Card key={index}>
                <p className="text-lg font-medium text-neutral-900 dark:text-night-text">{example.chinese}</p>
                <p className="text-sm text-neutral-600 dark:text-night-muted">{example.pinyin}</p>
                <p className="text-sm text-neutral-800 dark:text-night-text">{example.meaningVi}</p>
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
