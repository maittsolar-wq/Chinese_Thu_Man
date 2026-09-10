/**
 * Site-wide footer — rendered once in the root layout (app/layout.tsx),
 * below <main>, so every page shares it. Deliberately minimal per the
 * approved layout: a brand block on the left, a "Liên hệ" block with the
 * two social links on the right, a hairline divider, then the copyright
 * line left-aligned on its own row.
 *
 * No navigation links, no extra sections. Reuses the app's standard
 * content container (`mx-auto max-w-6xl px-4 sm:px-6`, same as AppHeader
 * and <main>) and design tokens: bg #F9F9F5 (`bg-surface-page`), #E2E8F0
 * borders, brand blue #025291 (`text-primary`), `text-ink` / `text-ink-
 * muted` (#64748B), `font-cjk` (Noto Serif SC) for 中文学习 and `font-ui`
 * (Be Vietnam Pro) for everything else.
 *
 * A plain server component — no interactivity, just two external links.
 */
export function Footer() {
  return (
    <footer className="border-t border-[#E2E8F0] bg-surface-page dark:border-night-border dark:bg-night-bg">
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 sm:py-12">
        <div className="flex flex-col gap-8 sm:flex-row sm:items-start sm:justify-between sm:gap-10">
          {/* LEFT — brand */}
          <div className="flex flex-col gap-1">
            <span className="font-cjk text-3xl font-bold leading-tight text-primary dark:text-night-primary">
              中文学习
            </span>
            <span className="font-ui text-sm text-ink-muted dark:text-night-muted">Chinese Thu Man</span>
          </div>

          {/* RIGHT — contact */}
          <div className="flex flex-col gap-1.5 sm:items-end sm:text-right">
            <span className="font-ui text-sm font-semibold text-ink dark:text-night-text">Liên hệ</span>
            <p className="font-ui text-sm">
              <a
                href="https://www.facebook.com/tiengtrungthuman.vn/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary transition-colors hover:text-primary-dark dark:text-night-primary"
              >
                Facebook
              </a>
              <span className="mx-2 text-ink-muted dark:text-night-muted" aria-hidden="true">
                ·
              </span>
              <a
                href="https://www.youtube.com/@TiengTrungThuMan"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary transition-colors hover:text-primary-dark dark:text-night-primary"
              >
                YouTube
              </a>
            </p>
          </div>
        </div>

        {/* Divider + copyright (left-aligned, its own row) */}
        <div className="mt-8 border-t border-[#E2E8F0] pt-6 dark:border-night-border">
          <p className="font-ui text-xs text-ink-muted dark:text-night-muted">© 2026 Chinese Thu Man</p>
        </div>
      </div>
    </footer>
  );
}
