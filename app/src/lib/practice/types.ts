import type { ComponentType, SVGProps } from "react";
import type { HskLevel } from "@/lib/data/types";
import { SearchIcon, BookOpenIcon, CardsIcon, PencilIcon } from "@/components/ui/icons";

/**
 * The four exercise types from docs/PRACTICE/02_PRACTICE_SPEC.md §4-7.
 * Naming follows the model suggested in docs/PRACTICE/04_DEVELOPMENT_SPEC.md
 * ("practiceType: meaning / character / flashcard / writing").
 */
export type PracticeType = "meaning" | "character" | "flashcard" | "writing";

export const PRACTICE_TYPES: PracticeType[] = ["meaning", "character", "flashcard", "writing"];

interface PracticeTypeInfo {
  /** Route segment under /practice/<slug>. */
  slug: string;
  title: string;
  description: string;
  icon: ComponentType<SVGProps<SVGSVGElement>>;
}

/**
 * Copy and route slugs are exact matches to docs/PRACTICE/02_PRACTICE_SPEC.md
 * §1 (Home cards) and its conceptual routing table in
 * 04_DEVELOPMENT_SPEC.md — not invented here.
 */
export const PRACTICE_TYPE_INFO: Record<PracticeType, PracticeTypeInfo> = {
  meaning: {
    slug: "meaning",
    title: "Chọn nghĩa",
    description: "Chọn nghĩa tiếng Việt đúng với từ vựng",
    icon: SearchIcon,
  },
  character: {
    slug: "character",
    title: "Chọn chữ Hán",
    description: "Chọn chữ Hán đúng với nghĩa",
    icon: BookOpenIcon,
  },
  flashcard: {
    slug: "flashcard",
    title: "Flashcard",
    description: "Ôn tập từ vựng với thẻ ghi nhớ",
    icon: CardsIcon,
  },
  writing: {
    slug: "writing",
    title: "Luyện viết",
    description: "Nhập tiếng Trung theo nghĩa tiếng Việt",
    icon: PencilIcon,
  },
};

export function practiceRoute(type: PracticeType): string {
  return `/practice/${PRACTICE_TYPE_INFO[type].slug}`;
}

export const HSK_LEVELS: HskLevel[] = [1, 2, 3, 4, 5, 6];

/**
 * "Số lượng từ" options — docs/PRACTICE/02_PRACTICE_SPEC.md §2 and
 * PRACTICE_SPEC.md §4 ("Tất cả / 50 / 20 / 10"). `"all"` stands in for
 * "Tất cả" (no fixed requested count); the actual/available-count
 * reconciliation described in the spec is session-creation logic, out of
 * scope for the configuration foundation.
 */
export type WordCountOption = "all" | 50 | 20 | 10;

export const WORD_COUNT_OPTIONS: { value: WordCountOption; label: string }[] = [
  { value: "all", label: "Tất cả" },
  { value: 50, label: "50" },
  { value: 20, label: "20" },
  { value: 10, label: "10" },
];

export interface PracticeConfigState {
  hskLevel: HskLevel;
  wordCount: WordCountOption;
}

/** Matches the default shown in every supplied configuration screenshot. */
export const DEFAULT_PRACTICE_CONFIG: PracticeConfigState = {
  hskLevel: 2,
  wordCount: 20,
};
