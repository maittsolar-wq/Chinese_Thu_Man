"use client";

import { PronunciationButton } from "@/components/vocabulary/PronunciationButton";
import type { FlashcardSessionState } from "@/lib/practice/flashcardSession";

/**
 * Exercise screen for Flashcard. Sequential, one card at a time — like the
 * other practice exercises: there are NO user-facing previous/next
 * controls. The only actions are "Không nhớ" (wrong) / "Đã nhớ" (correct);
 * choosing either records the answer and the parent auto-advances to the
 * next card (or, on the last card, to the Result screen). The card can
 * still be tapped to flip and reveal the meaning before choosing.
 *
 * Pure presentation: flip / evaluate are delegated to callbacks, which the
 * parent (FlashcardPracticeFlow) maps onto the flashcardSession.ts domain
 * functions. No score/evaluation/advance logic lives here.
 */
export function FlashcardExerciseView({
  session,
  onFlip,
  onEvaluate,
}: {
  session: FlashcardSessionState;
  onFlip: () => void;
  onEvaluate: (result: "correct" | "wrong") => void;
}) {
  const card = session.cards[session.currentIndex];
  const total = session.cards.length;

  if (!card) return null;

  const current = session.currentIndex + 1;
  const progressPercent = (current / total) * 100;

  return (
    // Visual-redesign pass: raw div (not shared `<Card>`) for the mockup
    // panel radius (24px) + #E2E8F0 border, matching Practice Config /
    // Result.
    <div className="flex flex-col gap-6 rounded-3xl border border-[#E2E8F0] bg-white p-6 shadow-card dark:border-night-border dark:bg-night-surface sm:p-8">
      <div className="flex flex-col gap-2">
        <p className="font-ui text-center text-lg font-bold text-neutral-900 dark:text-night-text">
          {current}/{total}
        </p>
        <div
          role="progressbar"
          aria-valuenow={current}
          aria-valuemin={1}
          aria-valuemax={total}
          className="h-2 w-full overflow-hidden rounded-full bg-primary-light dark:bg-night-input"
        >
          <div
            className="h-full rounded-full bg-primary transition-all"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      <div className="flex justify-center">
        <div
          role="button"
          tabIndex={0}
          onClick={onFlip}
          onKeyDown={(event) => {
            if (event.key === "Enter" || event.key === " ") {
              event.preventDefault();
              onFlip();
            }
          }}
          aria-label={card.isFlipped ? "Ẩn nghĩa" : "Xem nghĩa"}
          className="flex min-h-[220px] w-full max-w-md cursor-pointer flex-col items-center justify-center gap-3 rounded-2xl border border-[#E2E8F0] bg-white p-8 text-center shadow-card transition-colors dark:border-night-border dark:bg-night-surface"
        >
          <div className="flex items-center gap-3">
            <span className="font-cjk text-5xl font-semibold text-neutral-900 dark:text-night-text">
              {card.word}
            </span>
            {/*
              Audio wiring fix: reuses Vocabulary Detail's PronunciationButton
              verbatim — the app's single audio-playback component (fresh
              Audio() per attempt, `isBusyRef` re-entrancy guard so rapid
              clicks can't overlap, resets on word change, pauses on unmount,
              renders itself disabled + "chưa khả dụng" when `wordUrl` is
              null, never autoplays). The URL now reaches the card via
              `PracticeVocabularyItem.audioUrl` (fetchPracticeVocabulary ->
              flashcardSession) — previously this button was a hardcoded
              `disabled` placeholder because that URL was dropped and no
              playback UI existed.

              The wrapper stops click / Enter / Space from bubbling to the
              card's own flip handler (the old placeholder was `disabled` so
              it fired no event; a real button needs this guard).
            */}
            <span
              onClick={(event) => event.stopPropagation()}
              onKeyDown={(event) => event.stopPropagation()}
              className="inline-flex shrink-0"
            >
              <PronunciationButton wordUrl={card.audioUrl} />
            </span>
          </div>
          <span className="font-ui text-lg italic text-primary dark:text-night-primary">{card.pinyin}</span>
          {card.isFlipped && (
            <span className="font-ui text-xl font-bold text-neutral-900 dark:text-night-text">
              {card.meaningVi}
            </span>
          )}
        </div>
      </div>

      <p className="font-ui text-center text-neutral-600 dark:text-night-muted">
        Nhấn vào thẻ để xem nghĩa
      </p>

      {/* The two answer decisions. Choosing either records the result and
          the parent auto-advances — there is no manual "next". */}
      <div className="flex gap-3">
        <button
          type="button"
          onClick={() => onEvaluate("wrong")}
          className="font-ui flex-1 rounded-2xl border border-error bg-error-bg px-5 py-4 text-lg font-bold text-neutral-900 transition-colors hover:brightness-95"
        >
          Không nhớ
        </button>
        <button
          type="button"
          onClick={() => onEvaluate("correct")}
          className="font-ui flex-1 rounded-2xl border border-success bg-success-bg px-5 py-4 text-lg font-bold text-neutral-900 transition-colors hover:brightness-95"
        >
          Đã nhớ
        </button>
      </div>
    </div>
  );
}
