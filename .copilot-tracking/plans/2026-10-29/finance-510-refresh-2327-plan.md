---
title: Finance PR 510 main refresh plan
description: Local rebase and focused CI validation plan
ms.date: 2026-10-29
---

Task ID / slug: `finance-510-refresh-2327`.

## Executive Summary

Retain remote branch ancestry, rebase finance onto current main, preserve both
documentation contributions and use main-authoritative generated policy inputs.
Run focused core/API checks, independently review once, commit local evidence,
then attempt the complete local gate. No push or operational approval.

## User Decisions and Requirements

* Full dated RPI loop for PR #510 / branch `docs/finance-96`, Refs #96.
* Fetch and rebase main; preserve both sides, especially index and append-only log.
* Main owns `.github/rubric/*` and scenario manifest; rerun manifest regression.
* Source only in `src/`; tests outside packages; no legacy application code.
* Use `/tmp/mv`, project/sibling source and test paths, Ruff and mypy.
* Full API suite only with nonblocking heavy-lock admission.
* No Azure actions, no push, no issue-closing keywords.
* Conventional Commit with required Copilot coauthor; record commands/results.

## Goals

Make current main an ancestor while retaining finance behavior and review history.

## Scope and Non-Goals

Conflict resolution, focused validation, RPI evidence and local commits only.
No new finance features, altered approval status, deployment or remote mutation.

## Functional Requirements

Preserve original finance/source changes, main integration and both log/index
entries. Main rubric/manifest copies must be byte-identical.

## Non-Functional Requirements

No shared venv mutation unless a missing dependency is demonstrated. Assert local
module provenance. Preserve all original adverse evidence. No broad test skips.

## Acceptance Criteria

Main is ancestor, no conflicts or unintended source differences, no rubric or
manifest divergence; relevant local lint/format/types/tests pass. Dated original
critique and independent Review persist. Clean committed topic, no push.
Hosted CI and human approval remain unclaimed without actual evidence.

## Sources

`.copilot-tracking/research/2026-10-29/finance-510-refresh-2327-research.md`
and its C1-C5 evidence; current component pyprojects and `src/README.md`.

## Phase Checklist

<!-- P01 -->
### P01: Integrate main

* [x] P01-T01: Fast-forward score-only remote update and rebase main.
* [x] P01-T02: Resolve conflicts and prove preservation/source composition.

<!-- P02 -->
### P02: Validate and deliver locally

* [x] P02-T01: Ruff check/format, mypy and relevant core/API unittest modules.
* [x] P02-T02: One independent Review; reconcile artifacts; commit.
* [x] P02-T03: Nonqueued complete-gate attempt; report actual results externally.

## Test Ownership and Evidence Lock

Tests owned by `src/core/tests` and `src/api/tests`; removals none, maximum
additions zero absent demonstrated integration defect. Canonical source paths:
`src/core/src`, `src/api/src`; generated main-owned rubric and scenario manifest.
Regression: finance review/staging/pack, signoffs, matching, lifecycle, provenance,
rescan, scenario manifest, dependency rules and affected HTTP role inventory.
Semantic preservation: compare original finance and main against integrated
source, assert log append/index entry preservation, range-diff commits.
Full API discovery is unnecessary unless focused failures justify escalation;
if run, require both probe and held nonblocking lock. Gate uses `--lock-timeout 0`.

## Critique Disposition

Exactly one independent critique Complete / original Revise, Medium 2.
PC-001 adopted directly: adverse/blocked Review prevents ready handoff; evidence
commits or diagnostic gate attempts cannot supersede it. Route unresolved
findings to later work without repeating Review.
PC-002 adopted directly: success-only external receipt verification; base
drift blocks current-main coverage and requires reconciliation/new gate.
Both resolving branches are in P02-T02/T03 details. No user decision needed.

## Follow-Up Items

Coordinator publication and hosted CI after handoff; prior business/human
finance approval boundaries remain unchanged.
Original independent Review: Complete / Residual work, RV-001 Low (final
evidence commit and complete gate). No new integration defect. Outcome remains
unchanged; no second Review. Publication readiness stays unproven.
Complete-gate attempt exit 1: candidate has pre-existing ignored inputs.
No receipt created, verification inapplicable. Gate success remains blocked;
completion marker records the actual required attempt, not a passed gate.

## Handoff

Details: `.copilot-tracking/details/2026-10-29/finance-510-refresh-2327-phase-details.md`.
Changes: `.copilot-tracking/changes/2026-10-29/finance-510-refresh-2327-changes.md`.
Readiness remains blocked for any adverse Review or unmet publication gate.
