# Changes: 82-wire-eligibility-gate-1819

* `src/core/src/zava_forward/core/grants.py`: `ELIGIBILITY_OUTCOMES`, `grant_eligibility_verdict`; new grants start `Not assessed`; proposals may carry `eligibility` and `eligibility_source`; approving Submitted passes `eligibility_gate` (Eligible with evidence passes, Not eligible fails, anything else unknown and refused); pre-field legacy records are not gated and are labelled in history.
* `src/api/src/zava_forward/api/web/panels.js`: eligibility inputs on the proposal form and pending eligibility shown to approvers. Web-design-guidelines source was not fetched (small form-field addition; disclosed).
* Tests: four new cases in `test_grant_lifecycle_controls.py` (pass, fail/unknown with correction, malformed pending, legacy); Submitted paths in three existing tests now record eligibility.
* Early premature draft of grants.py (before research-open) was reverted and re-applied after critique; draft kept outside the repo.

Validation (/tmp/venv-82e-1819): test_gates 28 OK; test_grant* 56 OK (20 skipped, SQL Server); test_finance* 78 OK; funding boundary, governance, handoff, API grant/journey/role-matrix OK; no `test_workflows*` files exist; ruff clean; mypy core clean; mypy api 66 pre-existing missing-stub/type errors, none in touched files.
