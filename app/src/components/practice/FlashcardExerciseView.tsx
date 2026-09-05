"use client";

import clsx from "clsx";
import { Card } from "@/components/ui/Card";
import { ChevronLeftIcon, ChevronRightIcon, SpeakerIcon } from "@/components/ui/icons";
import {
  canGoToNextFlashcard,
  canGoToPreviousFlashcard,
  isFlashcardSessionComplete,
  type FlashcardSessionState,
} from "@/lib/practice/flashcardSession";

/**
 * Exercise screen for Flashcard (D4.2). Deliberately a separate component
 * from PracticeExerciseView rather than a shared/branching one: Flashcard's
 * interaction model (flip a card, evaluate independently of navigation,
 * freely move Previous/Next) is materially different from the
 * single-current-answer multiple-choice flow that PracticeExerciseView
 * renders, and forcing them into one component would risk regressing
 * Meaning/Character for no benefit — see FlashcardPracticeFlow.tsx's header
 * comment for the full reasoning.
 *
 * Pure presentation: every interaction (flip / evaluate / navigate) is
 * delegated to the callbacks, which the parent maps onto the D4.1 domain
 * functions in flashcardSession.ts. No score/evaluation state is computed
 * or duplicated here — `session.cards` (built by that module) is read
 * directly for what to render.
 */
export function FlashcardExerciseView({
  session,
  onFlip,
  onEvaluate,
  onPrevious,
  onNext,
}: {
  session: FlashcardSessionState;
  onFlip: () => void;
  onEvaluate: (result: "correct" | "wrong") => void;
  onPrevious: () => void;
  onNext: () => void;
}) {
  const card = session.cards[session.currentIndex];
  const total = session.cards.length;

  if (!card) return null;

  const current = session.currentIndex + 1;
  const progressPercent = (current / total) * 100;

  const canPrevious = canGoToPreviousFlashcard(session);
  // At the last card, "Next" instead means "finish" — only reachable once
  // every card in the session has been evaluated (never let the user
  // wander past the end, or complete the session, with cards still
  // unanswered). Before the last card, Next is a plain navigation step.
  const canNext = canGoToNextFlashcard(session) || isFlashcardSessionComplete(session.cards);

  return (
    <Card className="flex flex-col gap-6 p-6 sm:p-8">
      <div className="flex flex-col gap-2">
        <p className="text-center text-lg font-bold text-neutral-900 dark:text-night-text">
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

      <div className="flex items-center justify-center gap-3 sm:gap-6">
        <button
          type="button"
          aria-label="Thẻ trước"
          disabled={!canPrevious}
          onClick={onPrevious}
          className="shrink-0 rounded-full p-2 text-neutral-700 transition-colors hover:bg-neutral-100 disabled:cursor-not-allowed disabled:opacity-30 dark:text-night-text dark:hover:bg-night-input"
        >
          <ChevronLeftIcon className="h-8 w-8" />
        </button>

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
          className="flex min-h-[220px] w-full max-w-md cursor-pointer flex-col items-center justify-center gap-3 rounded-card border border-neutral-200 bg-white p-8 text-center shadow-card transition-colors dark:border-night-border dark:bg-night-surface"
        >
          <div className="flex items-center gap-3">
            <span className="text-5xl font-bold text-neutral-900 dark:text-night-text">
              {card.word}
            </span>
            {/*
              UI-009 polish: no audio/TTS mechanism exists anywhere in the
              project yet, so this stays a non-functional placeholder — but
              `disabled` (rather than a plain button with a no-op onClick)
              makes that honest for every input method, not just mouse
              hover: it's removed from the tab order, announced by screen
              readers as unavailable, and gets the same
              `disabled:cursor-not-allowed disabled:opacity-50` treatment
              Button.tsx already uses for disabled controls elsewhere. A
              disabled button fires no click event at all, so it can no
              longer bubble up to the card's flip handler — the
              `stopPropagation` this previously needed for that is gone.
            */}
            <button
              type="button"
              disabled
              aria-label="Nghe phát âm (chưa khả dụng)"
              title="Nghe phát âm (chưa khả dụng)"
              className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary text-white disabled:cursor-not-allowed disabled:opacity-50"
            >
              <SpeakerIcon className="h-4 w-4" />
            </button>
          </div>
          <span className="text-lg italic text-primary">{card.pinyin}</span>
          {card.isFlipped && (
            <span className="text-xl font-bold text-neutral-900 dark:text-night-text">
              {card.meaningVi}
            </span>
          )}
        </div>

        <button
          type="button"
          aria-label="Thẻ tiếp theo"
          disabled={!canNext}
          onClick={onNext}
          className="shrink-0 rounded-full p-2 text-neutral-700 transition-colors hover:bg-neutral-100 disabled:cursor-not-allowed disabled:opacity-30 dark:text-night-text dark:hover:bg-night-input"
        >
          <ChevronRightIcon className="h-8 w-8" />
        </button>
      </div>

      <p className="text-center text-neutral-600 dark:text-night-muted">
        Nhấn vào thẻ để xem nghĩa
      </p>

      <div className="flex gap-3">
        <button
          type="button"
          onClick={() => onEvaluate("wrong")}
          className={clsx(
            "flex-1 rounded-md border px-5 py-4 text-lg font-bold transition-colors",
            card.result === "wrong"
              ? "border-error bg-error text-white"
              : clsx(
                  "border-error bg-error-bg text-neutral-900 hover:brightness-95",
                  card.result === "correct" && "opacity-40"
                )
          )}
        >
          Không nhớ
        </button>
        <button
          type="button"
          onClick={() => onEvaluate("correct")}
          className={clsx(
            "flex-1 rounded-md border px-5 py-4 text-lg font-bold transition-colors",
            card.result === "correct"
              ? "border-success bg-success text-white"
              : clsx(
                  "border-success bg-success-bg text-neutral-900 hover:brightness-95",
                  card.result === "wrong" && "opacity-40"
                )
          )}
        >
          Đã nhớ
        </button>
      </div>
    </Card>
  );
}
