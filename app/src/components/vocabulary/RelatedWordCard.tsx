import Link from "next/link";
import { Card } from "@/components/ui/Card";

/**
 * UI Foundation Phase — Related Words moves from a compact pill (`Chip`,
 * still used nowhere else after this change) to a proper editorial card:
 * Chinese word, pinyin, and meaning all visible at once, sized per the
 * approved type scale (28-32px Chinese / 15-16px pinyin+meaning) instead of
 * the pill's single 16px hanzi line with no meaning shown at all.
 *
 * `Chip.tsx` is left in place, unused, rather than deleted or repurposed —
 * this is a distinct visual contract (card vs. pill, meaning shown vs.
 * not), not a restyle of the same component.
 */
export function RelatedWordCard({
  href,
  hanzi,
  pinyin,
  meaningVi,
}: {
  href: string;
  hanzi: string;
  pinyin: string;
  meaningVi: string;
}) {
  return (
    <Link href={href} className="block h-full">
      <Card className="flex h-full flex-col gap-1 p-4 transition-colors hover:border-primary hover:bg-primary-wash dark:hover:border-night-primary dark:hover:bg-primary-dark/10 sm:p-5">
        <p className="font-cjk text-3xl font-normal leading-tight text-ink dark:text-night-text">
          {hanzi}
        </p>
        <p className="font-ui text-base italic text-primary dark:text-night-primary">{pinyin}</p>
        <p className="font-ui text-base text-ink-muted dark:text-night-muted">{meaningVi}</p>
      </Card>
    </Link>
  );
}
