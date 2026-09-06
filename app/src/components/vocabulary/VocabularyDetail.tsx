import type { VocabularyWord } from "@/lib/data/types";
import { Card, Panel } from "@/components/ui/Card";
import { Breadcrumb, type BreadcrumbItem } from "@/components/ui/Breadcrumb";
import { HskLevelBadge, Badge } from "@/components/ui/Badge";
import { Chip } from "@/components/ui/Chip";
import { EmptyState } from "@/components/ui/EmptyState";
import { Tabs, type TabItem } from "@/components/ui/Tabs";
import { PencilIcon, BookOpenIcon, GraduationCapIcon } from "@/components/ui/icons";
import { RadicalCard } from "@/components/radicals/RadicalCard";
import { StrokeOrderViewer } from "@/components/vocabulary/StrokeOrderViewer";
import { PronunciationButton } from "@/components/vocabulary/PronunciationButton";
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
 * sections became a hero + quick-facts strip + four progressive-disclosure
 * tabs. UI Phase 01 (Modern Chinese Learning / Editorial direction) keeps
 * that exact information architecture and route/tab/data contracts, and
 * only restyles the hero (a focal, centered "learning moment" instead of a
 * document header), the quick-facts strip (three small cards instead of one
 * divided row) and the Stroke Order/Audio sections in their own files. No
 * data source, adapter contract, or route changed. StrokeOrderViewer's
 * fetch timing and PronunciationButton's Audio-API implementation are both
 * untouched by this pass — see those files' own docstrings.
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

      {/* HERO — the character is the focal "learning moment", not a
          document header: centered, generous spacing, a whisper of the
          brand blue on the surface itself (existing `primary-light` /
          `primary-dark` tokens only — no new color, no gradient, no
          illustration) instead of the neutral gray Panel used elsewhere.
          Content order (word -> pronunciation -> meaning, badges above) is
          unchanged from before this pass. */}
      <Panel className="flex flex-col items-center gap-4 bg-primary-light/60 p-8 text-center dark:bg-primary-dark/10 sm:p-10">
        <div className="flex flex-wrap items-center justify-center gap-2">
          {word.hskLevels.map((level) => (
            <HskLevelBadge key={level} level={level} href={`/hsk/${level}`} />
          ))}
          {word.partOfSpeech.map((pos) => (
            <Badge key={pos} tone="neutral">
              {pos}
            </Badge>
          ))}
        </div>

        <h1 className="font-cjk text-7xl font-semibold leading-none text-neutral-900 dark:text-night-text sm:text-8xl">
          {word.word}
        </h1>

        <div className="flex items-center gap-3">
          <p className="text-2xl italic text-primary dark:text-night-primary">{word.pinyin}</p>
          <PronunciationButton wordUrl={word.audio.wordUrl} />
        </div>

        <p className="text-lg text-neutral-800 dark:text-night-text">{word.meaningVi}</p>
      </Panel>

      {/* QUICK FACTS — three small, equal-width cards instead of one
          divided strip. `grid-cols-3` (not the old flex+overflow-x-auto
          row) means the three columns always divide the available width
          exactly, so there is no overflow to guard against at any
          viewport. Icons are purely decorative (existing icon set only). */}
      <div className="grid grid-cols-3 gap-2 sm:gap-3">
        <Card className="flex flex-col items-center gap-1 p-3 text-center sm:p-4">
          <PencilIcon className="h-5 w-5 text-primary dark:text-night-primary" />
          <span className="font-data text-lg font-semibold tabular-nums text-neutral-900 dark:text-night-text">
            {word.strokeCount ?? "—"}
          </span>
          <span className="text-xs text-neutral-500 dark:text-night-muted">Số nét</span>
        </Card>
        <Card className="flex flex-col items-center gap-1 p-3 text-center sm:p-4">
          <BookOpenIcon className="h-5 w-5 text-primary dark:text-night-primary" />
          <span className="font-data text-lg font-semibold tabular-nums text-neutral-900 dark:text-night-text">
            {characterCount}
          </span>
          <span className="text-xs text-neutral-500 dark:text-night-muted">Ký tự</span>
        </Card>
        <Card className="flex flex-col items-center gap-1 p-3 text-center sm:p-4">
          <GraduationCapIcon className="h-5 w-5 text-primary dark:text-night-primary" />
          <span className="font-data text-lg font-semibold text-neutral-900 dark:text-night-text">
            {word.hskLevels.join(", ")}
          </span>
          <span className="text-xs text-neutral-500 dark:text-night-muted">Cấp độ</span>
        </Card>
      </div>

      {/* LEARNING TABS — progressive disclosure instead of six stacked
          cards. Panels stay mounted (see Tabs.tsx) so Stroke Order's own
          fetch timing is unchanged from before this redesign. */}
      <Tabs items={tabs} label="Nội dung học tập" />
    </div>
  );
}
