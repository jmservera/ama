---
title: Issue 115 ledger digest live verification (demo)
description: Evidence that scheduled ledger digest verification is merged, tested and deployed on the synthetic demo, and what stays unproven
ms.date: 2026-11-22
ms.topic: reference
---

Refs #115. Scope: synthetic desktop demo, resource group `ama`, owner decisions of 2026-11-18. Azure use was read-only; nothing was created. No credentials were read or recorded.

## Result

Both acceptance criteria of #115 are already ticked. No source change was warranted.

| Criterion | Status | Evidence |
| --- | --- | --- |
| Digests land in an immutable container with a retention lock | Retention policy proven; lock unproven for the demo, deferred to production (#1908) | Container `ledger-digests` has a 365-day immutability policy in state Unlocked. Locking is irreversible and owner-deferred |
| Scheduled verification alerts on mismatch | Proven by tests and deployed configuration; no live mismatch drill (owner: no drills) | Tests below; job on a daily schedule; mismatch and missing-run alerts enabled |

## Commands and outputs

* From `src/core`: `PYTHONPATH=src:tests python3 -m unittest test_ledger_digest_blob -q`: 22 tests OK.
* From `src/orchestrator`: `PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest test_digest_blob -q`: 31 tests OK.
* `az containerapp job show -g ama -n job-cutover-test-demo-audit`: command `python -m zava_forward.orchestrator.digest_blob --publish`, cron `0 2 * * *`. Digest settings: container `ledger-digests`, `ZF_DIGEST_REQUIRE_RETENTION_LOCK=false`, `ZF_DIGEST_MIN_RETENTION_DAYS=365`.
* `az containerapp job execution list`: 2026-11-22T02:00 Succeeded; 2026-11-21T19:25 Succeeded; 2026-11-21T19:23 Failed (earlier manual run, not investigated here).
* `az storage container immutability-policy show`: `immutabilityPeriodSinceCreationInDays` 365, `state` Unlocked. Container reports an immutability policy and version-level immutability disabled.
* `az monitor scheduled-query list`: `alert-cutover-test-demo-ledger-digest-mismatch` and `alert-cutover-test-demo-ledger-verify-missing` enabled. The mismatch alert (severity 1, hourly) matches `LEDGER_DIGEST_ALERT` in the job console logs.
* Storage account `stcutovertestrzsrg`: public blob access disabled.

## Unproven for the demo

* Irreversible lock and owner-approved retention duration (production, #1908).
* End-to-end alert firing on a real mismatch, because drills are not authorised.
* Live data holds one calendar year, so sealed-year digests are not exercised (see issue 114 re-verification).
