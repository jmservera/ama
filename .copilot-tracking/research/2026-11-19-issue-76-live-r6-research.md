# Issue 76 r6 research (2026-11-19)

Refs #76. Synthetic desktop demo. Only unticked criterion: "Hazard and safeguarding items show a clock and named owner".

Prior passes: docs/reference/research/issue-76-live-r5-2026-11-19.md (clock and owner logic in `taskqueues.hazard_clock` and `project_safety_clock_and_owner`; hazard time values Unknown because the synthetic hazard record has no awareness timestamp; fail-closed by design).

Disposition: reused (r4/r5 evidence). Planning Readiness: Ready for a verification-only plan.
Re-run today: `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_taskqueues test_hazard_safeguarding_clock_owner -q` -> Ran 33 tests, OK.
Remaining gap: demo-data decision (seed an awareness time for hazards, or accept Unknown as showing a clock). Inventing a value in code would contradict the fail-closed tests. Needs the owner.
