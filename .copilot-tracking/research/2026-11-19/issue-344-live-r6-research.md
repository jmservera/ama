# Research r6, issue 344 (live)

Refs #344. Demo, desktop only. Disposition: executed. Planning Readiness: Ready (stop decision).

* Unticked criteria: 1, 3, 4, 5 (2 and 6 already ticked).
* Easy Auth on `ca-cutover-test-demo-api` is `RedirectToLoginPage` (read-only `az containerapp auth show`); the Return401 mode is the opt-in `entraBearerOnly` Bicep switch (`infra/modules/containerapps.bicep` line 302). A fix is an infra change and redeploy, so FULL tier; stop per brief.
* New live fact: `/api/time/status` 500 is an app `ProgrammingError` (database driver) raised from `exceptions.py:583` on three of three calls; `/api/me` 200 in the same session. Cause is in the SQL data plane (table or permission), so SQL scope; FULL tier.
* Evidence: `.copilot-tracking/evidence/2026-11-19/issue-344-live-r6/`.
