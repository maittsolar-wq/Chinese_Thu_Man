import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { RadicalDetailView } from "@/components/radicals/RadicalDetailView";
import { getAllRadicals, getRadicalDetailById } from "@/lib/data/radicalRepository";

export function generateStaticParams() {
  return getAllRadicals().map((radical) => ({ id: radical.id }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}): Promise<Metadata> {
  const { id } = await params;
  const radical = getRadicalDetailById(id);
  return { title: radical ? `${radical.radical} — Chinese Thu Man` : "Chinese Thu Man" };
}

/**
 * Radical -> Vocabulary navigation-context fix: related-vocabulary links
 * on this page now reuse the SAME `from=related&returnTo=<exact current
 * URL>` mechanism Related Vocabulary already uses on Vocabulary Detail
 * itself (see `buildCurrentPageUrl` in vocabulary/[id]/page.tsx), instead
 * of the old standalone `?from=radical&radicalId=...[&hskContext=1]`
 * shape. `returnTo` is this page's own full canonical URL — id/route
 * param plus every `from`/`parent`/`returnTo` search param it was
 * actually loaded with — so Vocabulary Detail's Back button returns to
 * the EXACT Radical Detail page (not a reconstructed guess), and
 * `AppHeader`'s existing `unwrapToOriginalSourceParams` walks straight
 * through this `returnTo` (since its own `from` here is
 * "radicals"/"home"/"hsk"/"radical", never "related") to recover the
 * true origin (Home/HSK/Dictionary/Radical Index) with no further
 * changes needed there beyond also unwrapping `from=radical` — see
 * AppHeader.tsx. See buildCurrentRadicalUrl below.
 *
 * Vocabulary -> Radical navigation-context fix: a THIRD entry shape now
 * exists alongside the two below — `?from=radical&returnTo=<exact
 * Vocabulary Detail URL>`, produced by VocabularyDetail's "Bộ thủ & chữ
 * Hán" section (see VocabularyDetail.tsx's `radicalHrefSuffix`). Unlike
 * `from=home`/`from=radicals`, this `from` value names no destination by
 * itself — like Vocabulary Detail's own `from=related`, it's a pure
 * "come back to exactly this URL" wrapper, resolved by validating
 * `returnTo` the same safe way `resolveReturnToBackHref` already does in
 * vocabulary/[id]/page.tsx (same-origin relative path only, reused here
 * rather than re-implemented) and falling back to the existing generic
 * "/radicals" default when `returnTo` is missing/invalid — never a new
 * navigation state, never browser history.
 *
 * Navigation-completion pass: Radical Detail's immediate parent is now
 * distinguished from its ultimate origin. Two more real entry shapes
 * exist besides the one above:
 *
 * - `?from=home` — Home's 5 featured-radical cards link here directly
 *   (no Radical Index in between) -> Back goes straight to "/".
 * - `?from=radicals&parent=<home|hsk|(none)>` — reached via the Radical
 *   Index (itself reached from Home, HSK, or directly) -> Back returns to
 *   that SAME index with its own context preserved
 *   ("/radicals?from=home" / "/radicals?from=hsk" / "/radicals"), never
 *   skipping straight past it to Home/HSK — the index is the immediate
 *   parent, not Home/HSK themselves.
 *
 * `?from=hsk` alone (no `parent`) is kept as a legacy/defensive mapping
 * only — no current link produces it (HSK's only radical entry point is
 * now the Index), but resolving it to "/hsk" rather than falling through
 * to the generic fallback costs nothing and protects any old bookmarked
 * link.
 *
 * Deterministic query-param mapping throughout (same pattern as
 * PracticeConfigView's useConfigBackHref), never browser history.
 * Anything unrecognized (missing/invalid `from`, `from=radical` with a
 * missing/invalid `returnTo`, or `from=radicals` with no/invalid
 * `parent`) safely falls back to "/radicals", the canonical parent
 * route — this is also this page's existing, unchanged behavior for
 * direct/bookmarked `/radicals/<id>` access with no query at all.
 */
function resolveBackHref(from: string | undefined, parent: string | undefined, returnTo: string | undefined): string {
  if (from === "radical") {
    if (returnTo && returnTo.startsWith("/") && !returnTo.startsWith("//")) return returnTo;
    return "/radicals";
  }
  if (from === "home") return "/";
  if (from === "hsk") return "/hsk";
  if (from === "radicals") {
    if (parent === "home") return "/radicals?from=home";
    if (parent === "hsk") return "/radicals?from=hsk";
    return "/radicals";
  }
  return "/radicals";
}

/**
 * Reconstructs THIS page's own canonical URL (its `id` plus every search
 * param it was actually loaded with, `returnTo` included) so
 * related-vocabulary links can hand it to Vocabulary Detail as
 * `returnTo` — mirrors `buildCurrentPageUrl` in vocabulary/[id]/page.tsx
 * exactly, including the reason it's computed server-side from route
 * params/searchParams rather than `window.location`: it's what keeps
 * `/radicals/[id]` static. Including `returnTo` here (new in the
 * Vocabulary -> Radical pass) is what lets a bidirectional chain like
 * Vocabulary A -> Radical X -> Vocabulary B -> Radical Y -> Vocabulary C
 * preserve every hop: Radical X's OWN reconstructed URL below still
 * carries its `returnTo=<Vocabulary A URL>`, so when THAT URL is in turn
 * embedded as Vocabulary B's `returnTo` (by RadicalVocabularyByLevel),
 * B's Back button can resolve all the way back to Radical X, and
 * Radical X's own Back button still resolves to Vocabulary A.
 */
function buildCurrentRadicalUrl(
  id: string,
  from: string | undefined,
  parent: string | undefined,
  returnTo: string | undefined
): string {
  const params = new URLSearchParams();
  if (from) params.set("from", from);
  if (parent) params.set("parent", parent);
  if (returnTo) params.set("returnTo", returnTo);
  const qs = params.toString();
  return `/radicals/${id}${qs ? `?${qs}` : ""}`;
}

export default async function RadicalDetailPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ from?: string; parent?: string; returnTo?: string }>;
}) {
  const { id } = await params;
  const radical = getRadicalDetailById(id);
  if (!radical) notFound();

  const { from, parent, returnTo } = await searchParams;
  const backHref = resolveBackHref(from, parent, returnTo);
  const currentRadicalUrl = buildCurrentRadicalUrl(id, from, parent, returnTo);

  return (
    <RadicalDetailView radical={radical} relatedWordReturnTo={currentRadicalUrl} backHref={backHref} />
  );
}
