<!-- markdownlint-disable-file -->
# RPI Phase Details: Phase 0 Retrofit-Flow Discovery Contract (Issue #124)

## Metadata

* Task ID: issue-124
* Task slug: phase0-retrofit-flow-discovery-124
* Related plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-research.md, docs/brds/retrofit-flow-discovery-brief.md, docs/brds/agentic-retrofit-programme-brd.md

## Phase Index

| Phase ID | Name                                                                        | Status | Detail sections        |
|----------|-----------------------------------------------------------------------------|--------|------------------------|
| P01      | Phase 0 Retrofit-Flow Discovery Contract and Governance Guard in `src/core` | ready  | P01, P01-T01, P01-T02  |
| P02      | Deterministic Unit Tests in `src/core/tests/`                               | ready  | P02, P02-T01           |
| P03      | Knowledge-Base Research Documentation, Focused Validation, and Local Commit | ready  | P03, P03-T01, P03-T02  |

<!-- rpi:phase id=P01 -->
## P01: Phase 0 Retrofit-Flow Discovery Contract and Governance Guard in `src/core`

### Context

`discovery_register.py` and `discovery_flow.py` currently implement the minimal PR #895 / #1030 rules (`DiscoveryOwner`, 10-string `REQUIRED_EVENTS`, `Constraint` with single mixed `evidence` tuple + `no_contradiction_note`, and basic population/leg/wait/loop helpers) without PAS 2035 stage/timestamp/wait/loop dictionary schemas, explicit `supporting_evidence` + `contradicting_evidence` tuples on ranked hypotheses, or an output-level fail-closed governance guard stamping `owner_validated=False` and `finding_status="candidate_hypothesis_not_company_finding"` (`C1`–`C4`, `C7`, `C8`).

### Intent

Deliver a unified, strictly typed, pure-stdlib Phase 0 retrofit-flow discovery contract in `discovery_contract.py` and additively align `discovery_register.py` and `discovery_flow.py` so every discovery output across `src/core` carries `owner_validated` and `finding_status` without breaking any existing test.

### Boundaries

* Included: `src/core/src/zava_forward/core/discovery_register.py`, `src/core/src/zava_forward/core/discovery_flow.py`, and `src/core/src/zava_forward/core/discovery_contract.py`.
* Excluded: SQL/JSON persistence, FastAPI endpoints, web UI assets, CSV ingestion scripts, and `pyproject.toml` lint/type exemptions.

### Likely Targets

* `src/core/src/zava_forward/core/discovery_register.py`: Add `CANDIDATE_FINDING_STATUS`, `VALIDATED_FINDING_STATUS`, and `GovernanceViolationError`; preserve legacy `is_company_finding` on `decide()`; add `owner_validated`, `owner_validated_by`, `supporting_evidence`, `contradicting_evidence`, and `finding_status` on `Constraint` + `validate_owner_finding()` + corresponding additive keys in `register_rows()`.
* `src/core/src/zava_forward/core/discovery_flow.py`: Stamp `owner_validated: False` and `finding_status: CANDIDATE_FINDING_STATUS` on `baseline_summary()`, `waits_by_party()`, new `leg_summary()`, and new `loop_summary()`.
* `src/core/src/zava_forward/core/discovery_contract.py`: New module implementing the complete Phase 0 contract and fail-closed governance guard.

### Dependencies

* None (pure Python 3.12 standard library + `zava_forward.core.discovery_register` / `discovery_flow`).

### Validation Expectations

* `ruff check`, `ruff format --check`, and `mypy` (`strict = true`) pass with zero warnings or ignore overrides; `test_dependency_rule.py` passes.

### Completion Evidence

* Clean module imports and passing unit/type/lint checks in `src/core`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add Additive Governance Fields and Nominated-Owner Guard to `discovery_register.py` and `discovery_flow.py`

#### Context

