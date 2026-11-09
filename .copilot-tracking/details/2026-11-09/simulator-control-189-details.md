<!-- markdownlint-disable-file -->
# Issue 189 details (2026-11-09)

Plan: [plan](../../plans/2026-11-09/simulator-control-189-plan.md).

## API contract (all under `/api/admin/simulator-control`)

* `GET` returns `{availability, state, owner, time_limit, approval_reference, cohort_size, budget_alert, capacity, revision, manual_route, writable}`. `availability` is `configured|unavailable|invalid|not_configured`. Home ids are never returned.
* `POST .../start` body: `owner`, `approval_reference`, `expires_at`, `homes` (list), `expected_revision`, `confirm` true. Refusals (fixed `code`, plain `error`): `ADMIN_REQUIRED` 403, `CONTROL_NOT_CONFIGURED` 503, `CONFIRMATION_REQUIRED` 400, `BODY_INVALID` 400, `STALE_CONTROL` 409, `ALREADY_RUNNING` 409, `CONTROL_INVALID`/`CONTROL_WINDOW_INVALID`/`B1_QUOTA_HEADROOM`/`RATE_TOO_LOW_FOR_HOMES` 400, `WRITE_FAILED` 503, `WRITE_NOT_VERIFIED` 503.
* `POST .../stop` body: `expected_revision`, `confirm` true. `NOTHING_TO_STOP` 409 (no readable control), `STALE_CONTROL`, `WRITE_FAILED`, `WRITE_NOT_VERIFIED`; already stopped returns 200 `changed:false`.
* Authorization: Entra identity, `app_admin` true, `identity.verified`. Everything else is 403 with the same body (no role enumeration). Trusted-proxy CSRF header check already runs before the hook.
* Audit: `store.audit(actor, "sim_control_start|stop", "-", detail)` after a verified write; if the audit fails the response carries `audit_recorded:false` (surfaced) but the verified file state is reported honestly.
* `revision` is the SHA-256 of the file bytes, or `absent`. An exclusive non-blocking `flock` on a sidecar lock file (`live_control.locked`, shared with the CLI) is held across read, check, write and read-back; a held lock is `CONTROL_BUSY` 409. The write is read back and compared. Critique revision: `state` keeps the `decide()` value (`send` shown as "Permitted") and `activity` is always `unverified`.

## Files

* New: `src/api/src/zava_forward/api/simulator_admin.py`, `.../web/simulator-control.js`, `src/api/tests/test_simulator_admin.py`, `src/api/checks/simulator_control_browser_check.py`.
* Hooks: `server.py` (import, GET, POST), `workbench.py` (admin destination `#/simulator`), `web/app.js` (loader entry, route), `web/index.html` (script tag), `README.md`.
* Existing test adapted deliberately: `test_entra_authoritative` admin navigation expectation (new available entry) and `test_content_standard.AUDITED_FILES` gains the new script (strictens).

## Screen

Heading "Simulator run control"; `dl` of State, Owner, Time limit, Approval reference, Cohort, Budget alert, Quota headroom; refresh button; start form (labels, native inputs, confirmation checkbox, "Start Finite Run"); stop form (confirmation checkbox, "Stop Run"); `role=status` and `role=alert` regions; manual route text.
