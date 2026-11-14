# Changes: deploy.py --dry-run

* `infra/scripts/deploy.py`: `--dry-run`, `deployment_command`, `dry_run_plan`.
* `infra/tests/test_deploy.py`: two dry-run tests.
* `infra/README.md`: dry-run usage note.
* Validation: test_deploy.py 21 OK; full `python3 -m unittest discover -s infra/tests -v` 598 run, 1 error, 4 skipped. The error is pre-existing: `test_ledger_alert_queries_match_the_verifier_markers` fails with missing `zava_forward.orchestrator` (package not installed in this environment). `ruff check` and `ruff format --check` (README flags) pass on the three files.
* Not pushed.

## Cycle 1 correction (Refs #148)

* Research: `ruff check` raised `EXE001` (shebang without executable bit) on `infra/scripts/deploy.py`; sibling `create-sql-users.py` is mode 100755.
* Fix: set mode 100755 on `infra/scripts/deploy.py`; applied `ruff format` to `deploy.py` and `infra/tests/test_deploy.py`.
* Validation: `ruff check` and `ruff format --check` pass on both files; `python3 -m unittest discover -s infra/tests -p 'test_deploy*.py'` 21 OK; `mypy infra/scripts/deploy.py` clean.
* Scope note: directory-wide `ruff check infra/scripts infra/tests` still reports 110 pre-existing findings in unrelated files (not touched here).
* Review: single-pass self-review of the diff found no further issues. Not pushed.
