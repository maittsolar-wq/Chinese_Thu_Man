"use client";

import { useState } from "react";
import { useSearchParams } from "next/navigation";
import { Card } from "@/components/ui/Card";
import { Button, LinkButton } from "@/components/ui/Button";
import { ArrowLeftIcon } from "@/components/ui/icons";
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
  const [config, setConfig] = useState<PracticeConfigState>(DEFAULT_PRACTICE_CONFIG);
  const backHref = useConfigBackHref();

  return (
    <div className="flex flex-col gap-6">
      {/* `backgroundColor` is set inline (not a `bg-primary/80` class) so it
          reliably wins over LinkButton's own `bg-primary` variant class
          regardless of Tailwind's generated CSS order — inline style
          always has higher specificity than any class. #025291CC = the
          same primary blue at exactly 80% alpha (0xCC = 204/255 = 0.8). */}
      <LinkButton
        href={backHref}
        className="w-fit transition-opacity hover:opacity-90"
        style={{ backgroundColor: "#025291CC" }}
      >
        <ArrowLeftIcon className="h-4 w-4" />
        Quay lại
      </LinkButton>

      <div className="flex flex-col gap-1">
        <h1 className="text-3xl font-bold text-primary dark:text-night-primary sm:text-4xl">
          {info.title}
        </h1>
        <p className="text-neutral-600 dark:text-night-muted">{info.description}</p>
      </div>

      <Card className="flex flex-col gap-8 p-6 sm:p-8">
        <h2 className="text-center text-2xl font-bold text-primary dark:text-night-primary">
          Cấu hình luyện tập
        </h2>

        <div className="flex flex-col gap-3">
          <span className="text-base font-medium text-neutral-900 dark:text-night-text">
            Phạm vi luyện tập
          </span>
          <HskSelector
            value={config.hskLevel}
            onChange={(hskLevel) => setConfig((prev) => ({ ...prev, hskLevel }))}
          />
        </div>

        <div className="flex flex-col gap-3">
          <span className="text-base font-medium text-neutral-900 dark:text-night-text">
            Số lượng từ
          </span>
          <WordCountSelector
            value={config.wordCount}
            onChange={(wordCount) => setConfig((prev) => ({ ...prev, wordCount }))}
          />
        </div>

        <Button type="button" onClick={() => onStart?.(config)} className="w-full py-4 text-lg">
          Bắt đầu luyện tập
        </Button>
      </Card>
    </div>
  );
}
