<!-- markdownlint-disable-file -->
# Review: Phase 0 Retrofit-Flow Discovery Contract c1 Remediation (Issue #124)

## Scope and Evidence

* Task ID: issue-124-c1
* Review date: 2026-11-15
* Review scope: full task (`P01` and `P02`: `P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`)
* Assessed boundary: Remediation of prior review findings `RV-001`, `RV-002`, and `RV-003` from .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md plus critique dispositions `PC-001` and `PC-002`, across `src/core/src/zava_forward/core/discovery_contract.py`, `src/core/tests/test_discovery_contract.py`, `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and `docs/reference/log.md` at commit `4e5f033a9` on `feat/gov-124-phase0-discovery` under the focused validation tier (`TMPDIR=/dev/shm`).
* Plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-c1-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md; .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md; commit `4e5f033a92629cb6fe53704f8ee765bd48f12b11`; focused `unittest` (`test_discovery*.py`, `test_live_doc_links.py`, `test_dependency_rule.py`), `ruff`, and `mypy` verification.

## Opening Review State

* Interpreted review goal: Verify once and from evidence whether commit `4e5f033a9` completely resolves `RV-001`, `RV-002`, and `RV-003` (including `PC-001` and `PC-002`), satisfies `FR-C1-1`–`FR-C1-5`, `NFR-C1-1`–`NFR-C1-2`, and `AC-C1-1`–`AC-C1-6`, reconciles all RPI artifacts, and leaves no regressions or open defects.
* Review scope: full task (`P01` and `P02`)
* Evidence readiness: Ready — plan (`P01`, `P02` checked `[x]`), phase details, single plan critique (`PC-001`, `PC-002` resolved), changes record (`Status: Complete`), research (`C1`–`C12`), and committed source/test/doc diff (`4e5f033a9`) are present and reconciled.
* Acceptance basis: `FR-C1-1`–`FR-C1-5`, `NFR-C1-1`–`NFR-C1-2`, `AC-C1-1`–`AC-C1-6`, critique dispositions `PC-001` and `PC-002`, and caller remediation contract for `RV-001`, `RV-002`, and `RV-003`.
* First comparison boundary: Plan-to-change reconciliation and adversarial semantic inspection of `src/core/src/zava_forward/core/discovery_contract.py` and `src/core/tests/test_discovery_contract.py` against `RV-001`–`RV-003` and `PC-001`–`PC-002` (strictly read-only outside this review log).
* Active read-only boundaries: Read-only across all repository code, tests, docs, research, plan, details, critique, and changes artifacts; write authority restricted solely to .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c1-review.md (and parent RPI state JSON upon handoff).
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full-task comparison of commit `4e5f033a9` against .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan.md, .copilot-tracking/details/2026-11-15/phase0-retrofit-flow-discovery-124-c1-phase-details.md, .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan-critique.md, .copilot-tracking/changes/2026-11-15/phase0-retrofit-flow-discovery-124-c1-changes.md, and independent adversarial `rubber-duck` inspection on 2026-11-15.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Phase P01 — Core Discovery Contract Hardening (`P01-T01`, `P01-T02`) | Reconciled | Source edits match planned markers; adversarial inspection found 5 bypass/boundary defects (`RV-001`–`RV-005`) routed to `rpi-implement`. |
| `P02` (`P02-T01`, `P02-T02`) | Phase P02 — Unit Tests, Documentation Sync, and Focused Validation (`P02-T01`, `P02-T02`) | Reconciled | `25` unit tests (`94` across `test_discovery*.py`), doc sync, `ruff`, `mypy`, and local commit `4e5f033a9` match the changes record; uncovered bypass paths require targeted test additions in `c2`. |
| `Follow-Up Items` | Optional CSV extract adapter | Reconciled | Preserved outside active `P01`/`P02` scope. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/discovery_contract.py` | Added `FrozenDict`, `calculation_digest`, `validated_role == owner_role` spec checks, canonical `1..10` `REQUIRED_FLOW_STAGE_CODES` order, and gap/invalid-handover promotion refusal | Commit `4e5f033a9` | `94` `test_discovery*.py` tests, `ruff`, `mypy` passed | Partial defect: `validated_role` and canonical stage order are solid, but `calculation_digest` blank reset (`RV-001`), `Mapping` guard bypass (`RV-002`), and `FrozenDict.__init__` re-init (`RV-003`) remain. |
| `P01-T02` | `src/core/src/zava_forward/core/discovery_contract.py` | Restricted cohort aggregations to `baseline_candidate_ids <= as_of`, grounded `zero_event_candidate_ids` strictly in lifecycle events, and added `unknown_cause_count` / `disputed_cause_count` | Commit `4e5f033a9` | `94` `test_discovery*.py` tests, `ruff`, `mypy` passed | Partial defect: lifecycle-only `zero_event_candidate_ids` and `RV-003` wait cause counters are solid, but incomplete active-work post-`as_of` ordering (`RV-004`) and `window_end` `23:59:59` fractional-second cutoff (`RV-005`) remain. |
| `P02-T01` | `src/core/tests/test_discovery_contract.py` | Updated 2 `P2` candidate fixtures (`0` removed tests) and added 7 focused unit tests | Commit `4e5f033a9` | `Ran 94 tests in 0.203s — OK` | Reconciled for tested paths; needs regression assertions for `RV-001`–`RV-005`. |
| `P02-T02` | `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md` | Updated Phase 0 contract docs and KB changelog with zero `.copilot-tracking/` references | Commit `4e5f033a9` | `test_live_doc_links.py`, `test_dependency_rule.py` (`Ran 4 tests — OK`) | Reconciled (`RV-001`–`RV-005` code tightenings will bring runtime behavior fully into alignment with documented guarantees). |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `## Dependencies` in `phase0-retrofit-flow-discovery-124-c1-plan.md` | Recorded ephemeral `/dev/shm/zf-124-c1-venv` `.pth` shim used when `test_discovery_assistant_demo.py` invokes `python3 -m zava_forward.core` | Shared `~/.local` editable install pointed at another worktree; no scope or AC change | Synchronized in plan `## Dependencies` and changes record | Not needed (local execution environment detail preserving approved intent) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001` and `PC-002` in .copilot-tracking/reviews/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c1-plan-critique.md were both recorded as `resolved` in `## Critique Disposition`.
* Material revisions: No material implementation-time scope or requirement revisions occurred.
* Dependent-work pause assessment: No dependent-work pause was needed or bypassed.
* Justification assessment: Critique dispositions were implemented, though adversarial review identified deeper bypass vectors (`RV-001`–`RV-005`) requiring a focused `c2` implementation pass.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Optional CSV extract adapter mapping synthetic year-one CSV tables into `discovery_contract` dataclasses | Phase 0 contract remains a pure rule-and-evidence layer | Sponsor / future implementation task | Distinct follow-up route (not a defect) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Blank `calculation_digest=""` reset via `dataclasses.replace` bypasses evaluated report provenance and promotion checks

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`FlowDiscoveryReport.__post_init__` and `validate_flow_report`)
* Impact: Calling `replace(gapped_report, gaps=(), calculation_digest="")` or `replace(validated_report, state_counts={"paused": 99}, calculation_digest="")` triggers blank-digest auto-generation in `FlowDiscoveryReport.__post_init__`, allowing synthetic or altered `FlowDiscoveryReport` instances not produced by `evaluate_property_flow` to pass `validate_flow_report` or claim `owner_validated=True`.
* Destination: `rpi-implement`
* Smallest useful next action: Require non-blank verified `calculation_digest` whenever `owner_validated=True` or `finding_status != CANDIDATE_FINDING_STATUS`, record evaluated report digests in a module-private provenance registry inside `evaluate_property_flow`, and require `calculation_digest` membership in that evaluated provenance set inside `validate_flow_report`, owner-validated `FlowDiscoveryReport.__post_init__`, `Phase0DiscoveryPack`, and `enforce_governance_guard`.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: `enforce_governance_guard` on `Mapping` payloads skips nested `FlowDiscoveryReport` dataclass instances and serialized flow-report digest verification

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`enforce_governance_guard`)
* Impact: A validated `Mapping` containing a `FlowDiscoveryReport` object under `"flow_report"` (rather than a nested `Mapping`) skips gap, invalid-handover, `owner_validated`, and `verify_digest()` checks; similarly, a serialized `FlowDiscoveryReport` mapping (`asdict(validated_report)`) with mutated counts passes `enforce_governance_guard` without recomputing and verifying `"calculation_digest"`.
* Destination: `rpi-implement`
* Smallest useful next action: Recursively validate nested `FlowDiscoveryReport` instances inside `Mapping` payloads (requiring `owner_validated=True` when the parent mapping claims owner validation) and verify `"calculation_digest"` integrity (plus evaluated provenance when `owner_validated=True`) on serialized flow-report mappings (both top-level and nested `"flow_report"`).

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: `FrozenDict` remains mutable via inherited `dict.__init__` re-initialization

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`FrozenDict`)
* Impact: Calling `report.state_counts.__init__({"paused": 42})` mutates the underlying dictionary in place without raising `TypeError`, violating the immediate container-immutability guarantee prior to a subsequent `verify_digest()` call.
* Destination: `rpi-implement`
* Smallest useful next action: Override `FrozenDict.__init__` with an instance-level lock attribute (`_frozen`) so any post-construction `__init__` call raises `TypeError`.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Incomplete active-work timestamp pair bypasses post-`as_of` cutoff filtering in `evaluate_property_flow`

