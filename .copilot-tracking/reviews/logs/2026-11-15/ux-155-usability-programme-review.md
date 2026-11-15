<!-- markdownlint-disable-file -->
# Review: Usability Testing Programme with Representative Users (Issue #155)

## Scope and Evidence

* Task ID: issue-155-usability-programme-1507
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Issue #155 acceptance criteria (`AC1`-`AC6` in plan), `zava_forward.core.usability_programme` contract/evaluator and unit tests, `docs/reference/research/ux/usability-test-programme-plan.md` specification and companion KB files (`design-system.md`, `docs/reference/README.md`, `docs/reference/log.md`, `src/core/README.md`), critique dispositions (`PC-001`..`PC-005`), focused-tier validation evidence, and external human follow-up boundaries (`Refs #155`)
* Plan: .copilot-tracking/plans/2026-11-15/ux-155-usability-programme-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ux-155-usability-programme-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/ux-155-usability-programme-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/ux-155-usability-programme-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/ux-155-usability-programme-research.md; `src/core/src/zava_forward/core/usability_programme.py`; `src/core/tests/test_usability_programme.py`; `docs/reference/research/ux/usability-test-programme-plan.md`; `docs/reference/research/ux/design-system.md`; `docs/reference/README.md`; `docs/reference/log.md`; `src/core/README.md`

## Opening Review State

