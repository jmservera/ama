---
title: Issue 1830 live r7 changes (2026-11-22)
ms.date: 2026-11-22
---

Tier: FOCUSED, documentation only. Added [r7 note](../../docs/reference/research/issue-1830-live-r7-2026-11-22.md), a README row and a log entry. No `src/` or `tools/` change; no live Azure; `rpi-checks.py --all` not run; no PR, so independent exact-head review and hosted CI were not observed. Validation: 56 unit tests OK, preflight selectors, direct 320px replay and map check. Temporary files removed.

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Wall, queue wait, timing, critical path, high-cost and repeated checks | Partly proven | Fourteen receipts in r6. Unproven: queue wait, same-head and base pair, redundant coverage |
| 2 | Exact-selector preflight, invalid input rejected, non-receipt label, #1297 caught, #1828 rerun | Proven for the demo | Original #1297 defect fails at `18d3de459f` (1637.4 over 1600) and passes at head; map check passes in 31 s |
| 3 | Tests, docs, benchmark method with before and after | Partly proven | Tests and docs pass; no optimization, so no before and after |
| 4 | Dated artifacts, tier, exact-head review, hosted CI | Partly proven | Artifacts and tier done; review and CI need a PR, forbidden here |
