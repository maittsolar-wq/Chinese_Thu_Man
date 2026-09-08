import Link from "next/link";
import type { VocabularyWord } from "@/lib/data/types";
import { HskLevelBadge } from "@/components/ui/Badge";
import { ChevronRightIcon } from "@/components/ui/icons";

/**
 * Compact vocabulary row for the HSK level listing (Phase 03) — a
 * dedicated component, NOT a restyle of the shared `VocabularyCard`
 * (Dictionary's popup and full-page results also render that component,
 * and standalone Search/Dictionary is out of scope for this phase, so it
 * stays byte-for-byte untouched).
 *
 * Deliberately a flat row (separated by the parent list's `divide-y`, no
 * per-item card shadow/border box) rather than a bordered card: an HSK
 * level can hold up to 1800 words
 * paginated 50 at a time, where a wall of shadowed cards reads as
 * "database browser." A single-column list of rows — same density
 * reasoning as a dictionary index — keeps the Chinese word dominant while
 * staying scannable at that volume. Vocabulary Detail (one word) rightly
 * keeps its own spacious hero treatment; this is the opposite end of the
 * same design language, not an inconsistency.
 */
export function HskVocabularyRow({
  word,
  href,
  currentLevel,
}: {
  word: VocabularyWord;
  href: string;
  /** The HSK level of the page this row is rendered on — shown as the
   *  single badge when the word belongs to it, matching VocabularyCard's
   *  own `currentLevel` contract so a word appearing on multiple levels
   *  still shows the level actually being browsed. */
  currentLevel: number;
}) {
  const primaryLevel = word.hskLevels.some((level) => level === currentLevel)
    ? currentLevel
    : word.hskLevels[0];

  return (
    <Link
      href={href}
      className="group flex items-center justify-between gap-3 py-3.5 transition-colors hover:bg-neutral-50 focus-visible:bg-neutral-50 focus-visible:outline-none dark:hover:bg-night-input dark:focus-visible:bg-night-input"
    >
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-baseline gap-x-3 gap-y-0.5">
          <span className="font-cjk text-2xl font-semibold text-neutral-900 dark:text-night-text sm:text-3xl">
            {word.word}
          </span>
          <span className="font-ui text-sm italic text-primary dark:text-night-primary">{word.pinyin}</span>
        </div>
        <p className="font-ui mt-0.5 truncate text-sm text-neutral-600 dark:text-night-muted">
          {word.meaningVi}
        </p>
      </div>

      <div className="flex shrink-0 items-center gap-2">
        {/* Navigation-completion pass (HSK flow): `colored` opts into the
            per-level HSK_LEVEL_HEX brand colors (frozen contract from the
            Search Popup pass — HskLevelBadge's own `colored` prop,
            unchanged) instead of the flat blue every level previously
            showed here. */}
        {primaryLevel !== undefined && <HskLevelBadge level={primaryLevel} colored />}
        <ChevronRightIcon className="h-4 w-4 text-neutral-400 transition-colors group-hover:text-primary dark:text-night-muted" />
      </div>
    </Link>
  );
}
