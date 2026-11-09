---
title: Details for #185 truthful action report (corrective)
ms.date: 2026-11-06
---

* Files: `src/core/src/zava_forward/core/synthetic/device_provision.py`, `src/core/tests/test_device_provision.py` (reuses `FakeRegistry`, `FakeStore`, `sensors`).
* Tests added: `test_applied_provision_report_says_credentials_stored`, `test_applied_teardown_with_original_manifest_reports_revoked`, strengthened dry-run assertions.
* Checks: `unittest -p "test_device_*.py"`, `ruff check --no-cache`, `ruff format --no-cache --check`, `mypy --cache-dir=/tmp/mypy-185-fix`, exits captured to files, not piped.
