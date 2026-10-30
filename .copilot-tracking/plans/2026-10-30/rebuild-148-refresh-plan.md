---
title: Rebuild 148 branch refresh plan
description: Local rebase and validation plan for draft PR 511
ms.date: 2026-10-30
---

## Task Metadata

Task: pr-511-refresh-2026-10-30. Slug: rebuild-148-refresh.
Readiness: implementation-ready; original critique Complete / Revise retained,
PC-001 directly resolved.

## Executive Summary

Rebase the existing draft onto fetched main and keep the original synthetic
rehearsal scope. Preserve both documentation intents and current-main
rubric/manifest data. Validate locally, record independent Review and commit;
the coordinator alone pushes.

### What You May Not Know

The old hosted rubric failure is an integration-permission error. Local
tests cannot prove that hosted permissions are fixed. Original RV-001 remains
open. Full publication evidence and human/hosted approvals remain distinct.

## Sources

Research: .copilot-tracking/research/2026-10-30/rebuild-148-refresh-research.md.
Original PR and RPI evidence dated 2026-10-27 are retained, not superseded.

## User Decisions and Requirements

* Rebase feat/rebuild-148 onto origin/main; preserve both conflict intents.
* Keep main's rubric files and scenario manifest; test changed source pins.
* Source under src only, external tests, no legacy code or Azure operations.
* Use /tmp/mv; run Ruff, format, applicable mypy and relevant unittests.
* No full API discovery unless the nonblocking heavy-lock probe succeeds.
* Conventional commit with required Copilot trailer; no push or issue-closing
  keywords. Record commands and results.

## Goals

Produce a clean, locally verified descendant of main for coordinator handoff.

## Scope and Non-Goals

Integration fixes and dated evidence only. No rebuild redesign, RV-001 fix,
workflow permission changes, private data, Azure operations or publication.

## Functional Requirements

Retain ordered synthetic rebuild behavior and current-main changes. Preserve
append-only documentation and README entries if any conflict arises.

## Non-Functional Requirements

Do not modify shared venv dependencies without an actual missing-dependency
failure. Retain every adverse result. Do not equate local passes with CI.

## Acceptance Criteria

* Main is an ancestor after successful rebase, with no conflict markers.
* Main rubric and scenario manifest match byte-for-byte.
* Ruff/format and mypy pass for affected orchestrator plus core/API checks;
  targeted synthetic tests and scenario-manifest regressions pass.
* Original evidence survives; one critique and one independent Review exist.
* Conventional commit uses authenticated noreply identity and required trailer.
* No push, Azure operations, source outside src, or tests inside packages.
* Missing complete exact-head publication receipt is explicitly reported;
  do not publish without it.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Integrate main
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Rebase and resolve

Run requested rebase and resolve preserving both intents. Test ownership stays
with existing orchestrator/core/API tests outside packages. Exact removals:
none. Maximum additions: zero test modules and zero production modules.
Canonical targets are existing conflicting files only; generated targets:
none. Regressions exercise unchanged semantic rebuild safety, namespace and
manifest binding rather than introducing new behavior.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and record
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run targeted local checks

Use /tmp/mv, sibling src/tests import paths, existing Ruff/mypy configuration,
orchestrator discovery and scenario/core/API dependency tests. Avoid full API
discovery by default. Record exact commands, outputs and failure dispositions.
Attempt complete local gate only after commit, honoring the shared heavy lock
and no-Azure boundary; unavailable prerequisites block publication.

<!-- rpi:phase id=P03 -->
### [ ] P03: Review and commit
<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Independent Review and local handoff

Fresh independent reviewer assesses refresh against main, validation and
plan; preserve outcome without a second Review or hidden follow-up fix.
Commit implementation and dated evidence with required trailer, then inspect
clean state and ancestry. No push.

At source-review handoff P01/P02 are complete with passing checks; P03 remains
unchecked until Review, evidence commit and the post-commit gate attempt are
recorded. This is administrative remaining work, not unfinished source.

## Critique Disposition

Exactly one independent critique completed with verdict Revise. PC-001
(Medium) applied directly: fresh-main binding, successful receipt verification
and invalidation requirements added to phase details. No user decision needed
and no second critique. Implementation was launched alongside critique
retrieval before this disposition/state write; this ordering deviation is
preserved in changes rather than presented as conformant sequencing.

## Follow-Up Items

* Original RV-001 belongs to a separately selected implementation task.
* Hosted rubric permission/score and publication gates belong to coordinator.

## Handoff

Details: .copilot-tracking/details/2026-10-30/rebuild-148-refresh-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-30/rebuild-148-refresh-plan-critique.md.
Changes destination: .copilot-tracking/changes/2026-10-30/rebuild-148-refresh-changes.md.
