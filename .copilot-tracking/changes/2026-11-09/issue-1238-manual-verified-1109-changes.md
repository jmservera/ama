<!-- markdownlint-disable-file -->
# Changes: issue 1238 F3 manual_verified supersession (1109)

Implementation recorded 2026-11-09 after the critique and after tests were
written first. Plan: [plan](../../plans/2026-11-09/issue-1238-manual-verified-1109-plan.md).

## Source and tests

* `src/core/src/zava_forward/core/resident_decisions.py` (+56/-3):
  `service_supersede_authorize` added to `RESIDENT_ACTIONS` and
  `FOLLOWUP_ACTIONS` (so it runs through `_operation`); handler
  `_res_service_supersede_authorize`; helper `_same_owner`; constant
  `_SUPERSEDE_ROLES`; `Superseded` added to the unresolved set in
  `_res_service_forward`. Unrelated formatting not applied (a trial
  `ruff format` of this file was reverted and the change reapplied surgically).
* `src/core/tests/test_resident_decisions.py` (+219): nine focused cases in
  `JsonResidentDecisions`, inherited by SQLite and MSSQL classes: valid flow,
  refusals, aged and non-`Pending` attempts, Independent review reviewer,
  reassignment after first authorization, atomic audit fault and replay,
  in-flight refusal, late outcome for a superseded attempt, retention deletion.
* `src/core/README.md` (+23): manual_verified boundary, interpretation and
  limits.

## Evidence (owned scratch `/tmp/issue1238-manual-verified-1109.134hqa`)

* Red (tests before source): `-k supersede -k late_outcome`: 27 run, 16
  failures/errors (14 `Unknown step`, 2 in-flight assertion), 2 passed (aged
  guard, already enforced), 9 skipped (MSSQL opt-in); `red-final.log`.
  Adverse first attempt: `NameError` at import from an unquoted test annotation
  (fixed; one `unchanged_failure` false green in the in-flight case tightened to
  assert the in-progress message).
* Green focused: 27 run, OK, 9 skipped (`green1.log`).
* Resident-decisions module (JSON, SQLite; MSSQL opt-in skipped): 344 run, OK,
  122 skipped (`module2.log`).
* `ruff check`, `ruff format --check`: pass after formatting the test file
  (first run flagged three E501 lines in new tests, `ruff-red.log`); strict
  `mypy`: 282 files pass.
* MSSQL (one nonqueued `flock -n` admission, lock holder none,
  `127.0.0.1` owned disposable container, removed after): `-k supersede -k
  late_outcome -k forward`: 87 run, OK, 0 skips; 29 per backend (JSON, SQLite,
  MSSQL). Raw: `mssql-selected.log`, `mssql-owned.txt`.
* A test defect found and fixed during green: attempt 1 stays `Pending` after
  a later attempt acknowledges, and is validly supersedable; the test now
  refuses only the `Acknowledged` attempt.

## Remaining gaps (not claimed closed)

Control-owner mapping awaits owner confirmation; evidence reference is not
machine-verified; no manual receipt-recording path; in-flight check is per
store instance; synthetic tests are not human approval.
