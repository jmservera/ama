---
title: Issue 80 importer verification research
ms.date: 2026-11-13
---

Task: run full src/importer suite and the issue 80 API CSV export unit module at 3b05143179 (Refs #80, #176, #135).

Disposition: executed. Planning Readiness: Ready.

Findings (local inspection):
* src/importer/tests: test_dependency_rule, test_document_form_fixtures, test_excel_transition, test_import_exceptions, test_version.
* src/api/tests/test_list_export_api.py is the issue 80 CSV export module ("every staff list offers a CSV copy"). Exception register CSV is in the same family (test_exception_register*.py do not mention CSV).
* README states synthetic data only, stdlib only; no Docker/SQL Server needed for the importer suite except noted C4 tests (SQL tests expected to skip without a container).
* Docs read at start: case study docs, docs/reference/README.md and memory.md (context only).
