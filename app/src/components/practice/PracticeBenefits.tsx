import Image from "next/image";

/**
 * "Vì sao nên luyện tập?" panel — reintroduces the 4-claim marketing panel
 * that a prior phase deliberately removed (see the comment this replaced
 * in app/practice/page.tsx) because nothing in the product backs claims
 * like adaptive review or progress tracking. This phase's brief explicitly
 * asks for this exact section back, copy included, using the newly
 * supplied benefit icons — flagged here and in the task's final report
 * rather than silently reintroducing it, but implemented as directed
 * since this is a direct, explicit instruction (not an invented feature).
 */
const BENEFITS = [
  {
    icon: "/icons/benefit-smart-review.png",
    iconBg: "#2563EB1A",
    title: "Ôn tập thông minh",
    description: "Hệ thống sẽ ưu tiên các từ bạn chưa thuộc và từ bạn hay trả lời sai.",
  },
  {
    icon: "/icons/benefit-personalized.png",
    iconBg: "#16A34A1A",
    title: "Cá nhân hóa",
    description: "Bài tập phù hợp với trình độ của bạn.",
  },
  {
    icon: "/icons/benefit-progress.png",
    iconBg: "#7C3AED1A",
    title: "Theo dõi tiến độ",
    description: "Giúp bạn thấy sự tiến bộ mỗi ngày.",
  },
  {
    icon: "/icons/benefit-anywhere.png",
    iconBg: "#F43F5E1A",
    title: "Học mọi lúc mọi nơi",
    description: "Luyện tập nhanh chóng trên mọi thiết bị.",
  },
] as const;

export function PracticeBenefits() {
  return (
    <section className="rounded-2xl border border-[#E2E8F0] bg-white p-6 dark:border-night-border dark:bg-night-surface sm:p-8">
      <h2 className="font-ui text-2xl font-bold text-[#0F172A] dark:text-night-text">Vì sao nên luyện tập?</h2>

      <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2">
        {BENEFITS.map((benefit) => (
          <div key={benefit.title} className="flex items-start gap-4">
            {/* Final visual-fix pass: icon container restored (compact
                pastel-tinted rounded square, matching the Practice cards'
                own treatment) — a prior pass removed it for a different,
                self-contained icon set; this one is a bare glyph. */}
            <span
              className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl"
              style={{ backgroundColor: benefit.iconBg }}
            >
              <Image src={benefit.icon} alt="" width={24} height={24} aria-hidden />
            </span>
            {/* max-w keeps the longest description ("Ôn tập thông minh")
                from wrapping into an unbalanced long-line/short-line pair
                — applied uniformly to all four items so they still read
                as one even grid, not one item narrower than the rest. */}
            <div className="flex max-w-[260px] flex-col gap-0.5">
              <h3 className="font-ui text-base font-bold text-[#0F172A] dark:text-night-text">
                {benefit.title}
              </h3>
              <p className="font-ui text-[15px] leading-snug text-neutral-600 dark:text-night-muted">
                {benefit.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
