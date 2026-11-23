---
title: Research for #2302 (second live run)
date: 2026-11-23
---

Disposition: executed. Planning Readiness: Ready.

## Findings

* Criteria 1 and 2 were already proven by the first run (`docs/reference/research/issue-2302-ai-economics-live-2026-11-23.md`, live revision 0000055 screenshot, 22 core and 5 API tests). Criterion 3 is a remote issue edit, which the worker does not perform.
* Gap in the renderer: `aiEconomicsRows` in `src/api/src/zava_forward/api/web/app.js` maps only numeric `0` to Unknown. The backend validator (`tokenomics.assert_tokenomics_invariants`) rejects zero strings such as "0.00", but the browser shows `USD 0.00` if a stale or non-conforming payload carries one. That breaks the Unknown-not-zero rule in the one place a manager reads it.
* Existing test `src/api/tests/test_overview_ai_economics_100.py` covers numeric zero only.

## Plan input

Treat zero-valued decimal strings as Unknown in the renderer; add one regression test. Tier FULL (src change), targeted tests only.
