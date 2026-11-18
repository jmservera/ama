---
title: Public Browser Access on the Deployed Demo, Third Pass (Issue 344)
description: Third live pass for issue 344 adding the server-side cause class of the /api/time/status 500 and a per-criterion proven and unproven table
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

Refs #344. This pass repeats the [first](public-browser-access-live-demo-2026-11-18.md) and [second](public-browser-access-live-rerun-2026-11-18.md) live notes and closes one of their open items.

## Scope and method

Owner decisions of 2026-11-18: synthetic demo, desktop only; live Azure authorised in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change). Target: `ca-cutover-test-demo-api`, revision `ca-cutover-test-demo-api--0000031`. Azure CLI use was read-only; no resource was created, so nothing needs deleting. Credentials were read from the owner's files at run time and never printed. Playwright Chromium ran at 1366 by 900 around 14:16 UTC. Evidence is in `.copilot-tracking/evidence/2026-11-18/issue-344-live-r3/`.

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Anonymous curl | `/healthz`, `/`, `/welcome.html` 200; `/api/me`, `/api/cases`, `/app`, `/workspace-shell.js`, `/api/time/status` 401; HTTP gets 301; `X-Requested-With: XMLHttpRequest` gets 403; invalid bearer gets 401 | `anon-curl.txt` |
| Browser-style anonymous API request | Browser User-Agent with `Accept: application/json` gets 302; in-page `fetch` (default, JSON and HTML Accept) is redirected in all three cases; `/healthz` 200 | `anon-curl.txt`, `access_proof.json` |
| Landing and sign-in | Landing 200, "Welcome to Zava Forward"; clicking `/sign-in` reaches `login.microsoftonline.com` and the sign-in field appears | `access_proof.json`, `1-landing-anonymous.png`; the Entra sign-in screenshot was blank while loading and is not retained, so the URL and field wait in the JSON carry the proof |
| Test-account sign-in | Returns to `/app` titled "Zava Forward"; `/api/me` 200 | `access_proof.json`; the workbench screenshot showed staff names and is not retained |
| Authenticated reachability | 11 of 11 assets 200; 22 of 25 API routes 200; `/api/law` 503 and `/api/account/photo` 503 (services not configured, as before); `/api/time/status` 500 | `access_proof.json` |
| `/api/time/status` cause | Container log shows `http-error GET /api/time/status status=500 exc=ProgrammingError` at the database layer, twice on each request. This is a database-side error class (for example a missing object or column), not an auth or edge fault. The exact object was not read; only the log line is retained | `time-status-logs.txt` |
| Easy Auth | Enabled, `RedirectToLoginPage`; excluded paths `/healthz`, `/readyz`, `/`, `/welcome.html`, `/style.css`, `/zava-logo.png`, `/sign-in` | `auth.json` |
| Edge | External Container Apps environment (`internal` false, public network access Enabled) | `env.json` |
| SQL `sql-cutover-test-rzsrg` | Public network access Disabled, 0 firewall rules, TLS 1.2 | `sql.json`, `sql-fw-count.txt` |

The earlier policy exemption result (0 exemptions at subscription and `ama` scope) and private endpoint approval were not re-run; they stand from the second pass.

## Per-criterion status

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Public HTTPS landing; sign-in starts Entra; protected pages need Entra; anonymous API 401 not a redirect | Partly proven | Landing, Entra start and protected-page gating proven. Anonymous non-browser API calls return 401; browser-style calls (browser User-Agent or in-page fetch) are redirected with 302, so the "not a redirect" clause is unproven for browsers until Easy Auth behaviour is changed or the owner accepts it. No production change was made |
| 2 | Public edge follows #143 | Already ticked | External environment, no Front Door on the demo |
| 3 | `/healthz` public; protected API 401 to anonymous API calls | Proven for non-browser clients | Same redirect caveat |
| 4 | SQL private, public access Disabled, no policy bypass | Proven for the demo server | Disabled, 0 firewall rules; zero exemptions from pass 2 |
| 5 | Parity check against the matrix, gaps listed and filed | Partly proven | Reachability only. `/api/time/status` 500 is now classed as a database-side `ProgrammingError`; no issue could be found by search, and none was filed because this worker may not write to shared systems. Write flows, AI, documents and chat are covered by #350 and #360 |
| 6 | Browser sign-in smoke recorded | Already ticked; refreshed | Passed with the test account, not a named real user |

No checkbox was changed; the owner ticks.

## Evidence limits

* The Entra screenshot was a blank loading card and is not retained; the proof is the recorded URL and field wait.
* The log excerpt is the filtered tail of the console stream, not a full export.
* The tenant id in the redirect URL is replaced with `<tenant-id>`.
