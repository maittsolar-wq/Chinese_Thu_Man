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
 */
export default function HomePage() {
  return (
    <div>
      <HomeHero />
      <div className="relative ml-[calc(50%-50vw)] mr-[calc(50%-50vw)] w-screen bg-[#F9F9F5] px-4 pb-8 pt-8 dark:bg-night-bg sm:px-6">
        <div className={`mx-auto flex ${HOME_CONTENT_MAX_WIDTH} flex-col gap-8`}>
          <HomeSearch />
          <HomeHskGrid />
          <HomeRadicalSection />
          <HomePracticeSection />
        </div>
      </div>
    </div>
  );
}
