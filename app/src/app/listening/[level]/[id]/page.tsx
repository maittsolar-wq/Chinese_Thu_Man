import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ListeningLessonDetailView } from "@/components/listening/ListeningLessonDetailView";
import { listeningRepository } from "@/lib/listening/listeningRepository";

export function generateStaticParams() {
  return listeningRepository.getLevels().flatMap((level) =>
    listeningRepository.getLessons(level.id).map((lesson) => ({ level: level.id, id: lesson.id }))
  );
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ level: string; id: string }>;
}): Promise<Metadata> {
  const { level: levelParam, id } = await params;
  const level = listeningRepository.getLevel(levelParam);
  const lesson = level ? listeningRepository.getLesson(level.id, id) : null;
  return {
    title: lesson ? `${lesson.code} - ${lesson.label} — Luyện nghe — Chinese Thu Man` : "Luyện nghe — Chinese Thu Man",
  };
}

export default async function ListeningLessonPage({
  params,
}: {
  params: Promise<{ level: string; id: string }>;
}) {
  const { level: levelParam, id } = await params;
  const level = listeningRepository.getLevel(levelParam);
  if (!level) notFound();

  const lesson = listeningRepository.getLesson(level.id, id);
  if (!lesson) notFound();

  const { previous, next } = listeningRepository.getAdjacentLessons(level.id, id);

  return <ListeningLessonDetailView lesson={lesson} level={level} previous={previous} next={next} />;
}
