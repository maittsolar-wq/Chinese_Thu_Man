import Link from "next/link";
import type { HskLevel, RadicalDetail, RadicalVocabularyRef } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { EmptyState } from "@/components/ui/EmptyState";
import { HskLevelBadge } from "@/components/ui/Badge";

const ALL_LEVELS: HskLevel[] = [1, 2, 3, 4, 5, 6];

/**
 * A vocabulary word can contain multiple characters that map to the same
 * radical (e.g. both 一 and 下 in 一下 map to radical 一), so the same
 * vocabularyId can legitimately appear more than once within a level's
 * entries. Dedupe here at render time only — the source mapping JSON is
 * left untouched — keeping the first occurrence.
 */
function dedupeByVocabularyId(
  entries: RadicalVocabularyRef[]
): RadicalVocabularyRef[] {
  const seen = new Set<string>();
  const result: RadicalVocabularyRef[] = [];
  for (const entry of entries) {
    if (seen.has(entry.vocabularyId)) continue;
    seen.add(entry.vocabularyId);
    result.push(entry);
  }
  return result;
}

/**
 * Radical Detail reuses Vocabulary Detail's visual language (Card,
 * Breadcrumb, HskLevelBadge, typography scale) but has its own
 * information hierarchy — it is not a copy of VocabularyDetail, and its
 * "related vocabulary" links out to the shared /vocabulary/[id] page
 * rather than rendering word details itself.
 */
export function RadicalDetailView({ radical }: { radical: RadicalDetail }) {
  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb
        items={[
          { label: "Trang chủ", href: "/" },
          { label: "Bộ thủ", href: "/radicals" },
          { label: radical.radical },
        ]}
      />

      <Card className="flex flex-col gap-3 p-6 sm:p-8">
        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-full bg-neutral-100 px-2.5 py-0.5 text-xs font-medium text-neutral-600 dark:bg-night-input dark:text-night-muted">
            Bộ thủ số {radical.kangxiIndex}
          </span>
          <span className="rounded-full bg-neutral-100 px-2.5 py-0.5 text-xs font-medium text-neutral-600 dark:bg-night-input dark:text-night-muted">
            {radical.strokeCount} nét
          </span>
        </div>

        <p className="text-6xl font-bold leading-tight text-neutral-900 dark:text-night-text">
          {radical.radical}
        </p>
        <p className="text-xl text-neutral-600 dark:text-night-muted">{radical.pinyin}</p>
        <p className="text-lg text-neutral-800 dark:text-night-text">
          {radical.nameVi} — {radical.meaningVi}
        </p>
        {radical.variants.length > 0 && (
          <p className="text-sm text-neutral-500 dark:text-night-muted">
            Biến thể: {radical.variants.join(", ")}
          </p>
        )}
      </Card>

      <section>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-neutral-600 dark:text-night-muted">
          Chữ Hán liên quan ({radical.characterCount})
        </h2>
        {radical.characters.length > 0 ? (
          <Card className="flex flex-wrap gap-2">
            {radical.characters.map((character) => (
              <span
                key={character.character}
                title={character.hskLevels.map((level) => `HSK ${level}`).join(", ")}
                className="flex h-11 w-11 items-center justify-center rounded-md border border-neutral-200 text-xl font-medium text-neutral-900 dark:border-night-border dark:text-night-text"
              >
                {character.character}
              </span>
            ))}
          </Card>
        ) : (
          <EmptyState title="Chưa có chữ Hán được ghi nhận cho bộ thủ này." />
        )}
      </section>

      <section>
        <div className="mb-3 flex items-baseline justify-between">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-neutral-600 dark:text-night-muted">
            Từ vựng HSK theo bộ thủ này
          </h2>
          <span className="text-sm text-neutral-500 dark:text-night-muted">
            {radical.vocabularyCount} từ vựng
          </span>
        </div>

        {radical.vocabularyCount === 0 ? (
          <EmptyState
            title="Bộ thủ này chưa xuất hiện trong từ vựng HSK 1–6."
            description="Đây là dữ liệu hợp lệ — không phải lỗi tải dữ liệu."
          />
        ) : (
          <div className="flex flex-col gap-5">
            {ALL_LEVELS.map((level) => {
              const entries = radical.vocabularyByLevel[level];
              if (!entries || entries.length === 0) return null;
              const dedupedEntries = dedupeByVocabularyId(entries);
              return (
                <div key={level}>
                  <div className="mb-2 flex items-center gap-2">
                    <HskLevelBadge level={level} />
                    <span className="text-xs text-neutral-500 dark:text-night-muted">
                      {dedupedEntries.length} từ
                    </span>
                  </div>
                  <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                    {dedupedEntries.map((entry) => (
                      <Link
                        key={entry.vocabularyId}
                        href={`/vocabulary/${entry.vocabularyId}?from=radical&radicalId=${radical.id}`}
                        className="block min-w-0"
                      >
                        <Card className="hover:shadow-md">
                          <p className="text-xl font-semibold text-neutral-900 dark:text-night-text">
                            {entry.word}
                          </p>
                          <p className="text-sm text-neutral-600 dark:text-night-muted">{entry.pinyin}</p>
                          {entry.meaningVi && (
                            <p className="truncate text-sm text-neutral-800 dark:text-night-text">
                              {entry.meaningVi}
                            </p>
                          )}
                        </Card>
                      </Link>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}
