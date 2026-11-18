<!-- markdownlint-disable-file -->
# Implementation Plan: Phase 0 Retrofit-Flow Discovery Contract c2 Hardening (Issue #124)

## Metadata

* Task ID: issue-124-c2
* Task slug: phase0-retrofit-flow-discovery-124-c2
* Parent task: issue-124-c1 (phase0-retrofit-flow-discovery-124-c1)
* Date: 2026-11-15
* Branch: feat/gov-124-phase0-discovery
* Planning status: ready
* Research artifact: .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md (`reused`)
* Phase details artifact: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md
* Plan critique artifact: .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c2-plan-critique.md
* Downstream changes path: .copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-c2-changes.md

## Executive Summary

Child task `issue-124-c2` closes the five adversarial bypass and boundary defects (`RV-001`–`RV-005`) surfaced during the `c1` post-implementation review (.copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c1-review.md) so the Phase 0 Retrofit-Flow Discovery Contract (`Issue #124`) achieves a clean, adversarially verified `Conformant` review verdict under `.copilot-tracking/`.

Phase `P01` hardens `src/core/src/zava_forward/core/discovery_contract.py` across two tight tasks: (1) binding `FlowDiscoveryReport` owner-validation and promotion (`FlowDiscoveryReport.__post_init__`, `validate_flow_report`, `Phase0DiscoveryPack`, and `enforce_governance_guard`) to evaluated calculation provenance (`_EVALUATED_FLOW_REPORT_DIGESTS` registered solely by `evaluate_property_flow`), enforcing nested `FlowDiscoveryReport` dataclass and serialized flow-report mapping digest/provenance checks inside `enforce_governance_guard` (plus a date-safe `FlowDiscoveryReport.to_json_dict()` helper), and locking `FrozenDict.__init__` / attribute mutation against post-construction re-initialization; and (2) checking active-work timestamps against `as_of` prior to the incomplete-pair branch and comparing candidate selection timestamps by UTC calendar date (`window_start <= ident_dt.date() <= window_end`) so fractional seconds on `window_end` are retained. Phase `P02` adds focused adversarial regression tests (`<= 6` additions, `0` removals) in `src/core/tests/test_discovery_contract.py`, refreshes coupled Phase 0 contract documentation if needed, runs the caller-specified focused validation suite with `TMPDIR=/dev/shm`, and leaves clean local Conventional Commits (`Refs #124` + Copilot trailer) without pushing or opening a PR.

## Sources and Evidence

* Prior `c1` review log: .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c1-review.md (`RV-001`–`RV-005`)
* Reused research synthesis: .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md (`C1`–`C12`)
* Canonical contract module: `src/core/src/zava_forward/core/discovery_contract.py`
* Canonical contract unit tests: `src/core/tests/test_discovery_contract.py`
* Coupled documentation: `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md`

## User Decisions and Requirements

* Complete the RPI remediation loop on branch `feat/gov-124-phase0-discovery` in `/home/azureuser/source/ama-demo-wt/feat-124-phase0-discovery` so `RV-001`–`RV-003` from the initial review and `RV-001`–`RV-005` from `phase0-retrofit-flow-discovery-124-c1-review.md` are fully resolved with a `Conformant` review verdict under `.copilot-tracking/`.
* Close blank `calculation_digest=""` reset / synthetic `dataclasses.replace(...)` promotion bypasses by binding owner-validated flow reports to `evaluate_property_flow` provenance (`c1` `RV-001`).
* Enforce nested `FlowDiscoveryReport` dataclass validation and serialized flow-report mapping digest/provenance verification inside `enforce_governance_guard` (`c1` `RV-002`).
* Lock `FrozenDict` against post-construction `.__init__(...)` and attribute mutation (`c1` `RV-003`).
* Check stage active-work timestamps against `as_of` before incomplete-pair handling (`c1` `RV-004`) and compare candidate `identified_at` against `window_start..window_end` by UTC calendar date so fractional final-day seconds are retained (`c1` `RV-005`).
* Use ONLY the focused validation tier with `TMPDIR=/dev/shm` (`test_discovery*.py`, `test_live_doc_links.py`, `test_dependency_rule.py`, `ruff check .`, `ruff format --check .`, `mypy`), commit locally with Conventional Commit (`Refs #124` + Copilot trailer), and do NOT push or open a PR.