`test_discovery_register.py` and `test_discovery_flow.py` assert existing behavior via named dict keys (`rank`, `status`, `notice`, `candidates`, `party`, `days`, etc.) and `Constraint.is_company_finding` (`C7`, `C8`). Per critique `PC-001`, domain-only `decide()` does not verify a nominated `DiscoveryOwner` (`ENDPOINT_AGREED`), a validated dictionary, human non-placeholder actors, or a `contradicting_evidence` item; therefore `owner_validated` and `finding_status` must remain `False` / `"candidate_hypothesis_not_company_finding"` after `decide()` until explicit nominated-owner validation via `validate_owner_finding()`.

#### Intent

Ensure outputs from `discovery_register` and `discovery_flow` expose `owner_validated` (`bool`) and `finding_status` (`"candidate_hypothesis_not_company_finding"` until explicit nominated-owner validation, `"owner_validated_company_finding"` only after `validate_owner_finding()` checks all prerequisites) and `supporting_evidence` / `contradicting_evidence` tuples, while preserving legacy `is_company_finding` for existing regression tests.

#### Boundaries

* Included: Additive constants (`CANDIDATE_FINDING_STATUS`, `VALIDATED_FINDING_STATUS`), `GovernanceViolationError(ValueError)`, `owner_validated: bool = False`, `owner_validated_by: str = ""`, `supporting_evidence`, `contradicting_evidence`, and `finding_status` on `Constraint` (with `__post_init__` raising `GovernanceViolationError` if `owner_validated=True` without `status == VALIDATED`, non-empty `supporting_evidence` and `contradicting_evidence`, and human `owner_validated_by != proposed_by`), `validate_owner_finding(constraint, discovery_owner, dictionary, *, by, note)` enforcing `discovery_owner.status() == "ENDPOINT_AGREED"`, zero `dictionary_gaps(dictionary)`, human non-placeholder/non-AI actors, and `by == discovery_owner.owner`, additive keys in `register_rows()`, and stamped `baseline_summary()`, `leg_summary()`, `waits_by_party()`, and `loop_summary()` in `discovery_flow.py`.
* Excluded: Breaking existing dataclass constructor signatures or changing legacy `is_company_finding` / `no_contradiction_note` behavior on domain-only `decide()`.

#### Likely Targets

* `src/core/src/zava_forward/core/discovery_register.py`: Define `CANDIDATE_FINDING_STATUS`, `VALIDATED_FINDING_STATUS`, `GovernanceViolationError`, human-actor check helper, `Constraint` fields/properties + `__post_init__` guard, `validate_owner_finding()`, and additive keys in `register_rows()`.
* `src/core/src/zava_forward/core/discovery_flow.py`: Import `CANDIDATE_FINDING_STATUS` from `.discovery_register`; include `"owner_validated": False` and `"finding_status": CANDIDATE_FINDING_STATUS` in `baseline_summary()` and `waits_by_party()` dicts; add `leg_summary(events)` and `loop_summary(loops)` returning governance-stamped dicts.

#### Dependencies

* None.

#### Validation Expectations

* All existing tests in `test_discovery_register.py` and `test_discovery_flow.py` pass unchanged alongside new governance-field assertions.

#### Completion Evidence

* `ruff check`, `mypy`, and unit tests pass on both modules.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Implement Unified Phase 0 Discovery Contract and Fail-Closed Governance Guard in `discovery_contract.py`

#### Context

Issue #124 Objective 2 requires a complete Phase 0 retrofit-flow discovery contract in `src/core`:
1. Nominated discovery owner and agreed `accepted handover` endpoint (`C1`, `C2`, `C13`).
2. Validated lifecycle and event dictionary covering all PAS 2035 / retrofit flow stages, timestamps, wait states, and return loops through `accepted handover` (`C1`, `C2`, `C9`, `C11`).
3. Ranked constraint register requiring and recording both `supporting_evidence` and `contradicting_evidence` for each constraint hypothesis (`C1`, `C3`).
4. Explicit governance guard enforcing `owner_validated=False` and `finding_status="candidate_hypothesis_not_company_finding"` on all discovery outputs until a nominated discovery owner records formal validation (`C1`, `C3`, `C13`).

#### Intent

Create `src/core/src/zava_forward/core/discovery_contract.py` containing frozen dataclasses, canonical seed definitions, deterministic validation/evaluation functions, and the fail-closed governance guard.

#### Boundaries

