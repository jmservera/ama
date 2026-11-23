# Issue 2257 r6 details

* `src/api/src/zava_forward/api/web/app.js`: in the `!res.ok` branch of `api()` add `e.gateway = body === undefined && startupFailure(res);`. In the map failure branch change the condition to `(!error.status || error.gateway)`.
* `src/api/tests/test_workspace_scripts.py`: a gateway error schedules one redraw; a JSON 500 does not.
* Web guidelines: no markup or styling change; behaviour only. Tier FULL (src changed); targeted tests only.
