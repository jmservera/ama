<!-- markdownlint-disable-file -->
# RPI Changes: Usability Testing Programme with Representative Users (Issue #155)

## Metadata

* Task ID: issue-155-usability-programme-1507
* Related plan: .copilot-tracking/plans/2026-11-15/ux-155-usability-programme-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ux-155-usability-programme-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`, `P03-T03`
* All remaining active-plan markers: None
* Status basis: Full declared plan (`P01`, `P02`, `P03`) executed, validated under the focused tier (`unittest`, `ruff check`, `ruff format --check`, `mypy`, Markdown link verification), and reconciled for `rpi-review`.

## Execution Summary

Delivered the complete Issue #155 usability testing programme specification and deterministic core contract/evaluator across `P01`, `P02`, and `P03`. Created `src/core/src/zava_forward/core/usability_programme.py` and `src/core/tests/test_usability_programme.py` (15 focused test methods, 0 skips), documented the module in `src/core/README.md`, upgraded `docs/reference/research/ux/usability-test-programme-plan.md` in place (`ms.date: 2026-11-15`), updated `docs/reference/research/ux/design-system.md`, `docs/reference/README.md`, and `docs/reference/log.md`, passed all focused `src/core` and `src/api` UX unit tests plus `ruff check`, `ruff format --check`, and `mypy`, and configured privacy-safe repository-local Git email (`8036360+jmservera@users.noreply.github.com`) for the post-Review local commit on `feat/ux-155-usability-programme`.

## Completed Work

### P01: Core usability programme contract and documentation (`P01-T01`, `P01-T02`)

* Bootstrapped gitignored `.venv` (`python3 -m venv --system-site-packages .venv && .venv/bin/pip install --no-deps -e src/core -e src/agents -e src/api -e src/importer -e src/orchestrator`) so all five `zava_forward.*` packages resolve directly to this worktree without mutating `/home/azureuser/.local`.
* Created `src/core/src/zava_forward/core/usability_programme.py` implementing `default_programme_plan`, `validate_programme_plan`, `derive_task_scripts`, `validate_task_scripts`, `validate_audit_use_agreement`, `evaluate_role_measures`, `log_finding`, `validate_findings_log`, `evaluate_programme_results`, and `build_synthetic_walkthrough_report`, verified clean under `ruff format --check`, `ruff check`, and `mypy`.
* Appended `## Usability testing programme contract and evaluator (#155)` to `src/core/README.md`.

### P02: UX usability testing programme specification and knowledge base (`P02-T01`, `P02-T02`)

* Upgraded `docs/reference/research/ux/usability-test-programme-plan.md` in place (`ms.date: 2026-11-15`) covering all 13 representative role cohorts (`5 to 8`) plus `proxy-pilot` (`2 to 3`), 8 accessibility clauses and 4 AT routes, 8 separate consent and synthetic-only data-handling clauses, all 21 contract-derived scripts (`T0`, `T1`..`T8`, `R-J1`..`R-R1`, `B1`..`B5`), `SA-010` prior staff agreement and sub-5 `None` masking, mandatory GitHub backlog issue links on `UF-NNN` findings, blank `Not run` human records, and the labelled `Synthetic walkthrough - not user validation` (`not_user_validation = True`) baseline.
* Updated `docs/reference/research/ux/design-system.md` column 5 on the Usability programme row while preserving column 3 and column 6 (`pending human test: ...`), updated Task Routing and the UX index row in `docs/reference/README.md`, and appended a dated 2026-11-15 entry to `docs/reference/log.md`.

### P03: Unit test coverage, focused validation, and local commit readiness (`P03-T01`, `P03-T02`, `P03-T03`)

* Created `src/core/tests/test_usability_programme.py` (`UsabilityProgrammeTests`, 15 focused test methods, 0 skips) verifying cohort sizing and pilot exclusion, accessibility/AT and consent/data clauses, live derivation of all 21 task scripts + `OUT_OF_SCOPE` exclusion + `O16` single-count enforcement, `SA-010` prior `named_human` agreement + ISO date validation + `FORBIDDEN_MEASURE_FIELDS` rejection + sub-5 `None` masking + `H4` stop-rule surfacing + cohort-scoped `T0` + accessible SUS `inconclusive` fallback, findings severity/backlog/anonymisation/`retested` rules, negative/inconclusive anti-suppression, `not_user_validation=True` synthetic/proxy enforcement, `build_synthetic_walkthrough_report()`, and `usability-test-programme-plan.md` contract alignment.
* Executed focused-tier validation across `src/core` and `src/api` (`unittest`, `ruff check .`, `ruff format --check .`, `mypy`, and relative Markdown link checks), passing with exit code `0`.
* Resolved authenticated GitHub user via `gh api user` (`8036360+jmservera@users.noreply.github.com`), configured repository-local `git config --local user.email`, verified branch `feat/ux-155-usability-programme`, and verified `.venv` is excluded by `.gitignore` ahead of the post-Review local commit (`Refs #155`, no push, no PR).

