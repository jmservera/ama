# Issue 2302 research (2026-11-25)

Planning Readiness: Ready. Research disposition: executed.

* Renderer: `aiEconomicsCard` / `aiEconomicsRows` in `src/api/src/zava_forward/api/web/app.js`, mounted in `overviewView` from `/api/stats` `ai_consumption_economics`.
* Existing tests: `test_overview_ai_economics_100.py` (renderer fed hand-built dicts), `test_management_tokenomics_api_100.py` (HTTP JSON only), `test_management_tokenomics_invariant_100.py` (core).
* Gap: no test feeds the real HTTP `/api/stats` body into the real renderer, so a key rename or shape drift on either side would pass both suites.
* Live demo: Overview card shows denominators (3 proposals, 0 accepted, 59 metered, 0 unmetered, 3 unreviewed, 0 rejected) and every cost Unknown. See docs/reference/research/issue-2302-live-2026-11-25.md.
