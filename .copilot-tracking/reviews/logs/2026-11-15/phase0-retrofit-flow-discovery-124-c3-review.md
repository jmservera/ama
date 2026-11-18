<!-- markdownlint-disable-file -->
# Review: Phase 0 Retrofit-Flow Discovery Contract c3 Final Provenance & Dictionary Binding (Issue #124)

## Scope and Evidence

* Task ID: issue-124-c3
* Review date: 2026-11-15
* Review scope: Full task (`P01` and `P02` of `phase0-retrofit-flow-discovery-124-c3`, together with end-to-end verification that original Issue #124 `RV-001`–`RV-003`, `c1` `RV-001`–`RV-005`, `c2` `RV-001`–`RV-005`, and `c3` `PC-001`–`PC-003` are resolved on `feat/gov-124-phase0-discovery` at `b6e918142`)
* Assessed boundary: Requirements `FR-C3-1`–`FR-C3-5`, `NFR-C3-1`–`NFR-C3-2`, acceptance criteria `AC-C3-1`–`AC-C3-5`, critique items `PC-001`–`PC-003`, prior review logs (`phase0-retrofit-flow-discovery-124-review.md`, `phase0-retrofit-flow-discovery-124-c1-review.md`, `phase0-retrofit-flow-discovery-124-c2-review.md`), code and test changes in `src/core/src/zava_forward/core/discovery_contract.py` and `src/core/tests/test_discovery_contract.py`, coupled Phase 0 documentation, and focused validation evidence.
* Plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c3-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c3-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-c3-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md (`reused`), .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md, .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c1-review.md, .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c2-review.md, commit `b6e918142`, focused validation suite output, and independent read-only adversarial lens (`c3-adversarial-lens`).

## Opening Review State

* Interpreted review goal: Perform one evidence-grounded, read-only post-implementation review of `issue-124-c3` verifying complete closure of original `RV-001`–`RV-003`, `c1` `RV-001`–`RV-005`, `c2` `RV-001`–`RV-005`, and `c3` `PC-001`–`PC-003` across `discovery_contract.py`, `test_discovery_contract.py`, and coupled Phase 0 documentation.
* Review scope: Full task (`P01`, `P02`)
* Evidence readiness: Ready (plan, phase details, single critique, changes record, prior reviews, research synthesis, committed implementation `b6e918142`, and focused validation results all available and reconciled)
* Acceptance basis: `FR-C3-1`–`FR-C3-5`, `NFR-C3-1`–`NFR-C3-2`, `AC-C3-1`–`AC-C3-5`, `PC-001`–`PC-003`, and original Issue #124 remediation scope (`RV-001`–`RV-003`)
* First comparison boundary: Plan-to-change reconciliation and independent adversarial verification of `dictionary_schema_digest` binding, `Phase0DiscoveryPack` signer parity, `_ALLOW_VALIDATED_FLOW_REPORT_INIT` construction gating, cross-process `Mapping` verification, and documentation precision.
* Active read-only boundaries: Read-only across source code, tests, docs, research, plan, details, critique, and changes; write authority restricted solely to this canonical review log.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full-boundary comparison and independent read-only adversarial verification (`c3-adversarial-lens`) on 2026-11-15 against commit `b6e918142`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`) | Dictionary Schema Binding, Pack Signer Parity, `ContextVar` Seal Gate, and Cross-Process Mapping Verification | Reconciled | Implemented in `src/core/src/zava_forward/core/discovery_contract.py`; `deepcopy`, `ContextVar` reset, and dataclass `Phase0DiscoveryPack` signer parity hold, while five `Mapping` / dictionary-extension edge cases remain (`RV-001`–`RV-005`). |
| `P02` (`P02-T01`, `P02-T02`) | Adversarial Regression Tests, Documentation Precision, and Focused Validation | Reconciled | 4 regression tests added (`33` total in `test_discovery_contract.py`, `102` across `test_discovery*.py`); Phase 0 docs updated cleanly (`RV-006` narrows historical repo-wide `.copilot-tracking/` phrasing to branch diff). |
| `## Follow-Up Items` | Optional CSV extract adapter | Reconciled | Preserved distinctly outside Phase 0 rule-layer scope. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/discovery_contract.py` | Added `_dictionary_schema_digest`, `Phase0DiscoveryPack` signer checks, `_ALLOW_VALIDATED_FLOW_REPORT_INIT`, and `_verify_flow_report_mapping` updates | Commit `b6e918142` | `102` `test_discovery*.py` tests, `ruff`, `mypy` passed | Gap (`RV-001`–`RV-005` surfaced by `c3-adversarial-lens`) |
| `P02-T01` | `src/core/tests/test_discovery_contract.py` | Added 4 focused regression tests including subprocess JSON round-trip | Commit `b6e918142` | `Ran 102 tests in 0.289s — OK` | Reconciled |
| `P02-T02` | `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md` | Clarified `FrozenDict` `dict`-subclass + `verify_digest()` semantics and `dictionary_schema_digest` | Commit `b6e918142` | `test_live_doc_links.py` & `test_dependency_rule.py` (`4` tests) passed | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` | Added candidate sub-report recursion on `dictionary_report` and `constraint_register` in `enforce_governance_guard` | Local hardening during implementation | Recorded in `c3-changes.md` | `PC-001`–`PC-003` resolved | Gap (`RV-002`: validated pack `Mapping` branch did not enforce `owner_validated=True` and signer/adjudication parity on sub-artifacts) |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001`, `PC-002`, and `PC-003` from `.copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c3-plan-critique.md` were applied before source edits.
* Material revisions: None during `c3` implementation.
* Dependent-work pause assessment: No early resumption occurred.
* Justification assessment: `ContextVar` seal gating and dataclass signer/dictionary parity work as intended, while `c3-adversarial-lens` exposed unkeyed `Mapping` sign-off forgery, validated pack `Mapping` candidate sub-artifacts, `_is_flow_report_mapping` collision on `dictionary_schema_digest`, blank candidate `LifecycleDictionaryReport` digest, and unvalidated `LifecycleDictionary` extension items (`RV-001`–`RV-005`).

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Optional CSV extract adapter for synthetic year-one CSVs | Phase 0 contract is a pure stdlib rule layer | Future discovery data-pipeline task | Open distinct follow-up (non-defect) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Unkeyed JSON `Mapping` verification allows forging `owner_validated=True` or recomputing `calculation_digest` without `validate_flow_report`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`_verify_flow_report_mapping`, `to_json_dict`)
* Impact: Removing `_EVALUATED_FLOW_REPORT_DIGESTS` / `_VALIDATED_FLOW_REPORT_SEALS` checks from `_verify_flow_report_mapping` allows a caller to take `candidate.to_json_dict()`, set `owner_validated=True` + sign-off fields (or mutate metrics and recompute `_compute_flow_report_digest`), and pass `enforce_governance_guard` without calling `validate_flow_report`.
* Destination: `rpi-implement`
* Smallest useful next action: Enforce `_EVALUATED_FLOW_REPORT_DIGESTS` and 5-tuple `_VALIDATED_FLOW_REPORT_SEALS` for unkeyed in-process `Mapping`s (`signing_key=None`), and support cross-process JSON verification via stdlib `hmac` (`to_json_dict(*, signing_key=...)` + `enforce_governance_guard(..., signing_key=...)`) authenticating both `calculation_digest` and sign-off fields only from verified evaluated/sealed `FlowDiscoveryReport` instances.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Validated pack `Mapping`s accept candidate `dictionary_report` and `constraint_register` sub-artifacts

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`enforce_governance_guard`)
* Impact: When an outer pack `Mapping` claims `owner_validated=True`, nested `dictionary_report` and `constraint_register` items are checked independently as candidates rather than requiring `owner_validated=True`, matching nominated-owner sign-off, schema parity, and adjudicated hypotheses.
* Destination: `rpi-implement`
* Smallest useful next action: Enforce full sub-artifact validation, nominated-owner signer equality, dictionary schema parity, and adjudicated hypothesis verification across `LifecycleDictionaryReport`, `RankedConstraintRegister`, `ConstraintHypothesis`, and `Phase0DiscoveryPack` `Mapping` representations whenever `owner_validated=True`.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: `lifecycle_dictionary_gaps` ignores unvalidated extension entries appended to `LifecycleDictionary`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`lifecycle_dictionary_gaps`)
* Impact: Appending an unvalidated exception `StageSpec` (or extension event/timestamp/wait/loop) to an otherwise validated `LifecycleDictionary` yields `lifecycle_dictionary_gaps(d) == []`, allowing unvalidated extension items to pass `validate_flow_report` and `enforce_governance_guard`.
* Destination: `rpi-implement`
* Smallest useful next action: Check every entry in `dictionary.stages`, `dictionary.events`, `dictionary.timestamps`, `dictionary.wait_states`, and `dictionary.return_loops` (including extensions beyond the required sets) for `is_validated` and cross-reference consistency inside `lifecycle_dictionary_gaps`.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: `_FLOW_REPORT_SIGNATURE_KEYS` includes shared `dictionary_schema_digest`, misclassifying `LifecycleDictionaryReport` mappings as flow reports

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`_FLOW_REPORT_SIGNATURE_KEYS`, `_is_flow_report_mapping`)
* Impact: Passing `dataclasses.asdict(summarize_lifecycle_dictionary(dictionary))` to `enforce_governance_guard` triggers `_verify_flow_report_mapping` and raises a spurious missing-`calculation_digest` error.
* Destination: `rpi-implement`
* Smallest useful next action: Exclude `"dictionary_schema_digest"` from `_FLOW_REPORT_SIGNATURE_KEYS` and verify `LifecycleDictionaryReport` mappings with a dedicated `_is_lifecycle_report_mapping` / `_verify_lifecycle_report_mapping` helper.

