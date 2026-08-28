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
      { label: "Từ điển", href: "/dictionary" },
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

  return <VocabularyDetail word={word} breadcrumb={breadcrumb} />;
}
