---
title: Critique for issue 2164 live r10
ms.date: 2026-11-23
---

Executed once. Verdict: proceed. The fix only tightens a fail-closed check and cannot widen access. Risk: legitimate bound staff with tenant-less rows must still pass, so the helper reuses `identity.legacy_tenant`, the same rule `identity.matches` used to bind them. Tests must cover that legitimate case. Because `src` changes, the tier is FULL; `rpi-checks.py --all` is not run by this worker (the coordinator runs gates).
