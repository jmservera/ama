---
title: Quality sensor values and review flag, fifth live audit (Refs #1288)
description: Fifth audit of the demo Quality sensor integration with a local test re-run, a read-only Azure probe and the per-criterion proven or unproven table
ms.date: 2026-11-19
---

Scope: synthetic demo, desktop only; docs and evidence only, FOCUSED tier. Follows the [fourth note](./issue-1288-live-r4-quality-sensor-evidence-2026-11-19.md).

## Result

The first unticked criterion is 3. Its code and tests already exist on main, so there is no source gap to build. Every remaining unticked criterion needs a model call, a release record or a simulator run, none of which the issue authorises.

| Criterion | Result for the demo | Evidence and limit |
| --- | --- | --- |
| 3 | Proven locally (mock provider); not proven live | Tests below; no live model call |
| 4 | Unproven | No approved release record (OQ-017); local dedup and bounds proven |
| 5 | Proven locally; not live | No live model output to display |
| 6 | Proven locally; stale and unavailable seen live in round 3 | Local tests, round 3 screenshot |
| 7 | Proven as local engineering evidence | Tests below |
| 8 | Unproven, cannot be proven for the demo | No simulator job, release or model call |

## Evidence (2026-11-19)

* Local engineering evidence (fixtures, mock provider), head `adb10ae6d`, from `src/api`: `python3 -m unittest tests.test_quality_sensor_grounding tests.test_quality_sensors_correlation tests.test_quality_sensors_c7 tests.test_quality_sensors_e1 tests.test_quality_sensors_e2` with the guide PYTHONPATH. Result: 272 tests, OK, 85 skipped (SQL Server and browser harness prerequisites).
* Azure CLI, read-only, resource group `ama`: jobs are init, verify, ledger-verify, import, orchestrator, smoke, mi-http and public-audit; no simulator job. Active revision of `ca-cutover-test-demo-api` is `--0000033`. Nothing was created or changed.
* No browser proof was repeated: no web file changed.

## Not demo work

Appointing the release approver, admitting a finite simulator run and recording a release are authority or Azure writes the issue does not grant. No tick or closure is claimed.
