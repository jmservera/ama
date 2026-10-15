---
title: Transactional hazard hold review follow-up evidence
description: Reused review reproduction and inspected store transaction contract
ms.date: 2026-10-15
---

## Identity and Readiness

Task: hazard-hold-rv001, parent src-hazard-referral-85, issue 85, PR 314.
Research disposition: reused. Planning Readiness: Ready.
The user explicitly selected RV-001 correction and RV-002 honest documentation.

## Evidence

* Prior canonical review:
  .copilot-tracking/reviews/logs/2026-10-15/src-hazard-referral-85-review.md.
  Its two-store reproduction commits emergency intake between the early guard
  and work-order completion.
* SqlStore.save skips unchanged case bodies, so procurement-only writes do not
  validate the dependent case version. _SyncLock only synchronizes at entry.
* Existing save transaction serializes writers: SQLite write transaction;
  MssqlStore adapter translates the existing begin to a transaction-owned
  exclusive application lock. Both use case rowversion and ConflictError.
* All eight explicit procurement/quality/signoff guards use
  require_safety_clear. Installation advancement also has a hazard gate and a
  touched case; include it explicitly in the shared dependency registration.
* On refusal, pending audit, case edits and procurement edits must be discarded.
  Otherwise outer lock exit can incorrectly append a refused completion event.
* origin/main conflicted only in docs/reference/log.md. Merged main, resolved
  with python3 /tmp/reslog.py docs/reference/log.md, preserving both logs.

## Boundaries

No new SQL dialect, schema, workload dependency, authority or deadline policy.
Actual SQL Server/Azure, verified repairs transport and human acceptance remain
unproved. Existing acceptance boxes remain unticked.
