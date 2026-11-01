---
title: Issue 189 publisher wiring changes
ms.date: 2026-11-01
task_id: issue-189-publisher-wiring
---

## Changes

* `src/api/src/zava_forward/api/iot_stream.py`: added `HubPublisher.run_controlled`, which starts a `RunController` (refusing without a matching recorded estimate), runs with the plan budget and controller pacer, and always stops the controller.
* `src/api/tests/test_iot_stream.py`: two tests (no estimate refuses and creates no client; recorded estimate publishes and leaves the controller stopped).

## Validation

`tests.test_iot_stream` 30 tests OK; `ruff check`, `ruff format --check` clean for src/api; mypy clean on touched files. Full api suite and heavy gate not run (CI is the evidence).
