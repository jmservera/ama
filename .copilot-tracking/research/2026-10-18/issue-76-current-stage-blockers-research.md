---
title: Issue 76 current-stage blockers research
description: Exact-base offline queue consistency investigation
ms.date: 2026-10-18
---
<!-- markdownlint-disable-file -->

## Research Brief

Investigate whether future final-check prerequisites incorrectly classify current
work as blocked. Audience: implementation and independent coordinator review.
Output mode: convergence. Research disposition: executed, complete.
Planning Readiness: Ready.

## Research Parameters

Focused posture, selected for caller's bounded, concrete candidate. Exact base:
6c1e376ff1241316272df22a5a3a6853aae9f87b; clean existing branch
fix/current-stage-queue-blockers-76, no existing PR. Evidence root:
.copilot-tracking/. Research source edits prohibited.

## Extension Registry and Provenance

* Repository .github/copilot-instructions.md selected; read both case studies,
  index, memory and component guides. No private data, support, environment
  secret files, cloud writes, billable operations or model inference.
* rpi-research selected; tightly coupled research inline.
* Web skills skipped: backend read-model correction, no web changes expected.
* Research specialist skipped: one continuous source trace.

## User Participation and Direction Controls

Explicit user request authorizes the full ordered loop and publication, one
independent critique and one original Review, maximum two source corrections.
No additional mode confirmation needed: this is the requested automatic loop.
No work in resident_decisions.py, projection.py or resident core/API tests.
Issue #76 remains OPEN; #290 verified CLOSED; #73 is hierarchy only.
Backlog Manager readiness is unavailable, not an approval. Live Entra and human
role-policy acceptance remain unmet. No new identity or authority implementation.

## Research Questions

1. What current-stage semantics do transitions, controls and technical gates use?
2. Do real JSON/SQL stores reproduce the alleged inconsistency at the exact base?
3. Which persistence and API surfaces consume membership and need parity checks?

## Prior Knowledge Gate

Caller hypothesis is unverified pending actual-source investigation. Owner memory
is context, not evidence. Live issue and dependency checked with gh CLI.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Starting paths: taskqueues, stores, SQL queue helpers, controls, technical gates,
core/API queue tests and component guides. External sources limited to live
GitHub issue metadata; no legal interpretation or live policy acceptance.
Inline breadth identified canonical evaluator, JSON cache, durable SQL flags,
shared SQL Server dialect, stage gate and HTTP projection. Reflection: the
candidate is real, but a membership-only fix would leave final-check metadata
false and persistent original flags certified under an unchanged fingerprint.

#### Wave 2: Deeper

Read transitions and missing_items before reproduction. Store.advance checks
the actual final-check stage and gate_reasons, which combines funding, resident
and technical gates; safety, stock and shared-building holds have independent
controls. Canonical fully supplied synthetic case isolates funding-only and
technical-only deficiencies. Original probe executed both Store and SqlStore:
eight semantic failures, including false membership before final checks and
false current_stop at final checks. Reflection: select current-stage activation,
not removal or bypass of prerequisites.

#### Wave 3: Contrarian

Challenged intentional future-work membership against published definition:
the definition explicitly excludes future-stage stops. Existing tests passed
(25 core/persistence and 3 real HTTP) while all eight semantic probes failed,
so parity alone is not correctness. Examined upgrade counterexample: original
SQL fingerprint certifies old flags even after evaluator correction unless an
input changes. A public default/reset version bump is unnecessary; a separate
internal membership revision must invalidate durable flags. Reflection:
contrarian evidence strengthens the bounded correction and adds upgrade tests.

#### Parent synthesis and disposition

Accept current-stage activation and one shared active list for selection and
membership (C1-C3). Accept internal evaluation revision for persisted upgrade
(C4); reject silently retaining stale indexes or changing the definition to
justify future-work membership. Keep future requirement records visible.
No further research cycle: domain, persistence and API paths covered; remaining
engine execution belongs to implementation validation.

## Evidence Log

| ID | Location | Evidence |
| --- | --- | --- |
| C1 | src/core/src/zava_forward/core/taskqueues.py:28-29,226-261,316-362 | Definition excludes future work; final requirements inactive; membership uses all blockers |
| C2 | src/core/src/zava_forward/core/store.py:155-164,504-521 | Final-check transition enforces separate unchanged gates |
| C3 | src/core/src/zava_forward/core/signoffs.py:26-45,94-118 | Existing competent-role missing items and approval controls |
| C4 | src/core/src/zava_forward/core/sqlstore.py:310-369 | Durable fingerprint and atomic generation refresh, inherited by MSSQL |
| C5 | src/core/src/zava_forward/core/store.py:232-261,314-326 | JSON cache invalidation; membership before unchanged downstream role projection |
| C6 | src/api/tests/test_task_queue_api.py:108-195 | Existing real loopback list/detail/CSV and denial harness |
| C7 | issue-76-current-stage-blockers-before.txt and probe.py beside this artifact | Exact-base real-store eight adverse observations; exit 1 |
| W1 | https://github.com/jmservera/ama/issues/76, retrieved 2026-10-18 | OPEN; live identity acceptance unmet |
| W2 | https://github.com/jmservera/ama/issues/290, retrieved 2026-10-18 | CLOSED, not an ordering blocker |

## Alternatives and Decision State

Select stage-aware final prerequisites, active-list membership and an internal
evaluation revision. Preserve public work-queues-1/default/reset shape because
the implementation is being restored to its existing definition, not changing
the contract. A public version bump is a viable but unnecessarily disruptive
alternative; no revision at all is rejected due to C4.

## Open Questions and Risks

Docker is available with local SQL Server 2022 image. Actual disposable MSSQL
is required because corrected semantics affect indexed persistence.
Do not equate optimized/uncached agreement with independent semantic correctness.

## Self-check

Three ordered inline waves completed; questions answered with C1-C7; no
research workers implied. Original baseline output preserved. Initial system
Python test failed for missing installed zava_forward; task-local pip editable
core[dev,sql], agents and api[dev] installation then succeeded. No model calls.
Production source remains byte-identical to exact base during Research.
