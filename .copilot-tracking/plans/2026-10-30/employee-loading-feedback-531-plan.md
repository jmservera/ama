---
title: Employee loading and briefing plan
ms.date: 2026-10-30
---

## Task Metadata

* Task ID: 531
* Task slug: employee-loading-feedback-531
* Planning status: Ready; original critique Complete / Revise, dispositions below
* Phase details: .copilot-tracking/details/2026-10-30/employee-loading-feedback-531-phase-details.md

## Executive Summary

The requested baseline already delivers the loading/HAX implementation through
merged #538. Preserve it and add explicit JavaScript-disabled static-shell
browser evidence, then freshly execute the existing regression scenarios.
Correct the guide's lock command to the requested wait-600 policy.

### What You May Not Know

Issue comments explicitly leave only live employee-site verification open.
Delaying app.js is useful but does not independently prove a static page
works with all page scripts disabled. The UX specialist returned intake
questions rather than a note; the existing parent-written HAX mapping remains
the design rationale, not specialist or staff acceptance.

## User Decisions and Requirements

* Run research, plan, implement, review in order; record dated artifacts.
* Use the current branch and main baseline 5634f9a077d175a931c15e3400114665d8c071ee.
* Implement issue scope including owner comment; do not duplicate delivered UI.
* Source in src/, tests outside packages, pip only, native Fluent 2 foundations,
  WCAG engineering baseline, plain language, non-colour text and reduced motion.
* Run API discovery, Ruff lint/format and mypy; actual local browser and axe.
* Serialize heavy gates with flock -w 600 /tmp/ama-rpi-heavy.lock.
* Commit locally with required trailer and Refs #531 only. No push, Azure,
  deployment, live sign-in, secrets or credential files.

## Goals

* Establish fresh, bounded evidence for each local acceptance criterion.
* Protect shipped startup, review, source and manual-work behavior.

## Scope and Non-Goals

In scope: the existing loading/briefing browser check, its README instructions
and dated evidence. No runtime source change unless a scoped reproduction
reveals a defect. Non-goals: redesigning delivered controls, framework changes,
live acceptance, assistive-technology claims or closing the issue.

## Functional Requirements

* Static shell remains visible/readable with page JavaScript disabled.
* Existing slow/retry/per-panel/action/HAX/review behavior remains exercised.
* Review is draft feedback only, never works approval or resident consent.

## Non-Functional Requirements

* Constructed synthetic loopback server only; external browser traffic blocked.
* Static shell checked at 320 and 1280 CSS px without horizontal overflow;
  startup status exposes polite native status semantics and no spinner-only signal.
* Existing actual-helper Node test in test_loading_feedback.py verifies 199/200
  ms timing; the browser runner verifies real pending controls, reduced motion
  and axe, not the exact threshold.

## Acceptance Criteria

| Criterion | Planned evidence |
| --- | --- |
| AC1 static/panel loading, live/slow/retry | New no-JS shell scenario plus existing shell/helper/panel tests |
| AC2 simulated cold start, not blank | Held app.js scenario plus no-JS static text/screenshots |
| AC3 AI/rules/source distinction and HAX note | Existing app/API tests, browser labels and README mapping |
| AC4 clear outcomes and unchanged boundaries | Existing conditional-review browser and API regressions |
| AC5 sources/time/unverified | Existing source/time/unverified browser and API regressions |
| AC6 automated browser/axe, no AT claim | Fresh pinned-axe report and browser log |
| AC7 separate live check | Not proven; prohibited in this run |

## Sources

Research: .copilot-tracking/research/2026-10-30/employee-loading-feedback-531-research.md.
Existing implementation and guide locations are C2-C6 there. Issue comments
confirm #538 merged; #529 dependency is merged.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Strengthen and execute local evidence

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add static pre-script browser coverage and align guide

Add one JavaScript-disabled scenario to the existing check; verify status text,
markup order, empty app, responsive geometry and retain
screenshots. Do not execute axe in this disabled-script scenario; existing
script-enabled axe scans remain separately reported. Correct guide lock text.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Validate and reconcile

Run API discovery, Ruff check/format, mypy and loading/briefing Playwright/axe
under heavy lock. Use existing /tmp/mv tools after recording system Python's
missing packages. Never mutate the shared environment if existing tools work.
Record exact output and limitations before one post-implementation Review.

## Locked Test Ownership and Targets

Canonical target: src/api/checks/loading_briefing_browser_check.py.
Guide target: src/api/README.md. Generated evidence: fresh external directory,
not bundled into the package. Test removals: none. Maximum additions: one
browser scenario with two viewport assertions. Existing browser runner owns
server creation/readiness/termination. Semantic coverage: no-script behavior
and geometry. Regression coverage: inherited action/HAX/retry suites.

## Dependencies

Existing installed source dependencies, Node, Chromium and pinned axe.
Full publication gate may be blocked by local scanner/SQL prerequisites.

Current local result: 1370 API tests passed (318 opt-in skips), Ruff lint and
format passed, mypy passed for 116 source files. Full existing browser scenario
and four axe scans passed, including the added no-script shell evidence.
Execution logs and original failed assertion are retained externally and
summarized in the changes record. No production behavior changed.

## Critique Disposition

One independent critique executed, original verdict Revise preserved at
.copilot-tracking/reviews/plans/2026-10-30/employee-loading-feedback-531-plan-critique.md.

| Finding | Disposition | Evidence |
| --- | --- | --- |
| PC-001 | Rejected as conflicting with confirmed caller direction | Parent has no temporary-path prohibition; user explicitly requires /tmp/ama-rpi-heavy.lock. Worker-local restrictions do not constrain parent. Existing tools /tmp/mv and pinned axe read are permitted. Use fresh external /tmp/ama-issue-531-20261030-* outputs; never substitute lock identity. |
| PC-002 | Applied directly | Exact 199/200 ms belongs to src/api/tests/test_loading_feedback.py test_actual_helper_timing_duplicates_errors_and_state_ownership; browser attribution corrected above. |

## Follow-Up Items

* Owner/coordinator: separately authorized live employee verification; no
  screen-reader/voice-control or full Fluent acceptance is claimed.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-30/employee-loading-feedback-531-changes.md.
After one Review and local commit, attempt complete local gate with original
evidence preserved. Final receipt stays external; no push is authorized.
Implementation P01 complete; ready for one post-implementation Review.
