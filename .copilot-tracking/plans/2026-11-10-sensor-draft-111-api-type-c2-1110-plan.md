---
title: Issue 111 API typing C2 plan
ms.date: 2026-11-10
task_id: 111-api-type-c2-1110
---

## Objective

Smallest fix of the single no-untyped-call error. Research: [research](../research/2026-11-10-sensor-draft-111-api-type-c2-1110-research.md). Details: [details](../details/2026-11-10-sensor-draft-111-api-type-c2-1110-details.md). Critique: [critique](critiques/2026-11-10-sensor-draft-111-api-type-c2-1110-plan-critique.md).

## Tier

Owner DEMO targeted. Typing-only test-file change; no dependency, runtime, schema, workflow, UI or production change. No full discovery, full gate or `--changed`. The 22 MSSQL cases carry forward from `2b050647b` because no runtime, test-behaviour or dependency input changes (diff proof is one comment-and-ignore line); they are not rerun.

## Change

In `src/api/tests/test_sensor_review_draft_api.py` line 63 add an exact-call, exact-code `# type: ignore[no-untyped-call]` with a justification comment on the legacy untyped `App` constructor, matching `tests/scale_load.py:102`. No `Any`, `cast`, fake constructor, module-wide pattern, `pyproject.toml` or production edit.

## Phases

* [ ] Plan, details, one critique, witness `plan-done`.
* [ ] Implement: prospective changes recorded, witness `implement-start`, edit, validate, complete changes, witness `implement-done`.
* [ ] One review, witness `review-done`; commit, literal HEAD, witness `commit-complete`, verify.

## Checks

1. Reproduction on unchanged head (done, exit 1, one error).
2. After fix, from `src/api`: `mypy --no-incremental --cache-dir <ext>` (full API project, expect exit 0).
3. `PYTHONPATH=../core/tests:../agents/tests python -m unittest tests.test_sensor_review_draft_api` (6 cases).
4. `ruff check` and `ruff format --check` on the touched file.
5. `node --check` of unchanged `ops.js` (syntax only).
6. `python -m checks.quality_sensors_browser_check` under own `flock -n /tmp/ama-rpi-heavy.lock` admission after an holder check; BUSY stops that check; failure stops for Root without repair.
