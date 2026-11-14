# Changes

* infra/main.bicep: ledger-digest-mismatch and ledger-verify-missing descriptions name Digital service owner and runbook anchors.
* infra/modules/operationalMonitoring.bicep: AI limit description links ai-limit-calls/tokens/budget/expiry.
* infra/tests/test_monitoring_alert_coverage.py: new.

Validation: infra unittest discover 574 tests OK (4 skipped) with PYTHONPATH=src/core/src:src/orchestrator/src (orchestrator path needed by an existing test). Ruff passes on the new file; repo-wide ruff check/format of infra/tests fails on pre-existing files (72 errors before this change).

Base: rebased onto origin/main 7f607d1c8 after parent PR #1609 (65757bc90) squash-merged.
Rebased checks: unittest OK, az bicep build main.bicep and operationalMonitoring.bicep pass; repo-wide ruff on infra/tests still has the same 72 pre-existing errors, new file clean.
