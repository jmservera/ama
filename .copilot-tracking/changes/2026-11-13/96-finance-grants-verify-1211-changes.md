# Changes: 96-finance-grants-verify-1211

Tracking-only. No src/ or docs/ edits. HEAD `3b05143179f83235c5b4e80e70aad99bdc44d83f`. Python 3.12.3. Refs #96, #98, #99, #93.

## Method

* Venv `/tmp/venv-96-1211` (system-site-packages), setuptools and wheel upgraded from the package index (offline index lacked wheel; the brief requires the upgrade), editable installs of src/core, agents, importer, api with `--no-deps --no-build-isolation --no-index`.
* `zava_forward.__path__[0]` = `/home/azureuser/source/ama-demo-wt/child-96-finance-1211/src/agents/src/zava_forward`, inside the worktree `src/` (namespace package).
* Run with ZF_DATA, ZF_TEST_MSSQL, ZF_FINANCE_MSSQL, ZF_GRANT_MSSQL, ZF_GRANT_BROWSER unset, PYTHONDONTWRITEBYTECODE=1. No Docker, MSSQL, Chromium or LLM calls. Core: `src/core`, `PYTHONPATH=tests`. API: `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests`.
* Disclosure: the first venv was deleted by an external process after 19 modules ran (shared host); the venv was rebuilt identically and the last two API modules were run in it. Exit codes 127 from that interval were environmental and are superseded by the reruns below. Venv removed at end.

## Results (producer exit code `$?`, all 0)

| Suite | Module | Ran | Outcome | Log sha256 (first 12) |
| --- | --- | --- | --- | --- |
| Core | test_finance_match_controls | 49 | OK skipped=19 (isolated local SQL Server) | 05a1c28faca7 |
| Core | test_finance_signoffs | 29 | OK | 5ddc189899ab |
| Core | test_funding_automation_boundary | 8 | OK | db953fa3089d |
| Core | test_grant_lifecycle_controls | 44 | OK skipped=16 (local SQL Server) | cc2614c2136a |
| Core | test_chat_case_funding_sources | 4 | OK | 0669583b7f83 |
| Core | test_form_staging | 17 | OK | 82379197a3b3 |
| Core | test_form_review | 23 | OK | ff786daa8973 |
| Core | test_form_review_pack | 8 | OK | b76cf1b2cade |
| Core | test_form_dependencies | 10 | OK | 9dc74b69693d |
| Core | test_form_export | 11 | OK | f14f070e26e2 |
| Core | test_exposure_limits | 16 | OK | f5faefd83b5e |
| Core | test_gates (extra) | 22 | OK | 61e549015a9f |
| Core | test_taskqueues (extra) | 22 | OK | 395708fb2aec |
| API | test_finance_match_api | 1 | OK | 428f32f8152d |
| API | test_grant_lifecycle_api | 2 | OK skipped=1 (local Playwright) | 225e1e027366 |
| API | test_finance_grants_screens | 20 | OK | 9ec1c440805f |
| API | test_finance_exposure_api | 4 | OK | 738f06c21172 |
| API | test_finance_exposure_screen | 3 | OK | 733871f4886b |
| API | test_form_staging_api | 14 | OK | 48fbd5fd7d9d |
| API | test_form_held_download_api | 16 | OK | 830eae9efe89 |
| API | test_programme_screen (extra) | 16 | OK | d542c82fc7be |

Totals: Core 263 tests, API 76 tests, 339 overall, 0 failures, 0 errors, 36 explicit opt-in skips (35 SQL Server, 1 Playwright). Aggregate sha256 of the per-module sha256 listing: `20e3cf2b591697f9f759cdf7bd7793b08a85be4918906c10e4cb533348cf7d44`. Full logs were kept outside the repository.

## Literal acceptance-criteria boundaries (unchanged, none ticked or proven here)

* #96 unchecked: approved versioned schema per assisted form; reviewed export never submits or implies eligibility; source, schema or rule change marks only dependents stale.
* #98 unchecked: validation uses approved rules and reviewer-confirmed inputs only; pack links fields, evidence and attachments with template and input versions.
* #99 unchecked: envelope and tolerances recorded as human-approved inputs, not invented; breach produces a pause signal for a human decision.

Passing synthetic unit tests is engineering evidence only. It grants no human, Finance (FD01-FD14), OD12/OD15, legal, privacy, submission or eligibility approval, and SQL Server and browser coverage was not exercised. No issue was edited or closed.
