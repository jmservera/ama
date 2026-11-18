<!-- markdownlint-disable-file -->
# Implementation Plan: Phase 0 Retrofit-Flow Discovery Contract c3 Final Provenance & Dictionary Binding (Issue #124)

## Metadata

* Task ID: issue-124-c3
* Task slug: phase0-retrofit-flow-discovery-124-c3
* Parent task: issue-124-c2 (phase0-retrofit-flow-discovery-124-c2)
* Date: 2026-11-15
* Branch: feat/gov-124-phase0-discovery
* Planning status: ready
* Research artifact: .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md (`reused`)
* Phase details artifact: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c3-phase-details.md
* Plan critique artifact: .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c3-plan-critique.md
* Downstream changes path: .copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-c3-changes.md

## Executive Summary

Child task `issue-124-c3` resolves the five adversarial findings (`RV-001`–`RV-005`) surfaced during the `c2` review (.copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c2-review.md) so the Phase 0 Retrofit-Flow Discovery Contract (`Issue #124`) achieves an adversarially verified `Conformant` review verdict under `.copilot-tracking/`.

Phase `P01` tightens `src/core/src/zava_forward/core/discovery_contract.py` across four bounded invariants: (1) computing deterministic `_dictionary_schema_digest(dictionary)` over structural lifecycle specs and recording `dictionary_schema_digest` on `FlowDiscoveryReport` (included in `calculation_digest` and `to_json_dict()`) and `LifecycleDictionaryReport`, verifying schema digest equality and stage/party/loop membership in `validate_flow_report`, `validate_lifecycle_report`, `Phase0DiscoveryPack.__post_init__`, and `enforce_governance_guard`; (2) enforcing nominated-owner signer equality across `dictionary_report`, `flow_report`, `constraint_register`, and `Phase0DiscoveryPack` inside `Phase0DiscoveryPack.__post_init__`; (3) gating `FlowDiscoveryReport(..., owner_validated=True)` dataclass construction via a `ContextVar[bool]` active solely inside `validate_flow_report` and `FlowDiscoveryReport.__deepcopy__` (blocking post-sign-off `dataclasses.replace(..., owner_validated=True)` seal replay); and (4) verifying deserialized `Mapping` payloads deterministically across process boundaries via full 21-field `calculation_digest`, `dictionary_schema_digest == _dictionary_schema_digest(dictionary)`, `discovery_owner` readiness, signer equality, zero gaps, and zero invalid handovers without failing on empty process-local memory registries in a fresh Python process. Phase `P02` adds `<= 5` focused adversarial regression tests (`0` removals, including a real cross-process `subprocess` JSON round-trip test) in `src/core/tests/test_discovery_contract.py`, narrows `FrozenDict` documentation claims (`dict` subclass for `asdict()`/JSON compatibility + `verify_digest()` tamper detection), passes the caller-specified focused validation suite (`TMPDIR=/dev/shm`), and records clean local Conventional Commits (`Refs #124` + Copilot trailer) without pushing.

## Sources and Evidence

* Prior `c2` review log: .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c2-review.md (`RV-001`–`RV-005`)
* Prior `c1` review log: .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c1-review.md
* Original Issue #124 review log: .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md
* Reused research synthesis: .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md
* Canonical contract module & tests: `src/core/src/zava_forward/core/discovery_contract.py`, `src/core/tests/test_discovery_contract.py`
* Coupled documentation: `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md`

## User Decisions and Requirements

* Resolve all remaining review defects on `feat/gov-124-phase0-discovery` and record a `Conformant` review verdict under `.copilot-tracking/` for Issue #124.
* Bind `evaluate_property_flow` dictionary schema to `validate_flow_report`, `Phase0DiscoveryPack`, and `enforce_governance_guard` (`c2` `RV-001`).
* Enforce sub-artifact signer equality (`dictionary_report`, `flow_report`, `constraint_register`) and dictionary parity inside `Phase0DiscoveryPack.__post_init__` (`c2` `RV-002`).
* Ensure `json.loads(json.dumps(validated.to_json_dict()))` passes `enforce_governance_guard` in a fresh Python process while rejecting any mutated metric, mismatched dictionary, or unready owner (`c2` `RV-003`).
* Prevent external `dataclasses.replace(..., owner_validated=True)` calls from replaying an existing in-process validation seal (`c2` `RV-004`).
* Accurately document `FrozenDict` `dict`-subclass semantics and `verify_digest()` tamper detection (`c2` `RV-005`).
* Run ONLY the focused validation tier with `TMPDIR=/dev/shm` and commit locally (`Refs #124` + Copilot trailer) without pushing or opening a PR.

