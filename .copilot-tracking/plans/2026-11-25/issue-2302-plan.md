# Issue 2302 plan (2026-11-25)

* [x] Phase 1: live Playwright proof of the Overview card (criterion 1).
* [ ] Phase 2: add wire-to-render test in `src/api/tests/test_overview_ai_economics_100.py`: real `/api/stats` body (accepted outcome present, no price source) through `aiEconomicsRows`; assert denominators and all costs Unknown. Mutation-check it fails if the server key drifts.
* [ ] Phase 3: research note with per-criterion table; changes and review records; commit.

Tier: FULL class (src test change only, no src code); coordinator owns the gate.
