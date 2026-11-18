<!-- markdownlint-disable-file -->
# RPI Plan: Phase 0 Retrofit-Flow Discovery Contract c1 Remediation (Issue #124)

## Task Metadata

* Task ID: issue-124-c1
* Task slug: phase0-retrofit-flow-discovery-124-c1
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan-critique.md

## Executive Summary

This `c1` remediation plan resolves all three post-implementation review findings (`RV-001`, `RV-002`, and `RV-003`) recorded in `.copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md` for Issue #124 (`BG-011`, `RULE-019`) on branch `feat/gov-124-phase0-discovery`:

1. **`RV-001` (Flow-report promotion, baseline cohort filtering, `as_of` cutoff, and zero-event semantics)**:
   * Refuse `FlowDiscoveryReport` owner validation across `FlowDiscoveryReport.__post_init__`, `validate_flow_report`, `Phase0DiscoveryPack.__post_init__`, and `enforce_governance_guard` with `GovernanceViolationError` whenever `report.gaps` or `report.invalid_accepted_handover_ids` is non-empty.
   * Restrict cohort aggregations in `evaluate_property_flow` strictly to `baseline_candidate_ids` with timestamps on or before `as_of` (UTC calendar date `<= as_of`), recording explicit plain-language `gaps` whenever a candidate `identified_at` or any stage/event/wait/loop timestamp falls after `as_of` or references a `property_id` outside `baseline_candidate_ids`.
   * Base `zero_event_candidate_ids` strictly on the presence of valid in-cohort `<= as_of` lifecycle events (so stage, wait, or return-loop records without lifecycle events never mask a zero-event candidate).
2. **`RV-002` (Deep container immutability, verified `calculation_digest`, role-bound spec checks, and canonical stage order)**:
   * Recursively freeze all nested mappings and sequences on `FlowDiscoveryReport` in `__post_init__` via a pure-stdlib `FrozenDict(dict[K, V])` + `tuple` coercion AND bind `FlowDiscoveryReport`, `validate_flow_report`, `validate_discovery_pack`, and `enforce_governance_guard` to a deterministic SHA-256 `calculation_digest`, blocking post-sign-off dict mutation (`TypeError`) as well as `object.__setattr__` or `dict.__setitem__` tampering (`GovernanceViolationError`) while preserving `dataclasses.asdict()` and `json.dumps()` compatibility.
   * Add `validated_role: str = ""` to `StageSpec`, `EventSpec`, `TimestampSpec`, `WaitStateSpec`, and `ReturnLoopSpec`, populate it in `validate_*_spec`, and require `validated_role == owner_role` in `.validated` and `lifecycle_dictionary_gaps()`.
   * Enforce exact canonical `(1..10, REQUIRED_FLOW_STAGE_CODES)` flow-stage ordering in `LifecycleDictionary.__post_init__` (raising `GovernanceViolationError(ValueError)` on any reordered, missing, or misnumbered flow stage).
3. **`RV-003` (Separate `unknown_cause_count` and `disputed_cause_count` in party wait summaries)**:
   * Add `unknown_cause_count` (`cause_code` in `{"UNKNOWN", ""}`) and `disputed_cause_count` (`cause_code == "DISPUTED"`) keys to each `waits_by_party` row in `evaluate_property_flow`, retaining both `unknown_or_disputed_count` and `unknown_or_disputed_cause` for backward compatibility.

### User Decisions and Requirements Highlights

* Run the full RPI correction loop (`research`, `plan` with critique, `implement`, `review`) in order for Issue #124 (`c1`), resolving `RV-001`, `RV-002`, and `RV-003` and recording a `Conformant` review verdict under `.copilot-tracking/`.
* Execute only the focused validation tier with `TMPDIR=/dev/shm` (`test_discovery*.py`, `test_live_doc_links.py`, `test_dependency_rule.py`, `ruff check`, `ruff format --check`, and `mypy`); do not run full `unittest discover` across all 3,730 `src/core` tests.
* Commit all changes and `.copilot-tracking/` `c1` artifacts locally on `feat/gov-124-phase0-discovery` using a Conventional Commit message (`Refs #124`) and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, without pushing or running `gh pr create`.

### What You May Not Know

