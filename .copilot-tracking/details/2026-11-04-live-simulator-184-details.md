---
title: Details for #184 live simulator container slice 1
ms.date: 2026-11-04
---

* Generator `core/synthetic/live_readings.py`: `DailyAverages` to 24 hourly anchors (mean preserved), smoothstep interpolation, seeded 30-minute noise knots eased between, per-home offsets, 5-minute UTC slot alignment, `Reading.row()` and `body()`.
* Runner `api/live_simulator.py`: `Sink` protocol, `MemorySink`, `StdoutSink`, `IotHubSink` (X.509 files from `ZF_SIM_CERT_DIR`), `Limits`, `check_capacity`, `Pacer`, `send_slot` (batches, throttle, backoff), `store_home_ids`, `run`, `main`.
* `src/api/live-simulator.Dockerfile` (context `src/`, hashed requirements, non-root, dry-run default command).
* `infra/live-simulator-job.bicep` (compile and lint only).
* Tests: `core/tests/test_live_readings.py`, `api/tests/test_live_simulator.py`.
* Docs: `src/api/README.md`, `infra/README.md`, research plan section, `docs/reference/log.md`.
