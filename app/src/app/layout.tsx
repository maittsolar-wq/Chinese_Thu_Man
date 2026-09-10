import type { Metadata } from "next";
import { AppHeader } from "@/components/layout/AppHeader";
import { Footer } from "@/components/layout/Footer";
import { ThemeProvider } from "@/components/theme/ThemeProvider";
import { DictionarySearchProvider } from "@/components/dictionary/DictionarySearchProvider";
import { DictionarySearchPopup } from "@/components/dictionary/DictionarySearchPopup";
import { beVietnamPro, ibmPlexMono } from "@/lib/fonts";
import "./globals.css";

export const metadata: Metadata = {
  title: "Chinese Thu Man — Học từ vựng HSK",
  description:
    "Học và tra cứu từ vựng HSK 1–6 cùng bộ thủ chữ Hán, dành cho người Việt.",
};

// Applies the persisted theme before hydration so there is no flash of the
// wrong theme. Kept intentionally tiny and defensive (try/catch) since it
// runs before any framework code.
const NO_FLASH_THEME_SCRIPT = `
try {
  var theme = localStorage.getItem('theme');
  if (theme === 'dark' || (!theme && matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
  }
} catch (e) {}
`;

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="vi"
      suppressHydrationWarning
      className={`${beVietnamPro.variable} ${ibmPlexMono.variable}`}
    >
      <head>
        <script dangerouslySetInnerHTML={{ __html: NO_FLASH_THEME_SCRIPT }} />
      </head>
      {/* Global background pass: `bg-surface-page` (#F9F9F5) replaces the
          old plain `bg-white` as the site-wide light-mode PAGE background —
          the single shared source every page inherits from, matching the
          already-approved Home/HSK tone. Card/Panel/modal/input surfaces
          (Card.tsx, AppHeader, etc.) keep their own explicit `bg-white`
          and are unaffected. Dark mode (`dark:bg-night-bg`) is untouched. */}
      <body className="min-h-screen bg-surface-page text-neutral-900 antialiased dark:bg-night-bg dark:text-night-text">
        <ThemeProvider>
          <DictionarySearchProvider>
            <AppHeader />
            <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6">{children}</main>
            <Footer />
            <DictionarySearchPopup />
          </DictionarySearchProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
