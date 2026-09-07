/**
 * HSK page Hero (visual-redesign, "HOME VISUAL FIX PASS" sibling for the
 * HSK tab). Mirrors the exact same fixed-frame + full-bleed CSS
 * background-image technique already established and approved by
 * HomeHero.tsx — not re-derived from scratch, so the two hero sections
 * behave identically (same frame heights, same `-mt-8` header-flush
 * offset, same escape-`<main>`'s-max-width trick).
 *
 * The background artwork (app/public/hero-hsk.jpg) is the user-supplied
 * reference image's own hero band, extracted as-is: the reference was a
 * flattened design mockup with its headline text already baked into the
 * pixels, so the mountain/pagoda/HSK-book-stack/cherry-blossom artwork
 * itself could only be reused by removing that baked text — done via
 * inpainting (OpenCV TELEA) restricted to the plain-sky region the text
 * sat in, never touching the pagoda/books/blossoms pixels. The headline,
 * "HSK", and description below are real HTML, not part of the image —
 * exactly how HomeHero already separates copy from artwork.
 *
 * Mobile crop: this Hero's text block (2-line H1 + 2-line description)
 * is taller/wider than Home's own, and the source artwork was composed
 * for a wide desktop banner — at 375-430px, `background-size: cover`
 * only ever shows a ~29% horizontal slice of it (frame-width ÷ scaled
 * image-width), too narrow for any single crop position to clear the
 * pagoda/books entirely while the text column is still this wide. Rather
 * than shrink the text or crop the books/pagoda out of frame (both
 * against the brief), a soft scrim (`#F9F9F5` fading to transparent,
 * mobile-only) sits between the text and the artwork so whatever of the
 * pagoda/books ends up behind the text column stays legible-through
 * instead of clashing with it — the standard technique for this exact
 * "wide banner artwork behind a narrow mobile text column" problem.
 */
const HERO_FRAME_HEIGHT = "h-[350px] sm:h-[400px]";

export function HskHero() {
  return (
    <section
      className={`relative -mt-8 ml-[calc(50%-50vw)] mr-[calc(50%-50vw)] w-screen overflow-hidden bg-[#F9F9F5] ${HERO_FRAME_HEIGHT}`}
    >
      <div
        aria-hidden
        className={`pointer-events-none absolute inset-x-0 top-0 bg-cover bg-no-repeat sm:hidden ${HERO_FRAME_HEIGHT}`}
        style={{ backgroundImage: "url(/hero-hsk.jpg)", backgroundPosition: "62% center" }}
      />
      <div
        aria-hidden
        className={`pointer-events-none absolute inset-x-0 top-0 bg-cover bg-no-repeat max-sm:hidden ${HERO_FRAME_HEIGHT}`}
        style={{ backgroundImage: "url(/hero-hsk.jpg)", backgroundPosition: "78% center" }}
      />
      <div
        aria-hidden
        className="pointer-events-none absolute inset-y-0 left-0 w-[78%] bg-gradient-to-r from-[#F9F9F5] via-[#F9F9F5]/75 to-transparent sm:hidden"
      />

      <div className="relative mx-auto flex h-full max-w-[1180px] flex-col justify-center px-4 sm:px-6">
        <div className="flex max-w-[560px] flex-col gap-4">
          <h1 className="font-ui flex flex-col text-[38px] font-extrabold leading-[1.15] sm:text-[52px]">
            <span className="text-[#0F172A]">Học từ vựng</span>
            <span className="text-[#015291]">HSK</span>
          </h1>
          <p className="font-ui text-[18px] leading-[1.5] text-[#343536]">
            Học từ vựng theo 6 cấp độ HSK từ cơ bản đến nâng cao.
          </p>
        </div>
      </div>
    </section>
  );
}
