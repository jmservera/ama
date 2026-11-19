# Issue 344 live r5 research (2026-11-19)

Refs #344. Disposition: reused. The fourth-pass note `docs/reference/research/public-browser-access-live-r4-2026-11-19.md` and its evidence are current for the demo.

* Criterion 1 (anonymous API 401, not a redirect, with browser sign-in kept): needs `unauthenticatedClientAction` change in `infra/modules/containerapps.bicep` line 302 plus redeploy, or an app-level sign-in flow. Infrastructure and deployment, so FULL tier.
* Criterion 3 shares the same clause.
* Criterion 4: proven for the demo server (earlier passes).
* Criterion 5: `/api/time/status` returns 500 on the deployed app. The handler `app.time.status` always queries the SQL store; cause is not visible because the container log tail shows no exception and reproducing needs a signed-in call. A fix would be a src change (FULL tier).
* Fresh read-only check: `az containerapp logs show --tail 300` on `ca-cutover-test-demo-api` revision 0000033 shows start-up lines only, no errors.
Planning Readiness: Ready (decision: stop).
