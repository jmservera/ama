---
title: Issue 188 live handover verifier plan
ms.date: 2026-11-01
---

* Research: ../../research/2026-11-01/2026-11-01-issue-188-live-handover-verifier-research.md
* [x] Phase 1: add `SensorConsumer.observed_series(home_ids)`, a read-only ordered query returning canonical 13-field rows with trusted control units (SQLite and mssql datetimes normalised to UTC `Z`).
* [x] Phase 2: add `zava_forward.api.sensor_handover_verify` (`run(store, ...)` plus `python -m` CLI): joint query per home, `report` with declared tolerances, optional `--replay-check` that re-feeds the reference window and asserts unchanged row counts and an identical series. Exit 0 pass, 1 numeric fail, 2 refusal.
* [x] Phase 3: extend `test_sensor_consistency.py` to use both; add a failing-tolerance control and a refusal control; document in the API README and the research plan without changing issue checkboxes.
* Critique (single pass, recorded in the changes file): compatible findings applied directly.
* Validation: focused unittest, ruff check, ruff format --check, mypy for src/core and src/api.
