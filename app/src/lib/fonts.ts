import { Be_Vietnam_Pro, IBM_Plex_Mono } from "next/font/google";

/**
 * Phase 02 (Vocabulary Detail redesign) typography tokens — approved in the
 * Phase 01 design proposal. Self-hosted via next/font (built at compile
 * time, no runtime request to Google's CDN, no layout shift via `swap` +
 * next/font's automatic fallback-metric adjustment).
 *
 * Scope: these are exposed as CSS variables on <html> (see layout.tsx) but
 * are NOT wired into Tailwind's default `sans`/`mono` keys — only the new
 * `font-ui`/`font-data`/`font-cjk` utility classes consume them (see
 * tailwind.config.ts). This is deliberate: Phase 02 redesigns ONLY
 * Vocabulary Detail, so every other screen must keep rendering in the
 * existing system-font stack until it is redesigned in a later phase.
 *
 * Noto Serif SC (the approved Chinese-headword face) is intentionally NOT
 * loaded here via next/font/google: its `subsets` option only selects from
 * Google's predefined subset names (latin/vietnamese/cyrillic/...) and
 * cannot subset to our own known character set, so requesting the family
 * through next/font would ship the full CJK glyph set (tens of MB).
 * Instead it's self-hosted as a manually-subsetted `@font-face` in
 * globals.css (~430KB/weight, covers exactly the ~2200 Han characters this
 * app ever renders — see that file's own comment for how the subset was
 * built). `--font-cjk` in globals.css wires the family in with a real
 * CJK-serif fallback chain for the rare character outside that subset.
 */
export const beVietnamPro = Be_Vietnam_Pro({
  subsets: ["latin", "vietnamese"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-ui",
  display: "swap",
});

export const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin", "vietnamese"],
  weight: ["400", "500"],
  variable: "--font-data",
  display: "swap",
});
