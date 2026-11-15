# Plan: diagnostic log privacy (Refs #146)

1. Redact StdoutSink dry-run output to device id, message id, label and byte size.
2. Add infra/tests/test_diagnostic_log_privacy.py (Bicep categories and sinks).
3. Add src/api/tests/test_diagnostic_log_privacy.py (runtime records, IoT rejection, dry run, simulator failure).
4. Run focused-tier validation. Avoid pyproject.toml, log.md, workbook and runbooks (open PRs 1600, 1603, 1604, 1608).
Critique: executed once; compatible findings applied (keep SYNTHETIC label for existing test).
