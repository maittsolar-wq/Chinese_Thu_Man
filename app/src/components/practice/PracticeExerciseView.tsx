"use client";

import clsx from "clsx";
import { CheckCircleIcon } from "@/components/ui/icons";
import type { ChoiceQuestion, ChoiceSessionState } from "@/lib/practice/session";

const OPTION_LETTERS = ["A", "B", "C", "D", "E", "F"];

function WrongIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" className={className}>
      <circle cx="12" cy="12" r="10" />
      <path
        d="M8.5 8.5l7 7M15.5 8.5l-7 7"
        fill="none"
        stroke="white"
        strokeWidth={2}
        strokeLinecap="round"
      />
    </svg>
  );
}

export function PracticeExerciseView({
  session,
  onAnswer,
  onNext,
}: {
  session: ChoiceSessionState;
  onAnswer: (option: string) => void;
  onNext: () => void;
}) {
  const question: ChoiceQuestion | undefined = session.questions[session.currentIndex];
  const total = session.questions.length;

  if (!question) return null;

  const current = session.currentIndex + 1;
  const progressPercent = (current / total) * 100;
  const hasScore = session.correctCount + session.wrongCount > 0;

  return (
    <div className="flex flex-col gap-4">
      {/* Visual-redesign pass: raw div (not shared `<Card>`) so the mockup
          panel radius (24px = `rounded-3xl`) and border (#E2E8F0) apply
          directly — same treatment as Practice Config / Practice Result. */}
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

        {session.practiceType === "character" ? (
          // Chọn chữ Hán: the prompt is the Vietnamese meaning, styled as
          // an accent heading — no secondary line (there's no pinyin for
          // a meaning prompt).
          <p className="font-ui text-center text-3xl font-bold text-primary sm:text-4xl">
            {question.promptPrimary}
          </p>
        ) : (
          // Chọn nghĩa: the prompt is the Chinese word, with pinyin below —
          // same font-cjk/italic-pinyin treatment as Vocabulary Detail's
          // hero, so the word looks like the same product everywhere.
          <div className="flex flex-col items-center gap-2">
            <p className="font-cjk text-5xl font-semibold text-neutral-900 dark:text-night-text">
              {question.promptPrimary}
            </p>
            {question.promptSecondary && (
              <p className="font-ui text-lg italic text-primary dark:text-night-primary">
                {question.promptSecondary}
              </p>
            )}
          </div>
        )}

        <div className="flex flex-col gap-3">
          {question.options.map((option, index) => {
            const isCorrectOption = option === question.correctAnswer;
            const isSelected = option === session.selectedAnswer;

            // Correct/wrong states use fixed light success/error surfaces
            // with fixed dark text — deliberately theme-independent, since
            // Tailwind can't reliably override an unconditional dark:text
            // class with a later-applied light-background state class
            // (cascade order between two same-specificity utilities isn't
            // guaranteed), which previously made this text unreadable in
            // dark mode.
            const colorClasses =
              session.isAnswered && isCorrectOption
                ? "border-success bg-success-bg text-neutral-900"
                : session.isAnswered && isSelected
                  ? "border-error bg-error-bg text-neutral-900"
                  : "border-[#E2E8F0] bg-white text-neutral-900 hover:bg-neutral-50 dark:border-night-border dark:bg-night-surface dark:text-night-text dark:hover:bg-night-input";

            return (
              <button
                key={option}
                type="button"
                disabled={session.isAnswered}
                onClick={() => onAnswer(option)}
                className={clsx(
                  "flex items-center gap-3 rounded-2xl border px-5 py-4 text-left font-semibold shadow-card transition-colors disabled:cursor-default",
                  session.practiceType === "character" ? "text-xl" : "text-base",
                  colorClasses
                )}
              >
                <span className="font-ui">{OPTION_LETTERS[index]}.</span>
                <span className={session.practiceType === "character" ? "font-cjk" : "font-ui"}>{option}</span>
              </button>
            );
          })}
        </div>

        {hasScore && (
          <div className="font-ui flex items-center gap-6 text-base font-bold">
            <span className="text-success">Đúng: {session.correctCount}</span>
            <span className="text-error">Sai: {session.wrongCount}</span>
          </div>
        )}

        {/* Feedback lives in the SAME card as the question rather than a
            second stacked Card (Phase 05: "avoid excessive containers") —
            a top border separates it instead. */}
        {session.isAnswered && (
          <div className="flex flex-col gap-4 border-t border-neutral-200 pt-6 dark:border-night-border">
            <div
              className={clsx(
                "flex items-start gap-3 rounded-2xl border p-4",
                session.isCorrect ? "border-success bg-success-bg" : "border-error bg-error-bg"
              )}
            >
              {session.isCorrect ? (
                <CheckCircleIcon className="h-8 w-8 shrink-0 text-success" />
              ) : (
                <WrongIcon className="h-8 w-8 shrink-0 text-error" />
              )}
              <div className="flex flex-col gap-1">
                <p
                  className={clsx(
                    "font-ui text-lg font-bold",
                    session.isCorrect ? "text-success" : "text-error"
                  )}
                >
                  {session.isCorrect ? "Chính xác!" : "Chưa chính xác!"}
                </p>
                {/*
                  Fixed dark text (no dark:text-* override) — this panel's
                  background is always the light success/error tint
                  regardless of site theme, same reasoning as the answer
                  options above.
                */}
                {!session.isCorrect && (
                  <p className="font-ui text-neutral-800">
                    Bạn chọn:{" "}
                    <span className={session.practiceType === "character" ? "font-cjk" : "font-ui"}>
                      {session.selectedAnswer}
                    </span>
                  </p>
                )}
                <p className="font-ui text-neutral-800">
                  Đáp án:{" "}
                  <span className={session.practiceType === "character" ? "font-cjk" : "font-ui"}>
                    {question.correctAnswer}
                  </span>
                </p>
              </div>
            </div>

            <button
              type="button"
              onClick={onNext}
              className="font-ui w-full rounded-[18px] bg-primary py-4 text-lg font-bold text-white transition-colors hover:bg-primary-dark"
            >
              Tiếp theo
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
