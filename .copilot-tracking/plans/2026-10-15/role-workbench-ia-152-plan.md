---
title: Role workbench IA 152 plan
description: Implementation-ready bounded shared layout and navigation plan
ms.date: 2026-10-15
---

Task: `152`; slug: `role-workbench-ia-152`. Status: implemented, review preparation.

## Executive Summary

Reuse the migrated API web and Fluent foundations. Describe existing navigation
on the server, label active scope, preserve queue context when opening cases,
and restore the default own queue/filter/sort with a focused, announced reset.
Bring safety detail forward and check narrow reflow without hiding controls.
This is shared IA, not role-screen delivery or owner-supported device approval.

## User Decisions and Requirements

* Execute Research, Plan, Implement and Review once; commit all evidence in PR.
* Work only on the specified worktree/branch. Code/tests in src, no mvp code.
* No new client role gating, SQL dialect changes, private data or deployment.
* Keep AI routes enabled/configurable, human approvals and resident consent.
* Run src suites, ruff, mypy, synthetic local app/browser checks; pip only.
* Record commands/results, update reference index/log, commit with required
  privacy-safe email and trailer, push and create main PR using Refs #152.
* Owner device decisions and unavailable evidence remain unchecked.

## Sources

Research: `.copilot-tracking/research/2026-10-15/role-workbench-ia-152-research.md`.
Issue #152 and comments, ADR 0006, parity matrix, PRD SA-001/002/003/007,
AC-034/043; current projection/server/web and merged #150/#151 foundations.

## Goals

Consistent authorized workspace navigation, clear scope and safe recoverability
at desktop/laptop/tablet/narrow engineering widths.

## Scope and Non-Goals

API navigation descriptor and web IA/CSS, tests and synthetic browser evidence.
No change to permission policy, store behavior, AI releases, role-specific
screens, supported device commitments or live platform deployment.

## Functional Requirements

* Navigation descriptors derive from existing server access rules; no client map.
* Show current page and signed-in scope; case back navigation restores queue.
* Reset clears every filter including sort and all-cases override, retains
  logical focus and announces counts; reset changes no case.
* Existing list row remains the single case-opening action, with plain status.
* Safety controls remain expanded and precede routine case forms.
* No-match and no-own-case messages differ. Unknown record details remain unknown.

## Non-Functional Requirements

Use Fluent tokens, semantic landmarks/links, visible current state, keyboard
focus and 320px reflow. No dependency changes or SQL additions. All new Python
remains typed; existing tooling exemptions are not expanded for new tests.

## Acceptance Criteria

* [ ] Owner agrees supported devices/widths: excluded pending owner decision.
* [x] Width evidence at 320, 390, 768, 1024, 1280 CSS px, plus text enlargement.
* [x] Server-described permitted navigation, own default, no role simulator.
* [x] Safety visible on list/case at checked widths; no permission expansion.
* [x] Bounded AC-034/043 manifest checks with every unrepresented perspective
  and workflow explicitly deferred; no full cross-profile acceptance claim.

## Phase Checklist

<!-- P01 -->
### P01: Shared navigation and recoverable context

* [x] P01-T01: Add typed API navigation descriptor and endpoint/unit coverage.
* [x] P01-T02: Render descriptors/current state; scope/reset/back context;
  safety-first case ordering and responsive shell.

<!-- P02 -->
### P02: Evidence, documentation and delivery

* [x] P02-T01: Add bounded manifest and real synthetic app browser checks;
  reuse existing isolated launcher without copying server lifecycle.
* [x] P02-T02: Run all five src suites, lint/types, JS syntax and browser
  checks. Attempt Docker; document unavailable SQL/model/Azure/human checks.
* [x] P02-T03: Update API README, UX synthesis, reference index/log and reconcile
  plan/details/changes for one review. Publication remains the parent action
  after Review: commit, push and open Refs #152 PR.

## Test Ownership and Change Budget

Canonical code: API workbench/server metadata. No generated production files.
Exact removals: none. Maximum additions: one API navigation module, one API
unit-test file, one browser-check file and one JSON manifest under API checks.
Tracking artifacts are explicitly requested and outside that code budget.
Reuse the existing browser launcher through a typed callback. Semantic coverage:
permitted descriptor endpoints, reset defaults/count/order/focus/record invariance,
back context, safety presence/reflow. Regression coverage: existing role matrix,
design-system/browser baseline, all src project suites. No weakened tests,
no new runtime or dev dependencies, no fabricated live inference success.

## Critique Disposition

Exactly one critique executed; verdict Revise. All findings are planner-owned
and compatible with user direction; no owner decision or repeated critique.

| Finding | Direct disposition and resolving evidence |
| --- | --- |
| PC-001 | Introduced failures block slice readiness. Fix/validate before Review; any material Review defect leaves not-ready outcome, never a false pass |
| PC-002 | API-only synthetic extension supplies eight roles, two owners, other contractor and empty queue. JSON freezes expected IDs/order/routes independently; eleven/nine declarations remain explicit partial coverage |
| PC-003 | Route lifetime aborts stale async loads; query state updates immediately, debounce cleared on route/reset. Direct case fallback is mine; return reloads page one and says so, not a promise to retain pagination |
| PC-004 | Browser scratch under ignored `.venv/` with explicit cleanup and sanitized environment |
| PC-005 | Queue/hazard checks at five widths, keyboard/reset/current nav/status, 200% root text, long source wrapping, failed load/session handling; no human/screen-reader claim |
| PC-006 | Existing CI browser entry point invokes both checks; generic CI is not live SQL/model/Azure proof |

The review artifact is
`.copilot-tracking/reviews/2026-10-15/role-workbench-ia-152-plan-critique.md`.

## Follow-Up Items

Owner device/browser matrix; complete eleven-profile/nine-workflow journey
acceptance; assistive-technology/human checks; authorized live AI/SQL/Azure
evidence. These do not block the bounded engineering slice.

Full originating-row focus, scroll, selection and pagination restoration are
not delivered. UX-07/full AC-034 are partial, not accepted by this slice.

## Handoff

Details: `.copilot-tracking/details/2026-10-15/role-workbench-ia-152-phase-details.md`.
Changes destination:
`.copilot-tracking/changes/2026-10-15/role-workbench-ia-152-changes.md`.
Implementation and local validation complete; P01/P02 complete for review.
Parent performs one Review, then publishes with unchecked issue criteria.
No further critique or implementation loop is authorized inside this task.
