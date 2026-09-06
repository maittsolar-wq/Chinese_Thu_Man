import Link from "next/link";
import Image from "next/image";
import clsx from "clsx";
import { Card, Panel } from "@/components/ui/Card";
import { LinkButton } from "@/components/ui/Button";
import { DictionarySearchTrigger } from "@/components/dictionary/DictionarySearchTrigger";
import {
  RadicalIcon,
  TargetIcon,
  ArrowRightIcon,
} from "@/components/ui/icons";
import type { HskLevel } from "@/lib/data/types";
import { getVocabularyByLevel } from "@/lib/data/vocabularyRepository";
import { HSK_LEVEL_INFO } from "@/lib/hsk/hskLevelInfo";
import { HSK_LEVEL_ACCENT_BG } from "@/lib/hsk/hskLevelAccent";

const HSK_LEVELS: HskLevel[] = [1, 2, 3, 4, 5, 6];

/** A small, real, deterministic slice of HSK 1 for the "Khám phá từ vựng"
 *  preview — the first 6 records of the level's own production order, not
 *  a curated hand-picked list and not client-side randomness (which would
 *  make this statically-generated page render differently per build/request
 *  for no benefit). Real vocabulary, per the brief's own requirement. */
const VOCABULARY_PREVIEW_COUNT = 6;

/**
 * Home (Phase 04 redesign). Previously five equally-weighted, full-width
 * feature cards (Hero, HSK grid, Dictionary search, a 6-radical teaser
 * grid, a 4-card Practice grid) — a feature catalog, not an entry point.
 * Redesigned around one descending priority order: Hero -> HSK (the
 * primary learning path) -> a small real-vocabulary preview -> two
 * intentionally minor secondary panels (Radicals, Practice) sharing one
 * row so neither competes with HSK/Vocabulary above them.
 */
