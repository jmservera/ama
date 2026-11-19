---
title: Quality sensor values and review flag, fourth live audit (Refs #1288)
description: Fourth audit of the demo Quality sensor integration with a local test re-run, a read-only Azure probe and the per-criterion proven or unproven table
ms.date: 2026-11-19
---

Scope: synthetic demo, desktop only; docs and evidence only, FOCUSED tier. Follows the [third note](./issue-1288-live-r3-quality-sensor-evidence-2026-11-18.md).

## Result

The first unticked criterion is 3. Its code and tests already exist on main, so there is no source gap to implement. Its live proof needs a model call, which stays held.

| Criterion | Result for the demo | Evidence and limit |
| --- | --- | --- |
| 3 | Proven locally (mock provider); not proven live | Tests below; no live model call |
| 4 | Unproven | Release gate held, no approved release record (OQ-017); local dedup and bounds proven |
| 5 | Proven locally; not live | No live model output to display |
| 6 | Proven locally; stale and unavailable seen live in round 3 | Local tests, round 3 screenshot |
| 7 | Proven as local engineering evidence | Tests below |
| 8 | Unproven, cannot be proven for the demo | No simulator job, release or model call |

## Evidence (2026-11-19)

* Local engineering evidence (fixtures, mock provider), head `06188c533`, from `src/api`: `python3 -m unittest test_quality_sensors_correlation test_quality_sensors_c7 test_quality_sensors_e1 test_quality_sensors_e2 test_quality_simulation_lane test_quality_sensor_grounding` with the guide PYTHONPATH. Result: 304 tests, OK, 85 skipped (SQL Server and browser harness prerequisites; those runs stand from the first note).
* Azure CLI, read-only, resource group `ama`: jobs are init, verify, ledger-verify, import, orchestrator, smoke, mi-http and public-audit, all manual; no simulator job. Active revision of `ca-cutover-test-demo-api` is `--0000033`. Nothing was created or changed.
* No browser proof was repeated: criteria 1 and 2 are ticked and the round 3 screenshot stands; no web file changed.

## Not demo work

Appointing the release approver, admitting a finite simulator run and recording a release would each be an authority or Azure write the issue does not grant. No tick or closure is claimed.