* Interpreted review goal: Independently verify that all Issue #155 acceptance criteria, plan tasks (`P01`-`P03`), critique dispositions (`PC-001`..`PC-005`), focused-tier validations, and non-validation human-gate boundaries (`not_user_validation=True`, `Refs #155`) are satisfied and reconciled without overclaiming human usability validation.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; research, plan, phase details, one-pass plan critique, and reconciled changes record are present and aligned.
* Acceptance basis: Issue #155 prompt acceptance criteria and Objectives 1-3, synthesized `FR1`-`FR8`, `NFR1`-`NFR5`, `AC1`-`AC6` in the plan, and resolved critique dispositions `PC-001`..`PC-005`.
* First comparison boundary: Reconcile `P01`-`P03` markers, implementation-time local judgments, and critique dispositions against the delivered files and validation outputs before recording final `RV-xxx` findings and verdict.
* Active read-only boundaries: `rpi-review` updates only `.copilot-tracking/reviews/logs/2026-11-15/ux-155-usability-programme-review.md` (and parent RPI session state on completion); production files, tests, documentation, plan, details, critique, research, and changes record remain read-only during Review.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Single-pass post-implementation review completed on 2026-11-15 across `.copilot-tracking/plans/2026-11-15/ux-155-usability-programme-plan.md`, `.copilot-tracking/details/2026-11-15/ux-155-usability-programme-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/ux-155-usability-programme-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/ux-155-usability-programme-changes.md`, `.copilot-tracking/research/2026-11-15/ux-155-usability-programme-research.md`, delivered source/tests/docs, focused validation results, and an independent read-only review lens check.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `P01: Core usability programme contract and documentation (P01-T01, P01-T02)` | Reconciled | `src/core/src/zava_forward/core/usability_programme.py` and `src/core/README.md` match planned functions, dataclasses, constants, and evidence boundaries |
| `P02` (`P02-T01`, `P02-T02`) | `P02: UX usability testing programme specification and knowledge base (P02-T01, P02-T02)` | Reconciled | `docs/reference/research/ux/usability-test-programme-plan.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/README.md`, and `docs/reference/log.md` updated and aligned with `usability_programme.py` |
| `P03` (`P03-T01`, `P03-T02`, `P03-T03`) | `P03: Unit test coverage, focused validation, and local commit readiness (P03-T01, P03-T02, P03-T03)` | Reconciled | `src/core/tests/test_usability_programme.py` (15 tests, 0 skips), focused `src/core` and `src/api` test/`ruff`/`mypy` runs, and privacy-safe `git config --local user.email` verified |
| `Follow-Up Items` | `Follow-Up Items` mirrored in changes record | Reconciled | External human `SA-010` sign-off, DPO retention decision, and moderated 5-8 participant sessions remain outside active software scope (`Refs #155`) |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/usability_programme.py` | Implemented typed usability programme plan validator, live 21-script derivation from `profile_journey_contract`, `perspective_walkthroughs`, `journey_register` and `learning_test_bundles`, `SA-010` prior `named_human` + ISO-date gate and sub-5 `None` cell masking, backlog-linked findings logger, negative/inconclusive anti-suppression, and `not_user_validation=True` synthetic walkthrough builder | Module present, imported cleanly in `.venv`, and exercised across all 15 unit tests | `unittest`, `ruff check .`, `ruff format --check .`, `mypy` passed in `src/core` | Reconciled |
| `P01-T02` | `src/core/README.md` | Documented `#155` contract API, `SA-010` privacy rules, and `not_user_validation=True` synthetic evidence boundary | Section `## Usability testing programme contract and evaluator (#155)` appended at EOF | Relative Markdown link check passed | Reconciled |
| `P02-T01` | `docs/reference/research/ux/usability-test-programme-plan.md` | Upgraded specification in place (`ms.date: 2026-11-15`) with 13 representative cohorts (`5 to 8`) + `proxy-pilot` (`2 to 3`), 8 accessibility clauses + 4 AT routes, 8 separate consent/synthetic-data clauses, 21 derived scripts (`T0`, `T1`-`T8`, `R-J1`..`R-R1`, `B1`-`B5`), `SA-010` statement, blank `Not run` human tables, and labelled synthetic baseline | Verified against `default_programme_plan()` by `test_markdown_specification_matches_contract_and_keeps_human_sessions_not_run` and `src/api` UX traceability suites | `test_usability_programme.py` and `src/api` UX traceability suites passed | Reconciled |
| `P02-T02` | `docs/reference/research/ux/design-system.md`, `docs/reference/README.md`, `docs/reference/log.md` | Linked `UsabilityProgrammeTests::test_markdown_specification_matches_contract_and_keeps_human_sessions_not_run` in `design-system.md` column 5 while keeping column 3 and column 6 `pending human test: ...`, updated KB routing/index rows, and appended dated 2026-11-15 log entry | `test_ux_design_traceability.py` `ast.parse` check and relative link checks passed | `src/api` UX traceability suites + link verifier passed | Reconciled |
| `P03-T01` | `src/core/tests/test_usability_programme.py` | Added 15 focused unit tests (`<= 30` budget, 0 removals, 0 skips) covering AC1-AC5 positive and refusal paths plus Markdown contract synchronization | All 15 tests pass in `0.035s` | `unittest`, `ruff check .`, `ruff format --check .`, `mypy` passed | Reconciled |
| `P03-T02` | `src/core`, `src/api` | Executed focused validation suites, linters, format checks, and strict type checks in worktree `.venv` | Recorded in changes `## Validation Record` with zero errors | Passed (`103 + 43` `src/core` tests, `30` `src/api` UX tests, `ruff`, `mypy`) | Reconciled |
| `P03-T03` | `.git/config` (worktree-local), `feat/ux-155-usability-programme` | Configured `8036360+jmservera@users.noreply.github.com` via `gh api user` and verified branch and `.venv` `.gitignore` exclusion for post-Review single local commit (`Refs #155`, no push/PR) | `git config --local --get user.email` and `git check-ignore -v .venv` verified | Passed | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` / `P03-T02` (`.venv` editable bootstrap) | Installed all five workspace distributions (`src/core`, `src/agents`, `src/api`, `src/importer`, `src/orchestrator`) with `.venv/bin/pip install --no-deps -e ...` without `--no-build-isolation` so `bdist_wheel` was available and cross-package tests resolved to this worktree | Local tooling behavior during `P01-T01` and `P03-T02`; no user decision needed | Recorded in `.copilot-tracking/changes/2026-11-15/ux-155-usability-programme-changes.md` under `## Implementation-Time Plan and Detail Updates`; `.venv` verified gitignored | Not needed; preserves `PC-001` worktree isolation intent | Reconciled |
| `P02-T01` (`T6` requirement ID tokens) | Replaced draft token `NFR-030` on `T6` with real `NFR-001` and `AC-093` in both `usability_programme.py` and `usability-test-programme-plan.md` | Direct check against `docs/brds/agentic-retrofit-programme-brd.md` and `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, enforced by `test_epic149_ux_journey_requirement_traceability.py`; no user decision needed | Synchronized across code, Markdown table, and changes record | Not needed; preserves approved requirement traceability | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five findings (`PC-001`..`PC-005`) in `.copilot-tracking/reviews/plans/2026-11-15/ux-155-usability-programme-plan-critique.md` were disposed as `resolved` in the plan's `## Critique Disposition` table and verified in delivered artifacts (`P01 -> P02 -> P03` execution order, `design-system.md` `path::Class::method` syntax, `T8` contractor script + `validate_same_home_walk()`/`run_report()`/`reconcile_o16()` wiring, `SA-010` ISO date + `named_human` + sub-5 `None` masking + `H4` breach surfacing + cohort-scoped `T0` + accessible SUS `inconclusive` rule, four-class `evidence_source` + removal of unlinked `"no issue yet"`, and `P03-T03` privacy-safe Git email + post-Review single local commit coordination).
* Material revisions: None occurred during implementation; both local judgments preserved approved scope, architecture, and acceptance criteria.
* Dependent-work pause assessment: No dependent-work pause was triggered; tasks executed in acyclic plan order `P01 -> P02 -> P03`.
* Justification assessment: Supported by test and traceability evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Obtain named staff representative sign-off on the `SA-010` non-surveillance audit-use statement and owner ratification of the usability test plan | Requires real human consultation with workplace/staff representatives and programme owner before live staff session metrics may be recorded | Programme owner and staff representatives (`Refs #155`, `#150`) | Open external human governance gate; routed as distinct follow-up (kept `Not agreed` in repo) |
| Record DPO lawful-basis, optional-recording, and retention decision for usability study consent/notes | Requires named Data Protection Officer review before participant recruitment or optional session recording | Data Protection Officer (`Refs #155`, `#128`) | Open external data-protection gate; routed as distinct follow-up (kept `Not agreed` in repo) |
| Execute 2-3 proxy pilot followed by moderated 5-8 participant sessions per role including assistive-technology users | Requires live human participant recruitment after `SA-010` and DPO gates clear; cannot be fabricated by AI or synthetic walkthroughs | UX researcher and Resident Engagement lead (`Refs #155`, `#151`) | Open external human validation work; routed as distinct follow-up (kept `Not run` in repo) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Pre-wave-1 multi-wave outcome keying, unobserved-metric tri-state, and custom audit-statement negation hardening

