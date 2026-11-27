# Research: issue 1204 live (2026-11-27)

Refs #1204. Synthetic demo, desktop only. Research disposition: executed (new scan; prior notes under docs/reference/research/issue-1204-* reused as baseline).

## Scope

Only criterion 2 is unticked: every tick has a next action and bounded closure-review progress when capacity is free; expired and newly granted approvals are reconciled without a global stop from one blocked lane. Criteria 1 and 3 to 6 are ticked in the issue and are not re-audited.

## Baseline

* tools/check-tick-log.py validates tick rows and has a `--require-extended` mode (2026-11-24, tools-only).
* The coordinator agent contract (lines 147-151) already tells the coordinator to record `closure_batch`, `approvals_granted`, `approvals_expired`, `reclassified` and `global_stop` in `tick_log`.
* Last recorded outcome: three local `tick_log` tables (216, 17 and 4 rows), none with extended columns.

## Open questions

1. Does any local `tick_log` window now carry the extended columns?
2. Do the checker and handoff tests still pass at this head?
3. Is there a real defect in checker or contract?

## Planning Readiness

Ready. No Azure, browser or src evidence is relevant to criterion 2, which is a prompt-behaviour criterion.

Evidence for the questions is recorded in docs/reference/research/issue-1204-extended-window-recheck-2026-11-27.md.

## Findings (executed 2026-11-27)

* Scan of 332 per-session databases: still three `tick_log` tables (216, 17 and 4 rows). Only the 216-row window is readable by the checker, and it has no extended columns. The 17 and 4 row tables use other schemas (exit 2, "no such column").
* Default mode on the 216-tick window: 0 violations. `--require-extended`: 216 violations. Criterion 2 runtime proof is therefore still absent.
* tools tests are flaky: `test_check_coordinator_handoff` wall-clock bounds (0.15 s, 0.25 s, 0.1 s, 0.5 s) fail intermittently at host load average 8 (2 of 4 reruns failed; 25 tests, `scale_elapsed` 0.172 s, `sub_elapsed` 0.263 s). A guard test that fails without any defect cannot be cited as evidence for criterion 2 or any handoff criterion.
* No contract defect: agent lines 147-151 already name every extended field.

Disposition: Planning Readiness Ready. Fix the flaky bounds (tools-only, focused tier); criterion 2 stays unproven.
