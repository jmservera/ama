---
title: Issue 1830 live r10 changes (2026-11-23)
ms.date: 2026-11-23
---

Tier: FOCUSED. Basis: read-only analysis tool; no gate semantics, receipt scope or security control change. No live Azure; `rpi-checks.py --all` not run; no PR, so exact-head review and hosted CI were not observed.

Changes (in progress): `tools/rpi-gate-timing.py` refuses malformed receipt bodies with exit 2; two tests in `tools/test_rpi_gate_timing.py`.

Final changes: `tools/rpi-gate-timing.py` (JSON, object, command-field, timezone and ordering validation), `tools/test_rpi_gate_timing.py` (two tests), [r10 note](../../docs/reference/research/issue-1830-live-r10-2026-11-23.md), README row, log entry. Validation: 22 timing tests OK (6 fail without the fix); ruff check and format clean.

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Wall, queue wait, timing, critical path, high-cost and repeated checks | Partly proven | r6 (fourteen receipts), r9 queue wait. Unproven: retained queue wait logs, same-head pair, redundant coverage |
| 2 | Preflight, rejections, non-receipt label, #1297 caught, #1828 rerun | Proven for the demo | r7 and r8 |
| 3 | Tests, docs, benchmark method, before and after | Partly proven | Tests added; no optimization, so no before and after |
| 4 | Dated artifacts, tier, exact-head review, hosted CI | Owner-gated | Artifacts and tier done; review and CI need a PR, forbidden |