* Included:
  * Human-actor & reference validation helper rejecting blank strings, placeholders (`tbd`, `todo`, `tbc`, `pending`, `unknown`, `n/a`, `na`, `none`, `null`, `placeholder`, `unassigned`, `unappointed`, `self`, `same person`, `same operator`), and automated/AI tokens (`ai`, `agent`, `bot`, `automation`, `automated`, `automatic`, `copilot`, `llm`, `model`, `system`, `workflow`, `scheduler`, `pipeline`, `service`, `script`), patterned after `restart_authority.py` (`C13`).
  * `NominatedDiscoveryOwner` + `nominate_discovery_owner(...)` + `agree_discovery_endpoint(...)`: enforces distinct human `nominated_by` (Executive Sponsor) and `owner` (Discovery Owner), `nominated_on: date | None`, canonical `endpoint == "accepted handover"`, and human `endpoint_agreed_by` / `endpoint_agreed_role` / `endpoint_agreed_on: date | None`, checking human/non-placeholder/non-AI and `nominated_by != owner` directly inside `NominatedDiscoveryOwner.status()` (`PC-002`).
  * `LifecycleDictionary` comprising:
    * `stages: tuple[StageSpec, ...]` covering all 10 ordered PAS 2035 / retrofit flow stages (`candidate_identification`, `resident_engagement_and_survey_booking`, `pas2035_retrofit_assessment`, `safety_and_dependency_triage`, `pas2035_design_and_coordination`, `resident_works_decision`, `funding_capacity_and_work_release`, `appointment_and_installation`, `quality_and_evidence_acceptance`, `resident_and_accepted_handover`) plus explicit exception/terminal states (`paused`, `excluded`, `withdrawn`, `cancelled`, `reopened_aftercare`, `PC-003`), each with `order`, `code`, `name`, `entry_event`, `exit_event`, `pas2035_role_boundary`, `owner_role`, `validated_by`, `validated_on`.
    * `events: tuple[EventSpec, ...]` covering all 15 required distinct events (`candidate selection`, `retrofit assessment completed`, `design approved`, `resident works decision recorded`, `ready to install`, `work release`, `appointment`, `installation`, `practical completion`, `invoice`, `documentary completion`, `physical acceptance`, `evidence acceptance`, `resident handover`, `accepted handover`), keeping commercial/quality/handover milestones strictly separate and anchoring both `BG-011` (`retrofit assessment completed -> ready to install`) and Phase 0 outcome (`candidate selection -> accepted handover`).
    * `timestamps: tuple[TimestampSpec, ...]` covering 8 required specs (`stage_entered_at`, `stage_exited_at`, `active_work_started_at`, `active_work_completed_at`, `event_occurred_at`, `wait_started_at`, `wait_ended_at`, `loop_recorded_at`, `PC-003`), requiring ISO date or timezone-aware ISO datetime, `source_system`, `source_ref`, and explicit non-imputation rule (`active_days=None` when active start/finish evidence is absent).
    * `wait_states: tuple[WaitStateSpec, ...]` covering all 7 governed wait states (`awaiting_supplier_or_professional_capacity`, `awaiting_handoff_acceptance_or_approval`, `awaiting_resident_access_adjustment_or_decision`, `safety_or_hazard_hold`, `building_or_planned_maintenance_dependency`, `funding_or_payment_hold`, `quality_defect_or_evidence_remediation`), with accountable role, clock rule, and explicit preservation of `UNKNOWN` / `DISPUTED` causes and `Unattributed` parties.
    * `return_loops: tuple[ReturnLoopSpec, ...]` covering `return`, `rejection`, `repeat visit`, and `reopen`, with trigger description, target stages, non-inference rule (e.g., failed access never implies resident refusal), and owner role.
  * Role-gated validation helpers (`validate_stage_spec`, `validate_event_spec`, `validate_timestamp_spec`, `validate_wait_state_spec`, `validate_return_loop_spec`) and `lifecycle_dictionary_gaps(dictionary) -> list[str]` + `summarize_lifecycle_dictionary(dictionary) -> LifecycleDictionaryReport` + `validate_lifecycle_report(...)`.
  * Deterministic property flow evaluation (`BaselineCandidateRecord`, `PropertyStageRecord`, `PropertyEventRecord`, `PropertyWaitRecord`, `PropertyReturnLoopRecord`, `FlowDiscoveryReport`, `evaluate_property_flow(...)`, `validate_flow_report(...)`, `PC-003`): retains baseline candidates even with zero downstream events; computes `BG-011` `assessment_to_ready_to_install_days`, `candidate_to_accepted_handover_days`, and handover legs (`installation -> physical acceptance -> evidence acceptance -> resident handover -> accepted handover`); enforces `BG-011` `accepted handover` prerequisites (`design approved`, `resident works decision recorded`, `physical acceptance`, `evidence acceptance`, `resident handover`, and no unresolved post-handover `reopen`, flagging missing prerequisites in `gaps` and tracking `intended_energy_outcome_status` separately); computes stage `calendar_days`, `wait_days`, and `active_days` (`None` unless explicit `active_started_at` / `active_completed_at` exist); summarizes waits by party/state keeping `UNKNOWN`/`DISPUTED`/`Unattributed` visible; counts return loops; and emits unusable/missing/out-of-order timestamps or unknown codes into `gaps` without guessing.
  * `EvidenceRecord`, `ConstraintTestAssessment`, `ConstraintHypothesis`, `RankedConstraintRegister`, `build_seed_constraint_register()`, `record_supporting_evidence()`, `record_contradicting_evidence()`, `constraint_evidence_gaps()`, `validate_constraint_by_domain_owner()`: enforces contiguous `1..N` ranks, non-empty `supporting_evidence` AND non-empty `contradicting_evidence` with valid `statement` + `source_ref` + human `recorded_by`, requires `constraint_test.passes_all` (all 5 criteria `True`) when accepting (`PC-002`), enforces proposer separation and domain-role authority, and preserves `DISPUTED` visibly.
  * Fail-closed governance guard (`CONTRACT_VERSION = "phase0-retrofit-flow-discovery-contract-v1"`, `CANDIDATE_FINDING_STATUS`, `VALIDATED_FINDING_STATUS`, `GovernanceViolationError`, `enforce_governance_guard(...)`, `validate_lifecycle_report(...)`, `validate_flow_report(...)`, `validate_constraint_by_discovery_owner(...)`, `validate_constraint_register(...)`, `build_default_phase0_pack(...)`, `validate_discovery_pack(...)`, `Phase0DiscoveryPack`, `PC-002`):
    * Ensures every discovery report, hypothesis, register, and pack defaults to `owner_validated=False` and `finding_status="candidate_hypothesis_not_company_finding"`.
    * `__post_init__` and `enforce_governance_guard()` verify per-artifact invariants fail-closed:
      1. `LifecycleDictionaryReport` / `FlowDiscoveryReport` require `ENDPOINT_AGREED`, zero `lifecycle_dictionary_gaps`, and human nominated-discovery-owner sign-off.
      2. `ConstraintHypothesis` requires `ENDPOINT_AGREED`, zero `lifecycle_dictionary_gaps`, non-empty `supporting_evidence` and `contradicting_evidence`, `constraint_test.passes_all == True`, `review_status == "OWNER_VALIDATED"` (never `"PROPOSED"` or `"DISPUTED"`), domain-owner validation (`!= proposed_by`), and exact nominated-discovery-owner sign-off (`!= proposed_by`).
      3. `RankedConstraintRegister` and `Phase0DiscoveryPack` require `ENDPOINT_AGREED`, zero `lifecycle_dictionary_gaps`, contiguous `1..N` ranks, zero unresolved `"PROPOSED"` hypotheses, two-sided evidence on every hypothesis, nominated-owner sign-off on all accepted hypotheses, and any `"DISPUTED"` child hypotheses preserved at `owner_validated=False` / `finding_status="candidate_hypothesis_not_company_finding"`.
