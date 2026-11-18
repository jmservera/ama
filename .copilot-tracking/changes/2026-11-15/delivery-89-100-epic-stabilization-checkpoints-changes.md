<!-- markdownlint-disable-file -->
# RPI Changes: Scoped Stabilization Checkpoints for Epic #89 and Epic #100

## Metadata

* Task ID: delivery-89-100-epic-stabilization-checkpoints-2026-11-15
* Related plan: .copilot-tracking/plans/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (P01, P02, P03, P04)
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P03, P03-T01, P04, P04-T01
* All remaining active-plan markers: None
* Status basis: All four phases (`P01`..`P04`) and all six tasks (`P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`, `P03-T01`, `P04-T01`) completed with passing focused local regression suites (`1,499` test executions across 6 Python test runs, `0` failures) and post-edit documentation/hygiene guards (`0` link, style, anchor, or `docs/`/`src/` legacy-reference violations, with zero subsequent edits to `docs/`).

## Execution Summary

Executed the `#440` scoped stabilization checkpoints for **Epic #89** (`#90`, `#91`, `#92`, `#132`, `#133`, `#1384`, `#1402`) and **Epic #100** (`#101`, `#102`, `#103`, plus management AI consumption economics on stacked `PR #1641`) on branch `feat/epic-89-100-stabilization-checkpoints` at parent-topic base `74273202817f9068f9c55cb325b39df7879cba7b` (`origin/main` `5e0c7f74432ffce73cfeaa672e4e40a605ca6274`, merge-base `61e1917dd075a8307f0fd436c42cc41f47906846`). Ran all planned focused `src/core`, `src/api`, companion `PR #1641`, and cross-cutting boundary suites locally without invoking `tools/rpi-checks.py`, updated `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, and `docs/reference/log.md`, and verified all post-edit guards cleanly with zero subsequent `docs/` edits.

## Completed Work

### Focused Local-First Regression and Integration Execution for Epic #89 and Epic #100

* Related phase or task: P01 (P01-T01, P01-T02)
* Files: Read-only execution across `src/core/tests/`, `src/api/tests/`, and `tools/`
* What changed and why: Inspected `git show --name-only` on stacked `PR #1641` commits (`23b675164` `#1745`, `d8cb35d25` `#1770`, `4dc285ad2` `#1657`, `77c7bfb18` `#1674`, `2fe7ff2e6` `#1792`) per `PC-003` and executed all focused Epic `#89` core/API/screen/script-retry suites, Epic `#100` core/API/tokenomics/manifest/export suites, cross-cutting dependency/auth/consent/manual-fallback suites, and baseline link/disposition/migration guards without invoking `tools/rpi-checks.py`.
* Completion evidence: 6 Python test runs executed (`322` + `257` + `247` + `213` + `53` + `382` + `25` = `1,499` tests ran, `0` failures; opt-in loopback SQL Server `ZF_*_MSSQL=1` and live Chromium skips recorded explicitly).
* Validation: Passed (`exit 0` across all `unittest` and `rename-zava-tests.py` runs; pre-existing `#201` `GUARD_FILES` gap in `tools/check-legacy-references.py` identified and isolated to `tools/test_epic_*.py` with `0` link or `docs/`/`src/` violations).

### Appended 2026-11-15 Scoped #440 Stabilization Checkpoints for Epic #89 and Epic #100

