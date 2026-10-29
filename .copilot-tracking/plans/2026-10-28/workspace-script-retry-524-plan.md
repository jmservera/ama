<!-- markdownlint-disable-file -->
---
title: Workspace script retry implementation plan
description: Bounded employee workspace recovery for issue 524
ms.date: 2026-10-28
---

# RPI Plan: workspace-script-retry-524

## Task Metadata

* Task ID: 524
* Task slug: workspace-script-retry-524
* Planning status: Ready; original Revise critique dispositioned directly
* Plan date: 2026-10-28
* Phase details: .copilot-tracking/details/2026-10-28/workspace-script-retry-524-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-28/workspace-script-retry-524-plan-critique.md

## Executive Summary

Retry only missing route dependencies twice after their initial HTML request,
then recheck readiness before rendering. Keep the existing terminal message,
status region, alert and native reload button. Shared per-path attempts prevent
navigation from multiplying requests. Only a definitive load error permits the
next attempt: timeout or load-without-readiness stops recovery, avoiding duplicate
execution of lexical scripts. Browser fault injection will demonstrate recovery,
exhaustion and safe late delivery against an owned synthetic server.

### What You May Not Know

Reloading every script risks lexical redeclarations and duplicate registrations.
The live transport cause is unresolved; correct local server headers do not
establish what happened on the deployed path. Live verification remains pending
the owner. Publication requires independent Review and the repository's complete
exact-head gate; missing prerequisites or lock contention may block publication.

## User Decisions and Requirements

* Run research, plan, implement and review for issue #524 in that order.
* Use fix/workspace-script-retry-524 in the requested worktree; source is src/.
* Preserve native semantics, existing plain language and non-colour signals.
* Do not use Azure, secrets, .env or private datasets.
* Hold /tmp/ama-rpi-heavy.lock nonblocking for heavy gates.
* Run API discovery and a browser failed-first-load simulation.
* Commit dated evidence with Conventional Commit style and supplied coauthor
  trailer; resolve privacy-safe identity with gh api user.
* Push without force and create a PR; use Refs #524 unless all criteria are proven.

## Goals

* A transient missing workspace dependency recovers without refreshing the page.
* Persistent failures stop predictably with the existing actionable error.
* Preserve current route, session and accessibility behavior.

## Scope and Non-Goals

Included: app.js startup guard, targeted unit/browser coverage, API README and
dated RPI artifacts. Excluded: HTML/CSS redesign, server/auth changes, deployment,
infrastructure speculation, real users/data and unrelated cleanup.

## Functional Requirements

* Preserve all existing route/role dependency predicates.
* Retry absent fixed same-origin script paths at most twice per page lifetime,
  sharing in-flight/completed attempts across routes.
* Recheck expected globals after recovery; a 200 response is not readiness.
  Do not re-evaluate a script that loaded without its expected global.
* Await readiness before rendering; an obsolete or signed-out route cannot render.
* Keep exact existing failure copy and native Reload workspace action.

## Non-Functional Requirements

* Each attempt times out after 5 seconds; use 250ms then 500ms delay.
  Timeout is terminal for that path: removing a tag does not guarantee execution
  cancellation, so no overlapping attempt is allowed after timeout.
* Remove retry elements and clear handlers/timers on settlement.
* Do not reload already-present dependencies or reset budgets on navigation.
* No new dependency; new Python lines <=100 characters.
* No color-only progress or failure state; reuse polite status for recovery.

## Acceptance Criteria

* AC1: Record unresolved live cause with inspected script order, serving headers,
  complete bytes and missing live transport/cold-start evidence.
* AC2: First script request fails; automatic retry loads the actual script and
  intended workspace without document reload.
* AC3: Initial failure plus two failed retries stops with exact existing text,
  alert/status and keyboard-operable Reload workspace button.
* AC4: Persist regression tests and execute browser failed-first-load coverage.
* AC5: Mark live post-deploy verification pending owner, not locally proven.
* Additional: needed companion script recovery, missing global despite HTTP 200,
  hanging attempt timeout, shared budgets, navigation cancellation and sign-out.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-28/workspace-script-retry-524-research.md
