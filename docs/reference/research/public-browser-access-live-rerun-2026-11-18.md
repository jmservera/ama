---
title: Public Browser Access on the Deployed Demo, Rerun (Issue 344)
description: Second live pass for issue 344 with curl, Playwright and read-only Azure evidence, adding the policy exemption check and a per-criterion proven and unproven table
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

Refs #344. This pass repeats and extends the [first live note](public-browser-access-live-demo-2026-11-18.md); related results are in [#349](entra-signin-live-demo-2026-11-18.md), [#350](deployed-parity-live-2026-11-18.md) and [#360](direct-ingress-live-demo-2026-11-18.md).

## Scope and method

Owner decisions of 2026-11-18: synthetic demo, desktop only; live Azure authorised in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change); billing reconciliation, DPO and Legal approval and person-run assistive-technology testing not needed. Target: `ca-cutover-test-demo-api`. Azure CLI use was read-only, so no resource was created and nothing needs deleting. Credentials were read from the owner's files at run time and never printed; a literal scan of the retained evidence found no match. Playwright Chromium ran at 1366 by 900 around 11:30 UTC. Evidence is in `.copilot-tracking/evidence/2026-11-18/issue-344-live-rerun/`.

## Observations

| Observation | Result | Status versus first pass | Evidence |
| --- | --- | --- | --- |
| Anonymous curl | `/healthz`, `/`, `/welcome.html` 200; `/api/me`, `/api/cases`, `/app`, `/workspace-shell.js` 401; HTTP gets 301 to HTTPS | Reproduced | `anon-curl.txt` |
| Browser-style anonymous API request | Browser User-Agent with `Accept: application/json` gets 302 to Entra; in-page `fetch` follows the same redirect | Reproduced (adverse) | `anon-curl.txt`, `access_proof.json` |
| Landing and sign-in action | Landing 200 "Welcome to Zava Forward"; clicking sign-in reaches `login.microsoftonline.com` | Reproduced | `access_proof.json`, `../../../.copilot-tracking/evidence/2026-11-18/issue-344-live/1-landing-anonymous.png` (reused from the first pass; the rerun capture was byte-identical and removed), `2-entra-signin-page.png` (Entra page shell only, the sign-in prompt had not rendered; the redirect itself rests on the URL recorded in `access_proof.json`) |
| Test-account sign-in | Returns to `/app` titled "Zava Forward" | Reproduced | `3-workbench-after-signin.png` |
| Authenticated reachability | 11 of 11 assets 200; 22 of 25 API routes 200; `/api/law` and `/api/account/photo` 503; `/api/time/status` 500 | Reproduced | `access_proof.json` |
| `/api/time/status` cause | Generic unexpected-error body; log output empty, no raw log retained | Cause unknown | `access_proof.json`, `time-status-logs.txt` |
| SQL `sql-cutover-test-rzsrg` | Public network access Disabled, 0 firewall rules, one private endpoint connection Approved, TLS 1.2 | Reproduced | `sql.json`, `sql-fw-count.txt`, `sql-pe.json` |
| Policy exemptions | 0 at subscription scope, 0 at `ama` scope; no resource-group assignments | New | `policy-exemptions-*.txt`, `policy-assign-rg.json` |
| Policy compliance for SQL | Audit-effect assignments `SQL_Auditing_Audit` and `SQL_ThreatDetection_Audit` (from `MCAPSGovAuditPolicies`) are NonCompliant; they audit and do not block | New (adverse) | `policy-sql-state.json` |

## Per-criterion status

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Public HTTPS landing; sign-in starts Entra; protected pages need Entra; anonymous API 401 not a redirect | Partly proven | All parts shown except that browser-style API requests are redirected by Easy Auth. Unproven until the owner accepts the redirect or the platform is changed |
| 2 | Public edge follows #143 | Already ticked | External Container Apps environment (see #360) |
| 3 | `/healthz` public; anonymous protected API 401 | Proven for non-browser clients | Same 302 caveat for browser-style calls |
| 4 | SQL private, public access Disabled, no policy bypass | Proven for the demo server | The exemption count of 0 closes the bypass gap; the audit-only SQL policy findings are recorded, not hidden |
| 5 | Parity with the matrix, gaps filed | Partly proven | Reachability only. Write flows, AI, documents and chat are not covered here (see #350 and #360). `/api/time/status` 500 needs a filed defect or diagnosis |
| 6 | Browser sign-in smoke recorded | Already ticked; refreshed | Passed again with the test account, not a named real user |

No checkbox was changed; the owner ticks.

## Evidence limits

* `time-status-logs.txt` and `policy-state.err` are empty files; the absence of console lines for `/api/time/status` is a claim with no raw log retained.
* The tenant id in the Entra redirect URL is replaced with `<tenant-id>` in `anon-curl.txt`.
* The first-pass state file is unchanged; this pass has its own `issue-344-live-rerun-state.json`.
