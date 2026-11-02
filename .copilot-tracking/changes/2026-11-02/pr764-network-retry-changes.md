---
title: PR 764 third CI failure changes
date: 2026-11-02
---

* `src/api/src/zava_forward/api/web/app.js`: `fetchReadRetrying` no longer retries network failures.
* `src/api/tests/test_workspace_scripts.py`: network-error, JSON-charset and gateway retry cases.

Local src-api results (venv /tmp/ci764b-venv, pip, PYTHONDONTWRITEBYTECODE=1): unit 1635 OK (323 skipped); ruff check and format PASS; mypy PASS; isolated harness lint PASS; employee_acceptance_check PASS; design_system_browser_check PASS; axe download OK; regulatory_ux_check PASS; case_journey_browser_check PASS; chat panel browser test PASS (failed before the fix). Docker, trivy and SBOM steps not run locally.
