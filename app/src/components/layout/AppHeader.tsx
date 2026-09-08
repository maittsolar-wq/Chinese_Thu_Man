"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import clsx from "clsx";
import { useTheme } from "@/components/theme/ThemeProvider";
import { useDictionarySearch } from "@/components/dictionary/DictionarySearchProvider";
import { HomeIcon, GraduationCapIcon, SearchIcon, TargetIcon, MoonIcon, SunIcon } from "@/components/ui/icons";

/**
 * Phase 07 information-architecture finalization, since revised by Pass 08.
 * Originally three primary destinations reflecting the actual learning
 * journey (HSK -> Vocabulary -> Vocabulary Detail, Tra cứu for fast lookup,
 * Luyện tập for reinforcement) — down from five, with "Trang chủ" removed
 * as a separate text item on the reasoning that the logo/brand block
 * (unchanged below) already links to "/" and doubles as the home link.
 *
 * Pass 08 reintroduces "Trang chủ" as an explicit first nav item (exact
 * label, not "Home") per that pass's own explicit requirement — the logo
 * still also links to "/", the two aren't mutually exclusive.
 *
 * - "Bộ thủ" is removed from primary navigation entirely, per Phase 07's
 *   explicit product-architecture requirement: Radicals are a contextual
 *   reference reached from a character (Vocabulary Detail's own "Bộ thủ &
 *   chữ Hán" tab, added in Phase 02), never a peer destination to HSK or
 *   Luyện tập. The /radicals route itself is untouched and still fully
 *   reachable by direct URL or from that contextual link — only the
 *   top-level nav entry is gone.
 *
 * "Từ điển" is renamed to "Tra cứu" to match the vocabulary already
 * established across the product for this exact feature (HSK's own
 * "Tra cứu bộ thủ" panel, Dictionary's own "Tra từ tiếng Trung" heading) —
 * one consistent name for one consistent action, not a fourth term for the
 * same capability. Still a popup TRIGGER, not a route link — opens the
 * same shared DictionarySearchPopup, unchanged mechanism.
 *
 * "Luyện tập" points at the standalone Practice Home route (/practice) —
 * its active state is computed via `isPracticeActive` rather than the
 * normal pathname-prefix check below, since it needs to match both the
 * bare /practice route and every /practice/* sub-route.
 */
const NAV_ITEMS = [
  { kind: "link", href: "/", label: "Trang chủ", icon: HomeIcon, usesPracticeActiveCheck: false },
  { kind: "link", href: "/hsk", label: "HSK", icon: GraduationCapIcon, usesPracticeActiveCheck: false },
  { kind: "popup-trigger", label: "Tra cứu", icon: SearchIcon },
  { kind: "link", href: "/practice", label: "Luyện tập", icon: TargetIcon, usesPracticeActiveCheck: true },
] as const;

/**
 * Pass 06 visual correction: text-sm(14px)/h-4(16px) icons/gap-1.5 read as
 * too small and too close together next to the rest of the (Pass 05)
 * larger-scale Home UI. Bumped to text-base(16px), 18px icons, py-2.5 for
 * a slightly taller tap target — padding is NOT increased into
 * button/pill territory (no border/bg added for the inactive state), so
 * these still read as plain nav links, not cards. Font-weight stays
 * font-medium (500) — already matched the spec, no change needed there.
 */
// Pass 14: rounded-md (6px) read as barely-rounded on the active/hover
// background pill — bumped to rounded-lg (8px).
// Pass 15: bumped again to rounded-xl (12px) — still short of a pill
// (which would need a much larger radius relative to this item's ~40px
// height) or a boxed button (no added border/heavier fill). Shared by
// all 4 items but only visible on active/hover backgrounds.
const NAV_ITEM_CLASSES =
  "flex items-center gap-2 rounded-xl px-3 py-2.5 text-base font-medium transition-colors";
const NAV_ITEM_INACTIVE_CLASSES =
  "text-neutral-800 hover:bg-primary-light hover:text-primary dark:text-night-muted dark:hover:bg-night-surface dark:hover:text-night-text";
const NAV_ITEM_ACTIVE_CLASSES =
  "bg-primary-light text-primary dark:bg-primary-dark/40 dark:text-white";

