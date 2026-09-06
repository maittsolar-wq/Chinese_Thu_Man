"use client";

import { useEffect, useRef, useState } from "react";
import clsx from "clsx";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { ReplayIcon } from "@/components/ui/icons";
import type { StrokeOrderCharacterData } from "@/lib/data/types";
import {
  fetchStrokeOrderData,
  getCharactersForWord,
} from "@/lib/data/strokeOrderLoader";

/**
 * Make Me a Hanzi's coordinate system has strokes/medians on a 1024x1024
 * grid with an inverted y-axis; this transform is the exact one documented
 * by the source project to render right-side-up. See
 * tools/hsk/stroke_order/README.md for the data source and license.
 */
const STROKE_TRANSFORM = "scale(1, -1) translate(0, -900)";
const AUTOPLAY_INTERVAL_MS = 550;

type ViewMode = "full" | "animate";

/** Synchronous, freshly-read check -- safe to call inside another effect's
 * callback without depending on this-or-another hook's state having
 * already committed a re-render (a stale-closure trap that a `useState`
 * mirror of this value would otherwise fall into on the very first mount,
 * since effects declared earlier in the same component don't get to
 * re-render before later effects run in that same commit pass). */
function prefersReducedMotionNow(): boolean {
  if (typeof window === "undefined" || !window.matchMedia) return false;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function usePrefersReducedMotion(): boolean {
  // Starts false to match server-rendered output (no hydration mismatch);
  // updated via effect for reactivity to a LIVE OS-setting change while the
  // page is open. The initial mode-switch decision below does NOT rely on
  // this value -- it calls prefersReducedMotionNow() directly instead,
  // since this state is not guaranteed to have committed yet on first mount.
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    const query = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(query.matches);
    const handler = (event: MediaQueryListEvent) => setReduced(event.matches);
    query.addEventListener("change", handler);
    return () => query.removeEventListener("change", handler);
  }, []);
  return reduced;
}

/**
 * Stroke-order viewer for a single Han character. Fetches its stroke data
 * lazily on mount (unchanged -- one JSON file per character, fired exactly
 * when this viewer mounts). All state/behavior below (view modes, run-once
 * animation, reduced-motion handling, manual step control) is unchanged
 * from the previous pass -- this file's edit is a layout-only rewrite: a
 * full-width two-column presentation (canvas left, mode/progress/controls
 * right on wide viewports; stacked on narrow ones) instead of a small card
 * in a wrapped row, per the UI Foundation Phase's "Stroke Order must not
 * read as an afterthought next to empty desktop whitespace" direction.
 */