* Related phase or task: P02 (P02-T01, P02-T02)
* Files: `docs/architecture/cutover-evidence-pack.md`
* What changed and why: Updated frontmatter `ms.date` to `2026-11-15` and appended `## Epic #89 scoped stabilization checkpoint (2026-11-15, Refs #89 #440)` and `## Epic #100 scoped stabilization checkpoint (2026-11-15, Refs #100 #440)` at EOF while preserving all existing sections (including the partial `2026-11-03` Epic `#89` checkpoint) unchanged. Recorded verified Git SHAs and prompt nominal SHA disclosures, normative document blob SHAs and honest draft/in-review/proposed/exercise-only statuses, `BRD` vs `PRD` `FR-*` numbering divergences, requirement-to-code/test/journey traceability, six cross-cutting boundary checks per epic, observed local regression matrices and verification classes, zero-defect/no-refactoring dispositions, authorized Azure/human/tariff (`#432` open/deferred) residuals, and `continue` recommendations.
* Completion evidence: `git diff docs/architecture/cutover-evidence-pack.md` shows strictly `ms.date: 2026-11-15` plus the two appended EOF sections using verified `src/core` and `src/api` module paths (`server.py`, `workbench.py`, `progress.py`, `sensor_badges.py`, etc.).
* Validation: Passed (`test_live_doc_links.py`, `tools/test_epic_child_disposition_audit.py`, and full-file link/reference/style checks).

### Updated Knowledge Base Index and Append-Only Change Log

* Related phase or task: P03 (P03-T01)
* Files: `docs/reference/README.md`, `docs/reference/log.md`
* What changed and why: Updated `docs/reference/README.md` (`ms.date: 2026-11-15` and appended the summary paragraph with verified fragment links to both `2026-11-15` checkpoint headings in `cutover-evidence-pack.md`) and appended a single `[2026-11-15]` update entry at EOF of `docs/reference/log.md`.
* Completion evidence: `git diff docs/reference/log.md` has zero removed or modified prior lines; both fragment anchors resolve against `docs/architecture/cutover-evidence-pack.md`.
* Validation: Passed (`test_live_doc_links.py` and diff hygiene check).

### Post-Edit Documentation, Disposition, and Hygiene Guard Verification

* Related phase or task: P04 (P04-T01)
* Files: `.copilot-tracking/changes/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-changes.md`, `.copilot-tracking/plans/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-plan.md`, `.copilot-tracking/details/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-phase-details.md`
* What changed and why: Re-ran `src/core/tests/test_live_doc_links.py`, `tools/test_epic_child_disposition_audit.py`, `check-legacy-references.py` link/reference checks, and automated regex diff audits over finalized `docs/` with zero subsequent edits to `docs/` (`PC-002`), then reconciled all `[x]` plan markers, phase details, and follow-up items.
* Completion evidence: `Ran 10 tests in 4.872s, OK` (`exit 0`) and `diff_links: []`, `full_live_links: []`, `edited_ref_violations: []`, `removed_lines_in_log_md: []`, `style_and_anchor_issues: []` (`exit 0`).
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

### PYTHONPATH Test Ordering for Mixed Root Runs Importing test_mssqlstore

* Affected plan area or markers: `Dependencies`, `P04-T01`
* What changed: Documented `src/api/tests` preceding `src/core/tests` on `PYTHONPATH` (`PYTHONPATH=src/api/src:src/api/tests:src/api:src/core/src:src/agents/src:src/core/tests:src/agents/tests`) when a mixed root `unittest` command imports `src/api/tests/test_mssqlstore.py`.
* Why: Both `src/core/tests/test_buildings.py` and `src/api/tests/test_buildings.py` exist; placing `src/api/tests` first ensures `import test_buildings` inside `test_mssqlstore.py` resolves `BuildingHttpTests`.
* Triggering evidence: Initial mixed cross-cutting invocation (`AttributeError: module 'test_buildings' has no attribute 'BuildingHttpTests'`), resolved immediately on rerun (`Ran 382 tests in 57.167s, OK`).
* User answer or decision: None needed (local judgment / current-state reconciliation).
* Reconciliation performed: Updated `Dependencies` in `plan.md`, `P04-T01` in `phase-details.md`, and Epic `#89` operational observations in `cutover-evidence-pack.md`.
* Planning and critique state: Not needed; `Ready` plan intent preserved (`PC-001`..`PC-003` intact).

### Pre-Existing #201 Guard Allowlist Gap in tools/check-legacy-references.py Routed as Follow-Up

