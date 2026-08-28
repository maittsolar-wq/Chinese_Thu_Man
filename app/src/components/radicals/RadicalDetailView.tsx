import Link from "next/link";
import type { HskLevel, RadicalDetail } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { EmptyState } from "@/components/ui/EmptyState";
import { HskLevelBadge } from "@/components/ui/Badge";

const ALL_LEVELS: HskLevel[] = [1, 2, 3, 4, 5, 6];

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
          <span className="rounded-full bg-neutral-100 px-2.5 py-0.5 text-xs font-medium text-neutral-600">
            Bộ thủ số {radical.kangxiIndex}
          </span>
          <span className="rounded-full bg-neutral-100 px-2.5 py-0.5 text-xs font-medium text-neutral-600">
            {radical.strokeCount} nét
          </span>
        </div>

        <p className="text-6xl font-bold leading-tight text-neutral-900">
          {radical.radical}
        </p>
        <p className="text-xl text-neutral-600">{radical.pinyin}</p>
        <p className="text-lg text-neutral-800">
          {radical.nameVi} — {radical.meaningVi}
        </p>
        {radical.variants.length > 0 && (
          <p className="text-sm text-neutral-500">
            Biến thể: {radical.variants.join(", ")}
          </p>
        )}
      </Card>

      <section>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-neutral-600">
          Chữ Hán liên quan ({radical.characterCount})
        </h2>
        {radical.characters.length > 0 ? (
          <Card className="flex flex-wrap gap-2">
            {radical.characters.map((character) => (
              <span
                key={character.character}
                title={character.hskLevels.map((level) => `HSK ${level}`).join(", ")}
                className="flex h-11 w-11 items-center justify-center rounded-md border border-neutral-200 text-xl font-medium text-neutral-900"
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
          <h2 className="text-sm font-semibold uppercase tracking-wide text-neutral-600">
            Từ vựng HSK theo bộ thủ này
          </h2>
          <span className="text-sm text-neutral-500">
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
              return (
                <div key={level}>
                  <div className="mb-2 flex items-center gap-2">
                    <HskLevelBadge level={level} />
                    <span className="text-xs text-neutral-500">{entries.length} từ</span>
                  </div>
                  <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                    {entries.map((entry) => (
                      <Link
                        key={entry.vocabularyId}
                        href={`/vocabulary/${entry.vocabularyId}?from=radical&radicalId=${radical.id}`}
                        className="block"
                      >
                        <Card className="hover:shadow-md">
                          <p className="text-xl font-semibold text-neutral-900">
                            {entry.word}
                          </p>
                          <p className="text-sm text-neutral-600">{entry.pinyin}</p>
                          {entry.meaningVi && (
                            <p className="truncate text-sm text-neutral-800">
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
