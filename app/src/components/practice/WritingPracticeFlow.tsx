"use client";

import { useCallback, useState } from "react";
import { PracticeConfigView } from "./PracticeConfigView";
import { WritingExerciseView } from "./WritingExerciseView";
import { PracticeResultView } from "./PracticeResultView";
import { PracticeExitConfirmDialog } from "./PracticeExitConfirmDialog";
import { EmptyState } from "@/components/ui/EmptyState";
import { Button, LinkButton } from "@/components/ui/Button";
import { ArrowLeftIcon } from "@/components/ui/icons";
import { fetchPracticeVocabulary } from "@/lib/practice/actions";
import { pickUnusedVocabulary, isLearningCycleComplete, type PracticeVocabularyItem } from "@/lib/practice/session";
import {
  createWritingSession,
  updateCurrentWritingAnswer,
  showHintForCurrentWriting,
  evaluateCurrentWritingAnswer,
  markCurrentWritingDontRemember,
  retryCurrentWriting,
  canAdvanceCurrentWritingItem,
  canGoToNextWritingItem,
  goToNextWritingItem,
  isWritingSessionComplete,
  countWritingResult,
  wrongWritingVocabularyIds,
  type WritingSessionState,
} from "@/lib/practice/writingSession";
import type { PracticeConfigState, WordCountOption } from "@/lib/practice/types";
import type { HskLevel } from "@/lib/data/types";

type Phase = "config" | "loading" | "exercise" | "result" | "empty";

/**
 * Owns the Configuration → Exercise → Result flow for Writing (D5),
 * structurally parallel to ChoicePracticeFlow (D2/D3) and
 * FlashcardPracticeFlow (D4.2) — same pool/hskLevel/wordCount/usedIds/
 * session state, same startSession/handleContinue/handleReviewWrong/
 * handleRestart shape — but calling the D5 writingSession.ts functions,
 * for the same reason Flashcard got its own sibling flow rather than
 * branching into ChoicePracticeFlow: Writing's interaction model (typed
 * input, hint reveal, wrong-then-retry-same-item) doesn't fit either
 * existing session shape without distorting it, so a focused component
 * avoids risking Meaning/Character/Flashcard regressions.
 *
 * Every state transition below is a direct call into writingSession.ts —
 * no second scoring/evaluation system is implemented here.
 */
