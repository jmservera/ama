<!-- markdownlint-disable-file -->
# Review: Phase 0 Retrofit-Flow Discovery Contract (Issue #124)

## Scope and Evidence

* Task ID: issue-124
* Review date: 2026-11-15
* Review scope: full task (`P01`, `P02`, `P03`)
* Assessed boundary: Issue #124 Phase 0 retrofit-flow discovery software contract and governance guard in `src/core` (`discovery_contract.py`, `discovery_register.py`, `discovery_flow.py`), deterministic unit tests (`test_discovery_contract.py`, `test_discovery_register.py`, `test_discovery_flow.py`), knowledge-base and component documentation (`docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `docs/reference/README.md`, `docs/reference/log.md`, `docs/brds/retrofit-flow-discovery-brief.md`, `src/core/README.md`), critique dispositions (`PC-001`–`PC-004`), focused validation tier, and local commit `0c2457297` on `feat/gov-124-phase0-discovery`.
* Plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-research.md, commit `0c2457297` on `feat/gov-124-phase0-discovery`, `docs/brds/retrofit-flow-discovery-brief.md`, `docs/brds/agentic-retrofit-programme-brd.md` (`BG-011`, `RULE-019`, `OD-16`, `OD-18`).

## Opening Review State

* Interpreted review goal: Verify once, read-only against the completed implementation and artifact set, whether commit `0c2457297` satisfies all Issue #124 software contract requirements (`FR-1`–`FR-6`, `NFR-1`–`NFR-2`, `AC-1`–`AC-6`), critique dispositions (`PC-001`–`PC-004`), repository documentation/governance rules, and focused validation expectations, keeping execution status separate from outcome and routing any open items cleanly.
* Review scope: full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; research, plan, phase details, plan critique, changes log, and committed code/tests/docs (`0c2457297`) are present and reconciled.
* Acceptance basis: `FR-1`–`FR-6`, `NFR-1`–`NFR-2`, `AC-1`–`AC-6`, `PC-001`–`PC-004` critique dispositions, and caller focused-tier instructions.
* First comparison boundary: Plan-to-change reconciliation across `P01`, `P02`, `P03`, and `Follow-Up Items` before detailed code/governance/documentation inspection.
* Active read-only boundaries: This review stage creates/updates only `.copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md` (and parent RPI state transition metadata); no production code, tests, docs, plan, details, critique, research, or changes files may be mutated.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single post-implementation review on 2026-11-15 across all planned phases (`P01`, `P02`, `P03`), critique dispositions (`PC-001`–`PC-004`), implementation-time updates, validation records, and committed source/test/documentation artifacts in commit `0c2457297` on `feat/gov-124-phase0-discovery`, assisted by an independent read-only review lens.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `P01 (P01-T01, P01-T02): Phase 0 Contract and Fail-Closed Governance Guard in src/core` | Reconciled | Checked `[x]` in plan; source artifacts `discovery_contract.py`, `discovery_register.py`, and `discovery_flow.py` match recorded evidence. |
| `P02` (`P02-T01`) | `P02 (P02-T01): Deterministic Unit Tests in src/core/tests/` | Reconciled | Checked `[x]` in plan; 21 new test methods added across 3 files (within <= 30 cap) and 0 existing tests removed. |
| `P03` (`P03-T01`, `P03-T02`) | `P03 (P03-T01, P03-T02): Knowledge-Base Documentation, Focused Validation, and Local Commit` | Reconciled | Checked `[x]` in plan; KB synthesis, index, log, discovery brief, `src/core/README.md`, validation table, and commit `0c2457297` are aligned. |
| `## Follow-Up Items` | `Follow-Up Items` (Optional CSV extract adapter) | Reconciled | Retained outside active `P01`–`P03` completion claims in both `plan.md` and `changes.md`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/discovery_register.py`, `src/core/src/zava_forward/core/discovery_flow.py` | Added additive `owner_validated`, `finding_status`, `supporting_evidence`, `contradicting_evidence`, `validate_owner_finding()`, `leg_summary()`, and `loop_summary()` while preserving legacy `Constraint.is_company_finding` backward compatibility (`PC-001`). | Commit `0c2457297`; `changes.md` under `P01` | `ruff check`, `ruff format --check`, `mypy --strict`, `test_discovery_register.py` (15/15), `test_discovery_flow.py` (7/7) Passed | Reconciled; conforms to `PC-001` backward-compatibility boundary. |
| `P01-T02` | `src/core/src/zava_forward/core/discovery_contract.py` | Delivered unified Phase 0 contract (`NominatedDiscoveryOwner`, 15-state / 15-event / 8-timestamp / 7-wait / 4-loop `LifecycleDictionary`, `evaluate_property_flow`, `RankedConstraintRegister`, `Phase0DiscoveryPack`, `enforce_governance_guard`). | Commit `0c2457297`; `changes.md` under `P01` | `ruff`, `mypy --strict`, `test_discovery_contract.py` (18/18) Passed | Delivered core contract; review identified hardening gaps `RV-001`–`RV-003` in flow promotion/cutoff checks, deep immutability, and wait cause counters. |
| `P02-T01` | `src/core/tests/test_discovery_contract.py`, `src/core/tests/test_discovery_register.py`, `src/core/tests/test_discovery_flow.py` | Added 18 semantic/governance unit tests in `test_discovery_contract.py` plus 3 additive tests across `test_discovery_register.py` and `test_discovery_flow.py` with 0 removals. | Commit `0c2457297`; `changes.md` under `P02` | 87/87 `test_discovery*.py` tests Passed in 0.507s | Reconciled; covers planned positive and negative invariants, though additional edge-case tests should accompany `RV-001`–`RV-003` in follow-up work. |
| `P03-T01` | `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `docs/reference/README.md`, `docs/reference/log.md`, `docs/brds/retrofit-flow-discovery-brief.md`, `src/core/README.md` | Documented Phase 0 contract, BSI PAS 2035:2023 overview snapshot scope (`gap-pas-2035-licensed`), two-sided constraint register, governance guard, and open Zava North Homes human gates (`OD-14`, `OD-16`, `OD-18`, `OD-36`). | Commit `0c2457297`; `changes.md` under `P03` | `test_live_doc_links.py` (2/2), Markdown style/isolation check, and `check-legacy-references.py` (`links: 0 violation(s)`) Passed | Reconciled and compliant with repository Markdown and regulatory provenance conventions. |
| `P03-T02` | Local branch `feat/gov-124-phase0-discovery` and `.copilot-tracking/` 2026-11-15 artifacts | Executed focused validation in `~/.cache/zf-124-venv`, cleaned temporary directories, set privacy-safe GitHub noreply email, and created commit `0c2457297` with Copilot trailer without pushing. | Commit `0c2457297`; `changes.md` `Validation Record` | Focused checks Passed; full-suite host/base-branch exclusions documented transparently | Reconciled. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T02` (`discovery_contract.py` imports) | Used explicit `X as X` re-exports from `discovery_register` to satisfy `mypy` under `strict = true` (`implicit_reexport = false`). | `mypy` check during `P02`; local judgment (no user decision needed). | Recorded in `changes.md` under `Implementation-Time Plan and Detail Updates`. | Not needed; preserves approved architecture and `PC-001`–`PC-004`. | Reconciled. |
| `P03-T02` (`plan.md`, `phase-details.md`, `changes.md`) | Used `site-packages/zava_forward_core.pth` inside `~/.cache/zf-124-venv` (`--system-site-packages`) because offline Python 3.12 `pip` lacked `wheel` for PEP 660 `bdist_wheel`, and recorded pre-existing untouched exclusions (`azure-iot-hub` optional SDK in `test_device_registry_azure.py`, 1 error in untouched `test_challenge_no_retaliation_220.py`, and 8 lines in untouched `tools/test_epic_*.py`). | Offline venv execution and broad regression run during `P03-T02`; immediately relevant current-state update. | Synchronized `P03-T02` validation text across `plan.md`, `phase-details.md`, and `changes.md`. | Not needed; preserves focused validation tier requested by caller and `PC-004` `~/.cache` isolation. | Reconciled. |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four critique findings (`PC-001`, `PC-002`, `PC-003`, `PC-004`) from `.copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-plan-critique.md` have explicit `resolved` dispositions in `plan.md` `## Critique Disposition` (plus `accepted_with_risk` for open Zava North Homes human sign-off gates and `gap-pas-2035-licensed`) and are implemented in `0c2457297`.
* Material revisions: No significant or divergent requirement/architecture revisions occurred during implementation; no second critique was run.
* Dependent-work pause assessment: No pause was triggered because all implementation discoveries were local judgment or immediately relevant current-state updates preserving approved intent.
* Justification assessment: Supported by test, typecheck, lint, and link-check evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Optional CSV extract adapter mapping `support/synthetic-data/retrofit-flow/zava-forward-year-one/` tables into `discovery_contract` dataclasses | `docs/brds/retrofit-flow-discovery-brief.md` specifies that extract import, persistence, and screens should wait for a nominated owner and approved company dataset rather than Phase 0 rule delivery. | Future sponsor/owner direction or optional child engineering task | Open distinct follow-up route (`follow_up`); kept outside active `P01`–`P03` scope and not treated as a defect. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Flow-report promotion, baseline cohort filtering, and `as_of` cutoff hardening in `discovery_contract`