* Related scope: `P01-T01`, `P03-T01`
* Evidence: `src/core/src/zava_forward/core/usability_programme.py` (`validate_audit_use_agreement`, `evaluate_role_measures`, `evaluate_programme_results`) and independent read-only review lens inspection. For single-wave evaluation and the canonical `DEFAULT_AUDIT_USE_STATEMENT`, all Issue #155 AC1-AC5 invariants hold (`human_usability_signoff` is unconditionally `False`, sub-5 cohorts mask `participant_count` and metrics to `None` per `journey_register.MIN_CELL_FLOOR = 5` while keeping `5-8` raw counts publishable per `SA-009`). Before ingesting multi-wave live human session batches alongside synthetic baselines in one combined call, three defensive tightenings would further harden the evaluator against caller misuse: keying `OutcomeRecord` uniqueness by `(target_id, cohort_id, evidence_source)` rather than `target_id` alone, distinguishing `None` (unobserved -> `inconclusive`) from observed `0` on `manual_fallback_completed_count` / `stop_rule_or_consent_blur_count`, and requiring `DEFAULT_AUDIT_USE_STATEMENT` exact match (or structured prohibition booleans) plus full 13-cohort `evaluate_role_measures()` coverage before `user_validation_established` can turn `True`.
* Impact: Non-blocking for Issue #155 specification and single-wave / synthetic evaluation (where synthetic and human tables are intentionally separated and `human_usability_signoff` remains `False`), but valuable defensive hardening before live wave-1 human session ingestion begins.
* Destination: follow-up
* Smallest useful next action: Add composite `(target_id, cohort_id, evidence_source)` keying, `None`-vs-`0` unobserved count handling, and exact/structured `AuditUseAgreement` + cohort-coverage checks in `usability_programme.py` prior to ingesting live wave-1 human session records.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `follow-up` | Optional engineering hardening in `zava_forward.core.usability_programme` before live wave-1 human data ingestion | Non-blocking defensive hardening beyond current single-wave / synthetic contract requirements |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001`: Optional defensive evaluator hardening (composite `(target_id, cohort_id, evidence_source)` multi-wave keying, `None`-vs-`0` unobserved metric tri-state, and structured `AuditUseAgreement` / full-cohort check on `user_validation_established`) before live wave-1 human data ingestion.
* External human governance and research execution items recorded in plan `## Follow-Up Items` (`SA-010` staff sign-off, DPO retention approval, and moderated 5-8 participant sessions per role; `Refs #155`).

