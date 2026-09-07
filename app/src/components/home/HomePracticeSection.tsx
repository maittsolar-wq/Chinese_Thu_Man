import Link from "next/link";
import Image from "next/image";
import { HomeSectionCard } from "./HomeSectionCard";
import { PRACTICE_TYPES, PRACTICE_TYPE_INFO, practiceRoute, type PracticeType } from "@/lib/practice/types";
import { PRACTICE_ACCENT_HEX } from "@/lib/hsk/homePalette";

/** Supplied practice icon assets (§2) — matched to the reference's globe /
 *  magnifying-glass / bolt / pencil glyphs, not the pre-existing, visually
 *  different PracticeMeaningIcon &c. SVGs in ui/icons.tsx. */
const PRACTICE_ICON_SRC: Record<PracticeType, string> = {
  meaning: "/icons/practice-meaning.png",
  character: "/icons/practice-character.png",
  flashcard: "/icons/practice-flashcard.png",
  writing: "/icons/practice-writing.png",
};

/**
 * Practice section (reference screenshot 1/3, "Luyện tập"). Titles and
 * descriptions are read from lib/practice/types.ts's own
 * `PRACTICE_TYPE_INFO` (already an exact match to the reference's card
 * copy) and routed through the existing `practiceRoute()` helper — no new
 * copy or routing logic, only a new Home-specific card presentation.
 *
 * Pass 12: card shadow color now matches each card's own accent (inline
 * `boxShadow`, same `accent` value already driving `borderColor`) instead
 * of a flat gray — same treatment as HomeHskGrid's cards. Dimensions
 * (265×185 desktop / 155px mobile) are unchanged: Pass 12's brief called
 * these "1:1 square," but they have been an intentional non-square
 * rectangle since Pass 04 and every pass since (08–11) explicitly
 * reaffirmed 265×185 as frozen — this pass's own stronger, repeated "do
 * not change card dimensions" rule wins over that one inaccurate line.
 */
export function HomePracticeSection() {
  return (
    <HomeSectionCard
      iconSrc="/icons/practice-target.png"
      iconBg={`${PRACTICE_ACCENT_HEX.flashcard}1A`}
      title="Luyện tập"
      subtitle="Học từ vựng theo 6 cấp độ HSK từ cơ bản đến nâng cao."
    >
      {/* Pass 04: 4 cards in one row on desktop (was a 2×2 grid of long
          horizontal rows) — a vertical icon/title/description card per
          activity, matching the reference's "learning card" treatment
          rather than a navigation-list look. */}
      <div className="grid grid-cols-1 gap-4 sm:flex sm:flex-wrap sm:justify-between sm:gap-x-0 sm:gap-y-4">
        {PRACTICE_TYPES.map((type) => {
          const info = PRACTICE_TYPE_INFO[type];
          const accent = PRACTICE_ACCENT_HEX[type];
          return (
            <Link
              key={type}
              href={practiceRoute(type)}
              className="flex h-[155px] flex-col items-center justify-center gap-2 rounded-[18px] border-2 bg-white p-5 text-center transition-transform hover:-translate-y-0.5 dark:bg-night-input sm:h-[185px] sm:w-[265px]"
              style={{ borderColor: accent, boxShadow: `0 4px 0 ${accent}` }}
            >
              <span
                className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full"
                style={{ backgroundColor: accent }}
              >
                <Image src={PRACTICE_ICON_SRC[type]} alt="" width={26} height={26} aria-hidden />
              </span>
              <span className="font-ui text-[21px] font-bold leading-tight" style={{ color: accent }}>
                {info.title}
              </span>
              <span className="font-ui text-sm leading-snug text-[#343536] dark:text-night-muted">
                {info.description}
              </span>
            </Link>
          );
        })}
      </div>
    </HomeSectionCard>
  );
}
