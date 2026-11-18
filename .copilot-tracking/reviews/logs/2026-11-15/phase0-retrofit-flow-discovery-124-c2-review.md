<!-- markdownlint-disable-file -->
# Review: Phase 0 Retrofit-Flow Discovery Contract c2 Hardening (Issue #124)

## Scope and Evidence

* Task ID: issue-124-c2
* Review date: 2026-11-15
* Review scope: Full task (`P01` and `P02` of `phase0-retrofit-flow-discovery-124-c2`, together with verification that original Issue #124 `RV-001`–`RV-003` and `c1` `RV-001`–`RV-005` are resolved on `feat/gov-124-phase0-discovery` at `b7c91e832`)
* Assessed boundary: Requirements `FR-C2-1`–`FR-C2-4`, `NFR-C2-1`–`NFR-C2-2`, acceptance criteria `AC-C2-1`–`AC-C2-5`, critique items `PC-001`–`PC-003`, prior review defects (`phase0-retrofit-flow-discovery-124-review.md` `RV-001`–`RV-003` and `phase0-retrofit-flow-discovery-124-c1-review.md` `RV-001`–`RV-005`), code and test changes in `src/core/src/zava_forward/core/discovery_contract.py` and `src/core/tests/test_discovery_contract.py`, coupled Phase 0 documentation, and focused validation evidence.
* Plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c2-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-c2-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md (`reused`), .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md, .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c1-review.md, commit `b7c91e832`, focused validation suite output, and independent read-only adversarial lens (`c2-adversarial-lens`).

## Opening Review State

* Interpreted review goal: Perform one evidence-grounded, read-only post-implementation review of `issue-124-c2` verifying complete closure of original `RV-001`–`RV-003`, `c1` `RV-001`–`RV-005`, and `c2` `PC-001`–`PC-003` across `discovery_contract.py`, `test_discovery_contract.py`, and coupled Phase 0 documentation.
* Review scope: Full task (`P01`, `P02`)
* Evidence readiness: Ready (plan, phase details, single critique, changes record, prior reviews, research synthesis, committed implementation `b7c91e832`, and focused validation results all available and reconciled)
* Acceptance basis: `FR-C2-1`–`FR-C2-4`, `NFR-C2-1`–`NFR-C2-2`, `AC-C2-1`–`AC-C2-5`, `PC-001`–`PC-003`, and original Issue #124 remediation scope (`RV-001`–`RV-003`)
* First comparison boundary: Plan-to-change reconciliation and adversarial verification of provenance/seal invariants, `FrozenDict` immutability, `Mapping` guard parity, and timestamp cutoff rules in `src/core/src/zava_forward/core/discovery_contract.py`
* Active read-only boundaries: Read-only across source code, tests, docs, research, plan, details, critique, and changes; write authority restricted solely to this canonical review log
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full-boundary comparison and independent read-only adversarial verification (`c2-adversarial-lens`) on 2026-11-15 against commit `b7c91e832`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Discovery Contract Provenance, Mapping Parity, `FrozenDict`, and Cutoff Bounds | Reconciled | Implemented in `src/core/src/zava_forward/core/discovery_contract.py`; `c1` `RV-004`/`RV-005` and `Mapping` 20-key digest checks work, while four residual provenance/dictionary/signer edge cases remain (`RV-001`–`RV-004`). |
| `P02` (`P02-T01`, `P02-T02`) | Adversarial Regression Tests, Documentation Sync, and Focused Validation | Reconciled | 4 regression tests added (`29` total in `test_discovery_contract.py`, `98` across `test_discovery*.py`); docs updated (`RV-005` narrows `FrozenDict` prose). |
| `## Follow-Up Items` | Optional CSV extract adapter | Reconciled | Preserved distinctly outside Phase 0 rule-layer scope. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/discovery_contract.py` | Locked `FrozenDict.__init__`/attributes, added weakref + seal provenance, `to_json_dict()`, and 20-key `Mapping` guard | Commit `b7c91e832` | `98` `test_discovery*.py` tests, `ruff`, `mypy` passed | Gap (`RV-001`–`RV-005` surfaced by adversarial lens) |
| `P01-T02` | `src/core/src/zava_forward/core/discovery_contract.py` | Ordered post-`as_of` active-work check ahead of incomplete-pair skip and compared `window_end` by UTC calendar date | Commit `b7c91e832` | Verified by `test_flow_excludes_incomplete_post_as_of_active_work_and_keeps_window_end_microseconds` | Reconciled |
| `P02-T01` | `src/core/tests/test_discovery_contract.py` | Added 4 focused regression tests (`0` removals) | Commit `b7c91e832` | `Ran 98 tests in 0.219s — OK` | Reconciled |
| `P02-T02` | `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md` | Synced Phase 0 contract docs and ran focused validation | Commit `b7c91e832` | `test_live_doc_links.py` & `test_dependency_rule.py` (`4` tests) passed | Gap (`RV-005` prose overstates `dict` subclass immutability against `dict.__setitem__`) |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` / `FR-C2-1` | Used `_EVALUATED_FLOW_REPORT_REFS` weakref map instead of private dataclass field so `dataclasses.asdict()` stays clean | Local implementation judgment preserving existing `asdict` tests | Synchronized in `c2-plan.md`, `c2-phase-details.md`, and `c2-changes.md` | `PC-001`–`PC-003` resolved; no planning change required | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001`, `PC-002`, and `PC-003` from `.copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c2-plan-critique.md` were applied before source edits.
* Material revisions: None during `c2` implementation.
* Dependent-work pause assessment: No early resumption occurred.
* Justification assessment: Weakref provenance tracking preserved `asdict()`, though adversarial testing exposed dictionary binding, pack signer equality, cross-process JSON verification, and post-sign-off `replace` seal replay gaps (`RV-001`–`RV-004`).

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Optional CSV extract adapter for synthetic year-one CSVs | Phase 0 contract is a pure stdlib rule layer | Future discovery data-pipeline task | Open distinct follow-up (non-defect) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: `evaluate_property_flow` dictionary schema is not bound to `validate_flow_report`, `Phase0DiscoveryPack`, or `enforce_governance_guard`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`evaluate_property_flow`, `validate_flow_report`, `Phase0DiscoveryPack.__post_init__`, `enforce_governance_guard`)
* Impact: A `FlowDiscoveryReport` evaluated against an unapproved or altered `LifecycleDictionary` (for example containing an extra `UNAPPROVED` stage) can be signed via `validate_flow_report` and accepted by `Phase0DiscoveryPack` and `enforce_governance_guard` using a different validated `LifecycleDictionary` that lacks that stage.
* Destination: `rpi-implement`
* Smallest useful next action: Record deterministic `dictionary_schema_digest` on `FlowDiscoveryReport` (included in `calculation_digest` and `to_json_dict()`) and verify schema digest equality plus stage/party/loop membership against `dictionary` in `validate_flow_report`, `Phase0DiscoveryPack.__post_init__`, and `enforce_governance_guard`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: `Phase0DiscoveryPack.__post_init__` accepts mismatched sub-artifact signers

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`Phase0DiscoveryPack.__post_init__`)
* Impact: `Phase0DiscoveryPack` checks `self.owner_validated_by == self.discovery_owner.owner` on the pack itself without checking `dictionary_report.owner_validated_by`, `flow_report.owner_validated_by`, or `constraint_register.owner_validated_by` against `discovery_owner.owner` (which `enforce_governance_guard` later rejects).
* Destination: `rpi-implement`
* Smallest useful next action: Enforce `owner_validated_by.strip() == self.discovery_owner.owner.strip()` across `dictionary_report`, `flow_report`, and `constraint_register` (plus `dictionary_report` / `dictionary` parity) inside `Phase0DiscoveryPack.__post_init__`.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Serialized `Mapping` guard depends on process-local memory registries and fails valid JSON round-trips in a fresh Python process

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`_verify_flow_report_mapping`)
* Impact: Requiring `_EVALUATED_FLOW_REPORT_DIGESTS` and `_VALIDATED_FLOW_REPORT_SEALS` membership inside `_verify_flow_report_mapping` rejects a genuine `json.loads(json.dumps(validated.to_json_dict()))` payload whenever `enforce_governance_guard` runs in a separate process whose in-memory sets are empty.
* Destination: `rpi-implement`
* Smallest useful next action: Keep strict in-process evaluation and construction provenance on `FlowDiscoveryReport` / `validate_flow_report` / `Phase0DiscoveryPack` while verifying deserialized `Mapping` payloads deterministically via full 21-field `calculation_digest`, `dictionary_schema_digest == _dictionary_schema_digest(dictionary)`, `discovery_owner` readiness, signer equality, zero gaps, and zero invalid handovers across process boundaries, and document the boundary clearly.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: External `dataclasses.replace(..., owner_validated=True)` can replay an existing in-process validation seal onto another report instance

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`FlowDiscoveryReport.__post_init__`, `validate_flow_report`)
* Impact: Once a clean report is signed in-process, `FlowDiscoveryReport.__post_init__` permits external `dataclasses.replace(gapped_report, gaps=(), owner_validated=True, ..., calculation_digest=clean_report.calculation_digest)` calls because `(digest, by, on, note)` is present in `_VALIDATED_FLOW_REPORT_SEALS`, bypassing `validate_flow_report` lineage checks.
* Destination: `rpi-implement`
* Smallest useful next action: Gate `FlowDiscoveryReport(..., owner_validated=True)` construction on a module-private `ContextVar[bool]` active only inside `validate_flow_report` and `FlowDiscoveryReport.__deepcopy__` so external `FlowDiscoveryReport` / `dataclasses.replace` calls can never mint `owner_validated=True` instances.

<!-- rpi:review id=RV-005 -->
### RV-005 [Low]: `FrozenDict` documentation overstates `dict` subclass immutability against `dict.__setitem__`

* Related scope: `P02-T02`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py`, `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`
* Impact: Because `FrozenDict` subclasses `dict` to preserve `dataclasses.asdict()` / `json.dumps()` behavior, calling `dict.__setitem__(report.state_counts, ...)` directly mutates the backing `PyDictObject` until `verify_digest()` rejects it at validation/governance boundaries; calling it "strictly immutable" without noting the `dict` base bypass is imprecise.
* Destination: `rpi-implement`
* Smallest useful next action: Clarify in `FrozenDict` docstring and Phase 0 docs that `FrozenDict` subclasses `dict` for `asdict()`/JSON compatibility, blocks standard `Mapping` item/attribute mutation and re-initialization, and relies on `verify_digest()` to detect low-level `dict.__setitem__` tampering.

## Defects

* `RV-001` [High] -> `rpi-implement`
* `RV-002` [Medium] -> `rpi-implement`
* `RV-003` [Medium] -> `rpi-implement`
* `RV-004` [Medium] -> `rpi-implement`
* `RV-005` [Low] -> `rpi-implement`

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Child task `issue-124-c3` | Bind `dictionary_schema_digest` between `evaluate_property_flow`, `validate_flow_report`, `Phase0DiscoveryPack`, and `enforce_governance_guard`. |
| `RV-002` | `rpi-implement` | Child task `issue-124-c3` | Enforce sub-artifact signer and dictionary report parity in `Phase0DiscoveryPack.__post_init__`. |
| `RV-003` | `rpi-implement` | Child task `issue-124-c3` | Make deserialized `Mapping` digest + dictionary schema verification work across fresh Python processes. |
| `RV-004` | `rpi-implement` | Child task `issue-124-c3` | Gate `owner_validated=True` `FlowDiscoveryReport` construction via `ContextVar` to `validate_flow_report` and `__deepcopy__`. |
| `RV-005` | `rpi-implement` | Child task `issue-124-c3` | Align `FrozenDict` docstring and Phase 0 Markdown claims with `dict` subclass + `verify_digest()` semantics. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Optional CSV extract adapter mapping `support/synthetic-data/retrofit-flow/zava-forward-year-one/` tables into `discovery_contract` dataclasses (distinct non-blocking follow-up outside Phase 0 rule-layer scope).

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none inside `issue-124-c2` (`P01` and `P02` completed; `RV-001`–`RV-005` routed to child remediation loop `issue-124-c3`).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PATH="/dev/shm/zf-124-c1-venv/bin:$PATH" TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_discovery*.py' -v` | `src/core/tests/test_discovery*.py` | Passed | `Ran 98 tests in 0.219s — OK` |
| `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_live_doc_links.py src/core/tests/test_dependency_rule.py -v` | Live doc links & core import boundaries | Passed | `Ran 4 tests in 3.499s — OK` |
| `cd src/core && TMPDIR=/dev/shm python3 -m ruff check . && TMPDIR=/dev/shm python3 -m ruff format --check . && TMPDIR=/dev/shm mypy` | `src/core` lint, format, strict typing | Passed | `All checks passed!`, `310 files already formatted`, `Success: no issues found in 363 source files` |

## Outcome

* Outcome: Defects found
* Outcome rationale: `c1` `RV-004`, `RV-005`, `FrozenDict.__init__` re-init locking, and 20-key `Mapping` signature detection work as intended, but adversarial testing uncovered four cross-boundary provenance/consistency defects (`RV-001`–`RV-004`) and one documentation precision item (`RV-005`).

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | Resolve `RV-001`–`RV-005` in child automatic RPI task `issue-124-c3` |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Optional CSV extract adapter (deferred outside Phase 0 rule-layer scope) |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: 98 `test_discovery*.py` tests, 4 doc-link/dependency tests, `ruff check .`, `ruff format --check .`, and `mypy` all passed (`TMPDIR=/dev/shm`)
* Blockers: none
