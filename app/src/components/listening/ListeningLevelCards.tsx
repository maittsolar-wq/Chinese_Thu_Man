import Image from "next/image";
import Link from "next/link";
import { ArrowRightIcon } from "@/components/ui/icons";
import { LISTENING_LEVEL_ACCENT } from "@/lib/listening/levelAccent";
import { listeningRepository } from "@/lib/listening/listeningRepository";

/**
 * Only the 3 levels with real (mock) lesson content — HSK 4-6 are
 * deliberately NOT rendered here at all (not even as disabled
 * placeholders), per the approved scope: this catalog has no lesson data
 * for those levels yet, and an empty-looking disabled card would be worse
 * than no card.
 *
 * Card composition (side illustration strip + content) mirrors
 * HskLevelGrid.tsx's own established pattern for `/hsk`'s level cards —
 * same idea (a real painted illustration, a colored border, a decorative
 * giant level number), applied with Listening's own dedicated per-level
 * assets/colors (LISTENING_LEVEL_ACCENT) instead of the site-wide
 * HSK_LEVEL_HEX + `/hsk-N-illustration.png` set.
 */
export function ListeningLevelCards() {
  return (
    <section className="flex flex-col gap-6">
      {/* Sized to match Home's own section heading hierarchy
          (HomeSectionCard.tsx: text-[28px] sm:text-[30px] font-bold,
          text-[17px] description). Left-aligned (no `text-center`) to
          match that same reference's own heading/description alignment —
          and HskLevelGrid.tsx's own "Chọn cấp độ HSK" heading on /hsk,
          literally the same heading text — neither centers this text; both
          are plain left-aligned blocks sitting flush with their page's own
          content edge, which this section already shares (no extra
          container was added/changed here, only the text-align). */}
      <div className="flex flex-col gap-1">
        <h2 className="font-ui text-[28px] font-bold leading-tight text-[#0F172A] dark:text-night-text sm:text-[30px]">
          Chọn cấp độ HSK
        </h2>
        <p className="font-ui text-[17px] text-neutral-600 dark:text-night-muted">
          Học từ cơ bản đến nâng cao với những bài nghe được thiết kế theo từng cấp độ.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
        {listeningRepository.getLevels().map((level) => {
          const accent = LISTENING_LEVEL_ACCENT[level.id];
          return (
            <Link
              key={level.id}
              href={`/listening/${level.id}`}
              className="group flex overflow-hidden rounded-2xl border bg-white transition-transform hover:-translate-y-0.5 dark:bg-night-surface"
              style={{ borderColor: accent.color }}
            >
              {/* The illustration container's own aspect ratio (3:4) is set
                  to match the source artwork (1086x1448 = exactly 3:4)
                  instead of a fixed percentage width — a flex row's default
                  `align-items: stretch` then makes this column exactly as
                  tall as the card, and its WIDTH is derived from that
                  height via `aspect-[3/4]`, so `object-cover` fills it
                  perfectly with zero cropping and zero letterboxing (a
                  mismatched fixed-width strip previously forced a choice
                  between the two). */}
              <div className="relative aspect-[3/4] shrink-0 self-stretch">
                <Image
                  src={accent.illustration}
                  alt=""
                  fill
                  aria-hidden
                  sizes="(min-width: 1024px) 220px, (min-width: 640px) 33vw, 36vw"
                  className="object-cover"
                />
              </div>

              <div className="relative isolate flex flex-1 flex-col gap-2 p-5">
                <span
                  aria-hidden
                  className="pointer-events-none absolute right-4 top-6 -z-10 font-ui text-5xl font-bold leading-none"
                  style={{ color: `${accent.color}1F` }}
                >
                  {level.hskLevel}
                </span>

                {/* text-xl/font-bold matches both HskLevelGrid's and
                    HomeHskGrid's own HSK-level card title exactly — 20px
                    is the established size for "HSK N" as a card title
                    across the site, not a Listening-specific choice. */}
                <h3 className="font-ui text-xl font-bold leading-none" style={{ color: accent.color }}>
                  {level.name}
                </h3>
                <span
                  className="font-ui w-fit rounded-full px-3 py-1 text-sm font-semibold"
                  style={{ backgroundColor: `${accent.color}1A`, color: accent.color }}
                >
                  {level.lessonCount} bài
                </span>
                <p className="font-ui max-w-[190px] flex-1 text-[15px] leading-snug text-neutral-700 dark:text-night-muted">
                  {level.description}
                </p>
                {/* `shrink-0` fix: without it, this span is a compressible
                    flex item inside the `flex-col` content column. HSK1's
                    description text ("Hội thoại cơ bản, chủ đề quen thuộc
                    trong cuộc sống hàng ngày.") is longer than HSK2/HSK3's,
                    so it wraps taller — on some widths that pushed the
                    column's natural content height right up against the
                    row's stretch-derived height (driven by the image
                    sibling's aspect-ratio), and the flex algorithm shrank
                    this circular button down to an oval (36x16 measured,
                    not 36x36) to make room. HSK2/HSK3 never hit that
                    squeeze with their shorter text, so their identical
                    className already rendered correctly — same style, same
                    component, made robust rather than forked per level. */}
                <span
                  className="flex h-9 w-9 shrink-0 items-center justify-center self-end rounded-full text-white transition-transform group-hover:translate-x-0.5"
                  style={{ backgroundColor: accent.color }}
                >
                  <ArrowRightIcon className="h-4 w-4" />
                </span>
              </div>
            </Link>
          );
        })}
      </div>
    </section>
  );
}
