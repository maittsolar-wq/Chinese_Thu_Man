import type { VocabularyWord } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { Breadcrumb, type BreadcrumbItem } from "@/components/ui/Breadcrumb";
import { HskLevelBadge, Badge } from "@/components/ui/Badge";
import { EmptyState } from "@/components/ui/EmptyState";
import { RadicalCard } from "@/components/radicals/RadicalCard";
import { StrokeOrderViewer } from "@/components/vocabulary/StrokeOrderViewer";
import { PronunciationButton } from "@/components/vocabulary/PronunciationButton";
import { RelatedWordCard } from "@/components/vocabulary/RelatedWordCard";
import { getVocabularyById } from "@/lib/data/vocabularyRepository";
import { getRadicalsForVocabularyId, getRadicalVocabularyCount } from "@/lib/data/radicalRepository";
import { getCharactersForWord } from "@/lib/data/strokeOrderLoader";

const SECTIONS = [
  { id: "stroke-order", label: "Nét chữ" },
  { id: "radical", label: "Bộ thủ" },
  { id: "related-words", label: "Từ liên quan" },
  { id: "examples", label: "Ví dụ" },
] as const;

/**
 * One visual language for every section heading on this page: a normal-
 * case (not uppercase/colored-eyebrow) title plus an optional one-line
 * Vietnamese subtitle. `text-2xl` (24px) sits inside both the approved
 * desktop (24-26px) and mobile (22-24px) ranges, so the title needs no
 * responsive split; the subtitle uses `text-base` (16px) uniformly for
 * the same reason (15-16px, no separate mobile/desktop values given).
 * Local to this file -- not yet a shared primitive, since no other screen
 * uses this heading shape yet.
 */
function SectionHeading({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="flex flex-col gap-1">
      <h2 className="text-2xl font-semibold text-ink dark:text-night-text">{title}</h2>
      {subtitle && <p className="text-base text-ink-muted dark:text-night-muted">{subtitle}</p>}
    </div>
  );
}