* Related scope: `P01-T02`, `P02-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`evaluate_property_flow`, `validate_flow_report`)
* Impact: `validate_flow_report` verifies nominated-owner `ENDPOINT_AGREED` status and a zero-gap `LifecycleDictionary`, but does not block promotion when `report.gaps` or `report.invalid_accepted_handover_ids` are non-empty. In `evaluate_property_flow`, stage, event, wait, and loop records whose `property_id` is absent from `baseline_candidate_ids` or whose timestamp falls strictly after `as_of` are aggregated without flagging an unmatched-cohort or post-cutoff gap, and `zero_event_candidate_ids` checks activity across stages/waits/loops rather than lifecycle events specifically.
* Destination: `rpi-implement`
* Smallest useful next action: Refuse `validate_flow_report` with `GovernanceViolationError` when `report.gaps` or `report.invalid_accepted_handover_ids` is non-empty, restrict cohort aggregations in `evaluate_property_flow` to `baseline_candidate_ids` up to `as_of` while recording unmatched/post-cutoff records in `gaps`, base `zero_event_candidate_ids` strictly on lifecycle event presence, and add focused unit tests in `src/core/tests/test_discovery_contract.py`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Deep container immutability and role-bound direct-construction checks on `FlowDiscoveryReport` and `LifecycleDictionary`

* Related scope: `P01-T02`, `P02-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`FlowDiscoveryReport`, `StageSpec`, `EventSpec`, `TimestampSpec`, `WaitStateSpec`, `ReturnLoopSpec`, `LifecycleDictionary`)
* Impact: Although `FlowDiscoveryReport` is a frozen dataclass, its nested `dict` fields (`state_counts`, `bg011_assessment_to_ready_to_install_days`, `candidate_to_accepted_handover_days`, `post_install_handover_legs_days`, `return_loops_by_property`, `return_loop_totals`, `explicit_rework_days_by_kind`) remain mutable dictionaries after sign-off rather than immutable `MappingProxyType` or tuple projections; additionally, directly constructing dictionary entry specs with `validated_by` and `validated_on` bypasses checking an explicit `validated_role == owner_role` field on `lifecycle_dictionary_gaps()`, and `LifecycleDictionary.__post_init__` checks contiguous `1..N` stage numbering without enforcing exact canonical `REQUIRED_FLOW_STAGE_CODES` order.
* Destination: `rpi-implement`
* Smallest useful next action: Freeze nested mappings on `FlowDiscoveryReport` (or bind `validate_flow_report` + `enforce_governance_guard` to a verified immutable `calculation_digest`), record and verify `validated_role == owner_role` inside dictionary spec gap checks and canonical `REQUIRED_FLOW_STAGE_CODES` order in `LifecycleDictionary.__post_init__`, and add unit tests in `src/core/tests/test_discovery_contract.py`.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Separate `unknown_cause_count` and `disputed_cause_count` in `evaluate_property_flow` party wait summaries

