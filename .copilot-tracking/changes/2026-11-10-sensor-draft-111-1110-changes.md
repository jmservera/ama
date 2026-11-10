<!-- markdownlint-disable-file -->
# Release Changes: sensor review drafts (#111), initial implementation, 2026-11-10

**Related Plan**: [2026-11-10-sensor-draft-111-1110-plan.instructions.md](../plans/2026-11-10-sensor-draft-111-1110-plan.instructions.md)
**Implementation Date**: 2026-11-10
**Branch**: `feat/demo-sensor-drafts-111-1110`, child of `feat/demo-sensor-review-109-1110` (product base `0d262beee`)

## Summary

First initial implementation (not a correction) of a NEW default-off, manual-review-only, PROPOSED and unapproved case-local sensor review draft over the existing `ReviewTaskCandidate`. It creates no task, work, owner, handoff, queue entry, model call, ranking, hold, hazard clock or consent change. The served policy carries no approval, so the served write is refused with `NO_APPROVED_RULE`; constructed approvals exist only in explicitly synthetic tests (`SYNTHETIC TEST ONLY`). Whole #111 stays unmet: no actual rule, method or human approval, no appointed staff, no UI creation control.

## Owner corrections applied before source

1. Tier: owner DEMO override. Targeted unit/static checks on modified and impacted code plus ACTUAL MSSQL and served-browser checks. No blanket full gate or full receipt. This supersedes the Tier paragraph of the committed plan (amendment below).
2. Interface accepted as ordinary engineering; TaskQueue and assistant task contracts are not reused.
3. Allocation limited to the new module and tests, bounded server routes, a projection pop and a read-only `sensorPanel` section. `store.py`, `sqlstore.py`, import, register, feed and `tools/` untouched.
4. Existing served sensor browser check extended; it has no scenario manifest or hash (verified by search), so no manifest update applies.

## Amendments to the committed plan (plan commit `34f06e40a` is preserved)

* Window maximum is 28 days (`Window` validation), not the 14 days stated in the plan.
* The draft digest is exposed only as a 12 character prefix; the full digest stays internal.
* The plan's UI creation control is NOT delivered; the screen section is read-only.
* The tier is the owner DEMO override above.

## Shared-hunk comparison (before writes)

* #135 worktrees: no diff in `projection.py`, `server.py` or `ops.js` against `0d262beee`.
* #132 worktree: `server.py` changes the `staff_intake` import, the workorders field-intake route kind and workorder GET/POST routes; `projection.py` adds `field_intake` to a GET-kinds tuple. None overlaps the sensor-draft hooks. The new import sits on the `simulation_lane` line, not the `staff_intake` line, to avoid a textual conflict.
* #1300 worktree: no comparable revision; `tools/` untouched.
* Disposition: independent. Textual ordering edge at parent integration only if both touch the same import region.

## Added

* `src/core/src/zava_forward/core/sensor_review_draft.py` - flag `ZF_SENSOR_REVIEW_DRAFTS`, case field `sensor_review_drafts`, role gate before flag (no flag oracle), current-staff and scope revalidation, consent-gated allowlisted read, digest-protected records, idempotent create by the existing `task_key`, bound of 20, rollback on failure, private synthetic seam.
* `src/core/tests/test_sensor_review_draft.py` - JSON, SQLite and MSSQL classes (MSSQL opt-in `ZF_SENSOR_DRAFT_MSSQL=1`, explicitly constructed `MssqlStore`).
* `src/api/tests/test_sensor_review_draft_api.py` - loopback HTTP tests.

## Modified

* `src/core/src/zava_forward/core/projection.py` - `redact_staff_detail` pops `sensor_review_drafts` first (1 line).
* `src/api/src/zava_forward/api/server.py` - GET `/api/cases/{id}/sensor-drafts`, POST `/api/cases/{id}/sensor-draft`, one import.
* `src/api/src/zava_forward/api/web/ops.js` - read-only `sensorDraftSection` inside `sensorPanel`.
* `src/api/checks/quality_sensors_browser_check.py` - draft scenarios: flag off, empty, synthetic seeded (markup rendered as text), consent withheld, unauthorised role, axe.

## Validation (targeted, owner DEMO override)

* Core: `test_sensor_review_draft` (61 tests: JSON, SQLite, MSSQL, 0 skipped with MSSQL enabled) plus `test_sensor_analysis`, `_store`, `_mssql`, `test_sqlstore`, `test_taskqueues`, `test_handoff_lifecycle`, `test_sensor_privacy`: 167 tests OK; the 10 skips are existing SQLite-only focused tests and one opt-in local SQL test unrelated to this change.
* MSSQL: disposable `mcr.microsoft.com/mssql/server:2022-latest` on loopback, labelled for this task, removed afterwards. Rollback, conflict and exactly-one-draft tests ran against it.
* API: `test_content_standard`, `test_quality_sensors`, `test_assistants`, `test_handoff_api`, `test_home_case_api`, `test_sensor_review_draft_api`: 341 tests OK (150 existing skips).
* Browser: `checks.quality_sensors_browser_check` with axe 4.10.3: 42 checks passed on the final source, run under `flock -n /tmp/ama-rpi-heavy.lock`. Run with a shortened scratch directory because the worktree path exceeds the Chrome socket path limit; the check source is unchanged by that.
* Static: `ruff check` clean; new files `ruff format` clean (existing `server.py` and `projection.py` are not ruff-formatted at base and were left as is); `node --check`; `git diff --check`; mypy clean for the new API test (existing mypy errors in `tests/test_quality_sensors.py` are pre-existing).
* Not run: blanket full gate or receipt, hosted CI, native assistive technology, real approval.

## Residuals

* No actual rule, method or human approval; served write always refuses by design.
* No UI creation control; AT and copy acceptance not performed.
* Issue-wide correction balance remains UNKNOWN.
* JSON backend `save` is a non-atomic whole-file rewrite; a failure after save loses only the audit line (existing store behaviour, not changed).
