<!-- markdownlint-disable-file -->
# RPI Plan Critique: Phase 0 Retrofit-Flow Discovery Contract c1 Remediation (Issue #124)

## Metadata

* Task ID: issue-124-c1
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Remediate post-implementation review defects `RV-001` [Medium], `RV-002` [Medium], and `RV-003` [Low] for Issue #124 (`BG-011`, `RULE-019`) on branch `feat/gov-124-phase0-discovery`; run only the focused validation tier (`TMPDIR=/dev/shm`, targeted `test_discovery*.py`, `test_live_doc_links.py`, `test_dependency_rule.py`, `ruff check .`, `ruff format --check .`, `mypy`); commit locally with `Refs #124` and Copilot trailer without pushing or opening a PR.
* Research and evidence considered: .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md, .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md (`C1`-`C12`), .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan.md, .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md, src/core/src/zava_forward/core/discovery_contract.py, src/core/tests/test_discovery_contract.py, docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md, src/core/README.md.
* Decisions, dependencies, and acceptance criteria considered: Confirmed caller decisions 1-4; `FR-C1-1`-`FR-C1-5`, `NFR-C1-1`-`NFR-C1-2`, `AC-C1-1`-`AC-C1-6`; contrarian findings `C11` (`P2` baseline candidate fixture alignment in two existing unit tests plus `unknown_or_disputed_cause` compatibility alias) and `C12` (`FrozenDict(dict)` + SHA-256 `calculation_digest` instead of `MappingProxyType` to preserve `dataclasses.asdict()`).
* Assessment boundary: Evaluates technical completeness, fail-closed governance soundness, type-checking and serialization compatibility, existing-test preservation, documentation synchronization, and focused validation fidelity across the supplied `c1` plan, phase details, research, review log, and target repository files. Does not evaluate live Zava North Homes human sign-offs (`OD-14`, `OD-16`, `OD-18`, `OD-36`) or out-of-scope CSV extract ingestion adapters.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1 / `RV-001` / `FR-C1-1` / `AC-C1-1` | Partial | `FlowDiscoveryReport.__post_init__`, `validate_flow_report`, `Phase0DiscoveryPack.__post_init__`, and `validate_discovery_pack` reject non-empty `gaps` and `invalid_accepted_handover_ids`, while `enforce_governance_guard` (`src/core/src/zava_forward/core/discovery_contract.py:1998-2046`) needs explicit `Mapping` gap/invalid-handover rejection (`PC-001`). |
| Caller Req 1 / `RV-001` / `FR-C1-2` / `AC-C1-2` | Partial | `P01-T02` covers candidate/stage/event/wait/loop cohort and `as_of` filtering, same-day open-clock clamping, and lifecycle-only `zero_event_candidate_ids`, while `duplicate_candidate_ids` (`src/core/src/zava_forward/core/discovery_contract.py:1130-1131`) still counts raw `candidates` before `as_of` and window filtering unless explicitly scoped to `in_window` (`PC-002`). |
| Caller Req 2 / `RV-002` / `FR-C1-3` / `AC-C1-3` / `C12` | Partial | `FrozenDict(dict)` + recursive `_freeze_container` preserves `dataclasses.asdict()` (`C12`) and `mypy --strict`, while `P01-T01` must specify that `verify_digest()` rejects blank digests, runs before `replace(...)` in `validate_flow_report`, and runs before the `not owner_val` early return in `enforce_governance_guard` (`PC-001`). |
| Caller Req 2 / `RV-002` / `FR-C1-4` / `AC-C1-4` / `C2`-`C3` | Covered | `P01-T01` adds `validated_role: str = ""` across all five spec dataclasses, sets it in `validate_*_spec`, requires non-blank `owner_role` and `validated_role == owner_role` in `.validated` and `lifecycle_dictionary_gaps()`, and enforces `[(s.order, s.code) for s in self.stages if s.kind == "flow"] == list(enumerate(REQUIRED_FLOW_STAGE_CODES, start=1))` in `LifecycleDictionary.__post_init__`. |
| Caller Req 3 / `RV-003` / `FR-C1-5` / `AC-C1-5` / `C5`, `C11` | Covered | `P01-T02` tracks `unknown_cause_count` (`cause_code.strip() in {UNKNOWN, ""}`) and `disputed_cause_count` (`cause_code.strip() == WAIT_CAUSE_DISPUTED`) separately while retaining `unknown_or_disputed_count` and `unknown_or_disputed_cause`. |
| Caller Req 4 / `NFR-C1-1`-`NFR-C1-2` / `AC-C1-6` | Covered | `P02` enforces `TMPDIR=/dev/shm`, targeted `test_discovery*.py`, `test_live_doc_links.py`, `test_dependency_rule.py`, `ruff check .`, `ruff format --check .`, `mypy`, `<= 12` added tests / `0` removed tests, KB/README/log sync without `.copilot-tracking/` leakage, and local `Refs #124` commit with Copilot trailer and no push/PR. |
| `P01` (`P01-T01`, `P01-T02`) | Partial | Clean single-module split in `src/core/src/zava_forward/core/discovery_contract.py`; requires minor planner tightening for `PC-001` and `PC-002`. |
| `P02` (`P02-T01`, `P02-T02`) | Covered | `P02-T01` updates the two `P2` fixtures (`C11`) without breaking any of the 8 existing `evaluate_property_flow` call sites and adds focused assertions for `RV-001`-`RV-003` (extend assertions slightly for `PC-001` and `PC-002`); `P02-T02` covers docs, validation, and local commit. |