/**
 * `?from=hsk` (carried on links from HskLevelVocabularyList, and
 * previously from a direct HSK -> Radical Detail link that no longer
 * exists) means the visitor is on a shared detail screen
 * (/vocabulary/[id], /radicals/[id]) that isn't literally under /hsk/*
 * but was reached FROM there — HSK stays active through that hop.
 *
 * `?parent=hsk` is the equivalent one level deeper: HSK's only radical
 * entry point today is RadicalCta -> /radicals?from=hsk -> a radical
 * card, which chains `?from=radicals&parent=hsk` onto the Radical Detail
 * link (see radicals/page.tsx) — HSK is still the ultimate origin even
 * though the immediate `from` value is now "radicals", not "hsk".
 *
 * `hskContext=1` is the same signal carried one hop further still: when
 * Radical Detail's HSK origin (from either shape above) needs to survive
 * into a related-vocabulary link, that link can't also say `from=hsk`
 * (that slot is already `from=radical`, which Vocabulary Detail's
 * breadcrumb depends on) — so RadicalDetailView appends this second,
 * independent marker instead (see radicals/[id]/page.tsx). Any of the
 * three signals alone is enough to keep HSK active; none is present
 * unless the chain genuinely started at HSK.
 *
 * `?from=home` / `?parent=home` are the same two-level idea for Trang
 * chủ: Home's featured-radical cards link `?from=home` directly, while
 * Home's "214 bộ thủ" CTA goes through the Radical Index first, chaining
 * `?from=radicals&parent=home` instead — neither shape is under `/`, so
 * Home wouldn't otherwise show active while viewing them.
 */
function getSourceContext(searchParams: URLSearchParams): { hsk: boolean; home: boolean } {
  const from = searchParams.get("from");
  const parent = searchParams.get("parent");
  return {
    hsk: from === "hsk" || parent === "hsk" || searchParams.get("hskContext") === "1",
    home: from === "home" || parent === "home",
  };
}

function isActive(
  pathname: string,
  href: string,
  sourceContext: { hsk: boolean; home: boolean }
): boolean {
  if (href === "/") return pathname === "/" || sourceContext.home;
  if (pathname === href || pathname.startsWith(`${href}/`)) return true;
  return href === "/hsk" && sourceContext.hsk;
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
  const [sourceContext, setSourceContext] = useState({ hsk: false, home: false });
  useEffect(() => {
    setSourceContext(getSourceContext(new URLSearchParams(window.location.search)));
  }, [pathname]);

  return (
    <header className="sticky top-0 z-10 border-b border-neutral-200 bg-white dark:border-night-border dark:bg-night-bg">
      {/*
        Mobile layout: logo+toggle share row 1, the nav gets its own
        full-width row 2 below — measured directly (375-430px) rather than
        assumed: logo (~138px) + toggle (36px) alone already leave too
        little room to also fit the nav on that same first line, so a
        clean two-row split reads better than a cramped forced single row.
        `sm:flex-nowrap` with each item's `sm:order-*`/`sm:w-auto` reset
        collapses back to the single desktop/tablet row, unchanged.

        Pass 08 added a 4th item ("Trang chủ"). Measured directly again:
        at 375px the 4 items' natural width (~449px incl. gaps) exceeds
        even row 2's own ~343px, so a plain `flex-wrap` row drops the 4th
        item alone onto an accidental, unbalanced 3rd row. Switched the
        nav itself to a deliberate `grid-cols-2` below `sm:` instead — a
        clean, symmetric 2×2 (each item ~half the row, comfortably wider
        than any label) rather than a lopsided 3-then-1 wrap. `sm:flex`
        overrides back to the single desktop row exactly as before.
      */}
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-x-4 gap-y-2 px-4 py-3 sm:flex-nowrap sm:px-6">
        <Link href="/" className="order-1 flex items-center gap-2.5">
          {/* Supplied Chinese Thu Man logo asset (app/public/logo.png), used
              exactly as provided — same 36x36 slot the previous "中" text
              badge occupied, nothing else in the header changed. */}
          <span className="flex h-9 w-9 shrink-0 overflow-hidden rounded-lg">
            <Image src="/logo.png" alt="Chinese Thu Man" width={36} height={36} className="h-9 w-9 object-cover" />
          </span>
          <span className="flex flex-col leading-tight">
            <span className="text-sm font-bold text-neutral-900 dark:text-night-text">中文学习</span>
            <span className="text-xs text-neutral-500 dark:text-night-muted">Chinese Thu Man</span>
          </span>
        </Link>

        <nav className="order-3 grid w-full grid-cols-2 items-center gap-2 sm:order-2 sm:flex sm:w-auto sm:gap-6">
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
                  {Icon && <Icon className="h-[18px] w-[18px]" />}
                  {item.label}
                </button>
              );
            }

            const active = item.usesPracticeActiveCheck
              ? isPracticeActive(pathname)
              : isActive(pathname, item.href, sourceContext);
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
                {Icon && <Icon className="h-[18px] w-[18px]" />}
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
