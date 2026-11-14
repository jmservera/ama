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

AC1-AC5 remain proven by existing tests in `test_job_pack.py` and `test_staff_intake_api.py` (pack, receipt, independent QA, no-show recovery, no self-approval). AC6 (named owner, never a contract instruction) is proven by the new tests above.
