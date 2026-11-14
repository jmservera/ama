# Plan: deploy.py --dry-run

1. Extract `deployment_command` and add `dry_run_plan` (no az, network or file access; deterministic text).
2. Add `--dry-run`, rejected together with `--apply`; image unresolved shows `<resolved-at-run-time>`.
3. Tests in `infra/tests/test_deploy.py`: zero az calls, identical output across runs, apply conflict exits 2.
4. Document in `infra/README.md`; keep criterion 4 (Azure from-empty) unmet.
Critique: executed once, no conflicting findings.

## Cycle 1 correction plan

* [x] `chmod +x infra/scripts/deploy.py`; format touched files; rerun focused tests, ruff, mypy.
