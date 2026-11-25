# Issue 1837 research, 2026-11-25 (live demo pass)

Refs #1837. Base `5bac4d3ff3`. Synthetic demo, desktop only. Research disposition: executed (source read) plus reused (prior records 2026-11-18 to 2026-11-23 r2).

## Findings

* The standalone route page posts JSON with the `X-ZF-CSRF` header via `/nomination-routes.js`; the HTTP 400 defect is fixed on main (earlier records, failing-first run at 9da3fcd).
* Negative coverage in `src/api/tests/test_nomination_api_routes.py` (unauthenticated, wrong role, malformed, cross-case, native urlencoded refusal, trusted-proxy missing CSRF header) exercises only `nomination_acknowledge`.
* `nomination_correct` and `challenge_open` share the `/resident` endpoint but have no negative test for the same boundaries. This is the concrete test gap for the criterion "negative tests preserve authorization, case isolation, malformed-input and same-origin/CSRF boundaries".
* Live: apps `ca-cutover-test-demo-api` and `ca-resident-demo` were verified in the 2026-11-23 r2 record; live writes would add irreversible records to the shared demo, so write proofs stay local.

## Planning Readiness

Ready. Add one focused API test for correction and challenge negatives; no src change expected (tier: focused, test-only). If the test reveals a defect, src changes and the FULL tier apply.
