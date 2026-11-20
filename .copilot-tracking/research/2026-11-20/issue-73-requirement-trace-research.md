# Research: issue 73 criterion 3, requirement traceability (2026-11-20)

Refs #73. Synthetic demo, desktop only. Task slug `issue-73-live`.

## Criteria read from the issue

* Unticked 1: stabilization checkpoint (#440). Needs an owner-recorded checkpoint; not buildable.
* Unticked 2: all children closed or deferred. #76, #79, #80 open; needs owner deferral or human signatures; not buildable.
* Unticked 3: each requirement traces to a passing acceptance check or a recorded deferral. Buildable: a curated trace matrix plus an offline test.

## Evidence found

* Requirements in scope: BG-011, FR-001 to FR-007, FR-032, FR-034, NFR-003 (BRD and PRD).
* The PRD traceability table (docs/prds/zava-forward-retrofit-programme-demonstrator.md, around line 2291) links each FR to AC ids, but no test file cites an FR id (only FR-003 in `test_hazard_safeguarding_clock_owner_76.py`). Existing tests are named by feature.
* BG-011 is a measured outcome (pilot cycle-time); NFR-003 is covered by role and field access tests plus AC-050.
* Existing `tools/test_epic_73_child_disposition.py` audits children only, not requirements.

## Planning Readiness

Ready. Research disposition: executed.
