<!-- markdownlint-disable-file -->
# Implementation Changes: Phase 0 Retrofit-Flow Discovery Contract c4 Mapping Provenance & Extension Hardening (Issue #124)

* Task ID: `issue-124-c4`
* Date: `2026-11-15`
* Plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c4-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c4-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c4-plan-critique.md
* Declared scope: Full plan (`P01-T01`, `P02-T01`, `P02-T02`)
* Execution status: `Completed`

## Summary

Completed `P01-T01`, `P02-T01`, and `P02-T02` to close all five `c3` review findings (`RV-001`–`RV-005`) and all four `c4` plan critique corrections (`PC-001`–`PC-004`).

## Task Evidence

### P01-T01: Authenticated JSON Provenance, 5-Shape Mapping Guards, and Dictionary Extension Validation

* Status: `Completed`
* Files modified: `src/core/src/zava_forward/core/discovery_contract.py`
* Evidence:
  * Added `_validate_signing_key` (`>= 16` bytes), `_compute_flow_report_hmac` (8-element canonical JSON array binding `calculation_digest`, `dictionary_schema_digest`, `owner_validated`, `finding_status`, `owner_validated_by`, `owner_validated_on`, `validation_note`, and `notice`), `FlowDiscoveryReport.to_json_dict(*, signing_key=None)`, and `enforce_governance_guard(..., signing_key=None)`, requiring in-process `_EVALUATED_FLOW_REPORT_DIGESTS` / `_VALIDATED_FLOW_REPORT_SEALS` provenance when `signing_key is None` and `hmac.compare_digest` verification when `signing_key` is supplied (`RV-001`, `PC-003`).
  * Added disjoint 5-shape `Mapping` classification (`_classify_discovery_mapping`) rejecting unclassified or multi-shape mappings, strict schema-checked coercers/verifiers for `FlowDiscoveryReport`, `LifecycleDictionaryReport`, `ConstraintHypothesis` (plus candidate `to_rows()` rows), `RankedConstraintRegister`, and `Phase0DiscoveryPack` (including embedded `discovery_owner` and `dictionary`), candidate metadata hygiene (`notice == NOT_FINDING` and blank sign-off fields), and custom `GovernedDiscoveryOutput` rejection on `owner_validated=True` (`RV-002`, `PC-001`, `PC-002`).
  * Required non-blank matching `dictionary_schema_digest` on candidate and validated `LifecycleDictionaryReport` and `Phase0DiscoveryPack` checks (`RV-003`).
  * Reworked `lifecycle_dictionary_gaps` to validate every entry across `stages`, `events`, `timestamps`, `wait_states`, and `return_loops` (including extensions, duplicate codes/orders/event names, stage cross-references, and `allowed_target_stages`) in a single pass after missing-required checks, preserving the exact 49-gap seed count (`RV-004`, `PC-004`).
  * Enforced `_is_calendar_date` (`isinstance(v, date) and not isinstance(v, datetime)`) and `_is_strict_int` across `NominatedDiscoveryOwner`, all five `*Spec` types and `validate_*_spec` helpers, `evaluate_property_flow`, `LifecycleDictionaryReport`, `FlowDiscoveryReport`, `ConstraintHypothesis`, `RankedConstraintRegister`, and `Phase0DiscoveryPack` (`RV-005`, `PC-004`).

### P02-T01: Adversarial Regression Tests in `src/core/tests/test_discovery_contract.py`

* Status: `Completed`
* Files modified: `src/core/tests/test_discovery_contract.py`
* Evidence:
  * Removed `0` existing tests; updated `test_cross_process_json_roundtrip_mapping_passes_guard_and_rejects_tampering` to exercise `signing_key`-authenticated cross-process subprocess verification plus refusal of unkeyed cross-process payloads, wrong keys, short keys, dictionary schema mismatches, tampered payloads, and candidate promotion.
  * Added exactly `4` focused regression tests (`<= 4` budget):
    1. `test_dictionary_gaps_reject_unvalidated_or_duplicate_extensions_and_bad_stage_refs` (`RV-004`, `PC-004`).
    2. `test_unkeyed_forged_flow_mapping_and_tampered_hmac_or_notice_fail_closed` (`RV-001`, `PC-003`).
    3. `test_all_five_mapping_shapes_enforce_schema_parity_and_reject_collisions` (`RV-002`, `PC-001`, `PC-002`).
    4. `test_blank_candidate_schema_digest_and_datetime_masquerading_as_date_rejected` (`RV-003`, `RV-005`, `PC-004`).

### P02-T02: Phase 0 Documentation Sync, Focused Validation, and Local Commit

* Status: `Completed`
* Files modified: `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md`
* Evidence:
  * Updated Phase 0 contract documentation in `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md` and `src/core/README.md` and appended a `2026-11-15` entry in `docs/reference/log.md` covering `signing_key`-authenticated `to_json_dict(signing_key=...)` cross-process HMAC verification, unkeyed in-process provenance checks, disjoint 5-shape `Mapping` parity, non-blank `dictionary_schema_digest` enforcement, and extension-inclusive `lifecycle_dictionary_gaps` checks.

## Discoveries and Plan Updates

* Local judgment: Added duplicate `stage.order` detection (`LifecycleDictionary contains duplicate stage orders`) in `lifecycle_dictionary_gaps` alongside duplicate stage code and event name checks while preserving stage boundary strings on seed stages (`49` default gaps unchanged), and used `dataclasses.replace(base_report)` in `test_unkeyed_forged_flow_mapping_and_tampered_hmac_or_notice_fail_closed` to exercise untracked non-evaluated instance refusal because `FlowDiscoveryReport.__deepcopy__` deliberately preserves provenance on unmodified deep copies.

## Validation

* `cd src/core && python3 -m ruff check .`: `All checks passed!`
* `cd src/core && python3 -m ruff format --check .`: `310 files already formatted`
* `cd src/core && python3 -m mypy`: `Success: no issues found in 363 source files`
* `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_discovery*.py' -v`: `Ran 106 tests in 0.391s — OK`
* `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_live_doc_links.py src/core/tests/test_dependency_rule.py -v`: `Ran 4 tests in 4.239s — OK`
* Tracking path hygiene check (`! git --no-pager diff 04e5da42e..HEAD -- src/ docs/ | grep -F '.copilot-tracking/' && ! git --no-pager diff -- src/ docs/ | grep -F '.copilot-tracking/'`): clean (`0` matches).

## Blockers and Remaining Work

* Blockers: none.
* Remaining work: none (`P01` and `P02` complete; ready for `rpi-review`).
* Retained non-blocking follow-up: Optional CSV extract adapter mapping synthetic year-one CSV tables into `discovery_contract` dataclasses.
