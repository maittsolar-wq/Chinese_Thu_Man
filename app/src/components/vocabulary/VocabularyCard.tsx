import Link from "next/link";
import type { VocabularyWord } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { HskLevelBadge } from "@/components/ui/Badge";

export function VocabularyCard({
  word,
  href,
  showAllLevels = false,
  currentLevel,
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
    <Link href={href} className="block min-w-0">
      <Card className="flex items-start justify-between gap-3 transition-shadow hover:shadow-md">
        <div className="min-w-0">
          <p className="text-2xl font-bold text-neutral-900 dark:text-night-text">{word.word}</p>
          <p className="text-sm text-neutral-600 dark:text-night-muted">{word.pinyin}</p>
          <p className="mt-1 truncate text-sm text-neutral-800 dark:text-night-text">{word.meaningVi}</p>
        </div>
        <div className="flex shrink-0 flex-wrap justify-end gap-1">
          {levels.map((level) => (
            <HskLevelBadge key={level} level={level} />
          ))}
        </div>
      </Card>
    </Link>
  );
}
