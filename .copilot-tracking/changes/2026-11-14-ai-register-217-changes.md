---
title: AI feature register changes (issue 217)
ms.date: 2026-11-14
---

## Changes

* `ai_registry.py`: `inputs`, `limits`, `owner` on every entry; completeness and fail-closed helpers.
* `ai.py`: `Ai.run` refuses unregistered features before any gate or model call (`registered=False`).
* `ai_tasks.py`, `agents/dispatch.py`: use the register's completeness check.
* Tests: new `test_ai_register_completeness.py`; `test_ai_input_bounds`, `test_ai_provider_payload_spy`, `test_data_protection` use registered names.

## Validation

* `src/core`: `mypy` clean (315 files), `ruff check` clean, `ruff format --line-length 100 --check` clean for touched formatted files.
* `src/agents`: `mypy` and `ruff` clean.
* Core suite: remaining failures are `test_device_registry_azure` (missing Azure IoT SDK) and one installed-command test; agents failures are `test_paired_report_command` subprocess tests. Neither involves the register; not rerun on baseline.
* Not run: full `tools/rpi-checks.py` gate, hosted CI. Tier: focused (small, no deployment or security-control change beyond fail-closed gating).
