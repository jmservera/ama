---
title: Issue 1830 live r9 changes (2026-11-23)
ms.date: 2026-11-23
---

Tier: FOCUSED. Basis: read-only analysis tool; no gate semantics, receipt scope or security control change. No live Azure; `rpi-checks.py --all` not run; no PR, so exact-head review and hosted CI were not observed.

Changes: `tools/rpi-gate-timing.py` (explicit null queue wait, refusal of malformed or reversed lock line), `tools/test_rpi_gate_timing.py` (two tests), [r9 note](../../docs/reference/research/issue-1830-live-r9-2026-11-23.md), README row, log entry. Validation: 59 unit tests OK; ruff check and format clean.

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Wall, queue wait, timing, critical path, high-cost and repeated checks | Partly proven | Fourteen receipts in r6; queue wait now explicit. Unproven: retained queue wait, same-head pair, redundant coverage |
| 2 | Preflight, rejections, non-receipt label, #1297 caught, #1828 rerun | Proven for the demo | r7 and r8 |
| 3 | Tests, docs, benchmark method, before and after | Partly proven | Tests added; no optimization, so no before and after |
| 4 | Dated artifacts, tier, exact-head review, hosted CI | Owner-gated | Artifacts and tier done; review and CI need a PR, forbidden |
