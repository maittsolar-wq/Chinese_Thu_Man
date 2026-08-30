import type { HskLevel } from "@/lib/data/types";

/**
 * Presentational-only copy for HSK Main's level cards and each
 * /hsk/[level] page's own description line — not derived from vocabulary
 * data (there's nothing in the production JSON to source this from), and
 * not invented per-page; one shared source both consume, matching the
 * approved HSK reference screenshots' subtitle/description text exactly.
 */
export interface HskLevelInfo {
  /** "Sơ cấp" / "Trung cấp" / "Cao cấp" — shared by HSK 1–2 / 3–4 / 5–6. */
  name: string;
  description: string;
}

export const HSK_LEVEL_INFO: Record<HskLevel, HskLevelInfo> = {
  1: { name: "Sơ cấp", description: "Từ vựng cơ bản cho người mới bắt đầu" },
  2: { name: "Sơ cấp", description: "Mở rộng vốn từ vựng cơ bản" },
  3: { name: "Trung cấp", description: "Từ vựng cho giao tiếp hàng ngày" },
  4: { name: "Trung cấp", description: "Từ vựng cho học tập và làm việc" },
  5: { name: "Cao cấp", description: "Từ vựng cho học thuật và chuyên sâu" },
  6: { name: "Cao cấp", description: "Từ vựng nâng cao và học thuật" },
};
