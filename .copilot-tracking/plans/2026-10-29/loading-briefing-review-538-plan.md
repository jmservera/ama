---
title: PR 538 citation and helper recovery plan
description: Implementation-ready correction candidate, refs 531
ms.date: 2026-10-29
---

Task ID: `538-review-corrections-2026-10-29`.

## Executive Summary

Preserve declared statement citations over line breaks and recognized English
abbreviations. Recover the actual async helper before startup/listener use,
reusing bounded script retries and explicit native reload on exhaustion.
Add narrow parser, loader and actual browser regressions. Run strict core/API
checks and, under a nonblocking heavy lock, full units and relevant browsers.
Keep evidence and commits local; no publication or cloud acceptance is claimed.

## Sources

`.copilot-tracking/research/2026-10-29/loading-briefing-review-538-research.md`
C1-C9; explicit user request and supplied reproductions.

## User Decisions and Requirements

* Fix all three supplied Copilot findings on feat/loading-briefing-hax-531.
* Run full Research, Plan, Implement, Review; preserve dated local evidence.
* `git pull --rebase` first, completed before investigation.
* Run mypy, `ruff check .`, `ruff format --check .` in core and API using
  `/tmp/mv`; install editable packages there; source-first unit fixture paths.
* Full suites require `flock -n /tmp/ama-rpi-heavy.lock`; if busy, targeted
  checks and honest residual reporting are explicitly allowed.
* No push, az, force-push, closing keywords or legacy source locations.
* Conventional Commits with the supplied Copilot coauthor trailer.

## Goals

G1 correct citation-to-statement ownership without inventing evidence.
G2 retain readable abbreviated statements.
G3 keep transient helper failures from stranding staff case work.

## Scope and Non-Goals

Parser and its existing regression file; app bootstrap/loader; existing Node
loader tests and loading browser check; directly related API README.
No new dependency, UI redesign, private data, cloud calls, hosted approval,
publication or re-review loop. Historical RPI artifacts remain unchanged.

## Functional Requirements

FR1 normalize whitespace only around trailing citation groups, including LF,
CRLF and mixed groups, before sentence splitting.
FR2 protect common titles and medial abbreviations (`Dr.`, `Mr.`, `Mrs.`,
`Ms.`, `St.`, `e.g.`, `i.e.`, `vs.` and related forms) while retaining genuine
sentence/newline boundaries and exact displayed text.
Supported related forms: Mx., Prof., Rev., Sr., Jr., cf., approx., etc.
Titles and e.g./i.e./vs./cf. require a following same-line word. Approx./etc.
are medial only before a lowercase word or digit. St. is a name prefix at
statement start, after lowercase context, or before a possessive name; an
ambiguous capitalized street suffix is conservatively left as a boundary.
FR3 include async helper readiness in missingWorkspaceScripts, including
pre-session bootstrap. Register helper-dependent listeners only after readiness.
FR4 preserve cached two-retry, uncertain-execution and stale-session contracts.
FR5 exhaustion/missing readiness shows an announced error and keyboard-native
reload, not silent degradation or renewed automatic retry budgets.

## Non-Functional Requirements

Typed new Python helpers/tests, existing Ruff conventions; no `Any` escape or
typing exemptions added. Native Fluent/plain-language patterns retained.
No model inference, mutation retry or weakened approval/citation controls.

## Acceptance Criteria

AC1 both exact parser examples return one expected cited statement per claim.
AC2 whitespace/group/title/abbreviation regressions pass; separate uncited
sentences remain uncited; newline and genuine punctuation still split.
AC3 initial helper abort recovers the actual helper without a document reload,
allows login and case work, and produces no page errors.
AC4 bounded failures and loaded-without-readiness terminate in native reload;
recovered action listeners execute and ordinary route guards still pass.
AC5 required static/unit/browser commands recorded with exits/skips; if heavy
lock is busy, targeted evidence and unperformed checks are explicitly recorded.
AC6 original critique and independent post-implementation Review are preserved;
all implementation/evidence commits stay local.

## Phase Checklist

<!-- P01 -->
### P01: Correct parser and startup

* [x] P01-T01 add failing parser regressions, implement scoped normalization and
  abbreviation protection, retain declared citation semantics.
* [x] P01-T02 add helper dependency, pre-session bootstrap and terminal recovery
  UX; extend existing Node loader and actual browser regressions.
* [x] P01-T03 update directly related API README and verify manifest scope.

P01 Complete. Regression source, documented behavior and targeted checks agree.

<!-- P02 -->
### P02: Validate and preserve

* [x] P02-T01 execute focused red/green tests, JS syntax, strict package checks;
  under nonblocking lock run full core/API units and relevant browsers.
* [x] P02-T02 reconcile plan/details/changes; commit candidate and original
  evidence for the independent Review. Review itself is the next RPI phase.

P02-T01 completed using the user-authorized targeted fallback: heavy admission
returned 75, owner PID 661156. Full core/API units, browsers and shared editable
setup are unperformed, not passes. Strict core/API mypy/Ruff and 83 focused
unit/manifest tests passed; original failed attempts are recorded in changes.

## Test Ownership and Change Budget

Canonical targets: `src/core/tests/test_ai_statement_sources.py`,
`src/api/tests/test_workspace_scripts.py`,
`src/api/checks/loading_briefing_browser_check.py`.
Generated targets: external browser/axe evidence only, not committed.
Exact removals: none. Maximum additions: four parser methods, one Node scenario
block, one browser scenario function with parameterized recovery/terminal modes.
Semantic coverage: citation ownership and bootstrap ordering. Regression:
existing retry budgets, stale routes/sessions, helper action feedback and
existing briefing browser behavior. No pinned manifest input is planned to change.

## Dependencies and Risks

P02 depends on P01. Browser execution needs installed Playwright/Chromium and
pinned axe 4.10.3. `/tmp/mv` exists; editable mutation and full work occur only
under the shared lock. If busy, no competing install or full run is started.
Abbreviation segmentation remains a bounded heuristic; explicit line breaks
remain authoritative and sentence-final references must not bleed.

## Critique Disposition

Single critique executed: original verdict Revise (PC-001 High, PC-002 Medium).
Preserved at
`.copilot-tracking/reviews/plans/2026-10-29/loading-briefing-review-538-plan-critique.md`.
PC-001 accepted/directly resolved in FR2 and P01-T01: contextual abbreviation
rules and exact same-token negative fixtures, no general NLP claim.
PC-002 accepted/directly resolved in P01-T02: null-session bootstrap selects
only helper, checks readiness, and cannot register helper listeners or call
start after terminal failure. No user decision needed; no second critique.

## Follow-Up Items

Human accessibility, deployed cold start and hosted/publication gates remain
outside this correction. FU-001: run full units, editable setup and both
relevant browser checks at a later explicit free-lock coordination event;
current browser regressions are authored/type-checked but unexecuted.

## Handoff

Details: `.copilot-tracking/details/2026-10-29/loading-briefing-review-538-phase-details.md`.
Changes: `.copilot-tracking/changes/2026-10-29/loading-briefing-review-538-changes.md`
(implementation-owned). Planning execution Complete; implementation-ready
after direct critique dispositions above.
Implementation reconciliation: P01/P02 Complete, all task markers evidenced.
Candidate and dated original evidence committed locally as `0e910aa1`.
Full/browser validation remains an explicit residual, not an implementation
acceptance claim. Ready for the one independent post-implementation Review.