export default function HomePage() {
  const previewWords = getVocabularyByLevel(1).slice(0, VOCABULARY_PREVIEW_COUNT);

  return (
    <div className="flex flex-col gap-10">
      {/* HERO — identity, value, one clear next step. No feature-icon row
          duplicating what the sections below already show for real. */}
      <section className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-center">
        <div className="flex flex-col gap-5">
          <div className="flex flex-col gap-3">
            <h1 className="text-3xl font-bold leading-tight text-neutral-900 dark:text-night-text sm:text-4xl">
              Học chữ Hán một cách
              <br />
              <span className="text-primary dark:text-night-primary">có hệ thống</span>
            </h1>
            <p className="max-w-xl text-neutral-600 dark:text-night-muted">
              Từ vựng chuẩn HSK, tra cứu tức thì, thứ tự nét và bộ thủ đi kèm mỗi
              chữ Hán — dành riêng cho người Việt học tiếng Trung.
            </p>
          </div>

          <div className="flex flex-wrap gap-3">
            <LinkButton href="/hsk">
              Bắt đầu với HSK
              <ArrowRightIcon className="h-4 w-4" />
            </LinkButton>
            <DictionarySearchTrigger label="Tra từ điển" />
          </div>
        </div>

        <Image
          src="/hero-illustration.png"
          alt=""
          width={1448}
          height={1086}
          priority
          className="mx-auto h-auto w-48 shrink-0 sm:w-64 lg:w-72"
        />
      </section>

      {/* HSK — the primary learning path. A concise preview, not a copy of
          /hsk's own page: level number + name only, no description/count. */}
      <section className="flex flex-col gap-4">
        <div className="flex items-baseline justify-between gap-4">
          <div className="flex flex-col gap-1">
            <h2 className="text-xl font-bold text-neutral-900 dark:text-night-text">
              Chọn cấp độ để bắt đầu
            </h2>
            <p className="text-sm text-neutral-600 dark:text-night-muted">
              6 cấp độ HSK, từ cơ bản đến nâng cao.
            </p>
          </div>
          <Link
            href="/hsk"
            className="hidden shrink-0 items-center gap-1.5 text-sm font-semibold text-primary hover:underline dark:text-night-primary sm:inline-flex"
          >
            Xem tất cả
            <ArrowRightIcon className="h-4 w-4" />
          </Link>
        </div>

        <Panel className="grid grid-cols-3 gap-2 p-3 sm:grid-cols-6">
          {HSK_LEVELS.map((level) => (
            <Link
              key={level}
              href={`/hsk/${level}`}
              className="flex flex-col items-center gap-1.5 rounded-md px-2 py-3 text-center transition-colors hover:bg-white dark:hover:bg-night-surface"
            >
              <span
                className={clsx(
                  "flex h-9 w-9 items-center justify-center rounded-lg text-sm font-bold text-white",
                  HSK_LEVEL_ACCENT_BG[level]
                )}
              >
                {level}
              </span>
              <span className="text-xs font-medium text-neutral-700 dark:text-night-text">
                HSK {level}
              </span>
              <span className="text-[11px] text-neutral-500 dark:text-night-muted">
                {HSK_LEVEL_INFO[level].name}
              </span>
            </Link>
          ))}
        </Panel>

        <Link
          href="/hsk"
          className="inline-flex items-center gap-1.5 text-sm font-semibold text-primary hover:underline dark:text-night-primary sm:hidden"
        >
          Xem tất cả cấp độ HSK
          <ArrowRightIcon className="h-4 w-4" />
        </Link>
      </section>

      {/* VOCABULARY DISCOVERY — real production words, not mock content.
          Each links straight into the (Phase 02) redesigned Vocabulary
          Detail. Kept small and lightweight, one level below HSK. */}
      <section className="flex flex-col gap-4">
        <div className="flex flex-col gap-1">
          <h2 className="text-xl font-bold text-neutral-900 dark:text-night-text">
            Khám phá từ vựng
          </h2>
          <p className="text-sm text-neutral-600 dark:text-night-muted">
            Một vài từ vựng HSK 1 để bạn bắt đầu.
          </p>
        </div>

        <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-6">
          {previewWords.map((word) => (
            <Link key={word.id} href={`/vocabulary/${word.id}`} className="block min-w-0">
              <Card className="flex flex-col gap-0.5 text-center hover:shadow-md">
                <p className="font-cjk text-3xl font-semibold text-neutral-900 dark:text-night-text">
                  {word.word}
                </p>
                <p className="text-xs italic text-primary dark:text-night-primary">{word.pinyin}</p>
                <p className="truncate text-xs text-neutral-600 dark:text-night-muted">
                  {word.meaningVi}
                </p>
              </Card>
            </Link>
          ))}
        </div>
      </section>

      {/* SECONDARY TOOLS — Radicals and Practice share one row, both
          intentionally minor: neither is a primary Home destination. */}
      <section className="grid gap-3 sm:grid-cols-2">
        <Panel className="flex items-center gap-3 p-5">
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary-light text-primary dark:bg-primary-dark/40 dark:text-night-primary">
            <RadicalIcon className="h-5 w-5" />
          </span>
          <div className="flex min-w-0 flex-col gap-0.5">
            <p className="text-sm font-semibold text-neutral-900 dark:text-night-text">Bộ thủ chữ Hán</p>
            <p className="text-sm text-neutral-600 dark:text-night-muted">
              Bộ thủ giúp bạn hiểu cấu tạo chữ Hán.
            </p>
            <Link
              href="/radicals"
              className="mt-1 inline-flex w-fit items-center gap-1 text-sm font-semibold text-primary hover:underline dark:text-night-primary"
            >
              Tra cứu bộ thủ
              <ArrowRightIcon className="h-3.5 w-3.5" />
            </Link>
          </div>
        </Panel>

        <Panel className="flex items-center gap-3 p-5">
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary-light text-primary dark:bg-primary-dark/40 dark:text-night-primary">
            <TargetIcon className="h-5 w-5" />
          </span>
          <div className="flex min-w-0 flex-col gap-0.5">
            <p className="text-sm font-semibold text-neutral-900 dark:text-night-text">Luyện tập</p>
            <p className="text-sm text-neutral-600 dark:text-night-muted">
              Ôn lại từ vựng đã học bằng flashcard, trắc nghiệm và luyện viết.
            </p>
            <Link
              href="/practice"
              className="mt-1 inline-flex w-fit items-center gap-1 text-sm font-semibold text-primary hover:underline dark:text-night-primary"
            >
              Đến trang luyện tập
              <ArrowRightIcon className="h-3.5 w-3.5" />
            </Link>
          </div>
        </Panel>
      </section>
    </div>
  );
}
