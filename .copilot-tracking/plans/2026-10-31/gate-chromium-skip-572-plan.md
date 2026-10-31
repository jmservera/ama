---
title: Chromium skip gate implementation plan
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: 572
* Task slug: gate-chromium-skip-572
* Planning status: Ready; one critique completed and disposed
* Plan date: 2026-10-31
* Phase details: .copilot-tracking/details/2026-10-31/gate-chromium-skip-572-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-31/gate-chromium-skip-572-plan-critique.md

## Executive Summary

Enumerate the two exact Chromium reasons, preserving the existing narrower
chat-panel discovery boundary and rejecting every required browser skip.
Add focused regressions and document the asset discovery exception.

### What You May Not Know

The merged base already requires exact chat-panel browser dispatch and receipt
evidence. The newly merged asset test can skip before Chromium installation;
allowing that known skip is not proof that it subsequently executes.
The caller prohibits the full gate, so complete issue acceptance remains unmet.

## User Decisions and Requirements

* Run Research, Plan, Implement and Review in order with dated artifacts.
* Work on fix/gate-chromium-skip-572 from origin/main 4cb5964f in this worktree.
* Recognise both exact reasons without accepting unknown skips; justify enumeration versus opt-in execution.
* Update tools/test_rpi_checks.py; do not change pinned workflows.
* Run requested unit, isolated Ruff and strict mypy checks; use flock for heavy runs.
* Use pip, no Azure/secrets/full gate/push. Commit locally with the requested trailer.
* Use Refs #572; distinguish proven contracts from unmet issue acceptance.

## Goals

* Remove the known asset discovery blocker without losing merged chat safeguards.
* Keep the fail-closed parser and receipt contracts demonstrably intact.

## Scope and Non-Goals

* Source targets: tools/rpi-checks.py, tools/test_rpi_checks.py and src/README.md.
* Evidence targets: dated research, plan/details, critique, changes, review and state.
* No workflow changes, browser test edits, full gate, external publication or issue closure.

## Functional Requirements

* Both exact reasons appear in EXPECTED_SKIP_REASONS.
* The existing chat reason remains valid only for its exact test identity in non-integration project-api discovery.
* The asset reason is recognised in general discovery, reported as a skip and never counted as execution.
* Integration mode rejects both Chromium reasons; unknown reasons and mutated reasons fail.
* Required chat dispatch and receipt checks remain unchanged.

## Non-Functional Requirements

* Surgical change using existing parser structures; no new dependency or abstraction.
* Requested workflow-aligned Ruff checks and strict mypy pass.
* No workflows or WORKFLOW_HASHES change.

## Acceptance Criteria

* Regression assertions prove exact reason membership and preserved chat scope.
* Regression assertions prove asset skip recording, integration rejection, near-miss/unknown rejection and summary-count consistency.
* Receipt validation recomputes the new asset skip and rejects tampering.
* All requested targeted validation commands pass.
* Independent critique and one independent post-implementation review are preserved.
* Local commit includes code, related documentation and original dated RPI evidence.

## Sources

* .copilot-tracking/research/2026-10-31/gate-chromium-skip-572-research.md: C1-C7; Research executed, Ready.
* Issue #572: original broader acceptance criteria, not all authorised here.
* .github/workflows/src-ci.yml: pinned strict validation commands.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement the bounded recognition contract

* Intent: remove known skip blocker and preserve all existing fail-closed boundaries.
* Dependencies: completed research and final-candidate critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Enumerate exact reasons and preserve chat scope

* Add both exact reasons; keep integration rejection and explicit scoped chat identity validation.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Regress parser and receipt boundaries; update guide

* Modify existing chat membership assertion without removing its negative cases.
* Add asset parser and receipt tests; document known discovery-only acceptance.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and hand off for independent review

* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run requested checks and reconcile evidence

* Unit discovery, isolated Ruff check/format and strict mypy, under the shared lock.
* Record results and unperformed full gate/browser/MSSQL evidence.

## Test Ownership and Change Budget

* Canonical test owner: tools/test_rpi_checks.py; semantic browser behavior stays in existing API suites.
* Exact removals: none.
* Maximum additions: two test methods (asset parser and asset receipt), plus parameter rows.
* Generated targets: none.
* Regression coverage: exact output/counts, unknown/near-match skips, integration refusal, receipt recomputation.
* Semantic evidence: existing dispatch contract tests only; no actual Chromium or MSSQL run claimed.

## Dependencies

* Python and existing test dependencies; restore only after missing-dependency failures, using pip.
* Shared lock /tmp/ama-rpi-heavy.lock for heavy validation.

## Critique Disposition

| Finding | Disposition | Evidence and rationale |
| --- | --- | --- |
| PC-001, original verdict Revise | Rejected as conflicting with confirmed caller direction | Caller explicitly requires flock -w 600 /tmp/ama-rpi-heavy.lock. Parent execution context does not prohibit /tmp or external session logs. The critique's extra worker-local constraints do not apply to parent validation. Keep the prescribed shared lock; no private substitute, source change or repeated critique. |

The original critique remains unchanged. Its source-contract assessment supports
the candidate; no unresolved implementation finding remains after disposition.

## Follow-Up Items

* Required asset browser execution evidence is outside the bounded recognition fix; review before publication.
* Fresh complete exact-head gate including browser and MSSQL, receipt verification and human/hosted approval remain required before publication.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-31/gate-chromium-skip-572-changes.md
* Implementation P01 and P02 complete; requested checks passed (37 unit tests).
* Next action: one independent Review of the bounded source and evidence.
* No publication permitted; full gate and actual browser/MSSQL evidence are not claimed.