* Excluded: Any mutable global state, wall-clock `date.today()` defaults, I/O, or external dependencies.

#### Likely Targets

* `src/core/src/zava_forward/core/discovery_contract.py`: New module (~450–550 lines, clean, strictly typed).

#### Dependencies

* `P01-T01` (`CANDIDATE_FINDING_STATUS`, `VALIDATED_FINDING_STATUS`, `ENDPOINT` shared constants from `discovery_register`).

#### Validation Expectations

* `mypy` (`strict = true`), `ruff check`, `ruff format --check`, and `test_dependency_rule.py` pass cleanly.

#### Completion Evidence

* `discovery_contract.py` passes static checks and unit tests in `P02-T01`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Deterministic Unit Tests in `src/core/tests/`

### Context

Repository testing guidelines require focused, deterministic unit tests that fail without the new contract and cover its semantic rules, edge cases, and regression boundaries without chasing trivial constant assertions (`C12`, `C14`, `C15`).

### Intent

Add deterministic unit tests proving every Issue #124 contract invariant and fail-closed governance rule while verifying zero regressions across existing `src/core` tests.

### Boundaries

* Included: New `src/core/tests/test_discovery_contract.py` (target 16–24 test methods; maximum 30 additions; exact removals: `none`) and small additive assertions (2–4 assertions) in `src/core/tests/test_discovery_register.py` and `src/core/tests/test_discovery_flow.py`.
* Excluded: Deleting or weakening any existing test in `src/core/tests/`.

