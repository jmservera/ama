---
title: Issue 1251 R2 lint correction plan
description: Prospective plan to fix the hosted E501 and format failures and correct the focused validation selection
ms.date: 2026-11-07
ms.topic: reference
---

## Objective

Make `tools/test_backlog_sync.py` pass the exact existing workflow lint, format and type checks with identical behaviour.

## Context

* [Research](../../research/2026-11-07/issue-1251-r2-lint-correction-research.md), [details](../../details/2026-11-07/issue-1251-r2-lint-correction-details.md), [critique](../../challenges/2026-11-07/issue-1251-r2-lint-correction-critique.md).
* Amendment to the original [plan](issue-1251-inactive-conflict-plan.md): its unchecked phase boxes are the historical state at creation and were not retrofitted; completion is evidenced by the original changes and review records. The E9,F-only lint selection is superseded by the checks below. Original review and critique are preserved unchanged.
* Tier: FOCUSED small tooling. No FULL gate, services, scanners, browser, SQL, images, lock use or push.

## Phases

* [ ] Phase 1: commit this plan, details, research and critique before any source edit
* [ ] Phase 2: `ruff format --isolated --line-length 100` on the test file, manual split of the 106-character f-string; AST comparison with pre-correction
* [ ] Phase 3: run the checks on the final HEAD with external logs; changes record and one original R2 Review; commit

## Validation (final HEAD, `PYTHONDONTWRITEBYTECODE=1`, logs in `/mnt/ama-gates/g1251-ci-r2-1107`)

* `python3 -m unittest discover -s tools -p test_backlog_sync.py -v` (17 tests)
* `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` and `ruff format --isolated --line-length 100 --check` on all five tools files named in the workflow
* `mypy --strict tools/rpi-checks.py tools/test_rpi_checks.py`; `mypy --ignore-missing-imports tools/test_backlog_sync.py tools/backlog-sync.py`
* `test_rpi_checks.py` and `test_ci_affected.py` unit suites; `git diff --check`
* `rpi-checks.py --changed` not selected: not required and may queue; workflow lint above is the applicable set.
