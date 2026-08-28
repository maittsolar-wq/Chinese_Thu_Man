import Link from "next/link";
import type { RadicalSummary } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";

export function RadicalCard({
  radical,
  vocabularyCount,
}: {
  radical: RadicalSummary;
  vocabularyCount: number;
}) {
  return (
    <Link href={`/radicals/${radical.id}`} className="block">
      <Card className="flex h-full flex-col gap-1 transition-shadow hover:shadow-md">
        <div className="flex items-start justify-between gap-2">
          <p className="text-3xl font-bold text-neutral-900">{radical.radical}</p>
          <span className="shrink-0 rounded-full bg-neutral-100 px-2 py-0.5 text-xs font-medium text-neutral-600">
            #{radical.kangxiIndex}
          </span>
        </div>
        <p className="text-sm text-neutral-600">{radical.pinyin}</p>
        <p className="text-sm text-neutral-800">
          {radical.nameVi} · {radical.meaningVi}
        </p>
        <p className="mt-auto pt-2 text-xs font-medium text-neutral-500">
          {vocabularyCount > 0
            ? `${vocabularyCount} từ vựng liên quan`
            : "Chưa có từ vựng liên quan"}
        </p>
      </Card>
    </Link>
  );
}
