import type { HskLevel } from "@/lib/data/types";

/**
 * Exact per-level hex colors approved for the Home redesign (visual
 * reference, 2026-09). Deliberately NOT merged into tailwind.config.ts's
 * existing `accent.*` tokens: those are shared by Practice's own
 * already-approved cards (see hskLevelAccent.ts's comment), and this
 * phase's brief is Home-only — touching a shared config token would risk
 * an unrequested visual change on Practice/HSK's `/hsk` route. Kept as a
 * plain hex map instead; consuming components apply it via Tailwind
 * arbitrary-value classes (`bg-[${HSK_LEVEL_HEX[level]}]`), matching this
 * codebase's own additive-token precedent (primary.tint/wash added
 * alongside primary.light without touching it).
 */
export const HSK_LEVEL_HEX: Record<HskLevel, string> = {
  1: "#015291",
  2: "#65B482",
  3: "#AB8BF2",
  4: "#F5A064",
  5: "#EE7F81",
  6: "#11B3AB",
};

/** Practice's 4 exercise types, colors drawn from the same approved HSK
 *  palette above (HSK1/2/3/5), per the Home reference's Practice cards. */
export const PRACTICE_ACCENT_HEX = {
  meaning: HSK_LEVEL_HEX[1],
  character: HSK_LEVEL_HEX[2],
  flashcard: HSK_LEVEL_HEX[3],
  writing: HSK_LEVEL_HEX[5],
} as const;
