import type { ListeningLevelId } from "./types";

/**
 * Per-level visual identity for the Listening feature ONLY — deliberately
 * separate from `HSK_LEVEL_HEX` (lib/hsk/homePalette.ts), which drives
 * HSK1-6 colors everywhere ELSE in the site (Home, /hsk, HskLevelBadge).
 * The approved Listening reference assigns its own scheme (HSK1 blue,
 * HSK2 coral, HSK3 green) that does not match HSK_LEVEL_HEX's HSK2=green/
 * HSK3=purple — reusing that shared token here would give the wrong
 * colors for 2 of 3 Listening levels, so this is its own small map
 * instead of a change to a token other screens depend on.
 *
 * `illustration` — dedicated Listening-only assets (added directly to
 * app/public/ for this feature): `/listening-hsk1.png` (blue pagoda),
 * `/listening-hsk2.png` (coral Great Wall), `/listening-hsk3.png` (green
 * pavilion). These replace the earlier placeholder approach of reusing
 * `/hsk-N-illustration.png` (a different, site-wide asset set with its own
 * HSK1=blue/HSK2=green/HSK3=purple palette) with a CSS hue-rotate filter
 * approximating HSK3's green — no filter is needed anymore since
 * `/listening-hsk3.png` is already painted green.
 */
export interface ListeningLevelAccent {
  /** Primary identity color — border, icon, badge, arrow CTA. */
  color: string;
  /** Dedicated Listening illustration for this level (app/public/). */
  illustration: string;
}

export const LISTENING_LEVEL_ACCENT: Record<ListeningLevelId, ListeningLevelAccent> = {
  hsk1: {
    color: "#025291",
    illustration: "/listening-hsk1.png",
  },
  hsk2: {
    color: "#DD6659",
    illustration: "/listening-hsk2.png",
  },
  hsk3: {
    color: "#3F9142",
    illustration: "/listening-hsk3.png",
  },
};
