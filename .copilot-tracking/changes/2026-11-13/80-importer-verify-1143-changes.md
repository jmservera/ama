---
title: Issue 80 importer verification changes
ms.date: 2026-11-13
---

Verification at 3b05143179f83235c5b4e80e70aad99bdc44d83f. No src/ or docs/ edits. Fictional fixtures only; no Docker, browser, cloud or private data.

Environment: `python3 -m venv --system-site-packages /tmp/venv-imp-1143`; pip upgrade setuptools and wheel exit 0; editable `--no-deps --no-build-isolation` install of core, agents, importer, api exit 0 (a first attempt failed on a vanished venv file, a /tmp race; the venv was recreated and the second attempt succeeded). Package paths verified inside this worktree `src/<pkg>/src/zava_forward/<pkg>`. Venv removed.

| Run | Exit | Tests | Skips | Log sha256 |
| --- | --- | --- | --- | --- |
| `src/importer`: unittest discover -s tests -v | 0 | 85 OK | 0 | cf4e9252aca818b3c40e9bb792808d61143bd4f71923d006efe6a7efe188f6fb |
| `src/api` (PYTHONPATH=../core/tests:../agents/tests): tests.test_list_export_api tests.test_exception_register_screen -v | 0 | 33 OK | 0 | 674cd8d050d4921e198ea184ac20a04579d32538150c3ba4afd256652a420804 |

Importer per module: test_dependency_rule 2, test_document_form_fixtures 8, test_excel_transition 30, test_import_exceptions 43, test_version 2.
API per module: test_list_export_api 11, test_exception_register_screen 22 (includes its CSV tests).

Logs copied to the external evidence directory. Exit codes were captured from each producer directly. No stray untracked source artefacts. Importer SQL Server C4 tests were not part of this run and the suite reported no skips.
