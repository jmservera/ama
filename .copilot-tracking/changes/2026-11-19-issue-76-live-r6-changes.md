# Changes r6 (2026-11-19)
No source change. FOCUSED tier. Refs #76. No Azure action; nothing created, nothing to delete.

Validation: `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_taskqueues test_hazard_safeguarding_clock_owner -q` -> 33 tests OK. mypy/ruff not applicable (no src edit).

| Criterion | Status |
| --- | --- |
| Default view single list, status and next action | Ticked in issue; not re-run |
| No perspective picker or simulator | Ticked in issue; not re-run |
| Queue categories with definitions | Ticked in issue; not re-run |
| Blocked steps reason, owner, next action | Ticked in issue; not re-run |
| Hazard and safeguarding clock and named owner | Unproven for hazard time values: safeguarding and owner proven (33 tests, r4 live); hazard awareness time is Unknown, needs an owner data decision |
| Views agree (FR-034) | Ticked in issue; not re-run |
| Single reset (FR-032) | Ticked in issue; not re-run |
