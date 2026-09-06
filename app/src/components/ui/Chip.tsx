import Link from "next/link";

/**
 * Lightweight tappable pill for a short Chinese word + pinyin pair —
 * introduced for the Related Words tab (Phase 02). A full bordered Card per
 * related word (the pre-redesign treatment) is heavier than 5–10 short
 * words need; a Chip keeps the Chinese text as the dominant element while
 * staying visually lighter than a list of cards.
 */
export function Chip({
  href,
  hanzi,
  pinyin,
}: {
  href: string;
  hanzi: string;
  pinyin: string;
}) {
  return (
    <Link
      href={href}
      className="inline-flex items-center gap-2 rounded-full border border-neutral-200 bg-white px-4 py-2 transition-colors hover:border-primary hover:bg-primary-light dark:border-night-border dark:bg-night-surface dark:hover:bg-night-input"
    >
      <span className="font-cjk text-base font-semibold text-neutral-900 dark:text-night-text">
        {hanzi}
      </span>
      <span className="text-xs text-neutral-500 dark:text-night-muted">{pinyin}</span>
    </Link>
  );
}
