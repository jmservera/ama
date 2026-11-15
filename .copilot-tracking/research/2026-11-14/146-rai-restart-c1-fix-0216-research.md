# C1 research: PR #1600 src-api failures
* Failure 1: new route /api/assistants/rai-metrics missing from the role inventory GET_ENDPOINTS (test_role_endpoint_inventory).
* Failure 2: rai_metrics returns insufficient only for zero events in the window. The default 1-day window held events seeded by complete_release_fixtures in test_continuity_epoch_export.HttpTests, which inherits test_assistants.ApiTests, so the test asserted fixture-dependent state. No production defect.
* Planning readiness: Ready.
