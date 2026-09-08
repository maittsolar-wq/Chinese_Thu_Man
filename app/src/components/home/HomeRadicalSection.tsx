import Link from "next/link";
import { HomeSectionCard } from "./HomeSectionCard";
import { getAllRadicals } from "@/lib/data/radicalRepository";
import { HSK_LEVEL_HEX } from "@/lib/hsk/homePalette";
import { ChevronRightIcon } from "@/components/ui/icons";
import type { RadicalSummary } from "@/lib/data/types";

/**
 * The 5 featured glyphs + their exact accent-color assignment (人→HSK5
 * pink, 口→HSK2 green, 心→HSK1 blue, 手→HSK3 purple, 水→HSK4 orange) are a
 * fixed decorative pick straight from the approved Home reference, not
 * derived from these radicals' own (generally different) real HSK-level
 * associations — §11 only asks for "the HSK palette at ~10%", not that a
 * card's tint match its glyph's true level. Every other field (pinyin,
 * Vietnamese name, stroke count, detail route id) is the real
 * getAllRadicals() record for that glyph — nothing here is invented text.
 */
const FEATURED_GLYPH_ACCENT: [string, string][] = [
  ["人", HSK_LEVEL_HEX[5]],
  ["口", HSK_LEVEL_HEX[2]],
  ["心", HSK_LEVEL_HEX[1]],
  ["手", HSK_LEVEL_HEX[3]],
  ["水", HSK_LEVEL_HEX[4]],
];

export function HomeRadicalSection() {
  const allRadicals = getAllRadicals();
  const cards = FEATURED_GLYPH_ACCENT.map(([glyph, accent]) => {
    const radical = allRadicals.find((r) => r.radical === glyph);
    return radical ? { radical, accent } : null;
  }).filter((entry): entry is { radical: RadicalSummary; accent: string } => entry !== null);

  return (
    <HomeSectionCard
      iconSrc="/icons/radical-zi.png"
      iconBg={`${HSK_LEVEL_HEX[2]}1A`}
      title="Hiểu chữ Hán từ 214 bộ thủ"
      subtitle={"Học bộ thủ giúp bạn ghi nhớ, đoán nghĩa và\nnhận diện chữ Hán dễ hơn"}
      cta={
        <Link
          href="/radicals?from=home"
          className="font-ui flex shrink-0 items-center gap-2 rounded-full border-2 border-[#015291] px-6 py-3 text-base font-semibold text-[#015291] transition-colors hover:bg-[#015291]/5 dark:text-night-primary dark:hover:bg-night-primary/10"
        >
          Khám phá 214 bộ thủ
          <ChevronRightIcon className="h-5 w-5" />
        </Link>
      }
    >
      <div className="grid grid-cols-3 gap-3 sm:flex sm:flex-wrap sm:justify-between sm:gap-x-0 sm:gap-y-4">
        {cards.map(({ radical, accent }) => (
          <Link
            key={radical.id}
            href={`/radicals/${radical.id}?from=home`}
            className="flex aspect-square flex-col items-center justify-center gap-1 rounded-[18px] px-3 text-center transition-transform hover:-translate-y-0.5 sm:w-[172px]"
            style={{ backgroundColor: `${accent}1A` }}
          >
            {/* font-normal (400) is deliberate — the reference's radical
                glyph is thin/elegant, not bold; do not reintroduce
                font-semibold/font-bold here. */}
            <span className="font-cjk text-[56px] font-normal leading-none text-neutral-900 dark:text-night-text">
              {radical.radical}
            </span>
            <span className="font-ui text-base italic" style={{ color: accent }}>
              {radical.pinyin}
            </span>
            <span className="font-ui text-base capitalize text-neutral-800 dark:text-night-muted">
              {radical.meaningVi}
            </span>
          </Link>
        ))}
      </div>
    </HomeSectionCard>
  );
}
