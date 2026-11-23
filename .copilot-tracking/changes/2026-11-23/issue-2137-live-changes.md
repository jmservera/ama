# Changes: issue 2137

No source change; tier: focused. Added docs/reference/research/issue-2137-live-2026-11-23.md, a README index row and a log entry.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| R1 to R3 complete before a derived measure is used beyond an exercise rule | Unproven, owner-gated | Code guard exists and is tested (34 tests OK); R1 sources not retrieved, R2 reviewer/Asset sign-off and R3 agreed limits are named human approvals, not waived on 2026-11-18 |

Validation: `python3 -m unittest test_sensor_analysis test_sensor_scenarios -q` from src/core: 34 tests OK (1 expected failure). Not run: full gate, hosted CI.
