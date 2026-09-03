import type { Metadata } from "next";
import { AppHeader } from "@/components/layout/AppHeader";
import { ThemeProvider } from "@/components/theme/ThemeProvider";
import { DictionarySearchProvider } from "@/components/dictionary/DictionarySearchProvider";
import { DictionarySearchPopup } from "@/components/dictionary/DictionarySearchPopup";
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
    <html lang="vi" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: NO_FLASH_THEME_SCRIPT }} />
      </head>
      <body className="min-h-screen bg-white text-neutral-900 antialiased dark:bg-night-bg dark:text-night-text">
        <ThemeProvider>
          <DictionarySearchProvider>
            <AppHeader />
            <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6">{children}</main>
            <DictionarySearchPopup />
          </DictionarySearchProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
