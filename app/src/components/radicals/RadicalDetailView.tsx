import type { RadicalDetail } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { LinkButton } from "@/components/ui/Button";
import { ArrowLeftIcon } from "@/components/ui/icons";
import { EmptyState } from "@/components/ui/EmptyState";
import { RadicalVocabularyByLevel } from "@/components/radicals/RadicalVocabularyByLevel";

/**
 * Radical Detail reuses Vocabulary Detail's visual language (Card,
 * HskLevelBadge, typography scale) but has its own information hierarchy
 * — it is not a copy of VocabularyDetail, and its "related vocabulary"
 * links out to the shared /vocabulary/[id] page rather than rendering
 * word details itself.
 *
 * Navigation-fix pass: the old "Trang chủ > Bộ thủ > [glyph]" Breadcrumb
 * is gone, replaced by the same source-aware "Quay lại" Back button
 * pattern HSK Detail (/hsk/[level]) already established — same
 * `LinkButton variant="neutral"` + ArrowLeftIcon + "Quay lại", no new
 * button style invented. `backHref` is computed server-side in
 * radicals/[id]/page.tsx from `?from=`, not read here.
 */
export function RadicalDetailView({
  radical,
  relatedWordReturnTo,
  backHref,
}: {
  radical: RadicalDetail;
  /** This page's own exact canonical URL (id + every `from`/`parent`
   *  search param it was loaded with), computed server-side by the page.
   *  Every related-vocabulary link hands this to Vocabulary Detail as
   *  `?from=related&returnTo=<this>`, so Back returns to the EXACT
   *  Radical Detail page — the same mechanism Related Vocabulary already
   *  uses on Vocabulary Detail itself. */
  relatedWordReturnTo: string;
  /** Deterministic Back destination, resolved from `?from=` by the page
   *  (home/hsk/radicals, safe "/radicals" fallback otherwise). */
  backHref: string;
}) {
  return (
    <div className="flex flex-col gap-6">
      <LinkButton href={backHref} variant="neutral" className="font-ui w-fit">
        <ArrowLeftIcon className="h-4 w-4" />
        Quay lại
      </LinkButton>

      <Card className="flex flex-col gap-3 p-6 sm:p-8">
        <div className="flex flex-wrap items-center gap-2">
          <span className="font-ui rounded-full bg-neutral-100 px-2.5 py-0.5 text-xs font-medium text-neutral-600 dark:bg-night-input dark:text-night-muted">
            Bộ thủ số {radical.kangxiIndex}
          </span>
          <span className="font-ui rounded-full bg-neutral-100 px-2.5 py-0.5 text-xs font-medium text-neutral-600 dark:bg-night-input dark:text-night-muted">
            {radical.strokeCount} nét
          </span>
        </div>

        <h1 className="font-cjk text-6xl font-bold leading-tight text-neutral-900 dark:text-night-text">
          {radical.radical}
        </h1>
        <p className="font-ui text-xl italic text-primary dark:text-night-primary">{radical.pinyin}</p>
        <p className="font-ui text-lg text-neutral-800 dark:text-night-text">
          {radical.nameVi} — {radical.meaningVi}
        </p>
        {radical.variants.length > 0 && (
          <p className="font-ui text-sm text-neutral-500 dark:text-night-muted">
            Biến thể: <span className="font-cjk">{radical.variants.join(", ")}</span>
          </p>
        )}
      </Card>

      <section>
        <h2 className="font-ui mb-3 text-sm font-semibold uppercase tracking-wide text-neutral-600 dark:text-night-muted">
          Chữ Hán liên quan ({radical.characterCount})
        </h2>
        {radical.characters.length > 0 ? (
          <Card className="flex flex-wrap gap-2">
            {radical.characters.map((character) => (
              <span
                key={character.character}
                title={character.hskLevels.map((level) => `HSK ${level}`).join(", ")}
                className="flex h-11 w-11 items-center justify-center rounded-md border border-neutral-200 font-cjk text-xl font-medium text-neutral-900 dark:border-night-border dark:text-night-text"
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
          <h2 className="font-ui text-sm font-semibold uppercase tracking-wide text-neutral-600 dark:text-night-muted">
            Từ vựng HSK theo bộ thủ này
          </h2>
          <span className="font-ui text-sm text-neutral-500 dark:text-night-muted">
            {radical.vocabularyCount} từ vựng
          </span>
        </div>

        {radical.vocabularyCount === 0 ? (
          <EmptyState
            title="Bộ thủ này chưa xuất hiện trong từ vựng HSK 1–6."
            description="Đây là dữ liệu hợp lệ — không phải lỗi tải dữ liệu."
          />
        ) : (
          <RadicalVocabularyByLevel
            vocabularyByLevel={radical.vocabularyByLevel}
            relatedWordReturnTo={relatedWordReturnTo}
          />
        )}
      </section>
    </div>
  );
}
