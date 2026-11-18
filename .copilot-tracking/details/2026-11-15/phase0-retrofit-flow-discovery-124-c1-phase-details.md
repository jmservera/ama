<!-- markdownlint-disable-file -->
# RPI Phase Details: Phase 0 Retrofit-Flow Discovery Contract c1 Remediation (Issue #124)

## Metadata

* Task ID: issue-124-c1
* Task slug: phase0-retrofit-flow-discovery-124-c1
* Related plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan.md
* Evidence sources: .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md, .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md

## Phase Index

| Phase ID | Name                                                                 | Status | Detail sections        |
|----------|----------------------------------------------------------------------|--------|------------------------|
| P01      | Harden `discovery_contract.py` for `RV-001`, `RV-002`, and `RV-003`  | ready  | P01, P01-T01, P01-T02  |
| P02      | Focused Unit Tests, Documentation Sync, and Validation               | ready  | P02, P02-T01, P02-T02  |

<!-- rpi:phase id=P01 -->
## P01: Harden `discovery_contract.py` for `RV-001`, `RV-002`, and `RV-003`

### Context

Parent post-implementation review `.copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md` identified two `Medium` governance-hardening defects (`RV-001`, `RV-002`) and one `Low` fidelity defect (`RV-003`) localized to `src/core/src/zava_forward/core/discovery_contract.py`. Research (`C1`–`C12`) verified all code paths and confirmed that `FrozenDict(dict)` + SHA-256 `calculation_digest` satisfies both deep runtime immutability and `dataclasses.asdict()` compatibility.

### Intent

Update `src/core/src/zava_forward/core/discovery_contract.py` so every `RV-001`, `RV-002`, and `RV-003` invariant is enforced fail-closed in pure Python 3.12 stdlib under `mypy --strict`.

### Boundaries

* Included: `FrozenDict` helper, `FlowDiscoveryReport` deep container freezing and `calculation_digest` binding/verification, `validate_flow_report` and `enforce_governance_guard` gap/handover/digest checks, `validated_role` on all five dictionary spec classes and `lifecycle_dictionary_gaps()`, canonical `REQUIRED_FLOW_STAGE_CODES` order check in `LifecycleDictionary.__post_init__`, strict `baseline_candidate_ids` and `as_of` filtering plus lifecycle-only `zero_event_candidate_ids` in `evaluate_property_flow`, and `unknown_cause_count` / `disputed_cause_count` keys in `waits_by_party`.
* Excluded: Changes to `discovery_register.py`, `discovery_flow.py`, or any non-core package; generated files (`none`).

### Likely Targets

* `src/core/src/zava_forward/core/discovery_contract.py`: Single canonical production module for all `RV-001`–`RV-003` fixes.

### Dependencies

* None.

### Validation Expectations

* `python3 -m compileall -q src/core/src`
* `cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && mypy`

### Completion Evidence

* Updated `discovery_contract.py` passing `ruff` and `mypy --strict` with zero errors.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement `RV-002` dictionary role/order invariants and `FlowDiscoveryReport` deep freeze + `calculation_digest`

#### Context

* `StageSpec`, `EventSpec`, `TimestampSpec`, `WaitStateSpec`, and `ReturnLoopSpec` (`C2`) currently store `validated_by` and `validated_on` without `validated_role`, allowing direct construction to appear `.validated == True` without role verification.
* `LifecycleDictionary` (`C3`) lacks a `__post_init__` check enforcing canonical `REQUIRED_FLOW_STAGE_CODES` order `1..10`.
* `FlowDiscoveryReport` (`C4`, `C6`, `C9`, `C12`) holds mutable nested `dict` objects, does not reject `owner_validated=True` when `gaps` or `invalid_accepted_handover_ids` is non-empty, and lacks a verified `calculation_digest`.

#### Intent

Enforce role-bound dictionary spec validation, canonical flow-stage ordering on `LifecycleDictionary`, deep `FrozenDict` + `tuple` immutability on `FlowDiscoveryReport`, and verified `calculation_digest` + zero-gap/zero-invalid-handover gates across `FlowDiscoveryReport`, `validate_flow_report`, `Phase0DiscoveryPack`, and `enforce_governance_guard`.

#### Boundaries

