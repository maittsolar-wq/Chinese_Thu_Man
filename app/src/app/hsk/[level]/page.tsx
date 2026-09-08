import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { LinkButton } from "@/components/ui/Button";
import { ArrowLeftIcon } from "@/components/ui/icons";
import { HskLevelVocabularyList } from "@/components/hsk/HskLevelVocabularyList";
import { getVocabularyByLevel, getVocabularyCountByLevel } from "@/lib/data/vocabularyRepository";
import { HSK_LEVEL_INFO } from "@/lib/hsk/hskLevelInfo";
import { HSK_LEVEL_HEX } from "@/lib/hsk/homePalette";
import type { HskLevel } from "@/lib/data/types";

const VALID_LEVELS = [1, 2, 3, 4, 5, 6];

function parseLevel(param: string): HskLevel | null {
  const value = Number(param);
  return VALID_LEVELS.includes(value) ? (value as HskLevel) : null;
}

export function generateStaticParams() {
  return VALID_LEVELS.map((level) => ({ level: String(level) }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ level: string }>;
}): Promise<Metadata> {
  const { level: levelParam } = await params;
  const level = parseLevel(levelParam);
  return { title: level ? `HSK ${level} — Chinese Thu Man` : "HSK — Chinese Thu Man" };
}

/**
 * Navigation-completion pass (HSK flow): the old "Trang chủ > HSK > HSK N"
 * Breadcrumb (which sat ABOVE an already-existing, previously-hardcoded
 * "Quay lại" -> /hsk button — a redundant double-nav) is gone. Only the
 * Back button remains, now source-aware instead of hardcoded: `?from=home`
 * (Home's own HSK cards) -> "/", `?from=hsk` (the /hsk overview's own
 * level cards) -> "/hsk", missing/invalid `from` (direct/bookmarked entry)
 * -> "/hsk", the canonical parent route. Same deterministic-query-param
 * pattern as Practice/Radical, no browser history.
 */
function resolveBackHref(from: string | undefined): string {
  if (from === "home") return "/";
  return "/hsk";
}

/**
 * Search here is live/client-side (HskLevelVocabularyList), scoped to
 * this level's own pool — no `?q=` searchParams anymore, no submit form.
 * `key={level}` on the client component forces a fresh mount (query
 * cleared, page reset to 1) whenever the level itself changes.
 */
export default async function HskLevelPage({
  params,
  searchParams,
}: {
  params: Promise<{ level: string }>;
  searchParams: Promise<{ from?: string }>;
}) {
  const { level: levelParam } = await params;
  const level = parseLevel(levelParam);
  if (!level) notFound();

  const { from } = await searchParams;
  const backHref = resolveBackHref(from);
  // Chained onto every Vocabulary Detail link this level's list renders,
  // so that Back from Vocabulary Detail can return to THIS exact level
  // page with its own origin preserved (/hsk/[level]?from=home|hsk), and
  // so the header's active-tab context survives that extra hop — see
  // vocabulary/[id]/page.tsx's resolveHskBackHref.
  const vocabularyParent = from === "home" ? "home" : from === "hsk" ? "hsk" : undefined;

  const words = getVocabularyByLevel(level);
  const info = HSK_LEVEL_INFO[level];
  const color = HSK_LEVEL_HEX[level];

  return (
    <div className="flex flex-col gap-6">
      <LinkButton href={backHref} variant="neutral" className="font-ui w-fit">
        <ArrowLeftIcon className="h-4 w-4" />
        Quay lại
      </LinkButton>

      <div className="flex items-center gap-4">
        {/* Bumped from h-14/w-14/text-xl (56px/20px) to h-16/w-16/text-2xl
            (64px/24px) per this pass's "số HSK 1-6 lớn hơn" requirement,
            and switched from the older generic accent.* palette
            (HSK_LEVEL_ACCENT_BG, e.g. #2563eb) to the canonical
            HSK_LEVEL_HEX brand colors already used by Home/`/hsk`'s own
            level cards and the frozen colored HSK badges (#015291 etc.) —
            one consistent per-level color everywhere, not two competing
            palettes. */}
        <span
          className="flex h-16 w-16 shrink-0 items-center justify-center rounded-lg text-2xl font-bold text-white"
          style={{ backgroundColor: color }}
        >
          {level}
        </span>
        <div className="flex flex-col gap-0.5">
          <h1 className="font-ui text-2xl font-bold text-neutral-900 dark:text-night-text">
            HSK {level}{" "}
            <span className="font-normal text-neutral-500 dark:text-night-muted">· {info.name}</span>
          </h1>
          <p className="font-ui text-sm text-neutral-600 dark:text-night-muted">
            {info.description} — {getVocabularyCountByLevel(level).toLocaleString("vi-VN")} từ vựng
          </p>
        </div>
      </div>

      <HskLevelVocabularyList key={level} words={words} level={level} vocabularyParent={vocabularyParent} />
    </div>
  );
}
