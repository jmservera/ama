<!-- markdownlint-disable-file -->
# RPI Plan: loading-briefing-hax-531-review-fixes

## Task Metadata

* Task ID: 531-review-fixes-2026-10-29
* Task slug: loading-briefing-hax-531-review-fixes
* Planning status: Ready; one critique Complete / original Revise, both findings resolved directly
* Plan date: 2026-10-29
* Phase details: .copilot-tracking/details/2026-10-29/loading-briefing-hax-531-review-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan-critique.md

## Executive Summary

Correct four reproduced review regressions without changing the product design:
repair review-dispatch test activation, retain separate citation ownership after
quoted/bracketed sentence endings and terminal name suffixes, and ensure the
native reload action renders when AsyncAction exists but has no callable handler.

### User Decisions and Requirements Highlights

* Reuse the rebased existing branch, commit the full dated RPI round locally,
  and stop without push, az, force-push or closing keywords.
* Run requested strict API/core checks, unit suites and relevant browser check;
  heavy work requires nonblocking lock admission and permits targeted fallback.

### What You May Not Know

* Existing Jr./Sr. title fixtures pass; indiscriminate period splitting breaks
  their citation ownership. Name-suffix detection remains conservative/heuristic.
* /tmp/mv tools exist, but editables point at another worktree. Setup must
  install this worktree under shared-lock ownership and use source-first paths.
* No planned source is pinned by scenario-manifest.json; verify final diff.
* Unready helper injection must use replay-safe var, not const: both initial
  and recovery requests evaluate in the same document before terminal failure.

### Unresolved Decisions or Blockers

Nonblocking heavy admission returned 75; PID 679022 owned the lock. Full unit,
browser and current-worktree editable installation were not run. Authorized
targeted fallback passes (103 correction tests, 11 manifest checks); strict
API/core checks pass. No broad/browser acceptance is claimed.

## User Decisions and Requirements

* Fix all four supplied PR #538 findings, refs #531, with regression tests.
* Pass an event with the actual Edit button as currentTarget and retry the
  submit action for the history barrier.
* Handle punctuation followed by closing quotes/brackets in citation relocation
  and statement segmentation consistently.
* Distinguish sentence-terminal Jr./Sr. from medial suffixes/titles.
* Check handler callability before wrapping listeners and exercise defined-but-
  unready helper recovery in tests/browser.
* Run mypy, ruff check . and ruff format --check . in src/api and src/core,
  source-first unit tests and relevant browser checks using /tmp/mv.
* Hold flock -n /tmp/ama-rpi-heavy.lock for full suites; if busy, run targeted
  tests and explicitly report the blocked suites.
* Preserve original evidence; commit new dated research/plan/implementation/
  review artifacts with Conventional Commit messages and the supplied trailer.

## Goals

* Prevent later citations from appearing to support an earlier uncited claim.
* Keep startup terminal recovery usable even when its helper is unusable.
* Restore the review dispatcher test's intended assertions.

## Scope and Non-Goals

### In Scope

* Named core/API source, owning tests, existing loading browser check and
  directly related API README.
* New dated correction-round artifacts and local commits.

### Non-Goals

* Redesign, parser dependency replacement, broad refactoring, cloud, publication,
  hosted/human approval, or modifying historical RPI outcomes.

## Functional Requirements

* Each quoted/bracketed sentence retains only its declared references; preserve
  exact clean punctuation/delimiters and unresolved references.
* Uncited terminal Jr./Sr. text stays uncited; medial name suffixes with lowercase
  continuations and existing Jr./Sr. titles remain a single statement.
* Defined-but-unready helper is rejected before API startup, renders terminal
  error and a keyboard-operable reload button, and does not reset retry budgets.
* Healthy helper listener wrapping and missing-helper pass-through remain intact.

## Non-Functional Requirements

* No new dependencies, exemptions, casts or typing relaxations.
* Existing human review, manual paths, native semantics and source trust caveats
  remain unchanged.
* Validation uses only constructed loopback data and current-worktree imports.

## Acceptance Criteria

* Exact supplied quoted and Jr./Sr. inputs produce two expected dictionaries
  with exact per-statement citations/unresolved lists, not merely a count.
* Closing ASCII/curly quotes and brackets, nested closers, punctuation .!? and
  whitespace/newlines are tested with citations before/after punctuation and
  an uncited first statement.
* Positive medial name suffix and negative terminal suffix fixtures both pass,
  including current title fixtures.
* Existing dispatch matrix reaches and passes all pending/newer-value/outcome
  assertions after opening Edit with its real currentTarget and retrying submit.
* Actual h()/startupFailed() unit harness renders error/reload and invokes native
  reload with AsyncAction = {} and non-callable handler; undefined and healthy
  helpers retain their behavior.
* Existing loading browser check injects a defined-but-unready helper, checks
  terminal error, no API reads, bounded requests, native keyboard reload and
  successful recovery; all checks pass or exact blockers are recorded.
* API/core mypy and Ruff checks pass; unit/browser outcomes and skips recorded.

## Implementation Context Record

