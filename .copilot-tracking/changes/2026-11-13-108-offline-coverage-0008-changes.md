# Changes: 108 offline coverage 0008 (2026-11-13)

## Files changed

* `src/agents/src/zava_forward/agents/ai_eval.py`: spy-observed dispatch plus final-outcome eligibility; `task_coverage` (registry-derived, `EXERCISED`, `FALLBACK_ONLY`, `NOT_EVALUATED`); `evidence.task_coverage`; `passed` also requires no coverage failures or namespace errors; scripted `funding_draft` and `read_document` checks on constructed public fixtures; truthful docstring; CLI coverage output.
* `src/agents/tests/test_ai_eval.py`: `TaskCoverageTests` (6 tests).
* `src/agents/README.md`: coverage note with limits.
* `docs/reference/log.md`: appended 2026-11-13 entry.

## Validation (focused tier)

* Failing-first: 3 failures and 3 errors before implementation (`108-offline-coverage-0008-failing-first.log` in the evidence root).
* After: `test_ai_eval` and `test_eval_registry` 28 OK; full agents suite 336 OK (`PYTHONPATH=tests:../core/tests`, because the documented core-first order shadows `test_dependency_rule` on discovery; the unchanged-code import clash is pre-existing); `test_dependency_rule` and `test_eval_registry` OK; ruff clean; mypy clean (ai_eval and its test are excluded from strict mypy and ruff-format by existing config).
* Denominators unchanged: 11 scenarios, 10 priority, 14 runs.

## Divergences and process notes

* Funding check initially reviewed a stale draft record; fixed to review the latest record.
* Process slip: early test edits used `sed -i` and `cat >>` through bash instead of the edit tool. Content verified by diff; no later slips.
* Recipe-hash metadata not required; no dependency, workflow, gate or tool change.
* Pip editable installs left ignored `egg-info` folders only.