* Related scope: `P01-T02`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`evaluate_property_flow` stage active-work branch)
* Impact: When `active_started_at` is after `as_of` and `active_completed_at` is blank (or vice versa), `if act_s is None or act_e is None:` executes before `elif act_s.date() > as_of or act_e.date() > as_of:`, retaining the stage row instead of recording the post-`as_of` gap and excluding it.
* Destination: `rpi-implement`
* Smallest useful next action: Check `(act_s is not None and act_s.date() > as_of) or (act_e is not None and act_e.date() > as_of)` before the incomplete-pair branch so any post-cutoff active timestamp records a post-`as_of` gap and skips the record.

<!-- rpi:review id=RV-005 -->
### RV-005 [Medium]: `window_end` `23:59:59` timestamp boundary excludes final-second fractional timestamps on `window_end`

* Related scope: `P01-T02`
* Evidence: `src/core/src/zava_forward/core/discovery_contract.py` (`evaluate_property_flow` candidate window boundary)
* Impact: Constructing `w_end = datetime(window_end.year, window_end.month, window_end.day, 23, 59, 59, tzinfo=UTC)` silently classifies a valid `window_end` timestamp with microseconds (for example `23:59:59.500000Z`) as outside the baseline window without recording a gap.
* Destination: `rpi-implement`
* Smallest useful next action: Compare UTC calendar dates (`window_start <= sel_dt.date() <= window_end`) so the full `window_end` UTC day including fractional seconds is included consistently with `sel_dt.date() > as_of`.

