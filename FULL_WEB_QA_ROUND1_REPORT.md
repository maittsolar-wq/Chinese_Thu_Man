# FULL WEB QA — ROUND 1 REPORT

## 1. QA Baseline

- Commit: `7f01821`
- HEAD: `7f018216a0a8ae6df80144e49716a5af12987ab3`
- origin/main: `7f018216a0a8ae6df80144e49716a5af12987ab3` (identical, confirmed clean/synchronized at start)
- Working tree: clean
- Application URL: `http://localhost:3000` (Next.js 15.5.24 dev server, freshly started with a cleared `.next` cache to avoid stale-build artifacts)
- Browser: Chromium (Playwright)
- Playwright/browser automation: used throughout, via scripts in the session scratchpad (no repository files touched)
- Date: 2026-09-03

## 2. Test Environment

| Environment | Viewport | Result |
|---|---:|---|
| Desktop | 1440×900 | PASS — no horizontal overflow, all content usable on any tested route |
| Tablet | 834×1112 | PASS — no horizontal overflow, all content usable |
| Mobile | 390×844 | PASS — no horizontal overflow; Dictionary popup specifically verified usable on this viewport |

## 3. Coverage

| Area | Tested | Result |
|---|---|---|
| Home | Full (content, nav, theme toggle, HSK/Dictionary/Practice entry points, back nav) | PASS |
| HSK | Full (all 6 level cards, navigation) | PASS |
| HSK Levels | Full (all 6 levels: list rendering, search, pagination, vocabulary open, breadcrumb level-context, back nav) | PASS |
| Radical | Full (index, 214 cards, navigation) | PASS (see Navigation Findings — no primary nav entry point) |
| Radical Detail | Full (detail render, related-vocabulary list, navigation to Vocabulary Detail, double back-nav) | PASS |
| Dictionary | Full (popup open, live search, no-result state, result selection, direct route, refresh, mobile) | PASS |
| Vocabulary Detail | Full (4 entry points: HSK level, Dictionary, Radical, direct/query-param; HSK1 and HSK6 vocab; related-words empty vs. populated states; examples empty state; radical section) | PASS |
| Practice | Full (Home, all 4 modes end-to-end, HSK filter, quantity/"Tất cả", direct routes, refresh) | PASS |
| Search | Full (Dictionary popup — the app's one search implementation — desktop + mobile; HSK-level in-page search) | PASS |
| Navigation | Full (forward links, browser back, breadcrumbs, history depth) | PASS, 1 finding (see §8) |
| Direct Routes | Full (all major routes loaded directly, plus invalid IDs/levels for 404 handling) | PASS |
| Refresh | Full (HSK Level, Vocabulary Detail, Dictionary, all 4 Practice routes) | PASS |
| Theme | Full (toggle, persistence across routes and refresh, dark-mode rendering) | PASS, 1 finding (see §6/§10) |
| Responsive | Full (3 viewports × 8 representative routes) | PASS |
| Console | Full (captured across every test) | 1 reproducible warning found (see §6) |
| Network | Full (captured across every test) | No actionable failures beyond expected 404s for intentionally-invalid test routes |
| Data Rendering | Full (Hanzi/pinyin/meaning/HSK-level/radical/related-words spot-checked across levels) | PASS |

## 4. Bug Summary

| Severity | Count |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 2 |
| P3 | 0 |
| Total | 2 |

## 5. BUG LOG

### BUG-001

- **Severity:** P2
- **Route:** All routes, whenever a full document load (not an in-app SPA link click) occurs while the user's persisted theme is `dark` — reproduced explicitly on `/`, `/hsk`, `/hsk/1`, `/radicals`, `/radicals/radical_001`, `/dictionary`, `/vocabulary/hsk1_001`, `/practice`
- **Viewport:** Reproduces at all viewports (not viewport-dependent)
- **Preconditions:** `localStorage.theme === "dark"` (i.e., the user has toggled dark mode at least once previously)
- **Steps:**
  1. Set dark mode (click the theme toggle once, or have `localStorage.getItem("theme") === "dark"` from a prior session)
  2. Perform any fresh full-document navigation — a hard refresh, typing a URL directly, or opening a new tab to any route
  3. Open the browser console
- **Expected:** No console errors/warnings; page renders in dark mode cleanly
- **Actual:** React logs a hydration-mismatch error every time: *"A tree hydrated but some attributes of the server rendered HTML didn't match the client properties... `<html lang=\"vi\" className=\"dark\">`"*. Root cause identified by source inspection: `app/src/app/layout.tsx` includes a pre-hydration inline script (`NO_FLASH_THEME_SCRIPT`) that correctly adds the `dark` class to `<html>` before React hydrates (to avoid a flash of the wrong theme), but the `<html>` JSX itself (`<html lang="vi">`) has no matching `suppressHydrationWarning` prop, so React's hydration diff flags the class attribute the inline script added as a server/client mismatch. This is a well-known interaction pattern with the "no-FOUC inline theme script" technique; the standard fix is `suppressHydrationWarning` on the `<html>` element.
- **Evidence:** Isolated single-fresh-load repro script (localStorage seeded with `theme=dark`, one clean `page.goto`) reproduced exactly 1 hydration error deterministically; full console text captured, `<html>` diff explicitly shows `- className="dark"` under the SSR tree vs. client tree.
- **Reproducibility:** 100% (8/8 routes tested, plus an isolated single-load repro) whenever dark mode is active and a fresh document load occurs.
- **User impact:** No visible/functional breakage — React does not "unpatch" the DOM (per its own warning text), so the page still renders correctly in dark mode (`body` background confirmed `rgb(26,26,26)` as expected). The impact is a console error appearing for any user who has dark mode enabled and refreshes or deep-links into the app, which fails a clean-console bar and could be surfaced by monitoring/error-tracking tooling as a false-positive error volume.
- **Suspected area:** `app/src/app/layout.tsx` (`<html lang="vi">` element)
- **Recommended fix direction:** Add `suppressHydrationWarning` to the `<html>` element in `RootLayout`. This is the standard, narrow, well-established fix for exactly this SSR/inline-theme-script pattern and would not require removing or altering the no-flash script itself.

### BUG-002

- **Severity:** P2
- **Route:** `/` (Home) and the global header navigation (present on every route)
- **Viewport:** Reproduces at all viewports
- **Preconditions:** None — default application state
- **Steps:**
  1. Load Home (`/`) fresh
  2. Inspect the header navigation and the full Home page for any link to `/radicals`
- **Expected:** Some discoverable path exists in the primary UI to browse the full Radicals index (214 radicals)
- **Actual:** Zero links to `/radicals` exist anywhere on Home (`document.querySelectorAll('a[href^="/radicals"]')` → 0 matches) and the header nav is exactly `Trang chủ / HSK / Từ điển / Luyện tập` (Home/HSK/Dictionary/Practice) — no "Bộ thủ" entry. The only in-app links that touch `/radicals/*` at all are individual radical *badges* on Vocabulary Detail pages, and each of those links to one *specific* radical's detail page (e.g. `/radicals/radical_087`), never to the browsable `/radicals` index itself. A user who has never guessed or been told the `/radicals` URL has no way to discover that a 214-radical browse feature exists.
- **Evidence:** Home-page link sweep (0 `/radicals` links found), header nav text dump (`"Trang chủ\nHSK\nTừ điển\nLuyện tập"`), Vocabulary Detail radical-badge href capture (`/radicals/radical_087`, a specific-radical link, not the index).
- **Reproducibility:** 100%, structural (not state-dependent).
- **User impact:** The Radicals *feature itself* is fully functional and bug-free once reached (confirmed extensively in §3/§9) — this is purely a discoverability/navigation gap. A typical user browsing normally would never find it.
- **Suspected area:** `app/src/components/layout/AppHeader.tsx` (nav item list) and/or Home page card list
- **Recommended fix direction:** Not attempted or diagnosed further per this phase's read-only scope. Noting for product/UX review: whether this is still an intentional, approved scope decision (an existing code comment elsewhere in `AppHeader.tsx` does document that "Bộ thủ" was deliberately omitted from the header to match an approved reference design) or whether it should be revisited now that the Radicals feature is fully built and stable.

## 6. Console Errors

| Route(s) | Error | Reproducibility | Impact |
|---|---|---|---|
| Any route, fresh load while `theme=dark` | React hydration mismatch on `<html className="dark">` (BUG-001) | 100%, deterministic | No visual/functional break; console-error hygiene issue only |

No other console errors, uncaught exceptions, or unhandled promise rejections were observed across the entire QA pass (light mode, all routes, all 3 viewports, all 4 Practice modes, all navigation flows).

## 7. Network Errors

No actionable failed requests were found. The only non-2xx responses observed were the intentionally-triggered 404s for deliberately invalid test routes (`/nonexistent-route-xyz`, `/vocabulary/hsk1_99999`, `/hsk/7`, `/radicals/radical_999`) — all four returned a proper 404 status with a graceful in-app "Không tìm thấy nội dung" (not found) page, no crash, no blank screen.

## 8. Navigation Findings

- **Back button (in-app "Quay lại" buttons):** correct on every tested flow — HSK Level → Vocabulary Detail, Radical → Radical Detail → Vocabulary Detail (double-back correctly returns to Radical Detail then Radicals index), Dictionary → Vocabulary Detail, Practice config/exercise exit.
- **Browser back button:** correct and matches expectation exactly on a 3-level-deep history stack (Home → HSK → HSK1 → Vocabulary Detail → back×3 → Home), with no duplicate or skipped history entries observed.
- **Context preservation:** HSK context (`?from=hsk&level=N`) and Radical context (`?from=radical&radicalId=...`) are both correctly attached by the originating list pages and correctly reflected in the Vocabulary Detail breadcrumb for every one of the 6 HSK levels and for the Radical flow. Standalone radical entry (no HSK context in play) correctly does **not** show a false HSK breadcrumb.
- **Query parameters:** `?from=hsk&level=1` and `?from=dictionary` both verified to produce the correct breadcrumb; no query-parameter loss observed across any navigation.
- **Direct routes / deep links:** every tested route loads correctly when opened directly (not navigated to from Home first), including with query parameters attached.
- **One finding:** see BUG-002 (§5) — no primary-navigation path to the Radicals index itself.

## 9. Responsive Findings

Zero horizontal overflow (`scrollWidth > clientWidth`) detected on any of the 24 route×viewport combinations tested (8 representative routes × desktop/tablet/mobile). Header remained visible and usable at every size. The Dictionary popup was specifically verified usable at 390×844 (mobile) with no overflow while open. No clipped content, overlapping elements, or inaccessible controls were found in this pass.

## 10. Theme Findings

- Toggle correctly flips `aria-pressed` and the `dark` class, and correctly persists across in-app navigation and a hard refresh.
- Dark-mode background/text rendering confirmed correct (`body` background `rgb(26,26,26)` in dark mode) across all 8 representative routes.
- One finding: BUG-001 (§5) — a reproducible hydration-mismatch console error on fresh loads while dark mode is active. This is a console-hygiene defect, not a visual rendering defect — no incorrect colors, contrast, or layout were observed in dark mode on any tested route.

## 11. Data Integrity Findings

No data defects found. Specifically checked and confirmed correct:
- HSK level filtering is accurate for all 6 levels; vocabulary IDs whose filename prefix differs from the level being browsed (e.g. `hsk1_046` appearing while browsing HSK 2, `hsk2_058` appearing while browsing HSK 6) were investigated and confirmed to be **legitimate, correct multi-level-tagged vocabulary** (the ID prefix reflects original sourcing, not current level membership — already documented behavior from prior audit phases), verified via the Vocabulary Detail breadcrumb correctly showing the level actually being browsed in every case. This is **not** cross-level leakage.
- HSK6 related words (integrated in P5.3) render correctly: `hsk6_0004` shows exactly 5 related-word cards as expected.
- HSK1 related words correctly show the empty state (`relatedWordIds` not yet integrated into production — expected, see §12).
- Radical sections on Vocabulary Detail render correctly and link to a real, valid radical.
- No wrong Hanzi/pinyin/meaning, no duplicated data, no impossible relationships observed in any spot-checked record.

## 12. Known Content / Product Gaps

Kept separate from the bug log — none of these are newly discovered issues, and none are treated as bugs:

- HSK1 `relatedWordIds` fully prepared (P5.4.1–P5.4.4) but not yet integrated into production — the "Từ liên quan" section on HSK1 Vocabulary Detail pages correctly shows its empty state.
- HSK2–HSK5 related-word work not yet started.
- Example Sentence production data not yet populated for any HSK level — the "Câu ví dụ" section correctly shows its empty state everywhere.
- HSK2–HSK6 vocabulary meanings remain AI-assisted and not fully human-reviewed.
- Final UI visual polish (pixel-level refinement against reference screenshots) intentionally deferred per the project's stated priorities.

## 13. Areas With No Bugs Found

Home · HSK index · all 6 HSK Level pages (list, search, pagination, navigation) · Radical index · Radical Detail (including related-vocabulary list and HSK-context isolation) · Dictionary (desktop and mobile, live search, empty state, result selection) · Vocabulary Detail (all 4 entry points, both HSK1 and HSK6 content, radical section) · Practice Home · all 4 Practice modes end-to-end (Chọn nghĩa, Chọn chữ Hán, Flashcard, Luyện viết) including scoring, restart, exit, HSK filter, quantity/"Tất cả" · direct-route loading and refresh for every major route · browser back-button and in-app back-button behavior · query-parameter/context preservation · responsive layout at 3 viewports · light-mode theming · network requests (no actionable failures) · 404 handling for invalid routes/IDs.

## 14. QA Statistics

- Total test scenarios: ~195 individual checks/assertions across all sections
- Passed: ~193
- Failed: 2 (BUG-001, BUG-002)
- Blocked: 0
- Bugs found: 2
  - P0: 0
  - P1: 0
  - P2: 2
  - P3: 0

## 15. Final Git State

- Working tree: clean (`git status --short` empty before and after this QA round)
- Files changed: 0
- Code modified: NO
- Data modified: NO

## 16. Conclusion

READY FOR BUG FIX PHASE
