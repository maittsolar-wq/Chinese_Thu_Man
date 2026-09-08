"use client";

import clsx from "clsx";
import { WORD_COUNT_OPTIONS, type WordCountOption } from "@/lib/practice/types";

export function WordCountSelector({
  value,
  onChange,
}: {
  value: WordCountOption;
  onChange: (count: WordCountOption) => void;
}) {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 sm:gap-4" role="radiogroup" aria-label="Số lượng từ">
      {WORD_COUNT_OPTIONS.map((option) => {
        const selected = option.value === value;
        return (
          <button
            key={option.value}
            type="button"
            role="radio"
            aria-checked={selected}
            onClick={() => onChange(option.value)}
            className={clsx(
              "font-ui flex h-[74px] items-center justify-center rounded-2xl border px-3 text-center text-[22px] font-semibold transition-colors",
              selected
                ? "border-primary bg-primary text-white"
                : "border-[#D7E0EA] bg-white text-neutral-900 hover:bg-neutral-50 dark:border-night-border dark:bg-night-input dark:text-night-text dark:hover:bg-night-surface"
            )}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}
