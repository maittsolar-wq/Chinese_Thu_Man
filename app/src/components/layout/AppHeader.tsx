"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";
import { useTheme } from "@/components/theme/ThemeProvider";
import { useDictionarySearch } from "@/components/dictionary/DictionarySearchProvider";
import { HomeIcon, GraduationCapIcon, RadicalIcon, SearchIcon, TargetIcon, MoonIcon, SunIcon } from "@/components/ui/icons";

/**
 * "Luyện tập" points at the standalone Practice Home route (/practice,
 * P4.2) — its 4 cards link into the existing, already-functional
 * /practice/{meaning,character,flashcard,writing} flows, nothing
 * duplicated. Its active state is computed via `isPracticeActive` rather
 * than the normal pathname-prefix check below, since it needs to match
 * both the bare /practice route and every /practice/* sub-route.
 * "Bộ thủ" (BUG-002 fix) links to the /radicals index — until now this
 * was reachable only by direct URL or via a radical badge on Vocabulary
 * Detail (which links to one specific radical, not the browsable index),
 * so the 214-radical feature had no primary-navigation discovery path.
 * Uses the same plain pathname-prefix `isActive` check as HSK/Trang chủ.
 *
 * "Từ điển" is a popup TRIGGER, not a route link — it opens the shared
 * DictionarySearchPopup (mounted once in layout.tsx) instead of
 * navigating, per the confirmed product requirement. The existing
 * /dictionary page is untouched and still reachable by direct URL; the
 * header just no longer links to it.
 */
const NAV_ITEMS = [
  { kind: "link", href: "/", label: "Trang chủ", icon: HomeIcon, usesPracticeActiveCheck: false },
  { kind: "link", href: "/hsk", label: "HSK", icon: GraduationCapIcon, usesPracticeActiveCheck: false },
  { kind: "link", href: "/radicals", label: "Bộ thủ", icon: RadicalIcon, usesPracticeActiveCheck: false },
  { kind: "popup-trigger", label: "Từ điển", icon: SearchIcon },
  { kind: "link", href: "/practice", label: "Luyện tập", icon: TargetIcon, usesPracticeActiveCheck: true },
] as const;

const NAV_ITEM_CLASSES =
  "flex items-center gap-1.5 rounded-md px-3 py-2 text-sm font-medium transition-colors";
const NAV_ITEM_INACTIVE_CLASSES =
  "text-neutral-800 hover:bg-primary-light hover:text-primary dark:text-night-muted dark:hover:bg-night-surface dark:hover:text-night-text";
const NAV_ITEM_ACTIVE_CLASSES =
  "bg-primary-light text-primary dark:bg-primary-dark/40 dark:text-white";

/**
 * `?from=hsk` (carried on links from HskLevelVocabularyList and, via
 * `radicalHrefSuffix`, from HSK's Bộ thủ section) means the visitor is on
 * a shared detail screen (/vocabulary/[id], /radicals/[id]) that isn't
 * literally under /hsk/* but was reached FROM there — HSK stays active
 * through that hop.
 *
 * `hskContext=1` is the same signal carried one hop further: when
 * Radical Detail was itself entered with `from=hsk`, its
 * related-vocabulary links can't also say `from=hsk` (that slot is
 * already `from=radical`, which Vocabulary Detail's breadcrumb depends
 * on) — so RadicalDetailView appends this second, independent marker
 * instead (see radicals/[id]/page.tsx). Either signal alone is enough to
 * keep HSK active; neither is present unless the chain genuinely started
 * at HSK.
 */
function hasHskContext(searchParams: URLSearchParams): boolean {
  return searchParams.get("from") === "hsk" || searchParams.get("hskContext") === "1";
}

function isActive(pathname: string, href: string, hskContext: boolean): boolean {
  if (href === "/") return pathname === "/";
  if (pathname === href || pathname.startsWith(`${href}/`)) return true;
  return href === "/hsk" && hskContext;
}

/**
 * Separate from `isActive` only because Practice must be active on the
 * bare /practice route itself AND every /practice/* sub-route — unlike
 * HSK's shared-detail-screen case (which genuinely needed a
 * `?from=`/`hskContext` query signal to cross into a different route
 * tree), this is a plain pathname check, no query param involved.
 */
