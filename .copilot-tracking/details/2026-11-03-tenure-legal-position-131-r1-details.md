# Details: tenure Legal position reference (R1)

## Phase 1

* New closed action `tenure_legal_position`: `case_id`, `report_version`, `expected_version`, `reviewer_name`, `reviewer_role`, `position_ref`, `position_version`, `reviewed_on`.
* Refused: unknown report, stale version, non-Legal reviewer role, reviewer equal to the recorder, future date, blank reference, extra fields.
* Append-only `legal_positions` on the report; `legal_position` text updated; hold, verification, decision_route and cost_position untouched.

## Phase 2

* `src/core/tests/test_resident_decisions.py`: attach keeps hold, refusals leave case and audit unchanged.
* `src/api/tests/test_resident_api.py`: HTTP attach, 403 for non-workflow role, no canary leak to restricted roles.

## Phase 3

* `src/core/README.md`, `src/api/README.md`.
