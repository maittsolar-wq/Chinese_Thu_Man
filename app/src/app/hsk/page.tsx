import type { Metadata } from "next";
import Link from "next/link";
import { Card } from "@/components/ui/Card";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { getVocabularyCountByLevel } from "@/lib/data/vocabularyRepository";
import type { HskLevel } from "@/lib/data/types";

export const metadata: Metadata = { title: "HSK — Chinese Thu Man" };

const HSK_LEVELS: HskLevel[] = [1, 2, 3, 4, 5, 6];

export default function HskOverviewPage() {
  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb items={[{ label: "Trang chủ", href: "/" }, { label: "HSK" }]} />
      <h1 className="text-2xl font-bold text-primary">HSK</h1>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {HSK_LEVELS.map((level) => (
          <Link key={level} href={`/hsk/${level}`} className="block">
            <Card className="flex flex-col gap-1 hover:shadow-md">
              <h2 className="text-xl font-semibold text-neutral-900">HSK {level}</h2>
              <p className="text-sm text-neutral-600">
                {getVocabularyCountByLevel(level).toLocaleString("vi-VN")} từ vựng
              </p>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
