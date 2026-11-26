---
title: Issue 1830 live r14 changes (2026-11-25)
ms.date: 2026-11-25
---

Tier: FULL, because `src/api/checks/map_fullscreen_browser_check.py` changed (one `settle_map_reads(page)` call before the expanded-width axe scan). Local checks: 62 timing and preflight tests, preflight accept and reject, ruff check and format, mypy in `src/api`, 18 of 18 parallel map-check runs after (5 of 30 instrumented parallel runs failed before). Not run: `rpi-checks.py --all`, hosted CI, exact-head independent review. Witness note: implement-start recorded a qualification because the one-line edit landed at the same moment as the witness call. No live Azure, no push or PR. Note: [r14](../../../docs/reference/research/issue-1830-live-r14-2026-11-25.md).

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Wall, queue wait, per-command timing, critical path, high-cost and repeated checks | Partly proven | r6 (fourteen receipts) and r9 analyses via `tools/rpi-gate-timing.py`. Unproven: retained queue-wait logs, a same-head receipt pair, redundant-coverage candidates; not rechecked in r14 |
| 2 | Preflight entry point, rejections, non-receipt label, #1297 caught, #1828 rerun | Proven for the demo | Accept, label and rejections (invalid selector, zero-test module, path escape) re-run at head in r14; #1297 replay from r7; #1828 map check reruns directly and its intermittent failures were found and reduced to 0 of 18. Unproven: the 390x568 focus-fit flake cause |
| 3 | Tests, docs, benchmark method, before and after for an optimization | Partly proven | 62 tests and docs exist; no gate optimization implemented, so no gate before and after. The map-check change has a failure-rate before and after only |
| 4 | Dated artifacts, tier, exact-head review, hosted CI | Owner-gated | Artifacts and tier FULL done; independent review and hosted CI need a PR, forbidden here |
