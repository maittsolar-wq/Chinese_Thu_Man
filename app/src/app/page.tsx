import Link from "next/link";
import { Card } from "@/components/ui/Card";
import { LinkButton } from "@/components/ui/Button";
import {
  getTotalVocabularyCount,
  getVocabularyCountByLevel,
} from "@/lib/data/vocabularyRepository";
import { getAllRadicals } from "@/lib/data/radicalRepository";
import type { HskLevel } from "@/lib/data/types";

const HSK_LEVELS: HskLevel[] = [1, 2, 3, 4, 5, 6];

const FEATURES = [
  {
    href: "/hsk",
    title: "HSK",
    description: "Học từ vựng theo từng cấp độ HSK 1–6.",
  },
  {
    href: "/dictionary",
    title: "Từ điển",
    description: "Tra cứu nhanh theo chữ Hán, pinyin hoặc nghĩa tiếng Việt.",
  },
  {
    href: "/radicals",
    title: "Bộ thủ",
    description: "Khám phá 214 bộ thủ và từ vựng liên quan.",
  },
] as const;

export default function HomePage() {
  const totalVocabulary = getTotalVocabularyCount();
  const totalRadicals = getAllRadicals().length;

  return (
    <div className="flex flex-col gap-10">
      <section className="flex flex-col gap-3">
        <h1 className="text-3xl font-bold text-primary sm:text-4xl">
          Học từ vựng tiếng Trung theo chuẩn HSK
        </h1>
        <p className="max-w-2xl text-neutral-600">
          {totalVocabulary.toLocaleString("vi-VN")} từ vựng HSK 1–6 và{" "}
          {totalRadicals} bộ thủ, kèm nghĩa tiếng Việt.
        </p>
      </section>

      <section className="grid gap-4 sm:grid-cols-3">
        {FEATURES.map((feature) => (
          <Link key={feature.href} href={feature.href} className="block">
            <Card className="flex h-full flex-col gap-2 hover:shadow-md">
              <h2 className="text-lg font-semibold text-primary">{feature.title}</h2>
              <p className="text-sm text-neutral-600">{feature.description}</p>
            </Card>
          </Link>
        ))}
      </section>

      <section>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-neutral-600">
          Truy cập nhanh theo cấp độ HSK
        </h2>
        <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-6">
          {HSK_LEVELS.map((level) => (
            <LinkButton key={level} href={`/hsk/${level}`} variant="secondary">
              <span className="flex flex-col items-center gap-0.5">
                <span>HSK {level}</span>
                <span className="text-xs font-normal text-neutral-500">
                  {getVocabularyCountByLevel(level).toLocaleString("vi-VN")} từ
                </span>
              </span>
            </LinkButton>
          ))}
        </div>
      </section>
    </div>
  );
}
