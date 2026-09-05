import Link from "next/link";
import Image from "next/image";
import clsx from "clsx";
import { Card } from "@/components/ui/Card";
import { LinkButton } from "@/components/ui/Button";
import { DictionarySearchTrigger } from "@/components/dictionary/DictionarySearchTrigger";
import { RadicalCard } from "@/components/radicals/RadicalCard";
import {
  GraduationCapIcon,
  SearchIcon,
  TargetIcon,
  ArrowRightIcon,
  BookOpenIcon,
} from "@/components/ui/icons";
import type { HskLevel } from "@/lib/data/types";
import { practiceRoute, PRACTICE_CARDS, PRACTICE_CARD_ACCENT_STYLES } from "@/lib/practice/types";
import { getAllRadicals, getRadicalVocabularyCount } from "@/lib/data/radicalRepository";

const HSK_LEVELS: HskLevel[] = [1, 2, 3, 4, 5, 6];

/** Same "highest vocabularyCount first" selection already used by
 *  DictionaryRadicalSection's teaser (UI-004) — reusing it here means the
 *  Home card shows the same representative radicals a visitor would also
 *  see on /dictionary and /hsk, rather than a third, different sample. */
const HOME_RADICAL_TEASER_COUNT = 6;

const HSK_ACCENT: Record<HskLevel, string> = {
  1: "text-accent-blue",
  2: "text-accent-green",
  3: "text-accent-purple",
  4: "text-accent-orange",
  5: "text-accent-red",
  6: "text-accent-teal",
};

const HERO_FEATURES = [
  {
    icon: GraduationCapIcon,
    title: "Học từ vựng",
    description: "Theo 6 cấp độ HSK",
  },
  {
    icon: SearchIcon,
    title: "Tra từ điển",
    description: "Nhanh chóng, chính xác",
  },
  {
    icon: TargetIcon,
    title: "Luyện tập",
    description: "Ôn tập hiệu quả",
  },
] as const;

