import type { VocabularyWord } from "@/lib/data/types";
import { Panel } from "@/components/ui/Card";
import { Breadcrumb, type BreadcrumbItem } from "@/components/ui/Breadcrumb";
import { HskLevelBadge, Badge } from "@/components/ui/Badge";
import { Chip } from "@/components/ui/Chip";
import { EmptyState } from "@/components/ui/EmptyState";
import { Tabs, type TabItem } from "@/components/ui/Tabs";
import { RadicalCard } from "@/components/radicals/RadicalCard";
import { StrokeOrderViewer } from "@/components/vocabulary/StrokeOrderViewer";
import { SpeakerIcon } from "@/components/ui/icons";
import { getVocabularyById } from "@/lib/data/vocabularyRepository";
import { getRadicalsForVocabularyId, getRadicalVocabularyCount } from "@/lib/data/radicalRepository";
import { getCharactersForWord } from "@/lib/data/strokeOrderLoader";

/**
 * The single canonical Word Detail view. Used by /vocabulary/[id] and
 * rendered no matter where the visitor arrived from (HSK Word List,
 * Dictionary results, or a radical's related-vocabulary list) — per
 * docs/DICTIONARY/DICTIONARY_SPEC.md §15, there is exactly one
 * implementation, only the breadcrumb trail changes.
 *
 * Phase 02 redesign: what was six independently-scrolled, equally-weighted
 * sections is now a hero (word/pinyin/meaning/HSK/pronunciation — the
 * brief's own priority order) + a compact quick-facts strip + four
 * progressive-disclosure tabs. No data source, adapter contract, or route
 * changed — this is a rendering-only redesign. StrokeOrderViewer's engine
 * (loading, animation, reduced-motion, keyboard handling) is untouched;
 * only its section wrapper changed.
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

  const tabs: TabItem[] = [
    {
      id: "stroke",
      label: "Nét chữ",
      content: <StrokeOrderViewer word={word.word} />,
    },
    {
      id: "radical",
      label: "Bộ thủ & chữ Hán",
      content:
        radicals.length > 0 ? (
          <div className="flex flex-col gap-3">
            <p className="text-sm text-neutral-600 dark:text-night-muted">
              Chữ trong <span className="font-cjk font-semibold text-neutral-900 dark:text-night-text">{word.word}</span> dùng bộ thủ sau:
            </p>
            <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
              {radicals.map((radical) => (
                <RadicalCard
                  key={radical.id}
                  radical={radical}
                  vocabularyCount={getRadicalVocabularyCount(radical.id)}
                />
              ))}
            </div>
          </div>
        ) : (
          <EmptyState title="Chưa có dữ liệu bộ thủ cho từ này." />
        ),
    },
    {
      id: "related",
      label: "Từ liên quan",
      content:
        relatedWords.length > 0 ? (
          <div className="flex flex-wrap gap-2.5">
            {relatedWords.map((related) => (
              <Chip
                key={related.id}
                href={`/vocabulary/${related.id}`}
                hanzi={related.word}
                pinyin={related.pinyin}
              />
            ))}
          </div>
        ) : (
          <EmptyState title="Chưa có từ liên quan cho mục này." />
        ),
    },
    {
      id: "examples",
      label: "Ví dụ",
      content:
        word.examples.length > 0 ? (
          <div className="flex flex-col gap-4">
            {word.examples.map((example, index) => (
              <div key={index} className="border-b border-neutral-200 pb-4 last:border-0 last:pb-0 dark:border-night-border">
                <p className="font-cjk text-xl font-medium text-neutral-900 dark:text-night-text">
                  {example.chinese}
                </p>
                <p className="mt-1 text-sm italic text-primary dark:text-night-primary">{example.pinyin}</p>
                <p className="mt-0.5 text-sm text-neutral-600 dark:text-night-muted">{example.meaningVi}</p>
              </div>
            ))}
          </div>
        ) : (
          <EmptyState title="Chưa có câu ví dụ cho từ này." />
        ),
    },
  ];

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb items={breadcrumb} />

      {/* HERO — word -> pronunciation -> meaning -> HSK, the brief's own
          priority order. Borderless Panel, not a Card: this is the page's
          identity block, not one interactive item among others. */}
      <Panel className="flex flex-col gap-4 p-6 sm:p-8">
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

        <h1 className="font-cjk text-6xl font-semibold leading-tight text-neutral-900 dark:text-night-text sm:text-7xl">
          {word.word}
        </h1>

        <div className="flex items-center gap-3">
          <p className="text-xl italic text-primary dark:text-night-primary">{word.pinyin}</p>
          {/*
            Pronunciation slot (Phase 02 §10): audio DATA exists but no
            playback UI is implemented yet. This must not pretend to work —
            same disabled/aria-label pattern already established by
            FlashcardExerciseView's speaker button, so "not available yet"
            reads identically everywhere in the product. No audio request
            is triggered by rendering this button.
          */}
          <button
            type="button"
            disabled
            aria-label="Nghe phát âm (chưa khả dụng)"
            title="Nghe phát âm (chưa khả dụng)"
            className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary text-white disabled:cursor-not-allowed disabled:opacity-50"
          >
            <SpeakerIcon className="h-4 w-4" />
          </button>
        </div>

        <p className="text-lg text-neutral-800 dark:text-night-text">{word.meaningVi}</p>
      </Panel>

      {/* QUICK FACTS — a compact strip, not another full-weight card; a
          single stroke-count integer no longer gets a whole page section
          to itself. */}
      <div className="flex divide-x divide-neutral-200 overflow-x-auto rounded-card border border-neutral-200 bg-white dark:divide-night-border dark:border-night-border dark:bg-night-surface">
        <div className="flex min-w-[92px] flex-col gap-0.5 px-5 py-3">
          <span className="font-data text-lg font-semibold tabular-nums text-neutral-900 dark:text-night-text">
            {word.strokeCount ?? "—"}
          </span>
          <span className="text-xs text-neutral-500 dark:text-night-muted">Số nét</span>
        </div>
        <div className="flex min-w-[92px] flex-col gap-0.5 px-5 py-3">
          <span className="font-data text-lg font-semibold tabular-nums text-neutral-900 dark:text-night-text">
            {characterCount}
          </span>
          <span className="text-xs text-neutral-500 dark:text-night-muted">Ký tự</span>
        </div>
        <div className="flex min-w-[92px] flex-col gap-0.5 px-5 py-3">
          <span className="font-data text-lg font-semibold text-neutral-900 dark:text-night-text">
            {word.hskLevels.join(", ")}
          </span>
          <span className="text-xs text-neutral-500 dark:text-night-muted">Cấp độ HSK</span>
        </div>
      </div>

      {/* LEARNING TABS — progressive disclosure instead of six stacked
          cards. Panels stay mounted (see Tabs.tsx) so Stroke Order's own
          fetch timing is unchanged from before this redesign. */}
      <Tabs items={tabs} label="Nội dung học tập" />
    </div>
  );
}