* Included:
  1. Add `validated_role: str = ""` to `StageSpec`, `EventSpec`, `TimestampSpec`, `WaitStateSpec`, and `ReturnLoopSpec`; set `validated_role=role` in `validate_stage_spec`, `validate_event_spec`, `validate_timestamp_spec`, `validate_wait_state_spec`, and `validate_return_loop_spec`; update `.validated` on all five specs to require `bool(self.owner_role.strip()) and self.validated_role == self.owner_role`; emit role-mismatch / unvalidated gap messages in `lifecycle_dictionary_gaps()`.
  2. Add `LifecycleDictionary.__post_init__` checking `[(s.order, s.code) for s in self.stages if s.kind == "flow"] == list(enumerate(REQUIRED_FLOW_STAGE_CODES, start=1))` and raising `GovernanceViolationError` (a `ValueError` subclass) on mismatch; mirror canonical code-order check in `lifecycle_dictionary_gaps()`.
  3. Add slot-free `FrozenDict(dict[K, V])` overriding `__setitem__`, `__delitem__`, `clear`, `pop`, `popitem`, `setdefault`, `update`, and `__ior__` to raise `TypeError`, plus recursive `_freeze_container` converting nested mappings to `FrozenDict` and sequences (`list`/`tuple`) to `tuple` inside `FlowDiscoveryReport.__post_init__` via `object.__setattr__`.
  4. Add `calculation_digest: str = ""` to `FlowDiscoveryReport`, compute canonical SHA-256 JSON digest over all calculation payload fields (`window_start` through `gaps`) when blank, verify non-blank `self.calculation_digest == expected_digest` on construction and in `verify_digest()`, execute `report.verify_digest()` and check `not report.gaps and not report.invalid_accepted_handover_ids` before `replace(...)` in `validate_flow_report`, execute `verify_digest()` unconditionally before the `if not owner_val:` early return in `enforce_governance_guard` on both `FlowDiscoveryReport` and `Phase0DiscoveryPack.flow_report`, and reject `owner_validated=True` `FlowDiscoveryReport`, `Phase0DiscoveryPack`, and `Mapping` outputs carrying non-empty `gaps` or `invalid_accepted_handover_ids` (`PC-001`).
* Excluded: `evaluate_property_flow` cohort/cutoff/wait-counter logic (`P01-T02`).

#### Likely Targets

* `src/core/src/zava_forward/core/discovery_contract.py`: Spec dataclasses, `LifecycleDictionary`, `FrozenDict`, `FlowDiscoveryReport`, `validate_flow_report`, `Phase0DiscoveryPack`, `enforce_governance_guard`.

#### Dependencies

* None.

#### Validation Expectations

* `mypy` (`strict = true`) passes on `FrozenDict` and `FlowDiscoveryReport` annotations without new `pyproject.toml` ignores.
* `dataclasses.asdict(report)` and `json.dumps(asdict(report), sort_keys=True, default=str)` succeed without `TypeError`.

#### Completion Evidence

* Direct mutation of any nested mapping in `FlowDiscoveryReport` raises `TypeError`; digest tampering or non-empty `gaps`/`invalid_accepted_handover_ids` raises `GovernanceViolationError`; direct-constructed spec role mismatch is caught by `.validated` and `lifecycle_dictionary_gaps()`; out-of-order `LifecycleDictionary` flow stages raise `GovernanceViolationError`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Implement `RV-001` cohort/`as_of`/zero-event rules and `RV-003` separate wait cause counters in `evaluate_property_flow`

#### Context

* `evaluate_property_flow` (`C5`) currently aggregates stage, event, wait, and loop records for property IDs outside `baseline_candidate_ids` and timestamps strictly after `as_of` without logging unmatched-cohort or post-cutoff gaps, computes `zero_event_candidate_ids` from `props_with_activity` (stages + events + waits + loops), and emits only combined `unknown_or_disputed_cause` in `waits_by_party`.

#### Intent

Constrain `evaluate_property_flow` cohort metrics strictly to `baseline_candidate_ids` up to `as_of`, record unmatched-cohort and post-cutoff records in `gaps`, base `zero_event_candidate_ids` strictly on lifecycle events, and emit separate `unknown_cause_count` and `disputed_cause_count` counters on `waits_by_party` rows.

#### Boundaries

