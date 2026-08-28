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

export default async function RadicalDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const radical = getRadicalDetailById(id);
  if (!radical) notFound();

  return <RadicalDetailView radical={radical} />;
}
