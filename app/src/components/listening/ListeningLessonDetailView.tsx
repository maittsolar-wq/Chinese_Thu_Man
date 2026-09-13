"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import clsx from "clsx";
import { LinkButton } from "@/components/ui/Button";
import {
  ArrowLeftIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  MessageListIcon,
  BookOpenIcon,
  PencilIcon,
} from "@/components/ui/icons";
import { formatDuration } from "@/lib/listening/format";
import { ListeningVideoPlayer, PLAYBACK_SPEEDS } from "./ListeningVideoPlayer";
import type { ListeningLesson, ListeningLevel } from "@/lib/listening/types";

type TabId = "content" | "vocabulary" | "notes";

const TABS: { id: TabId; label: string; icon: typeof MessageListIcon }[] = [
  { id: "content", label: "Nội dung", icon: MessageListIcon },
  { id: "vocabulary", label: "Từ vựng", icon: BookOpenIcon },
  { id: "notes", label: "Ghi chú", icon: PencilIcon },
];

/**
 * Owns the whole Lesson Detail screen's interactive state — a mock,
 * fully-client player (no real <video>/audio source; a later B2
 * Integration phase wires that up), a 3-tab content panel, and prev/next.
 * All state here is local/UI-only per this phase's explicit scope (no
 * persistence, no real transcript sync backend). No favorite control:
 * there's no persistent "favorite lessons" storage feature behind it, so
 * one isn't shown here (or on the lesson cards) — see ListeningLessonCard's
 * own comment.
 */
