# Research: 531 workbench UI verification (2026-11-13)

Base 74a93a137a983e0a87418e3321a6847ba9bcd278. Required docs (case study original/addendum, KB README, memory) consulted by scope; no source edits planned. Research disposition: executed. Planning Readiness: Ready.

## Test modules selected (offline unit tests, no browser/Docker/MSSQL)

Core (src/core/tests): test_buildings, test_coordinator, test_resident_journey_design, test_bulk_edits, test_progress_event_capture, test_progress_reports, test_atlas_screen_trace, test_journey_trace, test_taskqueues.

API (src/api/tests): test_design_system, test_workbench, test_workbench_live_defaults, test_buildings, test_bulk_edit_api, test_case_journey, test_nomination_screen, test_progress_dashboard, test_progress_report_api, test_loading_feedback, test_coordinator_api, test_queue_empty_state, test_task_queue_api, test_ui_support, test_chat_panel.

Note: no dedicated tenure/lease or Today's-briefing module name exists; coverage is by test_nomination_screen, test_progress_dashboard, test_loading_feedback and test_workbench (recorded as a coverage caveat).
