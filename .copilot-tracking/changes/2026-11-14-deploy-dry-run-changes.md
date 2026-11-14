# Changes: deploy.py --dry-run

* `infra/scripts/deploy.py`: `--dry-run`, `deployment_command`, `dry_run_plan`.
* `infra/tests/test_deploy.py`: two dry-run tests.
* `infra/README.md`: dry-run usage note.
* Validation: test_deploy.py 21 OK; full `python3 -m unittest discover -s infra/tests -v` 598 run, 1 error, 4 skipped. The error is pre-existing: `test_ledger_alert_queries_match_the_verifier_markers` fails with missing `zava_forward.orchestrator` (package not installed in this environment). `ruff check` and `ruff format --check` (README flags) pass on the three files.
* Not pushed.