* Related scope: `P01-T02`, `P02-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`evaluate_property_flow` `waits_by_party` construction)
* Impact: `waits_by_party` preserves `UNKNOWN` and `DISPUTED` wait causes without guessing by counting them together in `unknown_or_disputed_count`, whereas exposing separate `unknown_cause_count` and `disputed_cause_count` fields alongside `unknown_or_disputed_count` prevents downstream loss of distinction between unrecorded causes and owner-disputed causes.
* Destination: `rpi-implement`
* Smallest useful next action: Add `unknown_cause_count` and `disputed_cause_count` keys to each `waits_by_party` row in `evaluate_property_flow` (retaining `unknown_or_disputed_count` for compatibility) and assert both counters in `src/core/tests/test_discovery_contract.py`.

## Defects

* `RV-001` [Medium] -> `rpi-implement`
* `RV-002` [Medium] -> `rpi-implement`
* `RV-003` [Low] -> `rpi-implement`

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Tighten `validate_flow_report` gap rejection, baseline cohort filtering, `as_of` cutoff handling, and `zero_event_candidate_ids` semantics in `discovery_contract.py` + `test_discovery_contract.py`. | Implementation hardening defect within approved Phase 0 contract architecture. |
| `RV-002` | `rpi-implement` | Enforce deep mapping immutability / digest verification on `FlowDiscoveryReport`, `validated_role == owner_role` on dictionary specs, and canonical stage ordering in `LifecycleDictionary`. | Implementation hardening defect within approved Phase 0 contract architecture. |
| `RV-003` | `rpi-implement` | Expose separate `unknown_cause_count` and `disputed_cause_count` counters on `waits_by_party` rows in `discovery_contract.py`. | Minor implementation fidelity improvement within approved Phase 0 contract. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Optional CSV extract adapter mapping `support/synthetic-data/retrofit-flow/zava-forward-year-one/` tables into `discovery_contract` dataclasses (`follow_up`, deferred per `docs/brds/retrofit-flow-discovery-brief.md` until sponsor/owner direction).
* Real-world Zava North Homes human governance actions (`OD-14`, `OD-16`, `OD-18`, `OD-36`): Executive Sponsor nomination of Discovery Owner, operational owner sign-off of the PAS 2035 lifecycle dictionary, approved twelve-month company data extract, and formal owner validation of company findings (external human governance boundary; cannot be satisfied by software).

## Blockers and Remaining Work

* Blockers: none for the software contract task boundary (real-world Zava North Homes human sign-offs remain explicitly open governance gates as required by AC4 / `docs/brds/retrofit-flow-discovery-brief.md`).
* Remaining active work: none in the completed `P01`–`P03` run; `RV-001`–`RV-003` are routed to a follow-up `rpi-implement` selection.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `/home/azureuser/.local/bin/ruff check .` | `src/core` | Passed | `All checks passed!` (exit 0) |
| `/home/azureuser/.local/bin/ruff format --check .` | `src/core` | Passed | `310 files already formatted` (exit 0) |
| `/home/azureuser/.local/bin/mypy` | `src/core` (`strict = true`, 363 files) | Passed | `Success: no issues found in 363 source files` (exit 0) |
| `PYTHONPATH=src:tests ~/.cache/zf-124-venv/bin/python -m unittest discover -s tests -p 'test_discovery*.py' -v` | All 7 discovery test modules | Passed | `Ran 87 tests in 0.507s — OK` |
| `PYTHONPATH=src:tests ~/.cache/zf-124-venv/bin/python -m unittest tests.test_live_doc_links tests.test_dependency_rule -v` | Live Markdown links and `src/core` dependency boundary | Passed | `Ran 4 tests in 16.573s — OK` |
| `python3 -m compileall -q src/core/src` | `src/core/src` | Passed | Exit 0 |
| `python3 tools/rename-zava-tests.py` | Zava naming regression tests | Passed | `Ran 25 tests in 0.776s — OK` |
| `python3 tools/check-legacy-references.py` | Repository Markdown links and legacy path scan | Passed for touched scope (pre-existing untouched `tools/test_epic_*.py` failures noted) | `links: 0 violation(s) in 769 document(s)`; 0 reference violations in touched files |
| Broad `src/core` `unittest discover -s tests -q` | All 3,730 tests in `src/core` | Partial / Host-limited | 3,679 passed, 420 skipped; 0 failures in touched/discovery modules; 50 failures/errors in untouched `test_device_registry_azure` due to missing optional `azure-iot-hub` SDK on offline host and 1 pre-existing error in untouched `test_challenge_no_retaliation_220` |
| `python3 tools/rpi-checks.py --all` | Full local RPI gate | Skipped | Excluded per explicit caller instruction (`Validation tier: Focused ... do not run tools/rpi-checks.py --all`) |

## Outcome

* Outcome: Defects found
* Outcome rationale: Planned `P01`–`P03` deliverables, unit tests (87/87 discovery tests), `ruff`, `mypy --strict`, KB synthesis, and commit `0c2457297` executed cleanly and satisfy the core Phase 0 contract structure and `PC-001`–`PC-004` critique dispositions, while post-implementation review identified two `Medium` hardening defects (`RV-001`, `RV-002`) and one `Low` fidelity defect (`RV-003`) in `discovery_contract.py` routed to a follow-up `rpi-implement` pass. Per RPI stop rules, a conformant outcome is not claimed while material findings (`RV-001`, `RV-002`) remain open.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | Resolve `RV-001`, `RV-002`, and `RV-003` in `src/core/src/zava_forward/core/discovery_contract.py` and `src/core/tests/test_discovery_contract.py`. |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | `follow_up` | Optional CSV extract adapter (`support/synthetic-data/retrofit-flow/zava-forward-year-one/` -> `discovery_contract`) pending sponsor/owner direction; live Zava North Homes human sign-offs (`OD-14`, `OD-16`, `OD-18`, `OD-36`) remain human-owned. |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: Focused validation passed (`ruff check`, `ruff format --check`, `mypy --strict`, 87/87 `test_discovery*.py`, `test_live_doc_links`, `test_dependency_rule`, `compileall`, `rename-zava-tests.py`, 0 link violations in 769 docs); `tools/rpi-checks.py --all` skipped per caller instruction.
* Blockers: none

