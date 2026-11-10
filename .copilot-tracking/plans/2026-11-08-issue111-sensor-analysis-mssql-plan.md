---
title: Issue 111 sensor analysis MSSQL test increment, plan
ms.date: 2026-11-08
---

Research: [research](../research/2026-11-08-issue111-sensor-analysis-mssql-research.md). Details: [details](../details/2026-11-08-issue111-sensor-analysis-mssql-details.md).

* [ ] Add `src/core/tests/test_sensor_analysis_mssql.py`: subclass of the existing `RetainedAnalysisTests`, MSSQL setup, backend assertion, deliberate drop restored, one reopened-store reproducibility test
* [ ] Extend `src/api/checks/sensor_sql_check.py` with an allowlisted `--selector` (`default`, `analysis`) and result validation for `analysis`; default selection and cleanup unchanged
* [ ] Add `src/api/tests/test_sensor_sql_check.py` for selection and result validation
* [ ] Document the selector in `src/api/README.md`
* [ ] Run unit, Ruff, format and mypy on changed files
* [ ] Run the eight methods on a disposable loopback SQL Server under the heavy lock
* [ ] Record changes, review and commit locally (no push)

## Critique (executed once, before implementation)

Verdict: compatible, with three findings applied directly.

* Subclassing keeps one copy of the behavioural assertions, but `setUp` skips on MSSQL, so the subclass must replace `setUp` rather than call `super().setUp()`. Applied.
* The harness must not trust the unittest exit code alone: `OK (skipped=N)` exits 0. Validate `Ran 8 tests`, `OK` with no skip suffix. Applied. Validation applies only to the new selector, so the default selection keeps its exact behaviour.
* A generic `--module`/test-name argument would run arbitrary modules and is rejected; a closed `choices` selector is the simplest narrow interface. Applied.
* Captured unittest output must not echo the generated password. Redact before printing. Applied.
* Rejected: editing `test_sensor_analysis_store.py` or `sensor_consumer_fixture.py` to share setup (outside the authorised scope).
