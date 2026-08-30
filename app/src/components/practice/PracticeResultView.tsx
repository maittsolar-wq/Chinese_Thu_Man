"use client";

import { Card } from "@/components/ui/Card";
import { Button, LinkButton } from "@/components/ui/Button";
import type { HskLevel } from "@/lib/data/types";

/**
 * ONE reusable Result screen (docs/PRACTICE §11, this phase's spec §12)
 * covering all three states via conditional rendering:
 *   - Normal (mid-cycle): "Tuyệt vời" + optional "Luyện tập tiếp"
 *   - Completion, wrong > 0: "Hoàn thành HSK N!" + "Học lại từ đầu"
 *   - Completion, wrong === 0 (perfect): same, no "Ôn lại 0 câu sai"
 */
export function PracticeResultView({
  hskLevel,
  actualCount,
  correctCount,
  wrongCount,
  isCycleComplete,
  onReviewWrong,
  onContinue,
  onRestart,
}: {
  hskLevel: HskLevel;
  actualCount: number;
  correctCount: number;
  wrongCount: number;
  isCycleComplete: boolean;
  onReviewWrong: () => void;
  onContinue: () => void;
  onRestart: () => void;
}) {
  const accuracy = actualCount > 0 ? Math.round((correctCount / actualCount) * 100) : 0;

  return (
    <Card className="flex flex-col items-center gap-4 p-6 text-center sm:p-8">
      <h2 className="text-2xl font-bold text-primary">Kết quả luyện tập</h2>

      <span className="text-7xl" role="img" aria-label="Ăn mừng">
        🎉
      </span>

      {isCycleComplete ? (
        <div className="flex flex-col gap-1">
          <p className="text-2xl font-bold text-neutral-900 dark:text-night-text">
            Hoàn thành HSK {hskLevel}!
          </p>
          <p className="text-neutral-600 dark:text-night-muted">
            Bạn đã học hết toàn bộ từ vựng HSK {hskLevel}
          </p>
        </div>
      ) : (
        <div className="flex flex-col gap-1">
          <p className="text-2xl font-bold text-neutral-900 dark:text-night-text">Tuyệt vời</p>
          <p className="text-neutral-600 dark:text-night-muted">
            Bạn đã hoàn thành bài tập luyện tập
          </p>
        </div>
      )}

      <p className="text-3xl font-bold text-neutral-900 dark:text-night-text">
        {correctCount}/{actualCount} câu
      </p>

      <div className="grid w-full grid-cols-3 divide-x divide-neutral-200 rounded-card border border-primary dark:divide-night-border">
        <div className="flex flex-col gap-1 p-4">
          <span className="text-sm font-medium text-success">Đúng</span>
          <span className="text-2xl font-bold text-success">{correctCount}</span>
        </div>
        <div className="flex flex-col gap-1 p-4">
          <span className="text-sm font-medium text-error">Sai</span>
          <span className="text-2xl font-bold text-error">{wrongCount}</span>
        </div>
        <div className="flex flex-col gap-1 p-4">
          <span className="text-sm font-medium text-primary">Độ chính xác</span>
          <span className="text-2xl font-bold text-primary">{accuracy}%</span>
        </div>
      </div>

      <div className="flex w-full flex-col gap-3">
        {wrongCount > 0 && (
          <Button type="button" onClick={onReviewWrong} className="w-full py-4 text-lg">
            Ôn lại {wrongCount} câu sai
          </Button>
        )}

        {isCycleComplete ? (
          <Button
            type="button"
            variant="secondary"
            onClick={onRestart}
            className="w-full py-4 text-lg"
          >
            Học lại từ đầu
          </Button>
        ) : (
          <Button
            type="button"
            variant="secondary"
            onClick={onContinue}
            className="w-full py-4 text-lg"
          >
            Luyện tập tiếp
          </Button>
        )}

        <LinkButton href="/" variant="neutral" className="w-full py-4 text-lg">
          Về trang chủ
        </LinkButton>
      </div>
    </Card>
  );
}
