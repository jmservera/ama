<!-- markdownlint-disable-file -->
# Changes: staff-mediated synthetic job pack intake (#132)

Plan: [staff-intake-132-plan.md](../../plans/2026-11-09/staff-intake-132-plan.md). Base `a04668ae9`.
Owner decision 2026-11-09 (issue 132 comment 6753054374) covers only existing-staff-mediated intake.

## Added

* `src/core/src/zava_forward/core/staff_intake.py`: capture, correct, acknowledge, view, handle (strictly typed).
* `src/api/src/zava_forward/api/web/staff-intake.js`: screen `staff-job-pack-intake` for staff roles.
* `src/api/tests/test_staff_intake_api.py`: 12 tests on SQLite, JSON subclass, opt-in MSSQL.
* `src/api/tests/test_staff_intake_browser.py`: opt-in Playwright and axe capture.

## Shared hooks (smallest changes)

* H1 `quality.py`: `submit_quality(..., field_receipt=None)` and `_touched()` at the start of `_quality_operation` for SQL.
* H2 `server.py`: import, `get_kind` `field_intake`, GET branch, POST branch for `field-capture|field-correct|field-acknowledge`.
* H3 `projection.py`: `STAFF_GET` gains `field_intake`.
* H4 `index.html`: `staff-intake.js` script tag after `role-screens.js`.
* H5 `test_role_endpoint_inventory.py`, `test_content_standard.py`: new paths and audited file.

## Amendments and divergences

* Fix cycle 1: content-standard banned word "hold" in screen copy, reworded.
* Fix cycle 2: strict mypy and ruff on the new module (annotations, line length, typed wrappers).
* Fix cycle 3: web-guidelines review findings: submit button disabled in flight, autocomplete off on correction name.
* AC5 escalation write path is not built (no authority); display of configured or Unknown destination only.

## Validation

See the handoff for commands and exits. Focused tier; no full gate run.
