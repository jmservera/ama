---
title: Issue 1288 trend Cycle 1 mypy changes
ms.date: 2026-11-14
---

Changed src/api/tests/test_sensor_trend_summary.py only: dropped the test_quality_sensors import. Results: 10 focused tests OK; core and api ruff check, ruff format --check and mypy exit 0 (api mypy over src and the test file). No full discover and no rpi-checks run.
