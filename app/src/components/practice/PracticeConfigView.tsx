"use client";

import { useState } from "react";
import { useSearchParams } from "next/navigation";
import { LinkButton } from "@/components/ui/Button";
import { ArrowLeftIcon, BarChartIcon, BookOpenIcon } from "@/components/ui/icons";
import { HskSelector } from "./HskSelector";
import { WordCountSelector } from "./WordCountSelector";
import {
  PRACTICE_TYPE_INFO,
  DEFAULT_PRACTICE_CONFIG,
  type PracticeType,
  type PracticeConfigState,
} from "@/lib/practice/types";

/**
 * Source-aware "Quay lại" — §3/§4 of the navigation-fix pass. The card
 * links that lead here (Home's own Practice section, and this page's own
 * /practice landing) append `?from=home` / `?from=practice` respectively;
 * this reads that back and maps it to the one matching internal route.
 * Anything else (missing, mistyped, or some other value) falls back to
 * `/` — the exact previous hardcoded behavior for direct/bookmarked
 * visits, so that entry point is unchanged. The param is only ever
 * compared against known literals, never interpolated into a URL, so an
 * arbitrary `?from=` value can't produce an arbitrary redirect target.
 */
function useConfigBackHref(): string {
  const searchParams = useSearchParams();
  const from = searchParams.get("from");
  if (from === "practice") return "/practice";
  return "/";
}

/**
 * Shared Practice Configuration screen for all four exercise types — one
 * implementation rendering whichever type/content is passed in, per
 * docs/PRACTICE §2 ("Configuration — shared by all four exercise types").
 *
 * It holds hskLevel/wordCount as local state, matching the defaults shown
 * in every supplied reference screenshot (HSK 2 / 20). When `onStart` is
 * provided, "Bắt đầu luyện tập" calls it with the current selection —
 * used by the Chọn nghĩa flow (Phase D2). Practice types whose exercise
 * screen isn't implemented yet omit `onStart`, leaving the button inert
 * exactly as before (Phase D1) rather than faking a destination.
 */
export function PracticeConfigView({
  practiceType,
  onStart,
}: {
  practiceType: PracticeType;
  onStart?: (config: PracticeConfigState) => void;
}) {
  const info = PRACTICE_TYPE_INFO[practiceType];
  const Icon = info.icon;
  const [config, setConfig] = useState<PracticeConfigState>(DEFAULT_PRACTICE_CONFIG);
  const backHref = useConfigBackHref();

  return (
    <div className="mx-auto flex w-full max-w-[1180px] flex-col gap-8">
      {/* Visual-redesign pass: matches the same source-aware "Quay lại"
          treatment already established on Vocabulary Detail / Radical
          Detail / HSK Detail (`variant="neutral"` — outlined, white/
          transparent, neutral border, no solid-blue fill) instead of this
          screen's own previous one-off translucent-blue-fill style.
          `useConfigBackHref`'s logic/target is untouched — only the
          button's own classes changed. */}
      <LinkButton href={backHref} variant="neutral" className="font-ui h-12 w-fit rounded-xl px-6">
        <ArrowLeftIcon className="h-4 w-4" />
        Quay lại
      </LinkButton>

      <div className="flex flex-col gap-1">
        <h1 className="font-ui text-3xl font-bold text-primary dark:text-night-primary sm:text-4xl">
          {info.title}
        </h1>
        <p className="font-ui text-neutral-600 dark:text-night-muted">{info.description}</p>
      </div>

      {/* Visual-redesign pass: a large, airy "learning configuration
          panel" (per the approved mockup) rather than a small form card —
          a raw styled div (not the shared `<Card>`) so the exact mockup
          border color (#E2E8F0) and radius (24px = stock `rounded-3xl`)
          apply directly with no specificity fight against `<Card>`'s own
          default `border-neutral-200`. `shadow-card` (already the
          lightest shadow token in the system) is reused as-is for the
          "shadow rất nhẹ" requirement — no new shadow invented. */}
      <div className="flex w-full flex-col gap-8 rounded-3xl border border-[#E2E8F0] bg-white p-6 shadow-card dark:border-night-border dark:bg-night-surface sm:gap-9 sm:p-10 md:p-12 lg:p-16">
        <div className="flex flex-col items-center gap-3 text-center">
          <span className="flex h-20 w-20 items-center justify-center rounded-full bg-primary-light dark:bg-primary-dark/30">
            <Icon className="h-9 w-9 text-primary dark:text-night-primary" />
          </span>
          <h2 className="font-ui text-2xl font-bold text-primary dark:text-night-primary sm:text-[32px]">
            Cấu hình luyện tập
          </h2>
        </div>

        <div className="flex flex-col gap-3">
          <span className="font-ui flex items-center gap-2 text-xl font-semibold text-neutral-900 dark:text-night-text">
            <BookOpenIcon className="h-7 w-7 shrink-0 text-accent-red" />
            Phạm vi luyện tập
          </span>
          <HskSelector
            value={config.hskLevel}
            onChange={(hskLevel) => setConfig((prev) => ({ ...prev, hskLevel }))}
          />
          {/* §8: helper text restating the active selection — pure display,
              derived from the same `config.hskLevel` state already held
              above, no new state/logic. */}
          <p className="font-ui mt-1 text-base text-neutral-500 dark:text-night-muted">
            Luyện tập theo danh sách từ vựng HSK {config.hskLevel}
          </p>
        </div>

        <div className="flex flex-col gap-3">
          <span className="font-ui flex items-center gap-2 text-xl font-semibold text-neutral-900 dark:text-night-text">
            <BarChartIcon className="h-7 w-7 shrink-0 text-primary dark:text-night-primary" />
            Số lượng từ
          </span>
          <WordCountSelector
            value={config.wordCount}
            onChange={(wordCount) => setConfig((prev) => ({ ...prev, wordCount }))}
          />
        </div>

        {/* Not the shared `<Button>` here — measured its `BASE_CLASSES`
            (`rounded-md text-sm font-semibold`) reliably beating this
            button's own override classes for exactly these 3 properties
            in Tailwind's generated stylesheet (confirmed via
            getComputedStyle: overrides were present in the class
            attribute but lost the cascade anyway), the same class of risk
            the screen's own previous "Quay lại" implementation already
            worked around with an inline style. A raw button reusing
            Button's own `primary` variant treatment verbatim
            (`bg-primary text-white hover:bg-primary-dark` — "giữ
            hover/focus visual system hiện tại") sidesteps the conflict
            entirely instead of fighting it. */}
        <button
          type="button"
          onClick={() => onStart?.(config)}
          className="font-ui mt-4 flex h-[74px] w-full items-center justify-center rounded-[18px] bg-primary text-2xl font-bold text-white transition-colors hover:bg-primary-dark"
        >
          Bắt đầu luyện tập
        </button>
      </div>
    </div>
  );
}
