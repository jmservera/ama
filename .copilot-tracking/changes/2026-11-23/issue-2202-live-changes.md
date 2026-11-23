# Changes: issue 2202 readings coverage tool

Refs #2202. Tools and docs only; no src change (focused tier, no rpi-checks --all). No Azure change; nothing pushed.

## Files

* tools/demo_readings_coverage.py, tools/test_demo_readings_coverage.py (4 tests, OK; ruff clean)
* docs/reference/research/issue-2202-live-2026-11-23.md and folder (probes, tiles, coverage-result.json, screens)
* docs/reference/README.md, docs/reference/log.md
* .copilot-tracking research, plan, details, critique, changes, review, state

## Per-criterion proven or unproven

| Criterion (#2202) | Status |
| --- | --- |
| Images rebuilt and rolled | Unproven here: API 0058 and resident 0028 are running; jobs and source commit not checked |
| Revisions Running and Healthy; hardening; rollback; agents difference | Partly proven: 0058 and 0028 Healthy, Running; hardening, rollback not rechecked |
| Sensor charts | Not re-proven here (proven earlier on 0025) |
| Map gauges | Unproven: card with gauge not opened in this pass |
| Consent checkbox | Proven on resident 0028 |
| Chat routing | Not re-proven here (proven earlier) |
| Half of homes with readings | Proven: 261 of 443 (58.9%), all homes measured |
| Live receipt and log entry | Proven: note and log entry added |
