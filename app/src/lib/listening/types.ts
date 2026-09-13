import type { HskLevel } from "@/lib/data/types";

/**
 * Listening domain model — deliberately isolated from data/hsk/** and the
 * existing vocabularyRepository: this feature has its own catalog. UI
 * components (and the two dynamic routes) only ever see these types, not
 * whichever concrete source produced them (today: mockData.ts via
 * listeningRepository.ts; later: a real B2-backed catalog via the same
 * `ListeningRepository` interface — see listeningRepository.ts's own
 * comment for how that swap is meant to happen).
 *
 * Phase 1.5 shape check against the real per-lesson package
 * (video.mp4 / thumbnail.jpg / transcript.json / lesson.json):
 *  - `videoUrl` / `thumbnailUrl` were added to `ListeningLesson` (both
 *    optional, both unset by every mock lesson today) so the existing
 *    player/thumbnail components can read a real URL the moment the
 *    repository starts returning one, with no prop-shape change on either
 *    component — see ListeningVideoPlayer.tsx / ListeningLessonThumbnail.tsx.
 *  - `ListeningDialogueLine` was reshaped to match transcript.json's own
 *    `sentences[]` field names almost 1:1 (`id`, `start`, `end`, `chinese`,
 *    `pinyin`, `vietnamese`) instead of the ad-hoc `index`/`timestamp` pair
 *    it started with, so lib/listening/adapters.ts's transcript mapper is a
 *    near-passthrough rather than a renaming exercise. `end` is optional
 *    and not yet read by any UI logic (today's "active sentence" check only
 *    needs `start`) — kept because real data provides it and a real
 *    adapter shouldn't silently drop known fields.
 *  - `ListeningVocabularyItem` and the rest of `ListeningLesson` were left
 *    unchanged: lesson.json's exact schema hasn't been shared yet, so
 *    nothing here guesses at fields for it (see adapters.ts's comment).
 */

/** Route segment, e.g. "hsk1" — matches /listening/[level]. */
export type ListeningLevelId = "hsk1" | "hsk2" | "hsk3";

export interface ListeningLevel {
  id: ListeningLevelId;
  hskLevel: HskLevel;
  name: string;
  lessonCount: number;
  description: string;
  listDescription: string;
}

export interface ListeningDialogueLine {
  /** Stable id, e.g. "s01" — matches transcript.json's `sentences[].id`.
   *  Display order (the "1", "2", ... badge shown in the UI) comes from
   *  the dialogue array's own position, not a stored field. */
  id: string;
  /** Seconds from the start of the lesson — matches `sentences[].start`. */
  start: number;
  /** Seconds from the start of the lesson — matches `sentences[].end`.
   *  Optional: no current UI logic reads it (the "active sentence" check
   *  only needs `start`), kept for a lossless real-data mapping. */
  end?: number;
  chinese: string;
  pinyin: string;
  vietnamese: string;
}

export interface ListeningVocabularyItem {
  chinese: string;
  pinyin: string;
  meaningVi: string;
}

export interface ListeningLesson {
  /** URL-safe slug, e.g. "001-502" — matches /listening/[level]/[id] and
   *  the real B2 lesson folder name (e.g. `hsk2/001-502/`). */
  id: string;
  level: ListeningLevelId;
  hskLevel: HskLevel;
  /** Numeric lesson code shown before the label, e.g. "001". */
  code: string;
  /** Short label shown next to the code on the card, e.g. "502" / "好朋友". */
  label: string;
  chineseTitle: string;
  vietnameseTitle: string;
  /** Total lesson length in seconds — drives both the card duration badge
   *  and the detail player's total duration, kept as one source of truth
   *  so the two screens never disagree with each other. */
  durationSeconds: number;
  dialogue: ListeningDialogueLine[];
  vocabulary: ListeningVocabularyItem[];
  /** Real video source (from the lesson's `video.mp4` once B2 is wired).
   *  Unset (undefined/null) for every mock lesson today — every consumer
   *  falls back to its existing mock/placeholder rendering in that case,
   *  so adding this field changes no current behavior. B2 URL generation
   *  itself is out of scope for this phase. */
  videoUrl?: string | null;
  /** Real thumbnail source (from `thumbnail.jpg`) — same fallback rule as
   *  `videoUrl` above. */
  thumbnailUrl?: string | null;
}

/**
 * The one seam between the Listening UI and wherever lesson data actually
 * comes from. `listeningRepository.ts` implements this against mockData.ts
 * today; a later real/B2-backed implementation only has to satisfy this
 * same shape for every existing page/component to keep working unchanged.
 */
export interface ListeningRepository {
  getLevels(): ListeningLevel[];
  getLevel(id: string): ListeningLevel | null;
  getLessons(level: ListeningLevelId): ListeningLesson[];
  getLesson(level: ListeningLevelId, id: string): ListeningLesson | null;
  getAdjacentLessons(
    level: ListeningLevelId,
    id: string
  ): { previous: ListeningLesson | null; next: ListeningLesson | null };
}
