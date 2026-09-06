"use client";

import { useEffect, useRef, useState } from "react";
import clsx from "clsx";
import { SpeakerIcon } from "@/components/ui/icons";

type PlaybackStatus = "idle" | "loading" | "playing" | "error";

/**
 * Vocabulary Detail's pronunciation button. `VocabularyAudio.wordUrl` has
 * existed since the Audio integration pass but had no playback UI wired to
 * it (Phase 02 §10 deliberately left this disabled rather than pretend to
 * work) — this wires up real playback for the ~5377/5400 records that have
 * a URL, while keeping the exact original disabled/"chưa khả dụng" markup
 * for the ~23 that don't. Scoped to this one button only: the other
 * still-disabled speaker buttons elsewhere (e.g. FlashcardExerciseView) are
 * untouched.
 *
 * A dedicated small client component rather than converting the whole
 * (server-rendered) VocabularyDetail — same "interactive island" pattern
 * already used for ThemeToggle/DictionarySearchTrigger in this codebase.
 */
export function PronunciationButton({ wordUrl }: { wordUrl: string | null }) {
  const [status, setStatus] = useState<PlaybackStatus>("idle");
  const audioRef = useRef<HTMLAudioElement | null>(null);
  // Guards re-entrancy synchronously. `status` alone isn't enough: a burst
  // of clicks dispatched faster than a React re-render (e.g. OS key-repeat
  // holding Enter/Space, or several rapid taps) all run handleClick with
  // the SAME stale `status` closure before any `setStatus` from an earlier
  // call in that same burst has committed — the state check alone let every
  // click in the burst through, each constructing its own Audio and
  // overlapping playback. A ref mutates immediately, so it closes that race
  // regardless of React's batching.
  const isBusyRef = useRef(false);

  // Reset on navigation to a different word (wordUrl changes) and pause
  // playback on unmount — never let a previous word's audio keep playing
  // in the background after the button itself is gone.
  useEffect(() => {
    setStatus("idle");
    isBusyRef.current = false;
    return () => {
      audioRef.current?.pause();
      audioRef.current = null;
    };
  }, [wordUrl]);

  if (!wordUrl) {
    return (
      <button
        type="button"
        disabled
        aria-label="Nghe phát âm (chưa khả dụng)"
        title="Nghe phát âm (chưa khả dụng)"
        className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary text-white disabled:cursor-not-allowed disabled:opacity-50"
      >
        <SpeakerIcon className="h-4 w-4" />
      </button>
    );
  }

  function handleClick() {
    // Ignore clicks while a playback attempt is already in flight; once
    // ended/errored, isBusyRef clears and a click plays again from the
    // start (replay, and — since a fresh element is created on every
    // attempt — a genuine retry after a network error, not a reuse of a
    // media element stuck in an error readyState).
    if (isBusyRef.current) return;
    isBusyRef.current = true;

    audioRef.current?.pause();
    // Safe: this handler is only reachable from the button rendered below
    // the `!wordUrl` early return above, so wordUrl is a string here — TS
    // just can't narrow a prop across this closure boundary.
    const audio = new Audio(wordUrl as string);
    audio.addEventListener("ended", () => {
      isBusyRef.current = false;
      setStatus("idle");
    });
    audio.addEventListener("error", () => {
      isBusyRef.current = false;
      setStatus("error");
    });
    audioRef.current = audio;

    setStatus("loading");
    audio
      .play()
      .then(() => setStatus("playing"))
      .catch(() => {
        isBusyRef.current = false;
        setStatus("error");
      });
  }

  const isBusy = status === "loading" || status === "playing";
  const label =
    status === "loading"
      ? "Đang tải phát âm…"
      : status === "playing"
        ? "Đang phát âm, nhấn để dừng và phát lại"
        : status === "error"
          ? "Không phát được âm thanh, nhấn để thử lại"
          : "Nghe phát âm";

  return (
    <button
      type="button"
      onClick={handleClick}
      aria-label={label}
      title={label}
      aria-busy={isBusy}
      className={clsx(
        "inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary text-white transition-colors hover:bg-primary-dark focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-1",
        isBusy && "animate-pulse",
        status === "error" && "ring-2 ring-error"
      )}
    >
      <SpeakerIcon className="h-4 w-4" />
    </button>
  );
}