## Goals

* Bind `FlowDiscoveryReport` and `LifecycleDictionaryReport` deterministically to the structural `LifecycleDictionary` schema (`dictionary_schema_digest`) across evaluation, validation, pack construction, and `enforce_governance_guard`.
* Close `Phase0DiscoveryPack.__post_init__` signer mismatches and external `dataclasses.replace(..., owner_validated=True)` seal replay.
* Support deterministic cross-process JSON `Mapping` verification in `enforce_governance_guard` while retaining strict in-process evaluation and `validate_flow_report` construction provenance on `FlowDiscoveryReport` instances.
* Align `FrozenDict` docstrings and Phase 0 Markdown documentation accurately.

## Scope and Non-Goals

* In scope:
  * `src/core/src/zava_forward/core/discovery_contract.py`
  * `src/core/tests/test_discovery_contract.py`
  * `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md`
  * `.copilot-tracking/` `c3` plan, phase details, single critique, changes, review, and state records
* Out of scope / non-goals:
  * Cryptographic HMAC key management (Phase 0 is a pure deterministic stdlib rule contract)
  * Modifying `discovery_flow.py`, `discovery_register.py`, or `discovery_assistant_*.py`
  * Running full `src/core` test discovery or pushing to remote

## Functional Requirements

* `FR-C3-1` (Dictionary schema binding — `c2` `RV-001`, `PC-001`, `PC-002`): `_dictionary_schema_digest(dictionary: LifecycleDictionary) -> str` computes canonical JSON SHA-256 over structural `stages`, `events`, `timestamps`, `wait_states`, and `return_loops` definitions (excluding human sign-off metadata so pre-sign-off evaluation and post-sign-off validation of the identical dictionary schema share the same schema digest, while any added/removed/altered stage, event, timestamp, wait state, or return loop changes the digest). `FlowDiscoveryReport` records `dictionary_schema_digest: str` (included in `_FLOW_REPORT_DIGEST_KEYS`, `_FLOW_REPORT_SIGNATURE_KEYS`, `calculation_digest`, and `to_json_dict()`) and `LifecycleDictionaryReport` records non-blank `dictionary_schema_digest: str` from `summarize_lifecycle_dictionary`. `validate_flow_report`, `validate_lifecycle_report`, `Phase0DiscoveryPack.__post_init__`, and `enforce_governance_guard` (across both candidate and validated `FlowDiscoveryReport`, `LifecycleDictionaryReport`, `Phase0DiscoveryPack`, and flow-report `Mapping`s whenever `dictionary` is provided, requiring `dictionary` when `owner_validated=True` and comparing `pack.dictionary` against caller `dictionary`) verify `dictionary_schema_digest == _dictionary_schema_digest(dictionary)` plus stage/party/loop membership in `dictionary`.
* `FR-C3-2` (`Phase0DiscoveryPack` signer & sub-artifact parity — `c2` `RV-002`): When `Phase0DiscoveryPack.owner_validated` is `True`, `__post_init__` verifies `self.owner_validated_by.strip() == owner`, `self.dictionary_report.owner_validated_by.strip() == owner`, `self.flow_report.owner_validated_by.strip() == owner`, and `self.constraint_register.owner_validated_by.strip() == owner` (plus `accepted`/`disputed` hypothesis signer checks matching `enforce_governance_guard`), `self.dictionary_report.dictionary_schema_digest == schema_digest`, and `self.flow_report.dictionary_schema_digest == schema_digest`.
* `FR-C3-3` (Construction-gated `owner_validated=True` dataclass provenance — `c2` `RV-004`): A module-private `ContextVar[bool]` (`_ALLOW_VALIDATED_FLOW_REPORT_INIT`, default `False`) is set `True` exclusively inside `validate_flow_report` and `FlowDiscoveryReport.__deepcopy__`. `FlowDiscoveryReport.__post_init__` rejects any `owner_validated=True` initialization when `_ALLOW_VALIDATED_FLOW_REPORT_INIT.get()` is `False`, preventing external `FlowDiscoveryReport(..., owner_validated=True)` or `dataclasses.replace(..., owner_validated=True)` seal replay even after a clean report is validated in the same process.
* `FR-C3-4` (Cross-process deterministic `Mapping` verification — `c2` `RV-003`): `_verify_flow_report_mapping` verifies all 21 digest fields (`_FLOW_REPORT_DIGEST_KEYS` including `dictionary_schema_digest`) against `calculation_digest`, strict calendar-date strings, zero `gaps`, zero `invalid_accepted_handover_ids`, human `owner_validated_by` matching `discovery_owner.owner`, and (when `dictionary` is supplied, which `enforce_governance_guard` requires for `owner_validated=True` flow mappings) `dictionary_schema_digest == _dictionary_schema_digest(dictionary)` plus stage/party/loop membership — without depending on process-local `_EVALUATED_FLOW_REPORT_DIGESTS` / `_VALIDATED_FLOW_REPORT_SEALS` so `json.loads(json.dumps(validated.to_json_dict()))` verifies cleanly in a fresh Python process.
* `FR-C3-5` (`FrozenDict` documentation precision — `c2` `RV-005`): `FrozenDict` docstring, `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and `docs/reference/log.md` accurately describe `FrozenDict` as a `dict` subclass preserving `dataclasses.asdict()` / `json.dumps()` compatibility that blocks standard `Mapping` mutation, `__init__` re-initialization, and attribute mutation while `verify_digest()` catches low-level `dict.__setitem__` bypasses, and distinguish in-process dataclass construction provenance from cross-process SHA-256 tamper-evident JSON `Mapping` verification.

## Non-Functional Requirements

* `NFR-C3-1`: Pure Python 3.12 stdlib only (`contextvars`, `weakref`, `hashlib`, `json`); `ruff check .`, `ruff format --check .`, and `mypy` (`strict = true`) pass cleanly.
* `NFR-C3-2`: Canonical test file `src/core/tests/test_discovery_contract.py`; exact test removals: `none` (`0`); maximum new test methods: `5`; generated targets: `none`; zero `.copilot-tracking/` references in production code, docs, or commit messages.

## Acceptance Criteria

* `AC-C3-1`: Evaluating `evaluate_property_flow` with an extra unapproved stage in `dictionary_a` and calling `validate_flow_report(..., dictionary_b)` or `enforce_governance_guard(..., dictionary=dictionary_b)` against a validated `dictionary_b` lacking that stage raises `GovernanceViolationError`; evaluating with unvalidated default `dictionary` and signing after validating the identical schema succeeds.
* `AC-C3-2`: Constructing `Phase0DiscoveryPack(..., owner_validated=True)` where `flow_report`, `dictionary_report`, or `constraint_register` was signed by a different actor than `discovery_owner.owner` raises `GovernanceViolationError` inside `Phase0DiscoveryPack.__post_init__`.
* `AC-C3-3`: After signing `clean_report` via `validate_flow_report`, calling `dataclasses.replace(gapped_report, gaps=(), owner_validated=True, ..., calculation_digest=clean_report.calculation_digest)` or `dataclasses.replace(validated, ...)` raises `GovernanceViolationError`, while `copy.deepcopy(validated)` succeeds.
* `AC-C3-4`: `json.loads(json.dumps(validated.to_json_dict()))` passes `enforce_governance_guard(..., discovery_owner=owner, dictionary=dictionary)` inside a fresh `subprocess.run([sys.executable, "-c", ...])` Python process and raises `GovernanceViolationError` when any metric or `dictionary` schema differs.
* `AC-C3-5`: Focused validation commands (`test_discovery*.py`, `test_live_doc_links.py`, `test_dependency_rule.py`, `ruff check .`, `ruff format --check .`, `mypy`) pass with `TMPDIR=/dev/shm`, and clean local Conventional Commits (`Refs #124` + Copilot trailer) are recorded without pushing.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement Dictionary Schema Binding, Pack Signer Parity, `ContextVar` Seal Gate, and Cross-Process Mapping Verification

