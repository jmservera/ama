---
title: Source monitor retry implementation plan
description: Bounded implementation and delivery plan for issue 332
ms.date: 2026-10-16
---

## Task Metadata

Task: #332. Slug: source-monitor-retry-332. Full plan scope.

## Executive Summary

Measure source cadence from the last successful observation so a due source
remains eligible after retrieval failure. Preserve append-only failure evidence,
source isolation and latest-attempt clock protection.

### What You May Not Know

The existing job test encodes the faulty skip behavior. Success here means
retrieval, not verified law or permission to approve or activate a rule.

## Sources

* GitHub issue #332 and its comments (none at intake).
* .copilot-tracking/research/2026-10-16/source-monitor-retry-332-research.md
* docs/adrs/0006-src-layout-and-cutover.md

## User Decisions and Requirements

* Fix due() using successful observations or bounded retries; choose success-based cadence.
* Add failure-then-next-day coverage and prove it rejects the original implementation.
* Code only in src/, tests outside packages; portable SQL only.
* Use local pip venv unit suites, Ruff and mypy; no uv, Docker or Azure.
* Never read properwarm.json or touch .env, .vscode or .copilot-tracking/github-issues.
* Update relevant READMEs, append docs/reference/log.md, produce RPI evidence,
  commit with the requested identity/trailer, push and open a PR using Refs #332.

## Goals

Prevent failed attempts from postponing eligible retrievals.

## Scope and Non-Goals

Change core scheduling and core/orchestrator regression tests, their READMEs
and the reference log. No schema, network, infrastructure or approval changes.

## Functional Requirements

* No successful observation means due, including after repeated failures.
* A successful observation sets the per-source cadence; later failures do not.
* Reject a clock before the latest attempt, including a failed attempt.
* After a successful retry, resume normal skips and exact due boundaries.

## Non-Functional Requirements

Use existing adapter SQL and Python JSON decoding, with no SQL dialect additions.
Preserve locks, append-only evidence and observation/approval semantics.

## Acceptance Criteria

* Core tests cover 30/366-day intervals, no success, prior success, failures,
  successful recovery, exact boundaries and failed-attempt clock protection.
* The offline job actually checks a next-day retry and then skips after success.
* Original due() fails the new core and job tests; restored implementation passes.
* Component unit suites, Ruff check/format and mypy pass in a pip venv.
* Branch pushed and PR opened without merging or issue disposition.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement and validate

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Fix cadence, regressions and directly related documentation

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Run unit, static and mutation checks

<!-- rpi:phase id=P02 -->
### [ ] P02: Review and publish

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Record one implementation Review and reconcile evidence

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Commit, push and open PR

## Test Ownership and Critique Boundary

Core owns due() semantics; orchestrator owns job routing and reports.
Remove no tests. Add at most three core tests and one job test, updating the
existing failure expectation. No generated targets. Semantic tests cover
success/failure/clock behavior; mutation checks replace only due() in memory.
Run full core and orchestrator suites plus each component's static checks.

## Critique Disposition

One final-candidate critique executed: Revise, one Medium PC-001.
Applied for pip builds and monitor tests: configure TMPDIR under src/.
Implementation evidence showed 12 unrelated generator tests deliberately
require output outside any repository. Those tests must use system temporary
storage; no build or application source moves outside src/. This narrow
disposition preserves repository guards instead of bypassing them. No change
to acceptance, test ownership or maximum additions.

## Follow-Up Items

* None.

## Handoff

Implementation and validation complete; one Review executed, outcome
Conformant with justified divergence (generator scratch placement). Core: 466 run,
one opt-in skip. Orchestrator: 22 passed. Both components' Ruff check/format
and mypy passed. Mutation rejects the original due() in all four selected
test methods (five assertion failures including 30/366-day subtests).
P02-T02 publication remains under the explicit user delivery request.
