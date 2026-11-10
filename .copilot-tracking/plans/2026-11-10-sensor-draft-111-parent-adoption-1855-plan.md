---
title: Issue 111 parent adoption plan
ms.date: 2026-11-10
task_id: 111-parent-adoption-1855
---

## Objective

Ordinary `--no-ff` merge of declared parent `feat/demo-sensor-review-109-1110` (`06374dfcac47cf6bcce9e7b91f573e8565ab45e8`, equal to `origin/main`) into child head `325cb5c0c3efcd666145fe234c8fded1b50db89d`, then targeted validation of the final composition. Research: [research](../research/2026-11-10-sensor-draft-111-parent-adoption-1855-research.md). Details: [details](../details/2026-11-10-sensor-draft-111-parent-adoption-1855-details.md). Critique: [critique](critiques/2026-11-10-sensor-draft-111-parent-adoption-1855-plan-critique.md).

## Classification and tier

Owner DEMO focused tier. The merge brings parent main-composition changes only; no workflow, dependency, Dockerfile, permission or schema line is authored here. Persistence and main composition changed, so the MSSQL draft selectors run actually. No full gate, `--changed`, full discovery, unrelated browsers or images, cloud, credentials or private data.

## Steps

* [ ] Phase 2: plan, details, one critique, witness `plan-done`.
* [ ] Phase 3: prospective changes record, witness `implement-start`; then `git merge --no-ff` the declared parent; parse TOML; resolve only mechanical overlap, preserving both intents; stop for Root on any substantive conflict or discovered defect; run checks; complete changes record; witness `implement-done`.
* [ ] Phase 4: one Review, witness `review-done`; commit the merge and records, obtain the literal 40-hex HEAD, witness `commit-complete`, verify.

## Planned checks (exact, from `src/core` unless stated, `/tmp/zf-111-1110/venv`, `PYTHONDONTWRITEBYTECODE=1`, external caches)

1. Import origin asserted in this worktree for `zava_forward.core.sensor_review_draft`; `tomllib` parse of `src/core/pyproject.toml`.
2. `PYTHONPATH=src:tests python -m unittest tests.test_sensor_review_draft` (expect 65 discovered, 22 MSSQL skipped locally).
3. `PYTHONPATH=src:tests python -m unittest discover -s tests -p 'test_sensor_analysis*.py'`.
4. From `src/api`: `PYTHONPATH=../core/tests:../agents/tests python -m unittest tests.test_sensor_review_draft_api` (server, projection and ops.js were touched by this feature and by the merge).
5. `ruff check .`, `ruff format --check .`, `python -m mypy --no-incremental --cache-dir <external>` from `src/core` (configured full Core mypy; scoped exemption disclosed).
6. Actual MSSQL: one non-queued `flock -n /tmp/ama-rpi-heavy.lock` admission of a task-owned script with an own disposable container; `tests.test_sensor_review_draft.MssqlDraftCases` with `ZF_SENSOR_DRAFT_MSSQL=1`. Pass needs all discovered cases run, 0 skips, exit 0. BUSY or missing prerequisite is reported and stops that check.
7. The served sensor browser check only if the merge changes its served surface or recipe; otherwise stated as not run.

## Stop rules

Substantive conflict, discovered source, config or test defect, or a refused marker: stop, preserve evidence, no repair, no remaining-budget use.
