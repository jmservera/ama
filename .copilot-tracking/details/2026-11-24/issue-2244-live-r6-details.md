---
title: Issue 2244 live run 6 details
ms.date: 2026-11-24
---

Source edits mirror commit b580955913 (another branch): `_rec_order_indexes_present` in both stores, `_recommendations_current` and an early return in `_migrate_recommendations`, an early return in `_ensure_queue_membership` when the `queue_context` meta equals the fingerprint, and an early return in `_seed` for a populated `cases` table. Test: `PopulatedStartupLockCountTests` appended to `test_mssql_startup_lock.py`; `_rec_order_indexes_present` bound in the stub class of `test_sqlstore.py`. Tier: FULL (src change); the coordinator runs the gate.
