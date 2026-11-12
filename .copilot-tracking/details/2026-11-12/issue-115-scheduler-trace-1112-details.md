# Issue 115 scheduler trace details (2026-11-12, 1112)

## Phase 1 anchors

* `src/orchestrator/tests/test_digest_blob.py`: `BlobDigestTests.run_job` uses `main(..., store=, blob=, out=)`; add cases beside `test_empty_container_and_unreachable_container_alert`. Opening failure uses `env` with `ZF_STORE=mssql` and `store=None` patched `zava_forward.core.factory.open_store`.
* `infra/tests/test_bicep_policy.py:1141` `test_ledger_alerts_use_azure_monitor_resource_specific_console_schema` is the neighbour; the new test asserts the mismatch query `Log has` the value of `ALERT_MARKER` and the missing-success query the value of `OK_MARKER`.

## Phase 2 anchor

* `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py` `main()` lines 219-250.
* Message `ALERT_MARKER + " ledger verification could not run: <TypeName>"`; no message text, because SQL errors can carry connection details.

## Validation

* `PYTHONPATH=../core/tests <venv>/bin/python -m unittest tests.test_digest_blob -q` from `src/orchestrator`, then discovery.
* `ruff check`, `ruff format --check`, `mypy` as configured in `src/orchestrator/pyproject.toml` (digest_blob is exempt from several rules there; no new exemptions).
* Infra test needs `az bicep`; report blocked if unavailable.
