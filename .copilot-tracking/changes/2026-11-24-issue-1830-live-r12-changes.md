---
title: Issue 1830 live r12 changes (2026-11-24)
ms.date: 2026-11-24
---

Tier: FULL, because `src/api/checks/map_fullscreen_browser_check.py` changed. Local checks run: 62 timing and preflight tests, preflight accept and reject, ruff check and format, mypy in `src/api`, six direct map check reruns (all pass, load 9 to 12). Not run: `rpi-checks.py --all`, hosted CI, exact-head independent review. No live Azure; no push or PR.

Final changes: 1 px tolerance on the tile containment test in the map check; [r12 note](../../docs/reference/research/issue-1830-live-r12-2026-11-24.md); README row; log entry.

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Wall, queue wait, timing, critical path, high-cost and repeated checks | Partly proven | r6 (fourteen receipts), r9. Unproven: retained queue wait logs, same-head pair, redundant coverage; not rechecked in r12 |
| 2 | Preflight, rejections, non-receipt label, #1297 caught, #1828 rerun | Proven for the demo, one gap | Rejections and label re-run at head; #1297 replay from r7; map check passes 6 of 6 after the fix at load 9 to 12. Unproven: behaviour at load above 20 |
| 3 | Tests, docs, benchmark method, before and after | Partly proven | Tests and docs exist; no optimization, so no before and after |
| 4 | Dated artifacts, tier, exact-head review, hosted CI | Owner-gated | Artifacts and tier done; review and CI need a PR, forbidden here |
