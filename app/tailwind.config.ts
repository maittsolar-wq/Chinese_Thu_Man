import type { Config } from "tailwindcss";

// Design tokens sourced from docs/02_DESIGN_SYSTEM.md — do not add
// decorative colors outside this set without updating that spec.
const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#025291",
          dark: "#013c6b",
          light: "#e6eef5",
          // UI Foundation Phase additions. `light` above (#e6eef5) already
          // has broad, approved usage across Home/HSK/Header/Badge — its
          // value is untouched. `tint`/`wash` are new, additively-named
          // steps for the editorial foundation's own two-step "primary
          // light / primary subtle" scale, used first on Vocabulary Detail.
          tint: "#EAF3FA",
          wash: "#F4F8FC",
        },
        success: {
          DEFAULT: "#1f9254",
          bg: "#e7f6ee",
          border: "#8fd6b1",
        },
        error: {
          DEFAULT: "#c8321f",
          bg: "#fdecea",
          border: "#f0a99e",
        },
        hint: {
          DEFAULT: "#b5760a",
          bg: "#fff4e0",
          border: "#f0cd8a",
        },
        neutral: {
          50: "#f8f9fa",
          100: "#f1f3f5",
          200: "#e7eaed",
          300: "#d6dbe0",
          // 400/500 fill the gap found in the Phase 01 UI audit — every
          // "medium-emphasis" text color previously had to reuse 300 or 600
          // outright. Interpolated within the same cool blue-gray family as
          // their neighbors, not a separate palette.
          400: "#aab1b9",
          500: "#828a93",
          600: "#6b7280",
          800: "#2b2f33",
          900: "#1a1d1f",
        },
        // Quiet, borderless grouping surface — distinct from a bordered
        // Card, used for reference info that isn't an interactive item
        // (Phase 01 §F, "Card vs Panel spent by role"). Dark mode reuses
        // the existing `night.input` tone rather than a new dark token.
        surface: {
          sunken: "#eef2f6",
          // UI Foundation Phase additions — additive only, `sunken` above
          // is untouched and keeps its existing meaning/usage.
          DEFAULT: "#FFFFFF",
          subtle: "#F7F8FA",
          page: "#FAFBFC",
        },
        // New text-color pair for the editorial foundation (UI Foundation
        // Phase) — existing screens keep using raw `neutral-900`/`600` etc.
        // directly and are unaffected; this is an opt-in pair for screens
        // that adopt the new system, starting with Vocabulary Detail.
        ink: {
          DEFAULT: "#17212B",
          muted: "#64748B",
        },
        // Subtle card/section border (UI Foundation Phase) — sits alongside
        // the existing `neutral-200`/`neutral-300` borders rather than
        // replacing them, for the same "opt-in, new screens only" reason.
        hairline: "#DDE4EA",
        // Status/attention marker approved in the Phase 01 color system —
        // same DEFAULT/bg/border shape as success/error/hint. Reserved for
        // exactly one purpose (an unavailable/needs-attention marker); never
        // a second accent alongside primary blue.
        seal: {
          DEFAULT: "#9c3b2e",
          bg: "#f3e6e3",
          border: "#d9beb8",
        },
        // Per-level/per-card decorative accents from the approved Home
        // visual reference (HSK 1-6 cards, Practice cards). Added
        // 2026-08-29 — not yet mirrored into docs/02_DESIGN_SYSTEM.md.
        accent: {
          blue: "#2563eb",
          green: "#16a34a",
          purple: "#7c3aed",
          orange: "#f97316",
          red: "#f43f5e",
          teal: "#14b8a6",
        },
        // Dark-mode surface/text tokens from the approved Home Dark Mode
        // reference. Deliberately near-neutral grays, not tinted with the
        // existing `neutral` scale, per that reference's explicit values.
        night: {
          bg: "#1a1a1a",
          surface: "#202020",
          input: "#303030",
          border: "#3a3a3a",
          text: "#f5f5f5",
          muted: "#b5b5b5",
          // Raw brand blue (#025291) fails contrast as TEXT on these near-
          // black grounds (it stays fine as a fill/badge background, e.g.
          // the existing `dark:bg-primary-dark/40`). This is a lighter tint
          // for text/links only — found in the Phase 01 dark-mode audit.
          primary: "#5fa8e0",
        },
      },
      borderRadius: {
        card: "12px",
      },
      fontSize: {
        // The one size the approved type scale needs that stock Tailwind
        // doesn't already provide (8xl=96px, 9xl=128px) — the desktop
        // Chinese hero character's "visual anchor" role. Phase 09 bumped
        // the approved range to 128-144px (was 96-120px); 136px sits at
        // the midpoint. Every other element in the type scale maps onto
        // an existing stock text-* utility already in the approved ranges.
        "cjk-hero": ["8.5rem", { lineHeight: "1.2" }],
      },
      boxShadow: {
        card: "0 1px 2px rgba(16, 24, 40, 0.04), 0 1px 3px rgba(16, 24, 40, 0.06)",
      },
      fontFamily: {
        // Opt-in utilities only — deliberately NOT wired into Tailwind's
        // default `sans`/`mono` keys, so every screen outside Vocabulary
        // Detail keeps rendering in the existing system-font stack until
        // it is redesigned in a later phase. See lib/fonts.ts.
        ui: [
          "var(--font-ui)",
          "-apple-system",
          "Segoe UI",
          "Roboto",
          "sans-serif",
        ],
        data: ["var(--font-data)", "ui-monospace", "Menlo", "monospace"],
        cjk: ["var(--font-cjk)"],
      },
    },
  },
  plugins: [],
};

export default config;
