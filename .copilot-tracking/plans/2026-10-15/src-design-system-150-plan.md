---
title: Issue 150 implementation plan
ms.date: 2026-10-15
---
<!-- markdownlint-disable-file -->

## Task Metadata

Task ID: 150. Slug: src-design-system-150. Status: Ready after critique corrections.
Details: .copilot-tracking/details/2026-10-15/src-design-system-150-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-15/src-design-system-150-plan-critique.md.

## Executive Summary

Deliver a partial Fluent 2 adoption-foundation slice in the migrated
workbench; replace colour-only map and selected-filter cues with shapes and
visible words. Reuse the existing UI and its AI/human-review boundaries.

### What You May Not Know

The previous extend-current-UI recommendation is superseded by the owner's
Fluent 2 decision. This slice does not import a packaged Fluent UI runtime.
Adoption delivery remains an open gate owned by the delivery workstream: select
and integrate an actual Fluent component implementation, with rendered state,
dependency/CSP and accessibility evidence, or obtain explicit owner acceptance of
a native-only substitute. This PR must not close #150 or claim adoption complete.
Human accessibility acceptance and live AI/SQL/Azure evidence are unavailable
locally and will not be claimed. No production deployment is authorized.

## User Decisions and Requirements

* Run the complete RPI loop, commit evidence, push this branch and open a main PR.
* Work exclusively in the specified worktree and branch; all code/tests in src.
* Follow accepted ADR 0006 and the parity matrix, reusing merged moves #296-302.
* Adopt Fluent UI (Fluent 2), replacing the rejected extend-current-UI decision.
* Preserve AI availability, human approvals, resident consent and synthetic-only tests.
* Pip only; no excluded paths, deployment, new SQL or workload dependencies.
* Record every validation command/result and unmet evidence; use Refs #150.

## Goals

Consistent documented tokens/components and status/safety meaning independent
of colour, with reproducible local regression and browser evidence.

## Scope and Non-Goals

In scope: API web stylesheet/app, existing design/accessibility tests, one browser
check, API development dependencies and source-CI browser wiring,
design-system synthesis/index/log, API README, RPI artifacts.
Non-goals: framework rewrite, runtime library adoption claim, new AI provider,
SQL changes, Azure deployment, human or full WCAG conformance acceptance.

## Functional Requirements

* Fluent semantic aliases drive native buttons, fields, cards, type and spacing.
* Map normal/waiting/hazard markers have circle/square/triangle outlines and
  O/W/! text; key, title and accessible name explain the same meaning.
* Clusters visibly show total and safety count; list alternative remains.
* Tiles show "Selected" text, not only border/shadow; hazard tile has text cue.
* AI review and blocked owner/next-action patterns stay documented accurately.

## Non-Functional Requirements

* Text contrast at least 4.5:1 and relevant control/shape outlines 3:1 on surfaces.
* Keyboard map/list activation, forced colours and reduced motion are exercised.
* Synthetic browser checks at 320, 390 and 1280 CSS pixels; no injected record HTML.
* Preserve dependency/image rules and all relevant existing project suites.

## Acceptance Criteria

* [x] Tokens for colour/type/spacing/focus/motion defined, consumed and documented.
* [x] Inventory documents seven states, blocked owner/next action and AI review.
* [x] Map/cluster/tile status cues work without colour in tested synthetic states.
* [x] Superseded proposal replaced with sourced owner adoption decision.
* [x] Local suites/lint/types/browser evidence recorded, including limitations.
* [ ] Full Fluent UI runtime migration, human accessibility and live AI/SQL/Azure
  remain explicitly unverified; do not check their acceptance by proxy.

## Sources

Research: .copilot-tracking/research/2026-10-15/src-design-system-150-research.md,
C1-C7 and W1-W3. Official Fluent typography retrieved 2026-10-15 additionally
supports Segoe/system font stack and rem-equivalent title/body ramp.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement foundations and non-colour signals

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Adopt Fluent token aliases and native foundation styles

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Replace map/cluster and tile colour-only cues

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and document the slice

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Extend owned tests and execute local checks

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile design documentation and knowledge-base evidence

<!-- rpi:phase id=P03 -->
### [x] P03: Review and deliver

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Complete one implementation Review and publish the PR

After P02, activate rpi-review once, record outcome and route open findings
without a repeat review loop. Reconcile changes, plan/details and criteria.
Commit research, plan, details, critique, changes, review and state with source/docs.
Use authenticated identity and local noreply email; push only the specified
topic branch; open a main PR with Refs #150, every validation command/result and
unmet gates. Do not merge. Capture commit and PR identity as delivery evidence.

## Dependencies

#290 and moves #296-302 are merged. Installed packages and browser binaries are
local validation prerequisites; Docker permission and live services may block checks.

## Locked Test and Change Ownership

Removals: none. Maximum additions: one API browser-check module, no new production
modules or runtime dependencies. Pin Playwright as API development tooling so
strict type checking works on clean CI installations and run the harness in CI.
Update existing API design and contrast tests for semantic
tokens and regression assertions. Browser check owns rendered shape/text, actual
Leaflet point/cluster modes, keyboard activation, widths, forced colours, reduced
motion and preserved AI labels. Canonical targets are src/API assets and design
synthesis; no generated assets except committed RPI evidence. Full project suites
and per-project ruff/mypy guard integration; no existing exemptions added.
The new check must also pass isolated ruff lint/format with E,F,I,B,UP,
line length 100 and Python 3.12 to bypass inherited checks/*.py exemptions,
and strict project mypy.
Implementation-time relevant update: narrow Overview data tables use named,
focusable scroll containers to meet the planned 320px reflow check while
preserving native table semantics. Leaflet forwards key events but requires an
explicit Enter/Space handler for custom marker activation.

## Critique Disposition

One critique executed, verdict Revise. Compatible corrections applied directly;
no second critique. No user decision required for these truthful scope corrections.

| Finding | Disposition | Resolving change |
| --- | --- | --- |
| PC-001 High | Resolved for partial delivery | Explicit open adoption gate; #150 stays open; no native-only final-substitute claim |
| PC-002 Medium | Resolved | Concrete sourced mapping and deviations in details; assertions and rendered evidence required |
| PC-003 Medium | Resolved | Isolated lint/format plus strict mypy required for new check |
| PC-004 Medium | Resolved | P03 owns one Review, artifact completeness, privacy-safe commit, push and Refs PR |

## Follow-Up Items

* Packaged Fluent UI runtime migration: beyond native foundations; do not call
  token/style adoption a complete library rollout.
* Human accessibility acceptance and live AI/SQL/Azure validation: require
  authorized humans/services; not fabricated by local synthetic runs.

## Handoff

Implementation creates .copilot-tracking/changes/2026-10-15/src-design-system-150-changes.md.
P01/P02/P03 complete for the declared partial slice. One Review executed Complete,
outcome Residual work. Implementation commit
9f80a45115c5c8cebb8d3506518251fd7c75b074 is pushed on the requested branch;
main PR https://github.com/jmservera/ama/pull/313 is open with Refs #150.
Full adoption/human/live gates remain unchecked; CI and owner review precede
any merge. No further source changes or second Review occurred.
