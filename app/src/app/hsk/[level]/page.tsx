import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { LinkButton } from "@/components/ui/Button";
import { ArrowLeftIcon } from "@/components/ui/icons";
import { HskLevelVocabularyList } from "@/components/hsk/HskLevelVocabularyList";
import { getVocabularyByLevel } from "@/lib/data/vocabularyRepository";
import { HSK_LEVEL_INFO } from "@/lib/hsk/hskLevelInfo";
import type { HskLevel } from "@/lib/data/types";

const VALID_LEVELS = [1, 2, 3, 4, 5, 6];

function parseLevel(param: string): HskLevel | null {
  const value = Number(param);
  return VALID_LEVELS.includes(value) ? (value as HskLevel) : null;
}

export function generateStaticParams() {
  return VALID_LEVELS.map((level) => ({ level: String(level) }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ level: string }>;
}): Promise<Metadata> {
  const { level: levelParam } = await params;
  const level = parseLevel(levelParam);
  return { title: level ? `HSK ${level} — Chinese Thu Man` : "HSK — Chinese Thu Man" };
}

/**
 * Search here is live/client-side (HskLevelVocabularyList), scoped to
 * this level's own pool — no `?q=` searchParams anymore, no submit form.
 * `key={level}` on the client component forces a fresh mount (query
 * cleared, page reset to 1) whenever the level itself changes.
 */
export default async function HskLevelPage({
  params,
}: {
  params: Promise<{ level: string }>;
}) {
  const { level: levelParam } = await params;
  const level = parseLevel(levelParam);
  if (!level) notFound();

  const words = getVocabularyByLevel(level);
  const info = HSK_LEVEL_INFO[level];

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb
        items={[
          { label: "Trang chủ", href: "/" },
          { label: "HSK", href: "/hsk" },
          { label: `HSK ${level}` },
        ]}
      />

      <LinkButton href="/hsk" variant="neutral" className="w-fit">
        <ArrowLeftIcon className="h-4 w-4" />
        Quay lại
      </LinkButton>

      <div className="flex flex-col gap-1">
        <h1 className="text-2xl font-bold text-primary">HSK {level}</h1>
        <p className="text-sm text-neutral-600 dark:text-night-muted">
          Danh sách từ vựng HSK {level} - {info.description}
        </p>
      </div>

      <HskLevelVocabularyList key={level} words={words} level={level} />
    </div>
  );
}
