<!-- markdownlint-disable-file -->
# RPI Changes: Phase 0 Retrofit-Flow Discovery Contract c2 Hardening (Issue #124)

## Metadata

* Task ID: issue-124-c2
* Related plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: none
* Status basis: Completed all `P01` and `P02` tasks across `discovery_contract.py`, `test_discovery_contract.py`, and coupled Phase 0 documentation, and passed all focused validation gates (`TMPDIR=/dev/shm`).

## Execution Summary

Closed all five adversarial bypass and boundary findings (`RV-001`–`RV-005`) from `.copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c1-review.md` plus `c2` critique items `PC-001`–`PC-003`. Hardened `FrozenDict` against post-construction `__init__` and attribute mutation, bound `FlowDiscoveryReport` evaluation and owner sign-off to `_EVALUATED_FLOW_REPORT_REFS`, `_EVALUATED_FLOW_REPORT_DIGESTS`, and `_VALIDATED_FLOW_REPORT_SEALS`, added `FlowDiscoveryReport.to_json_dict()` and full 20-key `Mapping` / nested `FlowDiscoveryReport` parity in `enforce_governance_guard`, closed incomplete post-`as_of` active-work timestamp filtering and `window_end` fractional-second retention in `evaluate_property_flow`, added 4 focused adversarial regression tests (`29` total in `test_discovery_contract.py`, `98` across `test_discovery*.py`), updated Phase 0 contract documentation, and verified `ruff check .`, `ruff format --check .`, and `mypy`.

## Completed Work

### P01 (`P01-T01`, `P01-T02`): Discovery Contract Provenance, Mapping Parity, `FrozenDict`, and Cutoff Bounds

* `src/core/src/zava_forward/core/discovery_contract.py`:
  * `P01-T01`: Added `__slots__ = ("_frozen",)`, `@overload` `__init__` signatures, re-init blocking (`FrozenDict.__init__`), and attribute-mutation blocking (`__setattr__`, `__delattr__`) on `FrozenDict`. Extracted `_compute_flow_report_digest`, eliminated blank `calculation_digest=""` auto-fill in `FlowDiscoveryReport.__post_init__`, registered `evaluate_property_flow` outputs in `_EVALUATED_FLOW_REPORT_REFS` + `_EVALUATED_FLOW_REPORT_DIGESTS`, and bound `validate_flow_report`, `FlowDiscoveryReport.__post_init__` (`owner_validated=True`), `Phase0DiscoveryPack.__post_init__` (`owner_validated=True`), and `enforce_governance_guard` to `_VALIDATED_FLOW_REPORT_SEALS`. Added `FlowDiscoveryReport.to_json_dict() -> FrozenDict[str, object]` and expanded `enforce_governance_guard` across all 20 `_FLOW_REPORT_SIGNATURE_KEYS`, strict non-`datetime` ISO date checks, `GovernanceViolationError` wrapping, and nested `FlowDiscoveryReport` / `Mapping` verification.
  * `P01-T02`: Checked `(act_s is not None and act_s.date() > as_of)` and `(act_e is not None and act_e.date() > as_of)` before incomplete active-pair handling in `evaluate_property_flow`, and compared candidate selection timestamps via `window_start <= ident_dt.date() <= window_end`.

### P02 (`P02-T01`, `P02-T02`): Adversarial Regression Tests, Documentation Sync, and Focused Validation

* `src/core/tests/test_discovery_contract.py` (`P02-T01`): Added 4 focused regression tests (`0` removals; `29` total in file, within `<= 6` ceiling):
  * `test_flow_excludes_incomplete_post_as_of_active_work_and_keeps_window_end_microseconds`
  * `test_frozen_dict_blocks_reinit_and_attribute_mutation`
  * `test_provenance_blocks_blank_digest_reset_and_same_cohort_collision_forgery`
  * `test_mapping_guard_enforces_nested_flow_dataclass_and_json_roundtrip_digest`
* `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and `docs/reference/log.md` (`P02-T02`): Aligned prose with re-init-locked `FrozenDict`, `to_json_dict()`, and evaluated provenance / sign-off seals (zero `.copilot-tracking/` leaks).

## Implementation-Time Plan and Detail Updates

* Local judgment / immediately relevant current-state update (`P01-T01`, `P02-T01`): Tracked `evaluate_property_flow` / `validate_flow_report` instance provenance via module-private weakref map `_EVALUATED_FLOW_REPORT_REFS` (`id(report) -> weakref.ref`) rather than a private dataclass field on `FlowDiscoveryReport`, keeping `dataclasses.asdict(report)` completely free of internal state fields; aligned `AC-C2-3` / `AC-C2-4` prose in `phase0-retrofit-flow-discovery-124-c2-plan.md` and `phase0-retrofit-flow-discovery-124-c2-phase-details.md` with direct attribute syntax (`ruff` `B010`) and `WINDOW_END = 2026-10-31`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `unittest discover -s src/core/tests -p 'test_discovery*.py' -v` | `src/core/tests/test_discovery*.py` | Passed | `Ran 98 tests in 0.219s — OK` (`TMPDIR=/dev/shm`) |
| `unittest src/core/tests/test_live_doc_links.py src/core/tests/test_dependency_rule.py -v` | Live doc links & core import rules | Passed | `Ran 4 tests in 3.499s — OK` (`TMPDIR=/dev/shm`) |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` | Passed | `310 files already formatted` |
| `mypy` | `src/core` (`strict = true`) | Passed | `Success: no issues found in 363 source files` |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all `[x]`; `_EVALUATED_FLOW_REPORT_REFS` and `_VALIDATED_FLOW_REPORT_SEALS` synchronized across plan and phase details)
* Completed-work evidence and handoff prose: reconciled
* Validation, blockers, remaining work, and follow-up items: reconciled (`0` blockers, `0` remaining tasks)
* Review readiness: ready for single `rpi-review` on `issue-124-c2`

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c2-plan.md, `## Follow-Up Items`
* Optional CSV extract adapter mapping `support/synthetic-data/retrofit-flow/zava-forward-year-one/` tables into `discovery_contract` dataclasses (deferred outside Phase 0 rule-layer scope).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`, `P02`); completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`; remaining: none
* Validation coverage: 98 `test_discovery*.py` tests, 4 doc-link/dependency tests, `ruff check .`, `ruff format --check .`, and `mypy` all passed
* Blockers: none
* Current plan and detail updates: `_EVALUATED_FLOW_REPORT_REFS` weakref provenance implementation detail and `WINDOW_END = 2026-10-31` test fixture date recorded in plan and phase details
* Planning and critique state: ready (`PC-001`, `PC-002`, `PC-003` resolved)
* Follow-up items: optional CSV extract adapter (deferred)
* Review readiness or no-handoff reason: ready for `rpi-review`
* Continuation owner: confirmed automatic RPI Agent (`issue-124-c2`)
