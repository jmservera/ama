# Changes: assisted aftercare 133 Stage A (Refs #133)

Date: 2026-11-09. Base `a04668ae9`. Parent target `feat/demo-quality-workflows-89-1109`.

## Added

* `src/core/src/zava_forward/core/aftercare_intake.py`: `AftercareService`, `StateStore`, `FileStateStore`, errors, and the `handle` route contract.
* `src/core/tests/test_aftercare_intake.py`: 30 tests (roles, representative basis, channel provenance, idempotence, raw originals, owner binding, closure, sensor staff-only, evaluator denominators/Unknowns, restore validation, route statuses).
* `src/api/src/zava_forward/api/web/aftercare.js`: unwired screen module (form, receipt, concern, evaluator, submit).
* `src/api/tests/test_aftercare_screen.py`: 9 node-vm tests of the screen module.

## Modified

* `src/core/README.md`: Stage A paragraph with not-delivered list.
* `docs/reference/log.md`: appended entry.

## Not changed

`aftercare.py`, `server.py`, `role-screens.js`, `app.js`, `store.py`, `sqlstore.py`, endpoint inventory, common browser fixtures, `index.html`.

## Divergences from the plan

* Intake cannot name an owner (a new concern is `Unknown`); only `assign_owner` by a manager names one. Reason: record roles are Liaison/Coordinator, so a manager-only intake owner was unreachable. Safer and simpler.
* `aftercare.js` needs the shared `api()` helper to copy `data.errors` onto the thrown error (hook item, not edited).

## Validation (local, focused tier)

* Core: 56 tests pass (aftercare, intake, production consumer). ruff, ruff format and strict mypy clean.
* API screen test: 9 pass. ruff and mypy clean.
* Correction cycles used: 1 of 5 (owner-at-intake redesign and test typing).
* UNEXECUTED: connected API, persistence and restart, served browser, keyboard/error/receipt journeys, axe or AT, SQL tier, hosted CI.
