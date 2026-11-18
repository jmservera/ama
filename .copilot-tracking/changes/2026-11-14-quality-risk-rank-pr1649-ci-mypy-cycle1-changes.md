# Changes: PR 1649 Cycle 1 (Refs #111)

* Fixed hosted `src-agents` mypy `type-arg` errors: `list[dict]` became `list[dict[str, Any]]` in `src/agents/src/zava_forward/agents/quality_sensor_risk.py` and `list[dict[str, object]]` in `src/agents/tests/test_quality_sensor_risk_explanation.py`.
* Local checks from `src/agents`: `mypy` clean (59 files); `ruff check` and `ruff format --check` pass; the 5 explanation tests pass (run with `PYTHONPATH=src:../core/tests:../core/src` because the installed package points at another worktree).
* Not pushed; hosted CI on the new head unobserved.
