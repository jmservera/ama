---
title: PR 508 current-main rebase plan
description: Bounded integration, validation and unpushed handoff
ms.date: 2026-10-29
---

Task ID: pr-508-rebase-2026-10-29. Slug: iot-508-rebase.

## Executive Summary

Rebase the existing branch on main 56535475, preserve both documentation
contributions, retain authoritative rubric/manifest bytes and rerun local
core/API checks. Finish with one independent Review and a conventional
commit. No remote write or Azure operation.

## User Decisions and Requirements

* Execute Research, Plan, Implement and Review with dated tracking artifacts.
* Rebase origin/main; preserve both sides, including append-only log/index.
* Take main's `.github/rubric/*` and scenario manifest.
* Source stays in src; tests outside packages; no mvp source.
* Use /tmp/mv for Ruff, format, mypy and relevant unittests with sibling paths.
* No full API discovery unless nonblocking shared-lock admission succeeds.
* Conventional commit and required Copilot trailer; no push or closure keywords.

## Goals

Integrate current main without regressing bounded IoT or newer sensor scenarios.

## Scope and Non-Goals

Conflict resolution, directly coupled compatibility fixes, dated evidence.
No redesign, Azure, deployment, issue acceptance, hosted CI claims or push.

## Functional Requirements

Preserve finite pacing, cancellation/cleanup, provenance and outside-package
test ownership. Preserve main's new scenarios and both README/log entries.

## Non-Functional Requirements

No unapproved dependency changes, destructive cleanup or lost historical
evidence. Record commands, failures, skips and validation limits explicitly.

## Acceptance Criteria

* origin/main is an ancestor; no unresolved conflict markers.
* Rubric subtree and scenario manifest match the reviewed main.
* Both core/API configured Ruff, format and mypy pass.
* IoT, ingestion, sensor stream/consumer/scenarios, manifest and dependency
  boundary selectors pass or an explicit blocker prevents completion.
* One independent critique and one Review are recorded; no approval invented.
* Local commit with required identity/trailer; no push.

## Test Ownership and Evidence Boundary

Canonical source: src/core/src and src/api/src. Tests: owning src/*/tests.
Exact removals: none. Maximum additions: zero unless a discovered compatibility
defect requires a focused regression (then record amendment before addition).
No generated runtime outputs. Rubric/manifest are restored from main, not
regenerated. Existing scenario tests cover semantic integration; IoT selectors
cover regression. Full API discovery is not planned; if needed, acquire and
hold `/tmp/ama-rpi-heavy.lock` nonblockingly for its entire run.

## Phase Checklist

<!-- P01 -->
### P01: Integrate

* [x] P01-T01 Rebase and resolve preserving semantic intent.
* [x] P01-T02 Verify main ancestry, rubric/manifest identity and docs retention.

<!-- P02 -->
### P02: Validate

* [x] P02-T01 Run configured core/API static checks and relevant unittests.
* [x] P02-T02 Record exact results and resolve only coupled failures.

<!-- P03 -->
### P03: Review and commit

* [x] P03-T01 Execute one independent Review of integration and evidence.
* [x] P03-T02 Commit with privacy-safe identity and trailer; leave unpushed.

## Critique Disposition

One independent critique executed, Complete / Revise. PC-001 (Medium,
planner-owned) resolved directly by recording exact core/API module invocations
in phase details. No user decision needed and no repeat critique. Plan Ready.
Original critique: .copilot-tracking/reviews/plans/2026-10-29/iot-508-rebase-plan-critique.md.

## Follow-Up Items

Coordinator publication gate, remote update and hosted/human approval remain
outside this no-push integration handoff.

## Handoff

Research: .copilot-tracking/research/2026-10-29/iot-508-rebase-research.md.
Details: .copilot-tracking/details/2026-10-29/iot-508-rebase-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-29/iot-508-rebase-changes.md.
