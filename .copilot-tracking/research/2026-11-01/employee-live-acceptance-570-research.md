# Research: employee sign-in identity, live acceptance entry point (#570)

Date: 2026-11-01. Branch: fix/employee-signin-identity. Disposition: reused existing evidence plus fresh repo read.

## Findings

* Criterion 1 (cause): `/api/me` returned 200 but the 2026-10-30 runner compared display email (`account.email`), which is display-only and may be empty or an unbound `@entra.invalid` key. Documented in `src/api/README.md` ("Employee acceptance identity check (#570)"). Identity is `user.tid`/`oid`; role comes from the Entra app role.
* Criterion 2 (fix): merged in #601 (`checks/employee_identity_check.py` BINDING predicate) and `checks/employee_acceptance_check.py` (`verify_employee`) with regression tests in `src/api/tests/`.
* Criterion 3 (live chat/map/case): unproven. Owner decision 2026-10-31 (issue comment) authorizes the existing test user for acceptance testing; #616 and #617 are closed. No credentials or sign-in are available to this session, and none may be committed.
* Gap: `verify_employee` has no operator entry point. The module `__main__` only runs offline Chromium tests.

## Planning Readiness

Ready. Slice: a credential-free CLI that attaches to a caller-owned, already signed-in Chromium over CDP, runs `verify_employee` with independently supplied tid/oid, and prints fixed boolean JSON.

## Out of scope

Live sign-in, credential handling, any application mapping change (README: do not change mapping), new code in mvp/ or prototype/.