* Affected plan area or markers: `P04-T01`, `Follow-Up Items`
* What changed: Recorded that repo-wide `python3 tools/check-legacy-references.py` reports `links: 0 violation(s)` and `0` `docs/` or `src/` violations, while exiting `1` solely on `8` pre-existing matches in `tools/test_epic_legacy_path_retirement.py` and `tools/test_epic_parity_matrix_old_paths.py` (introduced in `0999ce7bf`, `PR #1610`, Refs `#201`), and added a follow-up item to register those two `#201` guard files in `GUARD_FILES`.
* Why: Modifying `tools/check-legacy-references.py` is outside this focused documentation-and-evidence scope (`docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md`); scoping `check_references` and `check_links` to edited `docs/` confirms zero violations introduced or present in changed files while routing the unrelated `#201` tool-guard fix cleanly.
* Triggering evidence: `git log -n 2 -- tools/test_epic_legacy_path_retirement.py tools/test_epic_parity_matrix_old_paths.py tools/check-legacy-references.py` (`0999ce7bf` PR `#1610`) and scoped `check-legacy-references.py` verification (`edited_ref_violations: []`, `diff_links: []`, `full_live_links: []`).
* User answer or decision: None needed (follow-up-only item outside immediate scope).
* Reconciliation performed: Updated `P04-T01` and `## Follow-Up Items` in `plan.md` and `phase-details.md`.
* Planning and critique state: Not needed; `Ready` state preserved.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Epic `#89` core focused suite (`test_quality_procurement`, `test_consultation_controls`, `test_job_pack`, `test_aftercare`, `test_aftercare_intake`, `test_aftercare_store`) | P01-T01 | Passed | `Ran 322 tests in 217.328s, OK (skipped=31)` (`ZF_RESIDENT_MSSQL=1` opt-in MSSQL skipped), `exit 0` |
| Epic `#89` API/screen/browser-check and `#1745`/`#1770` companions (`test_chat_case_answers`, `test_sensor_view_conflicts`, `test_procurement_api`, `test_procurement_screens`, `test_technical_quality_screens`, `test_staff_intake_api`, `test_staff_intake_browser`, `test_capacity_browser_check`, `test_aftercare_screen`, `test_aftercare_served`, `test_quality_sensor_grounding`, `test_quality_sensors_correlation`, `test_sensor_staleness_ui_badge`) | P01-T01 | Passed | `Ran 257 tests in 183.834s, OK (skipped=38)` (opt-in live Chromium and MSSQL skipped; `test_capacity_browser_check` ran 4/4 unskipped), `exit 0` |
| Epic `#100` core and `#1657`/`#1674`/`#1792` tokenomics suite (`test_coordinator`, `test_progress_reports`, `test_progress_event_capture`, `test_governance`, `test_list_export`, `test_ai_consumption`, `test_ai_consumption_skill_breakdown`, `test_ai_consumption_safety`, `test_tokenomics_comparison`, `test_management_tokenomics_invariant_100`) | P01-T02 | Passed | `Ran 247 tests in 41.491s, OK (skipped=34)` (`ZF_RAI126_MSSQL=1`, `ZF_CAPTURE_MSSQL=1` opt-in MSSQL skipped), `exit 0` |
| Epic `#100` API served integration suite (`test_coordinator_api`, `test_progress_dashboard`, `test_progress_report_api`, `test_programme_screen`, `test_governance_evidence_api`, `test_list_export_api`, `test_list_export_inventory`, `test_ai_consumption_api`, `test_management_tokenomics_api_100`) | P01-T02 | Passed | `Ran 213 tests in 218.658s, OK (skipped=21)` (`ZF_COORDINATOR_BROWSER=1`, `ZF_COORDINATOR_MSSQL=1`, `ZF_PROGRESS_MSSQL=1` skipped), `exit 0` |
| Remaining planned script-retry, manifest, needs-inventory, asset-board, and consent scenarios (`test_workspace_scripts`, `test_scenario_manifest`, `test_needs_inventory`, `test_asset_board_screen`, `test_safety_consent_exercise_scenarios_81`) | P01-T01, P01-T02 | Passed | `Ran 53 tests in 20.916s, OK (skipped=0)`, `exit 0` |
| Cross-cutting boundaries and baseline doc/disposition guards (`test_dependency_rule` core+api, `test_auth`, `test_entra_authoritative`, `test_role_matrix`, `test_ai_boundary`, `test_epic149_manual_fallback_continuity`, `test_mssqlstore`, `test_sqlstore`, `test_live_doc_links`, `tools/test_epic_child_disposition_audit`) | P01-T02 | Passed | `Ran 382 tests in 57.167s, OK (skipped=235)` (`ZF_TEST_MSSQL=1` disposable SQL Server skipped), `exit 0` |
| Migration regression guard (`python3 tools/rename-zava-tests.py`) | P01-T02 | Passed | `Ran 25 tests in 0.633s, OK`, `exit 0` |
| Post-edit `test_live_doc_links.py` and `tools/test_epic_child_disposition_audit.py` (`PC-002` zero-subsequent-edit verification) | P04-T01 | Passed | `Ran 10 tests in 4.872s, OK`, `exit 0` |
| Post-edit `check-legacy-references.py` scoped reference/link check and `docs/` Markdown/tracking hygiene diff scan | P04-T01 | Passed | `edited_ref_violations: []`, `diff_links: []`, `full_live_links: []`, `removed_lines_in_log_md: []`, `style_and_anchor_issues: []`, `exit 0` (repo-wide `check-legacy-references.py` has `0` link violations and `8` pre-existing `#201` `tools/test_epic_*.py` matches routed as follow-up) |
| `tools/rpi-checks.py` | Excluded by caller | Skipped | Explicitly prohibited by caller instructions to avoid shared worktree lock contention (focused validation tier) |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P04`, `P04-T01` all `[x]` and `Complete`).
* Completed-work evidence and handoff prose: Current across `changes.md`, `plan.md`, and `phase-details.md`.
* Validation, blockers, remaining work, and follow-up items: Current (`0` blockers, `0` remaining active tasks, `4` evidence-grounded follow-up items).
* Review readiness: Ready for `rpi-review`.

## Blockers

* None

## Remaining Work

* None within declared full-plan scope (`P01`..`P04` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-plan.md, `## Follow-Up Items`
* Add `tools/test_epic_legacy_path_retirement.py` and `tools/test_epic_parity_matrix_old_paths.py` to `GUARD_FILES` in `tools/check-legacy-references.py` (pre-existing `#201`/`#203` tooling hygiene from `PR #1610`).
* Rebase parent integration branch `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) onto latest `origin/main` (`5e0c7f74432ffce73cfeaa672e4e40a605ca6274`) (coordinator integration).
* Owner and commercial sign-off on provisional AI tariff, spend limits, and alert owners (`BRD::OD-51`, `PRD::OQ-027`, `#432`).
* Post-merge Epic `#89` and Epic `#100` criterion tick and issue closure (`#89`, `#100`, `#440`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`, `P02-T02`), `P03` (`P03-T01`), `P04` (`P04-T01`); remaining active-plan markers: `none`
* Validation coverage: `1,499` focused local Python tests executed (`0` failures; opt-in MSSQL and Chromium skips recorded explicitly), plus passing post-edit `test_live_doc_links.py`, `tools/test_epic_child_disposition_audit.py`, scoped `check-legacy-references.py`, and Markdown/hygiene diff audits with zero subsequent `docs/` edits
* Blockers: None
* Current plan and detail updates: Documented `src/api/tests`-first `PYTHONPATH` ordering for `test_mssqlstore.py` and routed pre-existing `#201` `GUARD_FILES` allowlist gap in `tools/check-legacy-references.py` as follow-up
* Planning and critique state: Ready (`PC-001`..`PC-003` resolved; no second critique needed)
* Follow-up items: 4 items mirrored from canonical plan list
* Review readiness or no-handoff reason: Ready for single-pass `rpi-review`
* Continuation owner: parent confirmed automatic RPI Agent