### Likely Targets

* `src/core/tests/test_discovery_contract.py`: New unit test module covering semantic contract and governance guard behavior.
* `src/core/tests/test_discovery_register.py`: Additive test verifying `supporting_evidence`, `contradicting_evidence`, `owner_validated`, and `finding_status` on `Constraint` and `register_rows()`.
* `src/core/tests/test_discovery_flow.py`: Additive test verifying `owner_validated=False` and `finding_status="candidate_hypothesis_not_company_finding"` on `baseline_summary()`, `waits_by_party()`, and `loop_summary()`.

### Dependencies

* `P01-T01`, `P01-T02`.

### Validation Expectations

* `python -m unittest discover -s tests -p 'test_discovery*.py' -v` and full `src/core` unit test suite pass with 0 failures.

### Completion Evidence

* Passing `unittest`, `ruff`, and `mypy` output recorded in `.copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add Focused Unit Tests in `test_discovery_contract.py` and Additive Assertions in `test_discovery_register.py` and `test_discovery_flow.py`

#### Context

Locked test plan for critique review:
* Test ownership: `src/core/tests/test_discovery_contract.py` (primary semantic + security/governance tests), `src/core/tests/test_discovery_register.py` and `src/core/tests/test_discovery_flow.py` (additive regression parity).
* Exact removals: `none`.
* Maximum test additions: <= 30 test methods total across the 3 files.
* Semantic-versus-regression split:
  1. Owner nomination & `accepted handover` endpoint agreement: rejects blank, placeholder (`TBD`, `pending`, `unknown`), automated (`AI agent`, `copilot`, `system`), self-nomination (`sponsor == owner`), direct-constructed invalid `NominatedDiscoveryOwner(...)`, and wrong endpoint (`practical completion`); reaches `ENDPOINT_AGREED` only on `"accepted handover"`.
  2. PAS 2035 / retrofit lifecycle dictionary: verifies all 10 stages + 5 exception/terminal states (`paused`, `excluded`, `withdrawn`, `cancelled`, `reopened_aftercare`), 15 distinct events, 8 timestamp specs (including active-work start/finish), 7 wait states, and 4 return loops start unvalidated with gaps; rejects wrong-role/placeholder/AI validators; reaches 0 gaps only when every entry is validated by its owning role.
  3. Property flow evaluation: verifies zero-event baseline candidate retention, `active_days=None` when active start/finish timestamps are absent, `BG-011` `accepted handover` prerequisite gap checks (and separate energy outcome tracking), `assessment_to_ready_to_install_days`, `candidate_to_accepted_handover_days`, post-installation handover legs, wait attribution preserving `UNKNOWN`/`DISPUTED`/`Unattributed`, return-loop counts (`return`, `rejection`, `repeat visit`, `reopen`), timezone-naive / malformed / out-of-order timestamp gap reporting without guessing, and multi-run SHA-256 repeatability.
  4. Ranked constraint register: verifies contiguous `1..N` rank validation, blocks domain or discovery-owner validation when `supporting_evidence` is empty, when `contradicting_evidence` is empty, or when any of the 5 `ConstraintTestAssessment` booleans is `False`, blocks proposer self-validation and wrong-role validation, and proves a validated register/pack can contain adjudicated `DISPUTED` hypotheses while keeping those `DISPUTED` child hypotheses at `owner_validated=False` / `finding_status="candidate_hypothesis_not_company_finding"`.
  5. Fail-closed governance guard: verifies all default/seed outputs (and domain-only `discovery_register.decide()` + `discovery_flow` summaries including `leg_summary` and `loop_summary`) carry `owner_validated=False` and `finding_status="candidate_hypothesis_not_company_finding"`, and verifies `GovernanceViolationError` is raised on every tampered/forged promotion path across `discovery_contract` and `discovery_register`.

#### Intent

Provide fast, deterministic, high-signal verification of every requirement in `FR-1` through `FR-5` and `NFR-1`/`NFR-2`.

#### Boundaries

* Included: `src/core/tests/test_discovery_contract.py`, `src/core/tests/test_discovery_register.py`, `src/core/tests/test_discovery_flow.py`.
* Excluded: Slow integration, network, SQL Server, or browser tests.

#### Likely Targets

* `src/core/tests/test_discovery_contract.py`
* `src/core/tests/test_discovery_register.py`
* `src/core/tests/test_discovery_flow.py`

#### Dependencies

* `P01-T01`, `P01-T02`.

#### Validation Expectations

* All tests pass under `unittest`, `ruff check`, `ruff format --check`, and `mypy`.

#### Completion Evidence

* Exact test count and exit codes recorded in the implementation changes artifact.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Knowledge-Base Research Documentation, Focused Validation, and Local Branch Commit

### Context

Objective 2 requires documenting the Phase 0 retrofit-flow discovery contract in `docs/reference/research/`, and repository instructions require updating `docs/reference/README.md` and appending to `docs/reference/log.md` whenever a knowledge-base file is added, keeping relative Markdown links valid (`test_live_doc_links.py`), avoiding retired paths (`tools/check-legacy-references.py`), updating directly related component/brief documentation (`src/core/README.md`, `docs/brds/retrofit-flow-discovery-brief.md`), running the focused validation tier, and committing all changes + `.copilot-tracking/` artifacts cleanly on `feat/gov-124-phase0-discovery` without pushing (`C1`, `C11`–`C16`).

### Intent

Complete all documentation, execute focused validation cleanly, and ensure the final commit on `feat/gov-124-phase0-discovery` contains all verified source, test, documentation, and RPI tracking files.

### Boundaries

* Included: `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `docs/reference/README.md`, `docs/reference/log.md`, `docs/brds/retrofit-flow-discovery-brief.md`, `src/core/README.md`, focused local checks, and local Git commit(s).
* Excluded: Running `tools/rpi-checks.py --all`, pushing to remote, or opening/editing a GitHub PR or issue.

