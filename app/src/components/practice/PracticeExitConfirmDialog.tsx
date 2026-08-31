"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/Button";

/**
 * Shared mid-session "exit practice?" confirmation (P2), reused by all
 * three Practice flow owners — ChoicePracticeFlow (Meaning/Character),
 * FlashcardPracticeFlow, WritingPracticeFlow — rather than duplicated
 * three times. The dialog itself carries no session-shape awareness;
 * each flow decides what "abandon" means for its own state (see each
 * flow's `handleExit`) and just supplies `onStay`/`onExit`.
 *
 * Modeled directly on DictionarySearchPopup's overlay+panel modal
 * pattern (fixed dimmed overlay, centered panel, stopPropagation on the
 * panel, Escape closes, body scroll locked while open) — the only
 * existing modal in the codebase — rather than inventing a new dialog
 * primitive.
 */
export function PracticeExitConfirmDialog({
  onStay,
  onExit,
}: {
  onStay: () => void;
  onExit: () => void;
}) {
  useEffect(() => {
    function handleKey(event: KeyboardEvent) {
      if (event.key === "Escape") onStay();
    }
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [onStay]);

  useEffect(() => {
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previous;
    };
  }, []);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <button
        type="button"
        aria-label="Đóng"
        onClick={onStay}
        className="fixed inset-0 cursor-default bg-neutral-900/40 dark:bg-black/60"
      />

      <div
        role="dialog"
        aria-modal="true"
        aria-label="Xác nhận thoát bài luyện tập"
        onClick={(event) => event.stopPropagation()}
        className="relative z-10 flex w-full max-w-sm flex-col gap-4 rounded-card border border-neutral-200 bg-white p-6 shadow-card dark:border-night-border dark:bg-night-surface"
      >
        <div className="flex flex-col gap-1">
          <h2 className="text-lg font-bold text-neutral-900 dark:text-night-text">
            Bạn muốn thoát bài luyện tập?
          </h2>
          <p className="text-sm text-neutral-600 dark:text-night-muted">
            Tiến độ hiện tại sẽ không được lưu.
          </p>
        </div>

        <div className="flex gap-3">
          <Button type="button" variant="primary" onClick={onStay} className="flex-1">
            Ở lại
          </Button>
          <Button type="button" variant="neutral" onClick={onExit} className="flex-1">
            Thoát
          </Button>
        </div>
      </div>
    </div>
  );
}
