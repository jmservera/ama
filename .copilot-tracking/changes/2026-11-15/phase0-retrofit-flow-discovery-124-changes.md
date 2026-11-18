<!-- markdownlint-disable-file -->
# RPI Changes: Phase 0 Retrofit-Flow Discovery Contract (Issue #124)

## Metadata

* Task ID: issue-124
* Related plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02`
* All remaining active-plan markers: none
* Status basis: Completed all source, test, documentation, focused validation, and pre-review commit preparation steps across `P01`–`P03`.

## Execution Summary

Implemented the unified Phase 0 retrofit-flow discovery contract in `src/core/src/zava_forward/core/discovery_contract.py`, aligned `discovery_register.py` and `discovery_flow.py` additively under the fail-closed `owner_validated` / `finding_status` governance contract, added 21 deterministic unit tests across `test_discovery_contract.py`, `test_discovery_register.py`, and `test_discovery_flow.py` (with 0 existing test removals), documented the contract and open Zava North Homes human gates in `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md` plus `docs/reference/README.md`, `docs/reference/log.md`, `docs/brds/retrofit-flow-discovery-brief.md`, and `src/core/README.md`, verified focused validation in an isolated `~/.cache` Python 3.12 virtualenv, and prepared Commit 1 cleanly on `feat/gov-124-phase0-discovery`.

## Completed Work

### P01 (`P01-T01`, `P01-T02`): Phase 0 Contract and Fail-Closed Governance Guard in `src/core`

* `src/core/src/zava_forward/core/discovery_register.py`: Added `CANDIDATE_FINDING_STATUS`, `VALIDATED_FINDING_STATUS`, `GovernanceViolationError`, `is_valid_human_actor`, additive `Constraint` fields (`owner_validated`, `owner_validated_by`, `supporting_evidence`, `contradicting_evidence`, `finding_status`) decoupled from legacy domain-only `is_company_finding` (`PC-001`), fail-closed `__post_init__` tampering checks, `validate_owner_finding()` gated on `DiscoveryOwner.status() == "ENDPOINT_AGREED"` and zero `dictionary_gaps`, and additive keys in `register_rows()`.
* `src/core/src/zava_forward/core/discovery_flow.py`: Stamped `owner_validated=False` and `finding_status="candidate_hypothesis_not_company_finding"` on `baseline_summary()` and `waits_by_party()`, and added governance-stamped `leg_summary()` and `loop_summary()`.
* `src/core/src/zava_forward/core/discovery_contract.py`: Implemented `NominatedDiscoveryOwner` (`nominate_discovery_owner`, `agree_discovery_endpoint`, direct `status()` human/separation enforcement), `LifecycleDictionary` (10 ordered PAS 2035 and retrofit flow stages plus `paused`, `excluded`, `withdrawn`, `cancelled`, and `reopened_aftercare` states, 15 distinct events, 8 timestamp specifications with `active_days=None` non-imputation, 7 wait states, and 4 return-loop kinds), `evaluate_property_flow()` (zero-event candidate retention, `BG-011` `assessment-to-ready-to-install` and `accepted handover` legs, `accepted handover` prerequisite checks, separate intended energy outcome tracking, and deterministic SHA-256 `calculation_digest`), `RankedConstraintRegister` (contiguous `1..N` ranks, required `supporting_evidence` and `contradicting_evidence`, all-`True` 5-part `ConstraintTestAssessment` for acceptance, proposer separation, and visible retention of adjudicated `DISPUTED` hypotheses as non-findings), `Phase0DiscoveryPack`, and `enforce_governance_guard()`.

### P02 (`P02-T01`): Deterministic Unit Tests in `src/core/tests/`

* `src/core/tests/test_discovery_contract.py`: Added 18 deterministic unit tests across `DiscoveryOwnerTests`, `LifecycleDictionaryTests`, `PropertyFlowEvaluationTests`, `RankedConstraintRegisterTests`, and `GovernanceGuardTests`.
* `src/core/tests/test_discovery_register.py`: Added 2 additive governance unit tests (`test_domain_decide_stays_unvalidated_until_nominated_owner_validates`, `test_forged_owner_validated_raises_governance_violation`) while keeping all 13 existing tests intact.
* `src/core/tests/test_discovery_flow.py`: Added `test_flow_summaries_carry_unvalidated_governance_fields` while keeping all 6 existing tests intact.

### P03 (`P03-T01`, `P03-T02`): Knowledge-Base Documentation, Focused Validation, and Local Commit

* Created `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md` and updated `docs/reference/README.md`, `docs/reference/log.md`, `docs/brds/retrofit-flow-discovery-brief.md`, and `src/core/README.md`, explicitly citing the BSI PAS 2035:2023 overview snapshot (`gap-pas-2035-licensed`) and keeping Zava North Homes human governance criteria (`OD-14`, `OD-16`, `OD-18`, `OD-36`) open.
* Configured local Git privacy-safe `user.email` (`8036360+jmservera@users.noreply.github.com`) via `gh api user`, cleaned up temporary `~/.cache/zf-124-venv` and `/dev/shm/zf-124-tmp` directories, and reconciled all RPI tracking artifacts for Commit 1 on `feat/gov-124-phase0-discovery`.

## Implementation-Time Plan and Detail Updates

* Local judgment (`mypy --strict` explicit re-exports): Updated `discovery_contract.py` to use explicit `X as X` re-export syntax for constants/errors imported from `discovery_register.py` so `mypy` passes under `strict = true` (`implicit_reexport = false`).
* Immediately relevant current-state update (`P03-T02` offline venv binding and baseline exclusions): Because Python 3.12's offline `venv` lacks `wheel` for PEP 660 `bdist_wheel`, `~/.cache/zf-124-venv` (`--system-site-packages`) bound `src/core/src` cleanly via `site-packages/zava_forward_core.pth` (generating zero `*.egg-info` files) so `test_discovery_assistant_demo.py` subprocess checks executed against the current worktree. Recorded two pre-existing host/base-branch exclusions observed outside touched files (`tools/test_epic_*.py` in `check-legacy-references.py`, missing optional `azure-iot-hub` SDK in `test_device_registry_azure.py`, and 1 pre-existing `test_challenge_no_retaliation_220.py` error on parent branch `feat/demo-164-chat-grounding-provenance-0900`), and synchronized `P03-T02` expectations in `plan.md` and `phase-details.md`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `ruff check .` | `src/core` | Passed | `All checks passed!` (exit 0) |
| `ruff format --check .` | `src/core` | Passed | `310 files already formatted` (exit 0) |
| `mypy` (`strict = true`) | `src/core` (363 source files) | Passed | `Success: no issues found in 363 source files` (exit 0) |
| `unittest discover -s tests -p 'test_discovery*.py' -v` | All 7 discovery test modules in `~/.cache/zf-124-venv` | Passed | `Ran 87 tests in 0.507s — OK` (18 in `test_discovery_contract`, 15 in `test_discovery_register`, 7 in `test_discovery_flow`, 47 in `test_discovery_assistant_*` including CLI subprocess tests) |
| `unittest tests.test_live_doc_links tests.test_dependency_rule -v` | Repository Markdown links and `src/core` import rules | Passed | `Ran 4 tests in 16.573s — OK` (0 unresolved relative links across live docs; 0 forbidden imports) |
| `python3 -m compileall -q src/core/src` | `src/core/src` bytecode compilation | Passed | Exit 0 |
| `python3 tools/rename-zava-tests.py` | Zava naming/migration regression suite | Passed | `Ran 25 tests in 0.776s — OK` (exit 0) |
| `python3 tools/check-legacy-references.py` | Markdown links and legacy path scan | Passed for touched scope (baseline exclusions noted) | `links: 0 violation(s) in 769 document(s)`; 0 reference violations in any new/modified file (8 pre-existing violations in untouched `tools/test_epic_*.py` on parent branch) |
| Full `src/core` `unittest discover -s tests -q` | Broad `src/core` regression sweep (3,730 tests) | Passed for all core/discovery modules (host/base exclusions noted) | 3,679 passed, 420 skipped; 0 failures in any touched or coupled module; 50 failures/errors in `test_device_registry_azure` due to absent optional `azure-iot-hub` SDK on offline host and 1 pre-existing error in untouched `test_challenge_no_retaliation_220` |
| Markdown style and `.copilot-tracking/` isolation check | New/modified `src/core` and `docs/` files | Passed | Verified 0 `.copilot-tracking` leaks, 0 em dashes, and 0 bolded-prefix list items |
| `tools/rpi-checks.py --all` | Full repository gate | Skipped | Explicitly excluded by caller instruction (`Validation tier: Focused ... do not run tools/rpi-checks.py --all`) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02` all checked `[x]`; `P03-T02` validation notes synchronized).
* Completed-work evidence and handoff prose: Reconciled across `changes.md`, `plan.md`, `phase-details.md`, and `state.json`.
* Validation, blockers, remaining work, and follow-up items: Current; 0 blockers; 0 remaining implementation tasks.
* Review readiness: Ready for `rpi-review`.

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-plan.md, `## Follow-Up Items`
* Optional CSV extract adapter mapping `support/synthetic-data/retrofit-flow/zava-forward-year-one/` tables into `discovery_contract` dataclasses: outside Issue #124 contract scope per `docs/brds/retrofit-flow-discovery-brief.md`; owned by future sponsor/owner direction.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`), `P03` (`P03-T01`, `P03-T02`); remaining: none
* Validation coverage: Focused tier complete (`ruff check`, `ruff format --check`, `mypy --strict`, 87/87 discovery unit tests, `test_live_doc_links`, `test_dependency_rule`, `compileall`, `rename-zava-tests.py`, Markdown style/isolation checks)
* Blockers: none
* Current plan and detail updates: Synchronized `P03-T02` `.pth` offline venv binding and baseline host/branch exclusions
* Planning and critique state: Ready (`PC-001`–`PC-004` resolved and verified in implementation)
* Follow-up items: Optional CSV extract adapter (deferred outside Issue #124 scope)
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
