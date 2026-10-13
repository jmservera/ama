---
title: Five Assistant Runtime Validation Plan
ms.date: 2026-10-13
---

## Approved Direction

Later implementation of RV-003/004 and the nonbillable actual-SQL portion of
RV-002, selected by the owner's explicit autonomous-completion direction.
Parent: five-retrofit-assistants-2026-10-13. Reuse its research, contracts and
accepted PC-001 to PC-008; no new product scope or architecture decision.
Preserve the completed parent Review rather than rewriting it.

## Scope and Acceptance

Existing runtime/UI/tests, CI's existing SQL job, corrected local image and
related PRD/ADR/operator/index/log evidence on #68. No live data reset, tenant
change, new cloud resources, merge or unapproved paid inference/rollout.
Close shutdown admission atomically without holding a lock during inference;
render manual controls independently of bounded auxiliary reads. Prove both
with nonbillable regressions. Exercise the same source/review/claim/allowance
contracts on actual disposable SQL Server, never the pilot database.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Fix and validate runtime contracts

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Close provider dispatch admission at shutdown

Add a dispatch gate and delayed-claim regression. Preserve conservative
reservation accounting and bounded stop; provider work stays outside locks.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Render ordinary controls before assistant reads finish

Depends on P01-T01 for the coherent source batch. Bound/cancel auxiliary reads,
ignore detached/stale panel results and test pending requests, manual writes,
timeout and navigation without real inference.

<!-- rpi:phase id=P02 -->
### [x] P02: Establish repeatable actual SQL coverage

Depends on P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run assistant contracts on disposable SQL Server

Reuse the existing test file, fixtures, pinned driver and CI SQL service.
Include five paths, human-review fixtures, stale/role denial, reservations,
leases, concurrency, recovery, append-only events and startup migrations.
Generate disposable local credentials privately and clean scoped containers.

<!-- rpi:phase id=P03 -->
### [ ] P03: Build and publish the corrected version

Depends on P02.

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Validate image, documentation and source publication

Run existing suites and browser checks, build exact corrected source, retain
source/image/SQL evidence and update canonical learning in place. Publish #68
with privacy-safe commit identity, preserving unrelated work and bot ancestry.

## Outside This Bounded Invocation

Owner-scoped retained-data Azure rollout and finite model allowance remain
required for parent P03/CON-009/AC-057. Human acceptance and semantic/benefit
calibration remain separate, not inferred from mocked inference or SQL parity.
