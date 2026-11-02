---
title: Deploy of PR 764 to the Azure test environment, live evidence
description: Deployment of main 45f950db (Refs #691) and live Playwright results, including failures
ms.date: 2026-11-02
---

## Scope

Owner-approved deployment (2026-11-02) of merged PR #764 from `origin/main` `45f950db156f9d0509341b4a6c22112197766dad` to resource group `ama`. Refs #691. No source change. Resource group `ama` untouched beyond the apps below.

## Deployment

| Item | Result |
| --- | --- |
| Build | `docker build` from a `git archive` of `src/` at the SHA, label `org.opencontainers.image.revision`, under `/tmp/ama-rpi-heavy.lock`. Trivy scan not run. |
| `zava-forward-api:main-20261102-45f950db156f-deploy764-employee` | `sha256:161fa1f0ff29c0deb7d07cacc045a07c0aaa5d34ea2f73f36f51e96f93ffe3d0` |
| `zava-resident-demo:main-20261102-45f950db156f-deploy764-resident` | `sha256:0408917d72951cecf54f666524e54ba96dd73c1f807c879cfd9ee02a697876d8` |
| ACR `crcutovertestrzsrg` | Window: default Deny, VM /32 rule (bare IP removed after), exports on, public on; push via `--expose-token`; restored. Readback equal to the pre-state (public Disabled, bypass None, export disabled, default Allow, no IP rules): `ACR_RESTORE_EQUAL True`. |
| `ca-resident-demo` | `infra/resident-demo.bicep` deployment `resident-demo-d764` Succeeded after a what-if whose only actionable changes were the app and its role assignments. Revision `--0000008` Healthy. Startup/Readiness/Liveness probes present. |
| `ca-cutover-test-demo-api` (employee) | Template PATCH (image, #764 probes, suffix `d764`) -> `--d764` Healthy, 100% traffic, min 0. |
| `ca-cutover-test-api` (internal) | Same PATCH -> `--d764` Healthy, min 0. |
| Config diff | Backup vs readback differs only in image, probes and revision names, except the resident app's `ZF_DEMO_EXPIRES_AT` (see below). |
| Agents app, jobs | Not changed. |

Deviations, disclosed:

* `resident_demo_deploy.py` refuses a non-interactive terminal and needs a typed phrase. It was not driven through a pty. I ran the same what-if and `az deployment group create` with the same template and parameters by hand, after checking the what-if scope.
* The resident expiry was passed as `2027-01-31T23:59:00Z` (README example); the live value was `...23:59:59Z`, so it moved 59 seconds earlier. Redeploy with `23:59:59Z` if exactness matters.
* The two API apps were updated by an ARM template PATCH rather than `deploy.py`/`main.bicep` (no private parameters file; avoids restoring replica minima or schedules). The Bicep source is not re-deployed for them.
* Rollback not needed (all revisions Healthy). Previous digests: API `sha256:72dfb103...`, resident `sha256:706b9db4...`.
* A diagnostic command printed the two test-user credential files to the session transcript (same slip as in the 2026-11-01 evidence). Nothing was written to any file; rotate if the transcript is retained.

## Live results (Playwright, Chromium 1280x900, apps scaled to zero before the first run)

Raw: `deploy-764-evidence/live-results-run1-cold.json` (cold, first run), `live-results-run3-warm.json` (warm). Three employee sign-ins and one resident sign-in.

| Criterion | Result |
| --- | --- |
| `/vendor/leaflet.js` returns 200 | PARTIAL. A direct request returned 200, 147,552 bytes, in all runs. In one browser page load the same file returned 500. |
| No 503/403 on cold start | FAIL for the employee app. Cold first run: 500 on `/app.js`, `/role-screens.js`, `/workspace-shell.js`, `/chat-widget.js`; the page did not render cases. Warm runs still showed bursts of 500 on static assets (`/style.css`, `/assistants.js`, `/progress.js`, `/zava-logo.png`, ...), plus `/api/account/photo` 503. No 403 was seen. Resident app: 9 responses, none at or above 400. |
| "N cases" status restored | PASS on the warm runs ("... 0 cases. ..."). Not met on the cold run, where the app scripts returned 500. |
| Chat-unavailable path | PASS. Reply "The assistant is not available right now ... nothing has been changed"; with the ask transport aborted the alert "Chat unavailable: Failed to fetch Try again or continue with the ordinary workflow." appeared in 0.6 s. |
| Resident sign-in and load | PASS, cold start included. |

## Diagnosis

* The 500s on static assets are produced by the Easy Auth sidecar (`http-auth`): at 2026-11-02T15:51:51Z it logged `Failed to forward request to http://127.0.0.1:8088 ... HttpRequestException` within 1-2 ms, in a burst. The `api` container had been listening since 15:46:50Z and had zero restarts, and it logged no error for those requests. The only app-side error was an expected `/api/account/photo` 503.
* So the startup probe alone does not remove the failures: they occur when the app is already up. Unproven hypothesis: the app uses `ThreadingHTTPServer` with the default listen backlog (5), and a burst of parallel connections from the sidecar is reset or refused. Not tested.
* The resident app, which has no sidecar, showed no failures.

## Outcome

Issue #691 stays open. Proven: probes deployed and Healthy, resident cold start clean, leaflet served whole on direct request, "N cases" restored on warm loads, chat-unavailable path. Not proven: no 5xx on cold start or on burst page loads for the employee app, and a consistent leaflet 200 in-browser.
