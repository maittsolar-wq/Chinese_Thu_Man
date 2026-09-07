import type { Metadata } from "next";
import { HskHero } from "@/components/hsk/HskHero";
import { HskLevelGrid } from "@/components/hsk/HskLevelGrid";
import { RadicalCta } from "@/components/hsk/RadicalCta";
import { HOME_CONTENT_MAX_WIDTH } from "@/components/home/HomeHero";

export const metadata: Metadata = { title: "HSK — Chinese Thu Man" };

/**
 * HSK Main visual-redesign ("Option 1.5" reference: Option 1's visual +
 * Option 2's information hierarchy). Replaces the previous plain
 * dashboard-style page (H1 + 3-icon feature row + plain Card grid +
 * Panel) with a Home-consistent Hero + illustrated level cards + a
 * Radical CTA — same `#F9F9F5` full-bleed background band and
 * `HOME_CONTENT_MAX_WIDTH` content column Home already established
 * (imported, not duplicated). Behavior/data untouched: same 6 HSK
 * levels, same `/hsk/[level]` routes, same `/radicals` route, same
 * HSK_LEVEL_INFO/getVocabularyCountByLevel sources.
 */
export default function HskOverviewPage() {
  return (
    <div>
      <HskHero />
      <div className="relative ml-[calc(50%-50vw)] mr-[calc(50%-50vw)] w-screen bg-[#F9F9F5] px-4 pb-10 pt-10 dark:bg-night-bg sm:px-6">
        <div className={`mx-auto flex ${HOME_CONTENT_MAX_WIDTH} flex-col gap-10`}>
          <HskLevelGrid />
          <RadicalCta />
        </div>
      </div>
    </div>
  );
}
