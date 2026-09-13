import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { LinkButton } from "@/components/ui/Button";
import { ArrowLeftIcon, HeadphonesIcon } from "@/components/ui/icons";
import { ListeningLessonGrid } from "@/components/listening/ListeningLessonGrid";
import { listeningRepository } from "@/lib/listening/listeningRepository";

export function generateStaticParams() {
  return listeningRepository.getLevels().map((level) => ({ level: level.id }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ level: string }>;
}): Promise<Metadata> {
  const { level: levelParam } = await params;
  const level = listeningRepository.getLevel(levelParam);
  return { title: level ? `${level.name} - Luyện nghe — Chinese Thu Man` : "Luyện nghe — Chinese Thu Man" };
}

export default async function ListeningLevelPage({ params }: { params: Promise<{ level: string }> }) {
  const { level: levelParam } = await params;
  const level = listeningRepository.getLevel(levelParam);
  if (!level) notFound();

  const lessons = listeningRepository.getLessons(level.id);

  return (
    <div className="flex flex-col gap-6">
      {/* No breadcrumb — "Quay lại" (back to /listening) is the only
          navigation-up control this screen needs, per the approved UI
          finalization pass. */}
      <LinkButton href="/listening" variant="neutral" className="font-ui h-12 w-fit rounded-xl px-6">
        <ArrowLeftIcon className="h-4 w-4" />
        Quay lại
      </LinkButton>

      <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        {/* Title sized to match `/hsk/[level]`'s own page title exactly
            (text-2xl font-bold, flat — no responsive escalation) — this
            page plays the exact same role (a per-level, paginated
            sub-listing) as that established HSK page. Description bumped
            to the standard 16px body-text size rather than that page's
            own smaller inline-tail value. */}
        <div className="flex flex-col gap-1">
          <h1 className="font-ui text-2xl font-bold text-[#0F172A] dark:text-night-text">
            {level.name} - Danh sách bài nghe
          </h1>
          <p className="font-ui text-base text-neutral-600 dark:text-night-muted">{level.listDescription}</p>
        </div>

        <div className="flex w-full items-center gap-3 rounded-2xl border border-[#E2E8F0] bg-primary-light px-5 py-4 dark:border-night-border dark:bg-primary-dark/20 lg:w-auto lg:min-w-[280px]">
          <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-white dark:bg-night-surface">
            <HeadphonesIcon className="h-5 w-5 text-primary dark:text-night-primary" />
          </span>
          <div className="flex flex-col">
            <span className="font-ui font-bold text-primary dark:text-night-primary">
              {level.name} · {level.lessonCount} bài nghe
            </span>
            <span className="font-ui text-sm text-primary/80 dark:text-night-muted">{level.description}</span>
          </div>
        </div>
      </div>

      <ListeningLessonGrid lessons={lessons} />
    </div>
  );
}
