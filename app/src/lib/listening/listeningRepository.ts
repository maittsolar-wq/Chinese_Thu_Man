import type { ListeningRepository } from "./types";
import {
  LISTENING_LEVELS,
  getListeningLevel,
  getListeningLessons,
  getListeningLesson,
  getAdjacentLessons,
} from "./mockData";

/**
 * The one place every page/component gets Listening data from. Today it's
 * a thin wrapper around mockData.ts's functions; when real (B2-backed)
 * data is ready, only this file's internals need to change to a real
 * implementation of the same `ListeningRepository` shape — every route and
 * component below already depends on `listeningRepository`, never on
 * mockData.ts directly, so that swap requires no changes anywhere else.
 *
 * Deliberately still synchronous (matching mockData.ts's own functions):
 * this phase does not fetch anything real, so there's nothing to await
 * yet. A real implementation reading from B2/an API will most likely need
 * to be async — that's an interface change for the future B2 Integration
 * phase to make deliberately, not something to speculate about here.
 */
export const listeningRepository: ListeningRepository = {
  getLevels: () => LISTENING_LEVELS,
  getLevel: getListeningLevel,
  getLessons: getListeningLessons,
  getLesson: getListeningLesson,
  getAdjacentLessons: getAdjacentLessons,
};