function SingleCharacterStroke({ character }: { character: string }) {
  const [status, setStatus] = useState<"loading" | "error" | "ready">("loading");
  const [data, setData] = useState<StrokeOrderCharacterData | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>("full");
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const prefersReducedMotion = usePrefersReducedMotion();
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    let cancelled = false;
    setStatus("loading");
    setData(null);
    setViewMode("full");
    setCurrentStep(0);
    setIsPlaying(false);
    fetchStrokeOrderData(character)
      .then((result) => {
        if (cancelled) return;
        setData(result);
        setStatus("ready");
        // Default view is the complete character -- no autoplay.
        setCurrentStep(result.strokes.length);
      })
      .catch(() => {
        if (!cancelled) setStatus("error");
      });
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [character]);

  useEffect(() => {
    if (!isPlaying || !data) return;
    intervalRef.current = setInterval(() => {
      setCurrentStep((step) => {
        const next = step + 1;
        if (next >= data.strokes.length) {
          setIsPlaying(false);
          return data.strokes.length;
        }
        return next;
      });
    }, AUTOPLAY_INTERVAL_MS);
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [isPlaying, data]);

  function stopAutoplay() {
    setIsPlaying(false);
    if (intervalRef.current) clearInterval(intervalRef.current);
  }

  /** Manual step jump -- preserved as a secondary, fine-grained control.
   *  Stop any autoplay, jump straight to the chosen stroke. */
  function goToStep(step: number) {
    stopAutoplay();
    setCurrentStep(step);
  }

  /** Runs (or re-runs) the animation from stroke 1 through the last
   *  stroke, respecting reduced-motion by jumping straight to the
   *  finished state instead of forcing a timed sequence. Used both when
   *  first switching into "Xem nét vẽ" and by the "Phát lại" button --
   *  replay never happens on its own. */
  function startAnimation() {
    if (!data) return;
    stopAutoplay();
    if (prefersReducedMotionNow()) {
      setCurrentStep(data.strokes.length);
    } else {
      setCurrentStep(1);
      requestAnimationFrame(() => setIsPlaying(true));
    }
  }

  function selectMode(mode: ViewMode) {
    if (mode === viewMode) return;
    setViewMode(mode);
    if (mode === "full") {
      stopAutoplay();
      setCurrentStep(data?.strokes.length ?? 0);
    } else {
      startAnimation();
    }
  }

  if (status === "loading") {
    return (
      <Card className="flex flex-col items-center gap-3 border-hairline p-6 sm:flex-row sm:items-start sm:gap-8 sm:p-8">
        <p className="font-cjk text-6xl font-normal text-neutral-300 dark:text-night-border">{character}</p>
        <p className="text-sm text-ink-muted dark:text-night-muted">Đang tải nét chữ…</p>
      </Card>
    );
  }

  if (status === "error" || !data) {
    return (
      <Card className="border-hairline p-6">
        <EmptyState
          title="Chưa có dữ liệu thứ tự nét."
          description={`Không tải được dữ liệu cho chữ "${character}".`}
        />
      </Card>
    );
  }

  const total = data.strokes.length;
  const isAnimationDone = viewMode === "animate" && !isPlaying && currentStep === total;
  const visibleStrokes = viewMode === "full" ? total : currentStep;

  return (
    <Card className="flex flex-col gap-6 border-hairline p-5 sm:flex-row sm:items-start sm:gap-8 sm:p-8">
      {/* LEFT — large canvas. Full-width per character, not a small card in
          a row: the biggest visual weight in this section besides the hero
          itself. */}
      <div className="flex shrink-0 justify-center sm:justify-start">
        <svg
          viewBox="0 0 1024 1024"
          role="img"
          aria-label={
            viewMode === "full"
              ? `Chữ ${character} đầy đủ, ${total} nét`
              : `Thứ tự nét của chữ ${character}, đang hiển thị nét ${currentStep}/${total}`
          }
          className="h-56 w-56 rounded-xl border border-hairline bg-white dark:border-night-border dark:bg-night-input sm:h-64 sm:w-64"
        >
          <g transform={STROKE_TRANSFORM}>
            {/* Faint ghost of the complete character so partial strokes stay
                legible in context -- only meaningful mid-animation. */}
            {viewMode === "animate" &&
              data.strokes.map((d, i) => (
                <path key={`ghost-${i}`} d={d} className="fill-neutral-300 dark:fill-night-border" opacity={0.25} />
              ))}
            {data.strokes.slice(0, visibleStrokes).map((d, i) => (
              <path
                key={`stroke-${i}`}
                d={d}
                className={
                  viewMode === "animate" && i === currentStep - 1
                    ? "fill-primary"
                    : "fill-ink dark:fill-night-text"
                }
              />
            ))}
          </g>
        </svg>
      </div>

      {/* RIGHT — identity, mode toggle, progress/controls. */}
      <div className="flex flex-1 flex-col gap-4">
        <div className="flex items-baseline gap-3">
          <p className="font-cjk text-3xl font-normal text-ink dark:text-night-text">{character}</p>
          <p className="text-sm text-ink-muted dark:text-night-muted">{total} nét</p>
        </div>

        <div
          role="group"
          aria-label={`Chế độ xem chữ ${character}`}
          className="inline-flex w-fit rounded-md border border-hairline p-0.5 dark:border-night-border"
        >
          <button
            type="button"
            onClick={() => selectMode("full")}
            aria-pressed={viewMode === "full"}
            className={clsx(
              "rounded px-3 py-1.5 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-1",
              viewMode === "full"
                ? "bg-primary text-white"
                : "text-ink-muted hover:text-primary dark:text-night-muted dark:hover:text-night-text"
            )}
          >
            Chữ đầy đủ
          </button>
          <button
            type="button"
            onClick={() => selectMode("animate")}
            aria-pressed={viewMode === "animate"}
            className={clsx(
              "rounded px-3 py-1.5 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-1",
              viewMode === "animate"
                ? "bg-primary text-white"
                : "text-ink-muted hover:text-primary dark:text-night-muted dark:hover:text-night-text"
            )}
          >
            Xem nét vẽ
          </button>
        </div>

        {viewMode === "animate" ? (
          <>
            <div className="flex flex-col gap-1.5">
              <p className="text-lg font-semibold text-ink dark:text-night-text" aria-live="polite">
                Nét {currentStep} / {total}
              </p>
              <div
                role="progressbar"
                aria-valuenow={currentStep}
                aria-valuemin={0}
                aria-valuemax={total}
                aria-label={`Tiến độ nét chữ ${character}`}
                className="h-2 w-full max-w-xs overflow-hidden rounded-full bg-neutral-100 dark:bg-night-input"
              >
                <div
                  className="h-full rounded-full bg-primary transition-[width] duration-300 dark:bg-night-primary"
                  style={{ width: `${(currentStep / total) * 100}%` }}
                />
              </div>
            </div>

            {isAnimationDone ? (
              <Button type="button" variant="secondary" onClick={startAnimation} className="w-fit gap-1.5">
                <ReplayIcon className="h-4 w-4" />
                Phát lại
              </Button>
            ) : (
              // Secondary, fine-grained manual control -- preserved from the
              // pre-redesign implementation (same goToStep/aria-pressed
              // behavior), visually de-emphasized under the progress bar.
              <div
                className="flex max-w-full flex-wrap gap-1"
                role="group"
                aria-label={`Chọn nét cho chữ ${character}`}
              >
                {Array.from({ length: total }, (_, i) => i + 1).map((step) => (
                  <button
                    key={step}
                    type="button"
                    onClick={() => goToStep(step)}
                    aria-label={`Nét ${step}`}
                    aria-pressed={currentStep === step}
                    className={clsx(
                      "flex h-6 w-6 shrink-0 items-center justify-center rounded text-[11px] font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-1",
                      currentStep === step
                        ? "bg-primary text-white"
                        : "bg-neutral-100 text-ink-muted hover:bg-neutral-200 dark:bg-night-input dark:text-night-muted dark:hover:bg-night-border"
                    )}
                  >
                    {step}
                  </button>
                ))}
              </div>
            )}
          </>
        ) : (
          <p className="text-sm text-ink-muted dark:text-night-muted">Chữ hoàn chỉnh</p>
        )}
      </div>
    </Card>
  );
}

/**
 * Top-level Stroke Order section for a vocabulary word. Renders one
 * self-contained, full-width SingleCharacterStroke viewer per Han
 * character in the word, stacked vertically -- each fetches and animates
 * independently -- multi-character words never merge stroke paths into a
 * single ambiguous animation, and picking a mode or replaying on one
 * character never affects any other.
 */
export function StrokeOrderViewer({ word }: { word: string }) {
  const characters = getCharactersForWord(word);

  if (characters.length === 0) {
    return <EmptyState title="Chưa có dữ liệu thứ tự nét." />;
  }

  return (
    <div className="flex flex-col gap-4">
      {characters.map((character, index) => (
        // Same character can repeat within a word (e.g. 认认真真); index
        // keeps keys unique without affecting data loading (still keyed by
        // character internally).
        <SingleCharacterStroke key={`${character}-${index}`} character={character} />
      ))}
    </div>
  );
}
