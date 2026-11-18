---
title: Direct Container Apps ingress and sign-in on the deployed demo (issue 360)
description: Per-criterion proven and unproven results for the unticked acceptance criteria c, d and e of issue 360, measured live on the synthetic demo
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

Refs #360. Scope: the synthetic demo, desktop only, resource group `ama`. Owner decisions of 2026-11-18 apply: live Azure authorised (cap USD 700, no drills, no Key Vault rotation, no production change); Azure billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. Sign-in and parity results from [#349](entra-signin-live-demo-2026-11-18.md) and [#350](deployed-parity-live-2026-11-18.md) are cited, not repeated; the 2026-10-16 Front Door observations of #344 stay historical (see [cut-over evidence pack](../../architecture/cutover-evidence-pack.md)).

## Method and boundaries

* Checks ran 2026-11-18 08:36 to 08:42 UTC with Azure CLI under the existing login and Playwright Chromium at 1366 by 900. Credentials were read from the owner's files at run time and never printed; a literal scan of every retained evidence file for each credential value found no match (27 files, 0 hits).
* Evidence (scripts, raw outputs, three screenshots, earlier failed attempts) is in `.copilot-tracking/evidence/2026-11-18/issue-360-live/`.
* Azure access was read-only. The only writes were one throwaway chat thread per AI run in the synthetic demo database, each deleted through the app (`delete` returned 200). No Azure resource was created, so none needed deleting.

## Live configuration facts