function isPracticeActive(pathname: string): boolean {
  return pathname === "/practice" || pathname.startsWith("/practice/");
}

function ThemeToggle({ className }: { className?: string }) {
  const { theme, toggleTheme } = useTheme();
  const isDark = theme === "dark";

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label={isDark ? "Chuyển sang giao diện sáng" : "Chuyển sang giao diện tối"}
      aria-pressed={isDark}
      className={clsx(
        "flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-neutral-300 text-neutral-700 transition-colors hover:bg-neutral-100 dark:border-night-border dark:text-night-muted dark:hover:bg-night-surface",
        className
      )}
    >
      {isDark ? <SunIcon className="h-4 w-4" /> : <MoonIcon className="h-4 w-4" />}
    </button>
  );
}

export function AppHeader() {
  const pathname = usePathname();
  const { open: openDictionarySearch } = useDictionarySearch();

  // Read via window.location rather than useSearchParams() — the latter
  // requires a Suspense boundary to avoid de-opting every page that
  // renders this header (including the ~5,600 statically-generated
  // /vocabulary/[id] and /radicals/[id] pages) from static to dynamic
  // rendering. This mirrors ThemeProvider's own established pattern in
  // this codebase: read client-only state after mount, re-read on each
  // client-side navigation. The one-render-late catch-up (from's bonus
  // active state applies a frame after initial paint) is an acceptable,
  // purely cosmetic tradeoff for a nav highlight.
  const [hskContext, setHskContext] = useState(false);
  useEffect(() => {
    setHskContext(hasHskContext(new URLSearchParams(window.location.search)));
  }, [pathname]);

  return (
    <header className="sticky top-0 z-10 border-b border-neutral-200 bg-white dark:border-night-border dark:bg-night-bg">
      {/*
        UI-003 mobile polish: below `sm`, the logo/toggle/nav no longer
        compete for width in one unwrapped row (which squeezed both the
        logo text and the 5 nav items into awkward independent wrapping —
        up to 3 nav rows plus a 4-line logo at 390px). `flex-wrap` here
        plus `order`/`w-full` on nav and the toggle splits mobile into two
        intentional rows — logo+toggle, then a full-width nav that wraps
        at most 2 rows on its own — while `sm:flex-nowrap` together with
        each item's `sm:order-*`/`sm:w-auto` reset reproduces the exact
        original single-row desktop/tablet layout, unchanged.
      */}
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-x-4 gap-y-2 px-4 py-3 sm:flex-nowrap sm:px-6">
        <Link href="/" className="order-1 flex items-center gap-2.5">
          <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-primary text-base font-bold text-white">
            中
          </span>
          <span className="flex flex-col leading-tight">
            <span className="text-sm font-bold text-neutral-900 dark:text-night-text">中文学习</span>
            <span className="text-xs text-neutral-500 dark:text-night-muted">Chinese Thu Man</span>
          </span>
        </Link>

        <nav className="order-3 flex w-full flex-wrap items-center gap-1 sm:order-2 sm:w-auto sm:gap-2">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;

            if (item.kind === "popup-trigger") {
              return (
                <button
                  key={item.label}
                  type="button"
                  onClick={openDictionarySearch}
                  className={clsx(NAV_ITEM_CLASSES, NAV_ITEM_INACTIVE_CLASSES)}
                >
                  {Icon && <Icon className="h-4 w-4" />}
                  {item.label}
                </button>
              );
            }

            const active = item.usesPracticeActiveCheck
              ? isPracticeActive(pathname)
              : isActive(pathname, item.href, hskContext);
            return (
              <Link
                key={item.href}
                href={item.href}
                aria-current={active ? "page" : undefined}
                className={clsx(
                  NAV_ITEM_CLASSES,
                  active ? NAV_ITEM_ACTIVE_CLASSES : NAV_ITEM_INACTIVE_CLASSES
                )}
              >
                {Icon && <Icon className="h-4 w-4" />}
                {item.label}
              </Link>
            );
          })}
        </nav>

        <ThemeToggle className="order-2 sm:order-3" />
      </div>
    </header>
  );
}
