# Research: issue 344 live (2026-11-21)

Disposition: executed. Planning Readiness: Ready.

Prior passes: docs/reference/research/public-browser-access-live-r7-2026-11-19.md (and r3 to r6).

Live probes (2026-11-21 15:25Z, demo `ca-cutover-test-demo-api`, resource group `ama`, read-only Azure):

* anonymous `/healthz` 200, `/welcome.html` 200, `/api/me`, `/api/time/status`, `/app` 401, `/sign-in` 302 to `/.auth/login/aad`
* Playwright: landing 200, sign-in click reaches `login.microsoftonline.com`, test account returns to `/app`; in-page anonymous `fetch` of `/api/me` still ends in a redirect (Easy Auth `RedirectToLoginPage`)
* SQL `publicNetworkAccess` Disabled, 0 firewall rules, 0 policy assignments
* `/api/time/status` now 200 (r6 500 resolved); signed-in sweep of 11 assets and 25 API paths: all 200 except `/api/ai/report` 500 (FileNotFoundError, blocked per parity matrix #350), `/api/law` 503 and `/api/account/photo` 503 (blocked per matrix #350, #349, #210)
* New defect: `/api/handoffs/unaccepted` and `.csv` return 500. Deployed handoffs carry naive `offered_at` ("2026-10-13T09:00"); `handoff_ageing` raises ValueError, escaping `Store.unaccepted_handoffs`. Log: `ValueError at=workflows.py:393:handoff_ageing`.

Evidence: .copilot-tracking/evidence/2026-11-21/issue-344-live/ (probe.py, handoff_probe.json).
