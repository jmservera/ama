---
title: Changes for #2302 (third live run)
date: 2026-11-23
---

Files: `src/api/src/zava_forward/api/web/app.js` (`aiEconomicsRows` shows per-outcome costs as Unknown unless the accepted-outcome count is positive, and every cost as Unknown when `price_source_configured` is false) and `src/api/tests/test_overview_ai_economics_100.py` (new regression test).

Tier: FULL basis (src change); only targeted checks run. Ran, all OK: `test_overview_ai_economics_100` (6 tests; 4 fail without the `app.js` change), `test_accessibility_baseline` (18), `test_content_standard` (30), `test_management_tokenomics_api_100` (2), ruff check and format check, `mypy` in `src/api` (clean). Not run: `rpi-checks.py` (coordinator-owned), hosted CI, live Azure (change not deployed; first run's live proof stands).

## Per-criterion status

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Management view renders AI economics with denominators in the demo workbench | Proven (first run) | `docs/reference/research/issue-2302-ai-economics-live-2026-11-23.md`: live screenshot and payload on revision 0000055; `aiEconomicsCard` on Overview. This change is not deployed, so no new live proof |
| 2 | Test proves Unknown, not zero, with no price source or accepted-outcome count | Proven | `src/core/tests/test_management_tokenomics_invariant_100.py`, `src/api/tests/test_overview_ai_economics_100.py` (now incl. the two renderer rules) |
| 3 | Tick the criterion on #100 with the evidence path | Unproven | Remote issue edit left to the owner; evidence path in row 1 |
