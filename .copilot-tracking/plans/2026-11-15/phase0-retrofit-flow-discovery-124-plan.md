<!-- markdownlint-disable-file -->
# RPI Plan: Phase 0 Retrofit-Flow Discovery Contract (Issue #124)

## Task Metadata

* Task ID: issue-124
* Task slug: phase0-retrofit-flow-discovery-124
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-plan-critique.md

## Executive Summary

This plan delivers the deterministic Phase 0 retrofit-flow discovery contract and governance guard in `src/core` (`zava_forward.core.discovery_contract`, integrated additively with `discovery_register` and `discovery_flow`) together with its cited knowledge-base synthesis in `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`. It closes the contract gaps between the initial PR #895/#1030 slices and the full Phase 0 requirements in `docs/brds/retrofit-flow-discovery-brief.md` and `docs/brds/agentic-retrofit-programme-brd.md` (`BG-011`, `RULE-019`, `OD-18`):

1. Nominated human discovery owner and `accepted handover` endpoint agreement validation, rejecting blank, placeholder, self-nominated, or AI/automated actors on both helper calls and direct dataclass construction.
2. Full PAS 2035 and retrofit-flow lifecycle dictionary covering all 10 end-to-end stages through `accepted handover` (plus `paused`, `excluded`, `withdrawn`, `cancelled`, and `reopened_aftercare` exception/terminal states), 15 distinct lifecycle events (preserving both the `BG-011` `assessment-to-ready-to-install` primary cycle-time leg and the `accepted handover` outcome endpoint with its prerequisite event checks), 8 required timestamp specifications (including explicit active-work start/finish timestamps so `active_days` is never imputed), 7 governed wait states, and 4 return-loop kinds (`return`, `rejection`, `repeat visit`, `reopen`), each gated by domain-owner role validation.
3. Ranked constraint register (`1..N`) requiring and recording non-empty, source-referenced `supporting_evidence` and `contradicting_evidence` tuples alongside an all-`True` 5-part constraint test before hypothesis acceptance, blocking proposer self-approval and keeping refuted/`DISPUTED` hypotheses visibly preserved inside validated registers and packs as non-findings.
4. Fail-closed governance guard stamping and verifying `owner_validated=False` and `finding_status="candidate_hypothesis_not_company_finding"` across all discovery outputs (`discovery_contract`, `discovery_register`, and `discovery_flow`) until a sponsor-nominated human discovery owner (with `ENDPOINT_AGREED` on `accepted handover` and a zero-gap validated dictionary) records formal validation.

### User Decisions and Requirements Highlights

