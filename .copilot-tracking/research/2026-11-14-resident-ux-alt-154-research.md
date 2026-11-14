# Research: resident non-digital alternatives and representative views (#154)

Date: 2026-11-14. Planning Readiness: Ready. Research disposition: executed.

* Design exists: `docs/reference/research/ux/customer-journeys/residents.md` (J1-J6, R1) with non-digital equivalents; guarded by `src/core/tests/test_resident_journey_design.py`.
* Authority is enforced at write time in `resident_decisions.authority_for` (status, task, measure, review date).
* Gap: no read-side, reusable projection of a representative's task-limited, expiring authority, and no machine-checkable per-step alternative with needs and a no-incapacity rule.
* Constraint: do not edit `src/api/.../web/role-screens.js` (in-flight UX PRs).
* Not proven: usability or accessibility with residents (pending #155).

## Cycle 2 (PR #1719 CI: src-core bare mypy)

* Evidence: `resident_access.py:66` list-item (`[None]` literal inferred as `list[None]` against `dict[str, Any]`); `tests/test_resident_access.py:6` no-untyped-def and `:29,32,40,46` no-untyped-call on `authority`.
* Planning Readiness: Ready. Research disposition: executed (CI log and source read).
