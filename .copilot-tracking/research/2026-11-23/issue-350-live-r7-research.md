# Issue 350 r7 research (2026-11-23)

Disposition: executed (builds on r6 note `docs/reference/research/issue-350-live-r6-2026-11-23.md`).

Findings:
* Criteria 2-10 need owner-only authorisation, a second role, or live model/map/photo/law inputs that code cannot supply. Criterion 9 is already proven.
* Criterion 1 is the first criterion that tooling can address: the app returns 401 (test_auth passes) but the platform edge (`excludedPaths` plus `RedirectToLoginPage` in `infra/modules/containerapps.bicep`) answers browser-style anonymous API requests with 302. No repeatable tool classifies this; each pass used an ad hoc probe.
* A path-scoped exemption of `/api` is unsafe without trusted-principal proof, so no infra change is made.

Slice: add `tools/check-edge-anonymous-401.py` with offline-testable classification and a live GET-only mode, plus a unit test. Run it live for evidence.

Planning Readiness: Ready.