### Likely Targets

* `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`: New knowledge-base research page documenting the Phase 0 discovery contract.
* `docs/reference/README.md`: Add routing/catalog entry linking to `./research/company/phase0-retrofit-flow-discovery-contract.md`.
* `docs/reference/log.md`: Append `## [2026-11-15] ingest | Phase 0 retrofit-flow discovery contract (Refs #124)`.
* `docs/brds/retrofit-flow-discovery-brief.md`: Update `Delivery Status` section (`ms.date: 2026-11-15`) to cite `discovery_contract.py` and the research page while keeping human-gated company criteria honestly `Unmet` pending real sponsor/owner sign-off and 12-month extract.
* `src/core/README.md`: Document `discovery_contract` and the updated governance fields in the Phase 0 discovery section.

### Dependencies

* `P01`, `P02`.

### Validation Expectations

* Isolated `~/.cache` Python 3.12 venv editable path binding (`site-packages/zava_forward_core.pth`) followed by `test_discovery*.py` (87 tests), `test_live_doc_links.py`, `test_dependency_rule.py`, `ruff check .`, `ruff format --check .`, `mypy`, `compileall`, and `python3 tools/rename-zava-tests.py` all exit 0; `tools/check-legacy-references.py` reports 0 link violations and 0 touched-file violations; `git status --short` is clean after final commit.

