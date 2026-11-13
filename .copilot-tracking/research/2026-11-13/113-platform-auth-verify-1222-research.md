# Research: Epic #113 platform/auth offline unit verification

Task: `113-platform-auth-verify-1222`. Base `74a93a137a983e0a87418e3321a6847ba9bcd278`. Disposition: executed. Planning Readiness: Ready.

Read at start: case_study_48_original.md, case_study_48_addendum.md, docs/reference/README.md (index), docs/reference/memory.md.

## Scope (tracking-only; no src/ or docs/ edits)

Core modules (src/core/tests): test_sqlstore, test_documents, test_document_rescan, test_resident_documents, test_data_protection, test_chat_privacy, test_chat_dpia_record, test_regulatory_privacy, test_sensor_privacy, test_list_export, test_form_export, test_version.

API modules (src/api/tests): test_auth, test_entra_authoritative, test_role_matrix, test_role_endpoint_inventory, test_role_screens, test_role_screens_conformance, test_chat_fixture_roles, test_expected_denials, test_document_controls, test_timecapture, test_timecapture_copy, test_ledger, test_resident_ledger_meter, test_continuity, test_continuity_epoch_export, test_map_fullscreen, test_list_export_api, test_resident_choice_export, test_lawstore, test_mssqlstore, test_version.

Issue mapping: #114 sqlstore/ledger/mssqlstore; #116 auth, entra, roles; #117 document_controls, documents; #119 map_fullscreen; #120 timecapture, chat_dpia_record; #121 data_protection, privacy, exports; #122 continuity, version; #350 anonymous 401 via auth/expected_denials.

Browser checks (Chromium) excluded. MSSQL tests are expected to skip without ZF_TEST_MSSQL.

## Method constraints

Venv /tmp/venv-113-1222 with system site packages, editable --no-deps installs of core, agents, api; verify import paths in worktree; run with `env -u ZF_DATA -u ZF_TEST_MSSQL`; no network, Docker or browsers.
