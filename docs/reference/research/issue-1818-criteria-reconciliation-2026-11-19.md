---
title: Issue 1818 criteria reconciliation, 2026-11-19
description: Per-criterion proven/unproven reconciliation for the IoT map and resident sensor view, with a correction that the receiver register fix is on main
ms.date: 2026-11-19
---

## Scope

Refs #1818. Synthetic demo, desktop only, within the owner authority of 2026-11-18. This pass created no Azure resource and changed no source, so nothing needs deleting and the focused tier applies. It adds no new live traffic; it reconciles the existing retained evidence against the open criterion.

## Correction

The [2026-11-19 re-observation](issue-1818-live-20261119-2026-11-19.md) and the [receiver fix note](issue-1818-sensor-register-receiver-fix-2026-11-18.md) say the receiver register fix is not on `main`. On this base it is: `git log -S"INSERT INTO sensor_register"` on `src/core/src/zava_forward/core/sensor_consumer.py` returns `e91b6fa81` (#2105), and `infra/README.md` lists `dbo.sensor_register` in the receiver grants. No code change remains for #1818. The earlier notes are kept unchanged as the adverse record.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 `/api/map` bounded, permission-projected sensor summary | Proven (demo) | 13:24 UTC read: 443 items, states stale 3, restricted 97, not-loaded 343 ([note](issue-1818-live-20261119-2026-11-19.md)) |
| 2 Map card, accessible list and stale filter with non-colour cues | Proven (demo) | same note; filter text "3 of 443 homes have a stale or offline sensor." |
| 3 Resident `#sec-sensors` freshness, provenance, single home | Proven (demo) | same note; no second `ZF-` id visible |
| 4 Unit/API tests and browser/axe checks on exact HEAD | Unproven here | ticked by #1826; no web or source change in this pass, so not re-run |
| 5 Live Hub to SQL to UI walkthrough | Proven for the demo from the [2026-11-18 round](issue-1818-live-iot-map-walkthrough-evidence-2026-11-18.md); sending leg not repeated today | The 10:50 UTC readings are served from Azure SQL; which job wrote them is not shown by today's read. The owner ticks the criterion |

## Not proven

* No telemetry was sent in this pass, so the Hub to SQL leg is not re-observed.
* The receiver minimum-grant SQL test needs SQL Server, which was unavailable; the full gate was not run (`rpi-checks.py --all` is out of scope).
