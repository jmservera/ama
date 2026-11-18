<!-- markdownlint-disable-file -->
# RPI Plan Critique: Phase 0 Retrofit-Flow Discovery Contract c2 Hardening (Issue #124)

## Metadata

* Task ID: issue-124-c2
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Remediate adversarial findings RV-001 through RV-005 from c1 review on branch feat/gov-124-phase0-discovery while preserving all previously passing 94 + 4 focused unit tests, ruff check, ruff format, and mypy strict typing; execute focused validation tier only with TMPDIR=/dev/shm and commit locally (Refs #124 plus Copilot trailer) without pushing or opening a PR.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c2-plan.md, .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md, .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c1-review.md, .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md, src/core/src/zava_forward/core/discovery_contract.py, and src/core/tests/test_discovery_contract.py.
* Decisions, dependencies, and acceptance criteria considered: FR-C2-1 through FR-C2-4, NFR-C2-1 through NFR-C2-2, AC-C2-1 through AC-C2-5, c1 findings RV-001 through RV-005, pure Python 3.12 standard-library constraint, test addition ceiling (at most 6 new tests, 0 removals), and commit 4e5f033a9 baseline.
* Assessment boundary: Evaluates completeness, bypass resistance, Python 3.12 runtime behavior, existing test compatibility, and mypy strict typing across P01 and P02 strictly from the supplied files; excludes unrelated src/core modules and external systems.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-C2-1, AC-C2-1, P01-T01 (c1 RV-001) | Partial | Leaving blank-digest auto-fill on candidate FlowDiscoveryReport plus digest-only set membership allows replace(gapped_report, gaps=(), calculation_digest="") to collide with prior clean cohort digests in the same process (such as P1 in GovernanceGuardTests), and P01-T01 omits the Phase0DiscoveryPack.__post_init__ check (PC-001). |
| FR-C2-2, AC-C2-2, P01-T01 (c1 RV-002) | Partial | _is_flow_report_mapping checks only 7 of 20 flow-unique keys, leaving partial-metric mapping bypasses, unguarded TypeError/ValueError exceptions, weak owner_validated_on / datetime-as-date checks, and skipped candidate nested-mapping guard checks (PC-002). |
| FR-C2-3, AC-C2-3, P01-T01 (c1 RV-003) | Partial | FrozenDict.__init__ runtime lock logic is sound, but (*args: object, **kwargs: object) breaks dict.__init__ overload checking and K, V type inference under mypy strict, and to_json_dict() returning _freeze_value(...) directly fails return-type checking (PC-003). |
| FR-C2-4, AC-C2-4, P01-T02 (c1 RV-004, RV-005) | Covered | Checking act_s.date() > as_of and act_e.date() > as_of before incomplete-pair handling and replacing start_dt/end_dt with window_start <= ident_dt.date() <= window_end (removing unused start_dt and end_dt locals for ruff F841) cleanly resolves RV-004 and RV-005. |
| NFR-C2-1, NFR-C2-2, AC-C2-5, P02-T01, P02-T02 | Covered | Focused test budget (0 removals, at most 6 additions in src/core/tests/test_discovery_contract.py), documentation sync without .copilot-tracking/ leaks, TMPDIR=/dev/shm validation commands, and local-only commit match caller constraints once PC-001 through PC-003 are applied. |

## Verdict

* Verdict: Revise
* Rationale: Three direct planner corrections in P01-T01 (and aligned FR-C2-1, FR-C2-2, and AC-C2-1 wording) are needed to prevent a deterministic same-cohort digest collision bypass on RV-001, close partial-key and exception gaps in the Mapping governance guard on RV-002, and keep mypy strict passing on FrozenDict and to_json_dict().

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Candidate blank-digest auto-fill and digest-only provenance allow same-cohort collision bypasses in validate_flow_report

* Related IDs: FR-C2-1, AC-C2-1, P01-T01, P02-T01
* Evidence: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c2-plan.md, .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md, src/core/src/zava_forward/core/discovery_contract.py, src/core/tests/test_discovery_contract.py
* Concern: P01-T01 still auto-populates calculation_digest when owner_validated is False and calculation_digest is blank, and tracks provenance only by digest string in _EVALUATED_FLOW_REPORT_DIGESTS. In src/core/tests/test_discovery_contract.py, GovernanceGuardTests first evaluates BaselineCandidateRecord("P1", "2026-01-10", "c-1") (registering the clean P1 digest) and later evaluates gapped_report with BaselineCandidateRecord("P1", "2026-01-10", ""). Calling replace(gapped_report, gaps=(), calculation_digest="") auto-generates the exact same 20-field SHA-256 digest already present in _EVALUATED_FLOW_REPORT_DIGESTS, so forged.verify_digest(), enforce_governance_guard(forged), and validate_flow_report(forged, ...) all pass without raising GovernanceViolationError. In addition, P01-T01 omits the Phase0DiscoveryPack.__post_init__ provenance check required by FR-C2-1.
* Impact: RV-001 remains exploitable via dataclasses.replace whenever an earlier evaluate_property_flow call produced matching aggregate outputs, and the planned AC-C2-1 regression test in GovernanceGuardTests will fail to raise GovernanceViolationError.
* Smallest useful change: Compute calculation_digest inside evaluate_property_flow via a private helper before instantiating FlowDiscoveryReport and remove blank-digest auto-fill from FlowDiscoveryReport.__post_init__ altogether (always running self.verify_digest() so replace(..., calculation_digest="") fails closed immediately in __post_init__ for both candidate and validated reports). Also stamp reports created by evaluate_property_flow (and promoted by validate_flow_report) via object.__setattr__(report, "_evaluated_provenance", _EVALUATED_PROVENANCE_TOKEN) using a module-private object() sentinel, require both _evaluated_provenance is _EVALUATED_PROVENANCE_TOKEN and calculation_digest in _EVALUATED_FLOW_REPORT_DIGESTS in validate_flow_report (blocking replace(gapped_report, gaps=(), calculation_digest=recomputed_digest) even under digest collision while keeping existing replace(validated) tamper tests working), add the calculation_digest in _EVALUATED_FLOW_REPORT_DIGESTS check to Phase0DiscoveryPack.__post_init__ when validated in P01-T01, and align FR-C2-1 and AC-C2-1 wording accordingly.
* Action owner: planning parent
* Exact resolving evidence: Updated FR-C2-1 and AC-C2-1 in .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c2-plan.md and updated P01-T01 and P02-T01 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md specifying unconditional non-blank calculation_digest verification in FlowDiscoveryReport.__post_init__, _EVALUATED_PROVENANCE_TOKEN plus _EVALUATED_FLOW_REPORT_DIGESTS enforcement in validate_flow_report, and Phase0DiscoveryPack.__post_init__ validated digest provenance check.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Mapping flow-report detection and verification leave partial-key, date-coercion, and exception-type gaps in enforce_governance_guard

* Related IDs: FR-C2-2, AC-C2-2, P01-T01, P02-T01
* Evidence: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md, src/core/src/zava_forward/core/discovery_contract.py, src/core/tests/test_discovery_contract.py
* Concern: Four edge holes exist in P01-T01's Mapping guard specification: (1) _is_flow_report_mapping checks only 7 of the 20 flow-report-unique keys, allowing a forged validated mapping carrying flow metrics such as accepted_handover_property_ids, bg011_assessment_to_ready_to_install_days, candidate_to_accepted_handover_days, or post_install_handover_legs_days without calculation_digest to bypass _verify_flow_report_mapping; (2) isinstance(value, date) in Python matches datetime instances unless isinstance(value, datetime) is excluded, and checking merely non-empty owner_validated_on accepts whitespace or non-date values; (3) unguarded date.fromisoformat or json.dumps on malformed Mapping values raises plain ValueError or TypeError rather than GovernanceViolationError; and (4) when "flow_report" is present on an unvalidated outer Mapping, P01-T01 permits flow_report=None or skips recursive enforce_governance_guard on a nested Mapping with invalid finding_status/owner_validated fields.
* Impact: Adversarial callers can bypass RV-002 with partial flow-metric mappings, non-date owner_validated_on values, or malformed nested flow_report mappings, or trigger unhandled TypeError instead of fail-closed GovernanceViolationError.
* Smallest useful change: Expand _FLOW_REPORT_SIGNATURE_KEYS in _is_flow_report_mapping to all 20 flow-report-unique keys (all 19 non-gaps digest payload keys plus "calculation_digest", all of which are disjoint from LifecycleDictionaryReport, ConstraintHypothesis, RankedConstraintRegister, and Phase0DiscoveryPack); validate date fields (window_start, window_end, as_of, and validated owner_validated_on) strictly as date excluding datetime or 10-character ISO YYYY-MM-DD strings; normalize nested Mapping/list/tuple payloads and wrap serialization/parsing errors in GovernanceViolationError; and when "flow_report" is in output (candidate or validated), reject non-FlowDiscoveryReport/non-Mapping values (including None) and validate nested Mapping instances through both _verify_flow_report_mapping and recursive enforce_governance_guard.
* Action owner: planning parent
* Exact resolving evidence: Updated P01-T01 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md (and FR-C2-2 if needed) specifying full 20-key _FLOW_REPORT_SIGNATURE_KEYS detection, strict date-not-datetime / YYYY-MM-DD parsing including owner_validated_on, GovernanceViolationError wrapping around digest canonicalization, and symmetric candidate/validated nested "flow_report" Mapping enforcement.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: FrozenDict.__init__ and FlowDiscoveryReport.to_json_dict() type annotations in P01-T01 fail mypy strict mode

* Related IDs: FR-C2-2, FR-C2-3, NFR-C2-1, P01-T01
* Evidence: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md, src/core/src/zava_forward/core/discovery_contract.py
* Concern: Defining FrozenDict.__init__(self, *args: object, **kwargs: object) -> None and calling super().__init__(*args, **kwargs) fails mypy strict checking with [call-overload] against dict[K, V].__init__ and breaks K, V inference at existing call sites such as FrozenDict(self) in __copy__ and generator calls in __deepcopy__ and _freeze_value. Additionally, FlowDiscoveryReport.to_json_dict(self) -> FrozenDict[str, object] returning _freeze_value({...}) fails [return-value] because _freeze_value returns object, and _is_flow_report_mapping(m: Mapping[str, Any]) uses Any without importing it (Mapping[str, object] avoids Any).
* Impact: P02-T02 validation command mypy (strict = true) will fail unless P01-T01 specifies strict-clean signatures up front.
* Smallest useful change: Specify typing.overload signatures on FrozenDict.__init__ covering (), (Mapping[K, V], /), (Iterable[tuple[K, V]], /), and (**kwargs: V) above a (*args: Any, **kwargs: Any) -> None implementation (importing Any, Iterable, and overload from collections.abc / typing), construct FrozenDict[str, object]((k, _freeze_value(v)) for k, v in raw.items()) directly in FlowDiscoveryReport.to_json_dict(), and type Mapping helpers with Mapping[str, object].
* Action owner: planning parent
* Exact resolving evidence: Updated P01-T01 in .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md recording strict-compatible FrozenDict.__init__ overloads, direct FrozenDict[str, object] construction in to_json_dict(), and Mapping[str, object] helper signatures.
* Decision route: direct planner correction

## Strengths and Residual Risk

* P01-T02 accurately pinpoints both timestamp boundary defects from c1 review (RV-004 active-work post-as_of check order and RV-005 UTC calendar-date comparison on window_end) without disturbing open-stage or open-wait arithmetic.
* Preserving FrozenDict as a dict subclass with __copy__ and __deepcopy__ plus adding FlowDiscoveryReport.to_json_dict() keeps dataclasses.asdict() determinism tests and plain json.dumps(...) callers working without external dependencies.
* Residual risk: _EVALUATED_FLOW_REPORT_DIGESTS is an in-memory per-process registry; cross-process verification relies on recomputing from source extracts via evaluate_property_flow, which aligns with the offline Phase 0 standard-library rule-layer scope.

## Questions or Blocking Evidence Gaps

* None. All required evidence is present in the supplied c1 review, reused research, source code, and test suite.

## Limitations

* Critique is bounded strictly to the read-only artifacts supplied by the caller; runtime test and type-checker commands were not executed during this read-only plan critique stage and remain gated in P02-T02.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Apply direct planner revisions for PC-001, PC-002, and PC-003 to .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c2-plan.md and .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c2-phase-details.md, record Critique Disposition, and finalize the plan for rpi-implement without another critique pass.
* User response required: no
