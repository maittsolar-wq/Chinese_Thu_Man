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
 * `?from=hsk` (direct entry, no longer produced by any current link — see
 * below) or `parent=hsk` (via the Radical Index) both mean HSK is the
 * ultimate origin of this visit — the header already detects either
 * directly on this URL. What that alone can't cover is the NEXT hop:
 * related-vocabulary links here already carry their own
 * `?from=radical&radicalId=...` (needed by Vocabulary Detail's
 * breadcrumb, unrelated to and not overridden by this). So HSK origin is
 * carried forward as a second, independent `&hskContext=1` marker
 * appended to those links only when this page's origin resolves to HSK —
 * never touching the `from` value Vocabulary Detail's breadcrumb logic
 * depends on.
 *
 * Navigation-completion pass: Radical Detail's immediate parent is now
 * distinguished from its ultimate origin. Two real entry shapes exist:
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
 * Anything unrecognized (missing/invalid `from`, or `from=radicals` with
 * no/invalid `parent`) safely falls back to "/radicals", the canonical
 * parent route.
 */
function resolveBackHref(from: string | undefined, parent: string | undefined): string {
  if (from === "home") return "/";
  if (from === "hsk") return "/hsk";
  if (from === "radicals") {
    if (parent === "home") return "/radicals?from=home";
    if (parent === "hsk") return "/radicals?from=hsk";
    return "/radicals";
  }
  return "/radicals";
}

export default async function RadicalDetailPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ from?: string; parent?: string }>;
}) {
  const { id } = await params;
  const radical = getRadicalDetailById(id);
  if (!radical) notFound();

  const { from, parent } = await searchParams;
  const hskOrigin = from === "hsk" || parent === "hsk";
  const vocabularyHrefSuffix = hskOrigin ? "&hskContext=1" : "";
  const backHref = resolveBackHref(from, parent);

  return (
    <RadicalDetailView radical={radical} vocabularyHrefSuffix={vocabularyHrefSuffix} backHref={backHref} />
  );
}
