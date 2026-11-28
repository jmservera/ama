---
title: Issue 1830 live r18 changes (2026-11-27)
ms.date: 2026-11-27
---

Tier: FULL by doubt (gate tool edit). Planned: `critical_chain` predecessor filter in `tools/rpi-gate-timing.py`; one test in `tools/test_rpi_gate_timing.py`; research note, README row, log entry. Final changes and the per-criterion table are appended after implementation.

Final changes: `tools/rpi-gate-timing.py` (`critical_chain` strict `(end, start)` predecessor ordering), `tools/test_rpi_gate_timing.py` (one test), research note, README row, log entry. Evidence: reproduced hang, 25 tests OK, new test fails without the fix, ruff clean.

Not run: `rpi-checks.py --all`, hosted CI, independent exact-head review. No live Azure, no push or PR.

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Wall, queue wait, timing, critical path, high-cost and redundant checks | Partly proven | Analyzer hardened (hang fixed). Unproven: multi-receipt measurement; the only retained receipts (`/tmp/r2188`, `/tmp/r2188t`) are partial or unsealed and are refused; the cited receipt is gone |
| 2 | Preflight, rejections, non-receipt label, #1297 caught, #1828 rerun | Proven for the demo | Earlier rounds r7, r15, r16; not re-run |
| 3 | Tests, docs, benchmark method, before and after | Partly proven | Tests and docs exist; no gate optimization implemented, so no gate before and after |
| 4 | Dated artifacts, tier, exact-head review, hosted CI | Owner-gated | Artifacts and FULL-by-doubt tier recorded; independent review and hosted CI need a PR, forbidden here |
