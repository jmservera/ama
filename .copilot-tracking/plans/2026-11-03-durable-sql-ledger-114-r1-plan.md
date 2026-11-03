---
title: Issue 114 round 1 plan
ms.date: 2026-11-03
---

* [x] Make verify_years fail closed on malformed, duplicate or unreadable year digests; report sealed_years
* [x] read_year_digests returns an unreadable stub; digest_blob upload skips stubs
* [x] Tests in test_recovery.py; README note
* [x] Run unit tests, ruff, mypy (cache /tmp/mypy-114)

Details: [details](../details/2026-11-03-durable-sql-ledger-114-r1-details.md)

Stacked slices after this one (need Azure access, not started): Azure SQL load and cost run; Azure SQL point-in-time restore drill with reapply_deletions; annual verify against real Blob anchors.

## Critique (executed once)

Verdict: compatible. Fail-closed is the safe direction; no behaviour change for valid digests. Applied directly.

Tier: focused. The slice touches the tamper-evident audit verifier (security-sensitive), so the complete gate would apply to publication; it was not run here and is left to the coordinator.
