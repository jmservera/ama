<!-- markdownlint-disable-file -->
# Implementation Plan: Phase 0 Retrofit-Flow Discovery Contract c4 Mapping Provenance & Extension Hardening (Issue #124)

* Task ID: `issue-124-c4`
* Parent Task ID: `issue-124-c3` (`phase0-retrofit-flow-discovery-124-c3`)
* Date: `2026-11-15`
* Branch: `feat/gov-124-phase0-discovery` (target base: `feat/demo-164-chat-grounding-provenance-0900`)
* Planning status: `ready` (single `rpi-plan-critique` `PC-001`–`PC-004` applied directly)
* Research disposition: `reused` (.copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md and .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c3-review.md)
* Critique artifact: .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c4-plan-critique.md

## Executive Summary

Child loop `issue-124-c4` closes all five findings (`RV-001`–`RV-005`) surfaced during the adversarial `c3` review (`phase0-retrofit-flow-discovery-124-c3-review.md`):

1. **Authenticated Cross-Process JSON & In-Process Mapping Provenance (`RV-001`)**: Restore strict `_EVALUATED_FLOW_REPORT_DIGESTS` and 5-tuple `_VALIDATED_FLOW_REPORT_SEALS` enforcement on unkeyed in-process flow-report `Mapping`s (`signing_key=None`) so callers cannot flip `owner_validated=True` on `candidate.to_json_dict()` or mutate metrics and recompute `_compute_flow_report_digest`. Add optional stdlib `hmac` SHA-256 authentication (`FlowDiscoveryReport.to_json_dict(*, signing_key: bytes | None = None)` and `enforce_governance_guard(..., signing_key: bytes | None = None)`) minted exclusively from live `_is_evaluated_report_instance(self)` (and 5-tuple sealed when `owner_validated=True`) `FlowDiscoveryReport` objects over `(calculation_digest, dictionary_schema_digest, owner_validated, finding_status, owner_validated_by, owner_validated_on, validation_note)` for cross-process JSON transport.
2. **Full `Mapping` Governance Parity Across Pack, Register, Hypothesis, and Lifecycle Shapes (`RV-002`, `RV-004`)**: Exclude shared `"dictionary_schema_digest"` from `_FLOW_REPORT_SIGNATURE_KEYS` so `LifecycleDictionaryReport` mappings are never misclassified as flow reports. Classify and strictly validate all five governed `Mapping` shapes (`FlowDiscoveryReport`, `LifecycleDictionaryReport`, `ConstraintHypothesis`, `RankedConstraintRegister`, and `Phase0DiscoveryPack`) and reject unrecognized `owner_validated=True` mappings that lack governed artifact payload structure. Require validated pack `Mapping`s to carry validated, schema-matched, same-signer `dictionary_report`, `flow_report`, and `constraint_register` sub-artifacts with adjudicated hypotheses.
3. **Complete Dictionary Extension Validation & Non-Blank Schema Digest (`RV-003`, `RV-005`)**: Validate every entry (including extensions and duplicate checks) across `dictionary.stages`, `dictionary.events`, `dictionary.timestamps`, `dictionary.wait_states`, and `dictionary.return_loops` inside `lifecycle_dictionary_gaps(dictionary)`, and require non-blank matching `dictionary_schema_digest` on `LifecycleDictionaryReport` (and mappings) whenever compared against a `LifecycleDictionary`.

## Sources

* .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c3-review.md (`RV-001`–`RV-005`)
* .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c2-review.md
* .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c1-review.md
* .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md
* .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md
* src/core/src/zava_forward/core/discovery_contract.py
* src/core/tests/test_discovery_contract.py

## User Decisions and Requirements

* Complete the autonomous RPI remediation loop (`research`, `plan`, `implement`, `review`) for Issue #124 and record a `Conformant` review verdict under `.copilot-tracking/`.
* Preserve focused validation (`TMPDIR=/dev/shm`, `test_discovery*.py`, `test_live_doc_links.py`, `test_dependency_rule.py`, `ruff check .`, `ruff format --check .`, `mypy`) without running the full 3,730-test `src/core` suite.
* Commit all source, test, doc, and `.copilot-tracking/` artifacts locally with Conventional Commit (`Refs #124` + Copilot trailer) without pushing or opening a PR.

## Goals

* Close `c3` `RV-001`–`RV-005` cleanly in `src/core/src/zava_forward/core/discovery_contract.py` while preserving all `c0`/`c1`/`c2`/`c3` guarantees.
* Prove closure with focused adversarial regression tests (`<= 5` new tests, `0` removed tests) in `src/core/tests/test_discovery_contract.py` and keep Phase 0 docs synchronized.

## Scope and Non-Goals