## Goals

* Guarantee that neither `dataclasses.replace(..., calculation_digest="")` nor direct `FlowDiscoveryReport(..., owner_validated=True)` can mint an owner-validated report bypassing `evaluate_property_flow`.
* Guarantee that `enforce_governance_guard` enforces identical digest, provenance, zero-gap, zero-invalid-handover, and `owner_validated` invariants across `FlowDiscoveryReport`, `Phase0DiscoveryPack`, and raw or JSON-serialized `Mapping` payloads (top-level and nested `"flow_report"`).
* Make `FrozenDict` strictly immutable against `.__init__(...)`, `setattr`, and `delattr` while preserving `dataclasses.asdict()`, `copy.deepcopy()`, and plain `json.dumps(report.to_json_dict())`.
* Close post-`as_of` incomplete active-timestamp filtering and `window_end` fractional-second candidate retention in `evaluate_property_flow`.

## Scope and Non-Goals

* In scope:
  * `src/core/src/zava_forward/core/discovery_contract.py`
  * `src/core/tests/test_discovery_contract.py`
  * `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and `docs/reference/log.md` (concise prose alignment for evaluated provenance and `to_json_dict()`)
  * `.copilot-tracking/` `c2` plan, phase details, single critique, changes, review, and state records
* Out of scope / non-goals:
  * Modifying `discovery_flow.py`, `discovery_register.py`, or `discovery_assistant_*.py`
  * Running the full 3,730-test `src/core` suite, pushing to remote, or creating/updating a GitHub PR

## Functional Requirements

* `FR-C2-1` (Evaluated & validated digest provenance — `c1` `RV-001`, `PC-001`): `evaluate_property_flow` pre-computes SHA-256 `calculation_digest`, registers it in `_EVALUATED_FLOW_REPORT_DIGESTS`, and tracks the returned instance in `_EVALUATED_FLOW_REPORT_REFS` (weakref identity registry keeping `dataclasses.asdict(report)` free of private fields). `FlowDiscoveryReport.__post_init__` never auto-fills blank `calculation_digest` (calling `self.verify_digest()` unconditionally so `replace(..., calculation_digest="")` fails closed immediately for both candidate and validated reports) and, when `owner_validated=True`, requires `(calculation_digest, owner_validated_by, owner_validated_on.isoformat(), validation_note)` membership in `_VALIDATED_FLOW_REPORT_SEALS` (registered solely by `validate_flow_report` after verifying `_is_evaluated_report_instance(report)` and `calculation_digest in _EVALUATED_FLOW_REPORT_DIGESTS`). `Phase0DiscoveryPack.__post_init__` (when validated) and `enforce_governance_guard` (when `owner_validated=True`) enforce the same validated provenance seal.
* `FR-C2-2` (`Mapping` guard parity & JSON round-trip — `c1` `RV-002`, `PC-002`, `PC-003`): `FlowDiscoveryReport.to_json_dict()` constructs a strict-typed `FrozenDict[str, object]` with ISO date strings supporting plain `json.dumps(...)`. `enforce_governance_guard` detects flow-report mappings across all 20 `_FLOW_REPORT_SIGNATURE_KEYS`, validates date fields strictly (`date` excluding `datetime`, or `YYYY-MM-DD` `str`, including `owner_validated_on`), wraps canonicalization/parsing failures in `GovernanceViolationError`, and enforces symmetric candidate and validated checks on both nested `FlowDiscoveryReport` instances and nested/top-level flow-report `Mapping` payloads (rejecting `flow_report=None` or non-report values).
* `FR-C2-3` (`FrozenDict` re-init lock — `c1` `RV-003`, `PC-003`): `FrozenDict` declares `@overload` signatures on `__init__` for `mypy --strict` compatibility and blocks post-construction `__init__`, `__setattr__`, and `__delattr__` with `TypeError` while continuing to support initial construction, `copy`, `deepcopy`, and `dataclasses.asdict()`.
* `FR-C2-4` (Stage active-work `as_of` cutoff & `window_end` UTC date inclusion — `c1` `RV-004`, `RV-005`): `evaluate_property_flow` checks parsed `active_started_at` and `active_completed_at` independently for `.date() > as_of` (recording the post-`as_of` gap and skipping the stage record) before checking for an incomplete active-work pair, and checks `window_start <= ident_dt.date() <= window_end` so fractional seconds on `window_end` are retained.

## Non-Functional Requirements

* `NFR-C2-1` (Zero stdlib-external dependencies & strict typing): Pure Python 3.12 stdlib only; `ruff check .`, `ruff format --check .`, and `mypy` (`strict = true`) pass with zero warnings/errors.
* `NFR-C2-2` (Test ownership & ceiling): Canonical test owner `src/core/tests/test_discovery_contract.py`; exact test removals: `none` (`0`); maximum new test methods: `6`; generated targets: `none`. No `.copilot-tracking/` references in production code, docs, or commit messages.

## Acceptance Criteria

* `AC-C2-1`: Both `replace(gapped_report, gaps=(), calculation_digest="")` and `replace(validated_report, state_counts={"paused": 99}, calculation_digest="")` raise `GovernanceViolationError` inside `FlowDiscoveryReport.__post_init__`, and `replace(gapped_report, gaps=(), calculation_digest=manual_or_colliding_sha256)` raises `GovernanceViolationError` in `validate_flow_report` and direct `owner_validated=True` construction even when an identical clean cohort digest exists in the same process.
* `AC-C2-2`: `enforce_governance_guard` raises `GovernanceViolationError` when a validated `Mapping` embeds an unvalidated or gapped `FlowDiscoveryReport` instance under `"flow_report"` or when a serialized flow-report mapping (`asdict(validated)` or `validated.to_json_dict()`) has any mutated metric, while accepting an unmodified `json.loads(json.dumps(validated.to_json_dict()))` mapping.
* `AC-C2-3`: Calling `report.state_counts.__init__({"paused": 42})`, `report.state_counts._frozen = False`, or `del report.state_counts._frozen` raises `TypeError` without mutating `report.state_counts`.
* `AC-C2-4`: A stage transition with `active_started_at > as_of` and blank `active_completed_at` (or vice versa) records an `after as_of` gap and is excluded from `stage_metrics`; a candidate identified at `2026-10-31T23:59:59.500000Z` on `window_end = 2026-10-31` is retained in `baseline_candidate_ids`.
* `AC-C2-5`: Focused validation commands (`test_discovery*.py`, `test_live_doc_links.py`, `test_dependency_rule.py`, `ruff check .`, `ruff format --check .`, `mypy`) all pass with `TMPDIR=/dev/shm`, and clean local Conventional Commits (`Refs #124` + Copilot trailer) are recorded without pushing.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Close Provenance, Mapping Guard, `FrozenDict`, and Timestamp Cutoff Bypasses in `discovery_contract.py`