* Python 3.12 `dataclasses.asdict()` fails with `TypeError: cannot pickle 'mappingproxy' object` on `types.MappingProxyType` (`C12` in `.copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md`). Using an immutable `FrozenDict(dict)` subclass combined with a verified SHA-256 `calculation_digest` blocks in-place mutation AND low-level tampering while keeping `asdict()` and `json.dumps()` deterministic.
* Two existing unit tests in `src/core/tests/test_discovery_contract.py` (`test_flow_preserves_unknown_disputed_unattributed_waits_and_counts_return_loops` and `test_flow_flags_malformed_naive_unknown_and_out_of_order_timestamps_without_guessing`) passed `P2` wait/event records without listing `P2` in `candidates` (`C11`). Updating those two fixtures to include `BaselineCandidateRecord("P2", ...)` preserves their intended in-cohort assertions while new `RV-001` tests explicitly verify unmatched-cohort rejection and gap logging.
* Existing `discovery_contract.py` and `test_discovery_contract.py` assert `unknown_or_disputed_cause` on `waits_by_party` rows while `RV-003` specifies `unknown_or_disputed_count`; emitting both compatibility aliases alongside `unknown_cause_count` and `disputed_cause_count` guarantees zero consumer breakage.

### Unresolved Decisions or Blockers

* None. Real-world Zava North Homes human governance actions (`OD-14`, `OD-16`, `OD-18`, `OD-36`) remain external human sign-off boundaries as established in parent Issue #124.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI correction loop (`research`, `plan`, `implement`, `review`) in order for Issue #124 (`c1`), resolving `RV-001`, `RV-002`, and `RV-003` from `.copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md` and recording a `Conformant` review verdict under `.copilot-tracking/` (`Caller prompt`).
* Work in `/home/azureuser/source/ama-demo-wt/feat-124-phase0-discovery` on branch `feat/gov-124-phase0-discovery` targeting base `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) (`Caller prompt`).
* Resolve `RV-001` [Medium]: refuse `validate_flow_report` with `GovernanceViolationError` when `report.gaps` or `report.invalid_accepted_handover_ids` is non-empty; in `evaluate_property_flow`, restrict cohort aggregations to `baseline_candidate_ids` up to `as_of` while recording unmatched-cohort or post-cutoff records in `gaps`; base `zero_event_candidate_ids` strictly on lifecycle event presence; add focused unit tests in `src/core/tests/test_discovery_contract.py` (`Caller prompt`; `RV-001`).
* Resolve `RV-002` [Medium]: freeze nested mappings on `FlowDiscoveryReport` and bind `validate_flow_report` + `enforce_governance_guard` to a verified immutable `calculation_digest`; record and verify `validated_role == owner_role` inside dictionary spec gap checks (`StageSpec`, `EventSpec`, `TimestampSpec`, `WaitStateSpec`, `ReturnLoopSpec` / `lifecycle_dictionary_gaps()`); enforce canonical `REQUIRED_FLOW_STAGE_CODES` order in `LifecycleDictionary.__post_init__`; add focused unit tests in `src/core/tests/test_discovery_contract.py` (`Caller prompt`; `RV-002`).
* Resolve `RV-003` [Low]: add `unknown_cause_count` and `disputed_cause_count` keys to each `waits_by_party` row in `evaluate_property_flow` (retaining `unknown_or_disputed_count` and existing `unknown_or_disputed_cause` for backward compatibility) and assert both counters in `src/core/tests/test_discovery_contract.py` (`Caller prompt`; `RV-003`).
* Execute focused validation only (`TMPDIR=/dev/shm`; `test_discovery*.py`, `test_live_doc_links.py`, `test_dependency_rule.py`, `ruff check .`, `ruff format --check .`, `mypy`), and commit all code, docs, and `.copilot-tracking/` `c1` artifacts locally with `Refs #124` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing or running `gh pr create` (`Caller prompt`).

## Goals

* Close all three open review defects (`RV-001`, `RV-002`, `RV-003`) in `src/core/src/zava_forward/core/discovery_contract.py` with fail-closed, stdlib-pure, strictly typed invariants.
* Prove every hardened governance, cohort, cutoff, immutability, role-matching, stage-ordering, and wait-counter invariant with deterministic unit tests in `src/core/tests/test_discovery_contract.py` while keeping all existing discovery, link, dependency, lint, and strict type checks green.
* Synchronize directly coupled documentation (`docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md`) and produce a clean `Conformant` RPI `c1` artifact chain committed locally on `feat/gov-124-phase0-discovery`.

