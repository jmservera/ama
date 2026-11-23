---
title: Issue 1830 live r8 changes (2026-11-23)
ms.date: 2026-11-23
---

Tier: FOCUSED, documentation only. Added [r8 note](../../docs/reference/research/issue-1830-live-r8-2026-11-23.md), a README row and a log entry. No `src/` or `tools/` change; no live Azure; `rpi-checks.py --all` not run; no PR, so independent exact-head review and hosted CI were not observed. Validation: 56 unit tests OK, preflight selectors, direct map and 320px journey checks PASS. Temporary files removed.

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Wall, queue wait, timing, critical path, high-cost and repeated checks | Partly proven | Fourteen receipts in r6. Unproven: queue wait, same-head and base pair, redundant coverage |
| 2 | Exact-selector preflight, rejections, non-receipt label, #1297 caught, #1828 rerun | Proven for the demo | Selectors and rejections re-run; r7 replay of #1297 at `18d3de459f`; map check passes in 36 s |
| 3 | Tests, docs, benchmark method with before and after | Partly proven | Tests and docs pass; no optimization, so no before and after |
| 4 | Dated artifacts, tier, exact-head review, hosted CI | Partly proven, owner-gated | Artifacts and tier done; review and CI need a PR, forbidden here |
