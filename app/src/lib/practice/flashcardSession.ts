import type { HskLevel } from "@/lib/data/types";
import type { WordCountOption } from "./types";
import type { PracticeVocabularyItem } from "./session";

/**
 * Flashcard domain/session logic (D4.1) — UI is implemented separately in
 * D4.2; this file is pure data/state, no React.
 *
 * Flashcard is deliberately NOT built on `PracticeSessionState<TQuestion>`
 * (session.ts): that generic shape assumes a single "current answer"
 * (`selectedAnswer`/`isAnswered`/`isCorrect`) that gets reset every time
 * the session advances — correct for Chọn nghĩa/Chọn chữ Hán, which never
 * go backward. Flashcard explicitly requires Previous/Next navigation
 * where an already-evaluated card's result must survive revisiting it,
 * so each card carries its OWN persistent `result` (and `isFlipped`)
 * inside the `cards` array instead of one transient session-level field.
 *
 * What IS reused unchanged from session.ts: `PracticeVocabularyItem` (the
 * same vocabulary shape fetched via actions.ts's `fetchPracticeVocabulary`,
 * itself unmodified) and the learning-cycle helpers `pickUnusedVocabulary`
 * / `isLearningCycleComplete`, which already operate generically on
 * `PracticeVocabularyItem[]` + a `Set<string>` of used ids — nothing about
 * them is multiple-choice-specific, so Flashcard calls them directly
 * (see session.ts) rather than duplicating vocabulary-selection or
 * completion logic here.
 */

export type FlashcardResult = "unanswered" | "correct" | "wrong";

export interface FlashcardItem {
  vocabularyId: string;
  word: string;
  pinyin: string;
  meaningVi: string;
  isFlipped: boolean;
  result: FlashcardResult;
}

export interface FlashcardSessionState {
  practiceType: "flashcard";
  hskLevel: HskLevel;
  requestedCount: WordCountOption;
  cards: FlashcardItem[];
  currentIndex: number;
  sessionCompleted: boolean;
}

export function createFlashcardSession(
  hskLevel: HskLevel,
  requestedCount: WordCountOption,
  selected: PracticeVocabularyItem[]
): FlashcardSessionState {
  return {
    practiceType: "flashcard",
    hskLevel,
    requestedCount,
    cards: selected.map((item) => ({
      vocabularyId: item.id,
      word: item.word,
      pinyin: item.pinyin,
      meaningVi: item.meaningVi,
      isFlipped: false,
      result: "unanswered",
    })),
    currentIndex: 0,
    sessionCompleted: false,
  };
}

/** Flips ONLY the currently-shown card. Never touches `result`. */
export function flipCurrentFlashcard(session: FlashcardSessionState): FlashcardSessionState {
  return {
    ...session,
    cards: session.cards.map((card, index) =>
      index === session.currentIndex ? { ...card, isFlipped: !card.isFlipped } : card
    ),
  };
}

/**
 * Records "Đã nhớ" (correct) / "Không nhớ" (wrong) for the current card,
 * matched by vocabulary identity rather than array index. Re-evaluating
 * an already-answered card (after navigating back to it) OVERWRITES that
 * one entry — it can never create a duplicate or double-count, because
 * every derived score (see below) is computed fresh from `cards` each
 * time, never accumulated incrementally.
 */
export function evaluateCurrentFlashcard(
  session: FlashcardSessionState,
  result: "correct" | "wrong"
): FlashcardSessionState {
  const current = session.cards[session.currentIndex];
  if (!current) return session;

  const cards = session.cards.map((card) =>
    card.vocabularyId === current.vocabularyId ? { ...card, result } : card
  );

  return { ...session, cards, sessionCompleted: isFlashcardSessionComplete(cards) };
}

export function canGoToPreviousFlashcard(session: FlashcardSessionState): boolean {
  return session.currentIndex > 0;
}

export function canGoToNextFlashcard(session: FlashcardSessionState): boolean {
  return session.currentIndex < session.cards.length - 1;
}

export function goToPreviousFlashcard(session: FlashcardSessionState): FlashcardSessionState {
  if (!canGoToPreviousFlashcard(session)) return session;
  return { ...session, currentIndex: session.currentIndex - 1 };
}

export function goToNextFlashcard(session: FlashcardSessionState): FlashcardSessionState {
  if (!canGoToNextFlashcard(session)) return session;
  return { ...session, currentIndex: session.currentIndex + 1 };
}

export function isFlashcardSessionComplete(cards: FlashcardItem[]): boolean {
  return cards.length > 0 && cards.every((card) => card.result !== "unanswered");
}

/** Đúng/Sai counts — always derived from `cards`, so a card that is
 *  re-evaluated (e.g. wrong → correct after going back) is never counted
 *  under both results and never counted twice. */
export function countFlashcardResult(cards: FlashcardItem[], result: FlashcardResult): number {
  return cards.filter((card) => card.result === result).length;
}

/** correct / answered * 100, rounded; 0 when nothing has been evaluated yet. */
export function flashcardAccuracy(cards: FlashcardItem[]): number {
  const answered = cards.filter((card) => card.result !== "unanswered").length;
  if (answered === 0) return 0;
  const correct = cards.filter((card) => card.result === "correct").length;
  return Math.round((correct / answered) * 100);
}

/** vocabularyIds currently marked wrong — feeds "Ôn lại X câu sai". */
export function wrongFlashcardVocabularyIds(cards: FlashcardItem[]): string[] {
  return cards.filter((card) => card.result === "wrong").map((card) => card.vocabularyId);
}
