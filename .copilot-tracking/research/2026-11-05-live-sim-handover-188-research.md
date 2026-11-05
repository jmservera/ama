---
title: Research for #188 live-sim handover omission
ms.date: 2026-11-05
---

* Research disposition: executed (source reading plus focused reproduction at head 40e6a35f4). Planning Readiness: Ready.
* Trigger: coordinator found a success-shaped omission in the retained round-trip split (prior slice live-sim-roundtrip-188, preserved unchanged). `sensor_handover_verify.run` passed `observed_series`, which excludes every live-sim row, to `report`, so the statistics silently omitted live rows.
* Reproduced: a store holding the backfill window plus one live row beside it returned `passed=true, idempotent=true` from `run(..., replay_check=True)`. That proved raw replay only. `sensor_consistency._index` accepts only the indoor schema with `calibrated=true`, so the result could not show live weather-to-backfill handover.
* Boundary: weather rows are not indoor measurements. No calibration is invented, no weather-to-indoor model, no physically incompatible reference comparison. A weather-to-weather versioned reference/continuity contract is separate, unapproved future research.
* Existing CLI pattern: `ValueError` code from `run` prints `{"passed": false, "refused": CODE}` and exits 2.
* Not run: FULL gate, SQL Server, browser, build. #96 PID 1232396 holds heavy resources. No private dataset read.
