---
title: Changes, issue 152 per-profile default manifest slice
ms.date: 2026-11-03
---

## Changes

* Modified `src/api/checks/workbench-manifest.json` (per-profile defaults).
* Modified `src/api/tests/test_workbench.py` (one test).
* Modified `src/api/README.md` (manifest paragraph).

## Divergences

None. No knowledge-base files changed, so no log.md entry.

## Validation

* Run: `python -m unittest tests.test_workbench` (5 tests, OK); `ruff check`; `ruff format --check`; `mypy --cache-dir=/tmp/mypy-152` on the test file.
* Not run: browser checks (manifest change does not alter them), full suites, benchmarks, RPI gate. Slice is not security, infrastructure, SQL or deployment, so the focused tier applies; independent review, hosted CI and owner approvals remain required.

## Acceptance criteria

* Unmet: criterion 1 (owner decision on supported devices) and criterion 5 (full AC-034/AC-043 execution; eight workflows and several profiles remain deferred or partial). Criteria 2 to 4 stay as ticked by earlier merged evidence.
