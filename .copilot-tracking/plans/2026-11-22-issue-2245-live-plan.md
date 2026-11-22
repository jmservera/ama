# Plan: issue 2245 and 2243

1. Add `AI_SUSPENDED` outcome; `chat_admission` returns it when the continuity block applies; `ChatModel` passes it through; panel shows hold-specific fallback and rules note; status disclaimer states the hold.
2. Replace the hard-coded resident EXPIRES check with `expires_at()` reading `ZF_DEMO_EXPIRES_AT`, fail closed.
3. Regression tests in `src/api/tests/test_chat_panel.py` and `test_resident_aoai.py`; run mypy, ruff, affected suites.
4. Build resident image, push via the guarded registry route, update `ca-resident-demo`, prove generative answers live; prove employee hold message live only if the employee image is rolled (decide by cost and risk).
5. Research note with per-criterion table; frozen commit.
