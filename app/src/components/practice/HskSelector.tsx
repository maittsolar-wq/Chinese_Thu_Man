"use client";

import { useEffect, useRef, useState } from "react";
import clsx from "clsx";
import type { HskLevel } from "@/lib/data/types";
import { HSK_LEVELS } from "@/lib/practice/types";
import { ChevronDownIcon, CheckCircleIcon } from "@/components/ui/icons";

/**
 * Custom HSK level dropdown for Practice configuration, matching the
 * open-state reference ("Luyện tập (6).png"): a bordered trigger button,
 * a floating white panel listing HSK 1-6, and a blue checkmark next to
 * the selected level. A full-page dimming backdrop appears while open,
 * matching that same reference, and closes the panel on click/Escape.
 */
export function HskSelector({
  value,
  onChange,
}: {
  value: HskLevel;
  onChange: (level: HskLevel) => void;
}) {
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    function handleKey(event: KeyboardEvent) {
      if (event.key === "Escape") setOpen(false);
    }
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [open]);

  return (
    <div ref={containerRef} className="relative">
      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        aria-haspopup="listbox"
        aria-expanded={open}
        className="flex w-full items-center justify-between rounded-md border border-neutral-300 bg-white px-4 py-3 text-left text-lg font-bold text-neutral-900 outline-none focus:border-primary focus:ring-1 focus:ring-primary dark:border-night-border dark:bg-night-input dark:text-night-text"
      >
        <span>HSK {value}</span>
        <ChevronDownIcon
          className={clsx("h-5 w-5 shrink-0 text-neutral-500 transition-transform dark:text-night-muted", {
            "rotate-180": open,
          })}
        />
      </button>

      {open && (
        <>
          {/* Dimming backdrop, matching the reference dropdown-open state. */}
          <button
            type="button"
            aria-label="Đóng danh sách cấp độ HSK"
            onClick={() => setOpen(false)}
            className="fixed inset-0 z-20 cursor-default bg-neutral-900/10 dark:bg-black/40"
          />
          <ul
            role="listbox"
            aria-label="Chọn cấp độ HSK"
            className="absolute left-0 right-0 top-full z-30 mt-2 max-h-80 overflow-auto rounded-card border border-neutral-200 bg-white py-2 shadow-card dark:border-night-border dark:bg-night-surface"
          >
            {HSK_LEVELS.map((level) => {
              const selected = level === value;
              return (
                <li key={level} role="option" aria-selected={selected}>
                  <button
                    type="button"
                    onClick={() => {
                      onChange(level);
                      setOpen(false);
                    }}
                    className="flex w-full items-center justify-between px-5 py-3 text-left text-lg text-neutral-900 hover:bg-neutral-50 dark:text-night-text dark:hover:bg-night-input"
                  >
                    <span>HSK {level}</span>
                    {selected && <CheckCircleIcon className="h-5 w-5 shrink-0 text-primary" />}
                  </button>
                </li>
              );
            })}
          </ul>
        </>
      )}
    </div>
  );
}
