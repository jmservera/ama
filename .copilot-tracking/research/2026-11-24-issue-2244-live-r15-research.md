---
title: Issue 2244 live r15 research
ms.date: 2026-11-24
---

Task issue-2244-live. Research disposition: executed. Planning Readiness: Ready.

## Findings

* Earlier runs (r9 and before) left C4 unproven because a drill on the live database was excluded.
* New approach: a throwaway copy of the database (`tmp-2244-lockproof`, same server) plus three throwaway Container Apps jobs running the deployed API image with the API managed identity. A holder connection takes the global write lock; `MssqlStore` is opened concurrently. The live `retrofit` database is never touched.
* Baseline job (no holder): store opens in 23.7 s.
* Schema-current job with the lock held 45 s: `_migrate` (called from `_initialize`, `BEGIN requested by execute < _migrate < _initialize`) still requested the write lock, hit two 15 s timeouts, retried and opened in 46.6 to 46.9 s. The retry (C1) is proven live. The fast path (C2) is NOT complete: `SqlStore._migrate` takes the lock unconditionally and also rewrites `continuity_open_holds` (DELETE + INSERT) every start.
* Consequence: a writer holding the lock for more than about 211 s (8 attempts x 15 s timeout plus 1+2+4+8+16+30+30 s backoff) still crash-loops the API. This is a real residual defect against the issue's suggestion "skip the write lock when the schema is already current".
* The existing count test (`PopulatedStartupLockCountTests`) allows up to 2 begins on re-open, which hides this.

## Gap and decision

Add a read-only `_migrate_current` fast path for `MssqlStore._migrate`: derived columns present, rank policy and support encoding current, derived identity columns agree with bodies, and the continuity gate tables already match the continuity document. Anything unusual takes the locked path unchanged. Src change, so the full tier applies; the gate is the coordinator's job (no `rpi-checks.py --all` here).
