---
title: Resident Synthetic Showcase Live Recheck (Issue #462)
description: Second 2026-11-18 live desktop and Azure check of the synthetic resident showcase, with retained evidence and a per-criterion proven/unproven table for the unticked #462 criteria
ms.date: 2026-11-18
---

## Scope and limits

This note records a second live pass over `ca-resident-demo` in resource group `ama` on 2026-11-18 (session `rpi-462-live`, task `issue-462-demo-recheck`), under the owner decisions of the same date: synthetic demo, desktop only, live Azure authorised (cap USD 700, no drills, no Key Vault rotation, no production change). Azure billing reconciliation, Legal and Data Protection Officer approval and person-run assistive-technology testing are not needed for the demo and are not claimed.

No source, infrastructure or Azure resource was changed and no throwaway resource was created. It is not a penetration test, a security acceptance, a production identity assessment or an accessibility acceptance. It supplements the [first live proof](./resident-showcase-live-proof-2026-11-18.md), the [2026-11-16 threat model](./resident-demo-threat-model-2026-11-16.md) and its [2026-11-17 update](./resident-demo-threat-model-update-2026-11-17.md), which stay unchanged.

Sign-in values were read at runtime from the owner files, were never printed, and the script asserts they appear in no retained output. The filled-form screenshot masks both fields; the signed-in page shows only the synthetic address.

Retained evidence, all under `.copilot-tracking/evidence/2026-11-18-resident-showcase-recheck/`: `live-checks.json`, `override-diagnosis.json`, `azure-app.json`, `azure-roles.json`, `azure-resident-resources.json`, `cost-by-service-oct1-nov18.json`, `cost-month-to-date.json`, the scripts `live_recheck.py` and `diagnose_overrides.py`, and five 1280x900 screenshots.

## Live browser and HTTP results

| Check | Result |
|-------|--------|
| HTTPS | Plain HTTP returns 301 to HTTPS; ingress `allowInsecure` is false |
| Sign-in page | Title "Your home improvement progress - synthetic showcase, not live"; banner says the shared sign-in does not prove identity and that Legal and DPO review is outstanding |
| Missing CSRF token; foreign `Origin` | 403 and 403 |
| Wrong password; unknown email | Both 401 with the identical body "We could not sign you in with those details."; no cookie set |
| Staff and probe routes (`/api/cases`, `/workbench`, `/api/staff`, `/admin`, `/demo/staff`, `/.env`) | All 404 |
| Unsigned view; forged cookie | 401 each; forged cookie reports signed out |
| Correct login in the browser UI | 200; page shows summary, status, timeline, documents, funding note, help, sensors and a "Not available in this showcase" panel (messages, uploads, downloads, appointments, consent, callbacks) |
| Cookies | `__Host-zfdemo`: Secure, HttpOnly, SameSite=Strict, path `/`, 1,795 seconds remaining on a 1,800 second lifetime. `__Host-zfdemo-csrf`: Secure, SameSite=Strict |
| Case binding | `/demo/view` returns 409 without or with a wrong `X-Resident-Session`. Query strings `case`, `case_id`, `email` and headers `X-Case-Id`, `X-Forwarded-User` change nothing; see the correction below |
| Projection | 18 top-level keys. One email-like string, equal to the signed-in fake address. Canary terms found: "password" once (the shared-demo-password notice), "phone" once ("shows no phone numbers or addresses"), "staff" five times ("Ask staff to check it"). No safeguarding, vulnerability, invoice, salary, IBAN, token, internal-note or date-of-birth term. This resolves the `phone` hit the first note left open |
| Write routes by GET | `/demo/logout`, `/demo/assistant`, `/demo/agenda` return 405 |
| Sign out | Account menu, Sign out: session reports signed out; `/demo/view` with the old session value returns 401 |
| Rate limit | In a fresh context the first of eight bad logins returned 401 and the rest 429. Earlier failures from the same source in the same run had already used the budget (limit 5 per source per 600 seconds), so this shows the limiter engages, not the exact count. It also blocked this session's correct login for about 25 minutes afterwards, which is the designed behaviour and an annoyance for repeated demo runs from one address |
| Security headers | `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Cache-Control` present. `Strict-Transport-Security` absent (observation; HTTPS is enforced by redirect and `__Host-` Secure cookies) |
| Password in page text or view JSON | Absent |

Correction to the first note: the same-signed-in-view comparison for the identity overrides is not byte-identical, because `sensors.freshness.age_seconds` grows with time. `override-diagnosis.json` compares each override with a baseline and finds that single path as the only difference, and that path also differs between two plain reads. The account email stays the signed-in address under every override.

## Azure facts (read-only, retained)

* Revision `ca-resident-demo--0000012`, running, 100 percent traffic, 0.25 CPU, 0.5 Gi, min 0 and max 1 replica, tags `workload=resident-demo` and `zava-forward-synthetic=true`. Image digest `sha256:65481780...bbbd19` in the private registry; the registry refused this session's tag read, so the source commit behind the digest is unconfirmed.
* Secrets are Container Apps secrets named `demo-password-verifier` and `demo-session-key` (Key Vault references); values were not read.
* Identity `id-resident-demo` holds AcrPull on the registry, Key Vault Secrets User on the two named secrets, and Cognitive Services OpenAI User on `aoai-resident-469`. No broad grant.
* Owned resources found by name: `ca-resident-demo`, `id-resident-demo`, `aoai-resident-469`. No throwaway resources exist or were created.
* Actual cost for `ama` (Cost Management, ActualCost): USD 440.90 from 2026-10-01 to 2026-11-18 and USD 89.15 month to date, so about USD 259 remains under the USD 700 cap. Largest lines: SQL Database 154.51, Virtual Network 71.11, Front Door 63.43, Container Apps 62.72, Container Registry 62.06. This run added no resource, so no new spend beyond a few seconds of scale-up. This is a read of actual cost, not a reconciliation, and not a forecast.
* Stop plan: scale to zero is the idle state; to stop the showcase run `infra/scripts/resident_demo_deploy.py --no-ingress` or delete `ca-resident-demo` only. SQL S0, the employee app and the resource group stay untouched.

## Per-criterion result

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1. Prospective RPI artifacts and threat model committed | Proven for this run and the earlier runs; original independent October review not re-derived | Research, plan, details, critique, changes and review for this run under `.copilot-tracking/`; threat model 2026-11-16 and update 2026-11-17 cover public fake-email login, shared credential, sessions, cross-case access, fields and isolation |
| 2. #444/#455 resolved; failed rubric resolved without edits | Unproven | #444 closed and #455 merged (recorded earlier); the rubric outcome needs a hosted run on a pushed head, which this local session may not do. Nothing was rerun or edited |
| 3. (ticked) Login, denials, canary fields | Re-observed | Table above |
| 4. (ticked) Secret handling, HTTPS session, abuse controls | Re-observed | Secret names, cookie flags, 429, generic denial; no production security acceptance claimed |
| 5. (ticked) Local SQL, Docker, browser, lint; gate; hosted | Not re-run | No source change |
| 6. Pre-spend record: resources, spend, remaining cap, plan, stop conditions | Proven for the demo | Azure facts above and retained cost JSON; remaining about USD 259 of USD 700; October USD 50 incremental cap superseded by the owner decision of 2026-11-18. The earlier "all-in cost forecast" gap is not closed: a forward forecast was not produced |
| 7. Deployed showcase verified in a browser | Proven on the demo, desktop only | Playwright run above on the real HTTPS URL, with actual login, correct-case data and negative paths. "Applicable gates passed before deploy" is not re-proven here; mobile is out of scope by owner decision |
| 8. (ticked) Image, URL, validation, limits, resources, expiry | Refreshed except source commit | Digest recorded; source commit unconfirmed |

## Not proven and why

* Hosted CI and rubric outcome on a pushed head, and any external gate receipt: need publication, which this session may not do.
* Source commit behind the deployed digest: registry reachable only from the private network.
* Expiry after 1,800 seconds was read from the cookie and not waited out; Container Apps scale-to-zero (R-01) was observed as `minReplicas` 0 only, with no replica-count history.
* Forward cost forecast, production identity, resident enrolment, Legal or DPO approval, assistive-technology and mobile checks: out of scope for the synthetic desktop demo by owner decision or not producible here.
* Issue #462 stays open: criterion 2 stays unmet.