## Verdict

* Verdict: Revise
* Rationale: The candidate `c1` plan and phase details accurately target `RV-001`, `RV-002`, and `RV-003` and proactively prevent `dataclasses.asdict()` (`C12`) and `P2` test-fixture (`C11`) regressions, while two narrow fail-closed edge cases in `P01-T01`/`P01-T02` (`PC-001` on unconditional pre-early-return / pre-`replace` digest verification and `Mapping` gap checks in `enforce_governance_guard`, and `PC-002` on scoping `duplicate_candidate_ids` to `in_window <= as_of`) need direct planner clarification before implementation.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Tighten `verify_digest()` timing and `Mapping` gap/handover checks across `validate_flow_report` and `enforce_governance_guard`

* Related IDs: Caller Req 1, Caller Req 2, `RV-001`, `RV-002`, `FR-C1-1`, `FR-C1-3`, `AC-C1-1`, `AC-C1-3`, `P01-T01`, `P02-T01`, `C4`, `C6`, `C8`, `C9`
* Evidence: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md (`P01-T01`, `P02-T01`), src/core/src/zava_forward/core/discovery_contract.py (lines 1425-1444, 1992-2046)
* Concern: Three subtle control-flow paths in `src/core/src/zava_forward/core/discovery_contract.py` could bypass the planned `RV-001`/`RV-002` checks if `P01-T01` item 4 is implemented literally as `"whenever owner_validated=True"`: (1) `enforce_governance_guard` (`lines 2020-2026`) returns early when `owner_validated is False`, so placing `verify_digest()` after that early return would let tampered candidate `FlowDiscoveryReport` or `Phase0DiscoveryPack` objects pass `enforce_governance_guard(report)` without raising `GovernanceViolationError`; (2) if an existing `FlowDiscoveryReport` is tampered with via `object.__setattr__(report, "calculation_digest", "")` alongside a payload mutation, `validate_flow_report`'s `replace(report, ...)` (`line 1435`) would pass `calculation_digest=""` into `FlowDiscoveryReport.__post_init__` and mint a new digest over the tampered payload unless `verify_digest()` rejects blank digests and executes before `replace(...)`; and (3) `enforce_governance_guard` accepts serialized `Mapping` outputs (`lines 1998-2006`), which would still allow `owner_validated=True` mappings with non-empty `"gaps"` or `"invalid_accepted_handover_ids"`.
* Impact: Leaves low-level tamper and serialized-mapping promotion loopholes open in `validate_flow_report` and `enforce_governance_guard` and risks a mismatch with `P02-T01`'s tamper-refusal tests.
* Smallest useful change: Specify in `P01-T01` item 4 (and include in `P02-T01`'s governance tests) that: (a) `FlowDiscoveryReport.verify_digest()` requires a non-blank `calculation_digest` matching the recomputed canonical SHA-256 payload digest; (b) `validate_flow_report` calls `report.verify_digest()` and checks `not report.gaps and not report.invalid_accepted_handover_ids` before `replace(...)`; (c) `enforce_governance_guard` runs `verify_digest()` unconditionally before the `if not owner_val:` early return on both `FlowDiscoveryReport` and `Phase0DiscoveryPack.flow_report`; and (d) when `owner_validated=True`, `enforce_governance_guard` also rejects `Phase0DiscoveryPack` and `Mapping` outputs with non-empty `gaps` or `invalid_accepted_handover_ids`.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Updated `P01-T01` and `P02-T01` in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md and `FR-C1-1`, `FR-C1-3`, and `## Critique Disposition` in .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan.md recording these exact guard invariants.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Low]: Scope `duplicate_candidate_ids` in `evaluate_property_flow` to filtered in-window `<= as_of` candidates

* Related IDs: Caller Req 1, `RV-001`, `FR-C1-2`, `AC-C1-2`, `P01-T02`, `P02-T01`, `C5`
* Evidence: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md (`P01-T02`), src/core/src/zava_forward/core/discovery_contract.py (lines 1130-1145)
* Concern: `evaluate_property_flow` currently computes `id_counts = Counter(c.property_id for c in candidates)` and `duplicate_ids` at lines 1130-1131 before filtering `candidates` for usable `identified_at`, `[window_start, window_end]` membership, and the new `ident_dt.date() <= as_of` cutoff in `P01-T02` item 1. Leaving `id_counts` over raw `candidates` lets post-`as_of` or out-of-window candidate records leak into `FlowDiscoveryReport.duplicate_candidate_ids`.
* Impact: Post-cutoff candidate records (`identified_at > as_of`) can still alter a `FlowDiscoveryReport` cohort summary field despite `FR-C1-2` restricting aggregations to `baseline_candidate_ids` up to `as_of`.
* Smallest useful change: Specify in `P01-T02` item 1 that `duplicate_candidate_ids` is computed from `in_window` (valid in-window `<= as_of` candidate rows prior to `dict.fromkeys` deduplication) rather than raw `candidates`, and assert in `P02-T01` that a post-`as_of` duplicate candidate record does not populate `duplicate_candidate_ids`.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Updated `P01-T02` and `P02-T01` in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md and `## Critique Disposition` in .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan.md scoping `duplicate_candidate_ids` to `in_window`.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Strong contrarian research integration: `FrozenDict(dict)` + SHA-256 `calculation_digest` avoids the Python 3.12 `dataclasses.asdict()` `MappingProxyType` crash (`C12`) while preserving `dict[...]` typing compatibility under `mypy --strict`.
* Regression-safe existing test reconciliation: `P02-T01` explicitly updates the two `P2` candidate tuples in `src/core/tests/test_discovery_contract.py` (`C11`) and retains `unknown_or_disputed_cause` alongside `unknown_or_disputed_count`, keeping all 8 existing `evaluate_property_flow` test call sites sound, including `max(as_of_dt, start_ts)` open-clock clamping for same-day UTC timestamps.
* Accepted external residual risks: Real-world Zava North Homes human sign-off gates (`OD-14`, `OD-16`, `OD-18`, `OD-36`), absence of licensed PAS 2035:2023 clause text (`gap-pas-2035-licensed`), and deferral of optional synthetic CSV ingestion adapters remain explicitly bounded outside Phase 0 software rule-layer delivery.

## Questions or Blocking Evidence Gaps

* None. All evidence required to finalize and implement `issue-124-c1` is present in the supplied artifacts and repository files.

## Limitations

* Read-only static critique of supplied planning artifacts and target `src/core` / `docs/` files; runtime test, lint, and `mypy` verification executes during `rpi-implement` under `P01` and `P02`.

## Recommended Next Action

* Highest-impact finding: `PC-001` [Medium]
* Action owner: planning parent (`rpi-plan`)
* Smallest next action: Apply direct planner corrections for `PC-001` and `PC-002` in `.copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan.md` and `.copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md`, record `resolved` critique dispositions, finalize the plan without another critique pass, and continue to `rpi-implement`.
* User response required: no
