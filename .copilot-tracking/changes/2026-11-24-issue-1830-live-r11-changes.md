---
title: Issue 1830 live r11 changes (2026-11-24)
ms.date: 2026-11-24
---

Tier: FULL, because `src/api/checks/map_fullscreen_browser_check.py` changed. Local checks run: 62 timing and preflight tests, ruff check and format, mypy in `src/api`, direct map check reruns. Not run: `rpi-checks.py --all` (the coordinator runs gates), hosted CI, exact-head independent review. No live Azure; no PR.

Final changes: three added `expect(card).not_to_contain_text("Loading sensor readings")` waits in `check_narrow_expand_reopen`; [r11 note](../../docs/reference/research/issue-1830-live-r11-2026-11-24.md); README row; log entry.

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Wall, queue wait, timing, critical path, high-cost and repeated checks | Partly proven | r6 (fourteen receipts), r9. Unproven: retained queue wait logs, same-head pair, redundant coverage; not rechecked in r11 (docs and receipt analysis) |
| 2 | Preflight, rejections, non-receipt label, #1297 caught, #1828 rerun | Proven for the demo with a residual | Rejections and label re-run at head; #1297 replay from r7; map check fixed and passes 3 of 4 reruns, with an unexplained 390x568 flake at load above 20 |
| 3 | Tests, docs, benchmark method, before and after | Partly proven | Tests and docs exist; no optimization, so no before and after |
| 4 | Dated artifacts, tier, exact-head review, hosted CI | Owner-gated | Artifacts and tier done; review and CI need a PR, forbidden here |
