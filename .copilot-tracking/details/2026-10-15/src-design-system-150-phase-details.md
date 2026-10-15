---
title: Issue 150 phase details
ms.date: 2026-10-15
---
<!-- markdownlint-disable-file -->

## Metadata

Task ID: 150. Slug: src-design-system-150.
Plan: .copilot-tracking/plans/2026-10-15/src-design-system-150-plan.md.
Research: .copilot-tracking/research/2026-10-15/src-design-system-150-research.md.

## Phase Index

| Phase | Intent | Status |
| --- | --- | --- |
| P01 | Fluent foundations and visible signals | Complete, browser and token checks passed |
| P02 | Validation and durable documentation | Complete, five suites/lint/types and 31 browser checks passed |
| P03 | One Review and persistent PR delivery | Depends on P02 |

<!-- rpi:phase id=P01 -->
## P01: Implement foundations and non-colour signals

Context: research C1-C7 and owner W1. API owns web assets; no workload/import or
data-model changes. Existing authorization and AI proposal behavior are invariant.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Adopt Fluent token aliases and native foundation styles

Targets: src/api/src/zava_forward/api/web/style.css.
Add Fluent-style neutral/brand semantic colours, font ramp, spacing/radii and
motion aliases; retain legacy names as bridges used by untouched screens. Preserve
accessible 16px base, teal brand, two-tone focus and reduced-motion preference.
Use tokens in touched native buttons/fields/cards/layout. Contrast tests must
resolve aliases; avoid fake "library installed" claims.
Completion: rendered tokens resolve and contrast thresholds hold.

Concrete mapping contract (official microsoft/fluentui token sources at
84abdb5fd25a10c627a08465ae82a96e17927270, retrieved 2026-10-15):

| Source | Values and consumption |
| --- | --- |
| packages/tokens/src/global/spacings.ts | XS/S/M/L/XXL = 4/8/12/16/24px; rem equivalents drive control/card padding, gaps and legacy spacing bridges |
| packages/tokens/src/global/borderRadius.ts | Medium=4px and XLarge=8px; rem equivalents drive fields/buttons and cards |
| packages/tokens/src/global/durations.ts | durationFast=150ms; transitions, overridden to zero for reduced motion |
| packages/tokens/src/alias/lightColor.ts | colorNeutralForeground1=#242424 and Foreground2=#424242; body and muted labels |
| https://fluent2.microsoft.design/typography | Segoe/system font, Subtitle1 20/26px and Title3 24/32px; rem-based headings |

Explicit customizations, not asserted official Fluent defaults: preserve the
existing teal brand/status palette; keep 16px body rather than Fluent 14px Body1;
retain two-tone 3px focus, stronger field boundary and 40px native controls.
Document semantic colour aliases and legacy bridges in the design synthesis.
The implementation is preparation, not final Fluent UI runtime adoption.
Completion evidence: mapped token/contrast tests passed; real rendered card,
heading and button dimensions checked in Chromium 156.0.8078.4.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Replace map/cluster and tile colour-only cues

Targets: app.js and style.css. Build Leaflet divIcon content with DOM/h(), not
interpolated record HTML. Normal/wait/hazard use distinct border shapes plus
visible O/W/!; include status in marker title/tooltip. Clusters show counts and
safety words including zero; labels do not depend on hover. Keep the existing
list alternative and keyboard links, with native marker keyboard handling.
Tiles include selected words and pressed state without obscuring the action.
Completion: point and cluster modes, forced colours and keyboard activation work.
Completion evidence: real API with 505 fictional homes, three point states and
safety/zero-safety cluster counts; Enter/Space, selected words, forced-colour
symbols and retained list checked. No mocked map API responses.

<!-- rpi:phase id=P02 -->
## P02: Validate and document the slice

<!-- rpi:task id=P02-T01 -->
### P02-T01: Extend owned tests and execute local checks

Targets: existing test_design_system.py, test_accessibility_baseline.py; one
src/api/checks/design_system_browser_check.py. Use the existing dataset fixture,
real loopback API and installed src packages. Force map mode with constructed
API fixtures if a natural >500-point cluster is excessive; disclose mocked map
responses and test real endpoint separately in existing suites. No private data.
Exercise 320/390/1280px, computed tokens, text and shape cues, focus, list/marker
activation, forced colours, reduced motion and AI label availability.
Run five src suites, ruff check/format/mypy, node syntax and Docker permission
probe. Record exact commands/results, including missing tools and failed attempts.
No new tooling exclusions; use pip when dependencies are actually missing.
New check additionally uses isolated ruff lint (E,F,I,B,UP; py312; 100 columns)
and isolated format checking so migration wildcards cannot hide findings.
Pin the browser package in API dev extras and execute the isolated checks and
synthetic browser harness in src-ci. This is test tooling only, not a production
dependency or workload/image change. Actual narrow-screen execution exposed
wide Overview tables; add named focusable scroll regions and verify keyboard
scrolling rather than altering native table display semantics.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile design documentation and knowledge-base evidence

Targets: docs/reference/research/ux/design-system.md, index, append-only log,
src/api/README.md. Record dated owner decision, native-foundation versus packaged
library boundary, seven-state usage and tested non-colour semantics. No claim of
human conformance or real inference. Record every unmet acceptance item.
Completion: links/diff reviewed, evidence reconciled with plan, ready for one
post-implementation Review; commit all requested RPI artifacts in the PR.

<!-- rpi:phase id=P03 -->
## P03: Review and deliver

<!-- rpi:task id=P03-T01 -->
### P03-T01: Complete one implementation Review and publish the PR

Review artifact: .copilot-tracking/reviews/logs/2026-10-15/src-design-system-150-review.md.
Assess actual changes and validation against this plan once. Keep full runtime
adoption and human/live-service gates open, with owner/evidence requirements.
Do not repeat Review or treat unresolved material findings as conformant.
Reconcile state and artifacts, commit all requested evidence, confirm noreply
author/committer, push feat/src-design-system-150 and create main PR with Refs #150.
No issue closure or merge. Record exact commands, results, commit SHA and PR URL.
