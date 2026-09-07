/** Shared Home content-column width: Hero, Search, and the
 *  HSK/Radical/Practice band all align to this same value — wider than
 *  the shared `app/layout.tsx` <main>'s own `max-w-6xl`, which is why
 *  each escapes that shared constraint locally via the full-bleed
 *  technique rather than widening `<main>` for every other route. */
export const HOME_CONTENT_MAX_WIDTH = "max-w-[1180px]";

/**
 * Fixed visual frame for the hero artwork (Pass 03/04/05). The background
 * lives on its own absolutely-positioned layer with this exact,
 * state-independent height — `background-size: cover` is always computed
 * against these numbers, never against variable content height, so the
 * artwork can never rescale/re-crop.
 *
 * Pass 04: Search moved out of Hero entirely (now its own section in
 * page.tsx, between Hero and HSK) — Hero itself is now fully independent
 * of Search by construction, not just by a fixed-height frame.
 * Pass 05: desktop frame lowered 420px → 400px per review; mobile
 * unchanged at 350px.
 */
const HERO_FRAME_HEIGHT = "h-[350px] sm:h-[400px]";

/**
 * Home Hero (reference screenshots). Uses the exact supplied mountain /
 * cherry-blossom hero background asset at app/public/hero-bg.jpg, placed
 * as a CSS background-image (not recreated/approximated) on the
 * fixed-height frame layer described above.
 *
 * The headline/subtitle block is intentionally narrower than the full
 * 1180px column (~625px) — an editorial hero layout, text confined to
 * the left against the photo, not stretched edge-to-edge.
 *
 * Pass 14: H1 line-height 1.05 → 1.15 (font-size/weight/width/copy all
 * unchanged) — the two lines were reading as visually touching.
 * Pass 15: 1.15 → 1.22, same reasoning, still not enough separation.
 */
export function HomeHero() {
  return (
    <section
      className={`relative -mt-8 ml-[calc(50%-50vw)] mr-[calc(50%-50vw)] w-screen overflow-hidden bg-[#F9F9F5] ${HERO_FRAME_HEIGHT}`}
    >
      <div
        aria-hidden
        className={`pointer-events-none absolute inset-x-0 top-0 bg-cover bg-center bg-no-repeat ${HERO_FRAME_HEIGHT}`}
        style={{ backgroundImage: "url(/hero-bg.jpg)" }}
      />

      <div className={`relative mx-auto flex h-full flex-col justify-center px-4 sm:px-6 ${HOME_CONTENT_MAX_WIDTH}`}>
        <div className="flex max-w-[625px] flex-col gap-5">
          <h1 className="font-ui text-[38px] font-extrabold leading-[1.22] text-neutral-900 sm:text-[52px]">
            Học tiếng Trung
            <br />
            Theo cấp độ HSK
          </h1>
          <p className="font-ui text-[18px] leading-[1.5] text-neutral-700">
            Học từ mới, tra cứu dễ dàng và luyện tập mỗi ngày
            <br />
            để ghi nhớ lâu hơn.
          </p>
        </div>
      </div>
    </section>
  );
}