* **In scope**: `src/core/src/zava_forward/core/discovery_contract.py`, `src/core/tests/test_discovery_contract.py`, `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md`, and `.copilot-tracking/` `c4` RPI artifacts.
* **Non-goals**: External non-stdlib packages, mutating real Zava North Homes governance criteria on Issue #124, or pushing commits.

## Functional Requirements

* `FR-C4-1` (`RV-001`, `PC-003`): Validate `signing_key` at the entry of `enforce_governance_guard` and `FlowDiscoveryReport.to_json_dict` whenever `signing_key is not None` (`isinstance(signing_key, (bytes, bytearray))` and `len(signing_key) >= 16`). In `_verify_flow_report_mapping`, enforce strict types on all governance fields (`isinstance(owner_validated, bool)`, `isinstance(..., str)` for `finding_status`, `owner_validated_by`, `validation_note`, `notice`, and `None` or `_strict_iso_date` for `owner_validated_on`); on candidate mappings (`owner_validated is False`), require `notice == NOT_FINDING`, blank `owner_validated_by` and `validation_note`, and `owner_validated_on is None`. When `signing_key is None`, require `raw_digest in _EVALUATED_FLOW_REPORT_DIGESTS` (for both candidate and validated mappings) and, when `require_validated=True`, require 5-tuple `(raw_digest, schema_digest, actor, on_iso, note) in _VALIDATED_FLOW_REPORT_SEALS`. When `signing_key is not None`, compute and verify `governance_hmac` via `hmac.new(..., hashlib.sha256)` and `hmac.compare_digest` over the 8-element canonical JSON array `[calculation_digest, dictionary_schema_digest, owner_validated, finding_status, owner_validated_by, owner_validated_on, validation_note, notice]`. `to_json_dict(signing_key=...)` must refuse minting an HMAC unless `self.verify_digest()` passes, `_is_evaluated_report_instance(self)` is `True`, and (if `self.owner_validated` is `True`) the 5-tuple seal is in `_VALIDATED_FLOW_REPORT_SEALS`.
* `FR-C4-2` (`RV-002`, `RV-004`, `PC-001`, `PC-002`): Exclude `"dictionary_schema_digest"` from `_FLOW_REPORT_SIGNATURE_KEYS`. In `enforce_governance_guard`, evaluate disjoint signature-key predicates across all five governed `Mapping` shapes (`FlowDiscoveryReport`, `LifecycleDictionaryReport`, `ConstraintHypothesis`, `RankedConstraintRegister`, and `Phase0DiscoveryPack`), immediately rejecting mappings that match more than one shape (`len(matched_shapes) > 1`), mappings that match zero shapes when `owner_validated is True`, or matched governed mappings that contain unexpected keys outside their allowed schema:
  * `LifecycleDictionaryReport` mappings: verify strict integer counts, `endpoint == ENDPOINT`, count parity + non-blank `dictionary_schema_digest == _dictionary_schema_digest(dictionary)` whenever `dictionary is not None`, candidate metadata hygiene (`notice == NOT_FINDING`, blank sign-off fields when `owner_validated is False`), and zero `gaps` + human `owner_validated_by == expected_owner` + valid `_strict_iso_date(owner_validated_on)` + non-blank `validation_note` when `owner_validated is True`.
  * `ConstraintHypothesis` mappings: unconditionally extract `discovery_owner_validated_by` as the discovery-owner signer; verify strict `int` (not `bool`) `rank >= 1`, `review_status != OWNER_VALIDATED` whenever `owner_validated is False`, and (when `owner_validated is True`) `review_status == OWNER_VALIDATED`, non-empty non-string `Sequence` `supporting_evidence` (`direction == SUPPORTS`) & `contradicting_evidence` (`direction == CONTRADICTS`) with non-blank `statement`/`source_ref` and valid human `recorded_by`, exact `bool` `True` across all five `constraint_test` criteria, non-empty non-string `Sequence[str]` `domain_owner_roles` with `domain_validated_role in domain_owner_roles` and valid human `domain_validated_by` case-insensitively distinct from `proposed_by`, valid `_strict_iso_date` dates, and valid human `discovery_owner_validated_by == expected_owner` case-insensitively distinct from `proposed_by` with non-blank `decision_note`. (Also permit `RankedConstraintRegister.to_rows()` summary dicts only in candidate mode when `owner_validated is False` and `review_status != OWNER_VALIDATED`.)
  * `RankedConstraintRegister` mappings: verify non-empty non-string `Sequence` `hypotheses` with contiguous ranks `1..N` and unique codes, validating each hypothesis in candidate mode; when `owner_validated is True`, require valid human `owner_validated_by == expected_owner`, `_strict_iso_date(owner_validated_on)`, non-blank `validation_note`, and every hypothesis to have two-sided evidence and `review_status in (OWNER_VALIDATED, DISPUTED)` (candidate non-finding with valid domain dispute metadata for `DISPUTED`; validated and matching `expected_owner` for `OWNER_VALIDATED`).
  * `Phase0DiscoveryPack` mappings: parse/coerce any present `"discovery_owner"` (`NominatedDiscoveryOwner` or `Mapping` with strict calendar dates) and `"dictionary"` (`LifecycleDictionary` or `Mapping` reconstructed into spec dataclasses so `LifecycleDictionary.__post_init__` and `lifecycle_dictionary_gaps` execute); bind nested sub-artifact checks to `effective_dictionary = dictionary if dictionary is not None else pack_dictionary` and require `_dictionary_schema_digest(pack_dictionary) == _dictionary_schema_digest(dictionary)` whenever both are present; when `owner_validated is True`, require non-blank `contract_version == CONTRACT_VERSION` (if present), ready matching `pack_owner` (if present), zero gaps on `pack_dictionary` (if present), and ALL THREE `"dictionary_report"`, `"flow_report"`, and `"constraint_register"` to be present with `owner_validated is True` and recursively pass `enforce_governance_guard(..., discovery_owner=discovery_owner, dictionary=effective_dictionary, signing_key=signing_key)`.
