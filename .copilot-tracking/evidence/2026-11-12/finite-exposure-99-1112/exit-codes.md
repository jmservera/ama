---
title: Command log and explicit exits (issue 99 finite guard)
description: Commands run, in order, with explicit exit codes; raw outputs sit beside this file
ms.date: 2026-11-12
---

Run from `src/core` with venv `/tmp/f99/venv` (outside the repository). Commands were run unpiped with `> file 2>&1; echo exit=$?`, so exits are the command's own.

| Step | Command | Exit | Output file |
| --- | --- | --- | --- |
| venv | `python3 -m venv /tmp/f99/venv` | 0 | none |
| install | `pip install -q -e src/core ruff mypy` (repo root) | 0 | pip.out |
| pin tools | `pip install -q ruff==0.17.1 mypy==2.4.0` | 0 | none kept |
| reproduce | `python /tmp/f99/repro.py` (before fix) | 0 (defect shown) | repro-before.out |
| failing-first 1 | `python -m unittest tests.test_exposure_limits -v` | 1 | test-before.out |
| mypy on first fix (type() plus isfinite) | `mypy <2 files>` | 1, two arg-type errors (lines 138, 156) | not kept; reworked |
| overflow check on candidate v2 | inline python, committed=10**400 | 1 OverflowError | bigint-overflow-candidate-v2.out |
| failing-first 2 | `python -m unittest tests.test_exposure_limits` | 1 | test-before-bigint.out |
| format check on helper version | `ruff format --check <2 files>` | 1 (one line wrapping) | ruff-format-fail-1.out |
| final format | `ruff format <file>` | 0 | none |
| final tests | `python -m unittest tests.test_exposure_limits -v` | 0 (16 tests OK) | test-after.out |
| final ruff check | `ruff check <2 files>` | 0 | ruff-check.out |
| final ruff format check | `ruff format --check <2 files>` | 0 | ruff-format.out |
| final mypy | `mypy <2 files>` | 0 | mypy.out |
| reproduction after | `python /tmp/f99/repro.py` | 0 (all nonfinite now Unknown) | repro-after.out |
| neighbouring finance tests | `python -m unittest discover -s tests -p "test_finance*.py" -q` | 0 (78 tests, skipped=19, skip reasons not examined) | test-finance.out |

The earlier test-after.out from the first (pre-helper) fix was overwritten by the final run.
