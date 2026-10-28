<!-- markdownlint-disable-file -->
---
title: Resident chat 520 expiry follow-up independent plan critique
ms.date: 2026-10-28
---

## Metadata

* Task ID: 520-expiry-followup
* Critique date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/resident-chat-520-expiry-followup-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/resident-chat-520-expiry-followup-phase-details.md
* Critique execution status: Complete
* Assessment: Exactly one independent final-candidate critique.
* Inspected source head: 72a7810189db0994111b0a2d9b3341bd002f2f17
* Branch: feat/resident-chat-520, tracking origin/feat/resident-chat-520.

## Inputs and Criterion Boundary

* Caller requirements: Resolve PR #525 thread PRRT_kwDOUU8JX86xTMcu with the smallest post-authorization proposal-expiry correction. Preserve slot-start checks, authorization, idempotency and transaction rollback. Use an injected clock, one new unit test method maximum, boundary subtests and persisted rollback/availability evidence.
* Planning inputs: The supplied plan, phase details and research at their paths below, including research Q1/Q2, C1-C6 and W1.
* Directly inspected implementation evidence: src/api/src/zava_forward/api/resident_demo/agenda.py, src/api/src/zava_forward/api/resident_demo/app.py:470-555, src/api/tests/test_resident_chat_agenda.py, src/api/tests/test_resident_chat_api.py:338-380, and the constructed HTTP fixture in src/api/tests/test_resident_demo_api.py:143-182.
* Validation evidence considered: src/api/pyproject.toml; callback contract and focused commands in src/api/README.md:108-205; local gate distinctions in src/README.md:62-145; bounded selector inspection of test_resident_assistant_api, test_resident_aoai and test_resident_assistant_provider.
* Project context: docs/case_study_48_original.md, the relevant opening of docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/memory.md and docs/reference/research/sector/housing-association-primer.md. These do not establish live appointment authority.
* Decisions and dependencies: P01-T01 precedes regression/static validation in P01-T02; P02 depends on completed P01 evidence. The owner authorizes normal push followed by the named thread reply/resolution, but excludes az, full-gate attempts, deployment, merge and force push. Browser execution is conditional on browser-facing changes and is not required for this backend-only candidate.
* Assessment boundary: Plan credibility and implementation readiness, not implemented correctness, executed validation, publication approval, accessibility acceptance or whole-issue acceptance. Supplied W1 and missing-tool observations are research evidence, not freshly repeated external/tool probes.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, C1, P01-T01: select expiry and recheck both deadlines | Covered | Agenda.book currently selects only s.* and checks only starts after authorised(). Selecting o.expires and comparing both against one fresh final instant directly closes the identified race. |
| C2, P01-T01: transactional rollback | Covered | Agenda._transaction rolls back exceptions before closing. Raising AgendaConflict after insertion and authorization remains inside this boundary. |
| C3, Q2, P01-T01: deterministic semantic regression | Covered | Existing NOW and next-day slots isolate expiry. Authorization advances callable time from expiry minus one second to minus one microsecond, exact expiry or plus one microsecond; asserting invocation distinguishes a delayed-authorization test from an initially expired lookup. |
| P01-T01: ownership and maximum additions | Covered | Canonical target is src/api/tests/test_resident_chat_agenda.py; maximum one new method with subtests, no removals and no generated targets. Cancellation or distinct owners prevents success-case contamination. |
| P01-T01: red/green and persisted availability | Covered | Preserve failure against original agenda.py before the fix. Reopen Agenda after rejected confirmations, require empty own(), then find/book the same original slot for another owner at the final instant. This checks durable rollback and the free-slot constraint, not merely an exception. |
| C1/C3, functional requirements: preserved behavior | Covered | The selected edit leaves committed-booking lookup/return and authorization ordering untouched. Existing tests cover static datetime callers, idempotent retry, cancellation, revocation rollback, competition and final slot-start rejection. |
| C4: API contract | Covered | The HTTP book handler already supplies callable app.now and maps AgendaConflict to 409. No endpoint, signature or browser change is needed. |
| C5, P01-T02: focused tests and package static checks | Covered | All six selectors are named; shared fixture paths are specified. API configuration supplies Ruff100 and strict mypy over src, tests and checks. Planned check/format commands preserve configured exemptions rather than silently widening scope. |
| P01-T02: heavy admission and dependency restoration | Covered | Nonblocking shared-lock attempts every 60 seconds for at most 40 minutes, held for heavy operations, match owner direction. Existing pinned dev dependencies follow recorded missing-tool observations; no dependency-manifest change is planned. |
| P01-T01: directly related documentation | Covered | src/api/README.md describes proposal expiry and confirmation checks; the planned single clarification belongs in that existing contract. |
| C6, P02: evidence, review and publication | Covered | Independent Review follows actual validation; original outcomes remain. Fetch/reconcile authorized bot advancement, rerun affected checks after rebase, normal push, remote-head verification and named-thread verification are explicit. |
| Owner prohibitions and inherited acceptance | Covered | No az/full-gate attempt, browser run for unchanged browser surfaces, deployment, merge, force push, private-data inspection or issue-closing semantics. Full-gate, human/AT and hosted acceptance remain separate and unclaimed. |

