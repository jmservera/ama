---
title: Employee acceptance browser gate plan for 570
description: Mandatory post-install command and receipt regression coverage
ms.date: 2026-10-31
---

## Task Metadata

Task ID: 570-employee-acceptance-gate. Slug: employee-acceptance-gate-570.
Date: 2026-10-31. Planning status: Ready; independent critique Complete/Pass.
Details: .copilot-tracking/details/2026-10-31/employee-acceptance-gate-570-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-31/employee-acceptance-gate-570-plan-critique.md.

## Executive Summary

Require the pinned CI employee acceptance CLI after Chromium installation in
both local dispatch and receipt verification, independently of extra selectors.
Require three reported tests and zero skips without weakening existing
discovery or SQL contracts. Add focused tooling regressions and update the
source gate guide and knowledge-base routing.
Publication evidence is separate from synthetic behavior and live acceptance.

## User Decisions and Requirements

* Continue issue #570, branch fix/employee-identity-check-570, open PR #601.
* Address only unresolved thread PRRT_kwDOUU8JX86yRJOA.
* Pull branch first, merge main, prefer main rubric score on conflict.
* Run the four RPI phases with dated artifacts and the requested tools suite.
* Owner requests CI as gate, no full-gate wait, pip only and no secrets.
* Commit with supplied Copilot trailer, non-force push, reply and resolve thread.

## Goals

* Close the default full-receipt browser coverage hole.
* Preserve qualification of early discovery skips without counting them as execution.

## Scope and Non-Goals

Runtime/receipt runner, its owning tests, directly related gate documentation,
knowledge-base index/log and dated evidence only. No workflow/pin changes,
receipt schema redesign, UI changes, live verification or historical rewrites.

## Functional Requirements

* Unconditional browser CLI immediately after Chromium installation, API cwd,
  exact pinned workflow PYTHONPATH, suite=True and integration=True.
* Trusted matrix requires the identical command, cwd, env and flags.
* Runtime and receipt parsing bound the CLI to three reported tests, zero skips.

## Non-Functional Requirements

* Reuse the existing suite parser with optional expected_count; default unchanged.
* Preserve exact chat-panel evidence and SQL non-applicability behavior.
* No dependencies added. Existing Ruff/format/mypy rules retained.

## Acceptance Criteria

* Default extras=[] browser/full matrix requires exactly one employee CLI.
* Dispatch matches matrix and follows Chromium installation.
* Valid three-test evidence verifies; missing command, paths, flags, nonzero exit,
  zero/wrong counts, discovery skips and SQL-only skip exception cannot verify.
* Requested unittest discovery passes; owning focused lint/types pass.
* Independent critique and post-implementation Review recorded once.

## Sources

Research: .copilot-tracking/research/2026-10-31/employee-acceptance-gate-570-research.md,
C1-C6 and W1, Complete/Ready. No research gap.

## Test Ownership and Targets

Owning file: tools/test_rpi_checks.py. Exact removals: none. Maximum additions:
three test methods, with subtests for negative cases. Update both existing
scoped/full success fixture builders for three-test CLI evidence.
Semantic coverage remains in the maintained API CLI; new regressions prove
orchestration, skip/count enforcement and receipt command identity.
Canonical source targets: tools/rpi-checks.py and tools/test_rpi_checks.py.
Generated targets: none. Preserve latest.json unless merge conflict requires main.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Mandatory browser contract

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Wire runtime and trusted receipt matrix

Share CLI module and pinned import-path constants. Extend check_skips with
optional expected_count used for employee acceptance runtime/verification.
Depends on research C1-C4.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add regression evidence and direct documentation

Add dispatch, adverse receipt and runtime count/skip tests; update fixture
counts and gate documentation/index/log. Depends on P01-T01.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and prepare Review

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run focused validation and prepare independent Review

Run python3 -m unittest discover -s tools -p 'test_rpi_checks.py' -q,
focused Ruff/format/mypy and git diff review. Reconcile markers and changes,
then independent Review. Depends on P01.
Implementation validation complete: 42 tests pass; owning Ruff/format/mypy pass;
new dispatch regression rejects the original gate. Independent Review is the
next lifecycle phase, not falsely claimed executed by this checked marker.

## Dependencies

Existing API editable packages and installed Chromium are requirements of
actual browser execution; fixture tests need neither. No new install planned.
Repository publication policy requires complete clean committed local evidence
before publication; owner requests no wait. Do not silently substitute CI
for a mandatory higher-priority publication requirement.

## Critique Disposition

One independent final-candidate critique executed Complete/Pass, zero findings.
Artifact: .copilot-tracking/reviews/plans/2026-10-31/employee-acceptance-gate-570-plan-critique.md.
No corrections, unresolved decisions or repeated critique.

## Follow-Up Items

* Independent private expected-ID attestation and live #570 acceptance remain
  outside tooling scope; retained from parent evidence.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-31/employee-acceptance-gate-570-changes.md.
Implementation scope complete and ready for one independent post-implementation
Review. Original critique Complete/Pass. No implementation decision gap.
