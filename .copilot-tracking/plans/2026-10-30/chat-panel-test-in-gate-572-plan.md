---
title: Chat panel gate implementation plan
ms.date: 2026-10-30
---

Task: #572, `chat-panel-test-in-gate-572`.
Status: implementation-ready; one critique completed and disposition recorded.

## Executive Summary

Add the existing exact chat-panel case to the required local Chromium stage,
with its opt-in flag and verified unittest evidence. Permit its exact discovery
ID/reason only in API general discovery, never in integration execution.
Keep runtime/UI, hosted workflows and broad skip allowlist unchanged.
Implementation and lightweight regressions/API static checks now pass.
Heavy validation admission timed out after 600 seconds; real Chromium, API
discovery and complete-gate acceptance remain unproven.

## Sources

Research: `.copilot-tracking/research/2026-10-30/chat-panel-test-in-gate-572-research.md`.
Details: `.copilot-tracking/details/2026-10-30/chat-panel-test-in-gate-572-phase-details.md`.

## User Decisions and Requirements

* Execute full Research, Plan, Implement, Review; dated original evidence.
* Deliver issue #572 exactly on caller branch/base; local commit, no push.
* Use pip, no uv/cloud/deployment/live sign-in/credential files/secrets.
* Hold heavy lock for heavy checks; run requested API unit/Ruff/mypy checks.
* Commit with required co-author and `Refs #572` only.
* Prove criteria individually; fresh complete exact-head receipt includes real
  Chromium and MSSQL, not a reused receipt.

## Goals

Unblock API discovery without hiding skips and make Chromium coverage required.

## Scope and Non-Goals

Change existing gate tooling/tests and directly related component documentation.
No runtime, UI, workflow/check-name, deployment, score or protection changes.

## Functional Requirements

* Required command inventory and runtime browser runner agree on exact
  `test_chat_panel.PanelTests.test_browser_warning_failure_keyboard_refusal_and_live_log`.
* Command includes `ZF_BROWSER_TESTS=1`, own/shared fixture paths, verbose
  unittest output, suite accounting and `integration=True`.
* Exact discovery ID/reason permitted only for `project-api` non-integration
  suite accounting; original skip retained in receipt.
* Receipt verification recomputes the same context and rejects missing,
  changed, failed, skipped or zero-execution browser commands.

## Non-Functional Requirements

Preserve fail-closed semantics, immutable adverse evidence, clean input
identity and external receipts. No new dependencies or harness abstractions.

## Acceptance Criteria

* AC1: exact case owned by local browser stage and command/coverage inventory,
  opt-in flag and real execution evidence.
* AC2: unexpected integration/dependency skips remain rejected; no broad
  allowlist expansion, disabling test or skip token.
* AC3: regressions prove required-stage execution and unexpected skip rejection.
* AC4: fresh complete exact-head gate and verification, browser and MSSQL
  included, before coordinator publication.

## Phase Checklist

<!-- phase: P01 -->
### P01: Integrate exact execution and accounting

* [x] P01-T01: narrow ID/reason discovery exception and verification context.
* [x] P01-T02: matching browser manifest and runtime command.
* [x] P01-T03: existing test-owner regressions and component docs.

<!-- phase: P02 -->
### P02: Validate, review, commit and exact-head gate

* [ ] P02-T01: targeted gate regressions, real exact case, API units/lint/types.
* [x] P02-T02: one independent post-implementation Review; preserve findings.
* [ ] P02-T03: local commit with dated evidence; full exact-head gate under lock
  and verify fresh receipt against current fetched origin/main.

## Test Ownership and Locked Budget

Canonical owners: `tools/test_rpi_checks.py` for gate contracts;
`src/api/tests/test_chat_panel.py` for unchanged semantic browser behavior.
Exact removals: none. Maximum additions: four gate regression methods;
no new test files or product tests. Update existing suite-count fixture.
Generated targets: external logs/receipt only, no committed receipt bundle.
Coverage: command/env identity and runtime-dispatch regression; strict skip
rejection; receipt mutation rejection; actual existing semantic browser case.
Validation: requested API command/Ruff/mypy plus full exact-head gate.

## Critique Disposition

Single critique executed, original verdict Revise preserved at
`.copilot-tracking/reviews/plans/2026-10-30/chat-panel-test-in-gate-572-plan-critique.md`.
PC-001 rejected: it assumes a no-`/tmp` restriction that does not apply to the
parent execution context and conflicts with the caller's explicit shared-lock
requirement. Parent already executed fixture tests and probed `/tmp/mv`
successfully. No safety exception or lock bypass is needed or authorized.
The conditional concern is valid in a restricted worker, not a parent blocker.
No other findings; no repeated critique.

## Follow-Up Items

Shared-lock contention blocks P02-T01 and the complete-gate portion of
P02-T03. Coordinator must provide a free heavy-validation slot for actual
Chromium/API units and complete exact-head gate, retaining fresh external
receipt and verification. Required human/hosted approval and coordinator
publication remain external to implementation acceptance.
The single Review is Complete / Residual work: RV-001 (Medium) routes actual
focused execution; RV-002 (High) routes committed exact-head full-gate evidence.
No demonstrated implementation defect. Original Review remains unchanged.

## Handoff

P01 implemented; original post-implementation Review completed with Residual
work. P02-T01 and P02-T03 remain incomplete until actual heavy validation
succeeds. Commit this candidate locally with original evidence, then attempt
nonqueued complete-gate admission using the runner's shared lock. If busy,
retain external admission failure and return the validation blocker to the
coordinator; do not launch another waiting gate or bypass serialization.
Changes record:
`.copilot-tracking/changes/2026-10-30/chat-panel-test-in-gate-572-changes.md`.
