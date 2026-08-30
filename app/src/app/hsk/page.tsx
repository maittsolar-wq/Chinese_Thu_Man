import type { Metadata } from "next";
import Link from "next/link";
import { Card } from "@/components/ui/Card";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { DictionaryRadicalSection } from "@/components/dictionary/DictionaryRadicalSection";
import { BookOpenIcon, CardsIcon, TargetIcon } from "@/components/ui/icons";
import { getVocabularyCountByLevel } from "@/lib/data/vocabularyRepository";
import { getAllRadicals, getRadicalVocabularyCount } from "@/lib/data/radicalRepository";
import { HSK_LEVEL_INFO } from "@/lib/hsk/hskLevelInfo";
import type { HskLevel } from "@/lib/data/types";

export const metadata: Metadata = { title: "HSK — Chinese Thu Man" };

const HSK_LEVELS: HskLevel[] = [1, 2, 3, 4, 5, 6];

/**
 * Matches the approved HSK Main reference's 3 highlight items exactly —
 * same icon+title+subtext pattern already established by Home's Hero
 * (HERO_FEATURES in app/src/app/page.tsx), reusing existing icons rather
 * than adding new ones.
 */
const HSK_FEATURES = [
  { icon: BookOpenIcon, title: "Chuẩn HSK", description: "Theo tiêu chuẩn chính thức" },
  { icon: CardsIcon, title: "Đầy đủ từ vựng", description: "Tổng hợp toàn bộ từ vựng HSK 1 - HSK 6" },
  { icon: TargetIcon, title: "Học hiệu quả", description: "Học, ôn tập và ghi nhớ khoa học" },
] as const;

/**
 * The Bộ thủ (214) section here is the EXACT same DictionaryRadicalSection
 * component already shipped on /dictionary — a second entry point to the
 * same shared radical repository/search, not a second implementation.
 * /dictionary and its own radical section are untouched by this file.
 */
export default function HskOverviewPage() {
  const radicals = getAllRadicals();
  const radicalVocabularyCounts = Object.fromEntries(
    radicals.map((radical) => [radical.id, getRadicalVocabularyCount(radical.id)])
  );

  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-col gap-6">
        <Breadcrumb items={[{ label: "Trang chủ", href: "/" }, { label: "HSK" }]} />

        <div className="flex flex-col gap-1">
          <h1 className="text-2xl font-bold text-primary">HSK</h1>
          <p className="text-sm text-neutral-600 dark:text-night-muted">
            Học từ vựng theo 6 cấp độ HSK từ cơ bản đến nâng cao.
          </p>
        </div>

        <div className="flex flex-wrap gap-6">
          {HSK_FEATURES.map((feature) => (
            <div key={feature.title} className="flex items-center gap-3">
              <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary-light text-primary dark:bg-primary-dark/40 dark:text-white">
                <feature.icon className="h-5 w-5" />
              </span>
              <div className="flex flex-col">
                <span className="text-sm font-semibold text-neutral-900 dark:text-night-text">
                  {feature.title}
                </span>
                <span className="text-xs text-neutral-600 dark:text-night-muted">
                  {feature.description}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {HSK_LEVELS.map((level) => {
          const info = HSK_LEVEL_INFO[level];
          return (
            <Link key={level} href={`/hsk/${level}`} className="block">
              <Card className="flex flex-col gap-1 hover:shadow-md">
                <h2 className="text-xl font-semibold text-neutral-900 dark:text-night-text">
                  HSK {level}
                </h2>
                <p className="text-sm font-medium text-primary">{info.name}</p>
                <p className="text-sm text-neutral-600 dark:text-night-muted">
                  {info.description}
                </p>
                <p className="text-xs text-neutral-500 dark:text-night-muted">
                  {getVocabularyCountByLevel(level).toLocaleString("vi-VN")} từ vựng
                </p>
              </Card>
            </Link>
          );
        })}
      </div>

      <DictionaryRadicalSection
        radicals={radicals}
        vocabularyCounts={radicalVocabularyCounts}
        radicalHrefSuffix="?from=hsk"
      />
    </div>
  );
}
