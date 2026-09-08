import Image from "next/image";
import type { VocabularyWord } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { Breadcrumb, type BreadcrumbItem } from "@/components/ui/Breadcrumb";
import { LinkButton } from "@/components/ui/Button";
import { ArrowLeftIcon } from "@/components/ui/icons";
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
      <h2 className="font-ui text-2xl font-semibold text-ink dark:text-night-text">{title}</h2>
      {subtitle && <p className="font-ui text-base text-ink-muted dark:text-night-muted">{subtitle}</p>}
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
  backHref,
  relatedWordReturnTo,
  radicalReturnTo,
}: {
  word: VocabularyWord;
  breadcrumb: BreadcrumbItem[];
  /** Navigation-completion pass: when set — the HSK-level-list origin
   *  (`from=hsk`), Home's own inline search widget (`from=dictionary&
   *  parent=home`), the DictionarySearchPopup, or Related Vocabulary
   *  (`from=related`), see vocabulary/[id]/page.tsx — renders a "Quay
   *  lại" Back button instead of `breadcrumb`. Undefined for every other
   *  origin (Radical, direct/param-less access) — those keep rendering
   *  `<Breadcrumb items={breadcrumb} />` exactly as before, byte-for-byte
   *  unchanged. */
  backHref?: string;
  /** Related Vocabulary Back pass: THIS page's own full URL (built
   *  server-side in vocabulary/[id]/page.tsx's `buildCurrentPageUrl`),
   *  handed to each Related Word link below as ITS `returnTo` — clicking
   *  one always returns to exactly this page, never Home/HSK/Dictionary,
   *  and the chain naturally extends however many `related` hops deep a
   *  visitor goes (A -> B -> C: C's Back goes to B, B's Back goes to A). */
  relatedWordReturnTo: string;
  /** Vocabulary -> Radical navigation-context fix: the exact same full
   *  URL as `relatedWordReturnTo` above (same underlying value, separate
   *  prop only so each consumer keeps its own clear name/doc-comment),
   *  handed to every Radical link in "Bộ thủ & chữ Hán" below as
   *  `?from=radical&returnTo=<this>`. Radical Detail resolves that into
   *  its own "Quay lại" pointing back to exactly this Vocabulary Detail
   *  page — see radicals/[id]/page.tsx's `resolveBackHref`. */
  radicalReturnTo: string;
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

  // Vocabulary -> Radical navigation-context fix: every Radical link
  // below carries this page's own exact URL as `returnTo`, reusing the
  // identical `?from=<x>&returnTo=<encoded URL>` shape Related Word links
  // already use (see the href below and RelatedWordCard's own href) —
  // not a new query-param convention.
  const radicalHrefSuffix = `?from=radical&returnTo=${encodeURIComponent(radicalReturnTo)}`;

  return (
    <div className="mx-auto flex max-w-[1120px] flex-col gap-8 bg-surface-page px-4 py-6 dark:bg-night-bg sm:gap-12 sm:px-6 sm:py-8 lg:gap-14">
      {backHref ? (
        <LinkButton href={backHref} variant="neutral" className="font-ui w-fit">
          <ArrowLeftIcon className="h-4 w-4" />
          Quay lại
        </LinkButton>
      ) : (
        <Breadcrumb items={breadcrumb} />
      )}

      {/* VOCABULARY HEADER — hero-redesign pass: the pronunciation button
          sits directly beside the Chinese title (`gap-3` = 12px, within
          the requested 12-16px range) — it reads as part of the title,
          not a stray control off on its own. Unchanged by the spacing-
          refinement pass below.

          Spacing-refinement pass: the card is a two-column row — content
          (badges -> word+pronunciation -> pinyin -> meaning -> metadata,
          hierarchy unchanged) on the left, illustration on the right.
          Inner horizontal padding steps up to `lg:px-16` (64px, within
          the requested 56-72px) at the desktop breakpoint where the
          illustration is actually visible, instead of staying at the
          original `sm:px-8` (32px) throughout — content now sits
          noticeably clear of the card's left edge on desktop. The
          content/illustration gap drops from `gap-6 lg:gap-10` to
          `gap-4 lg:gap-6`, closing the empty band that used to sit
          between them, and the illustration itself grows from `32%`
          (`sm:w-[32%]`) to `36%` (`w-[36%]`) of the row's width — with
          the 1120px content cap and the new lg:px-16 padding, that's
          ~357px at both 1440 and 1280px viewports, inside the requested
          300-360px/36-40% targets. `object-contain object-right` is
          unchanged, so the artwork (a transparent-background cutout, not
          a rectangular photo) is still never cropped and never overlaps
          the text column. Hidden below `sm` (illustration is supporting
          content, not primary; keeping the vocabulary hierarchy at full
          width on narrow screens matters more than showing a shrunk
          illustration there) — the same breakpoint convention already
          used throughout this app (e.g. HSK's `grid-cols-1
          sm:grid-cols-2`). */}
      <header className="rounded-card border border-hairline bg-white px-5 py-6 dark:border-night-border dark:bg-night-surface sm:px-8 sm:py-8 md:px-10 lg:px-16">
        <div className="flex items-center gap-4 lg:gap-6">
          <div className="flex min-w-0 flex-1 flex-col gap-3">
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

            <div className="flex items-center gap-3">
              <h1 className="font-cjk text-6xl font-medium leading-tight text-ink dark:text-night-text lg:text-cjk-hero">
                {word.word}
              </h1>
              <PronunciationButton wordUrl={word.audio.wordUrl} />
            </div>

            <p className="font-ui text-lg italic text-primary dark:text-night-primary">{word.pinyin}</p>

            <p className="font-ui text-xl font-semibold text-ink dark:text-night-text">{word.meaningVi}</p>

            <div className="font-ui mt-1 inline-flex w-fit items-center gap-2 rounded-full border border-hairline px-3 py-1 text-sm text-ink-muted dark:border-night-border dark:text-night-muted">
              <span>{characterCount} chữ</span>
              <span aria-hidden="true">·</span>
              <span>{word.strokeCount ?? "—"} nét</span>
            </div>
          </div>

          <div className="relative hidden h-40 w-[36%] shrink-0 sm:block sm:h-48 lg:h-60">
            <Image
              src="/vocabulary-hero-illustration.png"
              alt=""
              fill
              aria-hidden
              sizes="(min-width: 1024px) 360px, 260px"
              className="object-contain object-right"
            />
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
            className="font-ui shrink-0 whitespace-nowrap rounded-md px-3 py-2 text-sm font-medium text-ink-muted transition-colors hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-1 dark:text-night-muted dark:hover:text-night-text"
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
                hrefSuffix={radicalHrefSuffix}
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
                href={`/vocabulary/${related.id}?from=related&returnTo=${encodeURIComponent(relatedWordReturnTo)}`}
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
                <p className="font-ui text-base italic leading-normal text-primary dark:text-night-primary">
                  {example.pinyin}
                </p>
                <p className="font-ui text-base leading-relaxed text-ink-muted dark:text-night-muted">
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
