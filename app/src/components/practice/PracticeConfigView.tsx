"use client";

import { useState } from "react";
import { Card } from "@/components/ui/Card";
import { LinkButton } from "@/components/ui/Button";
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
 * Shared Practice Configuration screen for all four exercise types — one
 * implementation rendering whichever type/content is passed in, per
 * docs/PRACTICE §2 ("Configuration — shared by all four exercise types").
 *
 * This is the configuration *foundation* only: it holds hskLevel/wordCount
 * as local state, matching the defaults shown in every supplied reference
 * screenshot (HSK 2 / 20). The "Bắt đầu luyện tập" button intentionally has
 * no destination yet — the actual practice exercise/session screens don't
 * exist in the codebase yet (see docs/PRACTICE), and per instructions no
 * placeholder/fake route or exercise logic is invented here.
 */
export function PracticeConfigView({ practiceType }: { practiceType: PracticeType }) {
  const info = PRACTICE_TYPE_INFO[practiceType];
  const [config, setConfig] = useState<PracticeConfigState>(DEFAULT_PRACTICE_CONFIG);

  return (
    <div className="flex flex-col gap-6">
      <LinkButton href="/" className="w-fit">
        <ArrowLeftIcon className="h-4 w-4" />
        Quay lại
      </LinkButton>

      <div className="flex flex-col gap-1">
        <h1 className="text-3xl font-bold text-primary sm:text-4xl">{info.title}</h1>
        <p className="text-neutral-600 dark:text-night-muted">{info.description}</p>
      </div>

      <Card className="flex flex-col gap-8 p-6 sm:p-8">
        <h2 className="text-center text-2xl font-bold text-primary">Cấu hình luyện tập</h2>

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

        {/*
          Foundation-only CTA: the practice exercise screen for this type
          does not exist yet, so this intentionally has no navigation or
          exercise logic attached (see component doc comment above).
        */}
        <button
          type="button"
          className="w-full rounded-md bg-primary py-4 text-lg font-bold text-white transition-colors hover:bg-primary-dark"
        >
          Bắt đầu luyện tập
        </button>
      </Card>
    </div>
  );
}
