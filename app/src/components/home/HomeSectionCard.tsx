import Image from "next/image";
import type { ReactNode } from "react";

/**
 * Shared white "big card" wrapper (icon square + title + subtitle header,
 * optional right-aligned CTA, content below) — the HSK/Radical/Practice
 * sections in the Home reference all use this identical shell, factored
 * out once rather than duplicated three times. Card #FFFFFF, border
 * #E2E8F0.
 *
 * Pass 15: large-card shadow offset 10px → 2px (same #E2E8F0 color,
 * both light/dark), matched identically on HomeSearch's own feature-card
 * shell so all four large cards (Search/HSK/Radical/Practice) share one
 * shadow treatment.
 */
// No dark-mode palette was supplied for this redesign (all 3 reference
// screenshots are light-mode only) — the outer shell below reuses this
// app's existing, already-approved night-* tokens (see Card.tsx / tailwind
// config) rather than inventing new dark colors, so the section at least
// sits coherently on a dark page instead of staying a stray white block.
export function HomeSectionCard({
  iconSrc,
  iconBg,
  title,
  subtitle,
  cta,
  children,
}: {
  iconSrc: string;
  iconBg: string;
  title: string;
  subtitle: string;
  cta?: ReactNode;
  children: ReactNode;
}) {
  return (
    <section className="rounded-[22px] border border-[#E2E8F0] bg-white p-7 shadow-[0_2px_0_#E2E8F0] dark:border-night-border dark:bg-night-surface dark:shadow-[0_2px_0_#3a3a3a] sm:p-9">
      <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex items-start gap-4">
          <span
            className="flex h-[52px] w-[52px] shrink-0 items-center justify-center rounded-xl"
            style={{ backgroundColor: iconBg }}
          >
            <Image src={iconSrc} alt="" width={32} height={32} aria-hidden />
          </span>
          <div>
            <h2 className="font-ui text-[28px] font-bold leading-tight text-[#0F172A] dark:text-night-text sm:text-[30px]">
              {title}
            </h2>
            <p className="font-ui mt-1.5 whitespace-pre-line text-[17px] text-[#343536] dark:text-night-muted">
              {subtitle}
            </p>
          </div>
        </div>
        {cta}
      </div>

      <div className="mt-7">{children}</div>
    </section>
  );
}
