import Link from "next/link";
import type { VocabularyWord } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { HskLevelBadge } from "@/components/ui/Badge";

export function VocabularyCard({
  word,
  href,
  showAllLevels = false,
}: {
  word: VocabularyWord;
  href: string;
  /** Show every HSK level the word belongs to, not just the first. */
  showAllLevels?: boolean;
}) {
  const levels = showAllLevels ? word.hskLevels : word.hskLevels.slice(0, 1);

  return (
    <Link href={href} className="block">
      <Card className="flex items-start justify-between gap-3 transition-shadow hover:shadow-md">
        <div className="min-w-0">
          <p className="text-2xl font-bold text-neutral-900">{word.word}</p>
          <p className="text-sm text-neutral-600">{word.pinyin}</p>
          <p className="mt-1 truncate text-sm text-neutral-800">{word.meaningVi}</p>
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
