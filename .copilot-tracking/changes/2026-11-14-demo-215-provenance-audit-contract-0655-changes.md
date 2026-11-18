---
title: "Changes: #215 provenance and audit contract test"
ms.date: 2026-11-14
---

* Removed three `unused-ignore` comments in `test_alert_chat_{visit_consent_boundary,unblock_visit_grounding,end_to_end_stabilization}_215.py`.
* Divergence: the focused unittest command could not import `test_role_matrix`; added a one-line `sys.path.append` plus `# noqa: E402` in the three files and the new one (and `import sys`, `Path` where missing).
* Added `src/api/tests/test_alert_chat_provenance_audit_contract_215.py` (6 tests).
* Validation: unittest 96 tests OK; ruff check and format clean; mypy `Success: no issues found in 267 source files`.
