---
title: Issue 122 continuity epoch and export plan
description: Bounded implementation plan, not operational acceptance
ms.date: 2026-10-18
---

Task ID: 122. Slug: issue-122-continuity-epoch-export.
Status: Ready after direct dispositions of the one original Revise critique.

## Executive Summary

Baseline reproduction confirms stale ready proposals become actionable after
restart, can be accepted and exported as relied-on, and fresh invocation reuses
their IDs. Bind proposal lifetime to persisted epoch, retain old dispositions as
non-current history, and export retained task-release evidence with lifecycle
events and explicit gaps. Use current SQL transaction boundaries; no #87 files,
web work, schema refactor or live-system activity.

## User Decisions and Requirements

* Execute Research, Plan, Implement, one original Review in order, committing
  dated artifacts in the same change; one independent plan critique only.
* Bounded partial follow-up, Refs #122 only; do not close issue or claim all AC.
* Actual uniquely owned local Docker SQL tests, independent connections and
  deterministic overlap; no mocks labelled SQL.
* Actual local HTTP/manual transactions and hardened nonroot API image.
* Preserve adverse critique/Review; return defects for coordinator corrections
  (maximum two), never self-Pass or publish a knowingly defective PR.
* No genuine approvals, private data, paid inference, Azure/tenant writes/notices.

## Sources

Research artifact .copilot-tracking/research/2026-10-18/issue-122-continuity-epoch-export-research.md,
C1-C7, W1-W2. Base 99056cae7bc679d2ace3e42c75f28577cfce8887.

## Goals

Prevent cross-epoch reliance and new-work reuse while retaining permitted history;
make task-release evidence reconstructable offline without an AI provider/store.

## Scope and Non-Goals

Active: assistants.py, continuity.py, ai_tasks.py, tightly coupled legacy
store.py priority/cache surfaces, focused API tests and component documentation.
store.py is not among the coordinator's #87 overlap files. Do not change
appointments.py, procurement.py, sqlstore.py, server.py, projection.py or web.
No general reversible-serving-config machinery or operational approval system.

## Functional Requirements

* Creation epoch participates in identity; claim/dispatch/complete cannot promote
  old or unbound work. Missing epoch fails closed, including pre-change pending
  and historical ready/accepted records.
* List/detail/verify/accept/edit/export share epoch currentness without overwriting
  original disposition. Rejection and permitted history remain possible.
* Legacy AI text/document/priority and briefing cache enforce current epoch,
  including refreshed persisted reads by a gate-aware stale process.
* Offline exports include original release snapshot matching retained digest,
  current status/revision and release-ID events; missing, unavailable or truncated
  referenced evidence makes incompleteness explicit. Preserve external-head checks.
* No raw provider request/input additions; retain existing audience projections.

## Non-Functional Requirements

Use existing locks/independent connections and no SQL schema changes. Unknown
billing stays unknown/reserved; no remote cancellation or exactly-once claim.
Old images predating gates must be stopped/drained or externally denied serving
access; process-refresh proof applies only to gate-aware code.

## Acceptance Criteria

Ready and accepted E records remain non-current after suspend/restart with same
source/release; detail/list/review/edit/verify/export regressions prove it.
New reactive and eligible proactive work have epoch-distinct identity; queued
and leased old work cannot cross epoch. Deterministic independent SQL overlap
covers review/suspend and completion/suspend/restart, stale process refresh and
late quarantine. Actual manual case/challenge/hazard transactions still enforce
authority/safety. Offline serialized exports resolve release refs after revocation,
detect missing/truncated evidence and head/digest tampering. Static checks and
source-context hardened API image run with truthful actual outcomes/skips.

## Phase Checklist

<!-- P01 -->
### P01 - Lifetime enforcement and regressions

* [x] P01-T01 Add failing-first focused epoch tests, then implement durable and
  legacy epoch policies; preserve #87 signatures via existing tests.
<!-- P02 -->
### P02 - Offline evidence

* [x] P02-T01 Resolve release snapshots/events and incomplete states, preserve
  permitted projection and integrity; add serialized offline regressions.
<!-- P03 -->
### P03 - Local validation and handoff

* [x] P03-T01 Execute deterministic independent SQLite/MSSQL overlap, HTTP/manual
  paths, existing suites/static checks and hardened Docker image.
* [x] P03-T02 Reconcile changes/docs/evidence and submit once to original Review.

Execution markers do not mean acceptance. Actual HTTP export remains 403 on
SQLite, SQL Server and hardened image due to an existing missing route allowlist
entry in protected shared projection.py. No bypass or shared-file edit. Validation
and known blocker are reconciled in changes/details; original Review must assess
the failed boundary. Coordinator authorization/correction is required.

## Test Ownership and Candidate Lock

Worker owns added focused tests in test_continuity_epoch_export.py and minimal
direct adjustments in existing continuity tests if needed. Exact removals: none.
Maximum additions: 30 semantic test methods, inherited SQL reruns not new methods.
Canonical sources: installed src distributions; generated targets: only temporary
synthetic data, unique owned SQL databases/container and API image/container.
Semantic coverage: epoch policy, offline resolution, actual manual gates.
Regression coverage: existing assistant/continuity/legacy/release/appointment
signatures. Validation evidence must record commands, counts, skips and failures;
no claims based solely on SQL emulation or a note about manual availability.

## Critique Disposition

Original critique execution Complete, verdict Revise, retained unchanged at
.copilot-tracking/reviews/2026-10-18/issue-122-continuity-epoch-export-plan-critique.md.

* PC-001 High, applied directly: final legacy epoch decision and publication
  must share a serialized/optimistically checked writer boundary. Deterministic
  text/document/priority publication overlap tests required on SQLite/MSSQL.
* PC-002 High, applied directly: offline verifier independently resolves all
  release refs and validates snapshot digest/lifecycle event envelopes/counts,
  including recomputed-outer-digest negative fixtures.

No divergent user decision, no rejected findings, no second critique.

## Follow-Up Items

Genuine OQ-017 authority, witnessed authorized drill, immutable externally held
Azure head and Azure SQL drill remain unmet. Wider serving configuration
reversibility and old-image deployment exclusion remain outside this source slice.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-18/issue-122-continuity-epoch-export-changes.md.
Proceed only after critique findings receive explicit planner disposition.
Critique findings were directly dispositioned. Implementation and validation
execution are complete with the material HTTP failure retained; submit once to
original Review, then route defects to the coordinator without self-correction.
