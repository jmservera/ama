---
title: PR 507 current-main synchronization plan
ms.date: 2026-10-30
---

## Task Metadata

Task ID: pr-507-sync-2026-10-30. Slug: rubric-src-198-sync.
Branch: feat/rubric-src-198. Refs #198.

## Executive Summary

Rebase the five local topic commits onto current main, retaining independent
documentation histories and using main's entire rubric and scenario manifest.
Focused application/static and migration checks passed. The unchanged-main
rubric regression suite retains eighteen failures and seven runtime skips.
All outcomes are recorded; obtain one independent Review and commit locally
without pushing. Implementation is complete, not whole-CI acceptance.

### What You May Not Know

The original rubric fixes were removed during earlier integrations. Main's
rubric tests previously had eighteen failures; those inputs must not be changed
to manufacture a green result. Hosted CI and remote mergeability remain
coordinator-owned after the local commit.

## Sources

Research: .copilot-tracking/research/2026-10-30/rubric-src-198-sync-research.md.
Details: .copilot-tracking/details/2026-10-30/rubric-src-198-sync-phase-details.md.
Starting head: 6517adf10c692cdfd1f1abad8431d7e6e4e43cca.
Fetched main: 91e890e07af036263316c153cbc7ceff780cdaa2.
Final integrated main: ffd8f35e63b24905b9aeb937dbf2a7fe9968747f.
Main moved during validation by two training-material dev dependency commits;
same authorized rebase/preservation policy applied before the single Review.

## User Decisions and Requirements

* Execute the full dated RPI loop for draft PR #507 and Refs #198.
* Fetch and rebase origin/main; preserve both sides' documentation intent.
* Take main's rubric and scenario manifest; validate changed source pins.
* Sources belong in src only; tests stay outside packages; no legacy code.
* Use /tmp/mv for Ruff, format, applicable core/API mypy and relevant unittests
  with current project/sibling source and test paths.
* No full API discovery without successful nonblocking shared-lock admission.
* No Azure resource changes or push. Commit conventionally with required trailer.
* Record commands and actual results in the changes artifact.

## Goals

Produce a conflict-free locally committed descendant of current main with
truthful validation evidence and no unrelated executable changes.

## Scope and Non-Goals

Scope: rebase, documentation reconciliation, dated RPI artifacts and local checks.
Non-goals: changing inherited rubric inputs, scoring, deployment, historical
issue acceptance, human approval, full API suite, remote publication or merge.

## Functional Requirements

* Preserve main's log as an exact prefix and the complete original branch tail.
* Retain independent index entries and existing cut-over reconciliation.
* Preserve all original dated tracking artifacts byte-for-byte.
* Exact main equality for rubric, scenario manifest, source, workflows and infra.

## Non-Functional Requirements

No private dataset reads, dependency/environment mutations without actual missing
requirements, Azure actions or fabricated successful checks. Use privacy-safe
authenticated author/committer identity. No closing keywords.

## Acceptance Criteria

* Main is an ancestor, rebase finished, no conflict markers or whitespace errors.
* Preservation and authoritative-input assertions pass.
* Requested static and relevant unit checks pass, or failures remain explicit
  acceptance blockers; full rubric outcome recorded without claiming CI green.
* One critique and one independent Review retained with findings dispositions.
* Required local commit exists with correct identity/trailer and clean worktree.
* Coordinator owns push, fresh hosted CI, remote mergeability and publication gate.

## Test Ownership and Change Budget

Existing core manifest/dependency tests, API dependency tests and rubric pytest
suite own regression coverage. Migration tests cover retained layout guidance.
Test removals: none. Maximum added tests: zero. No canonical/generated production
targets change; rubric/manifest bytes are upstream-owned. Semantic validation is
history/content preservation, not a proxy of test counts.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Integrate main

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Rebase and reconcile actual conflicts

Combine independent index/log entries, preserve dated history and enforce
main-owned rubric/manifest after replay. Update current synchronization
qualification, index date and append-only log without rewriting older outcomes.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Prove preservation and layout invariants

Check ancestry, main log prefix, original topic log tail, all old artifact
bytes, independent index content and zero executable/infra/workflow delta.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and reconcile evidence

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run applicable local checks

Core/API Ruff lint, format, mypy; core manifest/dependency and API dependency
units; migration regression and existing system-pytest rubric suite. Probe
actual local namespace paths. No full API run or heavy gate is required for
this documentation-only synchronization; do not acquire a lock unnecessarily.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Record results and prepare one Review

Complete markers/details/changes and freeze the reviewed non-tracking delta.
Original Review findings remain historical. Independent Review writes only
its artifact; new findings route to follow-up, not a repeat Review.
After Review, finalize lifecycle evidence and commit all task-owned changes.

## Critique Disposition

One final-candidate independent critique executed Complete / Pass, no findings:
.copilot-tracking/reviews/plans/2026-10-30/rubric-src-198-sync-plan-critique.md.
No repeat critique or unresolved disposition.

## Follow-Up Items

* Coordinator: publish only after applicable gate/independent exact-head and hosted
  requirements; no push is authorized here.
* Rubric owner: inherited failing tests/runtime prerequisites, if reproduced.
* Owner: original #198 historical score/sequencing acceptance gaps.

## Handoff

Implementation complete, critique passed, one Review ready. Requested focused
checks passed; inherited rubric/runtime blockers remain unmet acceptance, not
unfinished implementation. Parent local commit and coordinator publication
are later lifecycle actions. Changes record:
.copilot-tracking/changes/2026-10-30/rubric-src-198-sync-changes.md.