export function ListeningLessonDetailView({
  lesson,
  level,
  previous,
  next,
}: {
  lesson: ListeningLesson;
  level: ListeningLevel;
  previous: ListeningLesson | null;
  next: ListeningLesson | null;
}) {
  const [currentTime, setCurrentTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState<(typeof PLAYBACK_SPEEDS)[number]>(1);
  const [activeTab, setActiveTab] = useState<TabId>("content");
  const [notes, setNotes] = useState("");

  // Reset all per-lesson state on navigation to a different lesson (via
  // Previous/Next) so nothing bleeds across lessons.
  useEffect(() => {
    setCurrentTime(0);
    setIsPlaying(false);
    setActiveTab("content");
    setNotes("");
  }, [lesson.id]);

  // Mock playback clock: advances currentTime once per second (scaled by
  // the selected speed), stopping automatically at the lesson's end. No
  // real media element — this is purely UI state for demonstrating the
  // player controls, per this phase's explicit "no real video hosting" scope.
  useEffect(() => {
    if (!isPlaying) return;
    const interval = setInterval(() => {
      setCurrentTime((prev) => {
        const nextTime = prev + speed;
        if (nextTime >= lesson.durationSeconds) {
          setIsPlaying(false);
          return lesson.durationSeconds;
        }
        return nextTime;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [isPlaying, speed, lesson.durationSeconds]);

  const activeDialogueIndex = useMemo(() => {
    let active = 0;
    lesson.dialogue.forEach((line, index) => {
      if (currentTime >= line.start) active = index;
    });
    return active;
  }, [currentTime, lesson.dialogue]);

  function handleSeek(seconds: number) {
    setCurrentTime(Math.max(0, Math.min(lesson.durationSeconds, seconds)));
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Source-aware "Quay lại" back to exactly the level list this lesson
          was opened from — no breadcrumb (removed per the approved UI
          finalization pass: this one button is the only navigation-up
          control this screen needs). */}
      <LinkButton href={`/listening/${level.id}`} variant="neutral" className="font-ui h-12 w-fit rounded-xl px-6">
        <ArrowLeftIcon className="h-4 w-4" />
        Quay lại
      </LinkButton>

      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div className="flex flex-col gap-1">
          {/* Title is code + Chinese title ONLY — `lesson.label` (the
              lesson list card's own short code, e.g. "502"/"超市") is
              deliberately NOT repeated here: for several mock lessons
              `label` and `chineseTitle` are identical strings, which used
              to render as a literal duplicate ("030 - 在超市 在超市").
              Sized as a Practice/HSK SUBPAGE title (PracticeConfigView's
              own "Chọn nghĩa" H1: text-3xl sm:text-4xl font-bold), not a
              Home/HSK Hero H1 — this screen is one level deeper than the
              Hero-scale Listening Landing, the same relationship a Practice
              exercise subpage has to Practice's own Hero. */}
          <h1 className="font-ui text-3xl font-bold text-[#0F172A] dark:text-night-text sm:text-4xl">
            {lesson.code} - <span className="font-cjk">{lesson.chineseTitle}</span>
          </h1>
          <p className="font-ui text-base text-neutral-600 dark:text-night-muted">{lesson.vietnameseTitle}</p>
        </div>

        <div className="flex shrink-0 flex-wrap items-center gap-2">
          {previous ? (
            <Link
              href={`/listening/${level.id}/${previous.id}`}
              className="font-ui flex h-11 items-center gap-1 rounded-xl border border-[#E2E8F0] px-4 text-sm font-semibold text-neutral-700 hover:bg-neutral-50 dark:border-night-border dark:text-night-muted dark:hover:bg-night-input"
            >
              <ChevronLeftIcon className="h-4 w-4" />
              Bài trước
            </Link>
          ) : (
            <span className="font-ui flex h-11 cursor-not-allowed items-center gap-1 rounded-xl border border-[#E2E8F0] px-4 text-sm font-semibold text-neutral-300 dark:border-night-border dark:text-night-border">
              <ChevronLeftIcon className="h-4 w-4" />
              Bài trước
            </span>
          )}
          {next ? (
            <Link
              href={`/listening/${level.id}/${next.id}`}
              className="font-ui flex h-11 items-center gap-1 rounded-xl border border-[#E2E8F0] px-4 text-sm font-semibold text-neutral-700 hover:bg-neutral-50 dark:border-night-border dark:text-night-muted dark:hover:bg-night-input"
            >
              Bài tiếp theo
              <ChevronRightIcon className="h-4 w-4" />
            </Link>
          ) : (
            <span className="font-ui flex h-11 cursor-not-allowed items-center gap-1 rounded-xl border border-[#E2E8F0] px-4 text-sm font-semibold text-neutral-300 dark:border-night-border dark:text-night-border">
              Bài tiếp theo
              <ChevronRightIcon className="h-4 w-4" />
            </span>
          )}
        </div>
      </div>

      <div className="flex flex-col gap-8 lg:flex-row lg:items-start">
        <ListeningVideoPlayer
          lesson={lesson}
          currentTime={currentTime}
          isPlaying={isPlaying}
          speed={speed}
          onTogglePlay={() => setIsPlaying((prev) => !prev)}
          onSeek={handleSeek}
          onSpeedChange={setSpeed}
        />

        <div className="flex w-full flex-col gap-4 rounded-3xl border border-[#E2E8F0] bg-white p-5 dark:border-night-border dark:bg-night-surface sm:p-6">
          <div role="tablist" aria-label="Nội dung bài nghe" className="flex gap-1 overflow-x-auto border-b border-neutral-200 dark:border-night-border">
            {TABS.map(({ id, label, icon: Icon }) => {
              const isActive = id === activeTab;
              return (
                <button
                  key={id}
                  type="button"
                  role="tab"
                  aria-selected={isActive}
                  onClick={() => setActiveTab(id)}
                  className={clsx(
                    // Matches the shared Tabs.tsx component's own tab-strip
                    // typography exactly (text-sm font-semibold) — the
                    // established site-wide tab treatment (Vocabulary
                    // Detail, etc.), not a Listening-specific size.
                    "font-ui flex shrink-0 items-center gap-1.5 whitespace-nowrap border-b-2 px-3 py-2.5 text-sm font-semibold transition-colors",
                    isActive
                      ? "border-primary text-primary dark:text-night-primary"
                      : "border-transparent text-neutral-500 hover:text-primary dark:text-night-muted"
                  )}
                >
                  <Icon className="h-4 w-4" />
                  {label}
                </button>
              );
            })}
          </div>

          {activeTab === "content" && (
            <div className="flex flex-col gap-3">
              <h2 className="font-ui text-2xl font-bold text-[#0F172A] dark:text-night-text">
                Hội thoại ({lesson.dialogue.length} câu)
              </h2>
              <div className="flex flex-col gap-2">
                {lesson.dialogue.map((line, index) => {
                  const isActive = index === activeDialogueIndex;
                  return (
                    <button
                      key={line.id}
                      type="button"
                      onClick={() => handleSeek(line.start)}
                      aria-current={isActive ? "true" : undefined}
                      className={clsx(
                        "flex w-full items-start gap-3 rounded-xl border px-4 py-3 text-left transition-colors",
                        isActive
                          ? "border-primary bg-primary-light dark:border-night-primary dark:bg-primary-dark/20"
                          : "border-[#E2E8F0] bg-white hover:bg-neutral-50 dark:border-night-border dark:bg-night-surface dark:hover:bg-night-input"
                      )}
                    >
                      <span
                        className={clsx(
                          "font-ui flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold",
                          isActive
                            ? "bg-primary text-white"
                            : "bg-neutral-100 text-neutral-600 dark:bg-night-input dark:text-night-muted"
                        )}
                      >
                        {index + 1}
                      </span>
                      {/* Chinese: 24px flat / Noto Serif SC / 500 ("Chinese
                          normal text" reference). Pinyin/Vietnamese: 16px
                          Be Vietnam Pro / 400 — pinyin keeps the site-wide
                          italic + primary-blue treatment (Vocabulary
                          Detail, HskVocabularyRow, Practice's own exercise
                          prompt all use it), just corrected back to 16px. */}
                      <span className="flex flex-1 flex-col gap-0.5">
                        <span className="font-cjk text-2xl font-medium text-[#0F172A] dark:text-night-text">
                          {line.chinese}
                        </span>
                        <span className="font-ui text-base italic text-primary dark:text-night-primary">
                          {line.pinyin}
                        </span>
                        <span className="font-ui text-base text-neutral-700 dark:text-night-muted">
                          {line.vietnamese}
                        </span>
                      </span>
                      <span className="font-ui shrink-0 text-sm text-neutral-400 dark:text-night-muted">
                        {formatDuration(line.start)}
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {activeTab === "vocabulary" && (
            <div className="flex flex-col gap-3">
              <h2 className="font-ui text-2xl font-bold text-[#0F172A] dark:text-night-text">Từ vựng</h2>
              <div className="flex flex-col divide-y divide-neutral-200 rounded-xl border border-[#E2E8F0] dark:divide-night-border dark:border-night-border">
                {lesson.vocabulary.map((item) => (
                  <div key={item.chinese} className="flex items-center justify-between gap-4 px-4 py-3">
                    <span className="font-cjk text-lg font-semibold text-[#0F172A] dark:text-night-text">
                      {item.chinese}
                    </span>
                    <span className="font-ui text-sm text-neutral-500 dark:text-night-muted">{item.pinyin}</span>
                    <span className="font-ui text-sm text-neutral-700 dark:text-night-muted">{item.meaningVi}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === "notes" && (
            <div className="flex flex-col gap-3">
              <h2 className="font-ui text-2xl font-bold text-[#0F172A] dark:text-night-text">Ghi chú</h2>
              <textarea
                value={notes}
                onChange={(event) => setNotes(event.target.value)}
                placeholder="Ghi chú của bạn cho bài nghe này..."
                rows={8}
                className="font-ui w-full resize-none rounded-xl border border-[#E2E8F0] bg-white p-4 text-sm text-neutral-900 outline-none placeholder:text-neutral-500 focus:border-primary focus:ring-1 focus:ring-primary dark:border-night-border dark:bg-night-input dark:text-night-text dark:placeholder:text-night-muted"
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
