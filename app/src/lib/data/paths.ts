import path from "node:path";

/**
 * The canonical /data directory lives at the repository root, one level
 * above this Next.js app (app/ is a sibling of data/, not a parent).
 * DATA_ROOT lets deployment configs override this if the app is ever
 * bundled/deployed separately from the rest of the repository.
 */
export const DATA_ROOT =
  process.env.DATA_ROOT ?? path.resolve(process.cwd(), "..", "data");

export function hskProductionPath(level: number): string {
  return path.join(
    DATA_ROOT,
    "hsk",
    `hsk${level}`,
    `hsk${level}_vocabulary_production.json`
  );
}

export const RADICALS_PATH = path.join(DATA_ROOT, "radicals", "radicals_214.json");
export const RADICAL_DETAIL_PATH = path.join(
  DATA_ROOT,
  "radicals",
  "radical_detail_data.json"
);
export const RADICAL_VOCABULARY_MAPPING_PATH = path.join(
  DATA_ROOT,
  "radicals",
  "radical_vocabulary_mapping.json"
);
