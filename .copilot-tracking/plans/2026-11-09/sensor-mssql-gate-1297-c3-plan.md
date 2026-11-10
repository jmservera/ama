---
title: Plan - #1297 correction C3
date: 2026-11-09
task_id: issue-1297-c3
---

## Executive Summary

Make the focused selection contract cover the two direct dependencies of the sensor MSSQL suite that the `sensor` keyword misses: tests/dataset.py and synthetic/__init__.py. Add an AST-derived regression so any direct first-party import of the suite must select mssql. No transitive-closure claim; the wider closure policy (roughly half of core runtime) is reported as an owner decision. Full gate, skip, selector and execution safeguards unchanged.

## User Decisions and Requirements

* Minimal fail-closed selection covering direct shared dependencies; tests for the dataset case, sensor tests and unrelated paths; no unsupported claim of full closure; stop and report if a cost policy decision is needed (it is only for alternative B, not chosen).
* Research: .copilot-tracking/research/2026-11-09/sensor-mssql-gate-1297-c3-research.md.

## Goals

Direct dependencies of the retained sensor MSSQL suite select mssql in `changed_groups`.

## Scope and Non-Goals

* In: tools/rpi-checks.py `changed_groups` and a named constant; tools/test_rpi_checks.py.
* Out: check_skips, matrix, receipt format, closure-wide selection, #184.

## Functional Requirements

* `src/core/tests/dataset.py` and `src/core/src/zava_forward/core/synthetic/__init__.py` select mssql.
* Unrelated paths (core timeline.py, other core tests, api/agents paths) do not.

## Non-Functional Requirements

* Pinned ruff 0.17.1 lint and format (gate flags), strict mypy 2.4.0, tools tests; no new ignored files.

## Acceptance Criteria

* Regression: AST-derived direct first-party imports of the three suite files all select mssql; dataset.py case explicit; unrelated paths do not select mssql.
* Existing C1 tests still pass.

## Phase Checklist

* [x] P01 Direct dependency selection and tests

## Critique Disposition

Critique: .copilot-tracking/plans/2026-11-09/sensor-mssql-gate-1297-c3-critique.md (one run, verdict Revise, no second critique). All findings are direct planner corrections.

* PC-001 accepted: the AST test uses ast.walk (nested imports), resolves bare names against src/core/tests and zava_forward.core.* against src/core/src, and for `from pkg import n` adds pkg/__init__.py (or pkg.py) and pkg/n.py only when they exist. It asserts the resolved set contains dataset.py, synthetic/__init__.py, mssqlstore.py and sensor_backfill.py.
* PC-002 accepted: the test asserts equality between the resolved paths that the keyword rule alone misses and set(SENSOR_MSSQL_DIRECT_DEPENDENCIES).
* PC-003 accepted: negative paths are named: src/core/tests/building_fixture.py, src/core/src/zava_forward/core/synthetic/climate_history.py and an api path, each checked to contain none of store, schema, sql, assistants or sensor; the test asserts project-core is selected and mssql is not. Paths found not to exist or to match a keyword are replaced and recorded in the changes record.
* PC-004 accepted: the research import and closure counts (15 of 17, 67 of 128) are caveated as script-derived and not independently reproduced; the critic counted 13 unique direct modules. The two misses are confirmed. Policy alternative B is reported with that caveat.

## Follow-Up Items

* Owner policy option: closure-wide or project-core-wide mssql selection (cost/coverage).
* Coordinator: fresh current-base full gate; #184 overlaps unchanged.
