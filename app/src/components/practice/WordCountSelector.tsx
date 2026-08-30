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
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4" role="radiogroup" aria-label="Số lượng từ">
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
              "rounded-md border px-4 py-3 text-center text-lg font-bold transition-colors",
              selected
                ? "border-primary bg-primary text-white"
                : "border-neutral-300 bg-white text-neutral-900 hover:bg-neutral-50 dark:border-night-border dark:bg-night-input dark:text-night-text dark:hover:bg-night-surface"
            )}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}