export function WritingPracticeFlow() {
  const [phase, setPhase] = useState<Phase>("config");
  const [pool, setPool] = useState<PracticeVocabularyItem[]>([]);
  const [hskLevel, setHskLevel] = useState<HskLevel>(2);
  const [wordCount, setWordCount] = useState<WordCountOption>(20);
  const [usedIds, setUsedIds] = useState<Set<string>>(new Set());
  const [session, setSession] = useState<WritingSessionState | null>(null);
  const [isExitConfirmOpen, setIsExitConfirmOpen] = useState(false);

  const startSession = useCallback(
    (
      nextPool: PracticeVocabularyItem[],
      used: Set<string>,
      count: WordCountOption,
      level: HskLevel
    ) => {
      const selected = pickUnusedVocabulary(nextPool, used, count);
      const newUsed = new Set(used);
      for (const item of selected) newUsed.add(item.id);
      setUsedIds(newUsed);
      setSession(createWritingSession(level, count, selected));
      setPhase("exercise");
    },
    []
  );

  const handleStart = useCallback(
    async (config: PracticeConfigState) => {
      setPhase("loading");
      setHskLevel(config.hskLevel);
      setWordCount(config.wordCount);

      const fetched = await fetchPracticeVocabulary(config.hskLevel);

      if (fetched.length === 0) {
        setPhase("empty");
        return;
      }

      setPool(fetched);
      startSession(fetched, new Set(), config.wordCount, config.hskLevel);
    },
    [startSession]
  );

  const handleAnswerChange = useCallback((value: string) => {
    setSession((prev) => (prev ? updateCurrentWritingAnswer(prev, value) : prev));
  }, []);

  const handleShowHint = useCallback(() => {
    setSession((prev) => (prev ? showHintForCurrentWriting(prev) : prev));
  }, []);

  const handleCheckAnswer = useCallback(() => {
    setSession((prev) => (prev ? evaluateCurrentWritingAnswer(prev) : prev));
  }, []);

  const handleDontRemember = useCallback(() => {
    setSession((prev) => (prev ? markCurrentWritingDontRemember(prev) : prev));
  }, []);

  const handleRetry = useCallback(() => {
    setSession((prev) => (prev ? retryCurrentWriting(prev) : prev));
  }, []);

  const handleNext = useCallback(() => {
    setSession((prev) => {
      if (!prev) return prev;
      // Mirrors the "Tiếp theo" button's own disabled condition: never
      // advance (or finish) past an item that hasn't been judged yet.
      if (!canAdvanceCurrentWritingItem(prev)) return prev;
      if (canGoToNextWritingItem(prev)) return goToNextWritingItem(prev);
      if (isWritingSessionComplete(prev.items)) setPhase("result");
      return prev;
    });
  }, []);

  const handleContinue = useCallback(() => {
    startSession(pool, usedIds, wordCount, hskLevel);
  }, [pool, usedIds, wordCount, hskLevel, startSession]);

  const handleReviewWrong = useCallback(() => {
    if (!session) return;
    const wrongIds = new Set(wrongWritingVocabularyIds(session.items));
    const reviewItems = pool.filter((item) => wrongIds.has(item.id));
    // Review does not touch `usedIds`: these vocabulary items are already
    // marked used from the session that just completed, and reviewing
    // them must not affect learning-cycle completion.
    setSession(createWritingSession(hskLevel, wordCount, reviewItems));
    setPhase("exercise");
  }, [session, pool, hskLevel, wordCount]);

  const handleRestart = useCallback(() => {
    startSession(pool, new Set(), wordCount, hskLevel);
  }, [pool, wordCount, hskLevel, startSession]);

  const handleRequestExit = useCallback(() => setIsExitConfirmOpen(true), []);
  const handleStayInSession = useCallback(() => setIsExitConfirmOpen(false), []);
  // Same abandon semantics as ChoicePracticeFlow's handleExitSession — see
  // that comment. No result screen, no score/usedIds mutation, no
  // persistence; the next "Bắt đầu luyện tập" from Configuration always
  // starts a brand-new session regardless of what's left in this state.
  const handleExitSession = useCallback(() => {
    setIsExitConfirmOpen(false);
    setSession(null);
    setPhase("config");
  }, []);

  if (phase === "config") {
    return <PracticeConfigView practiceType="writing" onStart={handleStart} />;
  }

  if (phase === "loading") {
    return (
      <div className="flex flex-col gap-6">
        <LinkButton href="/" className="w-fit">
          <ArrowLeftIcon className="h-4 w-4" />
          Quay lại
        </LinkButton>
        <EmptyState title="Đang chuẩn bị bài luyện tập..." />
      </div>
    );
  }

  if (phase === "empty") {
    return (
      <div className="flex flex-col gap-6">
        <LinkButton href="/" className="w-fit">
          <ArrowLeftIcon className="h-4 w-4" />
          Quay lại
        </LinkButton>
        <EmptyState
          title="Không có từ vựng cho cấp độ này."
          description="Vui lòng quay lại và chọn cấp độ HSK khác."
        />
      </div>
    );
  }

  if (phase === "exercise" && session) {
    return (
      <div className="flex flex-col gap-4">
        <Button variant="primary" className="w-fit" onClick={handleRequestExit}>
          <ArrowLeftIcon className="h-4 w-4" />
          Quay lại
        </Button>
        <WritingExerciseView
          session={session}
          onAnswerChange={handleAnswerChange}
          onShowHint={handleShowHint}
          onCheckAnswer={handleCheckAnswer}
          onDontRemember={handleDontRemember}
          onRetry={handleRetry}
          onNext={handleNext}
        />
        {isExitConfirmOpen && (
          <PracticeExitConfirmDialog onStay={handleStayInSession} onExit={handleExitSession} />
        )}
      </div>
    );
  }

  if (phase === "result" && session) {
    return (
      <PracticeResultView
        hskLevel={hskLevel}
        actualCount={session.items.length}
        correctCount={countWritingResult(session.items, "correct")}
        wrongCount={countWritingResult(session.items, "wrong")}
        isCycleComplete={isLearningCycleComplete(pool, usedIds)}
        onReviewWrong={handleReviewWrong}
        onContinue={handleContinue}
        onRestart={handleRestart}
      />
    );
  }

  return null;
}
