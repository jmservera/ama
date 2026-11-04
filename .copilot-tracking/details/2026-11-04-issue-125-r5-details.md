---
title: Issue 125 round 5 details
ms.date: 2026-11-04
---

## Phase 1

* `compare_methods(results)`: validates measure and method against fixed tuples, rejects unknown, duplicate and placeholder or malformed pointers (counted as invalid, not accepted), returns measures comparable only when all four methods have a pointer, and the incomplete map otherwise.
* `check_repeatability(calculation, dataset, runs=3)`: SHA-256 of canonical JSON per run; requires at least two runs.
* No I/O, model, clock or store. Manual path text included in the report.

## Phase 2

* README section under the existing #125 section (also closes the previously unclosed code fence); log entry appended.

## Phase 3

* `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_discovery_assistant_*.py' -q` from src/core; ruff check and format; mypy `--cache-dir=/tmp/mypy-530`.
