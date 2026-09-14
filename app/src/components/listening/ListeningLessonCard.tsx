import Link from "next/link";
import { ListeningLessonThumbnail } from "./ListeningLessonThumbnail";
import type { ListeningLesson } from "@/lib/listening/types";

/**
 * No favorite/heart control — there is no persistent "favorite lessons"
 * storage feature (client or server) behind it, so showing one would be a
 * control with nowhere to save its result. Removed per the approved UI
 * finalization pass; re-add only alongside a real favorites feature.
 *
 * No title text below the thumbnail either — the code/label/Chinese title
 * are already shown, large and high-contrast, ON the thumbnail itself
 * (ListeningLessonThumbnail's own bottom info plate). Repeating them here
 * used to read as a literal duplicate for several mock lessons; only the
 * HSK badge (metadata the thumbnail doesn't carry) remains below.
 *
 * Uses the shared `HskLevelBadge` (components/ui/Badge.tsx) as-is, at its
 * own established 12px/600 — a typography-correction pass reverted an
 * earlier Listening-local override back to this shared component, since
 * the size difference wasn't significant enough to justify a scoped
 * duplicate of it.
 */
export function ListeningLessonCard({ lesson }: { lesson: ListeningLesson }) {
  return (
    <Link
      href={`/listening/${lesson.level}/${lesson.id}`}
      className="group flex flex-col rounded-2xl border border-[#E2E8F0] bg-white p-2 transition-shadow hover:shadow-card dark:border-night-border dark:bg-night-surface"
    >
      <ListeningLessonThumbnail lesson={lesson} />
    </Link>
  );
}