## Scope and Non-Goals

### In Scope

* Contract hardening in `src/core/src/zava_forward/core/discovery_contract.py` for `RV-001`, `RV-002`, and `RV-003`.
* Deterministic unit test additions (`<= 12` new test methods, `0` test removals, plus updating `2` existing `P2` candidate fixtures) in `src/core/tests/test_discovery_contract.py`.
* Directly coupled documentation updates in `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and `docs/reference/log.md`.
* Focused validation execution (`TMPDIR=/dev/shm`) and clean local Git commit(s) on `feat/gov-124-phase0-discovery`.

### Non-Goals

* Modifying `discovery_register.py`, `discovery_flow.py`, or `discovery_assistant_*.py` (all reconciled in parent review with zero findings).
* Adding CSV extract loaders, persistence layers, API routes, or UI components.
* Running full 3,730-test `src/core` discovery, running `tools/rpi-checks.py --all`, pushing to `origin`, or opening/modifying any GitHub PR or issue.

## Functional Requirements

* FR-C1-1 (Fail-Closed Flow Report Promotion): `FlowDiscoveryReport.__post_init__`, `validate_flow_report`, `Phase0DiscoveryPack.__post_init__`, and `enforce_governance_guard` (including serialized `Mapping` and `Phase0DiscoveryPack` outputs) shall raise `GovernanceViolationError` whenever a flow report claims `owner_validated=True` (or promoted `finding_status`) while `report.gaps` or `report.invalid_accepted_handover_ids` is non-empty (`RV-001`, `PC-001`).
  * Observable acceptance criteria: Calling `validate_flow_report`, `validate_discovery_pack`, direct `FlowDiscoveryReport(..., owner_validated=True, ...)`, or `enforce_governance_guard` (on dataclass or serialized `Mapping` outputs) on a report with any gap or invalid accepted handover raises `GovernanceViolationError`.
* FR-C1-2 (Baseline Cohort and `as_of` Cutoff Filtering plus Strict Zero-Event Semantics): `evaluate_property_flow` shall exclude candidate records with `identified_at` after `as_of` (recording a post-cutoff gap and computing `duplicate_candidate_ids` strictly over valid in-window `<= as_of` candidates), exclude stage/event/wait/loop records whose `property_id` is absent from `baseline_candidate_ids` or whose parsed timestamp(s) fall after `as_of` (recording explicit unmatched-cohort or post-cutoff gaps), restrict all per-property and cohort aggregations strictly to `baseline_candidate_ids` up to `as_of`, and compute `zero_event_candidate_ids` strictly from the presence of valid in-cohort `<= as_of` lifecycle events (`RV-001`, `PC-002`).
  * Observable acceptance criteria: Out-of-cohort and post-`as_of` candidate, stage, event, wait, and loop records do not alter `duplicate_candidate_ids`, `stage_metrics`, `waits_by_party`, `waits_by_state`, `return_loop_totals`, `explicit_rework_days_by_kind`, or leg dictionaries, and each emits a plain-language gap; a baseline candidate with stage/wait/loop records but zero lifecycle events remains in `zero_event_candidate_ids`.
* FR-C1-3 (Deep Container Immutability and Verified `calculation_digest` on `FlowDiscoveryReport`): `FlowDiscoveryReport` shall recursively freeze all nested mappings and containers (`FrozenDict` + `tuple`) in `__post_init__` so post-construction dict mutations raise `TypeError`, and shall compute and verify a non-blank deterministic SHA-256 `calculation_digest` across all report data fields inside `FlowDiscoveryReport.__post_init__`, `FlowDiscoveryReport.verify_digest()`, `validate_flow_report()` (before `replace(...)`), `validate_discovery_pack()`, and `enforce_governance_guard()` (unconditionally before the `if not owner_val:` early return on both `FlowDiscoveryReport` and `Phase0DiscoveryPack.flow_report`) so any low-level tampering raises `GovernanceViolationError` (`RV-002`, `PC-001`).
  * Observable acceptance criteria: Mutating `report.state_counts[...]`, `report.post_install_handover_legs_days[...][...]`, `report.stage_metrics[0][...]`, `report.waits_by_party[0][...]`, or `report.return_loops_by_property[...][...]` raises `TypeError`; forging `calculation_digest` or bypassing freeze via `object.__setattr__` / `dict.__setitem__` raises `GovernanceViolationError` in `validate_flow_report` and `enforce_governance_guard`; `dataclasses.asdict(report)` and `json.dumps()` succeed deterministically.
* FR-C1-4 (Role-Bound Dictionary Spec Validation and Canonical Stage Ordering): `StageSpec`, `EventSpec`, `TimestampSpec`, `WaitStateSpec`, and `ReturnLoopSpec` shall carry `validated_role: str = ""` set by `validate_*_spec` and verify `validated_role == owner_role` in `.validated` and `lifecycle_dictionary_gaps()`, and `LifecycleDictionary.__post_init__` shall enforce exact canonical `(1..10, REQUIRED_FLOW_STAGE_CODES)` ordering across `kind == "flow"` stages (`RV-002`).
  * Observable acceptance criteria: Directly constructing any dictionary spec with `validated_by` and `validated_on` but missing or mismatched `validated_role` reports `spec.validated is False` and leaves an open gap in `lifecycle_dictionary_gaps()`; constructing `LifecycleDictionary` with reordered, misnumbered, missing, or extra flow stages raises `GovernanceViolationError(ValueError)`.
* FR-C1-5 (Separate `unknown_cause_count` and `disputed_cause_count` Party Wait Counters): Each `waits_by_party` row emitted by `evaluate_property_flow` shall include `unknown_cause_count` (where `cause_code.strip() in {"UNKNOWN", ""}`) and `disputed_cause_count` (where `cause_code.strip() == "DISPUTED"`), while retaining `unknown_or_disputed_count` and `unknown_or_disputed_cause` equal to their sum (`RV-003`).
  * Observable acceptance criteria: Party wait rows report exact `unknown_cause_count`, `disputed_cause_count`, `unknown_or_disputed_count`, and `unknown_or_disputed_cause` values across mixed `UNKNOWN`, blank, `DISPUTED`, and attributed wait records.

## Non-Functional Requirements

* NFR-C1-1 (Pure Stdlib Determinism and Serialization Compatibility): All `discovery_contract` types and functions remain pure Python 3.12 stdlib with zero external dependencies, deterministic SHA-256 digests, and full `dataclasses.asdict()` compatibility.
  * Objective threshold or evaluation condition: `test_dependency_rule.py` passes and repeated `asdict(evaluate_property_flow(...))` JSON digests match identically.
  * Operating condition or verification approach, if needed: Targeted unit tests run with `TMPDIR=/dev/shm`.
  * Observable acceptance criteria: `test_discovery_contract.py` and `test_dependency_rule.py` pass with exit code 0.
* NFR-C1-2 (Strict Static Typing, Formatting, and Test Discipline): Modified Python sources and tests pass `ruff check .`, `ruff format --check .`, and `mypy` (`strict = true`), adding at most 12 focused tests and removing 0 tests.
  * Objective threshold or evaluation condition: 0 lint errors, 0 format diffs, 0 `mypy` issues across `src/core`, `0` tests removed, and `<= 12` focused tests added in `test_discovery_contract.py`.
  * Operating condition or verification approach, if needed: Focused `src/core` lint, format, typecheck, and targeted `unittest` commands.
  * Observable acceptance criteria: All focused validation commands exit 0.

## Acceptance Criteria

* AC-C1-1: `validate_flow_report`, `FlowDiscoveryReport.__post_init__`, `Phase0DiscoveryPack.__post_init__`, and `enforce_governance_guard` reject owner validation with `GovernanceViolationError` whenever `gaps` or `invalid_accepted_handover_ids` is non-empty (`FR-C1-1`, `RV-001`).
* AC-C1-2: `evaluate_property_flow` restricts all cohort aggregations to `baseline_candidate_ids` on or before `as_of`, records unmatched-cohort and post-cutoff records in `gaps`, and computes `zero_event_candidate_ids` strictly from lifecycle events (`FR-C1-2`, `RV-001`).
* AC-C1-3: `FlowDiscoveryReport` deeply freezes nested mappings/sequences (`FrozenDict` + `tuple`) against post-construction mutation (`TypeError`), binds and verifies `calculation_digest` across `validate_flow_report`, `validate_discovery_pack`, and `enforce_governance_guard` (`GovernanceViolationError` on tamper), and preserves `dataclasses.asdict()` (`FR-C1-3`, `NFR-C1-1`, `RV-002`).
* AC-C1-4: All five dictionary spec classes verify `validated_role == owner_role` in `.validated` and `lifecycle_dictionary_gaps()`, and `LifecycleDictionary.__post_init__` rejects non-canonical flow-stage ordering against `REQUIRED_FLOW_STAGE_CODES` (`FR-C1-4`, `RV-002`).
* AC-C1-5: `waits_by_party` rows include accurate `unknown_cause_count` and `disputed_cause_count` counters while retaining `unknown_or_disputed_count` and `unknown_or_disputed_cause` (`FR-C1-5`, `RV-003`).
* AC-C1-6: Focused validation (`test_discovery*.py`, `test_live_doc_links.py`, `test_dependency_rule.py`, `ruff check .`, `ruff format --check .`, `mypy`) passes with `TMPDIR=/dev/shm`, documentation is synchronized, and all changes plus `c1` RPI artifacts are committed cleanly on `feat/gov-124-phase0-discovery` without push or PR creation (`NFR-C1-2`).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan.md                                                         |
| Phase details                    | .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md                                              |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan-critique.md (`Revise` with `PC-001` and `PC-002` applied and resolved) |
| Relevant research                | .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md                                                  |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-c1-changes.md is created by implementation as its evidence record |
| Planning execution and readiness | Complete and implementation-ready (`ready`)                                                                                              |
| Continuation context             | Confirmed automatic RPI Agent (`issue-124-c1`) continues automatically to `rpi-implement`                                                |

## Sources

* .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md: Authoritative specification of `RV-001`, `RV-002`, and `RV-003`.
* .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md: Codebase evidence (`C1`–`C12`), `FrozenDict` + `calculation_digest` verification, and `P2` test fixture findings.
* src/core/src/zava_forward/core/discovery_contract.py: Canonical Phase 0 contract implementation target.
* src/core/tests/test_discovery_contract.py: Canonical unit test target.
* docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md: Canonical KB synthesis target.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Harden `discovery_contract.py` for `RV-001`, `RV-002`, and `RV-003`

* Intent: Close flow-report gap/handover promotion checks, baseline cohort and `as_of` cutoff filtering, strict zero-event semantics, deep `FrozenDict` + `calculation_digest` immutability, `validated_role == owner_role` spec checks, canonical `LifecycleDictionary` stage ordering, and separate `unknown_cause_count` / `disputed_cause_count` counters in `src/core/src/zava_forward/core/discovery_contract.py`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement `RV-002` dictionary role/order invariants and `FlowDiscoveryReport` deep freeze + `calculation_digest`

* Requirement and evidence: `FR-C1-1`, `FR-C1-3`, `FR-C1-4`, `NFR-C1-1`, `NFR-C1-2`; `C1`–`C4`, `C6`, `C8`, `C9`, `C12`.
* Expected result: `StageSpec`, `EventSpec`, `TimestampSpec`, `WaitStateSpec`, and `ReturnLoopSpec` record and verify `validated_role == owner_role`; `LifecycleDictionary.__post_init__` enforces exact `(1..10, REQUIRED_FLOW_STAGE_CODES)` flow-stage ordering; `FlowDiscoveryReport` recursively freezes nested mappings/tuples via `FrozenDict`, computes/verifies `calculation_digest`, and rejects non-empty `gaps`, non-empty `invalid_accepted_handover_ids`, or digest mismatch across `__post_init__`, `validate_flow_report`, `Phase0DiscoveryPack`, and `enforce_governance_guard`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Implement `RV-001` cohort/`as_of`/zero-event rules and `RV-003` separate wait cause counters in `evaluate_property_flow`

* Requirement and evidence: `FR-C1-2`, `FR-C1-5`, `NFR-C1-1`, `NFR-C1-2`; `C5`, `C11`.
* Expected result: `evaluate_property_flow` filters candidates and stage/event/wait/loop records to `baseline_candidate_ids` with UTC calendar date `<= as_of`, records unmatched-cohort and post-cutoff gaps, computes `zero_event_candidate_ids` strictly from valid in-cohort `<= as_of` lifecycle events, and populates `unknown_cause_count`, `disputed_cause_count`, `unknown_or_disputed_count`, and `unknown_or_disputed_cause` on each `waits_by_party` row.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Focused Unit Tests, Documentation Sync, and Validation

* Intent: Prove all `RV-001`–`RV-003` invariants in `src/core/tests/test_discovery_contract.py`, synchronize directly coupled documentation, pass focused validation (`TMPDIR=/dev/shm`), and prepare clean local Git state.
* Dependencies: `P01`

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add focused `RV-001`–`RV-003` unit tests and align `P2` baseline candidate fixtures in `test_discovery_contract.py`

* Requirement and evidence: `AC-C1-1`–`AC-C1-5`, `NFR-C1-2`; `C11`, `C12`.
* Expected result: Canonical test owner `src/core/tests/test_discovery_contract.py` has `0` removed tests, `2` updated `P2` candidate tuples in existing tests so in-cohort `P2` assertions remain meaningful, and `<= 12` new semantic/governance unit tests covering gap/invalid-handover promotion refusal, unmatched-cohort and post-`as_of` filtering, lifecycle-only `zero_event_candidate_ids`, nested `FrozenDict` mutation `TypeError`, `calculation_digest` tamper `GovernanceViolationError`, direct-spec `validated_role` mismatch gaps, `LifecycleDictionary` non-canonical stage-order rejection, and separate `unknown_cause_count` / `disputed_cause_count` wait counters.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Synchronize Phase 0 contract documentation, run focused validation, and commit `c1` implementation locally

* Requirement and evidence: `AC-C1-6`, `NFR-C1-1`, `NFR-C1-2`; `C7`.
* Expected result: `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and `docs/reference/log.md` reflect deep immutability / `calculation_digest`, role-bound spec checks, baseline/`as_of` filtering, and separate wait cause counters; all caller-specified focused validation commands pass with `TMPDIR=/dev/shm`; code, tests, docs, and `c1` RPI artifacts through `rpi-implement` are committed locally on `feat/gov-124-phase0-discovery` (`Refs #124` + Copilot trailer) before `rpi-review` executes and records the final `Conformant` verdict commit.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md