## Blockers and Remaining Work

* Blockers: None for the Issue #155 specification and `src/core` contract/evaluator deliverables (live human usability acceptance itself remains gated on external human `SA-010`, DPO, and moderated participant sessions, so Issue #155 stays open under `Refs #155`).
* Remaining active work: None across `P01`, `P02`, or `P03` (only the post-Review single local Git commit on `feat/ux-155-usability-programme` remains for parent closeout).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `../../.venv/bin/python -m unittest tests/test_usability_programme.py -v` | `src/core/tests/test_usability_programme.py` | Passed | 15 tests passed in `0.035s` (`OK`) |
| `PYTHONPATH=tests ../../.venv/bin/python -m unittest tests/test_usability_programme.py tests/test_profile_journey_contract.py tests/test_learning_test_bundles.py tests/test_perspective_walkthroughs.py tests/test_journey_register.py tests/test_bulk_edits.py -q` (plus `PYTHONNOUSERSITE=1` runs of `test_historical_backfill`, `test_stock_fabric`, `test_taskqueues`) | `src/core` | Passed | `103 + 43` tests passed (`OK`) |
| `ruff check . && ruff format --check . && ../../.venv/bin/python -m mypy` | `src/core` | Passed | `All checks passed!`, `266 files already formatted`, `Success: no issues found in 319 source files` |
| `PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest tests/test_epic149_ux_journey_requirement_traceability.py tests/test_epic149_ux_evidence_results.py tests/test_ux_design_traceability.py tests/test_production_ux_acceptance_protocol.py tests/test_same_home_profile_journey_acceptance.py -q` | `src/api` UX traceability and acceptance suites | Passed | 30 tests passed in `6.892s` (`OK`) |
| `ruff check . && ruff format --check . && ../../.venv/bin/python -m mypy` | `src/api` | Passed | `All checks passed!`, `213 files already formatted`, `Success: no issues found in 297 source files` |
| Relative Markdown link verifier | Updated UX specification, `design-system.md`, `docs/reference/README.md`, `docs/reference/log.md` tail, `src/core/README.md` | Passed | All relative Markdown links resolved on disk |
| `python3 tools/rpi-checks.py --all` | Repository-wide full gate | Skipped | Explicitly excluded by user prompt (`Validation tier: Focused`) |

## Outcome

* Outcome: Conformant
* Outcome rationale: All planned tasks (`P01`-`P03`), synthesized requirements (`FR1`-`FR8`, `NFR1`-`NFR5`, `AC1`-`AC6`), critique dispositions (`PC-001`..`PC-005`), and Issue #155 specification and deterministic `src/core` evaluator objectives are complete, reconciled, and verified under the focused validation tier with zero material defects (`RV-001` is non-blocking `Low` defensive hardening routed to follow-up, and live human governance/sessions remain honestly marked `Not agreed` / `Not run` under `Refs #155`).

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | `RV-001` optional multi-wave evaluator hardening before wave-1 ingestion, plus external human `SA-010`, DPO, and moderated participant sessions (`Refs #155`) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier passed (`src/core` and `src/api` unit tests, `ruff check`, `ruff format --check`, `mypy`, relative Markdown link checks); `tools/rpi-checks.py --all` skipped per caller instruction
* Blockers: None

