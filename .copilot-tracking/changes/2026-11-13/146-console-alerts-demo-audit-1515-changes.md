<!-- markdownlint-disable-file -->
# Changes: 146-console-alerts-demo-audit-1515

Status: complete. Documentation only; no Bicep, test or source change.

* `infra/monitoring-runbooks.md`: added Demo Routing Decision section (decision, AC1..AC5 proof, production deferrals); `ms.date` 2026-11-13.
* `docs/reference/README.md`: one sentence in the #146 index paragraph.
* `docs/reference/log.md`: appended 2026-11-13 entry; `ms.date` bumped.

Validation: `infra/tests/test_bicep_policy.py` 61 tests OK (venv `/tmp/venv-146-1515`, `src/core` and `src/orchestrator` pip-installed); `az bicep build` of 10 root and 20 module files, 0 errors; `git diff --check` clean.

Divergences from brief: `infra/modules/observability.bicep` and `ledger_verifier.py` do not exist; equivalents are `monitoring.bicep`/`operationalMonitoring.bicep`/`main.bicep` and `digest_blob.py`.
