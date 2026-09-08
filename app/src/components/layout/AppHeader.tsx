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
 * "Luyện tập" points at the standalone Practice Home route (/practice).
 * Its active state used to be computed via a dedicated pathname-only
 * `isPracticeActive` check — navigation-completion pass (Practice source
 * context) folded that into the same unified, source-context-aware
 * `isActive` every other item already uses (see that function below):
 * Practice's own pathname-prefix behavior (bare /practice AND every
 * /practice/* sub-route) was already exactly what the generic branch of
 * `isActive` does for any href, so the special case was redundant once
 * Practice also needed to be source-context-*suppressible* (a Practice
 * exercise config screen reached from Home must NOT show Luyện tập
 * active, even though its pathname is under /practice/*).
 */
const NAV_ITEMS = [
  { kind: "link", href: "/", label: "Trang chủ", icon: HomeIcon },
  { kind: "link", href: "/hsk", label: "HSK", icon: GraduationCapIcon },
  { kind: "popup-trigger", label: "Tra cứu", icon: SearchIcon },
  { kind: "link", href: "/practice", label: "Luyện tập", icon: TargetIcon },
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
 * link (see radicals/page.tsx); an HSK Level page reached via `/hsk`'s own
 * level grid similarly chains `?from=hsk&level=N&parent=hsk` onto its
 * Vocabulary Detail links (see hsk/[level]/page.tsx /
 * HskLevelVocabularyList.tsx) — HSK is still the ultimate origin even
 * though the immediate `from` value is "radicals" / "hsk"-as-hop-type
 * rather than a literal top-level marker.
 *
 * `hskContext=1` is the same signal carried one hop further still: when
 * Radical Detail's HSK origin needs to survive into a related-vocabulary
 * link, that link can't also say `from=hsk` (that slot is already
 * `from=radical`, which Vocabulary Detail's breadcrumb depends on) — so
 * RadicalDetailView appends this second, independent marker instead (see
 * radicals/[id]/page.tsx). Any of these signals alone is enough to keep
 * HSK active; none is present unless the chain genuinely started at HSK.
 *
 * `?from=home` / `?parent=home` are the same idea for Trang chủ: Home's
 * featured-radical cards and HSK-card grid link `?from=home` directly,
 * while Home's "214 bộ thủ" CTA chains `?from=radicals&parent=home` and
 * an HSK Level page reached from Home chains `?from=hsk&level=N&parent=
 * home` onto ITS Vocabulary Detail links — none of these shapes are
 * under `/`, so Home wouldn't otherwise show active while viewing them.
 *
 * `home` takes priority when both are somehow present (e.g.
 * `from=hsk&parent=home`: reached via an HSK-level list, but that level
 * page's own ultimate origin was Home) — a page has exactly one true
 * origin, and `parent`, when set, always names it more precisely than the
 * `from` hop-type value beside it.
 *
 * `?from=practice` (Practice source-context pass): PracticeConfigView's
 * own existing `useConfigBackHref` already reads this exact value to
 * decide the Back destination — reused here as-is, not a new convention,
 * so the header agrees with Back about where a Practice exercise config
 * screen (/practice/meaning|character|flashcard|writing) came from. Only
 * needed to explicitly SUPPRESS Practice when `home` is set instead (see
 * `resolveExplicitActiveHref`) — `from=practice` alone doesn't change
 * anything plain pathname-prefix matching wasn't already going to give
 * Practice anyway, but naming it explicitly keeps the source model
 * complete/self-documenting rather than leaning on that as an implicit
 * coincidence.
 */
function getSourceContext(
  searchParams: URLSearchParams
): { hsk: boolean; home: boolean; practice: boolean } {
  const from = searchParams.get("from");
  const parent = searchParams.get("parent");
  const home = from === "home" || parent === "home";
  const hsk = !home && (from === "hsk" || parent === "hsk" || searchParams.get("hskContext") === "1");
  const practice = !home && from === "practice";
  return { hsk, home, practice };
}

/**
 * When a page carries an explicit source context, that context is
 * authoritative and exclusive — it names the ONE nav item that should
 * show active, overriding whatever the raw pathname would otherwise
 * suggest. This matters specifically for:
 *  - `/hsk/[level]` reached from Home (`?from=home`) — pathname starts
 *    with `/hsk/`, which would otherwise ALSO match the HSK nav item.
 *  - `/practice/<type>` reached from Home (`?from=home`) — pathname
 *    starts with `/practice/`, which would otherwise ALSO match the
 *    Luyện tập nav item, showing "Trang chủ" and "Luyện tập" active at
 *    once (the exact bug this pass fixes).
 * Only when there's no source context at all (direct/bookmarked access,
 * or `from=practice` — already correctly a no-op against Practice's own
 * pathname) does plain pathname-prefix matching apply.
 */
function resolveExplicitActiveHref(sourceContext: {
  hsk: boolean;
  home: boolean;
  practice: boolean;
}): string | null {
  if (sourceContext.home) return "/";
  if (sourceContext.hsk) return "/hsk";
  if (sourceContext.practice) return "/practice";
  return null;
}

function isActive(pathname: string, href: string, explicitActiveHref: string | null): boolean {
  if (explicitActiveHref) return href === explicitActiveHref;
  if (href === "/") return pathname === "/";
  return pathname === href || pathname.startsWith(`${href}/`);
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
  const [sourceContext, setSourceContext] = useState({ hsk: false, home: false, practice: false });
  useEffect(() => {
    setSourceContext(getSourceContext(new URLSearchParams(window.location.search)));
  }, [pathname]);
  const explicitActiveHref = resolveExplicitActiveHref(sourceContext);

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

            const active = isActive(pathname, item.href, explicitActiveHref);
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
