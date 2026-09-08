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
  from?: "hsk" | "dictionary" | "radical" | "related";
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
   *  inline HomeSearch widget (see HomeSearch.tsx). Any OTHER `from=
   *  dictionary` (i.e. `parent` unset/not "home") means the header's
   *  global DictionarySearchPopup instead — see `returnTo` below and
   *  resolveReturnToBackHref. */
  parent?: string;
  /** Shared by two flows that both need "go back to exactly one specific
   *  prior URL", validated identically by resolveReturnToBackHref:
   *
   *  - Dictionary-popup Back/restore (`from=dictionary`, not Home Search):
   *    the header popup's own current page (pathname + its existing query
   *    string) at the moment a result was clicked, with
   *    `dictionaryOpen=true&dictQuery=<term>` already merged in — see
   *    DictionarySearchPopup.tsx's `buildResultHref`.
   *
   *  - Related Vocabulary Back pass (`from=related`): the PREVIOUS
   *    Vocabulary Detail page's own full URL (this same page's `id` +
   *    whatever `searchParams` IT was loaded with) — see this file's
   *    `buildCurrentPageUrl` and VocabularyDetail.tsx's Related Word
   *    links. Chains naturally for A -> B -> C: C's `returnTo` is B's
   *    full URL (which itself still carries `from=related&returnTo=<A>`
   *    inside it, single-encoded), so Back always walks exactly one hop
   *    at a time and each page's own origin context survives the whole
   *    chain without needing anything beyond the URL itself. */
  returnTo?: string;
}

/**
 * Related Vocabulary Back pass: reconstructs THIS page's own canonical
 * URL (its `id` plus every search param it was actually loaded with) so
 * VocabularyDetail can hand it to each Related Word link as that word's
 * own `returnTo` — one hop back, always exact, regardless of how many
 * `related` hops deep the chain already is. Passing the id/searchParams
 * through explicitly (rather than reading `window.location` — this
 * function runs server-side) is what keeps `/vocabulary/[id]` static:
 * no client-only API is needed to know "what page am I".
 */
function buildCurrentPageUrl(id: string, searchParams: VocabularyDetailSearchParams): string {
  const params = new URLSearchParams();
  if (searchParams.from) params.set("from", searchParams.from);
  if (searchParams.level) params.set("level", searchParams.level);
  if (searchParams.radicalId) params.set("radicalId", searchParams.radicalId);
  if (searchParams.parent) params.set("parent", searchParams.parent);
  if (searchParams.returnTo) params.set("returnTo", searchParams.returnTo);
  if (searchParams.q) params.set("q", searchParams.q);
  const qs = params.toString();
  return `/vocabulary/${id}${qs ? `?${qs}` : ""}`;
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
 *
 * Dictionary-popup Back/restore pass: the old `from === "dictionary"`
 * breadcrumb branch ("Trang chủ > Tra cứu > word") is gone — EVERY
 * `from=dictionary` value now resolves to a `backHref` instead (either
 * this function's own Home Search branch, or the new popup-restore
 * branch below), so this function is never actually called for a
 * dictionary origin anymore; VocabularyDetail only renders `breadcrumb`
 * when `backHref` is undefined.
 */
function buildBreadcrumb(
  word: { id: string; word: string; hskLevels: number[] },
  searchParams: VocabularyDetailSearchParams
): BreadcrumbItem[] {
  const home: BreadcrumbItem = { label: "Trang chủ", href: "/" };

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

/**
 * Shared by the dictionary-popup flow and the Related Vocabulary flow —
 * both hand this page a fully-formed `returnTo` (see the field's own
 * comment above), so resolving it here is just validation, not
 * reconstruction. Only a same-origin relative path (starts with exactly
 * one `/`, never `//`, which a browser would treat as protocol-relative
 * to an external host) is accepted; anything missing/malformed/absent —
 * a direct/bookmarked `/vocabulary/x?from=dictionary` (or `from=related`)
 * link with no `returnTo` included — falls back to `/`, the same safe
 * default `useConfigBackHref` (Practice) already uses for its own
 * missing/invalid source param.
 */
function resolveReturnToBackHref(returnTo: string | undefined): string {
  if (returnTo && returnTo.startsWith("/") && !returnTo.startsWith("//")) return returnTo;
  return "/";
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
  // Four explicit flows get the Back button in place of the breadcrumb:
  // the HSK-level-list origin (unchanged from the HSK pass), Home's own
  // inline search widget (`parent=home`), the header's global
  // DictionarySearchPopup (any OTHER `from=dictionary`, i.e. `parent`
  // unset/not "home"), and — new in this pass — Related Vocabulary
  // (`from=related`): always returns to the exact prior Vocabulary Detail
  // page via `returnTo`, never to Home/HSK/Dictionary directly, however
  // many `related` hops deep the chain is. Direct/param-less access and
  // Radical origins are the only ones still falling through to
  // buildBreadcrumb's existing branches.
  const isHomeSearchFlow = resolvedSearchParams.from === "dictionary" && resolvedSearchParams.parent === "home";
  const isDictionaryPopupFlow = resolvedSearchParams.from === "dictionary" && resolvedSearchParams.parent !== "home";
  const isRelatedFlow = resolvedSearchParams.from === "related";
  const backHref =
    resolvedSearchParams.from === "hsk"
      ? resolveHskBackHref(resolvedSearchParams.level, resolvedSearchParams.parent)
      : isHomeSearchFlow
        ? "/"
        : isDictionaryPopupFlow || isRelatedFlow
          ? resolveReturnToBackHref(resolvedSearchParams.returnTo)
          : undefined;

  // Handed to VocabularyDetail so ITS OWN Related Word links can each
  // carry "come back here" — this page's full URL (id + every search
  // param it was loaded with), not just its bare id. See
  // buildCurrentPageUrl's own comment for why this is computed
  // server-side rather than read from window.location.
  const currentPageUrl = buildCurrentPageUrl(id, resolvedSearchParams);

  return (
    <VocabularyDetail
      word={word}
      breadcrumb={breadcrumb}
      backHref={backHref}
      relatedWordReturnTo={currentPageUrl}
    />
  );
}
