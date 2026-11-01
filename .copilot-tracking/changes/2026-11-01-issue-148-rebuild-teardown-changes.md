# Changes: issue 148 rebuild and teardown automation (2026-11-01)

Plan: [plan](../plans/2026-11-01-issue-148-rebuild-teardown-plan.md)

## Added

* `src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py`: Azure adapter, secret-argv and synthetic guards, dry-run default, `--apply`, `--from-stage` resume, operator-gated stop (exit 2).
* `src/orchestrator/tests/test_rebuild_azure.py`: 19 tests against a stateful fake `az`.

## Modified

* `infra/README.md`: scripted rebuild/teardown section; criteria status updated.

## Validation

* Orchestrator unittest: rebuild, rebuild_azure and dependency-rule suites pass (44 tests). Full discovery with core/agents test paths: 88 run, 1 error in `test_version` because the distribution is not pip-installed locally (unrelated to this change).
* `ruff check`, `ruff format --check`, `mypy src` for `src/orchestrator`: clean.

## Divergences

* None from plan. No live Azure run (not authorised).