* Included:
  1. Candidate cutoff check: if parsed `ident_dt.date() > as_of`, append a gap (`Candidate <id> identified_at '<raw>' is after as_of '<as_of>'`) and exclude from `in_window` / `baseline_candidate_ids`; compute `duplicate_candidate_ids` strictly from `in_window` (valid in-window `<= as_of` candidates prior to `dict.fromkeys` deduplication) rather than raw `candidates` (`PC-002`).
  2. Cohort and `as_of` checks across `event_records`, `stage_records`, `wait_records`, and `loop_records`:
     * If `record.property_id not in baseline_id_set`, append an explicit unmatched-cohort gap (`Property <id> <kind> ... is outside baseline_candidate_ids`) and skip aggregation.
     * If any parsed timestamp on the record (`occurred_at`, `entered_at`, `exited_at`, `active_started_at`, `active_completed_at`, `started_at`, `ended_at`, `recorded_at`) has `.date() > as_of` in UTC, append an explicit post-cutoff gap (`... after as_of '<as_of>'`) and skip aggregating that post-cutoff record.
     * For open stages/waits starting on `as_of` with a non-midnight UTC timestamp (`ent > as_of_dt` or `ws > as_of_dt`), clamp the open reference end to `max(as_of_dt, start_ts)` so same-day `as_of` datetimes yield `0.0` elapsed days while whole-date inputs (`YYYY-MM-DD`) preserve exact integer-day differences.
  3. Lifecycle-only zero-event computation: track `props_with_lifecycle_events: set[str]` populated exclusively by valid in-cohort `<= as_of` `PropertyEventRecord` entries; compute `zero_event_ids = tuple(pid for pid in baseline_ids if pid not in props_with_lifecycle_events)` and iterate leg summaries strictly over `baseline_ids`.
  4. Separate party wait cause counters (`RV-003`): track `party_unknown_cause` (`cause_code.strip() in {UNKNOWN, ""}`) and `party_disputed_cause` (`cause_code.strip() == WAIT_CAUSE_DISPUTED`) separately, and emit `unknown_cause_count`, `disputed_cause_count`, `unknown_or_disputed_count`, and `unknown_or_disputed_cause` on each `waits_by_party` row.
* Excluded: External CSV file parsing.

#### Likely Targets

* `src/core/src/zava_forward/core/discovery_contract.py`: `evaluate_property_flow`.

#### Dependencies

* `P01-T01`.

#### Validation Expectations

* Targeted `test_discovery_contract.py` passes all cohort, cutoff, zero-event, and party wait counter assertions.

#### Completion Evidence

* `evaluate_property_flow` emits frozen `FlowDiscoveryReport` instances obeying all `RV-001` and `RV-003` invariants.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Focused Unit Tests, Documentation Sync, and Validation

### Context

