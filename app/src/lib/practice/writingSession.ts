import type { HskLevel } from "@/lib/data/types";
import type { WordCountOption } from "./types";
import type { PracticeVocabularyItem } from "./session";

/**
 * Writing domain/session logic (D5) — UI lives in WritingExerciseView.tsx /
 * WritingPracticeFlow.tsx; this file is pure data/state, no React, in the
 * same spirit as flashcardSession.ts (D4.1).
 *
 * Writing is neither a ChoiceQuestion flow (session.ts) nor a Flashcard
 * flow (flashcardSession.ts): the user types the Chinese word for a given
 * Vietnamese meaning, can reveal a Pinyin hint first, can submit a wrong
 * answer and retry the SAME item, or give up via "Không nhớ". None of
 * that fits `PracticeSessionState<TQuestion>`'s single-current-answer
 * reset-on-advance shape, nor Flashcard's flip/evaluate-only-two-outcomes
 * shape — hence its own focused `WritingItem`/`WritingSessionState`.
 *
 * What IS reused unchanged from session.ts: `PracticeVocabularyItem` and
 * the learning-cycle helpers `pickUnusedVocabulary` / `isLearningCycleComplete`
 * (called directly by WritingPracticeFlow, exactly as Choice/Flashcard do)
 * — nothing about vocabulary selection or cycle completion is reimplemented
 * here.
 *
 * Like Flashcard, every score is DERIVED from `items` on each read rather
 * than accumulated incrementally, and every mutation matches the current
 * item by `vocabularyId` rather than array index — the property that makes
 * retrying a wrong answer overwrite that one item's result instead of
 * double-counting it.
 */

export type WritingResult = "unanswered" | "correct" | "wrong";

export interface WritingItem {
  vocabularyId: string;
  /** The Vietnamese meaning shown as the prompt. */
  meaningVi: string;
  /** The expected Chinese word — never shown until answered. */
  word: string;
  pinyin: string;
  /** Current text in the input for this item (kept in domain state so the
   *  input is a plain controlled reflection of it, and so "Thử lại" can
   *  hand the user back an editable field with what they last typed). */
  userAnswer: string;
  hintShown: boolean;
  /** Last-evaluated outcome — what scoring is derived from. Retrying after
   *  a wrong answer OVERWRITES this on the next evaluation; it is never
   *  appended to a separate list, so a card can never count under two
   *  results or be counted twice. */
  result: WritingResult;
  /** Whether the correct/wrong feedback panel is currently shown for this
   *  item. Separate from `result` on purpose: "Thử lại" hides the panel
   *  (back to an editable input) WITHOUT clearing `result` — if the user
   *  then advances without resubmitting, the last evaluation still stands,
   *  exactly like Flashcard's "re-evaluating updates, doesn't duplicate". */
  feedbackVisible: boolean;
}

export interface WritingSessionState {
  practiceType: "writing";
  hskLevel: HskLevel;
  requestedCount: WordCountOption;
  items: WritingItem[];
  currentIndex: number;
  sessionCompleted: boolean;
}

export function createWritingSession(
  hskLevel: HskLevel,
  requestedCount: WordCountOption,
  selected: PracticeVocabularyItem[]
): WritingSessionState {
  return {
    practiceType: "writing",
    hskLevel,
    requestedCount,
    items: selected.map((item) => ({
      vocabularyId: item.id,
      meaningVi: item.meaningVi,
      word: item.word,
      pinyin: item.pinyin,
      userAnswer: "",
      hintShown: false,
      result: "unanswered",
      feedbackVisible: false,
    })),
    currentIndex: 0,
    sessionCompleted: false,
  };
}

/** Conservative, predictable comparison — trims whitespace only. No fuzzy
 *  matching, no partial credit: this is typed Chinese text practice. */
export function normalizeWritingAnswer(value: string): string {
  return value.trim();
}

export function isWritingAnswerCorrect(userAnswer: string, expectedWord: string): boolean {
  const normalized = normalizeWritingAnswer(userAnswer);
  return normalized.length > 0 && normalized === normalizeWritingAnswer(expectedWord);
}