## Defects

* `RV-001` [High] -> `rpi-implement`
* `RV-002` [High] -> `rpi-implement`
* `RV-003` [Medium] -> `rpi-implement`
* `RV-004` [Medium] -> `rpi-implement`
* `RV-005` [Medium] -> `rpi-implement`

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Child remediation task `issue-124-c2` | Implementation defect within accepted immutability/provenance design |
| `RV-002` | `rpi-implement` | Child remediation task `issue-124-c2` | Implementation defect in `Mapping` governance guard |
| `RV-003` | `rpi-implement` | Child remediation task `issue-124-c2` | Implementation defect in `FrozenDict.__init__` lock |
| `RV-004` | `rpi-implement` | Child remediation task `issue-124-c2` | Implementation defect in stage active-timestamp `as_of` ordering |
| `RV-005` | `rpi-implement` | Child remediation task `issue-124-c2` | Implementation defect in `window_end` UTC date comparison |

Later implementation of a routed finding does not require another Review inside `issue-124-c1`; child automatic loop `issue-124-c2` will execute its own single Review to establish final conformance.

## Residual Work

* Optional CSV extract adapter mapping synthetic year-one CSV tables into `discovery_contract` dataclasses (non-blocking follow-up item outside Phase 0 rule-layer scope).

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none inside `issue-124-c1` (`P01` and `P02` executed; `RV-001`–`RV-005` routed to `issue-124-c2`).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PATH="/dev/shm/zf-124-c1-venv/bin:$PATH" TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_discovery*.py' -v` | `src/core/tests/test_discovery*.py` | Passed | `Ran 94 tests in 0.203s — OK` |
| `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_live_doc_links.py src/core/tests/test_dependency_rule.py -v` | Live doc links & dependency rules | Passed | `Ran 4 tests in 3.760s — OK` |
| `cd src/core && TMPDIR=/dev/shm python3 -m ruff check . && TMPDIR=/dev/shm python3 -m ruff format --check . && TMPDIR=/dev/shm mypy` | `src/core` lint, format, strict typing | Passed | `All checks passed!`, `310 files already formatted`, `Success: no issues found in 363 source files` |
| Full `src/core` `unittest discover` (`3,730` tests) | Unrelated `src/core` modules | Skipped | Explicit caller instruction to run focused validation tier only |

## Outcome

* Outcome: Defects found
* Outcome rationale: While `validated_role == owner_role` spec checks, canonical `1..10` stage ordering, lifecycle-only `zero_event_candidate_ids`, and separate `unknown_cause_count` / `disputed_cause_count` counters are conformant, adversarial verification exposed 2 High (`RV-001`, `RV-002`) and 3 Medium (`RV-003`–`RV-005`) implementation bypasses/edge defects in `discovery_contract.py` that must be closed before recording a `Conformant` verdict.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` (`RV-001`–`RV-005`) | Execute child remediation task `issue-124-c2` |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | Distinct follow-up | Optional CSV extract adapter (deferred) |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: Focused unit tests (`94 + 4`), `ruff`, and `mypy` passed; adversarial review uncovered 5 untested edge/bypass cases (`RV-001`–`RV-005`).
* Blockers: none
