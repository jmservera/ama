---
title: Sensor non-authority and reproducibility changes (Refs #109, #111)
date: 2026-11-14
---

## Changes

* `src/core/src/zava_forward/core/sensor_analysis.py`: `derive_signal` sorts home rows canonically before analysis, closing the digest-versus-output gap.
* `src/core/tests/test_sensor_analysis_reproducibility.py`: new, 6 tests.
* `src/api/tests/test_sensor_non_authority_boundary.py`: new, 4 tests.

## Validation (focused tier)

* Core `test_sensor*`, `test_ranking*`, `test_hazard*`, `test_household*`: pass. API `test_sensor*`, `test_hazard*`: pass. New suites: pass (the reproducibility suite ingests real rows and takes about 2 to 4 minutes).
* `ruff check`, `ruff format --check` and `mypy --cache-dir /tmp/mypy-109` clean for `src/core` and `src/api`; `/tmp/mypy-109` removed.
* Not run: SQL Server variants (`ZF_SENSOR_MSSQL`), full `rpi-checks.py` gate, hosted CI. `ruff format --check` from `src/` reports one pre-existing unformatted file outside this change.
* Not pushed; local commit only.

## Divergences

* Shuffled arrival cannot be proven identical at ingestion: the consumer rejects out-of-order rows by design. Order independence is proven over retained rows instead, and shuffled arrival is proven to fail closed.
