"use client";

import clsx from "clsx";
import { Card } from "@/components/ui/Card";
import { CheckCircleIcon, LightbulbIcon } from "@/components/ui/icons";
import {
  canAdvanceCurrentWritingItem,
  type WritingSessionState,
} from "@/lib/practice/writingSession";

function WrongIcon({ className }: { className?: string }) {
  // Mirrors PracticeExerciseView's local WrongIcon exactly (not exported
  // from there, so duplicated here rather than reaching into that
  // Meaning/Character-only component for a private helper).
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

export function WritingExerciseView({
  session,
  onAnswerChange,
  onShowHint,
  onCheckAnswer,
  onDontRemember,
  onRetry,
  onNext,
}: {
  session: WritingSessionState;
  onAnswerChange: (value: string) => void;
  onShowHint: () => void;
  onCheckAnswer: () => void;
  onDontRemember: () => void;
  onRetry: () => void;
  onNext: () => void;
}) {
  const item = session.items[session.currentIndex];
  const total = session.items.length;

  if (!item) return null;

  const current = session.currentIndex + 1;
  const progressPercent = (current / total) * 100;
  const canSubmit = item.userAnswer.trim().length > 0;

  return (
    <div className="flex flex-col gap-4">
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

        <p className="text-center text-3xl font-bold text-primary sm:text-4xl">{item.meaningVi}</p>

        <div className="flex justify-end">
          <button
            type="button"
            onClick={onShowHint}
            disabled={item.feedbackVisible}
            className="inline-flex items-center gap-1.5 rounded-md border border-hint bg-hint-bg px-3 py-1.5 text-sm font-semibold text-hint transition-colors hover:brightness-95 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <LightbulbIcon className="h-4 w-4" />
            Gợi ý
          </button>
        </div>

        <input
          type="text"
          value={item.userAnswer}
          onChange={(event) => onAnswerChange(event.target.value)}
          disabled={item.feedbackVisible}
          placeholder="Nhập Tiếng Trung"
          className="w-full rounded-md border border-neutral-300 bg-white px-5 py-4 text-2xl text-neutral-900 outline-none focus:border-primary focus:ring-1 focus:ring-primary disabled:cursor-not-allowed disabled:opacity-70 dark:border-night-border dark:bg-night-input dark:text-night-text"
        />

        {item.hintShown && (
          <p className="mx-auto rounded-md border border-dashed border-hint bg-hint-bg px-4 py-2 text-lg italic text-hint">
            {item.pinyin}
          </p>
        )}

        {!item.feedbackVisible && (
          <div className="flex gap-3">
            <button
              type="button"
              onClick={onDontRemember}
              className="flex-1 rounded-md border border-error bg-error-bg px-5 py-4 text-lg font-bold text-neutral-900 transition-colors hover:brightness-95"
            >
              Không nhớ
            </button>
            <button
              type="button"
              onClick={onCheckAnswer}
              disabled={!canSubmit}
              className="flex-1 rounded-md border border-success bg-success-bg px-5 py-4 text-lg font-bold text-neutral-900 transition-colors hover:brightness-95 disabled:cursor-not-allowed disabled:opacity-50"
            >
              Kiểm tra đáp án
            </button>
          </div>
        )}
      </Card>

      {item.feedbackVisible && (
        <Card className="flex flex-col gap-4 p-6 sm:p-8">
          <div
            className={clsx(
              "flex items-start gap-3 rounded-card border p-4",
              item.result === "correct" ? "border-success bg-success-bg" : "border-error bg-error-bg"
            )}
          >
            {item.result === "correct" ? (
              <CheckCircleIcon className="h-8 w-8 shrink-0 text-success" />
            ) : (
              <WrongIcon className="h-8 w-8 shrink-0 text-error" />
            )}
            {/*
              Fixed dark text (no dark:text-* override) — same reasoning as
              PracticeExerciseView's feedback panel: this panel's background
              is always the light success/error tint regardless of theme.
            */}
            <div className="flex flex-col gap-1">
              <p
                className={clsx(
                  "text-lg font-bold",
                  item.result === "correct" ? "text-success" : "text-error"
                )}
              >
                {item.result === "correct" ? "Chính xác!" : "Chưa chính xác!"}
              </p>
              {item.result === "wrong" && item.userAnswer.trim().length > 0 && (
                <p className="text-neutral-800">Bạn nhập: {item.userAnswer}</p>
              )}
              {/*
                The correct answer for Writing is the CHINESE WORD (that is
                what the user is asked to type) — not the Vietnamese meaning
                already shown as the prompt above. Deliberate, see D5 report.
              */}
              <p className="text-neutral-800">Đáp án: {item.word}</p>
            </div>
          </div>

          <div className="flex gap-3">
            {item.result === "wrong" && (
              <button
                type="button"
                onClick={onRetry}
                className="flex-1 rounded-md border border-primary bg-white py-4 text-lg font-bold text-primary transition-colors hover:bg-primary-light dark:bg-night-surface dark:hover:bg-night-input"
              >
                Thử lại
              </button>
            )}
            <button
              type="button"
              onClick={onNext}
              disabled={!canAdvanceCurrentWritingItem(session)}
              className="flex-1 rounded-md bg-primary py-4 text-lg font-bold text-white transition-colors hover:bg-primary-dark disabled:cursor-not-allowed disabled:opacity-50"
            >
              Tiếp theo
            </button>
          </div>
        </Card>
      )}
    </div>
  );
}