* `FR-C4-3` (`RV-003`, `PC-004`): Define `_is_calendar_date(value: object) -> TypeGuard[date]` (`isinstance(value, date) and not isinstance(value, datetime)`) and enforce it across all five `*Spec.validated` properties, all five `validate_*_spec` helpers, `NominatedDiscoveryOwner`, `LifecycleDictionaryReport`, `FlowDiscoveryReport`, `ConstraintHypothesis`, `RankedConstraintRegister`, `Phase0DiscoveryPack`, and `validate_*` promotion functions. Update `lifecycle_dictionary_gaps(dictionary)` to run duplicate-key checks first, missing-required-key presence checks (`if key not in by_key`) second, and a single per-entry completeness/cross-reference/role/validation `elif` pass over EVERY item in `dictionary.stages`, `dictionary.events`, `dictionary.timestamps`, `dictionary.wait_states`, and `dictionary.return_loops` (preserving the exact 49-gap baseline on `build_default_lifecycle_dictionary()` while catching any unvalidated or invalid extension item).
* `FR-C4-4` (`RV-005`, `PC-002`): Require non-blank `dictionary_schema_digest == _dictionary_schema_digest(dictionary)` unconditionally on `LifecycleDictionaryReport` (and lifecycle report `Mapping`s) whenever compared against a `LifecycleDictionary` (including an embedded pack `dictionary` mapping) in `Phase0DiscoveryPack.__post_init__`, `validate_lifecycle_report`, and `enforce_governance_guard` (both candidate and validated modes).

## Non-Functional Requirements

* `NFR-C4-1`: Pure Python 3.12 standard library only (`hmac`, `hashlib`, `contextvars`, `weakref`); zero new `.copilot-tracking/` references introduced in branch diff across `src/` or `docs/` or in commit messages.
* `NFR-C4-2`: Lock test discipline: canonical test file `src/core/tests/test_discovery_contract.py`; exact removals: `none` (`0` removed; update `test_cross_process_json_roundtrip_mapping_passes_guard_and_rejects_tampering` to exercise `signing_key` plus unkeyed cross-process refusal); maximum additions: `4` new test methods (`<= 5` ceiling).

## Acceptance Criteria

* `AC-C4-1`: Unkeyed `candidate.to_json_dict()` with `owner_validated=True` flipped (or tampered metric + recomputed `_compute_flow_report_digest`) raises `GovernanceViolationError`; cross-process `validated.to_json_dict(signing_key=key)` passes `enforce_governance_guard(..., signing_key=key)` in a fresh Python subprocess while rejecting candidate promotion, tampered metrics + recomputed digest, missing key, or wrong key.
* `AC-C4-2`: `enforce_governance_guard` accepts candidate and validated `asdict(summarize_lifecycle_dictionary(d))` mappings without misclassifying them as flow reports, and rejects validated pack `Mapping`s containing candidate `dictionary_report` or `constraint_register` sub-artifacts (or unadjudicated hypotheses) as well as blank `dictionary_schema_digest`.
* `AC-C4-3`: Appending an unvalidated extension `StageSpec` (or event/timestamp/wait/loop) to an otherwise validated `LifecycleDictionary` produces non-empty `lifecycle_dictionary_gaps(d)` and fails `validate_flow_report`, `validate_lifecycle_report`, and `enforce_governance_guard`.
* `AC-C4-4`: Focused validation commands (`test_discovery*.py`, `test_live_doc_links.py`, `test_dependency_rule.py`, `ruff check .`, `ruff format --check .`, `mypy`) pass with `TMPDIR=/dev/shm`, branch diff under `src/` and `docs/` introduces zero `.copilot-tracking/` strings, and clean local Conventional Commits (`Refs #124` + Copilot trailer) are recorded without pushing.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement Authenticated JSON Provenance, Full Mapping Shape Guards, and Dictionary Extension Validation

