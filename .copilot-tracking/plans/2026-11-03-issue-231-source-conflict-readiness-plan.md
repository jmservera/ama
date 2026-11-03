# Plan: issue #231 slice 3, source conflicts block technical readiness

* [x] Add unresolved-conflict reasons to `technical-queue` in `role-screens.js`
* [x] Update `test_technical_quality_screens.py`: resolve the conflict in the ready fixture, add a blocking test
* [x] Extend browser story `231` and read panels after scrolling them into view (`role_screens_browser_check.py`)
* [x] Update the README story description
* [x] Run focused unit tests, ruff, mypy and browser stories `231` and `231q`

## Critique (one pass, inline)

Verdict: proceed. Findings applied: do not invent a staleness threshold; keep the screen read-only with no new controls; do not change the resolved-event meaning already shown in the Source facts table; keep criteria 5 unproven. No finding conflicted with a confirmed decision.
