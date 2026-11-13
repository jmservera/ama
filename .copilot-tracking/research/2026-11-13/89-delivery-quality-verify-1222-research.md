# Research: Epic #89 unit verification (89-delivery-quality-verify-1222)

* Base: 74a93a137a983e0a87418e3321a6847ba9bcd278; Refs #89, #92, #132, #133
* Research disposition: executed. Planning Readiness: Ready.
* Sources read: docs/case_study_48_original.md, case_study_48_addendum.md, reference/README.md, reference/memory.md (index and context only; no source edits planned).

## Candidate modules (git ls-files, grep for capacity/appointment/work order/remedy/consultation/aftercare/intake/handover)

Core (src/core/tests): test_aftercare, test_aftercare_intake, test_aftercare_store, test_consultation_controls, test_job_pack, test_quality_procurement, test_resident_decisions, test_progress_event_capture.

API (src/api/tests): test_aftercare_screen, test_aftercare_served, test_staff_intake_api, test_procurement_api, test_procurement_screens, test_resident_api, test_resident_callbacks_page, test_technical_quality_screens, test_resident_preview_api.

Excluded: sensor modules (already run in #1288), test_capacity_browser_check and test_staff_intake_browser (Chromium), MSSQL-gated tests (skipped without ZF_TEST_MSSQL, reported as skips).

## Method

Scratch venv /tmp/venv-89-1222 (system site packages), editable no-deps installs of src/core, src/agents, src/api; verify package paths inside the worktree; run with env -u ZF_DATA -u ZF_TEST_MSSQL; offline; no Docker/browser/cloud. Write-only to .copilot-tracking.
