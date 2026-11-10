<!-- markdownlint-disable-file -->
# Merged-wave 440 checkpoint changes and execution record (2026-11-10)

Opened at 2026-11-10T02:05Z before the first validation command. Append-only; results are added below as observed.

Pinned source: `da4f52abb5bfdc50acc9b9b8aa84cc42babc77fe` (tree `823c9cba2e21`), start `origin/main` `da4f52abb` (ls-remote 02:04:16Z). Critique amendments F1 to F6 apply.

Source changes by this task: none intended. Writes allowed: cutover-evidence-pack, reference README, reference log, own RPI records.

## Execution log

Environment: Python 3.12.3, node v24.21.0, owned venv under the scratch directory with editable installs of this worktree's `src/core[sql,blob]`, `src/agents`, `src/api`, `src/orchestrator` and `src/importer`, and the declared `playwright==1.64.0` pin (api `dev` extra) for the opt-in browser class; the pre-existing user-site installs point at another checkout and were not used. Import origins of every selected package and test module were printed under the exact `PYTHONPATH` of each run and are inside this worktree (API runs put `tests` first so the API `test_version` and `test_dependency_rule` are not shadowed by the Core files of the same name). Each run used `env -i` with only `PATH`, `HOME`, `TMPDIR`, `LANG`, `ZF_DATA` (owned scratch) and `PYTHONPATH` (plus `ZF_BROWSER_TESTS=1` for R6 only), so no SQL, Azure, model or provider switch or credential existed. `timeout -k 10 900` bounded each. Raw logs stay in the owned scratch directory outside the repository (not committed); `SHA256SUMS` of the 13 logs `bf60e679516048770d27feac96f02d3f7deb8424b7b72c15cdfe7acdb4ebe599`.

| Id | Dir and selection | Exit | RUN | PASS | SKIP | Window (UTC) | Log sha256 prefix |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | `src/core` `test_form_dependencies` 10, `test_form_review` 23, `test_form_review_pack` 8, `test_form_export` 9, `test_form_staging` 17 | 0 | 67 | 67 | 0 | 02:06:02 to 02:06:29 | `547392defcf7` |
| R2 | `src/api` `test_form_staging_api` (14 `def test` in the module at this source) | 0 | 14 | 14 | 0 | 02:06:29 to 02:06:41 | `40ca12899631` |
| R3 | `src/core` `test_resident_decisions` (JSON 110, SQLite-backed `SqlResidentDecisions` 129, `MssqlResidentControls` 129, fake Azure 1, complaints route 1, priority query 1) | 0 | 371 | 239 | 132 | 02:06:58 to 02:07:43 | `ea4a09dd4726` |
| R4 | orchestrator first invocation `python -m unittest -v discover -s tests` | 2 | 0 | 0 | 0 | 02:06:45 | `5baef54942fc` |
| R4b | `src/orchestrator` `discover -v -s tests` (corrected argument order, `PYTHONPATH=../core/tests`): `test_rebuild_azure` 39, `test_rebuild` 23, `test_digest_blob` 27, `test_document_rescan_job` 10, `test_source_monitor` 5, `test_token_store` 4, dependency rule 2, version 2 | 0 | 112 | 112 | 0 | 02:07:40 to 02:07:51 | `85c4ce96b014` |
| R5 | `src/api` `test_timecapture` 26 pass, `test_timecapture_copy` 7 pass and 5 browser skips (no opt-in) | 0 | 38 | 33 | 5 | 02:06:45 to 02:06:52 | `4334b8253128` |
| R6 | `src/api` `test_timecapture_copy.StaffTimeGuidanceBrowser` with `ZF_BROWSER_TESTS=1` (loopback Chromium, external requests aborted) | 0 | 5 | 5 | 0 | 02:06:52 to 02:06:58 | `3f6bdd9dabde` |
| R7 | `src/api` `test_case_journey` 31, `test_role_matrix` 13, `test_workbench` 5 | 0 | 49 | 49 | 0 | 02:07:43 to 02:07:53 | `675cba7071a9` |
| R8 | `src/core` `test_scenario_manifest` 8, `test_needs_inventory` 11, `test_version` 3, `test_dependency_rule` 2 | 0 | 24 | 24 | 0 | 02:06:41 to 02:06:43 | `558d731d9dbe` |
| R9a to R9d | `test_version` and `test_dependency_rule` in api (3, 2), agents (2, 4), orchestrator (2, 2), importer (2, 2); each in its own project directory | 0 each | 5, 6, 4, 4 | 5, 6, 4, 4 | 0 | 02:06:43 to 02:06:45 | `abbc09fc7280`, `2488dfd09b9c`, `dc4e2071d493`, `60a7c7ac7b53` |

