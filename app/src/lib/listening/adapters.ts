import type { ListeningDialogueLine } from "./types";

/**
 * Pure raw-data -> domain-type mappers (Phase 1.5, architecture readiness
 * only). No I/O here — nothing fetches B2, nothing reads a real file; that
 * belongs to the later B2 Integration phase. This file exists so that,
 * once real transcript.json (and eventually lesson.json) content shows up,
 * turning it into `ListeningLesson`/`ListeningDialogueLine` is a matter of
 * calling an existing function, not inventing the mapping under time
 * pressure.
 *
 * transcript.json's shape:
 *   { version, lessonId, title, status, sentences: [{ id, start, end,
 *     chinese, pinyin, vietnamese }] }
 * `ListeningDialogueLine` (types.ts) was intentionally reshaped in this
 * same phase to use the exact same `id`/`start`/`end`/`chinese`/`pinyin`/
 * `vietnamese` field names, so this mapper is a near-passthrough rather
 * than a renaming exercise — see types.ts's own comment for why.
 *
 * lesson.json's exact schema has not been shared yet (only its filename
 * and its role — real per-lesson metadata — are known so far). Writing a
 * `mapLessonJsonToListeningLesson` mapper now would mean guessing at field
 * names for `chineseTitle`/`vietnameseTitle`/`code`/`label`/etc., which is
 * exactly the kind of invented-field speculation this phase's brief warns
 * against. That mapper should be added once lesson.json's real shape is
 * available — at that point it's the same small, mechanical exercise this
 * file's transcript mapper already demonstrates.
 */

export interface RawTranscriptSentence {
  id: string;
  start: number;
  end: number;
  chinese: string;
  pinyin: string;
  vietnamese: string;
}

export interface RawTranscript {
  version: number;
  lessonId: string;
  title: string;
  status: string;
  sentences: RawTranscriptSentence[];
}

export function mapTranscriptSentenceToDialogueLine(sentence: RawTranscriptSentence): ListeningDialogueLine {
  return {
    id: sentence.id,
    start: sentence.start,
    end: sentence.end,
    chinese: sentence.chinese,
    pinyin: sentence.pinyin,
    vietnamese: sentence.vietnamese,
  };
}

export function mapTranscriptToDialogue(transcript: RawTranscript): ListeningDialogueLine[] {
  return transcript.sentences.map(mapTranscriptSentenceToDialogueLine);
}