* Intent: Close `c2` findings `RV-001`–`RV-005` cleanly in `src/core/src/zava_forward/core/discovery_contract.py`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add `dictionary_schema_digest` binding, `Phase0DiscoveryPack` signer parity, `_ALLOW_VALIDATED_FLOW_REPORT_INIT` gate, and cross-process `Mapping` verification

* Requirement and evidence: `FR-C3-1`–`FR-C3-5`, `NFR-C3-1`; `c2` `RV-001`–`RV-005`.
* Expected result: `FlowDiscoveryReport` and `LifecycleDictionaryReport` bind to `_dictionary_schema_digest(dictionary)`; `Phase0DiscoveryPack.__post_init__` enforces signer and dictionary parity across all sub-artifacts; `_ALLOW_VALIDATED_FLOW_REPORT_INIT` blocks external `owner_validated=True` construction / `replace` seal replay while preserving `copy.deepcopy`; `_verify_flow_report_mapping` deterministically verifies 21-field `calculation_digest` and `dictionary_schema_digest` across fresh Python processes; `FrozenDict` docstring is narrowed accurately.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c3-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Adversarial Regression Tests, Documentation Precision, and Focused Validation

* Intent: Prove `AC-C3-1`–`AC-C3-5` in `src/core/tests/test_discovery_contract.py`, align Phase 0 docs, run focused validation (`TMPDIR=/dev/shm`), and commit locally.
* Dependencies: `P01`

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add focused regression tests (including cross-process subprocess JSON verification) in `test_discovery_contract.py`

