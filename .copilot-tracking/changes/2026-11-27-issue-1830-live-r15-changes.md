---
title: Issue 1830 live r15 changes (2026-11-27)
ms.date: 2026-11-27
---

Tier: FULL, because `src/api/checks/map_fullscreen_browser_check.py` changed. Process note: the source edit was made during research, before the plan and this record were persisted; the witness `implement-start` call therefore post-dates the edit.

Final changes: filter-tile geometry is read after the layout is stable; research note [issue-1830-live-r15-2026-11-27.md](../../docs/reference/research/issue-1830-live-r15-2026-11-27.md); README row; log entry.

Not run: `rpi-checks.py --all`, hosted CI, independent exact-head review. No live Azure, no push or PR. GitHub GraphQL was rate limited; the issue was read through the REST API.

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Wall, queue wait, timing, critical path, high-cost and repeated checks | Partly proven | Receipts analysed in r6 (fourteen) and r9, not redone here. Unproven: retained queue-wait logs, a same-head receipt pair, redundant-coverage candidates; the cited `/tmp` receipt is gone |
| 2 | Preflight, rejections, non-receipt label, #1297 caught, #1828 rerun | Proven for the demo | Re-run at head: 62 tests, accept, three rejections, label. #1297 320px replay is from r7, not repeated. Direct map check passes 12 of 12 after the fix; 2 of 14 failed before. Unproven: behaviour at load above 20 |
| 3 | Tests, docs, benchmark method, before and after | Partly proven | Tests and docs exist; no gate optimization implemented, so no gate before and after. The check fix has a small before and after (2 of 14, 0 of 12) |
| 4 | Dated artifacts, tier, exact-head review, hosted CI | Owner-gated | Artifacts and tier FULL done; independent review and hosted CI need a PR, forbidden here |
