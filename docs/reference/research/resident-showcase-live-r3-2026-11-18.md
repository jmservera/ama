---
title: Resident Synthetic Showcase Live Check r3 (Issue #462)
description: Third 2026-11-18 live desktop and Azure check of the synthetic resident showcase, with retained evidence, the criterion 2 hosted-run facts and a per-criterion proven/unproven table
ms.date: 2026-11-18
---

## Scope and limits

Session `rpi-462-live`, task `issue-462-live-r3`, on 2026-11-18 under the owner decisions of the same date: synthetic demo, desktop only, live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change). Billing reconciliation, Legal and Data Protection Officer approval and person-run assistive-technology testing are not claimed.

No source, infrastructure or Azure resource was changed and no throwaway resource was created. This is not a penetration test or a security, identity or accessibility acceptance. It supplements the [first proof](./resident-showcase-live-proof-2026-11-18.md), the [recheck](./resident-showcase-live-recheck-2026-11-18.md) and the [2026-11-16 threat model](./resident-demo-threat-model-2026-11-16.md).

Sign-in values were read at runtime from the owner files and never printed. The script asserts they appear in no retained output; the filled-form screenshot masks both fields. Evidence is in `.copilot-tracking/evidence/2026-11-18-resident-showcase-r3/`: `live-checks.json` (36 checks), `live_r3.py`, `gh-444.json`, `gh-455.json`, `gh-pr455.json` and two 1280x900 screenshots (the empty and masked sign-in forms). The signed-in, account-menu and signed-out captures showed an account email and a street address and are not retained.

## Live browser and HTTP results

Public URL: `https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io`, revision `ca-resident-demo--0000012`, state Running, image digest `sha256:65481780...bbbd19`, tags `workload=resident-demo` and `zava-forward-synthetic=true`.

| Check | Result |
|-------|--------|
| HTTPS and cold start | HTTP returns 301 to HTTPS; cold start 35.8 seconds (min replicas 0) |
| Sign-in page | Title says "synthetic showcase, not live"; banner says the shared sign-in does not prove identity and Legal and DPO review is outstanding |
| Missing CSRF token; foreign `Origin` | 403; 403 |
| Wrong password; unknown email | 401 and 401, identical generic body, no cookie set |
| Staff and probe routes | `/api/cases`, `/workbench`, `/api/staff`, `/admin`, `/demo/staff`, `/.env` all 404 |
| Unsigned view; forged cookie | 401 and 401; forged cookie reports signed out |
| Correct login in the browser | 200; timeline, documents, sensors and "Not available in this showcase" panel shown; the page text does not contain the password |
| Cookies | `__Host-zfdemo` Secure, HttpOnly, SameSite=Strict, path `/`, 1,795 of 1,800 seconds left; CSRF cookie Secure, SameSite=Strict |
| Case binding | `/demo/view` returns 409 without or with a wrong `X-Resident-Session`; the query strings `case`, `case_id`, `email` and headers `X-Case-Id`, `X-Forwarded-User` did not change the account (the comparison flags a time-driven sensor age field, as diagnosed in the recheck) |
| Projection | One email-like string, equal to the signed-in fake address; only the terms "password" (shared-demo notice), "phone" ("shows no phone numbers") and "staff" ("Ask staff to check it") appear; no safeguarding, vulnerability, invoice, salary, IBAN, token, internal-note or date-of-birth term |
| Write routes by GET | `/demo/logout`, `/demo/assistant`, `/demo/agenda` return 405 |
| Sign out | Session reports signed out and the old session value returns 401 on `/demo/view` |
| Rate limit | After two earlier failures, bad logins returned 401, 401, 401 then 429 on the fourth: five failures exhaust the budget, matching the documented 5 per 600 seconds. This confirms the exact count the recheck could not |
| Headers | CSP, nosniff, frame deny, referrer policy and cache control present; `Strict-Transport-Security` absent (observation; HTTPS rests on redirect and `__Host-` Secure cookies) |

## Criterion 2 facts (read-only `gh`)

* #444 is CLOSED (2026-10-27T17:31:06Z); PR #455 is MERGED (2026-10-25T21:25:42Z, merge commit `c8d16059c0c0a22c4ffba88c6b65ac068f64accc`).
* The Capstone Rubric Scorer history on the #455 branch shows one `failure` at head `b82a7c4c`, then `success` runs at `a3ce5984` and at the final head `2523a70b` (two runs, the last at merge time). The failure was cleared by later commits, not by a bypass: no skipped or edited score was found in the run list, but the run list cannot prove that no manual score edit happened.
* Review thread `discussion_r4372517587` ("Reject fixture pairs with missing identifiers", High) on #455 is still unresolved and not outdated after the merge. Whether main fixed it was not verified here. This blocks calling the dependency resolution complete.
* The scorer workflow is currently `disabled_manually`; a hosted run on a pushed head for this work is not possible from a local-only session.

## Cost and stop plan

Cost Management returned HTTP 429 (Too Many Requests) when queried again, so no fresh figure was read. Using the retained 2026-11-18 reads ([recheck](./resident-showcase-live-recheck-2026-11-18.md)): USD 440.90 from 2026-10-01 to 2026-11-18 (49 days, about USD 9.0 a day) and USD 89.15 month to date (18 days, about USD 4.95 a day). At the November rate the 12 remaining days add about USD 59, leaving roughly USD 170 of the USD 700 cap at month end; at the October to date average of USD 9.0 a day, about USD 108 more, leaving roughly USD 150. This arithmetic estimate is not a Microsoft forecast or a billing reconciliation. Stop plan unchanged: scale to zero when idle; `infra/scripts/resident_demo_deploy.py --no-ingress` or deleting `ca-resident-demo` alone; the resource group, SQL S0 and employee app stay untouched.

## Per-criterion result

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1. Prospective RPI artifacts and threat model | Proven for this run and earlier runs; original October independent review not re-derived | This run's `.copilot-tracking/` research, plan, details, critique, changes and review; threat model 2026-11-16 and update 2026-11-17 |
| 2. #444/#455 resolved, failed rubric resolved without edits | Partly proven, unmet | Closed and merged; rubric success at the final head. Unresolved High review thread and no proof of absence of manual edits; hosted run needs a push |
| 3. (ticked) Login, denials, canaries | Re-observed | Table above |
| 4. (ticked) Secrets, HTTPS session, abuse controls | Re-observed; rate-limit count now exact | Table above; no production security acceptance claimed |
| 5. (ticked) Local SQL, Docker, browser, lint; gate; hosted | Not re-run | No source change |
| 6. Pre-spend record | Proven for the demo, forecast as arithmetic only | Resources and stop plan as in the recheck; cost refresh throttled; estimate above. October USD 50 cap superseded by the owner decision |
| 7. Deployed showcase verified in a browser | Proven on the demo, desktop only | Playwright run above; "gates passed before deploy" and mobile not claimed |
| 8. (ticked) Image, URL, validation, limits, resources, expiry | Refreshed except source commit | Digest read; the registry is private-network only (`az acr` access denied), so the source commit stays unconfirmed |

## Not proven and why

* Criterion 2 completion: unresolved review thread, manual-edit absence and hosted rubric need publication or a maintainer decision.
* Source commit behind the digest: private registry.
* Fresh cost figure: Cost Management throttled.
* Session expiry after 1,800 seconds was read from the cookie, not waited out; scale-to-zero was seen only as a cold start and `minReplicas` 0.
* Production identity, Legal or DPO approval, assistive-technology and mobile checks: out of scope for the demo by owner decision.

Issue #462 stays open; criterion 2 is unmet. Refs #462.
