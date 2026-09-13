"use client";

import { HeadphonesIcon, PauseIcon, PlayIcon, SkipBackIcon, SkipForwardIcon, SpeakerIcon } from "@/components/ui/icons";
import { formatDuration } from "@/lib/listening/format";
import type { ListeningLesson } from "@/lib/listening/types";

export const PLAYBACK_SPEEDS = [0.75, 1, 1.25, 1.5] as const;

/**
 * No real video source exists yet (a later B2 Integration phase wires that
 * up) — this is a fully mock, portrait 9:16 player: a static frame
 * standing in for the video plus real play/pause/seek/speed UI state,
 * driven by a plain interval in the parent (ListeningLessonDetailView),
 * not an actual <video> element. Subtitle controls are intentionally NOT
 * implemented (out of scope for this phase — the real video already bakes
 * in Chinese/pinyin/Vietnamese).
 *
 * Interface readiness (Phase 1.5): `lesson.videoUrl` (types.ts) already
 * carries where a real source will come from — every mock lesson leaves it
 * unset, so this component always takes the mock-frame branch today. A
 * real `<video>` branch (keyed on `lesson.videoUrl` being present, using a
 * `<video ref>` for real play()/pause()/currentTime/playbackRate instead
 * of the interval-driven mock clock below) is deliberately NOT built yet —
 * there's no real file to test it against in this phase, and getting that
 * wiring right belongs with the B2 Integration phase that actually
 * produces a real `videoUrl` to point it at.
 */
export function ListeningVideoPlayer({
  lesson,
  currentTime,
  isPlaying,
  speed,
  onTogglePlay,
  onSeek,
  onSpeedChange,
}: {
  lesson: ListeningLesson;
  currentTime: number;
  isPlaying: boolean;
  speed: (typeof PLAYBACK_SPEEDS)[number];
  onTogglePlay: () => void;
  onSeek: (seconds: number) => void;
  onSpeedChange: (speed: (typeof PLAYBACK_SPEEDS)[number]) => void;
}) {
  const progress = lesson.durationSeconds > 0 ? currentTime / lesson.durationSeconds : 0;

  function handleScrub(event: React.ChangeEvent<HTMLInputElement>) {
    onSeek(Number(event.target.value));
  }

  function cycleSpeed() {
    const index = PLAYBACK_SPEEDS.indexOf(speed);
    onSpeedChange(PLAYBACK_SPEEDS[(index + 1) % PLAYBACK_SPEEDS.length]!);
  }

  return (
    <div className="mx-auto w-full max-w-[420px] shrink-0 lg:mx-0">
      <div className="overflow-hidden rounded-3xl border border-[#E2E8F0] bg-white shadow-card dark:border-night-border dark:bg-night-surface">
        <button
          type="button"
          onClick={onTogglePlay}
          aria-label={isPlaying ? "Tạm dừng" : "Phát"}
          className="relative flex aspect-[9/16] w-full flex-col items-center justify-center gap-3 overflow-hidden bg-neutral-900"
        >
          <HeadphonesIcon className="h-10 w-10 text-white/60" />
          <span className="font-cjk px-6 text-center text-2xl font-semibold text-white">
            {lesson.chineseTitle}
          </span>
          <span className="absolute inset-0 flex items-center justify-center bg-black/0 transition-colors hover:bg-black/20">
            <span className="flex h-16 w-16 items-center justify-center rounded-full bg-white/90 shadow-card">
              {isPlaying ? (
                <PauseIcon className="h-7 w-7 text-primary" />
              ) : (
                <PlayIcon className="h-7 w-7 translate-x-[2px] text-primary" />
              )}
            </span>
          </span>
        </button>

        <div className="flex flex-col gap-2 p-4">
          <input
            type="range"
            min={0}
            max={lesson.durationSeconds}
            step={1}
            value={currentTime}
            onChange={handleScrub}
            aria-label="Tua video"
            className="h-1.5 w-full cursor-pointer appearance-none rounded-full bg-neutral-200 accent-primary dark:bg-night-border"
            style={{
              background: `linear-gradient(to right, #025291 ${progress * 100}%, #E2E8F0 ${progress * 100}%)`,
            }}
          />
          <div className="font-ui flex items-center justify-between text-sm font-medium text-neutral-600 dark:text-night-muted">
            <span>{formatDuration(currentTime)}</span>
            <span>{formatDuration(lesson.durationSeconds)}</span>
          </div>

          {/* Only the functional controls remain — the previous gear
              (settings) and fullscreen icons had no implemented behavior
              behind them and were removed rather than left as dead
              decoration. Remaining controls sized up from the original
              pass for a more comfortable touch/click target. */}
          <div className="mt-1 flex items-center justify-between">
            <SpeakerIcon className="h-6 w-6 shrink-0 text-neutral-600 dark:text-night-muted" />
            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => onSeek(Math.max(0, currentTime - 10))}
                aria-label="Lùi 10 giây"
                className="flex h-10 w-10 items-center justify-center rounded-full text-neutral-700 hover:bg-neutral-100 dark:text-night-muted dark:hover:bg-night-input"
              >
                <SkipBackIcon className="h-6 w-6" />
              </button>
              <button
                type="button"
                onClick={onTogglePlay}
                aria-label={isPlaying ? "Tạm dừng" : "Phát"}
                className="flex h-14 w-14 items-center justify-center rounded-full bg-primary text-white hover:bg-primary-dark"
              >
                {isPlaying ? (
                  <PauseIcon className="h-6 w-6" />
                ) : (
                  <PlayIcon className="h-6 w-6 translate-x-[2px]" />
                )}
              </button>
              <button
                type="button"
                onClick={() => onSeek(Math.min(lesson.durationSeconds, currentTime + 10))}
                aria-label="Tiến 10 giây"
                className="flex h-10 w-10 items-center justify-center rounded-full text-neutral-700 hover:bg-neutral-100 dark:text-night-muted dark:hover:bg-night-input"
              >
                <SkipForwardIcon className="h-6 w-6" />
              </button>
            </div>
            <button
              type="button"
              onClick={cycleSpeed}
              aria-label={`Tốc độ phát ${speed}x, nhấn để đổi`}
              className="font-ui rounded-lg border border-neutral-300 px-3 py-2 text-base font-medium text-neutral-700 hover:bg-neutral-50 dark:border-night-border dark:text-night-muted dark:hover:bg-night-input"
            >
              {speed}x
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
