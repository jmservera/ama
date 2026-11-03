---
title: Issue 115 round 1 research
ms.date: 2026-11-03
---

Research disposition: executed (repository and merged PR inspection). Planning Readiness: Ready.

## Already delivered (do not redo)

* PR #268: container, create-only publish, scheduled verify job, mismatch and missing-heartbeat log alerts, unlocked retention policy in infra/modules/storage.bicep.
* PR #404: remote anchors must be recognised and canonical; failures alert and exit 1.
* PR #658: release digest stable after invalidation (related).

## Acceptance criteria status

* Digests land in an immutable container with a retention lock: unmet. The policy is created unlocked; owner-approved retention duration, the irreversible lock and live evidence are missing.
* Scheduled verification alerts on mismatch: unmet in hosted terms. Offline behaviour is tested; hosted run, Log Analytics table names, alert firing and recovery are unobserved.

## Gap chosen

Trust-on-first-use: initial publication needs second-person reconciliation, which has no tool. Slice 1 adds a read-only `--reconcile` check. Remaining owner or hosted steps cannot be done by code in this worktree.

## Stacked slices

1. This slice: offline reconcile aid (src/orchestrator only).
2. Owner decision: retention days, then lock (infrastructure/deployment; coordinator gate).
3. Hosted evidence: deployed run, alert drill, recovery notes.