All hardened contract behaviors need focused semantic/governance unit tests in `src/core/tests/test_discovery_contract.py`, synchronized documentation in `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and `docs/reference/log.md`, focused validation with `TMPDIR=/dev/shm`, and clean local Git commit closeout.

### Intent

Lock test coverage for `RV-001`–`RV-003`, update coupled documentation, run the caller-mandated focused validation suite, and commit cleanly on `feat/gov-124-phase0-discovery`.

### Boundaries

* Included:
  * Canonical test owner: `src/core/tests/test_discovery_contract.py` (`0` test removals, `<= 12` test additions, `2` fixture candidate-tuple updates for `P2`).
  * Canonical docs: `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md`.
  * Generated targets: `none`.
* Excluded: Full 3,730-test `src/core` run, `tools/rpi-checks.py --all`, `git push`, `gh pr create`.

### Likely Targets

* `src/core/tests/test_discovery_contract.py`: Unit test suite for `discovery_contract`.
* `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`: Phase 0 contract KB synthesis.
* `src/core/README.md`: Core package Phase 0 section.
* `docs/reference/log.md`: Append-only KB change log.

### Dependencies

* `P01`.

### Validation Expectations

* `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests ~/.cache/zf-124-venv/bin/python -m unittest discover -s src/core/tests -p 'test_discovery*.py' -v` (plus direct `python3` check)
* `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_live_doc_links.py src/core/tests/test_dependency_rule.py -v`
* `cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && mypy`

### Completion Evidence

* All focused test, link, dependency, lint, format, and `mypy` checks pass with exit code 0, and local Git commit is clean on `feat/gov-124-phase0-discovery`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add focused `RV-001`–`RV-003` unit tests and align `P2` baseline candidate fixtures in `test_discovery_contract.py`

#### Context

* Research (`C11`) identified two existing tests in `test_discovery_contract.py` (`test_flow_preserves_unknown_disputed_unattributed_waits_and_counts_return_loops` and `test_flow_flags_malformed_naive_unknown_and_out_of_order_timestamps_without_guessing`) that omitted `BaselineCandidateRecord("P2", ...)` from `candidates` while asserting in-cohort `P2` metrics.
* Semantic-versus-regression test budget: `0` removals, `<= 12` focused new test methods covering every `RV-001`, `RV-002`, and `RV-003` edge case that would fail without the `c1` remediation.

#### Intent

Update the two `P2` candidate fixtures and add focused unit tests proving every `RV-001`, `RV-002`, and `RV-003` behavior.

#### Boundaries

* Included:
  1. Update `candidates` in `test_flow_preserves_unknown_disputed_unattributed_waits_and_counts_return_loops` and `test_flow_flags_malformed_naive_unknown_and_out_of_order_timestamps_without_guessing` to include `BaselineCandidateRecord("P2", "2026-01-02", "c-2")`, and assert `unknown_cause_count == 1`, `disputed_cause_count == 0` for Installer Alpha and `unknown_cause_count == 0`, `disputed_cause_count == 1`, `unknown_or_disputed_count == 1` for `Unattributed`.
  2. Add focused tests for `RV-001` (`PC-001`, `PC-002`):
     * `validate_flow_report`, `validate_discovery_pack`, direct `FlowDiscoveryReport(..., owner_validated=True)`, and `enforce_governance_guard` (including serialized `Mapping` outputs) raise `GovernanceViolationError` when `report.gaps` or `report.invalid_accepted_handover_ids` is non-empty.
     * `evaluate_property_flow` excludes unmatched-cohort (`P-OUTSIDE`) and post-`as_of` candidate/stage/event/wait/loop records from all cohort aggregations (including `duplicate_candidate_ids`) while recording explicit gaps.
     * `zero_event_candidate_ids` retains baseline candidates that have stage, wait, or return-loop records (or only post-`as_of` events) when they have zero valid in-cohort `<= as_of` lifecycle events.
  3. Add focused tests for `RV-002` (`PC-001`):
     * Mutating any top-level or nested mapping on `FlowDiscoveryReport` (`state_counts`, `post_install_handover_legs_days["P1"]`, `stage_metrics[0]`, `waits_by_party[0]`, `return_loops_by_property["P1"]`) raises `TypeError`.
     * Tampering with `FlowDiscoveryReport` via `object.__setattr__` (including blanking `calculation_digest=""` on a candidate `owner_validated=False` report) or `dict.__setitem__` invalidates `calculation_digest` and raises `GovernanceViolationError` in `validate_flow_report` and `enforce_governance_guard`.
     * Direct construction of `StageSpec`, `EventSpec`, `TimestampSpec`, `WaitStateSpec`, and `ReturnLoopSpec` without matching `validated_role == owner_role` keeps `.validated is False` and emits gaps in `lifecycle_dictionary_gaps()`.
     * Constructing `LifecycleDictionary` with swapped or non-canonical `REQUIRED_FLOW_STAGE_CODES` order raises `GovernanceViolationError(ValueError)`.
  4. Add/verify focused assertions for `RV-003`:
     * Separate `unknown_cause_count` (blank + `"UNKNOWN"`), `disputed_cause_count` (`"DISPUTED"`), and `unknown_or_disputed_count` (`== unknown_cause_count + disputed_cause_count`) across multiple waits for the same party.
* Excluded: Trivial constant/getter assertions; modifying `test_discovery_register.py` or `test_discovery_flow.py`.

#### Likely Targets

* `src/core/tests/test_discovery_contract.py`: Canonical unit test file.

#### Dependencies

* `P01-T01`, `P01-T02`.

#### Validation Expectations

* `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests ~/.cache/zf-124-venv/bin/python -m unittest discover -s src/core/tests -p 'test_discovery*.py' -v` passes all tests.

#### Completion Evidence

* All existing and new discovery tests pass in `< 2s`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Synchronize Phase 0 contract documentation, run focused validation, and commit `c1` implementation locally

#### Context

* Repository rules require updating directly related documentation (`docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and an append-only entry in `docs/reference/log.md` when KB content changes materially), verifying links (`test_live_doc_links.py`) and dependency boundaries (`test_dependency_rule.py`), running `ruff` and `mypy`, configuring privacy-safe Git email via `gh api user`, and committing locally without pushing.

#### Intent

Update Phase 0 contract documentation for the `c1` hardening rules, run all focused validation commands with `TMPDIR=/dev/shm`, and create a clean local Conventional Commit (`Refs #124` + Copilot trailer) ready for `rpi-review`.

#### Boundaries

* Included: Concise updates to `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and `docs/reference/log.md`; focused validation commands; local Git commit.
* Excluded: Any `.copilot-tracking/` references in production code, docs, or commit messages; `git push`; `gh pr create`.

#### Likely Targets

* `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`
* `src/core/README.md`
* `docs/reference/log.md`

#### Dependencies

* `P02-T01`.

#### Validation Expectations

* `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_discovery*.py' -v` (or via `~/.cache/zf-124-venv/bin/python` if `test_discovery_assistant_demo.py` requires installed `zava_forward.core`)
* `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_live_doc_links.py src/core/tests/test_dependency_rule.py -v`
* `cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && mypy`

#### Completion Evidence

* Clean focused validation receipts recorded in `.copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-c1-changes.md` and clean local Git commit on `feat/gov-124-phase0-discovery`.

#### Unresolved Items

* None.
