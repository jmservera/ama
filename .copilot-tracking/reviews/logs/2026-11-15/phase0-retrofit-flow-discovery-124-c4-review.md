<!-- markdownlint-disable-file -->
# Review: Phase 0 Retrofit-Flow Discovery Contract c4 Mapping Provenance & Extension Hardening (Issue #124)

## Scope and Evidence

* Task ID: issue-124-c4
* Review date: 2026-11-15
* Review scope: Full task (`P01` and `P02` of `phase0-retrofit-flow-discovery-124-c4`, together with cumulative verification across `c0`–`c4` at commit `5c78777cb` on `feat/gov-124-phase0-discovery`)
* Assessed boundary: Requirements `FR-C4-1`–`FR-C4-4`, `NFR-C4-1`–`NFR-C4-2`, acceptance criteria `AC-C4-1`–`AC-C4-4`, critique dispositions `PC-001`–`PC-004`, prior review logs (`phase0-retrofit-flow-discovery-124-review.md`, `c1`, `c2`, `c3`), code and test changes in `src/core/src/zava_forward/core/discovery_contract.py` and `src/core/tests/test_discovery_contract.py`, coupled Phase 0 documentation, and focused validation output.
* Plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c4-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c4-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c4-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-c4-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md (`reused`), .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c3-review.md, commit `5c78777cb`, focused validation suite (`106` `test_discovery*.py` tests, `4` link/dependency tests, `ruff`, `mypy`), and independent read-only adversarial lens (`c4-adversarial-lens`).

## Opening Review State

