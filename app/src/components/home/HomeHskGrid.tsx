import Link from "next/link";
import Image from "next/image";
import { HomeSectionCard } from "./HomeSectionCard";
import { HSK_LEVEL_HEX } from "@/lib/hsk/homePalette";
import { HSK_LEVEL_INFO } from "@/lib/hsk/hskLevelInfo";
import { getVocabularyCountByLevel } from "@/lib/data/vocabularyRepository";
import { ArrowRightIcon } from "@/components/ui/icons";
import type { HskLevel } from "@/lib/data/types";

const HSK_LEVELS: HskLevel[] = [1, 2, 3, 4, 5, 6];

/**
 * HSK section (reference screenshot 1/3, "Chọn cấp độ HSK để bắt đầu").
 *
 * Visual-refinement pass: cards now show the level label ("Sơ cấp" /
 * "Trung cấp" / "Cao cấp") and word count alongside the level number —
 * both pulled from data that already exists elsewhere (HSK_LEVEL_INFO and
 * getVocabularyCountByLevel, the exact same source /hsk's own overview
 * page already uses), not invented or copied from the reference image's
 * own numbers. Each card gets a supplied illustration
 * (hsk-<level>-illustration.png, a true 3:4 source) plus a small circular
 * arrow affordance in the corner. Locked per-level colors (HSK_LEVEL_HEX)
 * and the /hsk/[level] route are unchanged.
 *
 * Visual fix pass (HOME VISUAL FIX PASS): the card itself used to be
 * forced to `aspect-[3/4]` as a whole, with the image confined to a
 * `h-[58%]` slice of that card under `object-cover` — since the image's
 * own native ratio (1086x1448, 3:4) didn't match that slice's ratio,
 * `object-cover` cropped a real chunk of the artwork off the bottom. The
 * `aspect-[3/4]` now moves onto the image's own wrapper instead of the
 * card, i.e. the wrapper's ratio exactly matches the source image's own
 * ratio, so `object-cover` has nothing to crop — the full illustration
 * renders, uncropped and undistorted. The card's total height is no
 * longer fixed; it's simply the header block's natural height plus the
 * image's own 3:4 height, which is intentionally taller than before.
 * The per-level colored drop-shadow (`box-shadow: 0 4px 0 color`) is
 * removed per the same pass — border + illustration + arrow only, no
 * shadow; this is local to these cards only (HomeSectionCard's own
 * shadow, used by Search/Radical/Practice, is untouched).
 *
 * Final visual fix pass (HOME HSK CARD — FINAL VISUAL FIX): the previous
 * pass still put HSK title/label/count in a separate flow block ABOVE
 * the image, i.e. the card's total shape was (header height) + (3:4
 * image), not itself a 3:4 card. Per the approved reference, the
 * illustration now IS the entire card — the `Link` itself carries
 * `aspect-[3/4]` and a `fill` Image covers it completely (same ratio as
 * the source art, so `object-cover` still crops nothing) — and the
 * title/label/count/arrow are all absolutely-positioned overlays on top
 * of it, not a separate white header. A subtle white-to-transparent
 * gradient sits behind just the text block (not a full opaque panel) so
 * the metadata stays legible regardless of what part of the artwork is
 * behind it; the same light gradient is used in both themes since the
 * artwork itself is always a light watercolor regardless of app theme.
 */
export function HomeHskGrid() {
  return (
    <HomeSectionCard
      iconSrc="/icons/hsk-cap.png"
      iconBg={`${HSK_LEVEL_HEX[1]}1A`}
      title="Chọn cấp độ HSK để bắt đầu"
      subtitle="Học từ vựng theo lộ trình từ cơ bản đến nâng cao"
    >
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
        {HSK_LEVELS.map((level) => {
          const color = HSK_LEVEL_HEX[level];
          const info = HSK_LEVEL_INFO[level];
          const count = getVocabularyCountByLevel(level);
          return (
            // Topbar/header z-index fix: `isolate` gives this card its own
            // stacking context, so the `z-10` overlays inside it (scrim,
            // title block, arrow badge) stack correctly above the card's
            // own image without ever competing with the page-level sticky
            // header (also `z-10`) — a same-value tie that previously
            // resolved in the card's favor purely by DOM order (later
            // content beats an earlier element at an equal z-index),
            // letting these cards paint over the header during scroll.
            <Link
              key={level}
              href={`/hsk/${level}?from=home`}
              className="group relative isolate block aspect-[3/4] overflow-hidden rounded-[18px] border bg-white transition-transform hover:-translate-y-0.5 dark:bg-night-input"
              style={{ borderColor: color }}
            >
              <Image
                src={`/hsk-${level}-illustration.png`}
                alt=""
                fill
                aria-hidden
                sizes="(min-width: 1024px) 190px, (min-width: 640px) 33vw, 50vw"
                className="object-cover"
                style={{ backgroundColor: `${color}14` }}
              />

              {/* Subtle scrim behind the overlaid text only — not a full
                  opaque panel — so the artwork stays visible underneath. */}
              <div
                aria-hidden
                className="pointer-events-none absolute inset-x-0 top-0 z-10 h-2/5 bg-gradient-to-b from-white/85 via-white/35 to-transparent"
              />

              <div className="absolute inset-x-0 top-0 z-10 flex flex-col items-start gap-1 p-3.5">
                <span className="font-ui text-xl font-bold leading-none" style={{ color }}>
                  HSK {level}
                </span>
                <span
                  className="font-ui rounded-full px-2 py-0.5 text-[11px] font-semibold leading-tight"
                  style={{ backgroundColor: `${color}26`, color }}
                >
                  {info.name}
                </span>
                <span className="font-ui text-xs font-medium text-neutral-700">
                  {count.toLocaleString("vi-VN")} từ
                </span>
              </div>

              <span
                className="absolute bottom-2.5 right-2.5 z-10 flex h-7 w-7 items-center justify-center rounded-full bg-white shadow-[0_1px_2px_rgba(15,23,42,0.15)] transition-transform group-hover:translate-x-0.5"
                style={{ color }}
                aria-hidden
              >
                <ArrowRightIcon className="h-3.5 w-3.5" />
              </span>
            </Link>
          );
        })}
      </div>
    </HomeSectionCard>
  );
}
