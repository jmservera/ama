---
title: Capacity delayed sibling 401 plan
description: Scoped lifecycle repair and regression for issue 523
ms.date: 2026-10-28
---

Task ID: 523-delayed-401. Slug: capacity-page-523-delayed-401.

## Executive Summary

Guard the successful capacity read boundary against aborted routes and ended
sessions. Extend the existing real-mutation browser scenario with deterministically
held sibling and retry reads. Prove red without the guard, then green with it.
Run focused units/static checks and one independent Review before normal push
and tested-thread resolution. The complete gate is blocked, not attempted,
because az is prohibited. Existing historical gates do not cover this candidate.

## Sources

Research: .copilot-tracking/research/2026-10-28/capacity-page-523-delayed-401-research.md
(C1-C4). Details:
.copilot-tracking/details/2026-10-28/capacity-page-523-delayed-401-phase-details.md.

## User Decisions and Requirements

* Continue fix/capacity-page-523 and PR #528; retain the bot rubric commit.
* Smallest correct fix in ops.js plus regression in capacity_browser_check.py.
* Demonstrate browser failure without the fix, then passing corrected behavior.
* Nonblocking heavy-lock admission, retry every 60 seconds for up to 40 minutes.
* Relevant units, Node syntax, strict Ruff/format at 100 and API mypy required.
* Commit with Conventional Commit, privacy-safe identity and Copilot trailer;
  normal push only, Refs #523 in PR, then reply/GraphQL resolve the thread.
* No az, full-gate attempt, merge, deployment, secrets, .env or private data.

## Goals

Sign-in remains authoritative when an old sibling expires the session while a
new capacity retry is pending. Preserve normal recovery, drafts and navigation.

## Scope and Non-Goals

Production: two-line guard after Promise.all in ops.js. Regression: existing
capacity browser check only. Direct documentation: API README.
No global auth change, new test framework, redesign, data migration or cloud use.

## Functional Requirements

Check captured abort state and current session after both reads succeed and
before constructing/rendering capacity content. Regression uses a real saved
mutation, failed refresh, pending older sibling, retry, delayed 401 and then
successful retry responses. Assert sign-in stays visible/focused and mutation
is persisted once, not replayed.

## Non-Functional Requirements

Deterministic request interception and explicit browser completion barriers,
not fixed sleeps. Real local owned SQL-backed fixture, no private inputs.
No test removals; preserve unexpected-error detection and other scenarios.

## Acceptance Criteria

* Both packages-first and workorders-first failure orderings reproduce stale
  rendering without the fix and preserve sign-in with it.
* Existing seeded/empty, manager navigation, draft, failure/retry, cancellation
  and expiry checks still pass on owned SQL Server/Chromium.
* Focused units, JS syntax, strict Ruff/format 100 and mypy pass.
* Exactly one critique and one post-implementation Review are recorded.
* Pushed SHA and thread action reported; no full-gate/live acceptance claim.

## Test Ownership and Locked Boundary

Canonical regression owner: src/api/checks/capacity_browser_check.py.
Generated targets: none. Removals: none. Maximum additions: one parameterized
two-endpoint scenario block and one local typed interception callback,
no new test file or production helper.
Semantic coverage: post-read abort/session guard. Regression coverage:
delayed-sibling-401 interleaving and once-only real mutation.
Browser assertions must wait for retry continuation completion, not merely
network response headers; compare persisted configuration count and POST count.

## Phase Checklist

<!-- P01 -->
### P01: Implement and verify

* [x] P01-T01 Add parameterized regression and demonstrate failure without guard.
* [x] P01-T02 Add guard, update README, run full capacity browser green and focused checks.

P01 complete: both genuine red runs and complete owned SQL/browser green,
82 focused units and final Node/Ruff/format/mypy/whitespace checks passed.

<!-- P02 -->
### P02: Review and publication

* [x] P02-T01 Reconcile evidence; run one independent original Review.
* [ ] P02-T02 Commit, normal push, reply and resolve the exact tested thread.

Dependencies: P01-T02 follows P01-T01; P02-T01 follows P01; P02-T02 follows
Review and passing scoped validation. Full gate remains explicitly blocked.

## Critique Disposition

Exactly one independent critique completed, original verdict Revise, preserved at
.copilot-tracking/reviews/plans/2026-10-28/capacity-page-523-delayed-401-plan-critique.md.

* PC-001 applied: retain the exact retry button ElementHandle, observe busy,
  release responses after sign-in, wait for that detached button's finally
  busy-to-settled transition before final assertions.
* PC-002 rejected: its claimed prohibition on temporary paths is not present
  in the parent execution instructions. The owner explicitly requires the
  /tmp/ama-rpi-heavy.lock path. Preserve that exact shared lock and existing
  installed interpreter/owned temporary fixture; do not substitute another lock.
* PC-003 applied: both red orderings mandatory, using separately recorded
  unguarded runs with opposite iteration order if the first assertion fails fast.

Planning readiness Ready. No significant/divergent unresolved user decision.

## Follow-Up Items

Owner live verification and full local gate remain unavailable in this run.
Prior RV-004/005/006 remain separately scoped, unchanged historical findings.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-28/capacity-page-523-delayed-401-changes.md.
One original independent Review Complete; scoped source/regression Conformant,
full task Residual work. Low RV-001 is routed parent evidence bookkeeping,
clarified in the changes handoff without regrading or repeating Review.
P02-T02 remains the post-commit operational publication step in this committed
snapshot; final receipt will be external session files/capacity-401-publication.json.
No child work selected. Full gate blocked and live owner acceptance pending.
