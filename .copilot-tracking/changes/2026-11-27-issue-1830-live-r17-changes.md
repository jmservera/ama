---
title: Issue 1830 live r17 changes (2026-11-27)
ms.date: 2026-11-27
---

Tier: FULL by doubt (gate tool edit). Planned: `load_receipt` in `tools/rpi-gate-timing.py` refuses receipts lacking `jobs`, `image_cache` or an aware `sealed`; one test in `tools/test_rpi_gate_timing.py`; research note, README row, log entry. Final changes and the per-criterion table are appended after implementation.

Final changes: `tools/rpi-gate-timing.py` (`load_receipt` validates `jobs`, `image_cache`, `sealed`), `tools/test_rpi_gate_timing.py` (one test, 5 subtests), research note [issue-1830-live-r17-2026-11-27.md](../../docs/reference/research/issue-1830-live-r17-2026-11-27.md), README row, log entry. Evidence: traceback before, REFUSED exit 2 after; 24 timing tests OK; ruff format clean.

Not run: `rpi-checks.py --all`, hosted CI, independent exact-head review. No live Azure, no push or PR. Dependency on #1297 for `rpi-checks.py`/`src/README.md` is not touched this round (only the timing tool).

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Wall, queue wait, timing, critical path, high-cost and redundant checks | Partly proven | Analyzer and r6/r9 receipt analyses exist; this round hardens its input checks. Unproven: retained queue-wait logs, same-head receipt pair, redundant-coverage candidates; the cited `/tmp` receipt is gone |
| 2 | Preflight, rejections, non-receipt label, #1297 caught, #1828 rerun | Proven for the demo | Rejections and non-receipt label proven in r7, r15, r16; not re-run this round |
| 3 | Tests, docs, benchmark method, before and after | Partly proven | Focused tests and docs exist; no gate optimization implemented, so no gate before and after |
| 4 | Dated artifacts, tier, exact-head review, hosted CI | Owner-gated | Artifacts and FULL-by-doubt tier recorded; independent review and hosted CI need a PR, forbidden here |
