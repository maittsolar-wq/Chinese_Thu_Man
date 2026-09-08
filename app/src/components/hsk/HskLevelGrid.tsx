import Link from "next/link";
import Image from "next/image";
import { HSK_LEVEL_HEX } from "@/lib/hsk/homePalette";
import { HSK_LEVEL_INFO } from "@/lib/hsk/hskLevelInfo";
import { getVocabularyCountByLevel } from "@/lib/data/vocabularyRepository";
import type { HskLevel } from "@/lib/data/types";

const HSK_LEVELS: HskLevel[] = [1, 2, 3, 4, 5, 6];

/**
 * HSK page's 6 level cards (visual-redesign, "Option 1.5" reference).
 * Distinct card composition from Home's own HSK cards (HomeHskGrid.tsx,
 * untouched by this task) — the approved reference for THIS page uses a
 * side-by-side layout (illustration strip on the left, title/level-badge
 * /description on the right), not Home's full-bleed overlay style, so
 * this is a separate component rather than a shared one forced to serve
 * two different approved designs.
 *
 * Level name, description, and vocabulary count are all pulled from the
 * exact same pre-existing sources the old dashboard-style /hsk page and
 * Home already used (HSK_LEVEL_INFO, getVocabularyCountByLevel) — no
 * hardcoded duplicate copy. The reference mockup's cards themselves don't
 * visually show the count, but the task's own written content spec lists
 * it per level explicitly, so it's kept as a small, visually subordinate
 * line under the description rather than dropped.
 */
export function HskLevelGrid() {
  return (
    <section className="flex flex-col gap-6">
      <div className="flex flex-col gap-1.5">
        <h2 className="font-ui text-[26px] font-bold leading-tight text-[#0F172A] dark:text-night-text sm:text-[28px]">
          Chọn cấp độ HSK
        </h2>
        <p className="font-ui text-[16px] text-[#343536] dark:text-night-muted">
          Mỗi cấp độ là một bước tiến gần hơn đến mục tiêu của bạn.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {HSK_LEVELS.map((level) => {
          const color = HSK_LEVEL_HEX[level];
          const info = HSK_LEVEL_INFO[level];
          const count = getVocabularyCountByLevel(level);
          return (
            <Link
              key={level}
              href={`/hsk/${level}?from=hsk`}
              className="group flex overflow-hidden rounded-2xl border bg-white transition-transform hover:-translate-y-0.5 dark:bg-night-surface"
              style={{ borderColor: color }}
            >
              <div className="relative w-[34%] shrink-0">
                <Image
                  src={`/hsk-${level}-illustration.png`}
                  alt=""
                  fill
                  aria-hidden
                  sizes="(min-width: 1024px) 140px, (min-width: 640px) 33vw, 34vw"
                  className="object-cover"
                  style={{ backgroundColor: `${color}14` }}
                />
              </div>

              {/* `isolate` scopes the decorative number's negative
                  z-index to just this card, so it sinks behind the
                  title/badge/description here without also sinking below
                  the card's own opaque white background (and every other
                  card's, since without it the -z-10 was resolving all
                  the way up to the page's root stacking context). */}
              <div className="relative isolate flex flex-1 flex-col gap-2 p-5">
                <span
                  aria-hidden
                  className="pointer-events-none absolute right-4 top-2 -z-10 font-ui text-6xl font-bold leading-none"
                  style={{ color: `${color}1F` }}
                >
                  {level}
                </span>

                <h3 className="font-ui text-xl font-bold leading-none" style={{ color }}>
                  HSK {level}
                </h3>
                <span
                  className="font-ui w-fit rounded-full px-3 py-1 text-sm font-semibold"
                  style={{ backgroundColor: `${color}1A`, color }}
                >
                  {info.name}
                </span>
                {/* Alignment fix: a fixed 2-line min-height so the
                    description block (and, via mt-auto below, the word
                    count) sits at the same position regardless of a given
                    level's description being 1 or 2 lines — previously
                    this only lined up when every card sharing a grid row
                    happened to need the same number of lines (true today,
                    but not guaranteed to stay true), not by construction.
                    Line-break fix: a max-width narrow enough that HSK2's
                    short description ("Mở rộng vốn từ vựng cơ bản") wraps
                    to 2 lines like every other level's, instead of sitting
                    alone on 1 line at the column's full width — text/
                    wording unchanged, only the wrap point moves. */}
                <p className="font-ui min-h-[41px] max-w-[170px] text-[15px] leading-snug text-neutral-700 dark:text-night-muted">
                  {info.description}
                </p>
                <p className="font-ui mt-auto text-sm text-neutral-500 dark:text-night-muted">
                  {count.toLocaleString("vi-VN")} từ vựng
                </p>
              </div>
            </Link>
          );
        })}
      </div>
    </section>
  );
}
