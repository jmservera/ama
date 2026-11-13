# Changes: 531 workbench UI verification

Tracking-only; no src/ or docs/ edits. Base 74a93a137a. Venv /tmp/venv-531-1222 (system-site-packages, editable --no-deps --no-build-isolation core/agents/api; __path__ verified inside worktree src/{core,agents,api}/src/zava_forward/*). Env: `env -i` allowlist, synthetic ZF_DATA=/tmp/h531/data.json, no MSSQL/browser opt-ins. Node (local, no browser) added to PATH for UI static-asset tests. API loopback HTTP is local only. Run as `python -m unittest tests.<module>` from src/<pkg>; API uses PYTHONPATH=tests:../core/tests:../agents/tests (first pass lacked tests/ and node on PATH: 7 modules errored, then rerun).

| Pkg | Module | Exit | Ran | Skips | Log sha256 |
| --- | --- | --- | --- | --- | --- |
| api | test_buildings | 0 | 3 | 0 | 974c815a2323e322 |
| api | test_bulk_edit_api | 0 | 6 | 0 | c7a96fe6a5384683 |
| api | test_case_journey | 0 | 31 | 0 | a9d0ea008995bc59 |
| api | test_chat_panel | 0 | 55 | skipped=1 | 30ec19203a12c7ce |
| api | test_coordinator_api | 0 | 21 | skipped=9 | e28011fe280a04a5 |
| api | test_design_system | 0 | 8 | 0 | 7c5860e4840dca48 |
| api | test_loading_feedback | 0 | 4 | 0 | a9d218f3ab6fe6c3 |
| api | test_nomination_screen | 0 | 5 | 0 | 50da7b235a229fb6 |
| api | test_progress_dashboard | 0 | 57 | 0 | 5106f17cbcee422e |
| api | test_progress_report_api | 0 | 33 | skipped=12 | cc3f154dd7dc3751 |
| api | test_queue_empty_state | 0 | 7 | 0 | 014d5abb48e8a7c8 |
| api | test_task_queue_api | 0 | 4 | 0 | b62b5006ce72d205 |
| api | test_ui_support | 0 | 12 | 0 | 72a4962f8be8be84 |
| api | test_workbench | 0 | 5 | 0 | e7b106218234ce20 |
| api | test_workbench_live_defaults | 1 | 1 | 0 | 72912b11f22ed4e4 |
| core | test_atlas_screen_trace | 0 | 17 | 0 | 53ff4527f7b78617 |
| core | test_buildings | 0 | 9 | 0 | 9fd73409370824dd |
| core | test_bulk_edits | 0 | 39 | 0 | 4c2cd395e47fb69d |
| core | test_coordinator | 0 | 28 | 0 | 4f8a87e8a225573e |
| core | test_journey_trace | 0 | 10 | 0 | 02c0f5862744fba2 |
| core | test_progress_event_capture | 0 | 51 | skipped=18 | 5e7c84fc530cc6ca |
| core | test_progress_reports | 0 | 21 | 0 | a045aa9a7229e838 |
| core | test_resident_journey_design | 0 | 9 | 0 | ae3b45a521c364e6 |
| core | test_taskqueues | 0 | 22 | 0 | 737ca7e5ae8ab04d |

Result: 23 of 24 modules exit 0 (final run). test_workbench_live_defaults exit 1: ImportError, no module named playwright; it is a Chromium/Playwright browser check excluded by the brief (not run, recorded as unavailable). Skips are the modules' own explicit MSSQL/opt-in skips. No dedicated Today's-briefing or tenure/lease module exists; covered indirectly by test_loading_feedback, test_nomination_screen, test_progress_dashboard, test_workbench. Failures in first pass were harness-environment only (node, PYTHONPATH), not code defects.
