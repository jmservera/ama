# Details: issue 233 withheld panel slice

## Phase 1

* `src/api/src/zava_forward/api/web/role-screens.js`: `screenWithheld(items)`
  renders a `screen-record` section titled "Not shown for this role" with a
  native list. Uses existing design system classes only.
* `programme-queue`: lists resident contact and access history, household and
  vulnerability details beyond step states, funding amounts and claim values.
* `resident-choice`: lists contact history, detailed household history, and
  contractor capacity and offered slots.

## Phase 2

* `src/api/tests/test_role_screens_conformance.py`: presence guard on both
  screens and trace label "Proposed rule; rendered behaviour and conformance not assessed".
* `docs/reference/research/ux/atlas-screen-trace.md`: tension row and guardrail text.
* `docs/reference/log.md`: appended entry.

## Phase 3 validation

Run: role-screen api tests, core atlas trace test and checker, ruff, mypy
(`--cache-dir=/tmp/mypy-233`), `node --check`. Not run: gate, benchmarks, full
suites, rendered browser or assistive-technology checks.
