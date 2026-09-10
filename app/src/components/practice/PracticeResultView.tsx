"use client";

import Image from "next/image";
import Link from "next/link";
import clsx from "clsx";
import { Button } from "@/components/ui/Button";
import { ArrowLeftIcon } from "@/components/ui/icons";
import { PRACTICE_TYPE_INFO, type PracticeType } from "@/lib/practice/types";
import type { HskLevel } from "@/lib/data/types";

/**
 * ONE reusable Result screen for every practice type (meaning / character /
 * flashcard / writing) — rendered by all three flow owners
 * (ChoicePracticeFlow, FlashcardPracticeFlow, WritingPracticeFlow) from
 * their `phase === "result"` branch.
 *
 * Visual-redesign pass (Practice Result): matches the approved reference —
 * the same "Quay lại" + title/subtitle header and `rounded-3xl` /
 * `#E2E8F0` / `shadow-card` panel already established on Practice Config,
 * an illustration per result state, a purple score pill, three pastel
 * statistic cards, and a state-driven CTA stack.
 *
 * Four presentation states, derived PURELY from data the flow already
 * computes — `isCycleComplete` (isLearningCycleComplete(pool, usedIds))
 * and `wrongCount` (this session's wrong answers). No scoring / progress /
 * question logic is touched here; `remainingCount` is just
 * `pool.length - usedIds.size` handed down by each flow owner.
 *
 *   incomplete-perfect : still vocab left, 0 wrong  -> success.png
 *   incomplete-wrong   : still vocab left, wrong>0  -> review.png
 *   complete-perfect   : whole HSK done,   0 wrong  -> complete.png
 *   complete-wrong     : whole HSK done,   wrong>0  -> complete.png
 */

type ResultState =
  | "incomplete-perfect"
  | "incomplete-wrong"
  | "complete-perfect"
  | "complete-wrong";

const ILLUSTRATION: Record<
  ResultState,
  { src: string; width: number; height: number }
> = {
  // natural pixel dimensions per asset -> next/image locks the aspect
  // ratio so the art is never cropped or stretched.
  "incomplete-perfect": { src: "/practice-result-success.png", width: 1254, height: 1254 },
  "incomplete-wrong": { src: "/practice-result-review.png", width: 1536, height: 1024 },
  "complete-perfect": { src: "/practice-result-complete.png", width: 322, height: 181 },
  "complete-wrong": { src: "/practice-result-complete.png", width: 322, height: 181 },
};

type CtaRole = "primary" | "secondary" | "tertiary";

const CTA_BASE =
  "font-ui flex h-[68px] w-full items-center justify-center rounded-[18px] px-4 text-center text-lg font-bold transition-colors sm:h-[72px]";

const CTA_ROLE_CLASSES: Record<CtaRole, string> = {
  primary: "bg-primary text-white hover:bg-primary-dark",
  secondary:
    "border-2 border-primary bg-white text-primary hover:bg-primary-light dark:bg-night-surface dark:hover:bg-primary-dark/20",
  tertiary:
    "border border-neutral-300 bg-white text-neutral-800 hover:bg-neutral-50 dark:border-night-border dark:bg-night-surface dark:text-night-text dark:hover:bg-night-input",
};

interface Cta {
  key: string;
  label: string;
  role: CtaRole;
  onClick?: () => void;
  href?: string;
}

