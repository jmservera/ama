# Changes: issue 2202 live2 (hardening check)

Tier: focused (tools only, no src change; no rpi-checks --all). Refs #2202. Nothing pushed; no Azure change.

## Files 

* tools/demo_preflight.py: add read-only `check_hardening` for API, resident, agents apps and live simulator and receiver jobs
* tools/test_demo_preflight.py: regression test
* docs/reference/research/issue-2202-live2-2026-11-23.md and folder, README index, log entry

Applied. Note: the first source edit was made before the witness calls and was reverted and reapplied after plan-done; the witness records that qualification. Tests: `python3 tools/test_demo_preflight.py` 8 pass; ruff check and format clean. Live preflight 13 pass, 0 fail, 2 unavailable.

## Per-criterion proven or unproven

| Criterion (#2202) | Status |
| --- | --- |
| Images rebuilt and rolled | Partly proven (new digests live; source commit not derivable) |
| Revisions Running and Healthy | Proven |
| Hardening enforced, rollback noted, agents difference explained | Proven enforced on API, resident, agents, both jobs; difference explained (idle, ScaledToZero); rollback not exercised |
| Sensor charts, map gauges, consent checkbox, chat routing, half of homes with readings | Unproven in this pass; see earlier notes |
| Live receipt and log entry | Proven |