## Verdict

* Verdict: Pass
* Rationale: The proposed query/final-check edit is sufficient for the observed race and preserves the existing transaction and public contracts. The locked single-method regression can demonstrate all three expiry boundaries, authorization timing, durable rollback and slot reuse without sleeps or wider test changes. Validation and publication are explicitly scoped to the owner's authorization.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.

## Findings

No actionable PC-xxx findings. The complete actionable finding set is empty; no concerns are withheld for another critique.

No finding owner, resolving evidence or direct-versus-user-decision classification is applicable because no correction is requested.

## Strengths and Residual Risk

* A single final timestamp keeps expiry and slot-start comparisons coherent. The existing final slot-start regression protects that behavior while the new regression isolates expiry.
* The idempotent committed-booking path deliberately bypasses proposal expiry but still checks authorization; preserving it avoids turning a successful retry into a false expired-proposal conflict.
* Persisted rollback and another owner's successful booking of the original slot prove more than an in-memory error result.
* The plan explicitly accepts unavailable full-gate evidence and separates focused success from full receipt, human/AT, hosted and whole-feature acceptance. This critique does not remove those gates.
* Tool restoration, lock admission and possible remote advancement remain execution contingencies. None is claimed complete by a planning Pass; actual logs, exit codes, test counts and any changed assessment boundary must be retained as already planned.

## Questions or Blocking Evidence Gaps

None within the supplied planning boundary. No significant or divergent user decision is required.

## Limitations

* No regression, unit/API suite, Ruff, formatting, mypy, browser or heavy command was executed by this critique.
* No dependency installation, lock acquisition, private-data access, GitHub query/mutation, fetch, commit, rebase or push was performed.
* Live thread status and upstream movement were not independently refreshed; research W1 and the caller establish the review target. P02 owns the later remote checks.
* The recorded missing ruff/mypy probes were not rerun. Future successful restoration and validation require actual implementation evidence.
* This assessment writes only this critique artifact. Supplied plan, phase details, research, source and tests remain unchanged.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Record this single critique's Pass disposition, then proceed to P01-T01 under the existing locked test ownership and scope.
* Exact continuation evidence: Retained original red output, fixed green boundary subtests with reopened rollback and original-slot reuse assertions, all six selector results, API Ruff100/format100 and package mypy results, followed by the independent Review and verified publication/thread evidence specified in P02.
* Decision route: Direct parent continuation; no plan correction or user decision.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-28/resident-chat-520-expiry-followup-plan.md | Assessed final-candidate plan |
| .copilot-tracking/details/2026-10-28/resident-chat-520-expiry-followup-phase-details.md | Locked implementation and validation details |
| .copilot-tracking/research/2026-10-28/resident-chat-520-expiry-followup-research.md | Supplied bounded research evidence |
| .copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-expiry-followup-plan-critique.md | This original independent critique |

## Next Steps

The active planning parent may record the Pass disposition and continue to P01-T01. No user action is required. This reviewer stops after the single critique; no implementation or publication action is performed here.
