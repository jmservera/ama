<!-- markdownlint-disable-file -->
# RPI Plan Critique: Phase 0 Retrofit-Flow Discovery Contract c3 Final Provenance & Dictionary Binding (Issue #124)

## Metadata

* Task ID: issue-124-c3
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c3-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Close `c2` review defects `RV-001`–`RV-005` on `feat/gov-124-phase0-discovery`, pass the focused validation tier (`TMPDIR=/dev/shm`), commit locally (`Refs #124` + Copilot trailer, no push), and achieve an adversarially verified `Conformant` review verdict.
* Research and evidence considered: `.copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c2-review.md`, `.copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md`, `src/core/src/zava_forward/core/discovery_contract.py`, `src/core/tests/test_discovery_contract.py`.
* Decisions, dependencies, and acceptance criteria considered: `FR-C3-1`–`FR-C3-5`, `NFR-C3-1`–`NFR-C3-2`, `AC-C3-1`–`AC-C3-5`.
* Assessment boundary: Read-only credibility review of `c3` plan and phase details against `discovery_contract.py` and `test_discovery_contract.py`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `FR-C3-1` / `P01-T01` (`RV-001`) | Partial | Needs explicit cross-check between `Phase0DiscoveryPack.dictionary` and caller-supplied `dictionary` in `enforce_governance_guard`, plus candidate-mode dictionary check when `dictionary is not None` (`PC-001`, `PC-002`). |
| `FR-C3-2` / `P01-T01` (`RV-002`) | Covered | `Phase0DiscoveryPack.__post_init__` enforces signer equality across pack and all three sub-artifacts. |
| `FR-C3-3` / `P01-T01` (`RV-004`) | Partial | Expand `_VALIDATED_FLOW_REPORT_SEALS` to include `dictionary_schema_digest` and keep `__deepcopy__` `ContextVar` window tight (`PC-003`). |
| `FR-C3-4` / `P01-T01` (`RV-003`) | Covered | Deterministic 21-field `calculation_digest` + `dictionary_schema_digest` verification works across fresh subprocesses. |
| `FR-C3-5` / `P02` (`RV-005`, tests & validation) | Covered | `<= 5` test ceiling (`0` removals) and focused `TMPDIR=/dev/shm` commands match caller instructions. |

## Verdict

* Verdict: Revise
* Rationale: Three direct planner tightenings (`PC-001`–`PC-003`) close cross-pack `dictionary` swap and candidate-mode `dictionary` verification edge cases before implementation.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: `enforce_governance_guard` on `Phase0DiscoveryPack` does not compare `pack.dictionary` against caller-supplied `dictionary`

* Related IDs: `FR-C3-1`, `FR-C3-2`, `P01-T01`, `AC-C3-1`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`enforce_governance_guard` `Phase0DiscoveryPack` branch)
* Concern: If a caller validates `pack` against `dictionary_a` and calls `enforce_governance_guard(pack, discovery_owner=owner, dictionary=dictionary_b)`, checking `pack.flow_report` only against `pack.dictionary` would miss a mismatch between `pack.dictionary` and `dictionary_b` (or open gaps in `pack.dictionary`).
* Impact: Could allow a validated `Phase0DiscoveryPack` built under a different `LifecycleDictionary` to pass `enforce_governance_guard(..., dictionary=expected_dictionary)`.
* Smallest useful change: Require `not lifecycle_dictionary_gaps(output.dictionary)` and `_dictionary_schema_digest(output.dictionary) == _dictionary_schema_digest(dictionary)` (plus sub-artifact signer equality) inside `enforce_governance_guard` whenever `output` is a `Phase0DiscoveryPack` and `dictionary is not None`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` in `phase0-retrofit-flow-discovery-124-c3-plan.md` and `phase0-retrofit-flow-discovery-124-c3-phase-details.md`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Candidate (`owner_validated=False`) outputs skip `dictionary` compatibility when `dictionary` is explicitly supplied, and `LifecycleDictionaryReport` validation allows blank `dictionary_schema_digest`

* Related IDs: `FR-C3-1`, `P01-T01`, `AC-C3-1`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`enforce_governance_guard` early `if not owner_val: return`, `validate_lifecycle_report`)
* Concern: Returning before checking `dictionary` when `owner_val=False` skips `_verify_report_matches_dictionary(output, dictionary)` when a caller explicitly supplies `dictionary`, and allowing blank `report.dictionary_schema_digest` in `validate_lifecycle_report` weakens dictionary-report binding.
* Impact: Weakens dictionary binding for candidate checks and `LifecycleDictionaryReport` promotion.
* Smallest useful change: Run `_verify_report_matches_dictionary` before `if not owner_val:` whenever `dictionary is not None` on `FlowDiscoveryReport`, `Phase0DiscoveryPack`, and flow-report `Mapping`s, and require non-blank `report.dictionary_schema_digest == _dictionary_schema_digest(dictionary)` in `validate_lifecycle_report`, `Phase0DiscoveryPack.__post_init__` (`owner_validated=True`), and `enforce_governance_guard` (`LifecycleDictionaryReport` when `owner_validated=True`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-C3-1` and `P01-T01` details.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: Bind `dictionary_schema_digest` inside `_VALIDATED_FLOW_REPORT_SEALS` and scope `__deepcopy__` `ContextVar` reset tightly

* Related IDs: `FR-C3-1`, `FR-C3-3`, `P01-T01`
* Evidence: `phase0-retrofit-flow-discovery-124-c3-phase-details.md` (`P01-T01`)
* Concern: Including `dictionary_schema_digest` explicitly inside `_VALIDATED_FLOW_REPORT_SEALS` `(calculation_digest, dictionary_schema_digest, actor, on_iso, note)` and evaluating deep-copied field values prior to entering `_ALLOW_VALIDATED_FLOW_REPORT_INIT.set(True)` avoids leaking the `ContextVar` into nested `__deepcopy__` hooks.
* Impact: Prevents subtle `ContextVar` scope leakage and binds seals explicitly to dictionary schema.
* Smallest useful change: Store 5-tuples in `_VALIDATED_FLOW_REPORT_SEALS` and set `_ALLOW_VALIDATED_FLOW_REPORT_INIT` only around the `FlowDiscoveryReport(...)` constructor call inside `__deepcopy__`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` details.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Separating in-process dataclass construction provenance (`_is_evaluated_report_instance` + `_ALLOW_VALIDATED_FLOW_REPORT_INIT` + `_VALIDATED_FLOW_REPORT_SEALS`) from deterministic cross-process 21-field SHA-256 + `dictionary_schema_digest` `Mapping` verification cleanly resolves both `RV-003` and `RV-004` without non-stdlib dependencies.

## Questions or Blocking Evidence Gaps

* none

## Limitations

* Focused validation tier only per caller constraint.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: planning_parent
* Smallest next action: Apply `PC-001`–`PC-003` directly to `c3` plan and phase details, mark `Planning status: ready`, and proceed to `rpi-implement`.
* User response required: no