* Intent: Resolve `c1` findings `RV-001`–`RV-005` cleanly in `src/core/src/zava_forward/core/discovery_contract.py`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement evaluated digest provenance, `Mapping` guard parity, `to_json_dict()`, and `FrozenDict.__init__` lock

* Requirement and evidence: `FR-C2-1`, `FR-C2-2`, `FR-C2-3`, `NFR-C2-1`; `c1` `RV-001`–`RV-003`.
* Expected result: `FrozenDict` locks `__init__`, `__setattr__`, and `__delattr__`; `evaluate_property_flow` registers `report.calculation_digest` in `_EVALUATED_FLOW_REPORT_DIGESTS`; `FlowDiscoveryReport.__post_init__`, `validate_flow_report`, `Phase0DiscoveryPack`, and `enforce_governance_guard` enforce evaluated provenance and full `Mapping` / `FlowDiscoveryReport` parity; `FlowDiscoveryReport.to_json_dict()` supports plain `json.dumps(...)` round-trip verification.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Fix incomplete active-timestamp `as_of` ordering and `window_end` UTC calendar-date comparison in `evaluate_property_flow`

* Requirement and evidence: `FR-C2-4`, `NFR-C2-1`; `c1` `RV-004`–`RV-005`.
* Expected result: `evaluate_property_flow` checks `act_s.date() > as_of` and `act_e.date() > as_of` before incomplete-pair handling and checks `window_start <= ident_dt.date() <= window_end` so fractional seconds on `window_end` are retained.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Adversarial Regression Tests, Documentation Sync, and Focused Validation