function mapCurrentItem(
  session: WritingSessionState,
  update: (item: WritingItem) => WritingItem
): WritingSessionState {
  const current = session.items[session.currentIndex];
  if (!current) return session;
  const items = session.items.map((item) =>
    item.vocabularyId === current.vocabularyId ? update(item) : item
  );
  return { ...session, items };
}

/** Updates the current item's in-progress input text. Never touches
 *  `result`/`feedbackVisible` — typing alone can never affect scoring. */
export function updateCurrentWritingAnswer(
  session: WritingSessionState,
  value: string
): WritingSessionState {
  return mapCurrentItem(session, (item) => ({ ...item, userAnswer: value }));
}

/** Reveals the current item's Pinyin. Idempotent, never reveals the
 *  Chinese word, never affects scoring. */
export function showHintForCurrentWriting(session: WritingSessionState): WritingSessionState {
  return mapCurrentItem(session, (item) => ({ ...item, hintShown: true }));
}

/**
 * "Kiểm tra đáp án" — judges the current item's `userAnswer` against its
 * expected word and shows the feedback panel. Overwrites this item's
 * result (matched by vocabularyId), so calling this again after "Thử lại"
 * updates the same entry instead of creating a second one.
 */
export function evaluateCurrentWritingAnswer(session: WritingSessionState): WritingSessionState {
  const current = session.items[session.currentIndex];
  if (!current) return session;
  const result: WritingResult = isWritingAnswerCorrect(current.userAnswer, current.word)
    ? "correct"
    : "wrong";
  const items = session.items.map((item) =>
    item.vocabularyId === current.vocabularyId ? { ...item, result, feedbackVisible: true } : item
  );
  return { ...session, items, sessionCompleted: isWritingSessionComplete(items) };
}

/**
 * "Không nhớ" — an immediate wrong result for the current item, regardless
 * of what (if anything) is typed. Same overwrite semantics as evaluate.
 */
export function markCurrentWritingDontRemember(session: WritingSessionState): WritingSessionState {
  const current = session.items[session.currentIndex];
  if (!current) return session;
  const items = session.items.map((item) =>
    item.vocabularyId === current.vocabularyId
      ? { ...item, result: "wrong" as const, feedbackVisible: true }
      : item
  );
  return { ...session, items, sessionCompleted: isWritingSessionComplete(items) };
}

/**
 * "Thử lại" — hides the feedback panel so the input becomes editable again
 * for another attempt at the SAME item. Deliberately does NOT reset
 * `result`: if the user advances without resubmitting, the last judged
 * outcome still stands (never silently reverts to "unanswered").
 */
export function retryCurrentWriting(session: WritingSessionState): WritingSessionState {
  return mapCurrentItem(session, (item) => ({ ...item, feedbackVisible: false }));
}

/** Whether the current item has been judged at least once — gates "Tiếp
 *  theo" so an unanswered item can never be skipped. */
export function canAdvanceCurrentWritingItem(session: WritingSessionState): boolean {
  const current = session.items[session.currentIndex];
  return !!current && current.result !== "unanswered";
}

export function canGoToNextWritingItem(session: WritingSessionState): boolean {
  return session.currentIndex < session.items.length - 1;
}

export function goToNextWritingItem(session: WritingSessionState): WritingSessionState {
  if (!canGoToNextWritingItem(session)) return session;
  return { ...session, currentIndex: session.currentIndex + 1 };
}

export function isWritingSessionComplete(items: WritingItem[]): boolean {
  return items.length > 0 && items.every((item) => item.result !== "unanswered");
}

/** Đúng/Sai counts — always derived from `items`, so retrying a wrong
 *  answer into a correct one is never counted under both results. */
export function countWritingResult(items: WritingItem[], result: WritingResult): number {
  return items.filter((item) => item.result === result).length;
}

export function wrongWritingVocabularyIds(items: WritingItem[]): string[] {
  return items.filter((item) => item.result === "wrong").map((item) => item.vocabularyId);
}