* Intent: Close `c3` `RV-001`–`RV-005` in `src/core/src/zava_forward/core/discovery_contract.py`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add `hmac` `signing_key` cross-process authentication + in-process `Mapping` provenance, 5-shape `Mapping` governance guards, non-blank dictionary digest checks, and extension-inclusive `lifecycle_dictionary_gaps`

* Requirement and evidence: `FR-C4-1`–`FR-C4-4`, `NFR-C4-1`; `c3` `RV-001`–`RV-005`.
* Expected result: All five governed `Mapping` shapes and all `LifecycleDictionary` extension items fail closed on any unvalidated, mismatched, or forged input while supporting both unkeyed in-process `to_json_dict()` and `hmac`-authenticated cross-process `to_json_dict(signing_key=key)` verification.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c4-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Adversarial Regression Tests, Documentation Sync, and Focused Validation

* Intent: Prove `AC-C4-1`–`AC-C4-4` in `src/core/tests/test_discovery_contract.py`, sync Phase 0 docs, run focused validation (`TMPDIR=/dev/shm`), and commit locally.
* Dependencies: `P01`

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update subprocess JSON test and add focused regression tests for unkeyed Mapping forgery, pack/lifecycle Mapping parity, blank candidate digest, and unvalidated dictionary extensions

* Requirement and evidence: `AC-C4-1`–`AC-C4-3`, `NFR-C4-2`; `c3` `RV-001`–`RV-005`.
* Expected result: `0` removed tests and `<= 4` new regression tests in `src/core/tests/test_discovery_contract.py` proving every `c3` `RV-001`–`RV-005` reproduction fails closed.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c4-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Sync Phase 0 documentation for `signing_key` cross-process JSON verification and extension validation, run focused checks, and commit locally

* Requirement and evidence: `AC-C4-4`, `NFR-C4-1`, `NFR-C4-2`.
* Expected result: `phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and `docs/reference/log.md` accurately document in-process vs `signing_key` cross-process JSON verification; all focused validation commands pass; clean local commit recorded before `c4` `rpi-review`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c4-phase-details.md

## Dependencies

* Commit `b6e918142` (`c3` implementation) on `feat/gov-124-phase0-discovery`.
* Python 3.12 toolchain (`unittest`, `ruff`, `mypy`) with `TMPDIR=/dev/shm` and `/dev/shm/zf-124-c1-venv`.

## Follow-Up Items

* Optional CSV extract adapter mapping synthetic year-one CSV tables under `support/synthetic-data/retrofit-flow/zava-forward-year-one/` into `discovery_contract` dataclasses — outside Phase 0 rule-layer scope; owner: future discovery data-pipeline task.

## Critique Disposition

Single final-candidate critique executed at `.copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c4-plan-critique.md` (`Execution status: Complete`, `Verdict: Revise`, `0` Critical, `2` High, `2` Medium, `0` Low, user response required: `no`):

* `PC-001` [High] — Applied directly: `_verify_hypothesis_mapping` checks `domain_validated_role in domain_owner_roles` and `is_valid_human_actor(domain_validated_by)`, unconditionally uses `discovery_owner_validated_by` as the discovery-owner signer, enforces `review_status != OWNER_VALIDATED` on candidate mappings, and `enforce_governance_guard` rejects multi-shape `Mapping` collisions (`len(matched_shapes) > 1`) and unexpected keys outside each shape's allowed set.
* `PC-002` [High] — Applied directly: `_verify_pack_mapping` parses/coerces embedded `"discovery_owner"` and `"dictionary"` dataclasses or serialized `asdict` mappings, enforces gap-free `pack_dictionary` and matching `pack_owner` + `contract_version == CONTRACT_VERSION` on validated pack mappings, and binds nested sub-artifact checks to `effective_dictionary`.
* `PC-003` [Medium] — Applied directly: Included `notice` as the 8th element of the `governance_hmac` canonical payload, added entry-level `_validate_signing_key`, and enforced strict candidate `notice == NOT_FINDING` and empty sign-off metadata on candidate mappings.
* `PC-004` [Medium] — Applied directly: Specified `_is_calendar_date` across all spec `.validated` properties, `validate_*_spec` helpers, and governance dataclasses/validators, and separated missing-required checks from single-pass per-item sequence validation in `lifecycle_dictionary_gaps` to preserve the exact 49-gap baseline.

## Handoff

* Mode: confirmed automatic RPI Agent (`issue-124-c4`).
* Implementation status: Completed (`P01` / `P01-T01`, `P02` / `P02-T01` / `P02-T02`).
* Next stage: `rpi-review` writing `.copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c4-review.md`.
