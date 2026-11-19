# Issue 1837 live research (opening)

Task: issue-1837-live. Refs #1837. Tier: FULL only if src changes; no full gate.

## Opening finding (before substantive search)

* `src/api/src/zava_forward/api/web/nomination-routes.js` (merged by #1878) already intercepts the three
  standalone forms and submits JSON with `X-ZF-CSRF: 1`. The issue was observed at `9da3fcd0`, before that script.
* `test_standalone_route_forms_submit_in_browser` exists in `src/api/tests/test_nomination_api_routes.py`.
* Hypothesis: the browser defect is already repaired on main; remaining gaps are negative tests, axe, live proof.

Research disposition: executed. Planning Readiness: pending details below.

## Findings

* Main (`cfd272051`) contains `web/nomination-routes.js` (added by #1878, merged 2026-11-18 00:50 +0100). It cancels the native submit and posts JSON with `X-ZF-CSRF: 1`. The server still reads JSON only (`server.py` `_body`), so a native urlencoded POST remains HTTP 400 `Could not read that.` by design.
* Server order in `do_POST`: body parse, sign-in, trusted-proxy `X-ZF-CSRF` check, role, then the resident handler. Accepting urlencoded bodies server side would let a cross-site HTML form post without the custom header only if the CSRF check were skipped; it is not, so a header-less urlencoded post would hit 403 in trusted-proxy mode. The client-side JSON bridge is therefore the smallest fix that keeps CSRF.
* Local: `python3 -m unittest tests.test_nomination_api_routes` ran 6 tests OK on main, including `test_standalone_route_forms_submit_in_browser` (three forms, statuses 200,200,200). That test asserts only the acknowledgement record afterwards; correction and challenge storage, urlencoded refusal and axe on the standalone page are not asserted.
* Live (deployed demo `ca-cutover-test-demo-api` revision 0000032, created 2026-11-18 16:20 UTC, Retrofit Programme Manager): `/nomination-routes.js` returns 404 and the routes page carries no script tag, so the deployed image predates the repaired source. Same-origin fetch probes (no writes, case unchanged): urlencoded with or without CSRF header 400; JSON without header 403 `Missing request header.`; malformed JSON 400; unknown case 404; body case differing from URL 400 (missing route fields). Record: `docs/reference/research/issue-1837-live-2026-11-18/live-negative-probe.json`.
* Not done live: creating a nomination record and submitting the three forms (the deployed image lacks the script, and redeploying is a production change that is not authorised). Not done: new Azure resources (none created).

## Planning Readiness

Ready. Plan: tests and a browser axe check only; no src change expected (tier FOCUSED-test-only; FULL not triggered by source because no src edit).
