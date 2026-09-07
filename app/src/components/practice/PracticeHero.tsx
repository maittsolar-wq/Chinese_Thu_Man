/**
 * Practice page Hero — same fixed-frame, full-bleed CSS background-image
 * technique already established by HomeHero.tsx and HskHero.tsx (not
 * re-derived): a `-mt-8` header-flush offset, the same escape-`<main>`'s
 * max-width trick, and the same frame heights. The background artwork
 * (app/public/hero-practice.jpg) is the latest user-supplied asset
 * (2508x627, an even wider panorama than the one it replaces), used
 * as-is via `background-size: cover` — that always preserves the image's
 * own aspect ratio and only ever crops, never stretches/distorts it, so
 * "preserve the original proportions" holds regardless of frame size.
 *
 * Mobile: same "wide banner art behind a narrow text column" clash as
 * HSK's hero (the flashcards/学 card sit close enough to the text column
 * that a plain crop-position fix alone left them touching) — same fix,
 * a mobile-only scrim between text and artwork plus a lighter crop
 * position, not a layout change.
 */
const HERO_FRAME_HEIGHT = "h-[350px] sm:h-[400px]";

export function PracticeHero() {
  return (
    <section
      className={`relative -mt-8 ml-[calc(50%-50vw)] mr-[calc(50%-50vw)] w-screen overflow-hidden bg-[#F9F9F5] ${HERO_FRAME_HEIGHT}`}
    >
      <div
        aria-hidden
        className={`pointer-events-none absolute inset-x-0 top-0 bg-cover bg-no-repeat sm:hidden ${HERO_FRAME_HEIGHT}`}
        style={{ backgroundImage: "url(/hero-practice.jpg)", backgroundPosition: "38% center" }}
      />
      <div
        aria-hidden
        className={`pointer-events-none absolute inset-x-0 top-0 bg-cover bg-no-repeat max-sm:hidden ${HERO_FRAME_HEIGHT}`}
        style={{ backgroundImage: "url(/hero-practice.jpg)", backgroundPosition: "72% center" }}
      />
      <div
        aria-hidden
        className="pointer-events-none absolute inset-y-0 left-0 w-[88%] bg-gradient-to-r from-[#F9F9F5] via-[#F9F9F5]/85 via-60% to-transparent sm:hidden"
      />

      <div className="relative mx-auto flex h-full max-w-[1180px] flex-col justify-center px-4 sm:px-6">
        <div className="flex max-w-[660px] flex-col gap-4">
          <h1 className="font-ui flex flex-col text-[26px] font-extrabold leading-[1.2] sm:text-[52px]">
            <span className="text-[#0F172A]">Luyện tập tiếng Trung</span>
            <span className="text-[#015291]">Hiệu quả Hơn Mỗi Ngày</span>
          </h1>
          <p className="font-ui text-[18px] leading-[1.5] text-[#343536]">
            Ôn tập từ vựng theo 6 cấp độ HSK với nhiều dạng bài tập thú vị, giúp bạn nhớ lâu hơn và sử dụng
            thành thạo hơn.
          </p>
        </div>
      </div>
    </section>
  );
}
