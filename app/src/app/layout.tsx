import type { Metadata } from "next";
import { AppHeader } from "@/components/layout/AppHeader";
import "./globals.css";

export const metadata: Metadata = {
  title: "Chinese Thu Man — Học từ vựng HSK",
  description:
    "Học và tra cứu từ vựng HSK 1–6 cùng bộ thủ chữ Hán, dành cho người Việt.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi">
      <body className="min-h-screen bg-white text-neutral-900 antialiased">
        <AppHeader />
        <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6">{children}</main>
      </body>
    </html>
  );
}
