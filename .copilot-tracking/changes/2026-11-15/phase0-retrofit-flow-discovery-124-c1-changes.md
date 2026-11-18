<!-- markdownlint-disable-file -->
# RPI Changes: Phase 0 Retrofit-Flow Discovery Contract c1 Remediation (Issue #124)

## Metadata

* Task ID: issue-124-c1
* Related plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: none
* Status basis: All planned source, unit-test, documentation, and focused validation items across `P01` and `P02` are complete and verified.

## Execution Summary

Completed full-plan `c1` remediation across `src/core/src/zava_forward/core/discovery_contract.py`, `src/core/tests/test_discovery_contract.py`, `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and `docs/reference/log.md`, resolving `RV-001`, `RV-002`, and `RV-003` alongside plan-critique tightenings `PC-001` and `PC-002`.

## Completed Work

### Phase P01 — Core Discovery Contract Hardening (`P01-T01`, `P01-T02`)

* Implemented `FrozenDict(dict[str, Any])` and recursive `_freeze_value()` in `src/core/src/zava_forward/core/discovery_contract.py` so `FlowDiscoveryReport` freezes `status_counts`, `cycle_time_legs`, `waits_by_party`, `return_loop_counts_by_property`, `return_loop_totals_by_kind`, and `energy_outcome_counts` against in-place mutation (`TypeError`) while preserving `isinstance(..., dict)` and `dataclasses.asdict()` compatibility (`RV-002`).
* Added deterministic SHA-256 `calculation_digest` computation (`_compute_flow_report_digest`) and `FlowDiscoveryReport.verify_digest()` enforced unconditionally in `FlowDiscoveryReport.__post_init__` (auto-computing when empty and verifying when supplied), `validate_flow_report` (verifying non-blank digest prior to `replace(...)`, addressing `PC-001`), `Phase0DiscoveryPack.__post_init__`, and `enforce_governance_guard` (verifying unconditionally prior to `if not owner_val:` early return, addressing `PC-001`) (`RV-002`).
* Refused `owner_validated=True` promotion with `GovernanceViolationError` whenever `report.gaps` or `report.invalid_accepted_handover_ids` is non-empty across `FlowDiscoveryReport.__post_init__`, `validate_flow_report`, `Phase0DiscoveryPack.__post_init__`, and `enforce_governance_guard` (including raw `Mapping` payloads, addressing `PC-001`) (`RV-001`).
* Added `validated_role: str | None = None` to `StageSpec`, `EventSpec`, `TimestampSpec`, `WaitStateSpec`, and `ReturnLoopSpec`; required `validated_role == owner_role` in `.validated` and `lifecycle_dictionary_gaps()`, and populated `validated_role=spec.owner_role` in every `validate_*_spec` helper (`RV-002`).
* Enforced canonical `1..10` `REQUIRED_FLOW_STAGE_CODES` ordering (`[(idx, code) for idx, code in enumerate(REQUIRED_FLOW_STAGE_CODES, start=1)]`) in `LifecycleDictionary.__post_init__` (`RV-002`).
* Restricted `evaluate_property_flow` cohort aggregations strictly to `baseline_candidate_ids` (`in_window` candidates with `selected_on <= as_of`), recording post-`as_of` candidates (`candidate-after-as-of:*`), unmatched-cohort stage/event/wait/loop records (`*-outside-baseline-cohort:*`), and post-cutoff stage/event/wait/loop records (`*-after-as-of:*`) in `gaps`, and scoping `duplicate_candidate_ids` to filtered in-window `<= as_of` candidates (`PC-002`, `RV-001`).
* Grounded `zero_event_candidate_ids` strictly in valid in-cohort `<= as_of` lifecycle event presence (`events_by_prop`) rather than stage transitions, waits, or return loops (`RV-001`).
* Added `unknown_cause_count` and `disputed_cause_count` keys to each `waits_by_party` row in `evaluate_property_flow` while retaining `unknown_or_disputed_count` and `unknown_or_disputed_cause` (`RV-003`).

### Phase P02 — Unit Tests, Documentation Sync, and Focused Validation (`P02-T01`, `P02-T02`)

* Updated 2 existing `P2` baseline candidate fixtures in `src/core/tests/test_discovery_contract.py` so in-cohort assertions remain valid under strict `baseline_candidate_ids` filtering (`C11`), removed `0` tests, and added `7` focused unit tests (`<= 12` ceiling) covering every `RV-001`, `RV-002`, `RV-003`, `PC-001`, and `PC-002` failure and acceptance path (`25` tests total in `test_discovery_contract.py`).
* Updated `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and appended an entry to `docs/reference/log.md` with zero `.copilot-tracking/` references in production code, docs, or commit messages.
* Executed all caller-specified focused validation checks with `TMPDIR=/dev/shm` and prepared the local Conventional Commit on `feat/gov-124-phase0-discovery`.

