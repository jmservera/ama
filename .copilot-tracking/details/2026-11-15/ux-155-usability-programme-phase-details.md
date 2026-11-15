<!-- markdownlint-disable-file -->
# RPI Phase Details: Usability Testing Programme with Representative Users (Issue #155)

## Metadata

* Task ID: issue-155-usability-programme-1507
* Task slug: ux-155-usability-programme
* Related plan: .copilot-tracking/plans/2026-11-15/ux-155-usability-programme-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/ux-155-usability-programme-research.md, docs/reference/research/ux/usability-test-programme-plan.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/brds/agentic-retrofit-programme-brd.md, src/core/src/zava_forward/core/profile_journey_contract.py, src/core/src/zava_forward/core/perspective_walkthroughs.py, src/core/src/zava_forward/core/learning_test_bundles.py, src/core/src/zava_forward/core/journey_register.py

## Phase Index

| Phase ID | Name                                                                        | Status      | Detail sections          |
|----------|-----------------------------------------------------------------------------|-------------|--------------------------|
| P01      | Implement deterministic usability programme contract and evaluator in `src/core` | Ready   | P01, P01-T01, P01-T02    |
| P02      | Upgrade UX usability testing programme specification and knowledge base     | Ready       | P02, P02-T01, P02-T02    |
| P03      | Add comprehensive unit tests, run focused validation, and prepare local commit governance | Ready | P03, P03-T01, P03-T02, P03-T03 |

<!-- rpi:phase id=P01 -->
## P01: Implement deterministic usability programme contract and evaluator in `src/core`

### Context

Research (`C1`, `C4`-`C7`) showed that `src/core` already encodes the 5-element profile journey contract (`profile_journey_contract.py`), the 11 PRD perspectives (`perspective_walkthroughs.py`), the 7 resident/representative journeys plus `IDENTITY_FIELDS` and `MIN_CELL_FLOOR = 5` (`journey_register.py`), and the 5 two-arm learning-test bundles (`learning_test_bundles.py`), while #155 had only a prose draft from 2026-11-04 and zero Python enforcement for plan structure, script derivation, `SA-010` staff audit-use gating, severity/backlog findings, negative/inconclusive outcome preservation, or synthetic walkthrough `not_user_validation=True` labelling.

### Intent

Add one cohesive, dependency-clean, `mypy --strict`-compliant module `src/core/src/zava_forward/core/usability_programme.py` and document it in `src/core/README.md`.

### Boundaries

