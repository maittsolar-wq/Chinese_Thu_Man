import Link from "next/link";
import type { VocabularyWord } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { HskLevelBadge } from "@/components/ui/Badge";

/**
 * Phase 06 audit: Home, HSK, and Vocabulary Detail have each moved to their
 * own dedicated result/preview component in earlier redesign phases
 * (HskVocabularyRow, Home's inline preview cards, ...) — this component's
 * only remaining consumers are /dictionary and DictionarySearchPopup
 * (verified directly, not assumed), so it is safe to redesign here without
 * affecting any already-approved screen.
 *
 * Search Results visual-fix pass: pinyin/meaning now carry `font-ui`
 * explicitly (Be Vietnam Pro is opt-in, not the Tailwind default `sans`,
 * so without it they fell back to the system font) — the Chinese word
 * already had `font-cjk`. The HSK badge now opts into `colored` (per-level
 * brand color instead of the flat blue every other badge caller keeps).
 */
export function VocabularyCard({
  word,
  href,
  showAllLevels = false,
  currentLevel,
  onClick,
}: {
  word: VocabularyWord;
  href: string;
  /** Show every HSK level the word belongs to, not just the first. */
  showAllLevels?: boolean;
  /**
   * The HSK level of the page this card is rendered on (e.g. /hsk/6).
   * When set and the word belongs to that level, it is shown as the single
   * badge instead of defaulting to hskLevels[0] — a word that belongs to
   * multiple levels must show the level the user is actually browsing.
   * Ignored when showAllLevels is true.
   */
  currentLevel?: number;
  /**
   * Optional handler fired when the card itself is activated (click or
   * keyboard Enter/Space on the underlying link) — e.g. DictionarySearchPopup
   * closing itself on navigation. Attached directly to the link rather than
   * a wrapping div, so it fires identically for mouse and keyboard use.
   */
  onClick?: () => void;
}) {
  const primaryLevel =
    currentLevel !== undefined && word.hskLevels.some((l) => l === currentLevel)
      ? currentLevel
      : word.hskLevels[0];

  const levels = showAllLevels
    ? word.hskLevels
    : primaryLevel !== undefined
      ? [primaryLevel]
      : [];

  return (
    <Link href={href} onClick={onClick} className="group block min-w-0">
      <Card className="flex items-start justify-between gap-3 transition-shadow hover:shadow-md">
        <div className="min-w-0">
          <p className="font-cjk text-2xl font-semibold text-neutral-900 dark:text-night-text">
            {word.word}
          </p>
          <p className="font-ui text-sm italic text-primary dark:text-night-primary">{word.pinyin}</p>
          <p className="font-ui mt-1 truncate text-sm text-neutral-800 dark:text-night-text">{word.meaningVi}</p>
        </div>
        <div className="flex shrink-0 flex-wrap justify-end gap-1">
          {levels.map((level) => (
            <HskLevelBadge key={level} level={level} colored />
          ))}
        </div>
      </Card>
    </Link>
  );
}
