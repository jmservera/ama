# Changes: 79 lifecycle verify (Refs #79 #76 #82 #83 #86)

Tracking-only verification at 3b05143179f83235c5b4e80e70aad99bdc44d83f; no src/ or docs/ edits. Venv /tmp/venv-79-1143 (system-site-packages, pip upgrade setuptools wheel, editable core/agents/api --no-deps --no-build-isolation); zava_forward.{core,agents,api}.__path__[0] verified inside this worktree src/. Run with all ZF_* variables unset, PYTHONDONTWRITEBYTECODE=1, `python -m unittest -v <module>` from src/core (PYTHONPATH=tests) or src/api (PYTHONPATH=tests:../core/tests:../agents/tests). No Docker, MSSQL, Chromium or cloud calls (API tests used local loopback only). Every producer exit code was 0.

Totals: core 661 tests (149 skipped), api 175 tests (14 skipped); 0 failures. Skips are NOT passes: 146 opt-in owned loopback SQL Server, 13 opt-in local Chromium, 1 opt-in local browser, 1 SQL replay only, 1 JSON file rollback only, 1 explicit isolated Azure SQL requirement.

| Module | Ran | Skipped | Exit | Log sha256 (first 16) |
| --- | --- | --- | --- | --- |
| core.test_exception_queue | 14 | 0 | 0 | c0b31e4e89e31df0 |
| core.test_gates | 22 | 0 | 0 | 9c2900c026fbd1a7 |
| core.test_handoff_lifecycle | 20 | 0 | 0 | 4c18cec33a36a47b |
| core.test_home_case | 8 | 0 | 0 | 834437fe56868832 |
| core.test_queue_benchmark | 1 | 0 | 0 | b83b814b6859f671 |
| core.test_ranking_archive_blob | 26 | 0 | 0 | 94b6698d183f7611 |
| core.test_ranking_publication | 57 | 0 | 0 | 1d9449a74a74268a |
| core.test_ranking_publication_runner | 53 | 0 | 0 | 836f074b8d83ca8a |
| core.test_resident_choice_queue | 4 | 0 | 0 | dc1db40892fe0d30 |
| core.test_resident_decisions | 419 | 149 | 0 | 53333ff5d4f3ce1c |
| core.test_sqlqueues | 15 | 0 | 0 | 47bd76789bcee898 |
| core.test_taskqueues | 22 | 0 | 0 | bd27a7995c1f2685 |
| api.test_handoff_api | 7 | 0 | 0 | 1c0fff07d4f543c7 |
| api.test_handoff_read_guidance | 15 | 7 | 0 | ea04f401aa1d5741 |
| api.test_handoff_waiting_view | 10 | 4 | 0 | d8d201cafbe2c793 |
| api.test_home_case_api | 6 | 0 | 0 | ccb90a7b0350afcb |
| api.test_queue_empty_state | 7 | 0 | 0 | b88a63e423521be7 |
| api.test_ranking_policy | 13 | 0 | 0 | f71a5c6e596ae7ec |
| api.test_ranking_publication_wiring | 36 | 0 | 0 | 55baca502d6cb93e |
| api.test_ranking_scale | 18 | 0 | 0 | 66d41ad19a0744f2 |
| api.test_resident_api | 21 | 1 | 0 | c4e40cf1fe4dea47 |
| api.test_task_queue_api | 4 | 0 | 0 | 84bddb77f17df2d0 |
| api.test_unaccepted_handoff_csv_api | 13 | 0 | 0 | a89ccf6b5a79d237 |
| api.test_unaccepted_handoff_download_ui | 6 | 2 | 0 | ec4d77eb53b89971 |
| api.test_workflows | 19 | 0 | 0 | bac65a283f6fb577 |

Cleanup: /tmp/venv-79-1143 and scratch logs removed after recording. Plan superseded in part by the critique amendments (details file: added test_resident_api, test_workflows, all ZF_* unset). Per-module skips are listed in the table; skip reasons are global (see above).
