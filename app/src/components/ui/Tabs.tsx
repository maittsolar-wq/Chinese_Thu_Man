"use client";

import { useRef, useState, type KeyboardEvent, type ReactNode } from "react";
import clsx from "clsx";

export interface TabItem {
  id: string;
  label: string;
  content: ReactNode;
}

/**
 * Generic, accessible tab set (WAI-ARIA "Tabs with Automatic Activation"
 * pattern: arrow keys move AND activate, matching native tab-strip
 * behavior). Introduced for the Vocabulary Detail redesign (Phase 02) but
 * intentionally has no Vocabulary Detail-specific knowledge — a reusable
 * primitive, not a one-off.
 *
 * All panels stay mounted (toggled via the `hidden` attribute) rather than
 * conditionally rendered, so a panel containing its own data-fetching
 * child (Stroke Order) keeps firing that fetch exactly when the page loads
 * — identical to its pre-redesign timing — instead of being deferred to
 * first tab-open, which would be a behavior change to preserve, not
 * introduce.
 *
 * The tab strip itself scrolls horizontally on narrow viewports — the same
 * `overflow-x-auto` interaction StrokeOrderViewer's step buttons already
 * use, not a new pattern to learn.
 */
export function Tabs({
  items,
  label,
  defaultId,
}: {
  items: TabItem[];
  /** Accessible name for the tablist, e.g. "Nội dung học tập". */
  label: string;
  defaultId?: string;
}) {
  const [activeId, setActiveId] = useState(defaultId ?? items[0]?.id);
  const tabRefs = useRef<Record<string, HTMLButtonElement | null>>({});

  function activate(id: string, focus: boolean) {
    setActiveId(id);
    if (focus) tabRefs.current[id]?.focus();
  }

  function handleKeyDown(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    let nextIndex: number | null = null;
    if (event.key === "ArrowRight") nextIndex = (index + 1) % items.length;
    else if (event.key === "ArrowLeft") nextIndex = (index - 1 + items.length) % items.length;
    else if (event.key === "Home") nextIndex = 0;
    else if (event.key === "End") nextIndex = items.length - 1;
    if (nextIndex === null) return;
    event.preventDefault();
    const next = items[nextIndex];
    if (next) activate(next.id, true);
  }

  return (
    <div className="flex flex-col gap-4">
      <div
        role="tablist"
        aria-label={label}
        className="flex gap-1 overflow-x-auto border-b border-neutral-200 dark:border-night-border"
      >
        {items.map((item, index) => {
          const isActive = item.id === activeId;
          return (
            <button
              key={item.id}
              ref={(el) => {
                tabRefs.current[item.id] = el;
              }}
              type="button"
              role="tab"
              id={`tab-${item.id}`}
              aria-selected={isActive}
              aria-controls={`panel-${item.id}`}
              tabIndex={isActive ? 0 : -1}
              onClick={() => activate(item.id, false)}
              onKeyDown={(event) => handleKeyDown(event, index)}
              className={clsx(
                "shrink-0 whitespace-nowrap rounded-t-md border border-b-0 border-transparent px-4 py-2.5 text-sm font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-1",
                isActive
                  ? "border-neutral-200 bg-white text-primary dark:border-night-border dark:bg-night-bg dark:text-night-primary"
                  : "text-neutral-500 hover:text-primary dark:text-night-muted dark:hover:text-night-text"
              )}
            >
              {item.label}
            </button>
          );
        })}
      </div>

      {items.map((item) => (
        <div
          key={item.id}
          role="tabpanel"
          id={`panel-${item.id}`}
          aria-labelledby={`tab-${item.id}`}
          hidden={item.id !== activeId}
        >
          {item.content}
        </div>
      ))}
    </div>
  );
}
