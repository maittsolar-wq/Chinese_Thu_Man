"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";
import { useTheme } from "@/components/theme/ThemeProvider";
import { useDictionarySearch } from "@/components/dictionary/DictionarySearchProvider";
import { HomeIcon, GraduationCapIcon, SearchIcon, TargetIcon, MoonIcon, SunIcon } from "@/components/ui/icons";

/**
 * "Luyện tập" points at the real Practice section on Home (#luyen-tap)
 * rather than a dedicated overview route — the Practice configuration
 * screens/routes don't exist in the codebase yet (spec-only, see
 * docs/PRACTICE/), and per instructions no placeholder/fake route is
 * created for them. This keeps the link genuinely functional instead of
 * dead. "Bộ thủ" is intentionally omitted here to match the approved
 * Home header reference; the /radicals route itself is untouched and
 * still reachable directly.
 *
 * "Từ điển" is a popup TRIGGER, not a route link — it opens the shared
 * DictionarySearchPopup (mounted once in layout.tsx) instead of
 * navigating, per the confirmed product requirement. The existing
 * /dictionary page is untouched and still reachable by direct URL; the
 * header just no longer links to it.
 */
const NAV_ITEMS = [
  { kind: "link", href: "/", label: "Trang chủ", icon: HomeIcon, isAnchor: false },
  { kind: "link", href: "/hsk", label: "HSK", icon: GraduationCapIcon, isAnchor: false },
  { kind: "popup-trigger", label: "Từ điển", icon: SearchIcon },
  { kind: "link", href: "/#luyen-tap", label: "Luyện tập", icon: TargetIcon, isAnchor: true },
] as const;

const NAV_ITEM_CLASSES =
  "flex items-center gap-1.5 rounded-md px-3 py-2 text-sm font-medium transition-colors";
const NAV_ITEM_INACTIVE_CLASSES =
  "text-neutral-800 hover:bg-primary-light hover:text-primary dark:text-night-muted dark:hover:bg-night-surface dark:hover:text-night-text";
const NAV_ITEM_ACTIVE_CLASSES =
  "bg-primary-light text-primary dark:bg-primary-dark/40 dark:text-white";

function isActive(pathname: string, href: string): boolean {
  if (href === "/") return pathname === "/";
  return pathname === href || pathname.startsWith(`${href}/`);
}

function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  const isDark = theme === "dark";

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label={isDark ? "Chuyển sang giao diện sáng" : "Chuyển sang giao diện tối"}
      aria-pressed={isDark}
      className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-neutral-300 text-neutral-700 transition-colors hover:bg-neutral-100 dark:border-night-border dark:text-night-muted dark:hover:bg-night-surface"
    >
      {isDark ? <SunIcon className="h-4 w-4" /> : <MoonIcon className="h-4 w-4" />}
    </button>
  );
}

export function AppHeader() {
  const pathname = usePathname();
  const { open: openDictionarySearch } = useDictionarySearch();

  return (
    <header className="sticky top-0 z-10 border-b border-neutral-200 bg-white dark:border-night-border dark:bg-night-bg">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
        <Link href="/" className="flex items-center gap-2.5">
          <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-primary text-base font-bold text-white">
            中
          </span>
          <span className="flex flex-col leading-tight">
            <span className="text-sm font-bold text-neutral-900 dark:text-night-text">中文学习</span>
            <span className="text-xs text-neutral-500 dark:text-night-muted">Chinese Thu Man</span>
          </span>
        </Link>
        <div className="flex items-center gap-1 sm:gap-2">
          <nav className="flex flex-wrap items-center gap-1 sm:gap-2">
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

              const active = !item.isAnchor && isActive(pathname, item.href);
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
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
