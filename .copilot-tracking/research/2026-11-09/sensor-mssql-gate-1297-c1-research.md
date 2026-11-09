---
title: Research - #1297 correction C1 (changed-selection gap)
date: 2026-11-09
task: issue-1297 correction C1
---

## Brief

* Purpose: verify independent finding (Medium) that the exact sensor discovery skip exemption lets `--changed` pass for sensor-analysis changes while `changed_groups` omits `mssql`.
* Posture: focused (bounded internal task, named failure evidence). Inline, no delegation.
* Preserved: original RPI artifacts under `.copilot-tracking/*/2026-11-08/`, prior receipt `/mnt/ama-gates/g1297-fdf-1108/receipt.json` and log `/tmp/rpi-g1297-full-1108.log` (historical, not proof for a new head).
* Non-goals: #184 two inherited sensor methods, `DEFAULT_TESTS` conflict, any heavy run.
* Start state verified: HEAD fdf9cf1220c74287aa33e8e976ded1565fc70b5e, tree b7234783bf733b1fff1723778b3b2138b545515a, parent fa7ae0c97, `git status --short --ignored` empty.
* Source: functional-findings.json (read as data).

## Extensions

Selected: repository AMA instructions (RPI gate rules). Skipped: web guidance (no web work), specialists (no independent uncertainty).

## Findings

* C1: `tools/rpi-checks.py` `changed_groups` selects `mssql` only for core/api requirement or pyproject files, or paths containing store, schema, sql, assistants (~line 743-747).
* C2: `check_skips` exempts the eight sensor pairs for `project-core` non-integration regardless of whether `mssql` was selected (original change).
* C3: Reproduced by calling `changed_groups` with single paths (exit 0):
  * `src/core/src/zava_forward/core/sensor_analysis.py`: no `mssql`.
  * `src/core/tests/sensor_consumer_fixture.py`: no `mssql`.
  * `src/core/src/zava_forward/core/sensor_consumer.py`: no `mssql`.
  * `src/core/src/zava_forward/core/synthetic/sensor_faults.py`: no `mssql`.
  * `.../sensor_analysis_store.py` and `tests/test_sensor_analysis_store.py`: `mssql` selected (name contains "store").
  * `src/core/.../sqlstore.py`: `mssql` selected.
* C4: The retained suite imports `test_sensor_analysis_store`, `sensor_consumer_fixture`, `sensor_analysis_store` (which imports `sensor_analysis`, `sensor_consumer`, `synthetic.sensor_scenarios`); the fixture imports `synthetic.sensor_backfill` and `sensor_faults`, and `sqlstore` (already selected).
* C5: Result before this correction: such a `--changed` run selects project-core, accepts the eight skips and never runs the flagged SQL command. A full receipt still requires MSSQL, so this is lost focused coverage, not a false full pass. Finding verified.
* C6: Api sensor modules (`src/api/**/sensor_*`) are not imported by the retained core suite; `project-api` runs them.

## Alternatives

* A. Select `mssql` for every `src/core` path whose lowercase path contains `sensor` (covers analysis, consumer, synthetic sensor modules, fixture, all sensor tests). Minimal, fail-closed, one-line, over-selection only costs a heavier focused run. Selected.
* B. Make `check_skips` require `mssql` in the selected groups. Rejected: skip checker has no selection context and receipt contract/verification would change.
* C. Exact path list of the suite's import closure. Rejected: brittle, new import silently loses coverage.
* D. Select `mssql` for api sensor paths too. Rejected: no evidence the core suite exercises them; widens scope.

## Decision state

Research disposition: executed. Planning Readiness: Ready. Residual risk: modules outside `sensor` naming that the suite imports (`dataset`, `sqlstore` is covered); recorded for review.