| Context item | Current artifact or record |
| --- | --- |
| Plan | .copilot-tracking/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan.md |
| Phase details | .copilot-tracking/details/2026-10-29/loading-briefing-hax-531-review-fixes-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan-critique.md; Complete / original Revise; PC-001/002 resolved directly |
| Relevant research | .copilot-tracking/research/2026-10-29/loading-briefing-hax-531-review-fixes-research.md; Ready |
| Changes-record role | .copilot-tracking/changes/2026-10-29/loading-briefing-hax-531-review-fixes-changes.md; implementation-owned |
| Planning execution and readiness | Complete / Ready; summary, details and critique dispositions reconciled |
| Continuation context | Explicit bounded automatic RPI; stop after local commits |

## Sources

* Research C2-C4: exact harness/parser reproductions and existing title contracts.
* Research C5-C6/W1: shared helper readiness and current web-interface rules.
* Research C7-C8: manifest pins, component validation and shared-lock boundaries.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct parser and review harness

* Intent: restore accurate assertion execution and reference ownership.
* Dependencies: completed Research and one disposed critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Repair review harness activation

* Use selected Edit button as event.currentTarget; use submit for history retry.
* Completion: full existing dispatch matrix passes.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Normalize and segment closing delimiters consistently

* Share a punctuation-plus-closing-delimiters pattern for relocation and splitting.
* Completion: exact statement/source fixtures including nested closers pass.

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Separate terminal Jr./Sr. suffix claims

* Before shielding, detect preceding capitalized name context and uppercase
  next claim; retain lowercase continuations and existing title behavior.
* Completion: terminal/medial/title ownership fixtures pass.

<!-- rpi:phase id=P02 -->
### [x] P02: Correct and exercise helper recovery

* Intent: no secondary exception while rendering terminal recovery.
* Dependencies: critique disposed; independent of P01 implementation.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Guard listener wrapper and extend recovery coverage

* Guard callable handler before wrapping; test real renderer for absent,
  unready and healthy helpers; extend existing browser scenario; update README.
* Completion: reload renders, keyboard reload recovers, no pre-readiness API call.
* Current evidence: implementation, loader readiness and actual-renderer unit
  regressions pass; actual browser is unperformed due to busy shared lock.

<!-- rpi:phase id=P03 -->
### [x] P03: Validate and persist local correction

* Intent: retain reliable validation and independent original Review evidence.
* Dependencies: P01 and P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run targeted then admitted broad validation

* Run focused parser/harness/helper tests first, then strict checks.
* Admit full core/API and loading/briefing browser suites nonblocking; if busy,
  targeted fallback only and report unperformed full/browser suites.
* Verify pins and diff; no publication receipt or push is authorized.
* Result: user-authorized targeted fallback complete; 103 correction tests and
  11 manifest checks pass; API/core strict checks pass. Full/browser unmet:
  flock -n returned 75, owner PID 679022. No retry/poll/foreign interruption.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Commit implementation and independent Review evidence

* Configure authenticated noreply email repository-locally; local Conventional
  Commit with exact Co-authored-by trailer. Review once independently, route any
  residual work without cycling this task, commit final original evidence.
* Completion: implementation commit 2b37261be30e61cf8baf7494561def0607693e0d;
  original independent Review Complete / Residual work, no source defect found.
  Final local evidence commit retains RV-001/FU-001 and RV-002/FU-002; session
  stopped per explicit user direction. No push or subsequent source changes.

## Test Ownership and Change Budget

* Canonical targets: test_ai_statement_sources.py (parser), test_case_journey.py
  (dispatcher), test_workspace_scripts.py (real recovery DOM), and
  loading_briefing_browser_check.py (actual browser).
* Exact removals: none. Maximum additions: four core test methods, one recovery
  unit method, two browser scenario invocations; extend existing dispatch method.
* Generated targets: none; heavy output external only.
* Semantic coverage: exact citation ownership and listener/reload behavior.
* Regression coverage: exact supplied examples plus close-delimiter, suffix and
  helper-readiness counterexamples. Count-only/source-string proxies insufficient.
* Validation evidence: actual commands/exits/skips in changes record; original
  failures remain in research; exact assessed boundary in original Review.

## Dependencies

* Existing pinned dev tools and Chromium/axe for browser; /tmp/mv source editables.
* Shared lock for setup/full suites; no queue, polling or foreign interruption.

## Critique Disposition

Exactly one final-candidate independent critique executed; original verdict Revise
is preserved. No user decision needed and no repeat critique.

| Finding | Owner / disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Parent / accepted, resolved directly | P02-T01 pins idempotent var injection and exact two-request terminal/reload assertions |
| PC-002 | Parent / accepted, resolved directly | P01-T02/T03 literal supplied goldens, sources and full expected dictionaries recorded below in details |

## Follow-Up Items

* FU-001: coordinator schedules full API/core unit and loading/briefing browser
  checks, including unready-helper keyboard reload, after explicit free-lock
  coordination. Outside current admitted scope because nonblocking lock was busy.
* FU-002: owner retains publication, hosted and human acceptance gates. No push
  or complete receipt/human accessibility acceptance is established by this round.

## Handoff

* Full bounded correction round complete with authorized targeted fallback.
  Original Review Complete / Residual work; task completed, session stopped.
* Implementation artifact: .copilot-tracking/changes/2026-10-29/loading-briefing-hax-531-review-fixes-changes.md
* No unresolved user decision; broad/browser validation blocker retained.
