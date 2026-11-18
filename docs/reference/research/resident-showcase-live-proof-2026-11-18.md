---
title: Resident Synthetic Showcase Live Proof (Issue #462)
description: Live desktop browser and Azure evidence for the unticked #462 acceptance criteria on the deployed synthetic resident showcase, with what stays unproven and why
ms.date: 2026-11-18
---

## Scope and limits

This note records a live check of the synthetic resident showcase `ca-resident-demo` in resource group `ama` on 2026-11-18, run by an agent session (`rpi-462-live`) under the owner decisions of the same date: synthetic demo, desktop width only, live Azure authorised (cap USD 700, no drills, no Key Vault rotation, no production change). Azure billing reconciliation, Legal and Data Protection Officer approval and person-run assistive-technology testing are not needed for the demo and are not claimed.

It is not a penetration test, a security acceptance, a production identity assessment or an accessibility acceptance. No source, infrastructure or Azure resource was changed, and no throwaway resource was created. Builds on the [2026-11-16 threat model](./resident-demo-threat-model-2026-11-16.md) and its [2026-11-17 update](./resident-demo-threat-model-update-2026-11-17.md), which stay unchanged.

Evidence: [live-checks.json](../../../.copilot-tracking/evidence/2026-11-18-resident-showcase-live/live-checks.json) (statuses and key names only) and four desktop (1280x900) screenshots in the same folder. The sign-in credentials were read at runtime by the script, which asserts they appear in no output; the filled-form screenshot masks both fields. Chromium via Playwright 1.x ran against the public HTTPS URL.

Disclosure: while inspecting the credential file's shape, one diagnostic command printed its two values into this session's terminal. They were not written to any artifact, commit or log in the repository. The password is a shared synthetic demo credential; the owner may choose to rotate it, which this session did not do.

## Live evidence

| Check | Result |
|-------|--------|
| URL | `https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io` (external ingress, `allowInsecure` false); plain HTTP returns 301 to HTTPS |
| Cold start | Scaled to zero between runs; first request took 14 to 35 seconds. Min replicas 0 is by design for cost |
| Signed-out page | 200, title says "synthetic showcase, not live", banner says the shared sign-in does not prove identity and that Legal and DPO review is outstanding |
| Login without CSRF token, or with a foreign `Origin` | 403 |
| Wrong password, unknown email | Both 401 with the identical body "We could not sign you in with those details."; no session cookie set |
| Repeated failures from one source | 429 after the fifth failure inside ten minutes (limit 5 per source per 600 seconds, in memory) |
| Staff and probe routes (`/api/cases`, `/workbench`, `/api/staff`, `/admin`, `/demo/staff`, `/.env`) | All 404 |
| Unsigned `/demo/view`; forged session cookie; tampered real session cookie | 401 each; the session endpoint reports signed out for a forged cookie |
| Correct demo login in the browser UI | Succeeds; page shows the read-only case summary, timeline, documents, sensors and "Not available in this showcase" panel for messages, uploads, downloads, appointments, consent and callbacks |
| Session cookie | `__Host-zfdemo`: Secure, HttpOnly, SameSite=Strict, path `/`, about 1,800 seconds lifetime. CSRF cookie `__Host-zfdemo-csrf`: Secure, SameSite=Strict |
| Case binding | `/demo/view` needs the matching `X-Resident-Session` value (409 without or with a wrong one). Query strings `case`, `case_id`, `email` and headers `X-Case-Id`, `X-Forwarded-User` returned a view identical to the signed-in one, so the case comes only from the signed session |
| Projection | 18 top-level keys, including the derived sensor keys; the only email-like field is `account.email`, the signed-in resident's own fake address. A scan for safeguarding, vulnerability, invoice, salary, IBAN, token, internal-note and date-of-birth terms found none. Matches for "staff" and "password" are the resident-facing sentences "Ask staff to check it" and the shared-demo-password notice |
| Sign out | Account menu, then Sign out: session reports signed out and `/demo/view` returns 401 |
| Replay of the old cookie after sign out | 401 in a fresh browser context (mechanism not isolated; the threat model records stateless signing, so this is an observation, not a revocation guarantee) |
| Password in page text or HTML | Not present |

Observation, not a defect claim: the response carried `Content-Security-Policy`, `X-Content-Type-Options: nosniff` and `X-Frame-Options: DENY` but no `Strict-Transport-Security` header. HTTPS is enforced by ingress redirect and `__Host-` Secure cookies.

## Azure facts recorded

* Running revision `ca-resident-demo--0000012`, created 2026-11-17T20:19:26Z, 100 percent traffic, 0.25 CPU, 0.5 Gi, min 0 and max 1 replica, tags `workload=resident-demo` and `zava-forward-synthetic=true`.
* Image `crcutovertestrzsrg.azurecr.io/zava-resident-demo@sha256:65481780cb3f5a55621f637fa783230004b263085dcaece1dfca93a928bbbd19`. The registry is private-network only, so this session could not read the image manifest or labels; the source commit behind the digest is therefore not independently confirmed here.
* Secrets come from Key Vault references (`demo-password-verifier`, `demo-session-key`); the app holds a verifier, not the password. `ZF_DEMO_EXPIRES_AT` is 2028-01-01T00:00:00Z.
* Identity `id-resident-demo` holds only AcrPull on the registry, Key Vault Secrets User on the two named secrets, and Cognitive Services OpenAI User on `aoai-resident-469`. No broad grant was found.
* Resources owned by the showcase: `ca-resident-demo`, `id-resident-demo`, `aoai-resident-469`, the two Key Vault secrets, and a read path to the existing `retrofit` database (Standard S0 untouched). It shares the environment `cae-cutover-test-demo` with `ca-cutover-test-demo-api`.
* Actual cost for resource group `ama` (Cost Management query, 2026-11-18): USD 440.90 from 2026-10-01 to 2026-11-18 and about USD 89 month to date, against the owner's USD 700 cap, leaving about USD 259. Shared network, registry and monitoring dominate; the resident app (Container Apps USD 1.52 month to date, scale to zero) is a small part. This is a read of actual cost, not a billing reconciliation.
* Stop and expiry plan: scale to zero is the idle state; to stop the showcase, remove ingress with `infra/scripts/resident_demo_deploy.py --no-ingress` (documented rollback) or delete `ca-resident-demo` only. The resource group, SQL sizing, employee app and Key Vault secrets stay untouched. The built-in expiry date of 2028-01-01 is later than the demo needs; the owner may shorten it by redeploying.

## Dependencies

* #444 is closed (2026-10-27) and PR #455 merged (2026-10-25). #441 stays open and is not accepted by this issue.
* The earlier failed rubric score was not rerun, edited or bypassed here.

## Per-criterion result

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1. Prospective RPI artifacts and threat model committed | Proven for this run; earlier runs preserved | Research, plan, details, critique, changes, review under `.copilot-tracking/` for this run; threat model of 2026-11-16 and update of 2026-11-17 cover login, shared credential, sessions, cross-case access, fields and isolation. The original independent review of the October implementation is not re-derived; independent human or coordinator review of this candidate remains separate |
| 2. #444/#455 resolved; failed rubric resolved without edits or reruns | Partly proven | Dependencies closed and merged (above). The rubric outcome needs a hosted run on a pushed head, which this local-only session cannot do; unproven |
| 3. (ticked) Login, denials, canary fields | Re-observed live | Table above |
| 4. (ticked) Secret handling, HTTPS session controls, abuse and error controls | Re-observed live | Key Vault references, cookie flags, 429, generic error. Production identity or security acceptance is not claimed |
| 5. (ticked) Local SQL parity, Docker, browser, lint; full gate verified; hosted checks | Not re-run | No source change, so no new gate; the ticked state rests on earlier evidence |
| 6. Pre-spend record: resources, accrued spend, remaining cap, resource plan, stop conditions | Proven for current state | Resources, actual cost, remaining USD 259 of USD 700, owned resources and stop plan above. No resource was created or changed, so no new spend was incurred. The October USD 50 incremental cap is superseded by the owner decision of 2026-11-18 |
| 7. Deployed showcase verified in a browser: real HTTPS URL, actual demo login, correct-case data, negative paths | Proven on the demo | Playwright desktop run above. "Applicable engineering and review gates passed before deploy" is not proven by this session, and mobile widths were out of scope by owner decision |
| 8. (ticked) Image identity, URL, validation, limits, owned resources, expiry | Refreshed except source commit | Image digest recorded; source commit for the digest unconfirmed (private registry) |

## Not proven and why

* Hosted CI and rubric outcome on a pushed head, and the full external gate receipt: need publication, which this session may not do, and the owner scoped the demo away from them.
* Expiry of a live session after 1,800 seconds was not waited out; the cookie lifetime was read and expiry is covered by the domain tests.
* Source commit behind the deployed digest: registry reachable only from the private network.
* Production identity, resident enrolment, Legal or DPO approval, assistive-technology and mobile checks: out of scope for the synthetic desktop demo by owner decision.
