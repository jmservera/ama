---
title: Issue 1830 live r13 changes (2026-11-24)
ms.date: 2026-11-24
---

Tier: FULL, because `src/api/checks/design_system_browser_check.py` changed. Local checks run: 62 timing and preflight tests, preflight accept and reject (invalid selector, zero-test module, path escape), ruff check and format, mypy in `src/api`, direct map check (2 of 2 before, 1 of 1 after), `test_browser_harness_scratch`, `test_epic149_ux_evidence_results`, `test_content_standard` through preflight. Not run: `rpi-checks.py --all`, hosted CI, exact-head independent review. No live Azure; no push or PR.

Final changes: owned-server health wait is a 60 s monotonic deadline instead of 100 polls (about 10 s); [r13 note](../../docs/reference/research/issue-1830-live-r13-2026-11-24.md); README row; log entry. The r12 failure under load 33 to 42 was not reproduced under synthetic load, so there is no measured before and after.

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Wall, queue wait, timing, critical path, high-cost and repeated checks | Partly proven | r6 (fourteen receipts) and r9. Unproven: retained queue wait logs, same-head receipt pair, redundant-coverage candidates; not rechecked in r13 |
| 2 | Preflight, rejections, non-receipt label, #1297 caught, #1828 rerun | Proven for the demo | Rejections and label re-run at head in r13; #1297 replay from r7; map check passes at head. Unproven: behaviour at load above 20 |
| 3 | Tests, docs, benchmark method, before and after | Partly proven | Tests and docs exist; no gate optimization implemented, so no before and after; the health-window change is defensive and unmeasured |
| 4 | Dated artifacts, tier, exact-head review, hosted CI | Owner-gated | Artifacts and tier FULL done; independent review and hosted CI need a PR, forbidden here |
