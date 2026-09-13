/**
 * Pure formatting helper — has nothing to do with where lesson data came
 * from (mock today, a real repository later), so it lives outside
 * mockData.ts rather than inside the file that's meant to become
 * replaceable/removable once a real data source exists.
 */
export function formatDuration(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = Math.floor(totalSeconds % 60);
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}
