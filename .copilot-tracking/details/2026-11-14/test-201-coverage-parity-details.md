---
title: Issue 201 coverage baseline parity details
ms.date: 2026-11-14
---

## Phase 1

* Per-project: test modules exist, `test_dependency_rule.py` present, `dev` extra declared.
* `src-ci.yml` matrix includes all five with `run:true` and discovery command; `tools/rpi-checks.py` `PROJECTS` equals the five.
* Floors: total >= 719; per project >= 504 / 70 / 549 / 22 / 39 (core/agents/api/orchestrator/importer) via static AST method count.
* Thresholds: any configured coverage `fail_under` must be non-negative; CI has no weakened coverage flags; disclosure sentence preserved while no threshold exists; rubric total >= 48.

## Phase 2

Validation commands per the task statement.