* Intent: Prove `AC-C2-1`–`AC-C2-5` in `src/core/tests/test_discovery_contract.py`, align Phase 0 docs, run focused validation (`TMPDIR=/dev/shm`), and commit locally.
* Dependencies: `P01`

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add focused regression tests for `c1` `RV-001`–`RV-005` in `test_discovery_contract.py`

* Requirement and evidence: `AC-C2-1`–`AC-C2-4`, `NFR-C2-2`; `c1` `RV-001`–`RV-005`.
* Expected result: `0` removed tests and `<= 6` focused regression tests in `src/core/tests/test_discovery_contract.py` covering `replace(..., calculation_digest="")` forgery refusal, nested `FlowDiscoveryReport` and mutated `asdict`/`to_json_dict` mapping guard refusal (plus valid `to_json_dict` round-trip acceptance), `FrozenDict.__init__`/attribute mutation `TypeError`, incomplete active-timestamp post-`as_of` exclusion, and `window_end` fractional-second candidate inclusion.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Align Phase 0 documentation, run focused validation (`TMPDIR=/dev/shm`), and commit `c2` locally

* Requirement and evidence: `AC-C2-5`, `NFR-C2-1`, `NFR-C2-2`.
* Expected result: `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and `docs/reference/log.md` accurately note evaluated digest provenance and `to_json_dict()` without `.copilot-tracking/` references; all focused validation commands pass; clean local Conventional Commit recorded on `feat/gov-124-phase0-discovery` before final `rpi-review`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md

## Dependencies

* Commit `4e5f033a9` (`c1` implementation) on `feat/gov-124-phase0-discovery`.
* Python 3.12 toolchain (`unittest`, `ruff`, `mypy`) with `TMPDIR=/dev/shm` and `/dev/shm/zf-124-c1-venv` `.pth` shim for `test_discovery_assistant_demo.py`.

## Critique Disposition

Critique artifact: .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c2-plan-critique.md (`Verdict: Revise`; single final-candidate critique executed once).

* `PC-001` [High] (`resolved` — direct planner correction): Removed blank-digest auto-fill from `FlowDiscoveryReport.__post_init__` altogether (pre-computing `calculation_digest` inside `evaluate_property_flow`), added `_EVALUATED_FLOW_REPORT_REFS` weakref instance-identity check in `validate_flow_report` plus `_VALIDATED_FLOW_REPORT_SEALS` sign-off seal across `FlowDiscoveryReport.__post_init__`, `Phase0DiscoveryPack.__post_init__`, and `enforce_governance_guard`, eliminating same-cohort SHA-256 collision bypasses while preserving `dataclasses.asdict()` cleanliness and existing `replace(validated)` tamper tests.
* `PC-002` [High] (`resolved` — direct planner correction): Expanded `_FLOW_REPORT_SIGNATURE_KEYS` to all 20 flow-report-unique keys, enforced strict `date` (excluding `datetime`) or `YYYY-MM-DD` validation on `window_start`, `window_end`, `as_of`, and `owner_validated_on`, wrapped canonicalization/parsing errors in `GovernanceViolationError`, and required symmetric candidate/validated checks on nested `"flow_report"` values (rejecting `None` or non-report objects).
* `PC-003` [Medium] (`resolved` — direct planner correction): Added `@overload` signatures on `FrozenDict.__init__`, direct `FrozenDict[str, object](...)` construction in `FlowDiscoveryReport.to_json_dict()`, and `Mapping[str, object]` helper annotations so `mypy --strict` passes cleanly.

## Follow-Up Items

* Optional CSV extract adapter mapping synthetic year-one CSV tables under `support/synthetic-data/retrofit-flow/zava-forward-year-one/` into `discovery_contract` dataclasses — outside Phase 0 rule-layer scope; owner: future discovery data-pipeline task.

## Handoff

* Mode: confirmed automatic RPI Agent (`issue-124-c2`).
* Next stage after single `rpi-plan-critique` disposition: `rpi-implement` writing `.copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-c2-changes.md`.