## Dependencies

* Existing commit `82b7b368d` (`0c2457297` implementation + review) on branch `feat/gov-124-phase0-discovery`: baseline for `c1` remediation.
* Python 3.12 toolchain (`unittest`, `ruff`, `mypy`) with `TMPDIR=/dev/shm` and ephemeral `/dev/shm/zf-124-c1-venv` `.pth` shim when isolated installed-module execution is needed by `test_discovery_assistant_demo.py`.

## Critique Disposition

Single final-candidate critique executed in `.copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan-critique.md` (`Verdict: Revise`; 0 Critical, 0 High, 1 Medium `PC-001`, 1 Low `PC-002`). Both findings were direct planner-owned tightenings applied in one coherent batch with no user decision required.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `c1-critique` `PC-001` [Medium] | resolved | Updated `FR-C1-1`, `FR-C1-3`, `P01-T01`, and `P02-T01` so `FlowDiscoveryReport.verify_digest()` rejects blank digests, `validate_flow_report` executes `verify_digest()` and checks `not gaps and not invalid_accepted_handover_ids` before `replace(...)`, `enforce_governance_guard` runs `verify_digest()` unconditionally before the `if not owner_val:` early return on both `FlowDiscoveryReport` and `Phase0DiscoveryPack.flow_report`, and `enforce_governance_guard` rejects `owner_validated=True` `Mapping` and `Phase0DiscoveryPack` outputs with non-empty `gaps` or `invalid_accepted_handover_ids`. |
| `c1-critique` `PC-002` [Low] | resolved | Updated `FR-C1-2`, `P01-T02`, and `P02-T01` so `duplicate_candidate_ids` in `evaluate_property_flow` is computed from `in_window` (valid in-window `<= as_of` candidates prior to `dict.fromkeys` deduplication) rather than raw `candidates`, preventing post-`as_of` duplicate candidates from leaking into cohort outputs. |

## Follow-Up Items

* Optional CSV extract adapter mapping `support/synthetic-data/retrofit-flow/zava-forward-year-one/` tables into `discovery_contract` dataclasses: deferred outside Phase 0 rule-layer scope per `docs/brds/retrofit-flow-discovery-brief.md` until sponsor/owner direction.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-c1-changes.md
* Ready phase or task: `P01` (`P01-T01`)
* Remaining provisional question or blocker: none