## Implementation-Time Plan and Detail Updates

* Local judgment / current-state sync: Updated the Dependencies note in `.copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan.md` to record `/dev/shm/zf-124-c1-venv` (ephemeral `.pth` shim isolating this worktree from shared `~/.local` editable installs when `test_discovery_assistant_demo.py` spawns `python3 -m zava_forward.core discovery-demo`). No requirements, scope, or acceptance criteria changed.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `PATH="/dev/shm/zf-124-c1-venv/bin:$PATH" TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_discovery*.py' -v` | All `test_discovery*.py` modules in `src/core/tests` (`94` tests, including `25` in `test_discovery_contract.py`) | Passed | `Ran 94 tests in 0.203s — OK` |
| `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_live_doc_links.py src/core/tests/test_dependency_rule.py -v` | Live Markdown relative links and cross-project dependency rules | Passed | `Ran 4 tests in 3.760s — OK` |
| `cd src/core && TMPDIR=/dev/shm python3 -m ruff check .` | `src/core` lint | Passed | `All checks passed!` |
| `cd src/core && TMPDIR=/dev/shm python3 -m ruff format --check .` | `src/core` formatting | Passed | `310 files already formatted` |
| `cd src/core && TMPDIR=/dev/shm mypy` | `src/core` strict static typing | Passed | `Success: no issues found in 363 source files` |
| Full `src/core` 3,730-test `unittest discover` | Unrelated `src/core` modules | Skipped (explicit caller instruction) | Caller specified focused validation tier (`DO NOT run full unittest discover across all 3,730 src/core tests`) |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all `[x]`)
* Completed-work evidence and handoff prose: reconciled
* Validation, blockers, remaining work, and follow-up items: reconciled (`94 + 4` targeted tests, `ruff`, and `mypy` all green; `0` blockers; `0` remaining work)
* Review readiness: ready for `rpi-review`

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan.md, `## Follow-Up Items`
* Optional CSV extract adapter mapping `support/synthetic-data/retrofit-flow/zava-forward-year-one/` tables into `discovery_contract` dataclasses (deferred outside Phase 0 rule-layer scope).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`, `P02`); completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`; remaining: none
* Validation coverage: `94` tests in `test_discovery*.py` passed (`0.203s`), `4` tests in `test_live_doc_links.py` + `test_dependency_rule.py` passed (`3.760s`), `ruff check .` passed, `ruff format --check .` passed (`310` files), `mypy` passed (`363` files)
* Blockers: none
* Current plan and detail updates: ephemeral `/dev/shm/zf-124-c1-venv` dependency note recorded in plan
* Planning and critique state: ready (`PC-001` and `PC-002` resolved)
* Follow-up items: optional CSV extract adapter (deferred)
* Review readiness or no-handoff reason: ready for `rpi-review`
* Continuation owner: confirmed automatic RPI Agent (`issue-124-c1`)
