"use client";

import { Suspense, useCallback, useEffect, useRef, useState } from "react";
import { PracticeConfigView } from "./PracticeConfigView";
import { FlashcardExerciseView } from "./FlashcardExerciseView";
import { PracticeResultView } from "./PracticeResultView";
import { PracticeExitConfirmDialog } from "./PracticeExitConfirmDialog";
import { PracticeStatusScreen } from "./PracticeStatusScreen";
import { Button } from "@/components/ui/Button";
import { ArrowLeftIcon } from "@/components/ui/icons";
import { fetchPracticeVocabulary } from "@/lib/practice/actions";
import { pickUnusedVocabulary, isLearningCycleComplete, type PracticeVocabularyItem } from "@/lib/practice/session";
import {
  createFlashcardSession,
  flipCurrentFlashcard,
  evaluateCurrentFlashcard,
  goToNextFlashcard,
  canGoToNextFlashcard,
  countFlashcardResult,
  wrongFlashcardVocabularyIds,
  type FlashcardSessionState,
} from "@/lib/practice/flashcardSession";
import type { PracticeConfigState, WordCountOption } from "@/lib/practice/types";
import type { HskLevel } from "@/lib/data/types";

type Phase = "config" | "loading" | "exercise" | "result" | "empty";

/**
 * Owns the Configuration → Exercise → Result flow for Flashcard (D4.2),
 * mirroring ChoicePracticeFlow's role for Meaning/Character on the same
 * single-route client-state-machine pattern — but built as its own
 * component rather than a third `SESSION_FACTORIES` entry there.
 *
 * Why not fold Flashcard into ChoicePracticeFlow: that component's
 * handlers (handleAnswer/handleNext) are written directly against
 * `ChoiceSessionState`'s single-current-answer fields (`selectedAnswer`/
 * `isAnswered`/`isCorrect`, reset every advance). Flashcard's session
 * (flashcardSession.ts, D4.1) deliberately has none of those — each card
 * carries its own persistent `result`, and Previous/Next never resets
 * anything. Bending ChoicePracticeFlow to also branch on a structurally
 * different session type risked exactly the kind of accidental
 * Meaning/Character regression this project's phases have consistently
 * guarded against; a focused sibling component with the same overall shape
 * (config/loading/exercise/result/empty phases, pool/usedIds/session
 * state, startSession/handleContinue/handleReviewWrong/handleRestart) is
 * both safer and, since the actual card/scoring logic all lives in
 * flashcardSession.ts, no more duplication than ChoicePracticeFlow itself
 * has relative to session.ts.
 *
 * Every state transition below is a direct call into the D4.1 domain
 * functions — no second scoring/evaluation system is implemented here.
 */
export function FlashcardPracticeFlow() {
  const [phase, setPhase] = useState<Phase>("config");
  const [pool, setPool] = useState<PracticeVocabularyItem[]>([]);
  const [hskLevel, setHskLevel] = useState<HskLevel>(2);
  const [wordCount, setWordCount] = useState<WordCountOption>(20);
  const [usedIds, setUsedIds] = useState<Set<string>>(new Set());
  const [session, setSession] = useState<FlashcardSessionState | null>(null);
  const [isExitConfirmOpen, setIsExitConfirmOpen] = useState(false);

  // Synchronous double-submit guard: an answer click sets this true, and it
  // stays true across the brief window between the click and the next card
  // (or the Result screen) rendering, so a rapid second click can't answer
  // a card the user hasn't seen yet. Same idea as PronunciationButton's
  // isBusyRef. The effect below clears it the moment the visible card /
  // phase actually changes.
  const isAdvancingRef = useRef(false);
  const currentCardIndex = session?.currentIndex;
  useEffect(() => {
    isAdvancingRef.current = false;
  }, [currentCardIndex, phase]);

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
      setSession(createFlashcardSession(level, count, selected));
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

  const handleFlip = useCallback(() => {
    setSession((prev) => (prev ? flipCurrentFlashcard(prev) : prev));
  }, []);

  /**
   * "Đã nhớ" → correct, "Không nhớ" → wrong. One call does all three of:
   * record the answer (`evaluateCurrentFlashcard` — the existing scoring
   * mechanism), then either auto-advance to the next card
   * (`goToNextFlashcard`) or, on the last card, finish: the answer is
   * already in `session.cards`, `phase` flips to "result", and the
   * existing `phase === "result"` branch reads counts/completion straight
   * off that same session. No manual "Next" anywhere.
   */
  const handleEvaluate = useCallback((result: "correct" | "wrong") => {
    if (isAdvancingRef.current) return;
    isAdvancingRef.current = true;
    setSession((prev) => {
      if (!prev) return prev;
      const evaluated = evaluateCurrentFlashcard(prev, result);
      if (canGoToNextFlashcard(evaluated)) return goToNextFlashcard(evaluated);
      // Last card just answered → every card is now evaluated → Result.
      setPhase("result");
      return evaluated;
    });
  }, []);

  const handleContinue = useCallback(() => {
    startSession(pool, usedIds, wordCount, hskLevel);
  }, [pool, usedIds, wordCount, hskLevel, startSession]);

  const handleReviewWrong = useCallback(() => {
    if (!session) return;
    const wrongIds = new Set(wrongFlashcardVocabularyIds(session.cards));
    const reviewItems = pool.filter((item) => wrongIds.has(item.id));
    // Review does not touch `usedIds`: these vocabulary items are already
    // marked used from the session that just completed, and reviewing
    // them must not affect learning-cycle completion (D4.1 §"review
    // isolation").
    setSession(createFlashcardSession(hskLevel, wordCount, reviewItems));
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
    // Suspense: see ChoicePracticeFlow's identical comment — required for
    // PracticeConfigView's useSearchParams() on this statically-rendered
    // route.
    return (
      <Suspense fallback={null}>
        <PracticeConfigView practiceType="flashcard" onStart={handleStart} />
      </Suspense>
    );
  }

  if (phase === "loading") {
    return <PracticeStatusScreen variant="loading" />;
  }

  if (phase === "empty") {
    return <PracticeStatusScreen variant="empty" />;
  }

  if (phase === "exercise" && session) {
    return (
      <div className="flex flex-col gap-4">
        <Button
          variant="neutral"
          onClick={handleRequestExit}
          className="font-ui h-12 w-fit rounded-xl px-6"
        >
          <ArrowLeftIcon className="h-4 w-4" />
          Quay lại
        </Button>
        <FlashcardExerciseView
          session={session}
          onFlip={handleFlip}
          onEvaluate={handleEvaluate}
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
        practiceType="flashcard"
        hskLevel={hskLevel}
        actualCount={session.cards.length}
        correctCount={countFlashcardResult(session.cards, "correct")}
        wrongCount={countFlashcardResult(session.cards, "wrong")}
        isCycleComplete={isLearningCycleComplete(pool, usedIds)}
        onReviewWrong={handleReviewWrong}
        onContinue={handleContinue}
        onRestart={handleRestart}
        onBack={handleExitSession}
      />
    );
  }

  return null;
}