| Fact | Observed | File |
| --- | --- | --- |
| Environment `cae-cutover-test-demo` | External (`internal` false), Succeeded, own subnet `snet-aca-demo` (10.40.6.0/23), Consumption profile | `env-demo.json`, `subnets.json` |
| Original environment `cae-cutover-test` | Still internal, public network disabled, own subnet `snet-aca` | `env-orig.json` |
| Subnet NSG `nsg-cutover-test-aca-demo` | `allow-internet-https-in` (443, priority 100) and `allow-vnet-in` | `nsg-demo.json` |
| Apps in the demo environment | `ca-cutover-test-demo-api` and `ca-resident-demo`: external ingress, `allowInsecure` false, minimum replicas 0 | `apps.json` |
| App settings | `ZF_STORE=mssql`, `ZF_AUTH=trusted-proxy`, `ZF_DEPLOYMENT_PROFILE=demo` | `app-env.json` |
| Easy Auth on the demo API | Enabled, `RedirectToLoginPage`, excluded paths `/healthz`, `/readyz`, `/`, `/welcome.html`, `/style.css`, `/zava-logo.png`, `/sign-in` | `auth.json` |
| SQL, Key Vault, storage, registry, Foundry (`aif-cutover-test-rzsrg`), IoT Hub | Public network access disabled (storage default action Deny, bypass None) | `sql.json`, `kv.json`, `storage.json`, `acr.json`, `foundry.json` |
| Adverse: Event Hub namespace `evhns-cutover-test-demo` | Public network access Enabled, default action Allow | `evh.json` |
| Adverse: Cognitive Services account `aoai-resident-469` | Public network access Enabled (a separate account, not the app's Foundry account) | `foundry.json` |
| Front Door | `az afd profile list`, `az network front-door list` and a type search for Cdn or FrontDoor resources in `ama` returned empty lists | `fd-resources.json` |

The Event Hub namespace and `aoai-resident-469` are outside the list of services that criterion a requires private (SQL, Key Vault, storage, registry, Foundry, IoT Hub), so they do not contradict it. They are recorded because the demo-only exposure was meant not to widen anything else; whether either is intended is an owner question.

## Criterion c: migration plan approved by the owner

Status: unproven; cannot be proven by an agent. The replacement environment and its apps already exist, so the replacement happened before this run (the issue's 2026-10-25 and 2026-10-31 comments and the infra runbook record the proposal and a bounded environment step). No record found in the repository or the issue shows the owner reviewing and approving the migration plan before that spend. The 2026-11-18 owner decision authorises live checks on the demo; it does not approve the plan retrospectively, and this run did not infer that it does. The box stays unticked until the owner records the approval.

## Criterion d: live direct HTTPS, sign-in, role, persistence and AI

| Element | Result | Evidence |
| --- | --- | --- |
| Direct HTTPS welcome and health 200 | Proven: `/healthz`, `/` and `/welcome.html` return 200 on the API app, `/healthz` and `/` on the resident app; TLS 1.3 with a Microsoft-issued certificate; plain HTTP gets 301 to HTTPS | `anonymous-curl.txt` |
| Anonymous protected API denied | Partly proven: non-browser requests get 401 on `/api/me`, `/api/cases`, `/app`; forged `X-ZF-Role`, forged principal headers and an invalid bearer token get 401 (`/api/me`, `/api/cases`). A request with a browser User-Agent and `Accept: application/json` still gets 302 to Entra, so the browser-mode 401 requirement fails (same as #350 item 1) | `anonymous-curl.txt`, `anonymous-denial.txt` |
| Real browser sign-in | Proven for the test account: `/app` redirects to `login.microsoftonline.com`, sign-in returns to the app origin and `/app` loads titled "Zava Forward | Zava North Homes" with the briefing and filters. Not a named real user (see #349) | `direct-signin-run7.json`, `1-welcome-anonymous.png`, `2-entra-redirect.png` (a blank card; the redirect host is shown only in `direct-signin-run7.json`), `3-workbench-signed-in.png` |
| Role enforcement | Partly proven: `/api/me` role `Retrofit Programme Manager`, app role `ZavaForward.ProgrammeManager`, `identity_source` `entra`; forged role and principal headers with a valid session leave the role unchanged; `/api/sensors` 403 for this role. Only one staff account exists, so denial for a second role is unproven | `direct-signin-run7.json` |
| SQL persistence | Proven for shared state, not for a restart drill: store is `mssql`; the load-balanced direct URL returned 443 open cases (two replicas exist, same revision, but each was not queried separately), matching #350 (443 open, 980 total). No restart or failover drill was run (excluded) | `replicas.json`, `direct-signin-run7.json` |
| AI call | Proven for the chat path: a case-grounded question in a throwaway thread returned an answer with `model_calls` 1, provider outcome `returned`, 1230 tokens in the first run, and the thread was deleted. A question without case context abstained with `model_calls` 0 (kept as run5). This is the demo-only chat activation; the five assistants stay release-denied (OQ-017, #350 item 4), which is a human release decision | `direct-signin-run5.json`, `direct-signin-run6.json`, `direct-signin-run7.json` |

Earlier attempts are kept: run 1 and 2 posted with Playwright's request client and got an empty 403 (the in-page fetch path with the `X-ZF-CSRF` header works, as a browser would), and run 3 showed the `unstored-ask` route refuses because chat storage is approved. Criterion d stays unticked because browser-mode 401 fails and real-user, second-role and restart persistence evidence is missing.

## Criterion e: Front Door retired after d, with owner authorisation

Status: unproven; nothing to retire and no authorisation on record. No Front Door, WAF or CDN resource exists in `ama` now, so the retirement outcome appears to hold, but the issue ties it to criterion d passing first and to explicit owner authorisation, and neither is recorded. Group `ama` exists and is `Succeeded`; this run changed nothing in it. The criterion stays unticked.

## Per-criterion summary

| Criterion | State on #360 | Result of this run |
| --- | --- | --- |
| a | Ticked | Not re-tested; live NSG, external environment and private backing services agree with it |
| b | Ticked | Not re-tested (offline tests) |
| c | Unticked | Unproven: owner approval not on record |
| d | Unticked | Partly proven: health, welcome, HTTPS, sign-in, role claim, shared SQL state and a real AI call; fails browser-mode 401; second role and restart persistence unproven |
| e | Unticked | Unproven: no Front Door resources found, but the authorisation and the order after d are not on record |
| f | Ticked | Not re-tested |

## Open follow-ups

* Decide the browser JSON API 302 versus 401 edge behaviour (#350 item 1).
* Owner: record migration approval (c) and Front Door retirement authorisation (e); confirm whether public access on `evhns-cutover-test-demo` and `aoai-resident-469` is intended.
* A second staff account with a different role for role denial; a deliberate restart check if a drill is later authorised.
