---
title: Live IoT Hub bounded implementation plan
ms.date: 2026-10-29
---

Task: 140-184 / iot-hub-live-140. Branch: feat/iot-hub-live-140.

## Executive Summary

Reused the existing B1 hub, not a second paid resource. Reconciled diagnostics
and verified the existing built-in consumer group using an isolated entry point, preserving
the production keyless/private routing graph unchanged. Separate publisher
approval from routed-consumer activation. Registry permission inspection found
only ARM Owner, so X.509 issue/send was parked without a public-network toggle.
Do not enable service SAS or self-grant missing permissions. If blocked, prove
the consumer against disposable real local SQL and record exact cloud gaps.

## Sources

Research: `.copilot-tracking/research/2026-10-29/iot-hub-live-140-research.md`.
ADR0003 decision6, infra README IoT section, issue140/184/137, current adapters.

## User Decisions and Requirements

* Full Research, Plan, Implement, Review sequence explicitly requested.
* Paid B1/one unit/one hub, ama/uksouth, USD5 additional through October31 approved.
* Hub only; no new endpoint, namespace or broad/operator RBAC. Existing API
  data role only if actually applicable and already approved.
* No secrets in output, logs, git or .env reads; ephemeral device files outside
  repo deleted afterwards. Never touch private datasets.
* All apps min0, eight jobs Manual, SQL private. Reuse initializer execution
  override for counts only; no app revision.
* Required Ruff/format/mypy/unittest with /tmp/mv; local commit with trailer,
  Refs #140 #184 only, no push or rubric score edits.

## Goals

Deliver the greatest verifiable safe portion of live telemetry immediately.
Make actual live delivery, local engineering proof and unapproved work distinct.

## Scope and Non-Goals

Scope: hub-only Bicep/profile/tests/docs, publisher activation separation,
bounded live attempt and counts, local real-SQL consumer proof, evidence.
Non-goals: new paid Event Hub/PE, new operator roles, service auth weakening,
new cloud app revision, real devices, automatic schedules or issue closure.

## Functional Requirements

* Dedicated profile references the exact existing hub and deploys only its
  metrics diagnostic and built-in consumer-group children, with actual
  ama/uksouth/B1/1 guards. Never PUT hub or change its private attachment,
  retention, auth, routing, tags or networking.
* Device-only activation does not permit receiver construction; existing
  receiver retains exact routed namespace and managed-identity requirements.
* Park issue/send when existing operator data permission is absent; no
  credentials, identity or public-network change on this observed outcome.
* SQL inspection counts sensor tables only, never rows; use existing Manual
  initializer command override, no resource/job-template update.

## Non-Functional Requirements

No shared credential reads; SDK tracing disabled; fixed errors only.
Budget attribution <=USD0.97 for three full hub days, reserve remainder of USD5
for existing shared metrics and bounded job; no claim of enforced spending cap.
Preserve production behavior, resident authority and human approvals.

## Acceptance Criteria

1. Both production and hub-only Bicep build/lint, isolated what-if reviewed
   for exact allowed types before apply; no broader graph deployed.
2. No new paid hub, namespace, PE, role, scale or schedule; metrics only.
3. Publisher activation has positive and negative regression tests; receiver
   cannot accept device-only activation.
4. Record live messages and SQL counts or exact blocker; never equate mock/local
   delivery with live end-to-end or claim gauges show live input unobserved.
5. Required static/unit and real local SQL proof recorded, dated artifacts,
   independent one-pass Review, local commit only. Full local gate attempted
   after commit if shared lock/prerequisites permit; failure blocks publication.

## Phase Checklist

<!-- P01 -->
### P01: Hub-only deployment boundary

* [x] P01-T01 Add isolated entry point/profile and compiled semantic tests.
* [x] P01-T02 Build/lint/what-if and reconcile exact existing hub children.

<!-- P02 -->
### P02: Bounded publisher and runtime proof

* [x] P02-T01 Separate device-only activation with targeted tests.
* [x] P02-T02 Verify existing registry authority; park absent permission, record
  zero hub ingress and no device/credential/network mutations.
* [x] P02-T03 Counts-only private SQL inspection and disposable local SQL proof.

<!-- P03 -->
### P03: Documentation, validation and handoff