* Included: `src/core/src/zava_forward/core/usability_programme.py` and `src/core/README.md`.
* Excluded: Modifying `journey_register.aggregate_usability` (#128), mutating `learning_test_bundles.py` or `profile_journey_contract.py`, or importing anything outside Python stdlib and `zava_forward.core`.

### Likely Targets

* src/core/src/zava_forward/core/usability_programme.py: New deterministic #155 contract, script derivation, `SA-010` evaluator, findings logger/validator, and synthetic walkthrough evaluator.
* src/core/README.md: Component index entry for `usability_programme`.

### Dependencies

* `zava_forward.core.profile_journey_contract` (`ELEMENTS`, `SIX_STAFF_PROFILES`, `BOUNDARIES`, `validate`)
* `zava_forward.core.perspective_walkthroughs` (`EVIDENCE`)
* `zava_forward.core.learning_test_bundles` (`BUNDLES`, `ARMS`, `O16_BUNDLES`, `OUT_OF_SCOPE`, `compare_bundle`)
* `zava_forward.core.journey_register` (`JOURNEYS`, `IDENTITY_FIELDS`, `MIN_CELL_FLOOR`)

### Validation Expectations

* `ruff check`, `ruff format --check`, `mypy`, and `test_dependency_rule.py` pass on `src/core`.

### Completion Evidence

* `zava_forward.core.usability_programme` imports cleanly from the worktree `.venv` and exposes typed contracts for all five Issue #155 acceptance criteria.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Bootstrap isolated worktree `.venv` and create `src/core/src/zava_forward/core/usability_programme.py`

#### Context

Issue #155 AC1-AC5 and Objectives 2a-2e require deterministic validation and evaluation across five tightly related boundaries (`C2`-`C11`), and `PC-001` requires bootstrapping the gitignored worktree-local `.venv` (`python3 -m venv --system-site-packages .venv && .venv/bin/pip install --no-build-isolation --no-deps -e src/core -e src/agents -e src/api`) first so all `P01` imports and `mypy` runs resolve this worktree rather than `/home/azureuser/source/ama`.

#### Intent

Bootstrap `.venv` and implement `usability_programme.py` with the following crisp, auditable public contract (incorporating `PC-002`, `PC-003`, and `PC-004`):

1. **Constants & boundaries**:
   * `MIN_ROLE_PARTICIPANTS = 5`, `MAX_ROLE_PARTICIPANTS = 8` (target 5-8 participants per role cohort across staff per `SA-009`, contractor, and voluntary resident/representative cohorts), `MIN_PILOT_PARTICIPANTS = 2`, `MAX_PILOT_PARTICIPANTS = 3`.
   * `PROTOTYPE_UX_CHECKS = ("UX-01", "UX-02", "UX-03", "UX-04", "UX-05", "UX-06", "UX-07", "UX-08")`.
   * `STAFF_PROFILE_TO_PERSPECTIVE`: explicit 1:1 mapping from `profile_journey_contract.SIX_STAFF_PROFILES` display names to their canonical `perspective_walkthroughs` slugs (`programme-coordinator`, `retrofit-case-team`, `assessor-designer`, `housing-resident-engagement`, `repairs-building-safety`, `quality-assurance`).
   * `ACCESSIBILITY_SUPPORT_CLAUSES` (`channel_choice`, `own_device_and_assistive_tech`, `advance_plain_language_briefing`, `interpreter_or_trusted_person`, `extra_time_no_stopwatch_pressure`, `voluntary_need_recording_only`, `pause_or_stop_anytime`, `manual_non_digital_parity`).
   * `CONSENT_DATA_CLAUSES` (`voluntary_participation`, `separate_from_tenancy_works_and_employment`, `synthetic_fictional_data_only`, `no_recording_without_separate_consent_and_dpo`, `revocable_before_aggregation`, `pseudonymised_notes_separate_from_signup`, `dpo_retention_gate_required`, `aggregate_reporting_only_sa010`).
   * `SEVERITY_LEVELS`: `1 -> "note"`, `2 -> "minor"`, `3 -> "major"`, `4 -> "blocker"`.
   * `FINDING_STATUSES = ("open", "in_progress", "retested", "accepted_risk")`.
   * `EVIDENCE_SOURCES = ("moderated_participant", "proxy_participant", "proxy_pilot", "synthetic_walkthrough")`.
   * `OUTCOMES = ("supported", "not_supported", "inconclusive", "not_run")`.
   * `SYNTHETIC_WALKTHROUGH_LABEL = "Synthetic walkthrough - not user validation"`.
   * `FORBIDDEN_MEASURE_FIELDS`: union of `journey_register.IDENTITY_FIELDS` and individual-surveillance keys (`"participant_id"`, `"participant_ids"`, `"employee_id"`, `"staff_id"`, `"staff_name"`, `"individual_scores"`, `"individual_times"`, `"participant_quotes"`, `"raw_sessions"`, `"session_recording"`).
2. **Plan schema & validator** (`ParticipantCohort`, `UsabilityTaskScript`, `UsabilityProgrammePlan`, `default_programme_plan()`, `validate_programme_plan(plan)`):
   * Role cohorts covering the 10 internal staff perspectives (`asset-investment`, `programme-coordinator`, `retrofit-case-team`, `assessor-designer`, `housing-resident-engagement`, `repairs-building-safety`, `procurement-contracts`, `quality-assurance`, `finance-grants`, `digital-auditor`), external supplier/contractor (`provider-contractor`), and voluntary resident & representative cohorts (`resident`, `resident-representative`), each sized with `min_participants=5, max_participants=8` (plus `proxy-pilot` cohort `2..3`, explicitly flagged `counts_toward_role_minimum=False`), with `t0_applicable=True` for staff/workbench cohorts and `t0_applicable=False` for `resident` and `resident-representative`.
   * Validates non-empty tasks, `5 <= min_participants <= max_participants <= 8` on every non-pilot role cohort, complete accessibility support clauses (including screen reader, keyboard-only, magnification/zoom, and non-digital route coverage), complete voluntary separate consent and synthetic-only data-handling clauses, and `thresholds_are_hypotheses=True`.
3. **Direct task-script derivation** (`derive_task_scripts()`, `validate_task_scripts(scripts)`):
   * Uses one canonical script ID set across code and Markdown:
     * **Profile & prototype scripts (`T0`, `T1`..`T8`)**: binds all 11 perspectives from `perspective_walkthroughs.EVIDENCE` and `perspective_walkthroughs.register()` (preserving `PROXY_ONLY` login gaps and `partial`/`unmet` element status), maps `SIX_STAFF_PROFILES` to perspective slugs for the connected same-home check, covers `T0` (`SA-009` unaided `<5m` find-case + next-step + owner hypothesis for staff/workbench cohorts), `T1`-`T7` mapped to `UX-01`..`UX-08`, and `T8` (`provider-contractor` submission, correction, acknowledgement vs quality acceptance, and rejected submission with no stated reason), with all five `profile_journey_contract.ELEMENTS` (`entry`, `evidence`, `safe_endpoint`, `recovery`, `handoff`) and `NFR-009` manual fallback prompts.
     * **Resident & representative scripts (`R-J1`..`R-J6`, `R-R1`)**: derives directly from `journey_register.JOURNEYS` (`J1`-`J6`, `R1`) with `entry`, `evidence`, `safe_endpoint`, `recovery`, and `handoff` checkpoints, resident channel choices, and `R1` authority-scope verification.
     * **Learning-test bundle scripts (`B1-story-once`, `B2-pre-visit-pack`, `B3-change-impact`, `B4-handover-aftercare`, `B5-funding-evidence`)**: derives directly from `learning_test_bundles.BUNDLES` with two arms (`comparator`, `workflow`), exact `comparator` baseline label, `atlas_ids`, `linked_requirements`, `learning_question`, `zero_measures`, `beyond_effort_measures`, `stop_rule`, constructed Atlas `C10` failure-case prompts, and explicit `O16` single-counting note on `change-impact` and `funding-evidence` (`O16_BUNDLES`).
   * `validate_task_scripts` verifies complete coverage of `T0`, `T1`-`T8`, `R-J1`..`R-J6`, `R-R1`, `B1-story-once`..`B5-funding-evidence`, all 11 perspectives, all 6 mapped `SIX_STAFF_PROFILES`, all 5 `profile_journey_contract.ELEMENTS`, `UX-01`..`UX-08`, all 7 `journey_register.JOURNEYS`, all 5 `learning_test_bundles.BUNDLES`, `O16` single-count metadata, and zero `OUT_OF_SCOPE` (`O10`, `O18`-`O20`) leakage.
4. **SA-010 audit-use agreement & aggregate-only measures** (`AuditUseAgreement`, `validate_audit_use_agreement(agreement, measurement_date=...)`, `evaluate_role_measures(role_records, agreement, measurement_date=...)`):
   * `AuditUseAgreement` holds `agreed_with_staff: bool`, `agreed_date: str | None` (`YYYY-MM-DD`), `staff_representatives: tuple[str, ...]`, `programme_owner: str | None`, `dpo_reviewer: str | None`, and `statement_text: str`.
   * Validates ISO dates via `datetime.date.fromisoformat`, validates every entry in `staff_representatives` with `rai_release.named_human`, requires `measurement_date` whenever any cohort has `participant_count > 0`, and raises `ValueError` if `not agreement.agreed_with_staff`, `agreed_date` is missing/invalid or after `measurement_date`, `staff_representatives` is empty or fails `named_human`, or `statement_text` lacks explicit non-audit / non-disciplinary / non-individual-performance guarantees (`SA-010`).
   * Inspects every role record recursively for `FORBIDDEN_MEASURE_FIELDS` and raises `ValueError` on any individual-level key or per-participant list, or out-of-range counts/SUS scores (`0.0 <= sus <= 100.0`).
   * Uses clean `snake_case` fields: `participant_count`, `unaided_under_5m_count`, `sus_median`, `sus_min`, `sus_max`, `accessible_sus_alternative_count`, `manual_fallback_completed_count`, `stop_rule_or_consent_blur_count`.
   * For `participant_count == 0`, marks status `"not_run"`. For `0 < participant_count < MIN_CELL_FLOOR` (`5`), sets `suppressed=True`, reason `"cell_below_min_floor_5"`, and masks `participant_count` (`n`) and ALL numeric count/percentage/SUS fields in the output summary to `None` so sub-5 cell sizes never leak (still flagging `h4_breach=True` if `stop_rule_or_consent_blur_count > 0` without leaking counts). For `participant_count >= 5`, reports raw counts alongside coarse whole-number percentages, scopes `T0` (`H1` `>=80%` `<5m`) to `t0_applicable=True` cohorts (`"not_applicable"` for resident/representative cohorts), treats `< 5` numeric SUS responses due to `accessible_sus_alternative_count > 0` as `"inconclusive"` rather than `"not_supported"`, flags any `stop_rule_or_consent_blur_count > 0` as `"not_supported"` (`h4_breach=True`), and sets `thresholds_are_hypotheses=True` and `human_usability_signoff=False`.
5. **Findings logger & validator** (`UsabilityFinding`, `log_finding(...)`, `validate_findings_log(findings)`):
   * Enforces `UF-\d{3,}` ID uniqueness, `severity in {1, 2, 3, 4}`, `evidence_source in EVIDENCE_SOURCES`, valid `script_id` / `journey_or_bundle_id`, plain-language `observation` and `impact` with no `IDENTITY_FIELDS` or email patterns, valid `backlog_issue` matching `^#[1-9]\d*$` or `^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/issues/[1-9]\d*$`, mandatory `rai_release.named_human(risk_owner)` + `risk_rationale` when `status == "accepted_risk"`, and rejects `status == "retested"` when `evidence_source in {"synthetic_walkthrough", "proxy_pilot"}`.
6. **Negative/inconclusive outcomes & synthetic walkthrough evaluator** (`OutcomeRecord`, `SyntheticWalkthroughReport`, `evaluate_programme_results(...)`, `build_synthetic_walkthrough_report(...)`):
   * `OutcomeRecord` captures `target_id`, `outcome` (`"supported"`, `"not_supported"`, `"inconclusive"`, `"not_run"`), `evidence_source` (`EVIDENCE_SOURCES`), `not_user_validation: bool`, `validation_label: str`, `summary: str`, and `negative_or_failure_notes: tuple[str, ...]`.
   * Rejects any record with `evidence_source == "synthetic_walkthrough"` that attempts `not_user_validation=False` or `validation_label != SYNTHETIC_WALKTHROUGH_LABEL`, and requires `not_user_validation=True` for `"proxy_pilot"` and `"proxy_participant"` as well (with honest pilot/proxy labels).
   * Rejects any `not_supported` or `inconclusive` record whose summary or failure notes are blank.
   * `evaluate_programme_results` returns outcome counts (`supported`, `not_supported`, `inconclusive`, `not_run`), verifies zero suppressed negative/inconclusive rows, keeps `human_usability_signoff=False` in automated outputs, and forces `user_validation_established=False` whenever any target is synthetic, proxy, `not_run`, `not_supported`, `inconclusive`, missing `SA-010` agreement, or carrying an open severity-4 blocker.
   * `build_synthetic_walkthrough_report()` executes `profile_journey_contract.validate()`, `profile_journey_contract.validate_same_home_walk()`, `learning_test_bundles.run_report()`, and `learning_test_bundles.reconcile_o16()` across constructed cases covering `supported`, negative (`not_supported`), and `inconclusive` arms, stamping every record and the top-level report with `not_user_validation=True`, `validation_label="Synthetic walkthrough - not user validation"`, `user_validation_established=False`, and `human_usability_signoff=False`.

#### Boundaries

* Included: Complete `usability_programme.py` implementation with docstrings and strict type annotations.
* Excluded: File I/O on user datasets (`ZF_DATA`), network calls, or mutating other `src/core` modules.

#### Likely Targets

* src/core/src/zava_forward/core/usability_programme.py: Create module.

#### Dependencies

* Existing `zava_forward.core` journey/bundle/perspective modules.

#### Validation Expectations

* `ruff check src/zava_forward/core/usability_programme.py`, `ruff format --check src/zava_forward/core/usability_programme.py`, and `mypy src/zava_forward/core/usability_programme.py` exit `0`.

#### Completion Evidence

* Module imports and executes `validate_programme_plan(default_programme_plan())`, `derive_task_scripts()`, and `build_synthetic_walkthrough_report()` cleanly.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Document `usability_programme` in `src/core/README.md`

#### Context

`src/core/README.md` documents core domain contracts and commands.

#### Intent

Add a concise reference bullet/row for `zava_forward.core.usability_programme` explaining its role for Issue #155 (`SA-009`/`SA-010`, script derivation from `profile_journey_contract` and `learning_test_bundles`, findings/backlog validation, and `not_user_validation=True` synthetic walkthrough labelling).

#### Boundaries

* Included: `src/core/README.md`.
* Excluded: Unrelated `src/core` documentation sections.

#### Likely Targets

* src/core/README.md: Update module summary.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Relative links and module names match `src/core/src/zava_forward/core/usability_programme.py`.

#### Completion Evidence

* Clean diff in `src/core/README.md`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Upgrade UX usability testing programme specification and knowledge base

### Context

`docs/reference/research/ux/usability-test-programme-plan.md` was drafted on 2026-11-04 (`C1`) before `profile_journey_contract.md` (#134) and the updated `journey-learning-test-bundles.md` (#129) landed on 2026-11-15 (`C6`, `C9`). It is already linked by `docs/reference/README.md` and `docs/reference/research/ux/design-system.md` (`C12`).

### Intent

Upgrade `usability-test-programme-plan.md` in place so every Issue #155 acceptance criterion and Objective 2 item is thoroughly specified and cross-linked to `zava_forward.core.usability_programme` and `test_usability_programme.py`, then update `design-system.md`, `docs/reference/README.md`, and `docs/reference/log.md`.

### Boundaries

* Included: `docs/reference/research/ux/usability-test-programme-plan.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/README.md`, and `docs/reference/log.md`.
* Excluded: Rewriting earlier `docs/reference/log.md` entries, editing `docs/reference/memory.md`, or claiming WCAG/human usability conformance in `design-system.md`.

### Likely Targets

* docs/reference/research/ux/usability-test-programme-plan.md: Upgrade specification in place.
* docs/reference/research/ux/design-system.md: Add `test_usability_programme.py` to Usability programme traceability row while preserving `pending human test` status text.
* docs/reference/README.md: Update Task Routing and UX table description/date for `usability-test-programme-plan.md`.
* docs/reference/log.md: Append 2026-11-15 entry.

### Dependencies

* P01-T01.

### Validation Expectations

* Relative Markdown links, YAML frontmatter, and AMA Markdown style rules pass inspection in `P02`; full automated cross-suite traceability tests (`test_epic149_ux_journey_requirement_traceability.py`, `test_epic149_ux_evidence_results.py`, `test_ux_design_traceability.py`, `test_production_ux_acceptance_protocol.py`) execute in `P03-T02` once `P03-T01` creates `src/core/tests/test_usability_programme.py`.

### Completion Evidence

* Updated Markdown diffs cleanly follow AMA Markdown style (`*` unordered lists, ASCII punctuation, no em dashes, no bolded-prefix list items in new content, valid YAML frontmatter with `ms.date: 2026-11-15` and no duplicate H1).

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Upgrade `docs/reference/research/ux/usability-test-programme-plan.md` in place

#### Context

Research (`C1`, `C2`, `C4`-`C12`) identified exact upgrades needed in `usability-test-programme-plan.md`:
1. Set proposed target cohort sizing to **5 to 8 participants per role** across staff roles (`SA-009`), contractor roles (`provider-contractor`), and voluntary resident and representative cohorts (`resident`, `resident-representative`), qualifying that `SA-009` directly sizes 5-8 Excel staff users per role while resident/representative and contractor 5-8 sizing is the programme's proposed cohort target (`MIN_CELL_FLOOR = 5`) subject to voluntary recruitment, Resident Engagement, owner, and DPO confirmation.
2. Add explicit derivation tables connecting:
   * Every one of the 11 PRD perspectives (`perspective_walkthroughs.EVIDENCE`), the 6-staff same-home contract (`SIX_STAFF_PROFILES`), and the five `profile_journey_contract.ELEMENTS` (`entry`, `evidence`, `safe_endpoint`, `recovery`, `handoff`) + `UX-01`..`UX-08` + `J1`-`J6`/`R1` to moderated task scripts `T0`, `T1`-`T7`, and `J1`-`J6`/`R1` (referencing `[profile-journey-contract.md](profile-journey-contract.md)`).
   * Every one of the 5 `learning_test_bundles` (`story-once`, `pre-visit-pack`, `change-impact`, `handover-aftercare`, `funding-evidence`) with its two arms (`comparator`, `workflow`), comparator baseline, Atlas IDs, zero-target safety/consent/provenance measures, stop rule, and `O16` single-counting rule to bundle scripts `B1`-`B5` (referencing `[journey-learning-test-bundles.md](journey-learning-test-bundles.md)` and `[customer-journeys/customer-journey-atlas.md](customer-journeys/customer-journey-atlas.md)`).
3. Document deterministic validation via `zava_forward.core.usability_programme` and `test_usability_programme.py`, including `SA-010` prior staff audit-use agreement enforcement, `n >= 5` cell floor, severity `1..4` + GitHub issue (`#NNN`) findings log rules, negative (`not_supported`) and `inconclusive` outcome reporting rules, and a clearly separated **Synthetic walkthrough contract verification (`not_user_validation=True`, `"Synthetic walkthrough - not user validation"`)** section alongside the **`Not run` human participant results register**.
4. Ensure every `(FR|NFR|AC|SA|OD)-\d+` ID used in the document exists in the BRD or PRD (`SA-009`, `SA-010`, `NFR-008`, `NFR-009`, `NFR-015`, `NFR-030`, `AC-071`, `FR-009`, `FR-010`, `FR-015`, `FR-025`, `FR-029`, `FR-032`; note `OQ-004`, `OQ-005`, `OQ-011`, `OQ-012` are open questions and valid).

#### Intent

Produce a complete, traceable, plain-ASCII specification in `docs/reference/research/ux/usability-test-programme-plan.md`.

#### Boundaries

* Included: `docs/reference/research/ux/usability-test-programme-plan.md`.
* Excluded: Claiming any human usability session has run or that `SA-010` staff agreement has been signed.

#### Likely Targets

* docs/reference/research/ux/usability-test-programme-plan.md: Edit in place.

#### Dependencies

* P01-T01 (strictly acyclic `P01 -> P02 -> P03` order; `test_usability_programme.py` is created in `P03-T01` before `P03-T02` runs the `src/api` UX traceability suites).

#### Validation Expectations

* Relative links, valid BRD/PRD requirement tokens, canonical script IDs (`T0`, `T1`-`T8`, `R-J1`..`R-J6`, `R-R1`, `B1-story-once`..`B5-funding-evidence`), removal of `"no issue yet"` from the Findings Log rule, and zero em dashes or bolded-prefix list items in new content; automated `src/api` + `src/core` traceability assertions pass in `P03-T02`.

#### Completion Evidence

* Updated `docs/reference/research/ux/usability-test-programme-plan.md` with `ms.date: 2026-11-15`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Update `design-system.md`, `docs/reference/README.md`, and `docs/reference/log.md`

#### Context

KB conventions require updating `docs/reference/README.md` and appending an entry to `docs/reference/log.md` whenever a knowledge-base document materially changes, and `design-system.md:237` holds the traceability row for `usability-test-programme-plan.md` whose column 5 is parsed by `ast.parse()` in `test_ux_design_traceability.py`.

#### Intent

* Preserve column 3 (`[usability-test-programme-plan.md](usability-test-programme-plan.md)`) and column 6 (`pending human test: ...`) of the `Usability programme` row in `docs/reference/research/ux/design-system.md`, and append `` `src/core/tests/test_usability_programme.py::UsabilityProgrammeTests::test_markdown_specification_matches_contract_and_keeps_human_sessions_not_run` `` alongside the existing `` `src/api/tests/test_production_ux_acceptance_protocol.py::ProductionUxAcceptanceProtocol::test_every_record_cell_is_not_run_or_names_tester_and_date` `` token in column 5.
* Update `docs/reference/README.md` Task Routing and UX table entry for `usability-test-programme-plan.md` to reflect the completed 2026-11-15 usability programme specification and `zava_forward.core.usability_programme` contract.
* Append a dated `2026-11-15` entry at the end of `docs/reference/log.md`.

#### Boundaries

* Included: `docs/reference/research/ux/design-system.md`, `docs/reference/README.md`, `docs/reference/log.md`.
* Excluded: Rewriting earlier `docs/reference/log.md` entries or modifying `docs/reference/memory.md`.

#### Likely Targets

* docs/reference/research/ux/design-system.md: Traceability table row column-5 append.
* docs/reference/README.md: Task Routing + UX index row update.
* docs/reference/log.md: Append-only log entry.

#### Dependencies

* P02-T01.

#### Validation Expectations

* Relative links resolve and column-5 syntax follows `path::Class::method`; verified via `test_ux_design_traceability.py`, `test_production_ux_acceptance_protocol.py`, and `test_epic149_ux_journey_requirement_traceability.py` in `P03-T02`.

#### Completion Evidence

* Clean Git diff across all three files.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Add comprehensive unit tests, run focused validation, and prepare clean branch state

### Context

Objective 3 and the focused validation tier require comprehensive unit tests in `src/core/tests/`, `ruff check`, `ruff format --check`, and `mypy`, plus clean local commit readiness on `feat/ux-155-usability-programme`. Research Contrarian Wave 3 also proved that a gitignored worktree-local `.venv` is required so subprocess CLI tests (`test_learning_test_bundles.py`) and `src/api/tests/` import `zava_forward.core` from this worktree rather than `/home/azureuser/source/ama`.

### Intent

Create `src/core/tests/test_usability_programme.py` and run all targeted checks cleanly inside `.venv`.

### Boundaries

* Included: `src/core/tests/test_usability_programme.py`, gitignored worktree-local `.venv` for validation, `unittest`, `ruff`, and `mypy`.
* Excluded: `tools/rpi-checks.py --all`, pushing to remote, opening a PR, or leaving untracked temporary files.

### Likely Targets

* src/core/tests/test_usability_programme.py: New unit test module (max 1 test file added, 0 removed).

### Dependencies

* P01, P02.

### Validation Expectations

* `src/core` full unit test discovery passes (`python -m unittest discover -s tests -v`).
* `src/api` UX traceability tests pass (`test_epic149_ux_journey_requirement_traceability.py`, `test_epic149_ux_evidence_results.py`, `test_ux_design_traceability.py`).
* `ruff check .`, `ruff format --check .`, and `mypy` pass in `src/core`.

### Completion Evidence

* Exact exit code `0` outputs recorded in `.copilot-tracking/changes/2026-11-15/ux-155-usability-programme-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Create `src/core/tests/test_usability_programme.py`

#### Context

Tests must cover behavioral invariants that would fail without `usability_programme.py` and verify edge/refusal cases across AC1-AC5 without trivial constant checks or `@unittest.skip`.

#### Intent

Author `src/core/tests/test_usability_programme.py` (1 file added, 0 removed, <= 30 test methods) covering:
* **AC1 (Plan validation)**: `default_programme_plan()` passes validation; out-of-range role cohorts (`<5` or `>8`), missing accessibility clauses (e.g., screen reader/keyboard/non-digital), missing voluntary separate consent, or allowing real personal data fails `validate_programme_plan()`.
* **AC2 (Task script derivation)**: `derive_task_scripts()` covers all 11 perspectives from `perspective_walkthroughs.EVIDENCE`, all 5 `profile_journey_contract.ELEMENTS`, the 6-staff same-home contract, `UX-01`..`UX-08`, `J1`-`J6`/`R1` from `journey_register.JOURNEYS`, and all 5 `learning_test_bundles.BUNDLES` with matching comparators, stop rules, zero-target measures, and `O16` single-count metadata; tampered or incomplete script sets fail `validate_task_scripts()`.
* **AC3 (`SA-010` & aggregate-only measures)**: `evaluate_role_measures()` raises `ValueError` when staff agreement is `False`, missing `staff_representatives`, missing non-surveillance statement wording, or dated after `measurement_date`; raises `ValueError` when any `IDENTITY_FIELDS` or per-participant keys appear; suppresses cells with `0 < n < 5`; computes coarse percentages alongside raw counts for `5 <= n <= 8`; and evaluates `SA-009` (`>=80%` `<5m`, `SUS >= 70`) strictly as hypotheses (`thresholds_are_hypotheses=True`, `human_usability_signoff=False`).
* **AC4 (Findings & backlog links)**: `log_finding()` / `validate_findings_log()` accept valid `UF-###` findings with severity `1..4` and `#NNN` or GitHub issue URLs; reject missing/invalid issue refs, out-of-range severities, duplicate IDs, leaked identity fields/emails, `accepted_risk` without `risk_owner`, and `retested` backed only by `synthetic_walkthrough`.
* **AC5 (Negative/inconclusive outcomes & synthetic walkthrough label)**: `evaluate_programme_results()` preserves `supported`, `not_supported`, `inconclusive`, and `not_run` outcomes, rejects blank summaries on `not_supported`/`inconclusive` records, rejects synthetic records claiming `not_user_validation=False`, and `build_synthetic_walkthrough_report()` emits `not_user_validation=True`, `validation_label="Synthetic walkthrough - not user validation"`, `user_validation_established=False`, and `human_usability_signoff=False` while exercising supported, negative (`not_supported`), and `inconclusive` constructed bundle/contract cases.
* **Doc-to-contract sync**: Reads `docs/reference/research/ux/usability-test-programme-plan.md` and verifies it contains the 5-8 participant band, all 5 bundle IDs, all 5 `profile_journey_contract` elements, `SA-010`, `"Synthetic walkthrough - not user validation"`, `not_user_validation`, and keeps human results `Not run`.

#### Boundaries

* Included: `src/core/tests/test_usability_programme.py`.
* Excluded: Browser/Playwright or SQL tests.

#### Likely Targets

* src/core/tests/test_usability_programme.py: Create unit test suite.

#### Dependencies

* P01-T01, P02-T01.

#### Validation Expectations

* `ruff check`, `ruff format --check`, `mypy`, and `unittest` pass on `tests/test_usability_programme.py`.

#### Completion Evidence

* All tests in `test_usability_programme.py` run and pass in < 2s.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Execute focused-tier tests, `ruff`, and `mypy` in isolated worktree `.venv`

#### Context

Using the gitignored worktree-local `.venv` created in `P01-T01` isolates all `unittest`, `ruff`, and `mypy` runs cleanly in this worktree without mutating `/home/azureuser/.local`.

#### Intent

Run and record:
1. `cd src/core && ../../.venv/bin/python -m unittest discover -s tests -v`
2. `cd src/core && ruff check . && ruff format --check . && ../../.venv/bin/python -m mypy`
3. `cd src/api && PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest tests/test_epic149_ux_journey_requirement_traceability.py tests/test_epic149_ux_evidence_results.py tests/test_ux_design_traceability.py tests/test_production_ux_acceptance_protocol.py -v`

#### Boundaries

* Included: `src/core` tests/lint/types, `src/api` UX traceability tests.
* Excluded: `tools/rpi-checks.py --all` (explicitly excluded by user prompt).

#### Likely Targets

* None tracked in Git (`/.venv/` is gitignored; verify with `git status --short`).

#### Dependencies

* P01, P02, P03-T01.

#### Validation Expectations

* Every command above exits `0` and `git status --short` shows zero `.venv` or cache artifacts untracked.

#### Completion Evidence

* Command outputs captured in `.copilot-tracking/changes/2026-11-15/ux-155-usability-programme-changes.md`.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T03 -->
### P03-T03: Configure privacy-safe Git author email and verify staged local commit readiness (`Refs #155`, no push/PR)

#### Context

Objective 3 and repository Git instructions require resolving `{id}+{login}@users.noreply.github.com` via `gh api user` into repository-local `git config --local user.email`, committing all `src/core/`, `docs/`, and `.copilot-tracking/` artifacts cleanly on `feat/ux-155-usability-programme` with `Refs #155` (never a closing keyword, even negated, because human session/agreement criteria remain open) and the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer, and NOT pushing or opening a PR (`PC-005`). Because `rpi-review` writes `.copilot-tracking/reviews/logs/2026-11-15/ux-155-usability-programme-review.md` and updates the session state immediately after `rpi-implement`, `P03-T03` sets local Git config and verifies clean worktree staging so the single final commit after `rpi-review` leaves `git status --short` completely clean without amending commits.

#### Intent

Configure repository-local `user.email` (and `user.name` if unset) from `gh api user`, verify `git branch --show-current == "feat/ux-155-usability-programme"`, verify `.venv` and cache folders are gitignored, and record commit readiness for post-`rpi-review` finalization.

#### Boundaries

* Included: `gh api user` inspection, `git config --local user.email`, `git status --short` / `git diff --stat` verification, and final single-commit handoff (`Refs #155` + Copilot trailer, zero `.copilot-tracking/` paths in the commit message body).
* Excluded: `git push`, `gh pr create`, global Git config edits, or closing keywords (`Closes`/`Fixes`/`Resolves`).

#### Likely Targets

* Local `.git` worktree config (`user.email`) and staged branch state on `feat/ux-155-usability-programme`.

#### Dependencies

* P03-T02.

#### Validation Expectations

* `git config --local user.email` matches `{id}+{login}@users.noreply.github.com` from `gh api user`; `git status --short` shows only intended `src/core/`, `docs/`, and `.copilot-tracking/` files.

#### Completion Evidence

* Recorded in `.copilot-tracking/changes/2026-11-15/ux-155-usability-programme-changes.md`, followed by final clean commit verification after `rpi-review`.

#### Unresolved Items

* None.