/**
 * The single canonical Word Detail view. Used by /vocabulary/[id] and
 * rendered no matter where the visitor arrived from (HSK Word List,
 * Dictionary results, or a radical's related-vocabulary list) — per
 * docs/DICTIONARY/DICTIONARY_SPEC.md §15, there is exactly one
 * implementation, only the breadcrumb trail changes.
 *
 * UI Foundation Phase: the four learning sections (Nét chữ / Bộ thủ & chữ
 * Hán / Từ liên quan / Ví dụ) are no longer hidden behind Tabs — every
 * section is always mounted AND always visible in the DOM, laid out one
 * after another on a single continuously-scrollable page, with a small
 * anchor-link nav (real `<a href="#section-id">`s, no JS state) to jump
 * between them. This removes the "pick one thing to read" tab model in
 * favor of "scroll to read everything" — same 4 destinations, same IDs
 * conceptually, same data, just no more mount/unmount or hidden-attribute
 * toggling. `Tabs.tsx` itself is untouched and no longer imported here
 * (it has no other consumer, so it's simply unused now, not deleted).
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

  // Same character-splitting/digit-suffix-normalization logic Stroke Order
  // already uses (tools/hsk/stroke_order) — one source of truth, not a
  // second regex, for "how many real Han characters does this word have".
  const characterCount = getCharactersForWord(word.word).length;

  return (
    <div className="mx-auto flex max-w-[1120px] flex-col gap-8 bg-surface-page px-4 py-6 dark:bg-night-bg sm:gap-12 sm:px-6 sm:py-8 lg:gap-14">
      <Breadcrumb items={breadcrumb} />

      {/* VOCABULARY HEADER — visual-refinement pass: back to a single
          white card (no more 2fr/1fr composition or blue-tinted surface),
          matching the approved reference exactly: badges row, then the
          Chinese word with the speaker button on the same line pinned to
          the right edge, pinyin on its own line, meaning below, and one
          compact bordered pill ("2 chữ · 8 nét") in place of the earlier
          three-item metadata block/column. HSK level is not repeated in
          the pill since it's already shown as a badge above. Content
          itself (badges -> word -> pronunciation -> meaning) is
          unchanged; only its size, alignment, and surrounding card
          changed. */}
      <header className="rounded-card border border-hairline bg-white px-5 py-6 dark:border-night-border dark:bg-night-surface sm:px-8 sm:py-8">
        <div className="flex flex-col gap-3">
          <div className="flex flex-wrap items-center gap-2">
            {word.hskLevels.map((level) => (
              <HskLevelBadge key={level} level={level} href={`/hsk/${level}`} />
            ))}
            {word.partOfSpeech.map((pos) => (
              <Badge key={pos} tone="neutral">
                {pos}
              </Badge>
            ))}
          </div>

          <div className="flex items-start justify-between gap-3">
            <h1 className="font-cjk text-6xl font-medium leading-tight text-ink dark:text-night-text lg:text-cjk-hero">
              {word.word}
            </h1>
            <PronunciationButton wordUrl={word.audio.wordUrl} />
          </div>

          <p className="text-lg italic text-primary dark:text-night-primary">{word.pinyin}</p>

          <p className="text-xl font-semibold text-ink dark:text-night-text">{word.meaningVi}</p>

          <div className="mt-1 inline-flex w-fit items-center gap-2 rounded-full border border-hairline px-3 py-1 text-sm text-ink-muted dark:border-night-border dark:text-night-muted">
            <span>{characterCount} chữ</span>
            <span aria-hidden="true">·</span>
            <span>{word.strokeCount ?? "—"} nét</span>
          </div>
        </div>
      </header>

      {/* SECTION QUICK NAV — plain anchor links, no JS, no tab semantics:
          clicking scrolls to the section (see globals.css for the
          reduced-motion-aware `scroll-behavior: smooth`). Every section
          below is always in the DOM; this is a wayfinding aid, not a
          content switch. Text bumped to 14px minimum with a clearer
          primary-blue active/hover state per the visual-refinement pass. */}
      <nav aria-label="Điều hướng nội dung từ vựng" className="flex gap-1 overflow-x-auto border-b border-hairline pb-2">
        {SECTIONS.map((section) => (
          <a
            key={section.id}
            href={`#${section.id}`}
            className="shrink-0 whitespace-nowrap rounded-md px-3 py-2 text-sm font-medium text-ink-muted transition-colors hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-1 dark:text-night-muted dark:hover:text-night-text"
          >
            {section.label}
          </a>
        ))}
      </nav>

      {/* NÉT CHỮ */}
      <section id="stroke-order" className="scroll-mt-20 flex flex-col gap-4">
        <SectionHeading title="Nét chữ" subtitle={`Cách viết và thứ tự các nét của ${word.word}`} />
        <StrokeOrderViewer word={word.word} />
      </section>

      {/* BỘ THỦ & CHỮ HÁN */}
      <section id="radical" className="scroll-mt-20 flex flex-col gap-4">
        <SectionHeading title="Bộ thủ & chữ Hán" subtitle="Thành phần cấu tạo nên chữ" />
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
          <EmptyState title="Chưa có dữ liệu bộ thủ cho từ này." />
        )}
      </section>

      {/* TỪ LIÊN QUAN */}
      <section id="related-words" className="scroll-mt-20 flex flex-col gap-4">
        <SectionHeading title="Từ liên quan" subtitle="Các từ vựng cùng chữ hoặc cùng chủ đề" />
        {relatedWords.length > 0 ? (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {relatedWords.map((related) => (
              <RelatedWordCard
                key={related.id}
                href={`/vocabulary/${related.id}`}
                hanzi={related.word}
                pinyin={related.pinyin}
                meaningVi={related.meaningVi}
              />
            ))}
          </div>
        ) : (
          <EmptyState title="Chưa có từ liên quan cho mục này." />
        )}
      </section>

      {/* VÍ DỤ */}
      <section id="examples" className="scroll-mt-20 flex flex-col gap-4">
        <SectionHeading title="Ví dụ" subtitle="Câu ví dụ sử dụng từ này" />
        {word.examples.length > 0 ? (
          <div className="flex flex-col gap-3">
            {word.examples.map((example, index) => (
              <Card key={index} className="flex flex-col gap-2 p-5 sm:p-6">
                <p className="font-cjk text-3xl font-normal leading-snug text-ink dark:text-night-text">
                  {example.chinese}
                </p>
                <p className="text-base italic leading-normal text-primary dark:text-night-primary">
                  {example.pinyin}
                </p>
                <p className="text-base leading-relaxed text-ink-muted dark:text-night-muted">
                  {example.meaningVi}
                </p>
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