* [x] P03-T01 Update cost/environment/ADR and KB index/log without rewriting history.
* [x] P03-T02 Required checks and reconciled handoff for original independent
  Review, local commit and full gate. Preserve adverse results and no push.

## Test Ownership and Change Limits

Canonical source: infra entry point/profile; API iot_stream.py.
Tests: infra/tests/test_iothub_module.py and src/api/tests/test_iot_stream.py.
Removals: none. Maximum additions: 12 focused test methods, one standalone Bicep
entry point, one parameter profile; no new dependency or generic framework.
Semantic checks: exact deployable types, auth/network defaults and activation
separation. Regressions: existing production module, publisher/receiver, replay,
ingestion/idempotency and actual SQL. Generated JSON only outside repository.

## Critique Disposition

Original critique: `.copilot-tracking/reviews/2026-10-29/iot-hub-live-140-plan-critique.md`,
executed once, Revise (3 High, 1 Medium); preserve verdict.

* PC-001 rejected in part: claimed temporary-file prohibition is not supported
  by parent environment or actual /tmp/mv command results, and changing the
  explicitly requested venv conflicts with owner direction. Retain /tmp/mv.
  Apply compatible portion: preflight scratch/gate paths; park on real failure.
* PC-002 applied: pin existing exact hub and child IDs. Reject hub Create/Delete,
  replacement, unknown property drift or endpoint-attachment changes. Allow
  metrics-only diagnostics, new built-in consumer group, explicit device/module
  auth flags and bounded public opt-in only. Preserve routing/fallback, identity,
  tags, TLS, SKU, partitions/retention and existing PE attachment IDs.
* PC-003 applied: all relevant local static/unit/compiled checks precede any
  cloud mutation; real local SQL proof precedes cloud SQL count execution.
* PC-004 applied: one deploy per intended state (private reconciliation,
  temporary public, private restoration), <=600seconds per apply, no blind
  retries. One device lookup/create/delete each with <=20seconds HTTP timeout;
  <=60seconds publishing, <=2 messages. Metrics <=3 queries over <=180seconds.
  One SQL execution only, query/login timeout15/10seconds, process self-exits
  <=45seconds, no retry; inspect existing job retry0 and replicaTimeout<=300
  before admission. Stop exact owned execution on overrun, verify terminal
  state. Reject admission if bounds cannot be established. USD1 attributed hub,
  USD1 reserved shared diagnostics/job, USD3 unspent contingency. Stop all new
  exercise activity by 2026-10-31T23:59:59Z; no ongoing simulator scheduled.

Candidate Ready after direct dispositions; no second critique.

## Follow-Up Items

Implementation amendment: direct hub PUT what-if proposed deleting service-owned
properties. No apply; isolated profile now references the existing hub and
reconciles children only, with actual B1/one-unit guards. No public toggle or
device creation attempted: exact operator role check finds only Owner, which
does not grant registry data actions. No service-key workaround is selected.
Local SQL45 tests pass before cloud counts. Actual initializer retry1/timeout600
is preserved: maximum three operator starts after two diagnosed transient-probe
failures, max six platform attempts/3600seconds conservative bound, each query
process has40second self-exit; <=USD1 ancillary reserve. No fourth attempt.
Third execution Succeeded, private SQL sensor reading/delivery/DQ tables absent
(availabilityfalse/count0, not three empty existing tables). This replaces
assumed retry0/300 without a job-definition change; failures retained.

* Registry permission if absent: owner may assign IoT Hub Registry Contributor
  to the existing operator at this exact hub, with separate approval.
* Keyless cloud consumer needs separately approved paid adapter and API revision;
  an ineffective receiver role on hub is not a workaround.
* Resident gauges need actual SQL/projection/freshness proof before acceptance.
* Credential lifecycle/OD43 and complete parent criteria remain unproven.

## Handoff

Details: `.copilot-tracking/details/2026-10-29/iot-hub-live-140-phase-details.md`.
Implementation changes: `.copilot-tracking/changes/2026-10-29/iot-hub-live-140-changes.md`.
Implementation ready for original independent Review after final documentation
reconciliation. Live telemetry is parked, not delivered; source/SQL engineering
and hub-child deployment evidence are recorded in the changes artifact.
Downstream lifecycle, not implementation acceptance: original Review, commit
including original evidence, full exact-head gate and no push. No operational
approval or live-message success is inferred from checked conditional tasks.
