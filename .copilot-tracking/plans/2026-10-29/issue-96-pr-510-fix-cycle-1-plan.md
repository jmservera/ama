---
title: Issue 96 PR 510 fix cycle 1 plan
description: Report-local freshness reuse implementation and regression plan
ms.date: 2026-10-29
---

## Task Metadata

* Task ID and slug: `issue-96-pr-510-fix-cycle-1`
* Planning status: Ready; single independent critique Complete / Pass.
* Phase details: `.copilot-tracking/details/2026-10-29/issue-96-pr-510-fix-cycle-1-phase-details.md`
* Critique: `.copilot-tracking/reviews/plans/2026-10-29/issue-96-pr-510-fix-cycle-1-plan-critique.md`

## Executive Summary

Reuse a freshness result only within a single report when source ID, version,
content hash and kind all match. Later reports must read current bytes again.
This removes repeated lock-held reads/hashes for shared field evidence without
changing output, finance authority or source visibility.

### What You May Not Know

Candidate review independently checks source bytes before producing a report;
that check is intentionally not shared. A stale schema already short-circuits
freshness checks and must continue to do so. No full publication gate, Azure,
hosted approval or whole-issue acceptance is claimed by this local-only cycle.

## User Decisions and Requirements

* Complete research, plan, implement and review with 2026-10-29 evidence.
* Fix the supplied report freshness finding for Refs #96 and PR #510.
* Source in `src/` only, tests outside the installed package.
* Use `/tmp/mv` and the supplied core/agents PYTHONPATH for validation.
* Commit locally with the specified Copilot trailer; do not push.
* No Azure, closing keywords or manual `latest.json` edits.

## Goals

* Read/hash each exact shared source no more than once per report.
* Preserve fresh verification on each later report.

## Scope and Non-Goals

Canonical targets: `src/core/src/zava_forward/core/form_review.py`,
`src/core/tests/test_form_review.py`, directly related `src/core/README.md`,
and this dated RPI artifact set. Generated targets: none.
No new dependency, cache service, changed lock scope, source policy, financial
decision, unrelated historical review fix or package layout change.

## Functional Requirements

* Cache boolean results, including false, under the exact four-part identity.
* Preserve `_current` exceptions and the existing schema short circuit.
* Keep visibility checks and candidate-review verification independent.

## Non-Functional Requirements

* Cache lifetime is exactly one `_report` call, with linear bounded storage
  in the number of distinct sourced field snapshots.
* No state is persisted on the store, draft, source or module.

## Acceptance Criteria

* Both JSON and SQLite synthetic fixtures prove one byte read for two fields
  sharing evidence in each view/diagnose report.
* Later reports detect changed bytes without relying on changed metadata.
* Negative freshness results are reused and all four key dimensions separate
  different snapshots; an ID-only cache cannot pass.
* Ruff check, Ruff format check, core mypy and relevant unittests pass.
* One independent critique and one post-implementation Review are preserved.

## Sources

Research: `.copilot-tracking/research/2026-10-29/issue-96-pr-510-fix-cycle-1-research.md`,
C1-C4. User request and read-only GitHub issue/PR retrieval dated 2026-10-29.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement and validate report-local reuse

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add cache and regression coverage

Use an explicitly typed dictionary keyed by `(id, version, content_sha256,
kind)` inside `_report`. Compute only on a cache miss, without changing
stale-schema behavior. Add at most three test methods and one shared-source
fixture helper in the existing test module. Exact removals: none.
Test ownership: core form review. Semantic checks: output and stale fields.
Regression checks: byte-read counts and `_current` invocation counts.
Prove at least the shared-source test fails against original code.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Validate and document

Update the core guide to state per-report identity/lifetime. From `src/core`,
run `/tmp/mv/bin/python -m ruff check .`,
`/tmp/mv/bin/python -m ruff format --check .`,
`/tmp/mv/bin/python -m mypy`, and with
`PYTHONPATH=src:tests:../agents/src:../agents/tests`, run unittest modules
`test_form_review test_form_staging test_finance_match_controls
test_finance_signoffs test_grant_lifecycle_controls test_change_provenance
test_document_rescan`. Record real counts/skips; no Azure.

## Dependencies

Existing `/tmp/mv` Python 3.12 environment and synthetic JSON/SQLite fixtures.
No new dependencies planned. Review follows successful reconciliation of
plan, details, changes and validation.

## Critique Disposition

Single independent critique Complete / Pass, no findings or required changes.
Original critique is preserved at the metadata path. No second critique.

## Follow-Up Items

* Whole finance acceptance, human authority and historical review outcomes
  remain governed by their original evidence, not this performance correction.

## Handoff

Changes path: `.copilot-tracking/changes/2026-10-29/issue-96-pr-510-fix-cycle-1-changes.md`.
P01 complete: red/green regression, requested static checks and 201 tests
(54 existing optional skips). Proceed to one independent Review.
No push or publication; full local publication gate is not requested here.
