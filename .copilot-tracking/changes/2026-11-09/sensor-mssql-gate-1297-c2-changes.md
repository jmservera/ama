---
title: Changes - #1297 correction C2
date: 2026-11-09
---

## P01 Apply pinned formatter and validate (complete)

* tools/rpi-checks.py: `ruff format --isolated --line-length 100` (ruff 0.17.1) collapsed the C1 `if (...)` condition in `changed_groups` to `if any(...) or (` plus the sensor operand. Diff is 2 insertions, 3 deletions, formatting only; selection semantics unchanged.
* tools/test_rpi_checks.py: no change.

## Validation (external scratch venv /tmp/ruff1297-c2 with ruff==0.17.1 and mypy==2.4.0, installed because the pins were absent locally; no SQL, Docker, browser or gate)

* Pre-fix reproduction: `ruff format --isolated --line-length 100 --check tools/rpi-checks.py tools/test_rpi_checks.py` exit 1, identical to the gate log hunk at lines 745-748.
* Post-fix, same command: exit 0, 2 files already formatted.
* `ruff check --isolated --no-cache --select E,F,I,B,UP --target-version py312 --line-length 100` on both files (0.17.1): exit 0.
* `python -m mypy --strict --cache-dir=/tmp/mypy-1297-c2` (2.4.0): exit 0, no issues.
* `cd tools && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_rpi_checks`: exit 0, Ran 99 tests OK.

## Adverse observations

* C1 validated with ruff 0.17.3 and without the format check, so the pinned-format failure was my omission.
* The critique step was skipped by recorded rationale (mechanical formatter change), not run.
* Artifacts were written with the create tool, but the plan checkbox was toggled with sed.
* The ignored tools/__pycache__/ (pre-existing) is retained; no new ignored files were created.
* Adverse historical evidence preserved: /mnt/ama-gates/g1297-c1-1109/receipt.json (SHA-256 be4c663d...cc0f), 0142-infra.log, /tmp/rpi-g1297-c1-full-1109.log.
