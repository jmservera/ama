# Changes: employee live acceptance CLI (#570)

Date: 2026-11-01. Plan: ../../plans/2026-11-01/employee-live-acceptance-570-plan.md

* Added `src/api/checks/employee_live_acceptance.py` (loopback CDP attach, env-supplied tid/oid, boolean JSON, exit 0/1/2).
* Added `src/api/tests/test_employee_live_acceptance.py` (3 offline tests).
* Updated `src/api/README.md` with the operator entry point.
* Validation: employee unit tests 22 OK (venv, pip); ruff check, ruff format --check, mypy clean for touched files. No heavy local gate (CI is the evidence).
* No divergences from plan. No sign-in, credential or live run performed.
