import type { Metadata } from "next";
import Link from "next/link";
import clsx from "clsx";
import { Card, Panel } from "@/components/ui/Card";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { BookOpenIcon, CardsIcon, TargetIcon, RadicalIcon, ArrowRightIcon } from "@/components/ui/icons";
import { getVocabularyCountByLevel } from "@/lib/data/vocabularyRepository";
import { HSK_LEVEL_INFO } from "@/lib/hsk/hskLevelInfo";
import { HSK_LEVEL_ACCENT_TEXT, HSK_LEVEL_ACCENT_BG } from "@/lib/hsk/hskLevelAccent";
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
 * Phase 03 redesign. The full 214-radical teaser grid this page used to
 * embed (DictionaryRadicalSection, still used unchanged by /dictionary
 * itself — that file is untouched) is replaced by one compact contextual
 * link: radicals are reachable from a character inside Vocabulary Detail's
 * own "Bộ thủ & chữ Hán" tab, or directly via /radicals — this page no
 * longer duplicates a second radical browser.
 */
export default function HskOverviewPage() {
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
            <Link key={level} href={`/hsk/${level}`} className="group block">
              <Card className="flex flex-col gap-2 hover:shadow-md">
                <div className="flex items-center justify-between">
                  <span
                    className={clsx(
                      "flex h-10 w-10 items-center justify-center rounded-lg text-base font-bold text-white",
                      HSK_LEVEL_ACCENT_BG[level]
                    )}
                  >
                    {level}
                  </span>
                  <ArrowRightIcon className="h-4 w-4 shrink-0 text-neutral-400 transition-colors group-hover:text-primary dark:text-night-muted" />
                </div>
                <h2 className="text-xl font-semibold text-neutral-900 dark:text-night-text">
                  HSK {level}
                </h2>
                <p className={clsx("text-sm font-medium", HSK_LEVEL_ACCENT_TEXT[level])}>
                  {info.name}
                </p>
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

      <Panel className="flex flex-col items-start gap-3 p-6 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-start gap-3">
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary-light text-primary dark:bg-primary-dark/40 dark:text-night-primary">
            <RadicalIcon className="h-5 w-5" />
          </span>
          <div className="flex flex-col gap-0.5">
            <p className="text-sm font-semibold text-neutral-900 dark:text-night-text">
              Bộ thủ chữ Hán
            </p>
            <p className="text-sm text-neutral-600 dark:text-night-muted">
              Mỗi từ vựng trong Chi tiết từ vựng đều hiển thị bộ thủ liên quan, giúp bạn hiểu cấu tạo chữ Hán.
            </p>
          </div>
        </div>
        <Link
          href="/radicals"
          className="inline-flex shrink-0 items-center gap-1.5 text-sm font-semibold text-primary hover:underline dark:text-night-primary"
        >
          Tra cứu bộ thủ
          <ArrowRightIcon className="h-4 w-4" />
        </Link>
      </Panel>
    </div>
  );
}