## Implementation-Time Plan and Detail Updates

* Local judgment (`P01-T01` / `P03-T02`): Installed all five editable workspace distributions (`src/core`, `src/agents`, `src/api`, `src/importer`, `src/orchestrator`) with `.venv/bin/pip install --no-deps -e ...` (omitting `--no-build-isolation` so `bdist_wheel` was available) so cross-package imports resolve cleanly to the current worktree; `.venv` remains gitignored.
* Local judgment (`P02-T01`): Verified every requirement token against `docs/brds/agentic-retrofit-programme-brd.md` and `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, replacing non-existent `NFR-030` on `T6` with real `NFR-001` and `AC-093` in both `usability_programme.py` and `usability-test-programme-plan.md`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `UsabilityProgrammeTests` (`test_usability_programme.py`) | `src/core` | Passed | 15 tests in `0.035s` (`OK`) |
| Related `src/core` UX/journey/bundle/store suites (`test_profile_journey_contract`, `test_learning_test_bundles`, `test_perspective_walkthroughs`, `test_journey_register`, `test_bulk_edits`, `test_historical_backfill`, `test_stock_fabric`, `test_taskqueues`) | `src/core` | Passed | 103 + 43 targeted tests (`OK`) |
| `src/core` lint, formatting, and static typing (`ruff check .`, `ruff format --check .`, `mypy`) | `src/core` | Passed | `All checks passed!`, `266 files already formatted`, `Success: no issues found in 319 source files` |
| `src/api` UX traceability, acceptance protocol, and same-home suites (`test_epic149_ux_journey_requirement_traceability`, `test_epic149_ux_evidence_results`, `test_ux_design_traceability`, `test_production_ux_acceptance_protocol`, `test_same_home_profile_journey_acceptance`) | `src/api` | Passed | 30 tests in `6.892s` (`OK`) |
| `src/api` lint, formatting, and static typing (`ruff check .`, `ruff format --check .`, `mypy`) | `src/api` | Passed | `All checks passed!`, `213 files already formatted`, `Success: no issues found in 297 source files` |
| Relative Markdown link verification | `usability-test-programme-plan.md`, `design-system.md`, `docs/reference/README.md`, `docs/reference/log.md` tail, `src/core/README.md` | Passed | Every relative target verified on disk |
| Complete local gate (`tools/rpi-checks.py --all`) | Repository-wide | Skipped | Explicitly excluded by caller instruction (focused validation tier selected for Issue #155) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P02`, `P03` and all `P01-T01`..`P03-T03` checked)
* Completed-work evidence and handoff prose: Reconciled
* Validation, blockers, remaining work, and follow-up items: Reconciled
* Review readiness: Ready for `rpi-review`

## Blockers

* None

## Remaining Work

* None in active implementation scope (`rpi-review` and final post-Review local Git commit follow immediately in the automatic RPI loop)

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/ux-155-usability-programme-plan.md, `## Follow-Up Items`
* Obtain named staff representative sign-off on the `SA-010` non-surveillance audit-use statement and owner ratification of the usability test plan (`Refs #155`, `#150`).
* Record DPO lawful-basis, optional-recording, and retention decision for usability study consent/notes (`Refs #155`, `#128`).
* Execute 2-3 proxy pilot followed by moderated 5-8 participant sessions per role including assistive-technology users (`Refs #155`, `#151`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan; completed `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`, `P02-T02`), `P03` (`P03-T01`, `P03-T02`, `P03-T03`); remaining: None
* Validation coverage: Focused tier passed (`src/core` and `src/api` unit tests, `ruff check`, `ruff format --check`, `mypy`, Markdown links)
* Blockers: None
* Current plan and detail updates: Local `NFR-001`/`AC-093` token alignment on `T6` and 5-package `.venv` editable install recorded
* Planning and critique state: Ready (`PC-001`..`PC-005` resolved)
* Follow-up items: Three external human governance/session items mirrored from plan
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
