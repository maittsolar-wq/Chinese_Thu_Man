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
 * One "Chọn nghĩa" question: a vocabulary item plus its shuffled
 * multiple-choice options. Other practice types will need their own
 * question shape (character options, flashcard front/back, a free-text
 * writing prompt) — this type intentionally isn't shared beyond meaning,
 * per docs/PRACTICE §4-7 defining genuinely different interactions per
 * type.
 */
export interface MeaningQuestion {
  vocabularyId: string;
  word: string;
  pinyin: string;
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

export type MeaningSessionState = PracticeSessionState<MeaningQuestion>;

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

/**
 * Builds the four-option "Chọn nghĩa" questions for a selected batch of
 * vocabulary. Distractors are drawn from OTHER real meanings in the same
 * HSK pool (never invented, never duplicated within one question's
 * options) — docs/PRACTICE §6 and this phase's spec §6.
 */
export function buildMeaningQuestions(
  selected: PracticeVocabularyItem[],
  pool: PracticeVocabularyItem[]
): MeaningQuestion[] {
  return selected.map((item) => {
    const correctAnswer = item.meaningVi;
    const correctKey = correctAnswer.trim().toLowerCase();

    const seen = new Set<string>([correctKey]);
    const distractorPool = shuffle(pool.filter((candidate) => candidate.id !== item.id));

    const distractors: string[] = [];
    for (const candidate of distractorPool) {
      const key = candidate.meaningVi.trim().toLowerCase();
      if (seen.has(key)) continue;
      seen.add(key);
      distractors.push(candidate.meaningVi);
      if (distractors.length === 3) break;
    }

    return {
      vocabularyId: item.id,
      word: item.word,
      pinyin: item.pinyin,
      correctAnswer,
      options: shuffle([correctAnswer, ...distractors]),
    };
  });
}

export function createMeaningSession(
  hskLevel: HskLevel,
  requestedCount: WordCountOption,
  selected: PracticeVocabularyItem[],
  pool: PracticeVocabularyItem[]
): MeaningSessionState {
  return {
    practiceType: "meaning",
    hskLevel,
    requestedCount,
    questions: buildMeaningQuestions(selected, pool),
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
