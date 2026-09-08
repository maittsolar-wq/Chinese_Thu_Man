import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { VocabularyDetail } from "@/components/vocabulary/VocabularyDetail";
import type { BreadcrumbItem } from "@/components/ui/Breadcrumb";
import { getAllVocabulary, getVocabularyById } from "@/lib/data/vocabularyRepository";
import { getRadicalSummaryById } from "@/lib/data/radicalRepository";

export function generateStaticParams() {
  return getAllVocabulary().map((word) => ({ id: word.id }));
}

interface VocabularyDetailSearchParams {
  from?: "hsk" | "dictionary" | "radical";
  level?: string;
  radicalId?: string;
  q?: string;
  /** Navigation-completion pass (HSK flow): the `/hsk/[level]` page's own
   *  `?from=` origin ("home" | "hsk"), chained through only when
   *  `from=hsk` — see resolveHskBackHref below.
   *
   *  Navigation-completion pass (Home Search flow): also doubles as the
   *  "which dictionary-style search produced this link" distinguisher
   *  when paired with `from=dictionary` — `parent=home` means Home's own
   *  inline HomeSearch widget (see HomeSearch.tsx), NOT the header's
   *  DictionarySearchPopup (which never sets `parent` and keeps the
   *  existing frozen "Trang chủ > Tra cứu > word" breadcrumb). Same
   *  query slot, same meaning ("who is the true parent screen"), reused
   *  rather than inventing a second marker. */
  parent?: string;
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}): Promise<Metadata> {
  const { id } = await params;
  const word = getVocabularyById(id);
  return { title: word ? `${word.word} — Chinese Thu Man` : "Chinese Thu Man" };
}

/**
 * Breadcrumb source context per docs/DICTIONARY/DICTIONARY_SPEC.md §16:
 * "Trang chủ > HSK 1 > 学习" from HSK, "Trang chủ > Từ điển > 学习" from
 * Dictionary. Extended here with a Radical origin for the new
 * Radical Detail → Related Vocabulary flow, since Word Detail stays the
 * single shared implementation regardless of entry point.
 */
function buildBreadcrumb(
  word: { id: string; word: string; hskLevels: number[] },
  searchParams: VocabularyDetailSearchParams
): BreadcrumbItem[] {
  const home: BreadcrumbItem = { label: "Trang chủ", href: "/" };

  if (searchParams.from === "dictionary") {
    return [
      home,
      // Nav-facing label kept in sync with AppHeader's "Tra cứu" (renamed
      // from "Từ điển" in the navigation phase) — docs/DICTIONARY/
      // DICTIONARY_SPEC.md §16 still documents the pre-rename string,
      // this is a display-label sync only, no href/route change.
      { label: "Tra cứu", href: "/dictionary" },
      { label: word.word },
    ];
  }

  if (searchParams.from === "radical" && searchParams.radicalId) {
    const radical = getRadicalSummaryById(searchParams.radicalId);
    if (radical) {
      return [
        home,
        { label: "Bộ thủ", href: "/radicals" },
        { label: radical.radical, href: `/radicals/${radical.id}` },
        { label: word.word },
      ];
    }
  }

  const level =
    Number(searchParams.level) || word.hskLevels[0] || undefined;
  if (level) {
    return [
      home,
      { label: "HSK", href: "/hsk" },
      { label: `HSK ${level}`, href: `/hsk/${level}` },
      { label: word.word },
    ];
  }

  return [home, { label: word.word }];
}

const VALID_HSK_LEVELS = new Set(["1", "2", "3", "4", "5", "6"]);

/**
 * Navigation-completion pass (HSK flow): when Vocabulary Detail was
 * reached from an HSK level's own vocabulary list (`from=hsk`, always
 * paired with `level`), its breadcrumb (built above, unchanged) is
 * replaced with a source-aware "Quay lại" Back button instead — returning
 * to that exact `/hsk/[level]` page, with THAT page's own origin
 * preserved via `parent` (mirroring `/hsk/[level]`'s own
 * resolveBackHref: `parent=home` -> "/hsk/[level]?from=home",
 * `parent=hsk` -> "/hsk/[level]?from=hsk", missing/invalid `parent` ->
 * plain "/hsk/[level]"). Missing/invalid `level` falls back to "/hsk",
 * the canonical parent route. Dictionary and Radical origins are
 * untouched by this function — it's only ever consulted when
 * `from === "hsk"`.
 */
function resolveHskBackHref(level: string | undefined, parent: string | undefined): string {
  if (!level || !VALID_HSK_LEVELS.has(level)) return "/hsk";
  const parentSuffix = parent === "home" ? "?from=home" : parent === "hsk" ? "?from=hsk" : "";
  return `/hsk/${level}${parentSuffix}`;
}

export default async function VocabularyDetailPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<VocabularyDetailSearchParams>;
}) {
  const { id } = await params;
  const word = getVocabularyById(id);
  if (!word) notFound();

  const resolvedSearchParams = await searchParams;
  const breadcrumb = buildBreadcrumb(word, resolvedSearchParams);
  // Only two explicit flows get the Back button in place of the
  // breadcrumb: the HSK-level-list origin (unchanged from the HSK pass),
  // and now Home's own inline search widget — distinguished from the
  // header's DictionarySearchPopup (which also sets `from=dictionary`,
  // but never `parent=home`) by that same `parent` marker. Direct/
  // param-less access, the DictionarySearchPopup, and Radical origins all
  // fall through unchanged to buildBreadcrumb's existing branches above.
  const isHomeSearchFlow = resolvedSearchParams.from === "dictionary" && resolvedSearchParams.parent === "home";
  const backHref =
    resolvedSearchParams.from === "hsk"
      ? resolveHskBackHref(resolvedSearchParams.level, resolvedSearchParams.parent)
      : isHomeSearchFlow
        ? "/"
        : undefined;

  return <VocabularyDetail word={word} breadcrumb={breadcrumb} backHref={backHref} />;
}
