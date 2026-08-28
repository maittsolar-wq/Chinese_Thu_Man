import type { Config } from "tailwindcss";

// Design tokens sourced from docs/02_DESIGN_SYSTEM.md — do not add
// decorative colors outside this set without updating that spec.
const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#025291",
          dark: "#013c6b",
          light: "#e6eef5",
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
          600: "#6b7280",
          800: "#2b2f33",
          900: "#1a1d1f",
        },
      },
      borderRadius: {
        card: "12px",
      },
      boxShadow: {
        card: "0 1px 2px rgba(16, 24, 40, 0.04), 0 1px 3px rgba(16, 24, 40, 0.06)",
      },
    },
  },
  plugins: [],
};

export default config;