* Requirement and evidence: `AC-C3-1`–`AC-C3-4`, `NFR-C3-2`; `c2` `RV-001`–`RV-004`.
* Expected result: `0` removed tests and `<= 5` new regression tests in `src/core/tests/test_discovery_contract.py` covering dictionary schema mismatch refusal, `Phase0DiscoveryPack` sub-artifact signer mismatch refusal, post-sign-off `replace(..., owner_validated=True)` seal replay refusal, and fresh-subprocess `to_json_dict()` round-trip verification.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c3-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Align Phase 0 documentation prose, run focused validation (`TMPDIR=/dev/shm`), and commit `c3` locally

* Requirement and evidence: `FR-C3-5`, `AC-C3-5`, `NFR-C3-1`, `NFR-C3-2`; `c2` `RV-005`.
* Expected result: `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and `docs/reference/log.md` accurately describe `dictionary_schema_digest`, `FrozenDict` `dict`-subclass + `verify_digest()` semantics, and cross-process JSON verification without `.copilot-tracking/` leaks; all focused checks pass; clean local Conventional Commit recorded before `c3` `rpi-review`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c3-phase-details.md

## Dependencies

* Commit `b7c91e832` (`c2` implementation) on `feat/gov-124-phase0-discovery`.
* Python 3.12 toolchain (`unittest`, `ruff`, `mypy`) with `TMPDIR=/dev/shm` and `/dev/shm/zf-124-c1-venv`.

## Critique Disposition

Critique artifact: .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c3-plan-critique.md (`Verdict: Revise`; single final-candidate critique executed once).

* `PC-001` [Medium] (`resolved` — direct planner correction): Added explicit `pack.dictionary` vs caller `dictionary` schema-digest and zero-gap checks (plus sub-artifact signer parity) in `enforce_governance_guard`.
* `PC-002` [Medium] (`resolved` — direct planner correction): Executed `_verify_report_matches_dictionary` before early candidate return in `enforce_governance_guard` whenever `dictionary is not None`, and required non-blank `dictionary_schema_digest == _dictionary_schema_digest(dictionary)` in `validate_lifecycle_report`, `Phase0DiscoveryPack.__post_init__`, and `enforce_governance_guard` (`LifecycleDictionaryReport`).
* `PC-003` [Low] (`resolved` — direct planner correction): Included `dictionary_schema_digest` in 5-tuple `_VALIDATED_FLOW_REPORT_SEALS` and scoped `_ALLOW_VALIDATED_FLOW_REPORT_INIT.set(True)` strictly around `FlowDiscoveryReport(...)` inside `__deepcopy__`.

## Follow-Up Items

* Optional CSV extract adapter mapping synthetic year-one CSV tables under `support/synthetic-data/retrofit-flow/zava-forward-year-one/` into `discovery_contract` dataclasses — outside Phase 0 rule-layer scope; owner: future discovery data-pipeline task.

## Handoff

* Mode: confirmed automatic RPI Agent (`issue-124-c3`).
* Next stage after single `rpi-plan-critique` disposition: `rpi-implement` writing `.copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-c3-changes.md`.