### Completion Evidence

* Clean `git status --short`, verified non-amended commits on `feat/gov-124-phase0-discovery` with Copilot trailer and noreply email, and passing test/lint/typecheck outputs.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Author `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md` and Synchronize Indexes and Guides

#### Context

New Markdown files in `docs/reference/` must have YAML frontmatter (`title`, `description`, `ms.date: 2026-11-15`, `ms.topic: reference`), no `#` H1 heading, `*` unordered lists without bolded-prefix list items, plain ASCII punctuation without em dashes, no `.copilot-tracking/` references in live documentation or production code, resolving relative links, and explicit provenance classification for regulatory/standards references (`pas-2035-2023-bsi-overview.md` overview snapshot retrieved 2026-09-19; licensed PAS 2035:2023 text not held, `C11`).

#### Intent

Publish a clear, cited, standards-compliant knowledge-base reference for the Phase 0 retrofit-flow discovery contract and synchronize all indexes and component guides.

#### Boundaries

* Included: `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `docs/reference/README.md`, `docs/reference/log.md`, `docs/brds/retrofit-flow-discovery-brief.md`, `src/core/README.md`.
* Excluded: Modifying `docs/case_study_48_original.md`, `docs/reference/memory.md`, or immutable `docs/reference/regulatory/` snapshots.

#### Likely Targets

* `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`
* `docs/reference/README.md`
* `docs/reference/log.md`
* `docs/brds/retrofit-flow-discovery-brief.md`
* `src/core/README.md`

#### Dependencies

* `P01`, `P02`.

#### Validation Expectations

* `test_live_doc_links.py` and `tools/check-legacy-references.py` exit 0; manual inspection confirms zero em dashes, zero bolded-prefix bullets, no H1 with frontmatter `title`, and zero `.copilot-tracking/` paths in live docs/code.

#### Completion Evidence

* Clean diff and passing link/legacy checks.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Run Focused Validation Suite and Commit Implementation + RPI Artifacts Locally

#### Context

`.github/workflows/src-ci.yml` runs `unittest discover -s tests -v`, `ruff check . && ruff format --check .`, and `mypy` inside `src/core` with `zava-forward-core` editable-installed (`C14`). Per critique `PC-004`, validation uses an isolated `~/.cache` Python 3.12 virtualenv (`--no-build-isolation`) rather than `/tmp`, cleans up temporary `src/core/src/*.egg-info` metadata before staging, configures local `git config --local user.email "{id}+{login}@users.noreply.github.com"` via `gh api user`, and avoids `git commit --amend` by committing all code, tests, docs, and RPI artifacts through `rpi-implement` in Commit 1, leaving `rpi-review` to add its review log and final state in Commit 2.

#### Intent

Verify all code and documentation checks pass in an isolated Python 3.12 editable environment, clean up temporary `src/core/src/*.egg-info`, and create a clean Conventional Commit with the Copilot trailer on `feat/gov-124-phase0-discovery`.

#### Boundaries

* Included: `~/.cache` virtualenv setup/cleanup, `unittest`, `ruff`, `mypy`, `check-legacy-references.py`, `rename-zava-tests.py`, local git config `user.email`, and `git commit` on `feat/gov-124-phase0-discovery`.
* Excluded: `tools/rpi-checks.py --all`, `git commit --amend`, `git push`, `gh pr create`, or modifying remote branches.

#### Likely Targets

* Local Git branch `feat/gov-124-phase0-discovery` and `.copilot-tracking/` 2026-11-15 artifacts.

#### Dependencies

* `P01`, `P02`, `P03-T01`.

#### Validation Expectations

* Zero test, ruff, mypy, or link failures across all touched and related modules (with pre-existing host/base-branch exclusions recorded explicitly in `changes.md`); `git status --short` empty after commit.

#### Completion Evidence

* Exact validation command outputs recorded in `.copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-changes.md` prior to commit.

#### Unresolved Items

* None.