* Interpreted review goal: Perform one evidence-based, read-only post-implementation review of `issue-124-c4` verifying closure of `c3` `RV-001`–`RV-005` and `c4` `PC-001`–`PC-004` across `discovery_contract.py`, `test_discovery_contract.py`, and Phase 0 documentation.
* Review scope: Full task (`P01`, `P02`)
* Evidence readiness: Ready
* Acceptance basis: `FR-C4-1`–`FR-C4-4`, `NFR-C4-1`–`NFR-C4-2`, `AC-C4-1`–`AC-C4-4`, `PC-001`–`PC-004`, and original Issue #124 `c1` scope
* First comparison boundary: Plan-to-change reconciliation and adversarial verification of HMAC JSON provenance, 5-shape `Mapping` parity, dictionary extension support, and strict scalar types.
* Active read-only boundaries: Read-only across source code, tests, docs, research, plan, details, critique, and changes; write authority restricted solely to this canonical review log.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full-boundary comparison and independent read-only adversarial verification (`c4-adversarial-lens`) on 2026-11-15 against commit `5c78777cb`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`) | Authenticated JSON Provenance, 5-Shape Mapping Guards, and Dictionary Extension Validation | Reconciled | HMAC-SHA256 `signing_key` cross-process transport, unkeyed mapping provenance, and 5-shape `Mapping` classification work as designed; `c4-adversarial-lens` identified 5 residual object-vs-mapping and dictionary-extension edges (`RV-001`–`RV-005`). |
| `P02` (`P02-T01`, `P02-T02`) | Adversarial Regression Tests, Documentation Sync, and Focused Validation | Reconciled | `4` regression tests added (`37` tests in `test_discovery_contract.py`, `106` across `test_discovery*.py`); Phase 0 docs and `log.md` synchronized cleanly. |
| `## Follow-Up Items` | Optional CSV extract adapter | Reconciled | Preserved distinctly outside Phase 0 rule-layer scope. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/discovery_contract.py` | Added `_compute_flow_report_hmac`, `signing_key` guards, disjoint 5-shape `Mapping` classification/verifiers, non-blank schema digest checks, extension-inclusive `lifecycle_dictionary_gaps`, and `_is_calendar_date` | Commit `5c78777cb` | `106` `test_discovery*.py` tests, `ruff`, `mypy` passed | Gap (`RV-001`–`RV-005` surfaced by `c4-adversarial-lens`) |
| `P02-T01` | `src/core/tests/test_discovery_contract.py` | Updated subprocess JSON test and added 4 focused regression tests | Commit `5c78777cb` | `Ran 106 tests in 0.391s — OK` | Reconciled |
| `P02-T02` | `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md` | Documented `signing_key` cross-process HMAC verification, 5-shape `Mapping` parity, and extension checks | Commit `5c78777cb` | `test_live_doc_links.py` & `test_dependency_rule.py` (`4` tests) passed | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` / `P02-T01` | Added duplicate `stage.order` detection in `lifecycle_dictionary_gaps` and used `replace(base_report)` for untracked-clone HMAC refusal check | Local implementation judgment preserving `FlowDiscoveryReport.__deepcopy__` and seed 49-gap count | Recorded in `c4-changes.md` | `PC-001`–`PC-004` resolved | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001`–`PC-004` from `.copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c4-plan-critique.md` were applied directly before implementation.
* Material revisions: None during `c4` implementation.
* Dependent-work pause assessment: None required.
* Justification assessment: All five `c3` findings (`RV-001`–`RV-005`) are closed on pure `Mapping` paths, while `c4-adversarial-lens` surfaced 5 compact residual parity/extension defects (`RV-001`–`RV-005` below).

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Optional CSV extract adapter for synthetic year-one CSVs | Phase 0 contract is a pure stdlib rule layer | Future discovery data-pipeline task | Open distinct follow-up (non-defect) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Candidate `FlowDiscoveryReport` dataclass and `Phase0DiscoveryPack` skip evaluated provenance checks enforced on `Mapping` inputs

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`Phase0DiscoveryPack.__post_init__`, `enforce_governance_guard`)
* Impact: Directly constructing a candidate `FlowDiscoveryReport(**p)` with tampered `baseline_candidate_ids` and a manually recomputed `calculation_digest` is rejected when serialized to an unkeyed `Mapping`, but passes `enforce_governance_guard(f, dictionary=d)` and candidate `Phase0DiscoveryPack` construction as a dataclass object because `_is_evaluated_report_instance` and `_EVALUATED_FLOW_REPORT_DIGESTS` are only checked on promotion, HMAC signing, or `Mapping` verification.
* Destination: `rpi-implement` — Require `_is_evaluated_report_instance(...)` and `calculation_digest in _EVALUATED_FLOW_REPORT_DIGESTS` on `FlowDiscoveryReport` dataclass instances in `Phase0DiscoveryPack.__post_init__` and `enforce_governance_guard` regardless of `owner_validated`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: `ConstraintTestAssessment` accepts non-boolean truthy integers (`1`) on dataclass and hybrid `Mapping` paths

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`ConstraintTestAssessment`, `_verify_hypothesis_mapping`)
* Impact: `ConstraintTestAssessment(1, 1, 1, 1, 1)` evaluates `passes_all` as `1` (truthy) because `ConstraintTestAssessment` lacks a `__post_init__` `isinstance(..., bool)` guard, bypassing the strict boolean check in `_verify_hypothesis_mapping` when a `ConstraintTestAssessment` instance is passed inside a hypothesis dataclass or mapping.
* Destination: `rpi-implement` — Add `ConstraintTestAssessment.__post_init__` enforcing `isinstance(..., bool)` on all five assessment fields (raising `GovernanceViolationError`) and evaluate `passes_all` with `is True`.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Validated `ReturnLoopSpec` dictionary extension raises `KeyError` in `evaluate_property_flow`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`evaluate_property_flow`)
* Impact: After `c4` enabled full validation of dictionary extensions in `lifecycle_dictionary_gaps`, a zero-gap `LifecycleDictionary` containing a validated extension `ReturnLoopSpec(kind="extra", ...)` raises `KeyError: 'extra'` inside `evaluate_property_flow` because `rework_by_kind`, `loops_by_prop`, and `loop_totals` initialize keys from `REQUIRED_RETURN_LOOP_KINDS` rather than the active dictionary's `return_loops` kinds (and similarly check `state_counts` against extension stages).
* Destination: `rpi-implement` — Initialize return-loop and state-count buckets in `evaluate_property_flow` from `REQUIRED_*` unioned in order with `dictionary.return_loops` / `dictionary.stages` so any validated extension kind or stage aggregates cleanly without `KeyError`.