export function PracticeResultView({
  practiceType,
  hskLevel,
  actualCount,
  correctCount,
  wrongCount,
  isCycleComplete,
  remainingCount,
  onReviewWrong,
  onContinue,
  onRestart,
  onBack,
}: {
  practiceType: PracticeType;
  hskLevel: HskLevel;
  actualCount: number;
  correctCount: number;
  wrongCount: number;
  isCycleComplete: boolean;
  /** pool.length - usedIds.size, computed by the flow owner (>= 0). Pure
   *  display — feeds the "Ôn lại từ chưa học (N từ)" label only. */
  remainingCount: number;
  onReviewWrong: () => void;
  onContinue: () => void;
  onRestart: () => void;
  /** Back to the configuration screen — each flow owner passes its own
   *  existing `handleExitSession` (session cleared, phase -> "config"),
   *  unchanged. */
  onBack: () => void;
}) {
  const info = PRACTICE_TYPE_INFO[practiceType];
  const accuracy = actualCount > 0 ? Math.round((correctCount / actualCount) * 100) : 0;
  const isPerfect = wrongCount === 0;

  const state: ResultState = isCycleComplete
    ? isPerfect
      ? "complete-perfect"
      : "complete-wrong"
    : isPerfect
      ? "incomplete-perfect"
      : "incomplete-wrong";

  const illustration = ILLUSTRATION[state];

  const mainTitle = isCycleComplete ? `Hoàn thành HSK ${hskLevel}!` : "Tuyệt vời";
  const subtitle = isCycleComplete
    ? `Bạn đã học hết toàn bộ từ vựng HSK ${hskLevel}`
    : "Bạn đã hoàn thành bài tập luyện tập";
  const helper = state === "complete-wrong" ? "Hãy ôn lại các từ vựng bạn còn sai nhé!" : null;

  const homeCta = (role: CtaRole): Cta => ({
    key: "home",
    label: "Về trang chủ",
    role,
    href: "/",
  });

  let ctas: Cta[];
  switch (state) {
    case "incomplete-perfect":
      ctas = [
        ...(remainingCount > 0
          ? [
              {
                key: "review-unlearned",
                label: `Ôn lại từ chưa học (${remainingCount} từ)`,
                role: "primary" as const,
                onClick: onContinue,
              },
              { key: "continue", label: "Luyện tập tiếp", role: "secondary" as const, onClick: onContinue },
            ]
          : [{ key: "continue", label: "Luyện tập tiếp", role: "primary" as const, onClick: onContinue }]),
        homeCta("tertiary"),
      ];
      break;
    case "incomplete-wrong":
      ctas = [
        { key: "review-wrong", label: `Ôn lại ${wrongCount} câu sai`, role: "primary", onClick: onReviewWrong },
        { key: "continue", label: "Luyện tập tiếp", role: "secondary", onClick: onContinue },
        homeCta("tertiary"),
      ];
      break;
    case "complete-perfect":
      ctas = [
        { key: "restart", label: "Luyện tập tiếp", role: "primary", onClick: onRestart },
        homeCta("secondary"),
      ];
      break;
    case "complete-wrong":
      ctas = [
        { key: "review-wrong", label: `Ôn lại ${wrongCount} câu sai`, role: "primary", onClick: onReviewWrong },
        { key: "restart", label: "Luyện tập tiếp", role: "secondary", onClick: onRestart },
        homeCta("tertiary"),
      ];
      break;
  }

  return (
    <div className="mx-auto flex w-full max-w-[1180px] flex-col gap-8">
      {/* Same standardized "Quay lại" as Practice Config / the detail
          screens — `variant="neutral"` outline + `font-ui h-12 rounded-xl
          px-6`. Back goes to the configuration screen via the flow's own
          existing `handleExitSession`; navigation behavior is untouched. */}
      <Button
        type="button"
        variant="neutral"
        onClick={onBack}
        className="font-ui h-12 w-fit rounded-xl px-6"
      >
        <ArrowLeftIcon className="h-4 w-4" />
        Quay lại
      </Button>

      <div className="flex flex-col gap-1">
        <h1 className="font-ui text-3xl font-bold text-primary dark:text-night-primary sm:text-4xl">
          {info.title}
        </h1>
        <p className="font-ui text-neutral-600 dark:text-night-muted">{info.description}</p>
      </div>

      <div className="flex w-full flex-col items-center gap-6 rounded-3xl border border-[#E2E8F0] bg-white p-6 text-center shadow-card dark:border-night-border dark:bg-night-surface sm:gap-8 sm:p-10 md:p-12">
        <h2 className="font-ui text-2xl font-bold text-primary dark:text-night-primary sm:text-[26px]">
          Kết quả luyện tập
        </h2>

        <Image
          src={illustration.src}
          alt=""
          width={illustration.width}
          height={illustration.height}
          sizes="(min-width: 1024px) 340px, (min-width: 640px) 320px, 240px"
          className="h-auto w-full max-w-[240px] object-contain sm:max-w-[320px] lg:max-w-[340px]"
          priority={false}
        />

        <div className="flex flex-col gap-2">
          <p className="font-ui text-[26px] font-bold leading-tight text-primary dark:text-night-primary sm:text-4xl">
            {mainTitle}
          </p>
          <p className="font-ui text-base text-neutral-700 dark:text-night-muted sm:text-lg">
            {subtitle}
          </p>
          {helper && (
            <p className="font-ui text-base text-neutral-700 dark:text-night-muted sm:text-lg">
              {helper}
            </p>
          )}
        </div>

        <span className="font-ui inline-flex items-center rounded-full bg-[#F3E9FF] px-6 py-2 text-xl font-bold text-accent-purple dark:bg-accent-purple/20 sm:text-2xl">
          {correctCount}/{actualCount} câu
        </span>

        <div className="grid w-full grid-cols-3 gap-3 sm:gap-4">
          <div className="flex flex-col items-center gap-1 rounded-2xl bg-success-bg px-2 py-4 dark:bg-success/10 sm:py-5">
            <span className="font-ui text-[13px] font-medium leading-tight text-success sm:text-base">
              Đúng
            </span>
            <span className="font-ui text-2xl font-bold text-success sm:text-3xl">{correctCount}</span>
          </div>
          <div className="flex flex-col items-center gap-1 rounded-2xl bg-error-bg px-2 py-4 dark:bg-error/10 sm:py-5">
            <span className="font-ui text-[13px] font-medium leading-tight text-error sm:text-base">
              Sai
            </span>
            <span className="font-ui text-2xl font-bold text-error sm:text-3xl">{wrongCount}</span>
          </div>
          <div className="flex flex-col items-center gap-1 rounded-2xl bg-primary-tint px-2 py-4 dark:bg-primary-dark/20 sm:py-5">
            <span className="font-ui text-[13px] font-medium leading-tight text-primary dark:text-night-primary sm:text-base">
              Độ chính xác
            </span>
            <span className="font-ui text-2xl font-bold text-primary dark:text-night-primary sm:text-3xl">
              {accuracy}%
            </span>
          </div>
        </div>

        <div className="flex w-full flex-col gap-3">
          {ctas.map((cta) =>
            cta.href ? (
              <Link
                key={cta.key}
                href={cta.href}
                className={clsx(CTA_BASE, CTA_ROLE_CLASSES[cta.role])}
              >
                {cta.label}
              </Link>
            ) : (
              <button
                key={cta.key}
                type="button"
                onClick={cta.onClick}
                className={clsx(CTA_BASE, CTA_ROLE_CLASSES[cta.role])}
              >
                {cta.label}
              </button>
            )
          )}
        </div>
      </div>
    </div>
  );
}
