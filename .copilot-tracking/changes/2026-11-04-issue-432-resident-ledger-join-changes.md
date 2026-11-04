---
title: "Changes: #432 resident adapter ledger join"
ms.date: 2026-11-04
---

* Edited `src/api/src/zava_forward/api/resident_demo/assistant.py` (optional `record_call`), added `resident_demo/ledger_meter.py`, added `src/api/tests/test_resident_ledger_meter.py` (6 tests), reworded one inventory description. No knowledge-base or log.md change.
* Validation (focused tier): the new tests, `test_resident_assistant_provider` and `test_ai_call_site_inventory` pass (26 tests); ruff check and format clean; `mypy --cache-dir=/tmp/mypy-432` from `src/api` (tests included, as CI) clean over 177 files. Not run: tools/rpi-checks.py gate, benchmarks, full suites, live Azure calls.
