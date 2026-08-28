/**
 * Process-level (not per-request) memoization for reading local static
 * data files. The content under /data does not change while the app is
 * running, so — unlike React's `cache()`, which only dedups within a
 * single request/render pass — this reuses one parsed copy for the
 * lifetime of the Node process, across every request and every page
 * generated during a static build.
 */
export function memoizeOnce<T>(load: () => T): () => T {
  let cached: T | undefined;
  let hasValue = false;
  return () => {
    if (!hasValue) {
      cached = load();
      hasValue = true;
    }
    return cached as T;
  };
}
