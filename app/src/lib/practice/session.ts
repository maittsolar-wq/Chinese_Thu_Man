import type { HskLevel } from "@/lib/data/types";
import type { PracticeType, WordCountOption } from "./types";

/** Minimal shape a Practice session needs from a vocabulary record. */
export interface PracticeVocabularyItem {
  id: string;
  word: string;
  pinyin: string;
  meaningVi: string;
}

/**
 * One multiple-choice question, shared by "Chọn nghĩa" (prompt: Chinese
 * word+pinyin, answer: Vietnamese meaning) and "Chọn chữ Hán" (prompt:
 * Vietnamese meaning, answer: Chinese word) — the two directions are
 * structurally identical, only which vocabulary field is the prompt vs.
 * the answer differs (docs/PRACTICE §4/§5; this phase's spec §4).
 *
 * `promptPrimary`/`promptSecondary` are pure content — PracticeExerciseView
 * decides how to style the prompt based on the session's `practiceType`,
 * keeping this type presentation-agnostic.
 */
export interface ChoiceQuestion {
  vocabularyId: string;
  promptPrimary: string;
  promptSecondary: string | null;
  correctAnswer: string;
  options: string[];
}

/**
 * Generic session state, reusable across practice types (only the
 * `questions` shape and answer-checking logic differ per type). Field
 * names follow docs/PRACTICE/02_PRACTICE_SPEC.md §3.
 */
export interface PracticeSessionState<TQuestion> {
  practiceType: PracticeType;
  hskLevel: HskLevel;
  requestedCount: WordCountOption;
  questions: TQuestion[];
  currentIndex: number;
  selectedAnswer: string | null;
  isAnswered: boolean;
  isCorrect: boolean | null;
  correctCount: number;
  wrongCount: number;
  /** vocabularyIds answered incorrectly in THIS session only — feeds "Ôn lại". */
  wrongVocabularyIds: string[];
  sessionCompleted: boolean;
}

export type ChoiceSessionState = PracticeSessionState<ChoiceQuestion>;

function shuffle<T>(items: T[]): T[] {
  const result = [...items];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const temp = result[i]!;
    result[i] = result[j]!;
    result[j] = temp;
  }
  return result;
}

/**
 * Resolves "Tất cả / 50 / 20 / 10" against real availability and picks
 * that many items the learning cycle hasn't used yet — docs/PRACTICE §2/§4:
 * "the actual question count cannot exceed available vocabulary" and
 * never repeats a vocabulary item already used in the current cycle.
 */
export function pickUnusedVocabulary(
  pool: PracticeVocabularyItem[],
  usedIds: ReadonlySet<string>,
  requestedCount: WordCountOption
): PracticeVocabularyItem[] {
  const unused = pool.filter((item) => !usedIds.has(item.id));
  const take = requestedCount === "all" ? unused.length : Math.min(requestedCount, unused.length);
  return shuffle(unused).slice(0, take);
}

export function isLearningCycleComplete(
  pool: PracticeVocabularyItem[],
  usedIds: ReadonlySet<string>
): boolean {
  return pool.length > 0 && usedIds.size >= pool.length;
}

type ChoiceDirection = "meaning" | "character";

/** Which vocabulary field is the correct-answer value for a direction. */
function choiceAnswerValue(direction: ChoiceDirection, item: PracticeVocabularyItem): string {
  return direction === "meaning" ? item.meaningVi : item.word;
}

/**
 * Shared question-generation core for both directions. Distractors are
 * drawn from OTHER real answer values in the same HSK pool — never
 * invented, never duplicated within one question's options — docs/PRACTICE
 * §6/§7 and this phase's spec §5.
 */
function buildChoiceQuestions(
  direction: ChoiceDirection,
  selected: PracticeVocabularyItem[],
  pool: PracticeVocabularyItem[]
): ChoiceQuestion[] {
  return selected.map((item) => {
    const correctAnswer = choiceAnswerValue(direction, item);
    const correctKey = correctAnswer.trim().toLowerCase();

    const seen = new Set<string>([correctKey]);
    const distractorPool = shuffle(pool.filter((candidate) => candidate.id !== item.id));

    const distractors: string[] = [];
    for (const candidate of distractorPool) {
      const value = choiceAnswerValue(direction, candidate);
      const key = value.trim().toLowerCase();
      if (seen.has(key)) continue;
      seen.add(key);
      distractors.push(value);
      if (distractors.length === 3) break;
    }

    return {
      vocabularyId: item.id,
      promptPrimary: direction === "meaning" ? item.word : item.meaningVi,
      promptSecondary: direction === "meaning" ? item.pinyin : null,
      correctAnswer,
      options: shuffle([correctAnswer, ...distractors]),
    };
  });
}

function initChoiceSession(
  practiceType: PracticeType,
  hskLevel: HskLevel,
  requestedCount: WordCountOption,
  questions: ChoiceQuestion[]
): ChoiceSessionState {
  return {
    practiceType,
    hskLevel,
    requestedCount,
    questions,
    currentIndex: 0,
    selectedAnswer: null,
    isAnswered: false,
    isCorrect: null,
    correctCount: 0,
    wrongCount: 0,
    wrongVocabularyIds: [],
    sessionCompleted: false,
  };
}

// ---- Chọn nghĩa (Chinese -> Vietnamese) ----

export function buildMeaningQuestions(
  selected: PracticeVocabularyItem[],
  pool: PracticeVocabularyItem[]
): ChoiceQuestion[] {
  return buildChoiceQuestions("meaning", selected, pool);
}

export function createMeaningSession(
  hskLevel: HskLevel,
  requestedCount: WordCountOption,
  selected: PracticeVocabularyItem[],
  pool: PracticeVocabularyItem[]
): ChoiceSessionState {
  return initChoiceSession("meaning", hskLevel, requestedCount, buildMeaningQuestions(selected, pool));
}

// ---- Chọn chữ Hán (Vietnamese -> Chinese) ----

export function buildCharacterQuestions(
  selected: PracticeVocabularyItem[],
  pool: PracticeVocabularyItem[]
): ChoiceQuestion[] {
  return buildChoiceQuestions("character", selected, pool);
}

export function createCharacterSession(
  hskLevel: HskLevel,
  requestedCount: WordCountOption,
  selected: PracticeVocabularyItem[],
  pool: PracticeVocabularyItem[]
): ChoiceSessionState {
  return initChoiceSession("character", hskLevel, requestedCount, buildCharacterQuestions(selected, pool));
}
