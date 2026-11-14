# Changes: #132 named-owner variation and escalation routing (2026-11-14)

* `src/core/src/zava_forward/core/job_pack.py`: `named_owner`, `assert_advisory`, `UNNAMED_OWNERS`, `ADVISORY_NOTE`; `escalation()` enforces both.
* `src/core/src/zava_forward/core/staff_intake.py`: `escalation_destination` owner status and advisory-only fields; `route_escalation`; `boundaries.advisory_only`.
* `src/api/src/zava_forward/api/web/staff-intake.js`: Owner status and contract-instruction rows.
* `src/core/tests/test_job_pack.py`: placeholder owners rejected, every kind routes to a named owner, advisory assertion.
* `src/api/tests/test_staff_intake_api.py`: unassigned owner explicit and blocks routing; variation routes to configured named owner.

## Validation (run with PYTHONPATH pointing at this worktree, since editable installs point to the main checkout)

* core: `tests.test_job_pack` 13 OK; ruff check, ruff format --check, mypy clean (307 files).
* api: `test_staff_intake_api` + `test_procurement_api` 138 tests OK (38 opt-in skips); ruff check and format clean.
* api mypy: 2 `unused-ignore` errors in untouched `tests/test_ai_consumption_api.py`, identical on the unmodified baseline (environment related), not introduced here.
* Full core discover suite exceeded a 500 s local timeout and was not completed. Complete local gate, hosted CI and browser check not run.

## AC proof map for #132

AC1-AC4 remain proven by existing tests in `test_job_pack.py` and `test_staff_intake_api.py` (pack, receipt, independent QA, no-show recovery, no self-approval). AC5 (named owner, never a contract instruction) is proven by the new tests above.

## Cycle 1 correction (1 of 5)

* `job_pack.py`: `UNNAMED_OWNERS` replaced by `_PLACEHOLDER_WORDS`, `_ROLE_WORDS` and a person-name pattern in `named_owner`.
* `staff_intake.py`: `_configured_owner` and `_valid_contact` (placeholder config yields no owner and `UNKNOWN` display fields); `route_escalation` takes optional owner and role and keeps the contact; new `escalate` action registered as `field-escalate`; `view()` adds `escalations`.
* `test_staff_intake_api.py`: replaced the two direct-call tests with five HTTP tests (unassigned, placeholder fail-closed, staff-only and validation, restart persistence with audit and work-order fields unchanged, configured routing); contractor 403 loop covers `field-escalate`.
* `test_role_endpoint_inventory.py`: `field-escalate` added to POST endpoints.
* `test_job_pack.py`: 10 more placeholder and role-only names, plus `test_real_names_are_accepted`.

Corrected counts: the original slice added 2 API tests and 3 core tests (not 13 total new). Validation, `PYTHONDONTWRITEBYTECODE=1`, no `uv`: core `tests.test_job_pack` 14 OK; api `test_staff_intake_api` + `test_role_endpoint_inventory` 135 tests OK (41 opt-in skips, including the loopback SQL Server class, so SQL readback is covered only by shared code path and not exercised); `ruff check .`, `ruff format --check .`, `mypy` clean in `src/core` and `src/api` (the earlier 2 api `unused-ignore` errors did not recur). Full discover suites, `rpi-checks.py --all`, hosted CI and browser checks were not run. No push.

## Cycle 2 correction (2 of 5)

Fixed independent cycle 1 findings: escalation summary held for roles without a recorded need (advisory note kept), staff-intake.js escalation form, readback and computed contract-instruction text, non-string and dotted-initial owner rejection, README and AC5 numbering. Focused core/api tests, ruff and mypy pass. Browser, SQL Server, human AT and hosted CI not run. Refs #132.
