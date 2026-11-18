<!-- markdownlint-disable-file -->
# RPI Changes: Phase 0 Retrofit-Flow Discovery Contract c3 Final Provenance & Dictionary Binding (Issue #124)

## Metadata

* Task ID: issue-124-c3
* Related plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c3-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: none
* Status basis: All planned `c3` changes, 4 new regression tests (`33` total in `test_discovery_contract.py`, `102` across `test_discovery*.py`), Phase 0 documentation updates, and focused validation checks passed cleanly.

## Execution Summary

Implemented `c3` provenance, dictionary-binding, signer-parity, and cross-process JSON verification across `src/core/src/zava_forward/core/discovery_contract.py`, `src/core/tests/test_discovery_contract.py`, and Phase 0 contract documentation (`docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md`), resolving `c2` review findings `RV-001`–`RV-005` and `c3` critique tightenings `PC-001`–`PC-003`.

## Completed Work

* `P01-T01` (`src/core/src/zava_forward/core/discovery_contract.py`):
  * Added `_dictionary_schema_digest(dictionary)` and `_verify_report_matches_dictionary(report_or_mapping, dictionary)` binding both `LifecycleDictionaryReport` and `FlowDiscoveryReport` (21-field `calculation_digest` including `dictionary_schema_digest`) to the exact `LifecycleDictionary` structural schema across `evaluate_property_flow`, `validate_flow_report`, `validate_lifecycle_report`, `Phase0DiscoveryPack`, and `enforce_governance_guard` (in both candidate and validated modes).
  * Enforced exact nominated-owner signer parity across `dictionary_report`, `flow_report`, `constraint_register`, and non-`DISPUTED` `ConstraintHypothesis` items inside `Phase0DiscoveryPack.__post_init__` and `enforce_governance_guard` (including nested pack `Mapping` sub-reports).
  * Added `_ALLOW_VALIDATED_FLOW_REPORT_INIT` (`ContextVar[bool]`) plus 5-tuple `_VALIDATED_FLOW_REPORT_SEALS` and `FlowDiscoveryReport.__deepcopy__` so external `FlowDiscoveryReport(..., owner_validated=True)` and `dataclasses.replace(..., owner_validated=True)` seal-replay calls fail closed while `copy.deepcopy(validated)` succeeds.
  * Updated `_verify_flow_report_mapping` to verify cross-process `to_json_dict()` JSON round-trip payloads deterministically via 21-field `calculation_digest`, `dictionary_schema_digest` + membership against the supplied zero-gap `LifecycleDictionary`, and human nominated-owner sign-off invariants without requiring process-local memory registries.
  * Narrowed `FrozenDict` docstring to state accurately that it subclasses `dict` for `dataclasses.asdict()` / JSON compatibility while `verify_digest()` catches low-level `dict.__setitem__` tampering.
* `P02-T01` (`src/core/tests/test_discovery_contract.py`):
  * Added 4 focused regression tests (`0` removed, within `<= 5` ceiling; `33` tests in `test_discovery_contract.py`, `102` total across `test_discovery*.py`): `test_dictionary_schema_binding_rejects_mismatched_dictionary_at_validation_and_pack`, `test_pack_rejects_sub_artifact_signer_mismatch_across_owners`, `test_post_signoff_replace_cannot_replay_existing_seal`, and `test_cross_process_json_roundtrip_mapping_passes_guard_and_rejects_tampering` (using a fresh `subprocess.run([sys.executable, "-c", ...])` interpreter).
* `P02-T02` (`docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md`):
  * Updated Phase 0 contract prose and appended a `2026-11-15` knowledge-base log entry with zero `.copilot-tracking/` leaks.

## Implementation-Time Plan and Detail Updates

None (implemented cleanly as specified after `PC-001`–`PC-003` critique disposition, plus pack `Mapping` sub-report recursion in `enforce_governance_guard`).

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `ruff check .` & `ruff format --check .` | `src/core` (`310` files) | Pass | All checks passed; 310 files already formatted |
| `mypy` | `src/core` (`363` files) | Pass | `Success: no issues found in 363 source files` |
| `unittest discover -s src/core/tests -p 'test_discovery*.py' -v` | `src/core/tests` (`102` tests) | Pass | `Ran 102 tests in 0.289s — OK` (`TMPDIR=/dev/shm`) |
| `unittest test_live_doc_links.py test_dependency_rule.py -v` | `src/core/tests` (`4` tests) | Pass | `Ran 4 tests in 3.270s — OK` (`TMPDIR=/dev/shm`) |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02` all checked `[x]`)
* Completed-work evidence and handoff prose: reconciled
* Validation, blockers, remaining work, and follow-up items: reconciled (`0` blockers, `0` remaining active tasks)
* Review readiness: ready for single post-implementation `rpi-review` (`issue-124-c3`)

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c3-plan.md, `## Follow-Up Items`
* Optional CSV extract adapter mapping `support/synthetic-data/retrofit-flow/zava-forward-year-one/` tables into `discovery_contract` dataclasses (deferred outside Phase 0 rule-layer scope).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`, `P02`); completed: `P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`; remaining: none
* Validation coverage: complete focused tier (`102` discovery tests, `4` doc-link/dependency tests, `ruff check`, `ruff format --check`, `mypy`)
* Blockers: none
* Current plan and detail updates: none
* Planning and critique state: ready (`PC-001`, `PC-002`, `PC-003` resolved)
* Follow-up items: optional CSV extract adapter (deferred)
* Review readiness or no-handoff reason: ready for `rpi-review`
* Continuation owner: confirmed automatic RPI Agent (`issue-124-c3`)
