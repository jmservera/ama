# Changes: 146-ai-alert-runbook-0150

* infra/monitoring-runbooks.md: four AI limit class sections.
* infra/tests/test_ai_alert_runbook_ownership.py: new, 4 tests.
* No .bicep change (az bicep build not required).
* Validation: ruff check/format clean; new + test_monitoring_alerts pass (12); full infra suite 1 pre-existing error (test_bicep_policy ledger markers), identical on baseline; core test_ai_consumption 4 pre-existing failures, identical on baseline.
