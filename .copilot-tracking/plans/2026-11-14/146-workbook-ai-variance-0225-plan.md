# Plan: 146-workbook-ai-variance-0225

1. Add panels operation-errors-latency and ai-variance-by-period to infra/monitoring-workbook.json.
2. Extend infra/tests/test_monitoring_workbook.py (panels, columns, notification wording, no raw prompt/PII, Bicep placeholders).
3. Focused validation: ruff, unittest, az bicep build.
Critique: single in-line pass; no conflicts with confirmed decisions.
