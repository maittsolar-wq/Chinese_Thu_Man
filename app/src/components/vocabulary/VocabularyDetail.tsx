import type { ReactNode } from "react";
import type { VocabularyWord } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { Breadcrumb, type BreadcrumbItem } from "@/components/ui/Breadcrumb";
import { HskLevelBadge, Badge } from "@/components/ui/Badge";
import { EmptyState } from "@/components/ui/EmptyState";
import { PencilIcon, BookOpenIcon, GraduationCapIcon } from "@/components/ui/icons";
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
 * Vietnamese subtitle, sized per the approved scale (20-24px desktop,
 * 18-20px mobile). Local to this file -- not yet a shared primitive, since
 * no other screen uses this heading shape yet.
 */
function SectionHeading({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="flex flex-col gap-1">
      <h2 className="text-lg font-semibold text-ink dark:text-night-text sm:text-2xl">{title}</h2>
      {subtitle && <p className="text-sm text-ink-muted dark:text-night-muted sm:text-base">{subtitle}</p>}
    </div>
  );
}

type MetadataItem = {
  icon: (props: { className?: string }) => ReactNode;
  value: string;
  label: string;
};

/**
 * Phase 09: replaces the earlier three-dashboard-card Quick Info strip.
 * These are QUICK METADATA, not a peer content block to the hero — they
 * must visibly "sit back" from the Chinese character, not compete with
 * it. Two call sites render the SAME data in two non-overlapping
 * presentations (each wrapped by its own caller in a responsive
 * visibility class, so exactly one exists in the accessible tree at any
 * viewport — see the two call sites in VocabularyDetail below):
 * "compact" is a single horizontal line for narrow viewports (icon +
 * value only, "·" separated — no room to spell "Số nét" three times on a
 * phone width); "list" is a small vertical stack for the desktop right
 * column (icon + value + label).
 */
function QuickMetadata({ items, variant }: { items: MetadataItem[]; variant: "compact" | "list" }) {
  if (variant === "compact") {
    return (
      <div className="flex flex-wrap items-center justify-center gap-x-3 gap-y-1">
        {items.map((item, index) => (
          <div key={item.label} className="flex items-center gap-1.5">
            {index > 0 && <span aria-hidden="true" className="text-ink-muted dark:text-night-muted">·</span>}
            <item.icon className="h-3.5 w-3.5 shrink-0 text-primary dark:text-night-primary" />
            <span className="text-sm font-medium text-ink dark:text-night-text">{item.value}</span>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      {items.map((item) => (
        <div key={item.label} className="flex items-center gap-2">
          <item.icon className="h-4 w-4 shrink-0 text-primary dark:text-night-primary" />
          <div className="flex flex-col leading-tight">
            <span className="text-sm font-medium text-ink dark:text-night-text">{item.value}</span>
            <span className="text-xs text-ink-muted dark:text-night-muted">{item.label}</span>
          </div>
        </div>
      ))}
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

  const metadataItems: MetadataItem[] = [
    { icon: PencilIcon, value: `${word.strokeCount ?? "—"} nét`, label: "Số nét" },
    { icon: GraduationCapIcon, value: `HSK ${word.hskLevels.join(", ")}`, label: "Cấp độ" },
    { icon: BookOpenIcon, value: `${characterCount} ký tự`, label: "Ký tự" },
  ];

  return (
    <div className="mx-auto flex max-w-[1120px] flex-col gap-8 sm:gap-12 lg:gap-14">
      <Breadcrumb items={breadcrumb} />

      {/* VOCABULARY HEADER — Phase 09: a two-column composition on wide
          viewports (content ~2/3, quick metadata ~1/3, via a single
          `lg:grid-cols-[2fr_1fr]`) instead of a tall centered hero
          followed by three large dashboard cards. Below `lg`, the same
          grid collapses to one column and the metadata block (rendered
          once, see QuickMetadata) simply falls in document order below
          the meaning line, matching the approved mobile stack. Content
          itself (badges -> word -> pronunciation -> meaning) is
          unchanged; only its size, alignment, and surrounding composition
          changed. Still a whisper of brand blue on the surface
          (`primary-wash`) -- no gradient, no illustration -- but
          noticeably shorter (padding cut roughly in half) despite the
          Chinese character growing, per "hero ngắn gọn hơn". */}
      <header className="rounded-2xl border border-hairline bg-primary-wash px-5 py-6 dark:border-night-border dark:bg-primary-dark/10 sm:px-8 sm:py-8">
        <div className="grid grid-cols-1 items-center gap-6 lg:grid-cols-[2fr_1fr] lg:items-start lg:gap-8">
          <div className="flex flex-col items-center gap-3 text-center lg:items-start lg:text-left">
            <div className="flex flex-wrap items-center justify-center gap-2 lg:justify-start">
              {word.hskLevels.map((level) => (
                <HskLevelBadge key={level} level={level} href={`/hsk/${level}`} />
              ))}
              {word.partOfSpeech.map((pos) => (
                <Badge key={pos} tone="neutral">
                  {pos}
                </Badge>
              ))}
            </div>

            <h1 className="font-cjk text-7xl font-medium leading-tight text-ink dark:text-night-text lg:text-cjk-hero">
              {word.word}
            </h1>

            <div className="flex items-center gap-3">
              <p className="text-2xl italic text-primary dark:text-night-primary lg:text-3xl">{word.pinyin}</p>
              <PronunciationButton wordUrl={word.audio.wordUrl} />
            </div>

            <p className="text-base text-ink dark:text-night-text lg:text-lg">{word.meaningVi}</p>

            {/* Mobile-only compact metadata row lives right under the
                meaning line, per the approved mobile order. The desktop
                column version of the same data renders from the sibling
                cell below. */}
            <div className="lg:hidden">
              <QuickMetadata items={metadataItems} variant="compact" />
            </div>
          </div>

          {/* RIGHT — quick metadata, desktop only. Deliberately "sits
              back" from the hero: small value/label pairs, no cards, no
              22px+ numerals, separated from the content column by a
              hairline rather than its own bordered box. */}
          <div className="hidden border-hairline dark:border-night-border lg:block lg:border-l lg:pl-8">
            <QuickMetadata items={metadataItems} variant="list" />
          </div>
        </div>
      </header>

      {/* SECTION QUICK NAV — plain anchor links, no JS, no tab semantics:
          clicking scrolls to the section (see globals.css for the
          reduced-motion-aware `scroll-behavior: smooth`). Every section
          below is always in the DOM; this is a wayfinding aid, not a
          content switch. */}
      <nav aria-label="Điều hướng nội dung từ vựng" className="flex gap-1 overflow-x-auto border-b border-hairline pb-2">
        {SECTIONS.map((section) => (
          <a
            key={section.id}
            href={`#${section.id}`}
            className="shrink-0 whitespace-nowrap rounded-md px-3 py-1.5 text-sm font-medium text-ink-muted transition-colors hover:bg-primary-wash hover:text-primary dark:text-night-muted dark:hover:bg-night-input dark:hover:text-night-text"
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
