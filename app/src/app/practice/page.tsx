import type { Metadata } from "next";
import Link from "next/link";
import Image from "next/image";
import { ArrowRightIcon } from "@/components/ui/icons";
import { PRACTICE_CARDS, practiceRoute, type PracticeType } from "@/lib/practice/types";
import { PracticeHero } from "@/components/practice/PracticeHero";
import { PracticeBenefits } from "@/components/practice/PracticeBenefits";

export const metadata: Metadata = { title: "Luyện tập — Chinese Thu Man" };

/**
 * Supplied practice icons (colored glyph on a tinted square) and card
 * background artworks — both new for this visual-redesign pass, kept as
 * local lookups inside this page only. `PRACTICE_CARDS` itself (title,
 * description, accent, route, and its own SVG `icon` field used elsewhere
 * — e.g. PracticeConfigView) is untouched: Home's own Practice section
 * (HomePracticeSection.tsx) already established this exact pattern of a
 * page-local icon map layered on top of the shared data, rather than
 * changing the shared `icon` field itself and risking every consumer.
 */
const PRACTICE_ICON_SRC: Record<PracticeType, string> = {
  meaning: "/icons/practice-icon-meaning.png",
  character: "/icons/practice-icon-character.png",
  flashcard: "/icons/practice-icon-flashcard.png",
  writing: "/icons/practice-icon-writing.png",
};

const PRACTICE_CARD_ART: Record<PracticeType, string> = {
  meaning: "/practice-card-meaning.png",
  character: "/practice-card-character.png",
  flashcard: "/practice-card-flashcard.png",
  writing: "/practice-card-writing.png",
};

/**
 * Optical icon sizing — the 4 icon containers stay identically 48×48px
 * (untouched); only the rendered glyph size inside each one changes. A
 * prior pass tried to equalize perceived weight by keeping every glyph's
 * bounding box at the same fill ratio and only nudging render size by a
 * few px — visually, Flashcard's graduation-cap glyph (lots of internal
 * transparent area within its own bounding box) still read smaller than
 * the others even at an equal box size. This pass sizes by eye against
 * the actual rendered screenshot instead of by bounding-box math: bigger,
 * deliberately unequal jumps, with Flashcard largest, "Chọn chữ Hán"
 * second, and "Chọn nghĩa"/"Luyện viết" (denser glyphs, read fuller at a
 * smaller size) left smallest. Not intended to be mathematically equal —
 * intended to look balanced.
 */
const PRACTICE_ICON_SIZE: Record<PracticeType, number> = {
  meaning: 29,
  character: 32,
  flashcard: 34,
  writing: 29,
};

/**
 * "Chọn dạng bài tập" card-refinement pass: exact locked hex values (§2 of
 * this pass's brief) — not the generic `accent-blue/green/purple/red`
 * Tailwind tokens `PRACTICE_CARD_ACCENT_STYLES` used before, and not
 * HSK_LEVEL_HEX imported from HSK's own module (these happen to be 3 of
 * those same 6 values plus one more, but this pass's brief gives them as
 * this page's own locked constants, so they're kept local rather than
 * reaching into another feature's file for a coincidental color match).
 * Local to this page only — PRACTICE_CARDS' own `accent` field and
 * PRACTICE_CARD_ACCENT_STYLES are untouched and still used elsewhere
 * (Home's Practice section, the Configuration screen).
 */
const CARD_ACCENT_HEX: Record<PracticeType, string> = {
  meaning: "#015291",
  character: "#65B482",
  flashcard: "#AB8BF2",
  writing: "#EE7F81",
};

/**
 * Practice landing (visual-redesign pass, matching the approved reference
 * — Hero + "Chọn dạng bài tập" cards + "Vì sao nên luyện tập?"). A prior
 * phase (Phase 05, see git history) deliberately removed the benefits
 * panel because no feature in the product actually backs claims like
 * adaptive review or progress tracking. This pass reintroduces it because
 * the current brief explicitly asks for it, copy included, by name and
 * reference screenshot — not something inferred or invented here. Flagged
 * in this pass's final report for visibility.
 *
 * Behavior unchanged: same 4 exercise types, same `practiceRoute()`
 * links, same `PRACTICE_CARDS` copy/accent data — only the presentation
 * (Hero, card art, icons, benefits section) is new.
 */