<!-- rpi:review id=RV-005 -->
### RV-005 [Medium]: Blank `dictionary_schema_digest` on candidate `LifecycleDictionaryReport` bypasses dictionary binding

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`Phase0DiscoveryPack.__post_init__`, `enforce_governance_guard`)
* Impact: Setting `dictionary_schema_digest=""` on a candidate `LifecycleDictionaryReport` skips digest comparison against `Phase0DiscoveryPack.dictionary` and `enforce_governance_guard(..., dictionary=d)`.
* Destination: `rpi-implement`
* Smallest useful next action: Require non-blank `dictionary_schema_digest == _dictionary_schema_digest(dictionary)` unconditionally whenever a `LifecycleDictionary` is present (`Phase0DiscoveryPack.__post_init__`, `validate_lifecycle_report`, and `enforce_governance_guard` in both candidate and validated modes).

## Defects

* `RV-001` [High] -> `rpi-implement`
* `RV-002` [High] -> `rpi-implement`
* `RV-003` [High] -> `rpi-implement`
* `RV-004` [Medium] -> `rpi-implement`
* `RV-005` [Medium] -> `rpi-implement`

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Child task `issue-124-c4` | Enforce in-process provenance for unkeyed `Mapping`s and stdlib `hmac` (`signing_key`) for cross-process JSON verification. |
| `RV-002` | `rpi-implement` | Child task `issue-124-c4` | Enforce validated sub-artifact signer/schema/hypothesis parity on pack, register, hypothesis, and lifecycle `Mapping`s. |
| `RV-003` | `rpi-implement` | Child task `issue-124-c4` | Validate all extension specs in `lifecycle_dictionary_gaps`. |
| `RV-004` | `rpi-implement` | Child task `issue-124-c4` | Remove `dictionary_schema_digest` from `_FLOW_REPORT_SIGNATURE_KEYS` and classify lifecycle report mappings distinctly. |
| `RV-005` | `rpi-implement` | Child task `issue-124-c4` | Reject blank `dictionary_schema_digest` whenever compared against a `LifecycleDictionary`. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Optional CSV extract adapter mapping `support/synthetic-data/retrofit-flow/zava-forward-year-one/` tables into `discovery_contract` dataclasses (distinct non-blocking follow-up outside Phase 0 rule-layer scope).

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none inside `issue-124-c3` (`P01` and `P02` completed; `RV-001`–`RV-005` routed to child remediation loop `issue-124-c4`).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PATH="/dev/shm/zf-124-c1-venv/bin:$PATH" TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_discovery*.py' -v` | `src/core/tests/test_discovery*.py` | Passed | `Ran 102 tests in 0.289s — OK` |
| `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_live_doc_links.py src/core/tests/test_dependency_rule.py -v` | Live doc links & core import boundaries | Passed | `Ran 4 tests in 3.270s — OK` |
| `cd src/core && TMPDIR=/dev/shm python3 -m ruff check . && TMPDIR=/dev/shm python3 -m ruff format --check . && TMPDIR=/dev/shm mypy` | `src/core` lint, format, strict typing | Passed | `All checks passed!`, `310 files already formatted`, `Success: no issues found in 363 source files` |

## Outcome

* Outcome: Defects found
* Outcome rationale: Dataclass `dictionary_schema_digest` binding, `Phase0DiscoveryPack` signer parity, `ContextVar` seal-replay prevention, and `copy.deepcopy` preservation all hold, while adversarial verification surfaced five `Mapping` / dictionary-extension gaps (`RV-001`–`RV-005`).

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | Resolve `RV-001`–`RV-005` in child automatic RPI task `issue-124-c4` |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Optional CSV extract adapter (deferred outside Phase 0 rule-layer scope) |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: 102 `test_discovery*.py` tests, 4 doc-link/dependency tests, `ruff check .`, `ruff format --check .`, and `mypy` all passed (`TMPDIR=/dev/shm`)
* Blockers: none
