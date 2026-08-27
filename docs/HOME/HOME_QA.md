# Chinese Thu Man — HOME QA Specification v1.0

## Navigation

### HOME-001
Click `Trang chủ`.
Expected:
Home opens and Home is active.

### HOME-002
Click `HSK`.
Expected:
HSK Overview opens.

### HOME-003
Click `Từ điển`.
Expected:
Dictionary opens.

### HOME-004
Click `Luyện tập`.
Expected:
Practice Home opens.

### HOME-005
Click an HSK level card.
Expected:
The selected HSK Word List opens.

## Data

### HOME-010
Compare displayed HSK vocabulary count with canonical dataset.
Expected:
Count is accurate.

### HOME-011
Change vocabulary dataset.
Expected:
Home-derived count changes automatically; no duplicated hard-coded count remains.

### HOME-012
Vocabulary data unavailable.
Expected:
Friendly error/loading state; page does not crash.

## MVP Scope

### HOME-020
Verify there is no login requirement.

### HOME-021
Verify there is no fake personal progress/statistics.

### HOME-022
Verify no payment/subscription UI exists.

## Visual QA

Check against approved Home UI:
- header alignment
- active Home state
- white background
- primary blue `#025291`
- card proportions
- border radius
- shadows
- typography hierarchy
- spacing
- CTA hierarchy
- HSK card layout

## Responsive WEB QA

Test at:
- desktop target width
- medium browser width
- narrow browser width

Expected:
- no horizontal overflow
- cards remain usable
- text remains readable
- navigation remains functional

This is responsive WEB testing, not mobile-app testing.

## Build QA

- dev server starts
- production build succeeds
- no Home console errors
- no broken Home routes
- no missing assets