export default function PracticeHomePage() {
  return (
    <div>
      <PracticeHero />

      <div className="mt-10 flex flex-col gap-10">
        <section className="flex flex-col gap-6">
          <div className="flex flex-col gap-1.5">
            <h2 className="font-ui text-[26px] font-bold leading-tight text-[#0F172A] dark:text-night-text sm:text-[28px]">
              Chọn dạng bài tập
            </h2>
            <p className="font-ui text-[16px] text-[#343536] dark:text-night-muted">
              Lựa chọn phương pháp luyện tập phù hợp với mục tiêu của bạn
            </p>
          </div>

          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {PRACTICE_CARDS.map((card) => {
              const hex = CARD_ACCENT_HEX[card.type];
              return (
                <Link
                  key={card.type}
                  href={`${practiceRoute(card.type)}?from=practice`}
                  className="group relative flex aspect-[5/6] flex-col overflow-hidden rounded-2xl border-2 bg-white p-5 transition-transform hover:-translate-y-0.5 dark:bg-night-input"
                  style={{ borderColor: `${hex}33` }}
                >
                  <Image
                    src={PRACTICE_CARD_ART[card.type]}
                    alt=""
                    fill
                    aria-hidden
                    sizes="(min-width: 1024px) 280px, (min-width: 640px) 45vw, 90vw"
                    className="object-cover object-bottom"
                  />
                  {/* Vertical (not diagonal) fade: text is top-aligned and
                      can span the card's full width, so a top-opaque /
                      bottom-transparent gradient guarantees it always sits
                      on the opaque part regardless of line length — a
                      diagonal fade let the longest description's later
                      lines cross into the fading art and lose contrast,
                      worst in dark mode against the light watercolor art. */}
                  <div
                    aria-hidden
                    className="pointer-events-none absolute inset-0 bg-gradient-to-b from-white from-0% via-white/55 via-55% to-transparent to-88% dark:from-night-input dark:via-night-input/55"
                  />

                  {/* Final balance pass: content is no longer vertically
                      centered (that left a visible empty band below the
                      description) — it now sits naturally at the top,
                      with `flex-1` on this wrapper only pushing the
                      remaining space (where the artwork shows through)
                      down toward the Next button, not around the text.
                      Micro-spacing pass: icon→title gap widened 8px→18px
                      (icon position itself unchanged) so the title/
                      description group reads ~10px lower without the gap
                      itself looking like empty space — it's still a single
                      deliberate group, just given a bit more room to breathe
                      under the icon. */}
                  <div className="relative z-10 flex flex-1 flex-col gap-[18px]">
                    <span
                      className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl"
                      style={{ backgroundColor: `${hex}1A` }}
                    >
                      <Image
                        src={PRACTICE_ICON_SRC[card.type]}
                        alt=""
                        width={PRACTICE_ICON_SIZE[card.type]}
                        height={PRACTICE_ICON_SIZE[card.type]}
                        aria-hidden
                      />
                    </span>
                    <div className="flex flex-col gap-1">
                      <h3 className="font-ui text-2xl font-bold" style={{ color: hex }}>
                        {card.title}
                      </h3>
                      <p className="font-ui text-base leading-snug text-neutral-800 dark:text-night-muted">
                        {card.description}
                      </p>
                    </div>
                  </div>

                  {/* Next button: solid white disc + accent-colored arrow
                      (not a pale accent-tinted fill) — a small shadow
                      separates it from the artwork underneath, the same
                      treatment already used for HSK's own white arrow
                      button on top of its card illustrations. */}
                  <span
                    className="relative z-10 mt-auto flex h-9 w-9 shrink-0 items-center justify-center self-end rounded-full bg-white shadow-[0_1px_2px_rgba(15,23,42,0.15)] transition-transform group-hover:translate-x-0.5"
                    style={{ color: hex }}
                    aria-hidden
                  >
                    <ArrowRightIcon className="h-4 w-4" />
                  </span>
                </Link>
              );
            })}
          </div>
        </section>

        <PracticeBenefits />
      </div>
    </div>
  );
}
