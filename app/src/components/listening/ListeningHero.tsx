import Image from "next/image";
import { HeadphonesIcon, CheckCircleIcon, TargetIcon, ClockIcon } from "@/components/ui/icons";

const FEATURE_POINTS = [
  { icon: CheckCircleIcon, title: "Thực tế", description: "Gần gũi cuộc sống" },
  { icon: TargetIcon, title: "Hiệu quả", description: "Nghe hiểu, phản xạ tốt hơn" },
  { icon: ClockIcon, title: "Mọi lúc, mọi nơi", description: "Trên máy tính, điện thoại" },
];

function HeroBadgeHeadingDescription() {
  return (
    <>
      <span className="font-ui mx-auto inline-flex w-fit items-center gap-2 rounded-full bg-primary-light px-4 py-1.5 text-sm font-semibold text-primary dark:bg-primary-dark/40 dark:text-night-primary lg:mx-0">
        <HeadphonesIcon className="h-4 w-4" />
        Luyện nghe
      </span>
      {/* Sized to match the established Home/HSK Hero H1 exactly
          (HomeHero.tsx / HskHero.tsx: text-[38px] sm:text-[52px] font-
          extrabold) — this hero shares the same "full-bleed banner" role,
          so it uses the same scale rather than a smaller one invented for
          Listening specifically. */}
      <h1 className="font-ui flex flex-col text-[38px] font-extrabold leading-[1.2] text-[#0F172A] dark:text-night-text sm:text-[52px]">
        <span>Luyện nghe</span>
        <span className="text-primary dark:text-night-primary">Tiếng Trung qua video</span>
      </h1>
      <p className="font-ui text-[18px] leading-[1.5] text-[#343536] dark:text-night-muted">
        Học qua những đoạn hội thoại thực tế, gần gũi với cuộc sống, giúp bạn nghe hiểu và phản xạ tự
        nhiên hơn.
      </p>
    </>
  );
}

function HeroFeaturePoints() {
  return (
    <div className="flex flex-col gap-4 pt-2 sm:flex-row sm:justify-center lg:justify-start">
      {FEATURE_POINTS.map(({ icon: Icon, title, description }) => (
        <div key={title} className="flex items-center gap-2.5 text-left">
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary-light dark:bg-primary-dark/30">
            <Icon className="h-5 w-5 text-primary dark:text-night-primary" />
          </span>
          <span className="flex flex-col">
            <span className="font-ui text-base font-semibold text-[#0F172A] dark:text-night-text">{title}</span>
            <span className="font-ui text-sm text-neutral-500 dark:text-night-muted">{description}</span>
          </span>
        </div>
      ))}
    </div>
  );
}

/**
 * Listening landing hero — two different structures per breakpoint,
 * per the approved reference:
 *
 * - Desktop (lg+): a genuinely full-bleed hero BAND — `/hero-listening-new
 *   .png` as the band's own background (edge-to-edge, no gutters, no
 *   wrapping card/border/shadow), with the real heading/description/
 *   feature-point text overlaid on its left side inside the site's normal
 *   content column. A FIXED frame height (matching the established
 *   PracticeHero/HskHero full-bleed-hero technique) rather than locking
 *   the frame to the image's own aspect ratio: at this image's very wide
 *   2151x714 (~3:1) ratio, an aspect-locked frame is too short at typical
 *   desktop widths for the overlaid text to fit. `object-cover` therefore
 *   does crop the image's left/right edges at narrower desktop widths —
 *   acceptable per the reference's own tolerance ("crop is fine as long as
 *   the video-preview visual itself is never cut") — `object-position`
 *   keeps that visual (~62% across the source) safely in frame.
 * - Mobile/tablet (< lg): stacked — text first (plain background), then
 *   the full image as its own block below, using `width`/`height` (no
 *   `fill`/crop) so its complete aspect ratio is always preserved. A
 *   fixed-height background crop has no room for a full text block at
 *   phone widths, so mobile intentionally does NOT reuse the desktop
 *   structure.
 */
export function ListeningHero() {
  return (
    <section className="relative -mt-8 ml-[calc(50%-50vw)] mr-[calc(50%-50vw)] w-screen overflow-hidden bg-surface-page dark:bg-night-bg">
      {/* Desktop: full-bleed background + overlaid text */}
      <div className="relative hidden h-[460px] lg:block xl:h-[520px]">
        <Image
          src="/hero-listening-new.png"
          alt=""
          fill
          sizes="100vw"
          className="object-cover"
          style={{ objectPosition: "62% center" }}
          priority
        />
        <div className="absolute inset-0 flex items-center">
          <div className="mx-auto w-full max-w-[1180px] px-6">
            {/* Widened to match HomeHero.tsx's own hero text column
                (max-w-[625px]) — needed once the H1 grew to match the real
                Home/HSK Hero scale (38/52px): at 52px, "Tiếng Trung qua
                video" measures ~581px and doesn't fit HskHero's narrower
                560px column, wrapping onto an unwanted 3rd line. */}
            <div className="flex max-w-[625px] flex-col gap-4">
              <HeroBadgeHeadingDescription />
              <HeroFeaturePoints />
            </div>
          </div>
        </div>
      </div>

      {/* Mobile/tablet: stacked, text then full (uncropped) image */}
      <div className="flex flex-col items-center gap-8 px-4 py-12 sm:px-6 sm:py-16 lg:hidden">
        <div className="flex max-w-[560px] flex-col gap-5 text-center">
          <HeroBadgeHeadingDescription />
          <HeroFeaturePoints />
        </div>
        <div className="w-full">
          <Image
            src="/hero-listening-new.png"
            alt=""
            width={2151}
            height={714}
            sizes="100vw"
            className="h-auto w-full"
          />
        </div>
      </div>
    </section>
  );
}
