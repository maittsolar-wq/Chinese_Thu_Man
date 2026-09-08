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
      {/* Visual-redesign pass: taller (~70px, was ~52px), mockup border
          color (#D7E0EA) and radius (16px = stock `rounded-2xl`), Be
          Vietnam Pro at 20px/weight 600 (was no font-ui at all, defaulting
          to the browser's fallback sans, plus the wrong 700 weight). */}
      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        aria-haspopup="listbox"
        aria-expanded={open}
        className="font-ui flex h-[70px] w-full items-center justify-between rounded-2xl border border-[#D7E0EA] bg-white px-6 text-left text-xl font-semibold text-neutral-900 outline-none focus:border-primary focus:ring-1 focus:ring-primary dark:border-night-border dark:bg-night-input dark:text-night-text"
      >
        <span>HSK {value}</span>
        <ChevronDownIcon
          className={clsx("h-6 w-6 shrink-0 text-neutral-500 transition-transform dark:text-night-muted", {
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
          {/* Positioning fix: the trigger above is now full-width (spans
              the whole ~1000px+ content area on desktop), so the old
              `left-0 right-0` (stretch to match the trigger's own full
              width) would make the popup itself absurdly wide there.
              From `sm:` up (>=640px, where the trigger has 600px+ to work
              with either way) it's anchored at the trigger's RIGHT edge
              (`sm:right-0`, `sm:left-auto`) with a fixed mockup width
              (320-360px, here 340px) so it "opens toward the left" from
              that anchor — the requested visual direction, safely clear
              of the viewport edge at every width `sm:` covers.
              Below `sm` (mobile), a flat `calc(100vw-Npx)` guess isn't
              reliable — the trigger's right edge sits inset from the
              viewport by however much page margin + card padding apply
              at that breakpoint (a real, measured overflow at 375px:
              anchoring a fixed 340px popup to a trigger edge that's
              already ~40px inset pushed the popup ~6px past the LEFT
              edge of the viewport). So on mobile this instead reverts to
              the original `left-0 right-0` (stretch to match the
              trigger's own width) — inherently overflow-safe, since the
              trigger itself never overflows the viewport, and per §11's
              own "no room to open left -> auto-pick a fitting direction"
              allowance. No positioning library needed for either case. */}
          <ul
            role="listbox"
            aria-label="Chọn cấp độ HSK"
            className="absolute left-0 right-0 top-full z-30 mt-2 max-h-[420px] overflow-auto rounded-[20px] border border-neutral-200 bg-white p-2 shadow-card dark:border-night-border dark:bg-night-surface sm:left-auto sm:w-[340px]"
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
                    className={clsx(
                      "font-ui flex h-[54px] w-full items-center justify-between rounded-xl px-4 text-left text-xl transition-colors",
                      selected
                        ? "bg-primary-tint font-semibold text-primary dark:bg-primary-dark/20 dark:text-night-primary"
                        : "text-neutral-900 hover:bg-neutral-50 dark:text-night-text dark:hover:bg-night-input"
                    )}
                  >
                    <span>HSK {level}</span>
                    {selected && <CheckCircleIcon className="h-5 w-5 shrink-0 text-primary dark:text-night-primary" />}
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