* Confirmed automatic RPI loop execution (`rpi-research` -> `rpi-plan` with independent critique -> `rpi-implement` -> `rpi-review`) writing 2026-11-15 artifacts under `.copilot-tracking/` on branch `feat/gov-124-phase0-discovery` (stacked on `feat/demo-164-chat-grounding-provenance-0900`, PR #1641).
* Focused validation tier required: run `src/core` unit tests, `ruff check`, `ruff format --check`, and `mypy`; do not run `tools/rpi-checks.py --all`.
* Exact governance contract required: constraint hypotheses must require and record both `supporting_evidence` and `contradicting_evidence`, and all discovery outputs must carry `owner_validated=False` and `finding_status="candidate_hypothesis_not_company_finding"` until a nominated discovery owner records formal validation.
* Local commit closeout required: commit code, documentation, and `.copilot-tracking/` artifacts cleanly on `feat/gov-124-phase0-discovery` with the Copilot trailer; do not push or open a PR.

### What You May Not Know

* `discovery_register.py` and `discovery_flow.py` already exist from PRs #895 and #1030 with 20 unit tests (`test_discovery_register.py`, `test_discovery_flow.py`), including a specific test for legacy `no_contradiction_note`. Enriching those two modules additively while placing the full strict Phase 0 contract in `discovery_contract.py` preserves 100% of existing regression tests while ensuring every discovery output carries `owner_validated` and `finding_status`.
* `test_discovery_assistant_demo.py` invokes `sys.executable -m zava_forward.core discovery-demo` from a scrubbed temporary directory without `PYTHONPATH`, so focused validation must execute inside an isolated `~/.cache` Python 3.12 virtualenv (avoiding `/tmp` restrictions and supporting offline `--no-build-isolation` editable install of `src/core`) and remove temporary `*.egg-info` metadata before staging Git commits.
* To preserve clean Git history without `git commit --amend`, implementation commits code, tests, docs, and RPI artifacts through `rpi-implement` in one Conventional Commit, and `rpi-review` commits the post-implementation review log and final state JSON in a second additive Conventional Commit, both carrying the Copilot trailer.
* The repository holds only the BSI PAS 2035:2023 overview (`pas-2035-2023-bsi-overview.md`), not the licensed standard (`gap-pas-2035-licensed`), and Zava North Homes is a fictional case customer; both code defaults and documentation keep live Zava North Homes findings unvalidated (`owner_validated=False`, `finding_status="candidate_hypothesis_not_company_finding"`).

### Unresolved Decisions or Blockers

* None blocking implementation. Real-world Zava North Homes sponsor nomination, domain-owner sign-off, and 12-month extract commissioning remain open human governance gates (`OD-14`, `OD-16`, `OD-18`, `OD-36`) and are explicitly preserved as unvalidated in default seed state and documentation.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`rpi-research`, `rpi-plan` including independent plan critique, `rpi-implement`, and `rpi-review`) with dated artifacts under `.copilot-tracking/*/2026-11-15/` for Issue #124 (`Caller prompt`).
* Work in `/home/azureuser/source/ama-demo-wt/feat-124-phase0-discovery` on branch `feat/gov-124-phase0-discovery` stacked onto `feat/demo-164-chat-grounding-provenance-0900` (`Caller prompt`).
* Implement and validate the Phase 0 retrofit-flow discovery contract in `src/core` and document it in `docs/reference/research/` (`Caller prompt`; `docs/brds/retrofit-flow-discovery-brief.md`; `docs/brds/agentic-retrofit-programme-brd.md` `BG-011`).
* Deliver a validated lifecycle and event dictionary covering all PAS 2035 / retrofit flow stages, timestamps, wait states, and return loops through `accepted handover` (`Caller prompt`; Issue #124 AC1, AC2).
* Deliver a ranked constraint register that requires and records both `supporting_evidence` and `contradicting_evidence` for each constraint hypothesis (`Caller prompt`; Issue #124 AC3).
* Deliver an explicit governance guard enforcing that all discovery outputs carry `owner_validated=False` and `finding_status="candidate_hypothesis_not_company_finding"` until a nominated discovery owner records formal validation (`Caller prompt`; Issue #124 AC1, AC4).
* Add deterministic unit tests in `src/core/tests/`, run focused validation (`unittest`, `ruff check`, `ruff format --check`, `mypy`; do not run `tools/rpi-checks.py --all`), and commit all changes plus `.copilot-tracking/` artifacts cleanly on `feat/gov-124-phase0-discovery` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, without pushing or opening a PR (`Caller prompt`).

## Goals

* Deliver a pure, offline, strictly typed Phase 0 retrofit-flow discovery contract in `src/core` covering discovery owner nomination, `accepted handover` endpoint agreement, the complete PAS 2035 / retrofit lifecycle dictionary (stages, events, timestamps, wait states, return loops), deterministic flow/leg/wait/loop evaluation, the ranked two-sided-evidence constraint register, and a fail-closed output governance guard.
* Preserve backward compatibility across existing `discovery_register.py`, `discovery_flow.py`, and `discovery_assistant_*.py` modules while upgrading `discovery_register` and `discovery_flow` outputs with `owner_validated` and `finding_status` metadata.
* Document the Phase 0 contract, role boundaries, PAS 2035 overview provenance limits, and open Zava North Homes human validation gates in `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, keeping `docs/reference/README.md`, `docs/reference/log.md`, `docs/brds/retrofit-flow-discovery-brief.md`, and `src/core/README.md` synchronized.

## Scope and Non-Goals

### In Scope

* New module `src/core/src/zava_forward/core/discovery_contract.py`.
* Additive, backward-compatible governance field/property enrichments in `src/core/src/zava_forward/core/discovery_register.py` and `src/core/src/zava_forward/core/discovery_flow.py`.
* New deterministic unit test suite `src/core/tests/test_discovery_contract.py` and targeted additive assertions in `src/core/tests/test_discovery_register.py` and `src/core/tests/test_discovery_flow.py`.
* New knowledge-base synthesis `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md` and updates to `docs/reference/README.md`, `docs/reference/log.md`, `docs/brds/retrofit-flow-discovery-brief.md`, and `src/core/README.md`.
* Focused local validation (`src/core` unit tests, `ruff`, `mypy`, Markdown link resolution, and legacy-reference checks) and local Git commit on `feat/gov-124-phase0-discovery`.

### Non-Goals

* Fabricating real Zava North Homes sponsor nominations, real operational-owner validations, or real 12-month company extracts.
* SQL/JSON persistence, API endpoints, web workbench UI screens, or CSV extract importers for Phase 0 discovery records.
* Running `tools/rpi-checks.py --all`, pushing to `origin`, opening/updating a GitHub pull request, or ticking/closing Issue #124 on GitHub before human company gates exist.

## Functional Requirements

* FR-1 (Discovery Owner Nomination and Endpoint Agreement): `discovery_contract` shall model and validate sponsor nomination of a named human discovery owner (distinct from the sponsor, non-placeholder, non-AI/automated) and explicit agreement on the canonical `"accepted handover"` endpoint by a named human authority, enforcing those actor checks inside `NominatedDiscoveryOwner.status()` itself as well as helper constructors, and reporting `"NOT_NOMINATED"`, `"ENDPOINT_NOT_AGREED"`, or `"ENDPOINT_AGREED"`.
  * Observable acceptance criteria: Unnominated, placeholder, automated, self-nominated, or `"practical completion"` endpoint records (whether created via helpers or direct `NominatedDiscoveryOwner(...)` construction) report non-agreed status and block downstream owner validation; valid sponsor nomination + `"accepted handover"` agreement reports `"ENDPOINT_AGREED"`.
* FR-2 (PAS 2035 / Retrofit Lifecycle, Event, Timestamp, Wait-State, and Return-Loop Dictionary): `discovery_contract` shall define the canonical Phase 0 lifecycle dictionary covering all 10 ordered PAS 2035 / retrofit flow stages through `accepted handover` (plus `paused`, `excluded`, `withdrawn`, `cancelled`, and `reopened_aftercare` exception/terminal states), 15 distinct lifecycle events (keeping candidate selection, retrofit assessment completed, design approved, resident works decision recorded, ready to install, work release, appointment, installation, practical completion, invoice, documentary completion, physical acceptance, evidence acceptance, resident handover, and accepted handover separate), 8 timestamp specifications (including `active_work_started_at` and `active_work_completed_at`), 7 wait states, and 4 return-loop kinds (`return`, `rejection`, `repeat visit`, `reopen`), enforcing role-matched human validation per entry and reporting plain-language dictionary gaps.
  * Observable acceptance criteria: `build_default_lifecycle_dictionary()` starts unvalidated with explicit gaps for every unvalidated entry; wrong-role, blank, placeholder, or AI validation raises `ValueError`; validating every stage, event, timestamp spec, wait state, and return loop by its owning role produces zero dictionary gaps.
* FR-3 (Deterministic Property-Flow, Leg, Wait, and Return-Loop Evaluation): `discovery_contract` shall evaluate baseline candidate property records and timestamped property stage/event/wait/loop records against the dictionary, retaining baseline candidates even when they have zero downstream events, returning `active_days=None` rather than imputing `calendar_days - wait_days` when explicit active-work start/finish timestamps are absent, enforcing `BG-011` `accepted handover` prerequisites (`design approved`, `resident works decision recorded`, `physical acceptance`, `evidence acceptance`, `resident handover`, and no unresolved post-handover `reopen`, while keeping intended energy outcome tracked separately), computing `BG-011` `assessment_to_ready_to_install_days`, `candidate_to_accepted_handover_days`, and post-installation handover legs alongside wait days by party (preserving `UNKNOWN`, `DISPUTED`, and `Unattributed` causes visibly) and return-loop counts/durations, and recording missing, malformed, timezone-naive datetime, unknown-code, or out-of-order timestamps as explicit `gaps` without imputation.
  * Observable acceptance criteria: Deterministic synthetic cases yield exact expected durations, `active_days=None` when active timestamps are absent, zero-event candidate retention, `accepted handover` prerequisite gap flags, loop counts, and gap lists across repeated runs without guessing.
* FR-4 (Ranked Constraint Register with Two-Sided Evidence): `discovery_contract` shall maintain a strictly ranked (`1..N` contiguous) constraint hypothesis register seeded with the 5 Phase 0 hypotheses (`CAP`, `HANDOFF`, `RESIDENT`, `DEPEND`, `QUALITY`), requiring both non-empty `supporting_evidence` and non-empty `contradicting_evidence` tuples (each `EvidenceRecord` carrying non-blank `statement`, `source_ref`, `direction`, and human `recorded_by`) on every adjudicated hypothesis and requiring all 5 `ConstraintTestAssessment` booleans to be `True` before domain-owner or discovery-owner acceptance (`validate_constraint_by_domain_owner` / `validate_constraint_by_discovery_owner`), rejecting proposer self-validation and keeping `DISPUTED` hypotheses visibly preserved inside registers and packs.
  * Observable acceptance criteria: Attempting to accept/validate any hypothesis with empty `supporting_evidence`, empty `contradicting_evidence`, any `False` `ConstraintTestAssessment` criterion, duplicate/non-contiguous ranks, wrong domain role, or proposer self-approval raises `ValueError`; disputing a hypothesis records `review_status="DISPUTED"` and retains non-finding status even when the enclosing register/pack is validated.
* FR-5 (Fail-Closed Discovery Output Governance Guard): `discovery_contract` (and additive fields in `discovery_register` and `discovery_flow`) shall enforce that every discovery output carries `owner_validated=False` and `finding_status="candidate_hypothesis_not_company_finding"` until a `NominatedDiscoveryOwner` in `"ENDPOINT_AGREED"` status and a zero-gap validated `LifecycleDictionary` are present and the exact nominated human discovery owner records formal sign-off (`validate_owner_finding` in `discovery_register`; `validate_lifecycle_report`, `validate_flow_report`, `validate_constraint_by_discovery_owner`, `validate_constraint_register`, and `validate_discovery_pack` in `discovery_contract`), keeping legacy domain-only `discovery_register.decide()` and `DISPUTED` child hypotheses at `owner_validated=False`; any forged or inconsistent `owner_validated=True` or promoted `finding_status` shall raise `GovernanceViolationError(ValueError)`.
  * Observable acceptance criteria: All seed/unvalidated/incomplete/domain-only/disputed discovery outputs carry `owner_validated=False` and `finding_status="candidate_hypothesis_not_company_finding"`; tampered outputs raise `GovernanceViolationError`; complete synthetic owner sign-off transitions eligible artifacts to `owner_validated=True` and `finding_status="owner_validated_company_finding"` while preserving any `DISPUTED` child hypotheses as non-findings.
* FR-6 (Knowledge-Base and Brief Documentation): Author `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md` and update `docs/reference/README.md`, `docs/reference/log.md`, `docs/brds/retrofit-flow-discovery-brief.md`, and `src/core/README.md` with traceable contract details and explicit Zava North Homes human-gate caveats.
  * Observable acceptance criteria: All relative Markdown links resolve (`test_live_doc_links.py`), legacy path checks pass (`tools/check-legacy-references.py`), and Markdown formatting conforms to repository rules.

## Non-Functional Requirements

* NFR-1 (Determinism and Offline Purity): All `src/core` discovery contract operations shall be pure, deterministic, in-memory stdlib Python 3.12 functions with zero network, database, filesystem, environment, wall-clock, or AI-model calls, and imports restricted to `zava_forward.core`.
  * Objective threshold or evaluation condition: Zero external/sibling-package imports (`test_dependency_rule.py`) and identical SHA-256 JSON digests across repeated runs.
  * Operating condition or verification approach, if needed: Unit tests in `src/core/tests/` including `test_dependency_rule.py` and repeatability check.
  * Observable acceptance criteria: `test_dependency_rule.py` and `test_discovery_contract.py` pass with zero external side effects.
* NFR-2 (Strict Static Typing and Lint Formatting): All modified and new Python modules and tests in `src/core` shall pass strict `mypy` and `ruff` without adding `pyproject.toml` ignore overrides.
  * Objective threshold or evaluation condition: Zero `mypy` errors (`strict = true`), zero `ruff check` findings (`E, F, I, B, UP`), and zero `ruff format --check` diffs (`line-length = 100`).
  * Operating condition or verification approach, if needed: Run `ruff check .`, `ruff format --check .`, and `mypy` from `src/core` in an isolated `~/.cache` Python 3.12 virtualenv with `src/core` installed editable (`--no-build-isolation`), cleaning temporary `*.egg-info` artifacts afterward.
  * Observable acceptance criteria: All three commands exit 0 with zero new `pyproject.toml` exclusions.

## Acceptance Criteria

* AC-1: `NominatedDiscoveryOwner` enforces human sponsor nomination (distinct from nominee, non-placeholder, non-AI) and explicit agreement on `"accepted handover"` endpoint across helpers and `status()` (`FR-1`).
* AC-2: `LifecycleDictionary` covers all 10 PAS 2035 / retrofit stages (plus `paused`, `excluded`, `withdrawn`, `cancelled`, `reopened_aftercare`), 15 distinct lifecycle events, 8 timestamp specs (including active-work start/finish), 7 wait states, and 4 return-loop kinds through `accepted handover`, enforces owner-role validation, and evaluates property flows (`BG-011` and handover legs, `accepted handover` prerequisites, zero-event candidate retention, `active_days=None` non-imputation, waits, loops, timestamp gaps) deterministically (`FR-2`, `FR-3`, `NFR-1`).
* AC-3: `RankedConstraintRegister` enforces contiguous `1..N` ranking, requires both non-empty `supporting_evidence` and non-empty `contradicting_evidence` tuples with traceable `source_ref`, requires all 5 `ConstraintTestAssessment` booleans to be `True` for acceptance, enforces proposer separation and domain-role rights, and visibly preserves `DISPUTED` records inside validated registers/packs as non-findings (`FR-4`).
* AC-4: `enforce_governance_guard` and all discovery outputs across `discovery_contract`, `discovery_register` (decoupled from domain-only `decide()`), and `discovery_flow` (`baseline_summary`, `leg_summary`, `waits_by_party`, `loop_summary`) carry `owner_validated=False` and `finding_status="candidate_hypothesis_not_company_finding"` until formal nominated-owner validation with all prerequisites met, raising `GovernanceViolationError` on any invalid promotion (`FR-5`).
* AC-5: All unit tests in `src/core/tests/` (existing suite + new `test_discovery_contract.py`, capped at <= 30 focused test methods and 0 test removals), `ruff check .`, `ruff format --check .`, `mypy`, `test_live_doc_links.py`, `tools/check-legacy-references.py`, and `tools/rename-zava-tests.py` pass (`NFR-1`, `NFR-2`, `FR-6`).
* AC-6: Research documentation in `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, KB index/log updates, `src/core/README.md`, `docs/brds/retrofit-flow-discovery-brief.md`, code, tests, and `.copilot-tracking/` artifacts are committed cleanly in non-amended additive commits on `feat/gov-124-phase0-discovery` with the Copilot trailer and not pushed (`FR-6`).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-plan.md                                                            |
| Phase details                    | .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-phase-details.md                                                 |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-plan-critique.md with Revise disposition (`PC-001`–`PC-004` resolved) |
| Relevant research                | .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-research.md                                                     |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-changes.md is created by implementation as its evidence record   |
| Planning execution and readiness | Complete; Ready (`PC-001` through `PC-004` applied directly in final plan and phase details)                                             |
| Continuation context             | Confirmed automatic RPI Agent parent return; transitions immediately to `rpi-implement`                                                  |

## Sources

* `.copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-research.md`: Codebase evidence `C1`–`C16`, gap analysis, backward-compatibility proof, and convergent contract design.
* `docs/brds/retrofit-flow-discovery-brief.md`: Canonical Phase 0 proposition, outcomes, population/time attribution rules, 5-part constraint test, 12 evidence domains, 5 candidate constraints, and Issue #124 delivery status (`C1`).
* `docs/brds/agentic-retrofit-programme-brd.md`: `BG-011` (`OBJ-11`), `RULE-019`, `OD-16`, and `OD-18` cycle-time vs `accepted handover` endpoint and frozen-dictionary requirements (`C2`).
* `src/core/src/zava_forward/core/discovery_register.py` and `src/core/src/zava_forward/core/discovery_flow.py`: Existing Phase 0 slices to preserve and enrich additively (`C3`, `C4`, `C7`, `C8`).
* `docs/reference/research/retrofit-synthetic-data/data-dictionary.md` and `docs/reference/regulatory/retrofit-standards-and-funding/pas-2035-2023-bsi-overview.md`: Lifecycle stages/events and PAS 2035 BSI overview provenance boundary (`C9`, `C11`).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Phase 0 Retrofit-Flow Discovery Contract and Governance Guard in `src/core`

* Intent: Deliver the unified Phase 0 discovery contract in `discovery_contract.py` and additive governance metadata in `discovery_register.py` and `discovery_flow.py`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add Additive Governance Fields and Nominated-Owner Guard to `discovery_register.py` and `discovery_flow.py`

* Requirement and evidence: `FR-5`, `NFR-1`, `NFR-2`; research `C3`, `C4`, `C7`, `C8`; critique `PC-001`.
* Expected result: `discovery_register` exports `CANDIDATE_FINDING_STATUS`, `VALIDATED_FINDING_STATUS`, and `GovernanceViolationError`, keeps legacy `is_company_finding` intact for domain-only `decide()`, gates `owner_validated=True` / `finding_status="owner_validated_company_finding"` on `validate_owner_finding()` (`ENDPOINT_AGREED`, zero `dictionary_gaps`, non-empty `supporting_evidence` and `contradicting_evidence`, human actor checks, `__post_init__` fail-closed check), and `discovery_flow` stamps `owner_validated=False` and `finding_status="candidate_hypothesis_not_company_finding"` across `baseline_summary()`, `leg_summary()`, `waits_by_party()`, and `loop_summary()`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Implement Unified Phase 0 Discovery Contract and Fail-Closed Governance Guard in `discovery_contract.py`

* Requirement and evidence: `FR-1`, `FR-2`, `FR-3`, `FR-4`, `FR-5`, `NFR-1`, `NFR-2`; research `C1`–`C5`, `C9`–`C13`, `C15`; critique `PC-002`, `PC-003`.
* Expected result: `src/core/src/zava_forward/core/discovery_contract.py` implements `NominatedDiscoveryOwner` (enforcing human/separation rules in `status()`), full PAS 2035 `LifecycleDictionary` (10 stages + 5 exception/terminal states, 15 events, 8 timestamp specs including active-work start/finish, 7 wait states, 4 return loops) + `evaluate_property_flow()` (zero-event candidate retention, `active_days=None` non-imputation, `BG-011` `accepted handover` prerequisite checks), `RankedConstraintRegister` requiring non-empty `supporting_evidence` and `contradicting_evidence` and all-`True` 5-part `ConstraintTestAssessment` on acceptance while preserving `DISPUTED` hypotheses inside validated registers/packs as non-findings, and fail-closed `enforce_governance_guard()` / `validate_lifecycle_report()` / `validate_flow_report()` / `validate_constraint_by_domain_owner()` / `validate_constraint_by_discovery_owner()` / `validate_constraint_register()` / `validate_discovery_pack()`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Deterministic Unit Tests in `src/core/tests/`

* Intent: Prove semantic and regression conformance across happy paths, gap reporting, two-sided evidence rules, and fail-closed governance tampering.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add Focused Unit Tests in `test_discovery_contract.py` and Additive Assertions in `test_discovery_register.py` and `test_discovery_flow.py`

* Requirement and evidence: `AC-1`–`AC-5`, `NFR-1`, `NFR-2`; research `C7`, `C8`, `C12`, `C14`, `C15`.
* Expected result: `src/core/tests/test_discovery_contract.py` (15–25 focused deterministic test methods, 0 existing test removals) plus additive checks in `test_discovery_register.py` and `test_discovery_flow.py` verify owner/endpoint nomination, PAS 2035 stage/event/timestamp/wait/loop validation and flow arithmetic, two-sided constraint register gates, and fail-closed governance guard rejections.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Knowledge-Base Research Documentation, Focused Validation, and Local Branch Commit

* Intent: Document the Phase 0 contract in the knowledge base and component guides, pass all focused checks in an isolated Python 3.12 environment, and commit cleanly on `feat/gov-124-phase0-discovery`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Author `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md` and Synchronize Indexes and Guides

* Requirement and evidence: `FR-6`, `AC-6`; research `C1`, `C2`, `C11`, `C15`, `C16`.
* Expected result: `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md` documents the contract, PAS 2035 BSI-overview scope, two-sided constraint register, governance guard, and open Zava North Homes human gates; `docs/reference/README.md`, `docs/reference/log.md`, `docs/brds/retrofit-flow-discovery-brief.md`, and `src/core/README.md` are updated consistently with zero broken links or legacy path violations.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Run Focused Validation Suite and Commit Implementation + RPI Artifacts Locally

* Requirement and evidence: `AC-5`, `AC-6`, `NFR-2`; research `C12`, `C14`, `C15`, `C16`; critique `PC-004`.
* Expected result: Focused `src/core` unit tests (`test_discovery*.py`, `test_live_doc_links.py`, `test_dependency_rule.py`), `ruff check .`, `ruff format --check .`, `mypy`, `compileall`, and `tools/rename-zava-tests.py` exit 0 using an isolated `~/.cache` Python 3.12 virtualenv (`zava_forward_core.pth` editable binding without `wheel`/PyPI fetches), while `tools/check-legacy-references.py` confirms 0 link violations and 0 touched-file reference violations (recording pre-existing base-branch/host exclusions explicitly); code, tests, docs, and RPI artifacts through `rpi-implement` are committed cleanly in one Conventional Commit with privacy-safe GitHub noreply email and the Copilot trailer, leaving `rpi-review` to record its review log and final state in a second non-amended Conventional Commit.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-phase-details.md

## Dependencies

* Python 3.12 toolchain (`unittest`, `ruff`, `mypy`) in an isolated `~/.cache` virtualenv with `src/core` installed editable (`--no-build-isolation`) so `test_discovery_assistant_demo.py` subprocess checks resolve `zava_forward.core` from the current worktree without `/tmp` dependencies or outbound PyPI fetches.
* Existing modules `zava_forward.core.discovery_register` and `zava_forward.core.discovery_flow`, whose public APIs must remain backward-compatible.
* Authenticated `gh api user` check to set repository-local privacy-safe `user.email` (`{id}+{login}@users.noreply.github.com`) before committing.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 `PC-001` [High]: `discovery_register.Constraint` promoted on domain-only `decide()` without nominated owner or `contradicting_evidence`; missing `leg_summary()` in `discovery_flow` | resolved | Decoupled legacy `is_company_finding` from `owner_validated` / `finding_status` in `P01-T01`, gating `owner_validated=True` on `validate_owner_finding()` (`ENDPOINT_AGREED`, zero `dictionary_gaps`, both `supporting_evidence` and `contradicting_evidence`, human actor checks, `__post_init__` `GovernanceViolationError`) and adding stamped `leg_summary()` in `discovery_flow.py`. |
| Run 1 `PC-002` [High]: Pack/register rule blocked legitimate `DISPUTED` hypotheses, 5-part constraint test booleans unchecked on acceptance, `NominatedDiscoveryOwner.status()` skipped direct-init actor checks, and helper names diverged | resolved | Aligned helper names across plan and phase details, enforced human/separation rules directly inside `NominatedDiscoveryOwner.status()`, required all 5 `ConstraintTestAssessment` booleans `True` for hypothesis acceptance, and allowed validated registers/packs to contain adjudicated `DISPUTED` hypotheses while keeping those child hypotheses at `owner_validated=False` / `finding_status="candidate_hypothesis_not_company_finding"`. |
| Run 1 `PC-003` [Medium]: Omitted active-work start/finish timestamp specs (`active_days=None`), `paused`/`cancelled` states, zero-event baseline candidate retention, and `BG-011` `accepted handover` prerequisite checks | resolved | Added `active_work_started_at` and `active_work_completed_at` (8 timestamp specs, `active_days=None` when absent), added `paused` and `cancelled` exception/terminal states, retained zero-event baseline candidates in `evaluate_property_flow()`, and added `BG-011` `accepted handover` prerequisite gap checks while keeping energy outcome separate. |
| Run 1 `PC-004` [Medium]: Hardcoded `/tmp` venv path and self-referential SHA / post-review amend conflict | resolved | Replaced `/tmp` with a `~/.cache` Python 3.12 venv using `--no-build-isolation` + `*.egg-info` cleanup, removed self-referential commit SHA insertion in `changes.md`, and specified two non-amended additive Conventional Commits (`rpi-implement` commit + `rpi-review` commit). |
| Residual risk: Live Zava North Homes human governance steps (`OD-14`, `OD-16`, `OD-18`, `OD-36`) and licensed PAS 2035 text (`gap-pas-2035-licensed`) | accepted_with_risk | Software defaults keep all Zava North Homes seed artifacts at `owner_validated=False` / `finding_status="candidate_hypothesis_not_company_finding"`, and KB documentation explicitly discloses the BSI PAS 2035 overview scope and open human gates. |

## Follow-Up Items

* Optional CSV extract adapter mapping `support/synthetic-data/retrofit-flow/zava-forward-year-one/` tables into `discovery_contract` dataclasses: outside Issue #124 contract scope per `docs/brds/retrofit-flow-discovery-brief.md` ("Persistence, a screen and extract import are not built and should wait for the nominated owner and approved data"); owned by future sponsor/owner direction.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-changes.md
* Ready phase or task: P01 (`P01-T01`, `P01-T02`), P02 (`P02-T01`), P03 (`P03-T01`, `P03-T02`)
* Remaining provisional question or blocker: none
