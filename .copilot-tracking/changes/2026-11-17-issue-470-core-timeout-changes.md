---
title: Issue 470 core suite timeout changes
ms.date: 2026-11-17
---

* `tools/rpi-checks.py`: `SUITE_TIMEOUTS`, `suite_timeout()`; core unit suite 3600 s, others 1800 s at the planned contract and both runner sites.
* `tools/test_rpi_checks.py`: regression `test_core_unit_suite_gets_the_longer_timeout_in_the_planned_contract`.
* `src/README.md`: note on the ceiling and receipt impact.
* Validation: `python3 -m unittest tools.test_rpi_checks -q` 109 tests OK; `ruff format --isolated --line-length 100 --check` on both files clean. Full gate, mypy for src projects and SQL/browser checks not applicable here (FULL tier gate left to coordinator).
* Measurement: no local heavy reproduction (shared lock held); issue figures used as baseline.
