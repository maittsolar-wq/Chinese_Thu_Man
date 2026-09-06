"use client";

import { useEffect, useRef, useState } from "react";
import clsx from "clsx";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
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
  // page is open. The initial animation decision on data-load does NOT rely
  // on this value -- it calls prefersReducedMotionNow() directly instead,
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
 * lazily on mount, then renders `currentStep` strokes (1-indexed: step N
 * means strokes 1..N are shown) as cumulative SVG paths — no raster images,
 * no per-step assets, one JSON file per character.
 */
function SingleCharacterStroke({ character }: { character: string }) {
  const [status, setStatus] = useState<"loading" | "error" | "ready">("loading");
  const [data, setData] = useState<StrokeOrderCharacterData | null>(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const prefersReducedMotion = usePrefersReducedMotion();
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    let cancelled = false;
    setStatus("loading");
    setData(null);
    fetchStrokeOrderData(character)
      .then((result) => {
        if (cancelled) return;
        setData(result);
        setStatus("ready");
        if (prefersReducedMotionNow()) {
          // Respect prefers-reduced-motion: show the complete character
          // immediately rather than forcing a timed animation.
          setCurrentStep(result.strokes.length);
          setIsPlaying(false);
        } else {
          setCurrentStep(1);
          setIsPlaying(true);
        }
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

  function goToStep(step: number) {
    stopAutoplay();
    setCurrentStep(step);
  }

  function replay() {
    stopAutoplay();
    setCurrentStep(prefersReducedMotion ? (data?.strokes.length ?? 0) : 1);
    if (!prefersReducedMotion) {
      // restart autoplay from step 1
      requestAnimationFrame(() => setIsPlaying(true));
    }
  }

  if (status === "loading") {
    return (
      <Card className="flex min-w-[220px] flex-col items-center gap-3 p-4">
        <p className="text-4xl font-bold text-neutral-300 dark:text-night-border">{character}</p>
        <p className="text-sm text-neutral-500 dark:text-night-muted">Đang tải nét chữ…</p>
      </Card>
    );
  }

  if (status === "error" || !data) {
    return (
      <Card className="min-w-[220px] p-4">
        <EmptyState
          title="Chưa có dữ liệu thứ tự nét."
          description={`Không tải được dữ liệu cho chữ "${character}".`}
        />
      </Card>
    );
  }

  const total = data.strokes.length;

  return (
    <Card className="flex min-w-[220px] flex-col items-center gap-3 p-4">
      <div className="flex items-baseline gap-2">
        <p className="text-2xl font-bold text-neutral-900 dark:text-night-text">{character}</p>
        <p className="text-xs text-neutral-500 dark:text-night-muted">{total} nét</p>
      </div>

      <svg
        viewBox="0 0 1024 1024"
        role="img"
        aria-label={`Thứ tự nét của chữ ${character}, đang hiển thị nét ${currentStep}/${total}`}
        className="h-40 w-40 rounded-md border border-neutral-200 bg-white dark:border-night-border dark:bg-night-input sm:h-48 sm:w-48"
      >
        <g transform={STROKE_TRANSFORM}>
          {/* Faint ghost of the complete character so partial strokes stay legible in context. */}
          {data.strokes.map((d, i) => (
            <path key={`ghost-${i}`} d={d} className="fill-neutral-300 dark:fill-night-border" opacity={0.25} />
          ))}
          {data.strokes.slice(0, currentStep).map((d, i) => (
            <path
              key={`stroke-${i}`}
              d={d}
              className={
                i === currentStep - 1
                  ? "fill-primary"
                  : "fill-neutral-800 dark:fill-night-text"
              }
            />
          ))}
        </g>
      </svg>

      <p className="text-sm font-medium text-neutral-700 dark:text-night-muted" aria-live="polite">
        {currentStep} / {total}
      </p>

      <div className="flex max-w-full gap-1 overflow-x-auto pb-1" role="group" aria-label={`Chọn nét cho chữ ${character}`}>
        {Array.from({ length: total }, (_, i) => i + 1).map((step) => (
          <button
            key={step}
            type="button"
            onClick={() => goToStep(step)}
            aria-label={`Nét ${step}`}
            aria-pressed={currentStep === step}
            className={clsx(
              "flex h-7 w-7 shrink-0 items-center justify-center rounded-md text-xs font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-1",
              currentStep === step
                ? "bg-primary text-white"
                : "bg-neutral-100 text-neutral-700 hover:bg-neutral-200 dark:bg-night-input dark:text-night-muted dark:hover:bg-night-border"
            )}
          >
            {step}
          </button>
        ))}
      </div>

      <Button
        type="button"
        variant="secondary"
        onClick={replay}
        className="text-xs"
        aria-label={`Xem lại thứ tự nét của chữ ${character}`}
      >
        Xem lại
      </Button>
    </Card>
  );
}

/**
 * Top-level Stroke Order section for a vocabulary word. Renders one
 * self-contained SingleCharacterStroke viewer per Han character in the
 * word (each fetches and animates independently — multi-character words
 * never merge stroke paths into a single ambiguous animation).
 */
export function StrokeOrderViewer({ word }: { word: string }) {
  const characters = getCharactersForWord(word);

  if (characters.length === 0) {
    return <EmptyState title="Chưa có dữ liệu thứ tự nét." />;
  }

  return (
    <div className="flex flex-wrap gap-3">
      {characters.map((character, index) => (
        // Same character can repeat within a word (e.g. 认认真真); index
        // keeps keys unique without affecting data loading (still keyed by
        // character internally).
        <SingleCharacterStroke key={`${character}-${index}`} character={character} />
      ))}
    </div>
  );
}
