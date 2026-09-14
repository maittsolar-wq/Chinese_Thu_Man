#!/usr/bin/env node

/** Produces reviewable Listening title candidates from video filenames.
 * Deliberately separate from the production catalog: no lesson.json schema
 * has been approved. It never inspects video frames, calls AI, or overwrites
 * verified metadata. */
import { readdir, stat, writeFile } from "node:fs/promises";
import { basename, extname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const VIDEO_EXTENSIONS = new Set([".mp4", ".m4v", ".mov", ".webm"]);
const VIETNAMESE_WORDS = new Map([
  ["o", "ở"], ["sieu", "siêu"], ["thi", "thị"], ["ban", "bạn"], ["be", "bè"],
  ["den", "đến"], ["giup", "giúp"], ["do", "đỡ"], ["cua", "của"], ["ly", "Lý"],
  ["huyen", "Huyền"], ["gai", "gái"], ["se", "sẽ"], ["tuc", "tức"], ["gian", "giận"],
]);

function titleCase(value) {
  return value ? value[0].toLocaleUpperCase("vi-VN") + value.slice(1) : value;
}

/** Parse only an identifier and a filename-derived Vietnamese candidate. */
export function parseLessonFilename(filename) {
  const extension = extname(filename).toLowerCase();
  const stem = basename(filename, extension);
  const match = /^(\d+)(?:[-_]+(.+))?$/.exec(stem);
  if (!match) return null;
  const [, id, rawSlug] = match;
  const vietnameseTitle = rawSlug
    ? titleCase(rawSlug.split(/[-_]+/).filter(Boolean).map((word) => VIETNAMESE_WORDS.get(word.toLowerCase()) ?? word).join(" "))
    : null;
  return { id, vietnameseTitle, vietnameseTitleSource: vietnameseTitle ? "filename" : null, chineseTitle: null, chineseTitleSource: null, needsReview: true };
}

async function collectVideoFiles(inputPath) {
  const info = await stat(inputPath);
  if (info.isFile()) return VIDEO_EXTENSIONS.has(extname(inputPath).toLowerCase()) ? [inputPath] : [];
  const entries = await readdir(inputPath, { withFileTypes: true });
  return (await Promise.all(entries.map((entry) => collectVideoFiles(resolve(inputPath, entry.name))))).flat();
}

export async function prepareLessonTitleMetadata(inputPath) {
  const files = await collectVideoFiles(resolve(inputPath));
  return files.map((file) => parseLessonFilename(basename(file))).filter((candidate) => candidate !== null)
    .sort((a, b) => a.id.localeCompare(b.id, undefined, { numeric: true }));
}

async function main() {
  const [inputPath, outputPath] = process.argv.slice(2);
  if (!inputPath) throw new Error("Usage: node tools/listening/prepare-lesson-title-metadata.mjs <input-folder-or-video> [output.json]");
  const json = `${JSON.stringify(await prepareLessonTitleMetadata(inputPath), null, 2)}\n`;
  if (outputPath) await writeFile(resolve(outputPath), json, "utf8"); else process.stdout.write(json);
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => { console.error(error.message); process.exitCode = 1; });
}
