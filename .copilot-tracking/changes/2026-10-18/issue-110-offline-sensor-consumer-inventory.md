---
title: Issue 110 offline sensor consumer full delivery inventory
description: Owned source, documentation and ordered RPI evidence inventory
ms.date: 2026-10-18
---

Pinned base: 578631ac75cc8c6a7af53922c6aaae4435e7761c.
Branch: feat/offline-sensor-consumer-110.
Final intended inventory: 23 paths. Original Review is pending at candidate commit;
its completed original and publication state are added without source correction.

## Source and tests (6)

* src/core/src/zava_forward/core/sensor_consumer.py
* src/core/tests/sensor_consumer_fixture.py
* src/core/tests/test_sensor_consumer.py
* src/api/src/zava_forward/api/sensor_ingestion.py
* src/api/tests/test_sensor_ingestion.py
* src/api/checks/sensor_sql_check.py

## Configuration (2)

* src/core/pyproject.toml
* src/api/pyproject.toml

## Documentation (6)

* src/core/README.md
* src/api/README.md
* docs/adrs/0003-journey-derived-capabilities-runtime-fit.md
* docs/case_study_48_addendum.md
* docs/reference/README.md
* docs/reference/log.md

## Ordered RPI evidence (9)

* .copilot-tracking/research/2026-10-18/issue-110-offline-sensor-consumer-research.md
* .copilot-tracking/plans/2026-10-18/issue-110-offline-sensor-consumer-plan.md
* .copilot-tracking/details/2026-10-18/issue-110-offline-sensor-consumer-phase-details.md
* .copilot-tracking/reviews/plans/2026-10-18/issue-110-offline-sensor-consumer-plan-critique.md
* .copilot-tracking/changes/2026-10-18/issue-110-offline-sensor-consumer-changes.md
* .copilot-tracking/changes/2026-10-18/issue-110-offline-sensor-consumer-inventory.md
* .copilot-tracking/reviews/2026-10-18/issue-110-offline-sensor-consumer-review.md
* .copilot-tracking/rpi-sessions/2026-10-18/issue-110-offline-sensor-consumer-log.jsonl
* .copilot-tracking/rpi-sessions/2026-10-18/issue-110-offline-sensor-consumer-state.json

## Preserved and excluded

No original case/memory, private env/data/support, shared sqlstore/mssqlstore,
governance/consultation/queue/recorder/DPIA source or existing tests, infra,
browser/UI, live SDK or transport change. Existing exact replay loader unchanged.
No issue/board/AC/merge/rebase/force-push action.
