---
title: Issue 350 live research (2026-11-23)
---

Research disposition: executed. Planning Readiness: Ready.

Scope: the ten unticked criteria of #350 against main (HEAD 342fad401d; `src/` identical to origin/main ed9500a188) and live revisions api `ca-cutover-test-demo-api--0000054` (image sha256:3f2be664, created 2026-11-22 23:14 UTC) and resident `ca-resident-demo--0000026`.

Findings (raw evidence in docs/reference/research/issue-350-live-r6-2026-11-23/raw/):

* Edge unchanged: native 401, browser 302 on `/api/*`, `unauthenticatedClientAction` RedirectToLoginPage. The app-side regression `test_auth.test_anonymous_api_is_401_for_browser_style_requests_and_pages_still_redirect` passes on main.
* Staff sign-in works (Retrofit Programme Manager); 28 GET probes give the same shape as run 5: 443 open, 537 completed, 601 work orders, 167 funding, ledger 5976 entries intact; law store configured with 0 sources; photo 503; time capture off with explanation.
* New: the audit job log of 2026-11-22 02:00 shows `LEDGER_DIGEST_OK` with 4 immutable digests verified; `digests_checked` 0 on the API is by design (API reads the local `ZF_DIGEST_DIR`, the job verifies the `ledger-digests` blobs). No code defect found.
* Resident app: root and healthz 200, no staff API; resident sign-in not exercisable from this host.
