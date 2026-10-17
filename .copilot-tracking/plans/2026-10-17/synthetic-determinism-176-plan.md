---
title: Issue 176 recovery plan verification
description: Reconcile the completed plan before fresh implementation inspection
ms.date: 2026-10-17
---

Task ID: 176. Stable slug: synthetic-determinism-176.

## Executive Summary

Verified the existing delivered plan rather than proposing new application
behavior. Research, plan verification and implementation inspection are
complete. All 45 scoped tests passed without skips; whole-core Ruff
check/format and project mypy passed. No source bug or behavior change.
Recovery Review is Complete / Residual work, with no implementation defects.
Next commit/push only dated recovery artifacts on the existing PR. Full
issue acceptance remains partial.

## User Decisions and Requirements

* Perform Research, Plan verification, implementation inspection and Review
  in that order now; do not manufacture lost execution evidence.
* Reuse existing artifacts and independent review as historical inputs only
  to the extent they can actually be recovered.
* No application change absent a genuine bug; no original stock replacement.
* No Azure, new spending, private data, secrets or unrelated file edits.
* Use pip only in an owned temporary venv if dependencies are missing.
* Commit with authenticated repository-local privacy-safe identity and the
  required co-author trailer; normal push on feat/synthetic-determinism-176.
* Keep PR #368 as Refs #176, with no closing relationship, merge or force push.
* Stop after concrete phases, final SHA, validation and remaining gaps.

## Goals

Create persistent fresh recovery evidence adequate for coordinator review.
Preserve current behavior and acceptance honesty.

## Scope and Non-Goals

Read the existing feature, helpers, tests and related documentation. Write
only new dated tracking artifacts. No dataset refresh, historical artifact
rewrite, new generator, operational approval or unrelated remediation.
User explicitly authorizes each phase and final stop; no autonomous child
task or automatic follow-up session is started.

## Functional Requirements

Verify strict optional date parsing, label-only date semantics, exact
read-once source digests, BOM/quoted-CRLF compatibility, unchanged v1 draws,
optional cases/history, source revision, default paths and refusal guards.

## Non-Functional Requirements

Use declared pip tooling and Python 3.12. Retain exact new command output
inside tracked recovery evidence, not solely ephemeral logs. Run scoped
tests only after confirming they substitute fictional/temporary data.
Run core's CI lint commands (`ruff check .`, `ruff format --check .`) and
project mypy. No changed dependency manifests or new dependencies.

## Acceptance Criteria

| Criterion | Required recovery result |
| --- | --- |
| Four requested phases | Distinct dated artifacts, ordered state transitions and fresh results |
| AC1 complete generator replay | Unmet overall; no original OSM generator/pinned inputs/runtime |
| AC2 complete manifests | Partial overall; historical receipts not rewritten |
| AC3 refresh protection policy | Documented only; owner adoption/live reset not performed |
| Upstream and independent review claims | Report exact git/check evidence and unavailable review provenance, not a blanket docs-only/MERGE claim |
| Publication | Same branch/PR, Refs #176, empty closing relationships, remote/local SHA match |

## Phase Checklist

<!-- P01 -->
### P01: Recovery inspection and validation (complete)

* [x] P01-T01: Inspect implementation and original plan/critique coverage.
* [x] P01-T02: Rerun four named scoped test modules and core project lint/type checks.

<!-- P02 -->
### P02: Recovery review and publication

* [x] P02-T01: Perform one new recovery Review; dispose findings and acceptance gaps.
* [ ] P02-T02: Commit/push dated evidence and verify PR relationship and final SHA.

## Original Plan Verification and Critique Disposition

Verified existing 2026-10-16 plan/details against current issue and artifacts.
P01-T01/T02 correspond to the two touched Python files. P02 evidence still
needs fresh execution because lost ephemeral output is not available.
The original one final-candidate critique is reused, not rerun: PC-001
requires explicit disposition of blocking findings; PC-002 requires precise
raw-byte/parser/date compatibility oracles. Both are incorporated in the
original completed plan/details and present in the current tests, subject to
implementation inspection and fresh execution in P01. This recovery does
not expand the implementation candidate or reset its critique count.
No new critique/delegation is needed for this bounded verification-only pass.

## Locked Test and Change Budget

Test ownership: existing test_stock_fabric, test_synthetic_determinism,
test_sensor_stock and test_generated_dataset modules. Removals: none.
Maximum production/test additions: zero unless an evidenced genuine bug
requires an explicit recorded amendment. Canonical targets: dated recovery
tracking files; generated application/dataset targets: none committed.
Semantic evidence: source digest/date/parser/refusal assertions.
Regression evidence: golden rows, payload hashes, sensors and fixture-backed
programme persistence. Historical CLI smoke is not reclassified as new.

## Follow-Up Items

Original stock generator and pinned inputs/runtime remain owner-supplied
prerequisites for AC1/AC2. Human owner adopts/amends refresh policy separately.
Independent prior MERGE receipt remains unavailable in retrieved records;
the caller's report is not falsified or independently certified.

## Handoff

Readiness: Recovery Review Complete / Residual work; only P02-T02 publication pending.
Research: .copilot-tracking/research/2026-10-17/synthetic-determinism-176-research.md.
Details: .copilot-tracking/details/2026-10-17/synthetic-determinism-176-phase-details.md.
Original critique: .copilot-tracking/plans/2026-10-16/synthetic-determinism-176-critique.md.
Next changes record: .copilot-tracking/changes/2026-10-17/synthetic-determinism-176-changes.md.
