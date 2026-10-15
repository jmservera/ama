---
title: Issue 176 src synthetic determinism plan
description: Bounded completion of migrated generator reproducibility and safe refresh
ms.date: 2026-10-15
---

Task: #176. Slug: issue-176-src-determinism. Mode: automatic.

## Executive Summary

Reuse migrated scale/sensor generators. Record explicit as-of and
dependency-aware source revision, refuse nonempty output destinations, and
test exact bytes across every output including multiple sensor shards.
Preserve historical default generated rows and current SQL/AI/human gates.
Private stock reproduction and refresh approval are not achievable here.

## User Decisions and Requirements

* Full research, plan, implement and review loop; commit its evidence in PR.
* Work only in prescribed worktree/branch, new code/tests only in src.
* Follow ADR 0006 and parity matrix; no workload imports from core.
* Use ZF_DATA/private temporary outputs; no private data, env or VS Code edits.
* SQL Server portable SQL, pip only, Azure-only deployment.
* Local suites, ruff, mypy and synthetic app smoke first; no fake AI evidence.
* Commit/push and PR to main with Refs #176; leave unsupported ACs unticked.

## Goals

Reproduce all migrated scale/sensor output bytes from recorded parameters;
make source changes visible and prevent silent fixture refresh.

## Scope and Non-Goals

Extend core/synthetic only, add core tests and related operational docs.
No new private stock generator, external climate/device integration,
operational approvals, model configuration change, deployment or live reset.

## Functional Requirements

* Shared typed helper computes source revision from explicit dependencies,
  validates ISO date, and creates only a new or empty destination.
* Scale records fixed exercise as-of (2026-09-30); event distribution stays
  the historical calendar-year fixture, not a new event cutoff.
* Sensor accepts as-of (exclusive UTC end); omitted date preserves START
  (2024-10-01), including custom days. Full default window ends 2026-10-01.
  Thread start through estimate, outdoor and readings, including estimate-only
  CLI; record start, end, days, cadence and stock seed.
* Both manifests record version, seed, as_of, generator_revision and per-file
  SHA-256 for every generated payload (manifest excluded from self-hash).
* Reject invalid counts, cadence and dates before any writes. Refuse existing
  nonempty destination without overwrite override. Existing loader unchanged.

## Non-Functional Requirements

No clock/Git/path dependence in output metadata, deterministic UTF-8/LF output,
no dependencies or new lint/type exemptions. No code removals; at most one
shared helper and one new test file. Existing moved modules retain their
existing exemptions; new helper/tests must pass strict checks.

## Acceptance Criteria

* [x] Slice: all scale and multi-shard sensor output bytes match on rerun;
  seed/date changes affect output, manifest hashes verify.
* [x] Slice: invalid inputs and refresh refusal preserve existing bytes.
* [x] Slice: component suites, lint/type, synthetic app smoke recorded.
* [ ] Issue AC1: each generator including private stock register deterministic.
* [ ] Issue AC2: each generator output manifest includes seed/version/revision.
* [ ] Issue AC3: cadence/approval/live-protection policy accepted by owner.

## Sources

Research: .copilot-tracking/research/2026-10-15/issue-176-src-determinism-research.md
Evidence C1-C7 and W1-W3. Existing support-generator regressions remain owned
by src/core/tests/test_generated_dataset.py; portable loader coverage remains
in test_sensor_backfill.py.

## Phase Checklist

<!-- P01 -->
### P01: Generator contract and regression coverage

Phase status: completed.

* [x] P01-T01: Add shared provenance/refresh helper and extend existing writers.
* [x] P01-T02: Add semantic and byte-level regression tests in core/tests.

<!-- P02 -->
### P02: Documentation and local validation

Phase status: completed; image/real Azure execution not claimed.

* [x] P02-T01: Update core guide, synthesis, reference index and append log.
* [x] P02-T02: Run all five project suites, ruff/format/mypy, synthetic local
  app and Docker probe; record exact commands/results.

<!-- P03 -->
### P03: Review and delivery

Phase status: completed; PR #309 open to main, no merge.

* [x] P03-T01: One post-implementation RPI review; route residual work.
* [x] P03-T02: Commit changes/evidence with privacy-safe identity and trailer;
  push topic and create PR to main. Never merge.

## Critique Disposition

Executed once, Complete/Revise; six findings evaluated and resolved in this
candidate. No second critique. Artifact:
.copilot-tracking/reviews/2026-10-15/issue-176-src-determinism-critique.md.

* PC-001: accepted; annotate writer signatures and revision-source helpers
  so strict new tests call typed public boundaries, no new ignores/casts.
* PC-002: accepted; exact dependency sets specified in details.
* PC-003: accepted; estimation and estimate-only share resolved window.
* PC-004: accepted; pre-change hashes captured before edits; default start
  preserved even for existing custom-days callers.
* PC-005: accepted; validate full representable window before mkdir.
* PC-006: accepted readiness distinction; any in-scope blocking Review
  finding prevents a ready claim. The suggestion to fix after Review conflicts
  with the one-pass RPI routing contract and is rejected: route findings to
  later work and report blocked/needs-follow-up, never claim acceptance.

Planning Readiness: Ready for the bounded slice after these direct revisions.

## Follow-Up Items

Private stock generator source/reproduction; owner approval of proposed
refresh cadence/versioning; full-scale sensor and external climate evidence;
real Azure model smoke if unavailable locally. Do not implement these here.
CI on implementation commit 774137a passed all eleven checks, including images
and SQL Server; later documentation/evidence-only delivery does not replace
the recorded local limitations.

## Handoff

Details: .copilot-tracking/details/2026-10-15/issue-176-src-determinism-phase-details.md
Changes: .copilot-tracking/changes/2026-10-15/issue-176-src-determinism-changes.md
Critique dispositions resolved; implementation and one Review completed.
Review outcome: Residual work, not issue-wide acceptance. Delivery PR #309
uses Refs #176. No child follow-up started and no merge performed.
