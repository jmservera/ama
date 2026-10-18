---
title: Issue 122 continuity epoch and export plan
description: Bounded implementation plan, not operational acceptance
ms.date: 2026-10-18
---

Task ID: 122. Slug: issue-122-continuity-epoch-export.
Status: Authorized correction TWO final source cycle implementation and fresh
validation complete; publication permitted, independent acceptance pending.
Original Complete / Not accepted Review remains frozen. No further critique or Review.
Current operation: coordinator-authorized integration only onto exact
3104bb69ddc26c81e0e9d2f57000dac1d99a419a after #397, not a third source
correction. Original base and correction evidence below are historical.

## Executive Summary

Baseline reproduction confirms stale ready proposals become actionable after
restart, can be accepted and exported as relied-on, and fresh invocation reuses
their IDs. Bind proposal lifetime to persisted epoch, retain old dispositions as
non-current history, and export retained task-release evidence with lifecycle
events and explicit gaps. Use current SQL transaction boundaries; the sole #87
exception is the coordinator-authorized two-name STAFF_GET append. No web work,
schema refactor or live-system activity.

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
Current integration base: 3104bb69ddc26c81e0e9d2f57000dac1d99a419a.
Original tested correction source 0067f2a1 is preserved byte-for-byte in rebased
24ee70347064886a1847b1fea8b5219ad6323e6d, except the explicitly composed
upstream projection and additive README context; no domain changes.

## Goals

Prevent cross-epoch reliance and new-work reuse while retaining permitted history;
make task-release evidence reconstructable offline without an AI provider/store.

## Scope and Non-Goals

Active: assistants.py, continuity.py, ai_tasks.py, tightly coupled legacy
store.py priority/cache surfaces, focused API tests and component documentation.
store.py is not among the coordinator's #87 overlap files. Correction ONE may
append only continuity and continuity_export to projection.STAFF_GET. Do not
otherwise change projection.py, appointments.py, procurement.py, sqlstore.py,
server.py or web.
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

Execution markers do not mean acceptance. Original HTTP 403 evidence and both High
findings remain frozen in the original Not accepted Review. Authorized correction
ONE supplies fresh evidence; no new Review or self-acceptance is permitted.

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

### Authorized ancestry integration after #397

* [x] I01 Verify exact old head/remote lease and exact fetched base, rebase owned
  branch only, retain all 35 upstream changed files and prove owned-source parity.
* [x] I02 Execute targeted host, actual SQL cross-domain and rebuilt installed-image
  integration checks, reconcile metadata and exact-lease update the same PR #398.

Sole conflict is adjacent README section insertion; both sections retained.
Original frozen hashes and append-only knowledge-log prefix remain intact.
Independent full review is scheduled after integration by coordinator, not run here.
Integration execution complete: host 563 (108 skips), actual owned SQL 81,
installed hardened image 329 (58 skips), configured static checks pass. No known
failure found in these selected boundaries; no new source cycle or acceptance.

### Authorized correction TWO final source cycle

Coordinator permits existing-policy audience projection in continuity export.
Reason-ineligible managers retain export access but receive explicitly limited,
incomplete evidence, never restricted text or an allegedly intact redacted chain.
Canonical server-side ledger and full reason-authorized manager proof remain.
No appointment/shared SQL/web/policy/cryptographic protocol change or new Review.

* [x] P05-T01 Reproduce retained failure, reuse audit/export projection prior art,
  implement limited export and nested evidence/full-proof regressions.
* [x] P05-T02 Run fresh targeted host/role inventory, actual owned MSSQL and rebuilt
  hardened-image/static checks; reconcile and publish only if no known source failure.

### Authorized correction ONE (2026-10-18)

Original Review is Complete / Not accepted and remains frozen. Same-session
coordinator direction authorizes only appending continuity and continuity_export
to projection.STAFF_GET, with existing inner audience controls unchanged.
Correction ONE implements both RV-001/RV-002 together; no new critique/Review.

* [x] P04-T01 Add failing-first metadata/completeness and actual HTTP audience
  regressions; apply only authorized route append and offline verifier corrections.
* [x] P04-T02 Execute fresh owned MSSQL races/HTTP, host suites/static and rebuilt
  hardened image; reconcile separate receipt. Conditional publication is blocked,
  not performed; retain adverse regression and commit local evidence only.

Implementation changes record:
.copilot-tracking/changes/2026-10-18/issue-122-continuity-epoch-export-changes.md.
Original critique findings were directly dispositioned; original Review ran once.
Coordinator authorized both routed findings as correction ONE. Fresh validation
is complete but adverse: existing role endpoint inventory plus focused host,
actual MSSQL and hardened-image HTTP reproduce restricted ledger-reason disclosure
to Programme Support Officer. Commit local evidence, no push/PR, return the
remaining correction to coordinator. That correction ONE handoff is historical:
the coordinator subsequently authorized P05 correction TWO. Its fresh host 245
(49 opt-in skips), existing 163, actual MSSQL 72 and hardened-image 44 runs pass;
no known source failure remains in these checks. Publish under the explicit
authorization, preserve the original adverse verdict, and return independent
acceptance and operational gates to the coordinator. No further source cycle.
