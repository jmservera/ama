# Research: 79 lifecycle verify (Refs #79 #76 #82 #83 #86)

Disposition: executed. Base 3b05143179f83235c5b4e80e70aad99bdc44d83f.

Planning Readiness: Ready.

Core modules (src/core/tests): test_gates, test_handoff_lifecycle, test_home_case, test_ranking_archive_blob, test_ranking_publication, test_ranking_publication_runner, test_resident_choice_queue, test_resident_decisions, test_taskqueues, test_sqlqueues (MSSQL-gated, expect skips), test_exception_queue, test_queue_benchmark.
API modules (src/api/tests): test_ranking_policy, test_ranking_publication_wiring, test_ranking_scale, test_home_case_api, test_task_queue_api, test_queue_empty_state, test_handoff_api, test_handoff_read_guidance, test_handoff_waiting_view, test_unaccepted_handoff_csv_api, test_unaccepted_handoff_download_ui (browser-gated, expect skips).
Fixtures need PYTHONPATH=../core/tests:../agents/tests for API (repo guidance).
