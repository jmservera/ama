---
title: Issue 349 preflight correction2 plan
description: Implementation plan for malformed response collection handling
ms.date: 2026-10-22
---

Task ID: 349. Slug: issue349-tenant-readiness-preflight-correction2.
Status: P01 complete; one P02 Review complete with Residual work. Publication pending.

## Executive Summary

Validate non-null response collections as lists before iterating. Malformed
fields produce sanitized unknown/malformed-response checks and blocked exit 1.
Keep absent/null behavior and valid-list behavior unchanged. Use one focused
offline regression matrix; no live operations or acceptance claims.

## User Decisions and Requirements

* Complete research, plan, implement and review in order with distinct dated artifacts.
* Correct all three supplied readers; preserve absent-field behavior and sanitize output.
* Retain the original NEEDS CHANGES review; no live tenant/resource operations.
* Keep issue #349 open, unmet criteria unticked and any PR draft without closing keywords.
* Commit only correction/evidence with privacy-safe identity and required trailer.
* Run exactly one full gate against b4d467cad84535ed106cffa1ae9aa303db7bfed2,
  wait on the shared lock, verify the new receipt/head/current base, then push normally.
* Leave independent final PR review and merge authority to the coordinator/owner.

## Sources

Research: .copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-correction2-research.md
(C1-C8). Original candidate: 4753af1edf74db7f5cf0ec1025b69d22f72f18f5.
Details: .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-correction2-phase-details.md.

## Goals

Remove malformed-shape crashes and false-ready iterable behavior at the three readers.

## Scope and Non-Goals

Only infra/scripts/tenant-readiness-preflight.py, its focused test module and
correction2 RPI artifacts. No schema-wide rewrite, live lookups, resource changes,
private datasets, acceptance, issue checkbox changes or unrelated cleanup.

## Functional Requirements

* Non-null values other than lists, including falsey values, produce unknown/malformed-response.
* Missing/null collections retain existing mismatch or absent outcomes.
* Malformed checks expose no raw values or derived counts.
* Callback target failure retains existing blocked-by-callback-target precedence.

## Non-Functional Requirements

Use local shape guards without broad exception catches or coercion; retain fixed
read-only command guard, existing list-member filtering and report schema.

## Acceptance Criteria

* All three fields reject integer, boolean, string and object JSON shapes.
* CLI JSON and text return blocked/exit 1 without stderr traceback or sentinels.
* Null/missing/empty lists and valid lists preserve prior status/reason/facts.
* Focused tests, isolated Ruff/format and strict script mypy pass.
* One post-implementation Review records its real outcome; no repeat Review.
* Publication requires a fresh complete passing gate and exact-head/current-base receipt.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Shape guards and regression evidence

* [x] P01-T01: Add test matrix, observe failure, then implement three guards.
* [x] P01-T02: Run focused suite, Ruff/format and strict script mypy; record changes.

<!-- rpi:phase id=P02 -->
### [ ] P02: Review and exact-head publication

* [x] P02-T01: Execute one RPI Review; reconcile all evidence and remaining gates.
* [ ] P02-T02: Resolve gh identity, commit correction/evidence, run one full gate,
  fetch/verify receipt, push normally and create a draft non-closing PR.

## Locked Test Ownership and Boundaries

Owner: infra/tests/test_tenant_readiness_preflight.py. Exact removals: none.
Maximum additions: three test methods, with subtests for the three fields and
JSON types/output modes. Canonical targets: the script and that test module.
Generated targets: none. Semantic coverage: fixed malformed result, blocked exit
and redaction. Regression coverage: null/missing/empty and valid-list behavior,
callback dependency precedence. Existing 29 tests remain intact.
Evidence: focused unittest, isolated Ruff with E,F,I,B,UP / py312 / line length
100, Ruff format, strict mypy on script; full local gate after committed Review.
Keep all caches and receipts external.

## Critique Disposition

Execution: completed once. Original verdict: Revise (two High findings).
Artifact: .copilot-tracking/reviews/plans/2026-10-22/issue349-tenant-readiness-preflight-correction2-plan-critique.md.

* PC-001 rejected as inapplicable to the parent execution context: the critique
  assumes a temporary-directory prohibition that is not present here. The caller
  explicitly requires the unchanged /tmp/ama-rpi-heavy.lock. External scratch is
  permitted and already used for the missing-tool environment. Do not relocate
  the lock, modify the runner or invent a publication blocker from worker-local
  constraints. Preserve the original critique unedited.
* PC-002 accepted and applied directly: add an explicit second fetch after the
  gate and before exact-head receipt verification/push. Stop publication if the
  base moved; do not rebase or launch a second gate.

No unresolved significant decision; no repeat critique.

## Follow-Up Items

Independent exact-head PR assessment and all live/human #349 criteria remain
coordinator/authorized-owner work, not satisfied by this correction.

## Handoff

The research/plan/implement/review sequence is complete. Proceed only with the
authorized P02-T02 publication gates; no new implementation or repeated Review.
Committed evidence necessarily predates the exact-head gate. Final gate/receipt
and publication results remain external so no later commit invalidates the gate.