export default function HomePage() {
  const radicals = getAllRadicals();
  const radicalVocabularyCounts = Object.fromEntries(
    radicals.map((radical) => [radical.id, getRadicalVocabularyCount(radical.id)])
  );
  const teaserRadicals = [...radicals]
    .sort((a, b) => (radicalVocabularyCounts[b.id] ?? 0) - (radicalVocabularyCounts[a.id] ?? 0))
    .slice(0, HOME_RADICAL_TEASER_COUNT);

  return (
    <div className="flex flex-col gap-8">
      <section className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-center">
        <div className="flex flex-col gap-6">
          <div className="flex flex-col gap-3">
            <h1 className="text-3xl font-bold leading-tight text-neutral-900 dark:text-night-text sm:text-4xl">
              Học từ vựng tiếng Trung
              <br />
              <span className="text-primary">Theo cấp độ HSK</span>
            </h1>
            <p className="max-w-2xl text-neutral-600 dark:text-night-muted">
              Học từ mới, tra cứu dễ dàng và luyện tập mỗi ngày để ghi nhớ lâu hơn.
            </p>
          </div>

          <div className="flex flex-wrap gap-6">
            {HERO_FEATURES.map((feature) => (
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

          <LinkButton href="/hsk" className="w-fit">
            Bắt đầu học
            <ArrowRightIcon className="h-4 w-4" />
          </LinkButton>
        </div>

        <Image
          src="/hero-illustration.png"
          alt=""
          width={1448}
          height={1086}
          priority
          className="mx-auto h-auto w-56 shrink-0 sm:w-72 lg:w-80"
        />
      </section>

      <Card className="flex flex-col gap-4 p-6 sm:p-8">
        <div className="flex flex-col gap-1 text-center">
          <h2 className="flex items-center justify-center gap-2 text-xl font-bold text-neutral-900 dark:text-night-text">
            <GraduationCapIcon className="h-6 w-6 text-primary" />
            Chọn cấp độ HSK để bắt đầu
          </h2>
          <p className="text-sm text-neutral-600 dark:text-night-muted">
            Học từ vựng theo lộ trình từ cơ bản đến nâng cao
          </p>
        </div>
        <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-6">
          {HSK_LEVELS.map((level) => (
            <Link key={level} href={`/hsk/${level}`} className="block min-w-0">
              <Card className="flex flex-col items-center justify-center gap-0.5 py-4 text-center hover:shadow-md">
                <span className="text-xs font-medium text-neutral-500 dark:text-night-muted">
                  HSK
                </span>
                <span className={clsx("text-2xl font-bold", HSK_ACCENT[level])}>{level}</span>
              </Card>
            </Link>
          ))}
        </div>
      </Card>

      <Card className="flex flex-col gap-4 p-6 sm:p-8">
        <div className="flex flex-col gap-1">
          <h2 className="flex items-center gap-2 text-xl font-bold text-neutral-900 dark:text-night-text">
            <SearchIcon className="h-6 w-6 text-primary" />
            Tra từ điển nhanh
          </h2>
          <p className="text-sm text-neutral-600 dark:text-night-muted">
            Nhập chữ Hán để tra cứu từ vựng HSK.
          </p>
        </div>
        <DictionarySearchTrigger placeholder="Nhập chữ Hán, pinyin, bộ thủ ..." />
      </Card>

      <Card className="flex flex-col gap-4 p-6 sm:p-8">
        <div className="flex flex-col gap-1">
          <h2 className="flex items-center gap-2 text-xl font-bold text-neutral-900 dark:text-night-text">
            <BookOpenIcon className="h-6 w-6 text-primary" />
            Bộ thủ chữ Hán
          </h2>
          <p className="text-sm text-neutral-600 dark:text-night-muted">
            Tra cứu 214 bộ thủ Khang Hy và từ vựng HSK liên quan.
          </p>
        </div>
        <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
          {teaserRadicals.map((radical) => (
            <RadicalCard
              key={radical.id}
              radical={radical}
              vocabularyCount={radicalVocabularyCounts[radical.id] ?? 0}
            />
          ))}
        </div>
        <LinkButton href="/radicals" variant="secondary" className="w-fit">
          Xem tất cả 214 bộ thủ
          <ArrowRightIcon className="h-4 w-4" />
        </LinkButton>
      </Card>

      <Card id="luyen-tap" className="flex scroll-mt-20 flex-col gap-4 p-6 sm:p-8">
        <div className="flex flex-col gap-1">
          <h2 className="flex items-center gap-2 text-xl font-bold text-neutral-900 dark:text-night-text">
            <TargetIcon className="h-6 w-6 text-primary" />
            Luyện tập
          </h2>
          <p className="text-sm text-neutral-600 dark:text-night-muted">
            Học từ vựng theo 6 cấp độ HSK từ cơ bản đến nâng cao.
          </p>
        </div>
        <div className="grid gap-3 sm:grid-cols-2">
          {PRACTICE_CARDS.map((card) => {
            const style = PRACTICE_CARD_ACCENT_STYLES[card.accent];
            return (
              <Link key={card.title} href={practiceRoute(card.type)} className="block min-w-0">
                <Card
                  className={clsx("flex items-start gap-3 border-2 hover:shadow-md", style.border)}
                >
                  <span
                    className={clsx(
                      "flex h-10 w-10 shrink-0 items-center justify-center rounded-lg",
                      style.badgeBg,
                      style.icon
                    )}
                  >
                    <card.icon className="h-5 w-5" />
                  </span>
                  <div className="flex min-w-0 flex-col">
                    <span className="text-base font-semibold text-neutral-900 dark:text-night-text">
                      {card.title}
                    </span>
                    <span className="text-sm text-neutral-600 dark:text-night-muted">
                      {card.description}
                    </span>
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