Totals (final processes R1, R2, R3, R4b, R5, R6, R7, R8, R9a to R9d): RUN 699, PASS 562, SKIP 137, failures and errors 0. The 5 R5 browser skips are the same tests that ran in R6, so distinct tests are 694: 562 passed and 132 skipped (all in R3). R4 is an adverse invocation fault of this run (the `-v` option before `discover` is rejected by `python -m unittest`, usage error, 0 tests, exit 2); its log is kept and not counted, and R4b is the same selection with the order corrected. No product failure occurred.

R3 skips (132, read from `-v`): 129 "opt-in owned loopback SQL Server" (the `MssqlResidentControls` class), 1 "Explicit isolated synthetic Azure SQL database required", 1 "JSON file rollback only", 1 "SQL replay only" (the JSON-class run of `test_supersede_binding_changed_during_sql_replay_is_refused`; the SQLite-backed class executed it and passed). None is a SQL Server pass.

Named representative cases (all `ok` on JSON and on the SQLite-backed class, `skipped` on the SQL Server class): `test_forward_defaults_unconfigured_and_keeps_local_request`, `test_supersede_default_unconfigured_rejects_inferred_roles_and_forged_rows`, `test_supersede_binding_not_created_from_staff_requests_or_body`, `test_supersede_binding_is_validated_and_immutable`, `test_supersede_changed_binding_withdraws_earlier_authorization`, `test_supersede_restamped_binding_digest_on_an_old_approval_does_not_count`, `test_supersede_evidence_substituted_after_a_genuine_approval_does_not_count`, `test_supersede_forged_stored_authorization_is_withdrawn_not_counted`, `test_supersede_legacy_generic_audit_entry_is_not_proof`; plus `ComplaintsRouteConfiguration.test_only_unconfigured_is_known_and_it_sends_nothing` (ok).

Named finance cases (ok): `test_form_export` `test_export_carries_ordered_detached_review_history`, `test_history_is_integrity_covered_and_legacy_copy_is_invalid`, `test_edited_or_incomplete_saved_export_is_invalid_not_trusted`, `test_export_is_held_and_links_evidence_without_authority`; `test_form_review` `test_missing_bytes_block_stale_rejected_and_replaced_retained_history`; API CSV cases `test_schema_csv_*` (seven) and the seven staging and held-review cases (registry stage, rescanned SQL sources, auth scope, working field review, review denials, sibling availability, storage failure).

Named four-image cases (ok, `FakeAzure`, no network): `test_all_four_workloads_build_from_their_source_contexts`, `test_application_deploy_maps_every_tag_and_passes_the_orchestrator_explicitly`, `test_build_failure_stops_before_later_builds_and_deployment`, `test_resume_deploys_when_all_four_tags_exist`, `test_resume_never_treats_the_api_tag_as_four_image_readiness`, `test_unpublished_image_fails_verification_before_deployment`, `test_workload_images_cannot_be_overridden`, `test_dry_run_lists_the_four_images_without_io`, `test_default_is_dry_run_with_no_azure_calls`.

Named time-capture cases (ok): `test_off_by_default_and_nothing_is_written`, `test_dpia_alone_does_not_switch_it_on`, `test_notice_must_be_acknowledged_before_recording_or_listing`, `test_enabling_is_manager_only_and_audited_through_the_api`, `test_report_suppresses_small_groups_and_lists_no_person`; the five browser cases (disabled and missing-prerequisite owner and next action, invalid minutes, read failure distinct from blocked, ambiguous save claims nothing, server detail not rendered) passed in R6.

Noise, not a failure: R7 prints 24 handled tracebacks "Rule evaluation unavailable ... The law store is not loaded; rule checks are unknown." from fixtures without a law store; the same fail-closed log pattern was already recorded at the 2026-11-09 checkpoint (37 then). No defect is asserted.

Source identity after: `git rev-parse HEAD:src` `f8cf2443b124c0e8e089ea4f49ed6ef1eeebd6f3` before and after the series; `git status --short` showed only this task's six own tracking files; `git diff --stat` empty. No product, test, tool, infra or policy file changed.

Main at end of the runs: `git ls-remote origin refs/heads/main` at 02:10:18Z resolved `6f24e554aa22da67756006c5185a329c14101ec3` (rubric bot commit 02:06:46Z, only `.github/rubric/scores/latest.json`); `src`, `tools`, `infra`, `.github/workflows`, the evidence pack and the reference index blobs and trees are identical to the pin. Observations apply to `da4f52abb`, not to a later main; the bot commit is not merged here.

Not run: SQL Server legs (SQL tests skipped, none attempted), Azure SQL, IoT Hub, real image builds or push, any model or provider call, hosted CI, assistive technology, human approvals.