<!-- rpi:review id=RV-004 -->
### RV-004 [Low]: Candidate `LifecycleDictionaryReport` dataclass and `Mapping` allow non-`accepted handover` `endpoint` or suppressed `gaps`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`LifecycleDictionaryReport.__post_init__`, `_verify_lifecycle_report_mapping`, `enforce_governance_guard`, `Phase0DiscoveryPack.__post_init__`)
* Impact: On candidate (`owner_validated=False`) `LifecycleDictionaryReport` dataclasses and mappings, `endpoint` can be changed from `"accepted handover"` to `"practical completion"` and `gaps` can be cleared to `()` on an unvalidated dictionary without `enforce_governance_guard(..., dictionary=raw)` raising `GovernanceViolationError`.
* Destination: `rpi-implement` — Enforce `endpoint == ENDPOINT` unconditionally on candidate and validated `LifecycleDictionaryReport` dataclasses and mappings, and verify `tuple(gaps) == tuple(lifecycle_dictionary_gaps(dictionary))` whenever `dictionary is not None`.

<!-- rpi:review id=RV-005 -->
### RV-005 [Low]: `StageSpec` constructor accepts `order=True` (`bool` subclass of `int`) in `LifecycleDictionary.__post_init__`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`StageSpec`, `LifecycleDictionary.__post_init__`, `ConstraintHypothesis`, `LifecycleDictionaryReport`)
* Impact: Because `bool` subclasses `int` (`True == 1`), `replace(raw.stages[0], order=True)` satisfies `(s.order, s.code) == (1, 'candidate_identification')` in `LifecycleDictionary.__post_init__` instead of failing closed at construction.
* Destination: `rpi-implement` — Enforce `_is_strict_int` in `StageSpec.__post_init__` (`order >= 1`), `ConstraintHypothesis.__post_init__` (`rank >= 1`), and `LifecycleDictionaryReport.__post_init__` (count fields `>= 0`).

## Validation Assessment

* Validation executed:
  * `cd src/core && python3 -m ruff check .`: `All checks passed!`
  * `cd src/core && python3 -m ruff format --check .`: `310 files already formatted`
  * `cd src/core && python3 -m mypy`: `Success: no issues found in 363 source files`
  * `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_discovery*.py' -v`: `Ran 106 tests in 0.391s — OK`
  * `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_live_doc_links.py src/core/tests/test_dependency_rule.py -v`: `Ran 4 tests in 4.239s — OK`
  * Branch diff tracking-string check (`04e5da42e..HEAD -- src/ docs/`): `0` matches.
* Validation skipped or unavailable: Full 3,730-test `src/core` suite intentionally skipped per focused validation tier instruction.

## Outcome

* Outcome: Defects found
* Severity summary: `0` Critical, `0` High, `3` Medium (`RV-001`–`RV-003`), `2` Low (`RV-004`–`RV-005`)
* Rationale: `c4` resolved all `High` findings from `c3`, including authenticated HMAC cross-process JSON verification and 5-shape `Mapping` classification, leaving 3 `Medium` and 2 `Low` object/mapping parity and extension-evaluation findings (`RV-001`–`RV-005`) requiring one compact child remediation loop (`issue-124-c5`) before recording `Conformant`.

## Recommended Destinations

| Finding or gap | Recommended destination | Why this stage owns the resolution |
|----------------|-------------------------|------------------------------------|
| `RV-001`–`RV-005` | `rpi-implement` (via child automatic RPI loop `issue-124-c5`) | Concrete, localized code and unit-test fixes within established Phase 0 contract architecture requiring zero new requirements or external research. |
| Optional CSV extract adapter | Distinct follow-up item | Non-defect future data-pipeline enhancement outside Phase 0 pure stdlib rule-layer scope. |
