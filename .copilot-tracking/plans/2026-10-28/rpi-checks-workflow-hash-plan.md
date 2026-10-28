---
title: Local gate workflow pin correction plan
description: Brief implementation and validation plan for a reviewed pin refresh
ms.date: 2026-10-28
---

Task: rpi-checks-workflow-hash. Status: implementation-ready.

## Executive Summary

Refresh only src-deploy.yml's raw-byte hash, accepting the already-merged
#500 release safeguards. Extend the existing pin test, preserving the
fail-closed policy. No workflow changes or new testing infrastructure.
Research is Complete / Ready; no unresolved design choices.

## User Decisions and Requirements

* Check every WORKFLOWS entry, not just the reported deployment workflow.
* Keep light, dated research/plan/changes/review artifacts.
* Extend an existing pin test only; run the runner suite and real preflight
  if available.
* Do not modify workflows, access .env or push main. Commit with the
  requested Copilot trailer, push the topic and open a PR using Refs.

## Goals

Restore preflight without weakening workflow drift detection.

## Scope and Non-Goals

Canonical targets: tools/rpi-checks.py and tools/test_rpi_checks.py.
Evidence: dated tracking artifacts. Generated targets: none.
No dependency, workflow, application, deployment or private-data changes.

## Functional Requirements

Explicitly pin deployment SHA256
3c2f1ed59b1486fc1316a48207cc4ef7d6a830bbba1dcad4152acab4bd2f1bbc.
Keep all four matching pins unchanged. Retain all five fail-closed checks.

## Non-Functional Requirements

Reuse hashlib/read_bytes behavior and unittest conventions; no new helpers
or CLI flags. Preserve original failures and independent-review outcomes.
Standing repository instructions require the complete clean-commit --all
gate and receipt verification before publication, despite the README's
documented lighter tier. A failed gate blocks push, not an excuse to bypass it.

## Acceptance Criteria

All five actual pins equal digest(file), a matched fixture preflight passes,
and mutating each fixture workflow fails with its exact name. Existing runner
tests pass. Real Runner.preflight runs tools/version checks and all pins;
there is no preflight-only CLI flag. Workflow diff remains empty.

## Phase Checklist

<!-- P01 -->
### P01: Correct and validate

* [x] P01-T01: Extend test_matrix_drift_and_unreviewed_extra_commands_refuse
  and show the stale real pin fails before correcting it.
* [x] P01-T02: Refresh the single drifted hash; run all tooling tests and
  real preflight. Run existing Ruff/mypy if available.

<!-- P02 -->
### P02: Review and publication

* [x] P02-T01: Execute one independent post-implementation Review and
  preserve its exact assessed boundary/outcome.
* [ ] P02-T02: Commit source and dated evidence with authenticated
  privacy-safe identity and trailer; execute the complete local gate in a
  new external directory. Fetch main, verify receipt against current
  origin/main, obtain independent exact-head assessment, then push topic
  and create a main-target PR using Refs #500. No publication on failure.

## Test Ownership

tools/test_rpi_checks.py owns the orchestration/pin contract. Exact removals:
none. Maximum additions: extend one existing test method, zero new test files
or methods. Semantic coverage: each fixture mismatch still blocks.
Regression coverage: actual repository bytes match all declared pins.
Evidence: baseline 30 passing tests; red/green extension, real preflight and
existing lint/types; full external gate required for publication.

## Critique Disposition

One independent final-candidate critique executed: Pass, no findings.
Original: .copilot-tracking/reviews/plans/2026-10-28/rpi-checks-workflow-hash-plan-critique.md.
No dispositions or user decisions remain open; critique is not repeated.

## Follow-Up Items

None supported by current evidence.

## Sources and Handoff

Research: .copilot-tracking/research/2026-10-28/rpi-checks-workflow-hash-research.md.
Details: .copilot-tracking/details/2026-10-28/rpi-checks-workflow-hash-phase-details.md.
Changes destination: .copilot-tracking/changes/2026-10-28/rpi-checks-workflow-hash-changes.md.
P01 and P02-T01 complete. Original Review: Complete / Conformant, no findings,
against source diff at 98b0bb98; not publication approval. P02-T02 remains
publication work after Review, not incomplete source implementation.
Before first commit, topic fast-forwarded to b6755bb5 (unrelated merged
documentation #459); tooling and workflow bytes are unchanged by that update.
The committed state is a pre-publication snapshot; external exact-commit
gate/assessment and the PR record the subsequent publication outcome.
