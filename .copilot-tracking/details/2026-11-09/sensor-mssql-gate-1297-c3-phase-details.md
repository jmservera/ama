---
title: Phase details - #1297 correction C3
date: 2026-11-09
---

## P01 Direct dependency selection and tests

* P01-T01: add `SENSOR_MSSQL_DIRECT_DEPENDENCIES = ("src/core/tests/dataset.py", "src/core/src/zava_forward/core/synthetic/__init__.py")` near the sensor constants and select mssql for exact path matches in `changed_groups`. Evidence: research C1.
* P01-T02: tests (add only, at most two, none removed): (1) AST (ast.walk, including nested imports) of the direct first-party imports of test_sensor_analysis_mssql.py, test_sensor_analysis_store.py and sensor_consumer_fixture.py; resolve bare names against src/core/tests and zava_forward.core.* against src/core/src; for `from pkg import n` add pkg/__init__.py or pkg.py and pkg/n.py only if they exist; assert each resolved path selects mssql, the set contains dataset.py, synthetic/__init__.py, mssqlstore.py and sensor_backfill.py, and the keyword-missed subset equals set(SENSOR_MSSQL_DIRECT_DEPENDENCIES); (2) negative paths src/core/tests/building_fixture.py, src/core/src/zava_forward/core/synthetic/climate_history.py and an api path (verified free of the five keywords) select no mssql, with project-core selected for the core ones. Critique PC-001 to PC-004 applied (see plan Critique Disposition).
* Validation: pinned ruff 0.17.1 (`--isolated --line-length 100`) lint and format check, mypy --strict, `cd tools && python3 -m unittest test_rpi_checks`.
