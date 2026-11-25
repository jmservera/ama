---
title: Issue 2310 anonymous protected API 401 proof (2026-11-25)
description: Evidence that the three acceptance tests already exist and pass, plus a live anonymous probe of the demo API app
ms.date: 2026-11-25
---

Refs #2310, #350, #116. Synthetic demo, desktop only, owner decisions of 2026-11-18.

## Finding

The two acceptance tests named by the issue already exist in `src/api/tests/test_auth.py`, added by commit `d29535aca0` (#1005) and extended since. Writing them again would duplicate coverage, so no test or source change was made.

| Criterion | Existing test |
| --- | --- |
| Anonymous protected API GET, browser User-Agent, `Accept: application/json` returns 401, not a redirect | `ProxyHttpTests.test_anonymous_api_is_401_for_browser_style_requests_and_pages_still_redirect` (GET `/api/me`, `/api/cases`, `/api/account/photo`), and `test_anonymous_api_never_redirects_for_any_method_accept_or_unknown_path` (asserts no `Location` header) |
| Anonymous protected page still redirects | Same first test: `/app` with `Accept: text/html` returns 302 to `/sign-in`; the second test asserts `/sign-in` returns 302 to `/.auth/login/aad?post_login_redirect_uri=%2Fapp` |
| Existing auth tests pass, no weakening | Local run below |

## Local evidence

Run from `src/api` with `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`:

* `python3 -m unittest test_auth.ProxyHttpTests test_auth.TrustedProxyTests -v`: 31 tests, OK.
* `python3 -m unittest test_auth`: 45 tests, OK.

No route protection was changed.

## Live probe of the demo app (anonymous, no credentials)

Target: `ca-cutover-test-demo-api` in resource group `ama`. Requests used a Chrome User-Agent. Query strings of the redirect are omitted.

| Request | Result |
| --- | --- |
| GET `/api/me`, `Accept: application/json` | 302 to `login.microsoftonline.com/.../oauth2/v2.0/authorize` |
| GET `/api/cases`, `Accept: application/json` | 302 to Entra |
| GET `/app`, `Accept: text/html` | 302 to Entra |
| GET `/` | 200 (excluded public path) |

`az containerapp auth show` reports `globalValidation.unauthenticatedClientAction = RedirectToLoginPage`, with excluded paths `/healthz`, `/readyz`, `/`, `/welcome.html`, `/style.css`, `/zava-logo.png`, `/sign-in`. `infra/modules/containerapps.bicep:302` selects `Return401` only for `entraBearerOnly`.

Interpretation: the platform authentication layer answers anonymous `/api/*` requests before the application sees them, so on the deployed demo the browser-style API request gets a redirect. The application-level 401 proven by the tests applies once a request reaches the app (for example, an unauthenticated path or a different platform setting). This is a deployment-configuration gap, not a code defect, and it was not changed: the owner decision forbids production changes. Whether a browser `fetch` follows that redirect is a CORS failure rather than a 401; a Playwright fetch proof was not recorded, since the curl status above already shows the 302.

## Follow-up (not done)

Decide whether the demo should exclude `/api/*` from platform redirect (the app returns 401 itself) or switch API traffic to `Return401`. Needs an owner decision and a security review because it changes platform auth behaviour.
