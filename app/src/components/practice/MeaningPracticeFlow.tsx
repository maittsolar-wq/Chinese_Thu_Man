"use client";

import { useCallback, useState } from "react";
import { PracticeConfigView } from "./PracticeConfigView";
import { PracticeExerciseView } from "./PracticeExerciseView";
import { PracticeResultView } from "./PracticeResultView";
import { EmptyState } from "@/components/ui/EmptyState";
import { LinkButton } from "@/components/ui/Button";
import { ArrowLeftIcon } from "@/components/ui/icons";
import { fetchPracticeVocabulary } from "@/lib/practice/actions";
import {
  pickUnusedVocabulary,
  isLearningCycleComplete,
  createMeaningSession,
  type PracticeVocabularyItem,
  type MeaningSessionState,
} from "@/lib/practice/session";
import type { PracticeConfigState, WordCountOption } from "@/lib/practice/types";
import type { HskLevel } from "@/lib/data/types";

type Phase = "config" | "loading" | "exercise" | "result" | "empty";

/**
 * Owns the full Chọn nghĩa flow (Configuration → Exercise → Result) as a
 * client-side state machine on the single /practice/meaning route — no
 * separate exercise/result routes are introduced, per instructions.
 *
 * The "learning cycle" (usedIds) tracks vocabulary already used for this
 * practiceType + hskLevel combination, scoped to this component's
 * lifetime (docs/PRACTICE §3, this phase's spec §33): it survives
 * Continue/Review within the flow but does not persist across a full
 * navigation away (e.g. "Về trang chủ" then back), matching "do not
 * persist unnecessary information".
 */
export function MeaningPracticeFlow() {
  const [phase, setPhase] = useState<Phase>("config");
  const [pool, setPool] = useState<PracticeVocabularyItem[]>([]);
  const [hskLevel, setHskLevel] = useState<HskLevel>(2);
  const [wordCount, setWordCount] = useState<WordCountOption>(20);
  const [usedIds, setUsedIds] = useState<Set<string>>(new Set());
  const [session, setSession] = useState<MeaningSessionState | null>(null);

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
      setSession(createMeaningSession(level, count, selected, nextPool));
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

  const handleAnswer = useCallback((option: string) => {
    setSession((prev) => {
      if (!prev || prev.isAnswered) return prev;
      const question = prev.questions[prev.currentIndex];
      if (!question) return prev;
      const isCorrect = option === question.correctAnswer;
      return {
        ...prev,
        selectedAnswer: option,
        isAnswered: true,
        isCorrect,
        correctCount: prev.correctCount + (isCorrect ? 1 : 0),
        wrongCount: prev.wrongCount + (isCorrect ? 0 : 1),
        wrongVocabularyIds: isCorrect
          ? prev.wrongVocabularyIds
          : [...prev.wrongVocabularyIds, question.vocabularyId],
      };
    });
  }, []);

  const handleNext = useCallback(() => {
    setSession((prev) => {
      if (!prev) return prev;
      const nextIndex = prev.currentIndex + 1;
      if (nextIndex >= prev.questions.length) {
        setPhase("result");
        return { ...prev, sessionCompleted: true };
      }
      return {
        ...prev,
        currentIndex: nextIndex,
        selectedAnswer: null,
        isAnswered: false,
        isCorrect: null,
      };
    });
  }, []);

  const handleContinue = useCallback(() => {
    startSession(pool, usedIds, wordCount, hskLevel);
  }, [pool, usedIds, wordCount, hskLevel, startSession]);

  const handleReviewWrong = useCallback(() => {
    if (!session) return;
    const wrongIds = new Set(session.wrongVocabularyIds);
    const reviewItems = pool.filter((item) => wrongIds.has(item.id));
    // Review does not touch `usedIds`: these vocabulary items are already
    // marked used from the session that just completed, and reviewing
    // them must not affect learning-cycle completion (spec §17).
    setSession(createMeaningSession(hskLevel, wordCount, reviewItems, pool));
    setPhase("exercise");
  }, [session, pool, hskLevel, wordCount]);

  const handleRestart = useCallback(() => {
    startSession(pool, new Set(), wordCount, hskLevel);
  }, [pool, wordCount, hskLevel, startSession]);

  if (phase === "config") {
    return <PracticeConfigView practiceType="meaning" onStart={handleStart} />;
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
    return <PracticeExerciseView session={session} onAnswer={handleAnswer} onNext={handleNext} />;
  }

  if (phase === "result" && session) {
    return (
      <PracticeResultView
        hskLevel={hskLevel}
        actualCount={session.questions.length}
        correctCount={session.correctCount}
        wrongCount={session.wrongCount}
        isCycleComplete={isLearningCycleComplete(pool, usedIds)}
        onReviewWrong={handleReviewWrong}
        onContinue={handleContinue}
        onRestart={handleRestart}
      />
    );
  }

  return null;
}
