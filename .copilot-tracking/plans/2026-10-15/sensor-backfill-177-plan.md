---
title: Sensor backfill 177 implementation plan
description: Bounded register-backed backfill with explicit evidence limits
ms.date: 2026-10-15
---

Task ID: 177. Slug: sensor-backfill-177. Status: Completed bounded delivery; parent issue remains open.

## Executive Summary

Extend the existing core simulator with an explicit synthetic-register mode,
using merged stock-fabric-v1 rather than independently invented home attributes.
Generate only explicitly granted monitoring fixtures, record every exclusion and
selected home, estimate before writing and preserve legacy fixture payloads.
This is partial delivery of #177, not closure of its still-open children.

## Sources

.copilot-tracking/research/2026-10-15/sensor-backfill-177-research.md;
ADR 0006; parity matrix; issue #177 and children #178-#183.

## User Decisions and Requirements

* Full RPI loop, commit research/plans/changes/reviews and open main-targeted PR.
* Only this worktree and branch; new code/tests in src; no mvp changes.
* Reuse merged fabric; deterministic seeded synthetic data only; pip only.
* Preserve human approval, consent, AI-enabled architecture and portable SQL.
* Test locally including src suites, ruff, mypy and synthetic local app.
* Record unavailable evidence and owner decisions without ticking criteria.
* Refs #177 unless all criteria genuinely met; no main push or merge.

## Goals

Resolve output home IDs to an explicitly supplied synthetic register, retain
stock fabric assumptions and show repeatable bounded two-year evidence.

## Scope and Non-Goals

Core synthetic adapter and existing writer; src tests; core README and existing
synthetic-data synthesis/index/log. No live data, deployment, new AI authority,
new SQL schema migration, real climate claim or child-story closure.

## Functional Requirements

* Optional --register CSV mode consumes only allowlisted synthetic identity,
  building_form_osm, locality_theme and monitoring_consent (granted/declined/unknown).
  Require is_synthetic=true. Missing choice is unknown, not granted.
* Sort opaque unique IDs, reject invalid IDs/duplicates/invalid choices before
  output; --homes selects a declared sorted subset, not a fabricated register.
* Use stock_fabric.fabric at its fixed seed, map dwelling and build-year age to
  existing projection coefficients, add labelled construction exercise factors.
  Stock mode has no invented retrofit history; legacy mode is unchanged.
* Stable sensor IDs preserve opaque IDs without truncation collisions.
  Stock IDs are SENS-SYN- plus full SHA-256 (73 ASCII characters); reading IDs
  append epoch seconds (at most 96 characters). Home IDs support up to 128 UTF-16
  code units. Add STOCK_SQL_DDL with VARCHAR(73)/VARCHAR(96)/NVARCHAR(128),
  recorded as stock-reading-v1; retain legacy SQL_DDL unchanged. Reject oversized
  homes before output. Callers apply the matching schema, then create_schema=None;
  no automatic database migration.
* Register estimate/write both require explicit positive --homes within register
  size. Select the first N sorted register IDs before filtering monitoring;
  never silently replace excluded homes with granted homes outside the subset.
* Record selected/excluded coverage, stock/fabric seed/version/input hash,
  sanitized fabric snapshot, source hashes and estimate from the actual sensors.
* Declined and unknown homes produce no readings; all excluded is valid empty
  output with explicit zero estimate. Synthetic consent is not real consent.
* New stock snapshots stay outside any repository, refuse symlinks/nonempty
  destinations; no source names, addresses or resident fields copied to output.

## Non-Functional Requirements

Same seed/input bytes/window produce identical payloads and metadata. Record
normalized inputs without filesystem-path dependence. Legacy payload hashes
remain unchanged. Core has no workload imports; no new dependencies/SQL syntax.
Current AI release admission remains unchanged and is exercised by local App
smoke; scripted inference is not claimed as live AI.

## Acceptance Criteria

* [x] Supplied synthetic register IDs and v1 fabric reconcile exactly.
* [x] Explicit subset and choice exclusions reconcile; no declined readings.
* [x] Repeats, seed variation, full 730-day boundaries and sharding pass tests.
* [x] Actual selected-sensor estimate is recorded before payload generation.
* [x] Invalid input and unsafe destinations fail without payload writes.
* [x] Local src suites/lint/types/app evidence recorded, limitations explicit.
* [x] Documentation and RPI artifacts committed in a Refs #177 PR.

## Phase Checklist

<!-- phase: P01 -->
### P01: Register-backed generator

* [x] P01-T01: Add typed register adapter and wire writer/estimate/CLI.
* [x] P01-T02: Add tests and retain legacy regressions.

P01 complete: 14 new contract tests plus existing sensor/byte regressions pass.

<!-- phase: P02 -->
### P02: Evidence and delivery

* [x] P02-T01: Update core/synthesis/index/log and run local validation.
* [x] P02-T02: One RPI review, then commit, push and create PR.

P02 complete: review Complete / Residual work; implementation commit 00c0137,
pushed feat/src-sensor-backfill-177 and opened PR #320 to main with Refs #177.
CI was queued/in progress at first observation, not assumed passing.

## Test Ownership and Validation Lock

Core owns tests. Exact removals: none. Maximum additions: one core test module
with at most 16 tests; update existing source revision expectation only.
Canonical targets: core synthetic sources/tests and existing docs.
Generated targets: temporary, outside repository only, deleted after checks.
Semantic coverage: ID/fabric/consent/subset/730-day/unsafe-input contracts.
Regression coverage: existing sensor plausibility/determinism and all src suites.
Validation: unittest in all five projects; ruff check/format and mypy per project;
existing local HTTP release smoke with synthetic data, SQLite loader idempotency,
Docker build attempt, migration regression, git diff checks.

## Critique Disposition

Exactly one critique executed; initial verdict Revise, all findings disposed.

* PC-001 accepted: additive STOCK_SQL_DDL and preflight identifier bounds above;
  test full lengths and portable parameter-preserving loading. No schema migration.
* PC-002 rejected as inapplicable: the critique worker asserted a /tmp prohibition
  absent from this parent's actual instructions. Worktree-only means source/git
  operations in this checkout; existing tests necessarily use temporary synthetic
  outputs. Caller explicitly requires local tests. Use ephemeral temp output and
  session-local tooling, never another checkout/private dataset; retain guard.
* PC-003 accepted: explicit N required for both stock estimate and write, reject
  oversized/zero/negative values, selection before consent and identical estimates.

No divergent user decision required. No second critique.

## Follow-Up Items

Existing #178 climate provenance/licence, #180 dated measures, #181 fuller
behaviour, #182 configurable complete fault/truth classes, #110 consumer reuse,
full-stock storage approval and real AI/SQL Server/Azure/human acceptance.
No owner decision inferred and no issue state changed.

## Handoff

Details: .copilot-tracking/details/2026-10-15/sensor-backfill-177-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-15/sensor-backfill-177-changes.md.
