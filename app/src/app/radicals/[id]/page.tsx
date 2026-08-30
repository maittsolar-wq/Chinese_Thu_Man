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
 * `?from=hsk` here means Radical Detail itself was reached from HSK (via
 * RadicalCard's hrefSuffix, see hsk/page.tsx) — the header already
 * detects that directly on this URL. What that alone can't cover is the
 * NEXT hop: related-vocabulary links here already carry their own
 * `?from=radical&radicalId=...` (needed by Vocabulary Detail's
 * breadcrumb, unrelated to and not overridden by this). So HSK origin is
 * carried forward as a second, independent `&hskContext=1` marker
 * appended to those links only when this page itself was reached with
 * `from=hsk` — never touching the `from` value Vocabulary Detail's
 * breadcrumb logic depends on.
 */
export default async function RadicalDetailPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ from?: string }>;
}) {
  const { id } = await params;
  const radical = getRadicalDetailById(id);
  if (!radical) notFound();

  const { from } = await searchParams;
  const vocabularyHrefSuffix = from === "hsk" ? "&hskContext=1" : "";

  return <RadicalDetailView radical={radical} vocabularyHrefSuffix={vocabularyHrefSuffix} />;
}
