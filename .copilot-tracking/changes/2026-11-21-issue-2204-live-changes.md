# Changes: issue 2204 role sign-in proof (2026-11-21)

Tier: focused. No src change, so no defect fix and no full tier. Not run: `rpi-checks.py --all`, hosted CI (no push by instruction).

## Files

* Added `docs/reference/research/issue-2204-role-signin-wrong-role-denial-live-2026-11-21.md`.
* Updated `docs/reference/README.md` (index row) and `docs/reference/log.md` (entry).
* Added evidence under `.copilot-tracking/evidence/2026-11-21/issue-2204-live/`: `live_role_probe.py`, `live-role-probe.json`, two denial screenshots, `local_role_matrix.py`, `local-role-matrix.json`, `local-role-matrix-server.log`, and three adverse attempt records.

## Validation

* Live Playwright probe on `ca-cutover-test-demo-api` (read-only); local matrix via the real server.
* `python3 -m unittest test_entra_authoritative test_auth test_role_matrix test_role_screens test_employee_identity_check` from `src/api`: 108 tests OK.
* Credential literal scan of the evidence folder: no match. No Azure resource created, so nothing to delete.

## Per-criterion table

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Each role signs in and sees only its permitted views; admin sees all | Partly proven, unticked | Live: Programme Manager only (13 views, data 200, admin-only 403). Local application-layer matrix covers all eight staff roles, contractor, administrator alone and with a staff role. Unproven live: seven other staff roles and the administrator; no accounts and `az ad` returns insufficient privileges |
| 2 | One wrong-role denial shown; no credentials printed or stored | Proven | Programme Manager refused `/api/admin/simulator-control` (403 `ADMIN_REQUIRED`) and the simulator and repairs screens in the browser; credential scan no match |
| 3 | Evidence recorded | Proven | Research note and evidence folder |

## Divergences

* The live probe and local matrix ran during Research, before the plan was written, because the plan depended on whether a defect existed. The plan was then written with the evidence in hand.
