import Image from "next/image";
import { PlayIcon } from "@/components/ui/icons";
import { formatDuration } from "@/lib/listening/format";
import { LISTENING_LEVEL_ACCENT } from "@/lib/listening/levelAccent";
import type { ListeningLesson } from "@/lib/listening/types";

/**
 * No real per-lesson thumbnails exist yet — every mock lesson leaves
 * `thumbnailUrl` unset, so this renders its OWN level's illustration
 * (LISTENING_LEVEL_ACCENT — the same asset used on the Listening Landing's
 * HSK cards) as a full-bleed background instead of a flat gray/tint block.
 * It's still honestly a placeholder (every lesson within a level shares
 * the same background painting), not real per-lesson photography — the
 * moment a lesson DOES carry a real `thumbnailUrl` (a later B2 Integration
 * phase), this same component renders that instead; no caller
 * (ListeningLessonCard, ListeningVideoPlayer's own frame) needs to change.
 * The 9:16 ratio itself (aspect-[9/16]) is the one thing that IS
 * load-bearing from the reference and is preserved exactly either way,
 * never cropped to 16:9.
 *
 * Identifying text (code/label/Chinese title) and the duration badge live
 * ON the thumbnail itself (large, high-contrast, on a dark plate) rather
 * than repeated again as separate text below the card — ListeningLessonCard
 * has no metadata underneath, so nothing is stated twice.
 */
export function ListeningLessonThumbnail({ lesson }: { lesson: ListeningLesson }) {
  const accent = LISTENING_LEVEL_ACCENT[lesson.level];

  return (
    <div className="relative flex aspect-[9/16] w-full flex-col overflow-hidden rounded-2xl">
      {lesson.thumbnailUrl ? (
        <Image
          src={lesson.thumbnailUrl}
          alt=""
          fill
          sizes="(min-width: 1024px) 220px, 45vw"
          className="object-cover"
        />
      ) : (
        <Image
          src={accent.illustration}
          alt=""
          fill
          aria-hidden
          sizes="(min-width: 1024px) 220px, 45vw"
          className="object-cover"
        />
      )}

      <span className="font-ui absolute right-2 top-2 rounded-md bg-black/70 px-2 py-1 text-sm font-semibold text-white">
        {formatDuration(lesson.durationSeconds)}
      </span>

      {/* Bottom info plate — code/label + Chinese title (the card's own
          title) sit here, on the thumbnail, at a size that reads clearly
          at a glance; nothing about the lesson is repeated below it.
          Code/label: 16px/700 (legible over the artwork — 12px read as too
          small). Chinese title: 24px/500 matching "Chinese normal text"
          (Noto Serif SC, 500) rather than the heavier 600 used for a
          compact list row like HskVocabularyRow — this is a card title,
          not a scan-list row. */}
      <div className="relative mt-auto flex items-end justify-between gap-2 bg-black/55 p-3">
        <div className="flex min-w-0 flex-col gap-0.5">
          <span className="font-ui text-base font-bold text-white/85">
            {lesson.code} - {lesson.label}
          </span>
          <span className="font-cjk truncate text-2xl font-medium leading-tight text-white">
            {lesson.chineseTitle}
          </span>
        </div>
        <span
          className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-white/95 shadow-card"
          aria-hidden="true"
        >
          <PlayIcon className="h-4 w-4 translate-x-[1px]" style={{ color: accent.color }} />
        </span>
      </div>
    </div>
  );
}
