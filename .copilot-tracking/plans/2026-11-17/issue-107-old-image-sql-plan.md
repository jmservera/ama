---
title: Issue 107 old-image SQL probe plan
description: Plan for the bounded test-only actual older-image SQL probe
ms.date: 2026-11-17
---

## Objective

Add a test-only, fixed-argv probe that can execute the retained older API image against a task-owned disposable SQL Server while a separate current-source connection revokes or mutates release state, and light deterministic tests of its control logic. Refs #107 only.

Research: [research](../../research/2026-11-17/issue-107-old-image-sql-research.md). Details: [details](../../details/2026-11-17/issue-107-old-image-sql-details.md).

## Phases

* [x] Phase 1: in-image worker `src/api/checks/old_image_worker.py` (identify, provision, execute; structured JSON; protocol discovery; SQLite self-test mode).
* [x] Phase 2: host check `src/api/checks/old_image_sql_probe.py` (guards, owned SQL container, pinned image, fixed argv, named cases, classification, exit codes, adverse output kept).
* [x] Phase 3: `src/api/tests/test_old_image_sql_probe.py` (argv/guard/classification tests; worker self-test on SQLite with explicit lower fidelity).
* [x] Phase 4: `src/api/README.md` short section with the exact continuation and outcome meanings.
* [x] Phase 5: lint, format, mypy, targeted tests, changes record, one Review, commit.

## Boundaries

* No production, schema, policy, UI, cloud or gate-semantics change; not registered in `tools/rpi-checks.py`; unit discovery never runs or substitutes the actual check.
* Actual-image and disposable-SQL execution is not performed here; the result is FULL / ACTUAL OLD-IMAGE SQL EVIDENCE MISSING, NOT PUBLISHABLE.
* Child targets `feat/assistant-107-integration` (pinned 1c9ac230be1dad9a4ecc21975f9ffe0845309fc4), never silently main.

## Validation

Ruff check and format, mypy for the new files, the new unit module plus the existing `test_assistant_restart_non_replenishment` and `test_assistant_release` modules. Full gate and actual SQL/image run belong to the coordinator.