(executed, Ready). Changes:
.copilot-tracking/changes/2026-10-28/workspace-script-retry-524-changes.md.
Automatic parent owns ordered continuation after critique disposition.

## Sources

* Issue 524 and research C1-C7/W1-W2 establish contracts and explicit uncertainty.
* src/api/tests/test_role_screens.py supplies Node VM regression prior art.
* src/api/checks/design_system_browser_check.py supplies synthetic server lifecycle.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement bounded recovery

* Dependencies: completed research and final-candidate critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Await missing dependencies safely

Use fixed-path load promises with two timed attempts; retain route predicates and
terminal copy, and check the route signal after awaiting recovery.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add regression coverage and operator documentation

Unit tests own retry mechanics and route guard semantics; browser check owns real
script evaluation, HTTP delivery and native UI recovery/exhaustion.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and prepare independent Review

* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Run focused and API validation

Run Node checks, new unit tests, API discovery, Ruff/mypy and owned Chromium
fault injection under nonblocking shared lock.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile evidence and hand off to Review

Mark executed work honestly; preserve failures, pending live checks and any gate
blocker. Independent Review is once-only; findings route to follow-up work.

## Test Ownership and Change Budget

* Canonical production target: src/api/src/zava_forward/api/web/app.js.
* Documentation target: src/api/README.md.
* Removals: none. Generated production targets: none.
* Maximum added executable files: two, test_workspace_scripts.py and
  workspace_scripts_browser_check.py. No framework/dependency additions.
* Semantic coverage: real script execution, actual view rendered, unchanged
  native status/alert/button, no stale view. Regression coverage: exact attempt
  count, timeouts, shared promises, no unnecessary loads and unchanged error copy.
* Evidence: new checks, API suite output and original critique/Review artifacts;
  final exact-head full receipt remains external.

## Dependencies

Existing API/core/agents dev distributions, Node, Chromium/Playwright. Installed
existing dev distributions in /tmp/ama-524-venv after system import failed.
Complete publication gate additionally requires its pinned local prerequisites.

## Critique Disposition

Exactly one critique executed; original verdict Revise is preserved.

| Finding | Disposition | Resolving plan evidence |
| --- | --- | --- |
| PC-001 | Applied | Timeout is terminal, never followed by reinjection. Browser withholds a lexical companion beyond timeout, releases it late and checks no duplicate/stale rendering. |
| PC-002 | Partially applied; unsafe retry advice rejected | Global recheck remains mandatory, but a completed load without its sentinel is terminal, not retried: it may have installed lexical constants before failing. Browser and unit tests explicitly prove terminal semantics and retained budget. This is a safe limitation, not transport recovery success. |
| PC-003 | Rejected as inapplicable | Parent execution rules and explicit user direction authorize /tmp task environment and mandated /tmp shared lock. Critique worker's claimed temporary-directory prohibition is not present in the parent execution contract. No lock substitution or gate waiver. |

## Follow-Up Items

* RV-001, later rpi-implement: guard session validity after recovery without
  relying on an artificial route abort; add actual 401/session-ended coverage.
* RV-002, later rpi-implement: make late lexical-script evaluation/settlement
  proof deterministic and compare independent-route status before/after delivery.
* RV-003, later bounded evidence collection: execute mandatory API/Chromium
  checks under the required lock and retain actual output, then complete required
  exact-head publication gates. Original missing evidence is preserved.
* Owner: capture authenticated live failed response status/size/headers and correlate
  cold-start/auth telemetry, then verify after separately approved deployment.

## Handoff

P01 source/tests/documentation complete. P02-T01 heavy validation remains blocked
by nonblocking shared-lock contention; P02-T02 reconciliation complete.
Hand off the stable candidate once for independent Review with missing API/browser
evidence explicitly declared. This is not a conformant implementation or
publication-readiness claim. No second critique or Review.
The one independent Review has now completed with outcome Not accepted.
RV-001/RV-002 are unresolved defects, RV-003 is missing mandatory execution
evidence, and RV-004 routes the pre-existing owner live follow-up. No source
correction or repeated Review is performed inside this completed assessment.
