import Link from "next/link";
import { HomeSectionCard } from "./HomeSectionCard";
import { HSK_LEVEL_HEX } from "@/lib/hsk/homePalette";
import type { HskLevel } from "@/lib/data/types";

const HSK_LEVELS: HskLevel[] = [1, 2, 3, 4, 5, 6];

/** HSK section (reference screenshot 1/3, "Chọn cấp độ HSK để bắt đầu").
 *  Cards intentionally show only the level number — no vocabulary count or
 *  other invented statistic, per §13's "do not invent additional
 *  statistics" instruction; the reference itself shows none either. */
export function HomeHskGrid() {
  return (
    <HomeSectionCard
      iconSrc="/icons/hsk-cap.png"
      iconBg={`${HSK_LEVEL_HEX[1]}1A`}
      title="Chọn cấp độ HSK để bắt đầu"
      subtitle="Học từ vựng theo lộ trình từ cơ bản đến nâng cao"
    >
      <div className="grid grid-cols-3 gap-3 sm:flex sm:flex-wrap sm:justify-between sm:gap-x-0 sm:gap-y-4">
        {HSK_LEVELS.map((level) => {
          const color = HSK_LEVEL_HEX[level];
          return (
            <Link
              key={level}
              href={`/hsk/${level}`}
              className="flex aspect-square flex-col items-center justify-center gap-1 rounded-[18px] border-2 bg-white px-3 text-center shadow-[0_4px_0_#E2E8F0] transition-transform hover:-translate-y-0.5 dark:bg-night-input dark:shadow-[0_4px_0_#3a3a3a] sm:w-[160px]"
              style={{ borderColor: color }}
            >
              <span className="font-ui text-base font-semibold" style={{ color }}>
                HSK
              </span>
              <span className="font-ui text-[48px] font-bold leading-none" style={{ color }}>
                {level}
              </span>
            </Link>
          );
        })}
      </div>
    </HomeSectionCard>
  );
}
