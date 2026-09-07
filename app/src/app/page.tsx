import { HomeHero, HOME_CONTENT_MAX_WIDTH } from "@/components/home/HomeHero";
import { HomeSearch } from "@/components/home/HomeSearch";
import { HomeHskGrid } from "@/components/home/HomeHskGrid";
import { HomeRadicalSection } from "@/components/home/HomeRadicalSection";
import { HomePracticeSection } from "@/components/home/HomePracticeSection";

/**
 * Home (visual redesign per the approved reference screenshots). Approved
 * information architecture — Header / Hero / Search / HSK / Radical /
 * Practice, no new sections, no login/gamification.
 *
 * Pass 04: Search moved out of Hero into its own section, first item in
 * the same `HOME_CONTENT_MAX_WIDTH` column HSK/Radical/Practice already
 * share (so all four sections have identical left/right alignment — see
 * HomeSearch.tsx's own comment on why it doesn't set its own width). Its
 * active-state result panel is a `position: absolute` overlay with a
 * `position: fixed` backdrop (both built inside HomeSearch itself), not
 * inline content — this section's own box height, and every section
 * below it, never changes when a query is typed.
 *
 * Pass 10: Search pulled out of the shared `flex-col gap-8` group into
 * its own wrapper with a tighter margin, so its Hero↔Search and
 * Search↔HSK gaps could shrink without touching the HSK/Radical/Practice
 * group's own mutual gap-8 spacing.
 * Pass 12: those two gaps (16px) felt slightly too tight next to the
 * group's own 32px rhythm — bumped to 24px each.
 * Pass 14: bumped again, 24px → 32px each (pt-6→pt-8, mt-6→mt-8), to
 * fully match the HSK↔Radical / Radical↔Practice group's own 32px
 * (gap-8) rhythm — all four major gaps were a uniform 32px.
 * Pass 15: bumped once more, 32px → 40px uniformly (pt-8→pt-10,
 * mt-8→mt-10, gap-8→gap-10) — same rhythm kept across all four gaps.
 */
export default function HomePage() {
  return (
    <div>
      <HomeHero />
      <div className="relative ml-[calc(50%-50vw)] mr-[calc(50%-50vw)] w-screen bg-[#F9F9F5] px-4 pb-10 pt-10 dark:bg-night-bg sm:px-6">
        <div className={`mx-auto ${HOME_CONTENT_MAX_WIDTH}`}>
          <HomeSearch />
        </div>
        <div className={`mx-auto mt-10 flex ${HOME_CONTENT_MAX_WIDTH} flex-col gap-10`}>
          <HomeHskGrid />
          <HomeRadicalSection />
          <HomePracticeSection />
        </div>
      </div>
    </div>
  );
}
