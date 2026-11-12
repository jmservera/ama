# Issue 115 scheduler trace changes (2026-11-12, 1112)

Base `cd81888e4a81cf4c712d50b357ca900fd5c8c06b`. Refs #115 only.

* `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py`: `main()` delegates to `_publish_and_verify()`; `DocumentStoreError` output unchanged; any other `Exception` from store open, blob open, publish or verify prints `LEDGER_DIGEST_ALERT ledger verification could not run: <TypeName>` and returns 1. Exit 2 for absent URL, `--reconcile` path, `SystemExit` unchanged.
* `src/orchestrator/tests/test_digest_blob.py`: three failing-first cases (store read failure on publish and verify paths, upload failure, store/blob initialisation failure) with a secret-sentinel leak check. All three errored before the fix.
* `infra/tests/test_bicep_policy.py`: `test_ledger_alert_queries_match_the_verifier_markers` binds the two ledger alert queries to `ALERT_MARKER` and `OK_MARKER` (guard; passed before and after).
* `src/orchestrator/README.md`: one sentence on the unexpected-failure alert.

## Validation (focused tier; venv `files/venv` with `--system-site-packages`, `pip install --no-deps -e src/core -e src/orchestrator`, origin verified to this worktree)

* `PYTHONPATH=../core/tests python -m unittest discover -s tests -q` in `src/orchestrator`: 112 baseline OK; 115 OK after.
* `ruff check`, `ruff format --check`, `mypy src tests` in `src/orchestrator`: pass (ruff 0.17.3 installed vs 0.17.1 pinned).
* `infra`: `unittest tests.test_bicep_policy -q`: 61 OK. `ruff check infra/tests/test_bicep_policy.py` reports one RUF100 at line 168, pre-existing on base, not touched.

## Not done / not claimed

No hosted alert, scheduler run, retention duration, lock, second-person reconciliation or #115 acceptance. Residual: `SystemExit` from SQL configuration bypasses the marker; the traceback is no longer printed for unexpected errors.
