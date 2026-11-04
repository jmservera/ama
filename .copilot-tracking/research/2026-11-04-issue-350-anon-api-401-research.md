# Research: issue #350 anonymous API 401 (2026-11-04)

Research disposition: executed. Planning Readiness: Ready for slice 1.

## Delivered by merged PRs

* #352 (merged): public src edge and browser auth configuration (`entraBearerOnly=false` gives RedirectToLoginPage).
* #436 (merged): offline demo feedback evidence checker (Refs #350).
* No merged PR proves criterion 1 for browser-style API requests.

## Findings per acceptance criterion

| Criterion | Implementable offline | Reason |
| --- | --- | --- |
| 1 Anonymous API 401 for browser UA | Partly | App half: `server.py` returns 401 JSON for any anonymous `/api/` call and 302 `/sign-in` for pages (existing tests cover default UA only). Platform half: `infra/modules/containerapps.bicep` line 239 and `edge-existing-auth.bicep` use `RedirectToLoginPage`, which intercepts `/api` with 302 before the app. Changing it is an infrastructure and security change needing live Azure proof of trusted platform-principal headers. |
| 2 to 10 | No | Need tenant/staff prerequisites, owner-authorised data, model deployments, map licence, consent, law store SQL/Blob, DPIA approvals and per-role live runs. |

## Decision

Slice 1: pin the app-level contract with a browser-style anonymous request test. Platform change (e.g. AllowAnonymous with app enforcement, or a path-scoped rule) is deferred and tagged infrastructure/security: stop short of the gate; coordinator runs gates.

## Follow-ups

1. Slice 2 (infra, needs live Azure): resolve the platform 302 for `/api` with trusted-principal proof.
2. Remaining criteria 2 to 10 need owner/Azure actions.
