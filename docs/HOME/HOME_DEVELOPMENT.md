# Chinese Thu Man — HOME Development Specification v1.0

## 1. Target

Implement Home in the existing Chinese Thu Man WEB project.

Before coding:
- inspect the current framework
- inspect existing routes
- inspect global layout/header
- inspect design tokens
- inspect vocabulary repository
- inspect reusable card/button components

Reuse existing architecture.

## 2. Component Responsibilities

Recommended conceptual components:

```text
HomePage
├── AppHeader
├── HeroSection
├── FeatureCard
├── FeatureGrid
├── HSKQuickAccess
└── HSKLevelCard
```

Use existing project component names where applicable.

## 3. Data Access

Home should consume a repository/service abstraction rather than importing raw JSON everywhere.

Conceptual API:

```text
getTotalVocabularyCount()
getVocabularyCountByHsk(level)
```

If the dataset is static, these functions may operate locally.

Do not create a second Home-specific vocabulary dataset.

## 4. Routing

Use the existing router.

Conceptual destinations:

```text
HSK → /hsk
Dictionary → /dictionary
Practice → /practice
HSK Level → /hsk/{level}
```

Adapt to actual repository routing.

## 5. No Fake Data

Do not hard-code:
- vocabulary counts
- learning progress
- user statistics

Static copy such as titles/descriptions may be defined in UI configuration.

## 6. Reuse

Use shared:
- header
- buttons
- cards
- colors
- typography
- spacing

Do not create a separate Home design system.

## 7. Performance

Home should load quickly.

Prefer:
- static local vocabulary data
- derived counts
- no unnecessary API calls
- no heavy dependencies

Do not add a backend solely to support Home.

## 8. Error Handling

If vocabulary data fails:
- preserve page layout
- show a local error state for dynamic counts
- keep primary navigation functional

## 9. Responsive WEB

Implement responsive web behavior:
- flexible feature grid
- wrapping HSK cards
- constrained content width
- no horizontal overflow

Do not create mobile-app-specific navigation.

## 10. Implementation Order

1. Inspect repository
2. Identify/reuse AppHeader
3. Implement Home layout
4. Connect feature navigation
5. Connect HSK count data
6. Add loading/error states if needed
7. Verify desktop layout
8. Verify narrower browser widths
9. Run tests/build

## 11. Completion Report

Report:
- files created
- files modified
- routes connected
- data source used
- tests run
- build result
- visual differences from approved UI
