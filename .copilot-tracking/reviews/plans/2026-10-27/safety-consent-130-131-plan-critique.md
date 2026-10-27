---
title: Safety-consent 130-131 final-candidate plan critique
description: One independent assessment of the bounded intake and unknown-tenure hold plan
ms.date: 2026-10-27
---

## Metadata

* Task ID: 130-131
* Task slug: safety-consent-130-131
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/safety-consent-130-131-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/safety-consent-130-131-phase-details.md
* Critique execution status: Complete
* Assessment count: exactly one final-candidate critique; no nested delegation.

## Inputs and Criterion Boundary

* Read the supplied plan, phase details and .copilot-tracking/research/2026-10-27/safety-consent-130-131-research.md, including C1-C11, the decision state and bounded acceptance criteria.
* Read the required repository context: docs/reference/README.md, docs/reference/memory.md, docs/case_study_48_original.md, the opening scope of docs/case_study_48_addendum.md and the sector primer. Memory is context, not delivery evidence.
* Used cited implementation evidence only where necessary: resident transaction and SQL replay, representative authority, resident gates, retention deletion, projection and API resident dispatch. Compared C1/C2 with the BRD FR-037/AC-065 and FR-015/AC-021 text. Existing resident tests supplied examples of the writer-race contract.
* Caller direction controls: full ordered RPI for #130/#131, one draft PR, Refs unless all criteria are proven, independent implementation followed by a stop at actual owner/Legal/DPO/Compliance decisions. No invented operational authority, Azure, secrets, .env, private datasets or uv. No --all; at most one locked --changed for large changes, with none planned for this bounded slice.
* Assessment covers the proposed ledger intake and registered-unresolved-tenure hold, P01-T01, P01-T02 and P02-T01, their dependency order, acceptance evidence and publication limits. It does not demand implementation of excluded eligibility, verified tenure, legal interpretation, participation validation or whole-programme coverage.
* Test ownership is fixed: existing core resident JSON/SQLite tests and existing API resident tests; no removals and at most 12 new methods. Findings below must fit that contract, not expand the runner or introduce cloud validation.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| #130/#131 scope and publication | Covered | Partial/blocked status, Refs, one draft PR and no whole-issue closure are explicit. |
| FR-037/AC-065, C1, P01-T01 | Partial | Accounts, channels and review owner are specified; correctable subject identity is not yet a defined revision contract: PC-002. |
| FR-015/AC-021, C2, P01-T02 | Partial | Unknown verification and no release action are explicit; affected scope and unresolvable household binding need a fail-closed rule: PC-001. |
| C3/C6/C8/C11, human decision boundaries | Covered | No new representative grants, Legal role, actual participation or appointment is claimed. Preserve these exclusions. |
| C4/C5, P01 transaction and SQL validation | Partial | Reuse is credible, but planned proof omits specific writer-race/replay outcomes: PC-003. |
| C7/C10, raw intake access and projection | Partial | Dual entitlement is required; restoration, alternate read paths and current-registry denial need explicit evidence: PC-003. |
| C9, hazard separation | Covered | Explicit refusal before nomination write and independent hazard intake; no clock or classification authority is added. |
| Retained sensitive accounts and unresolved holds | Partial | Existing deletion behavior makes field placement consequential; lifecycle and hold survival are unspecified: PC-004. |
| P02-T01, test ownership and maximum | Covered with required refinement | No removals and <=12 new methods are locked. Refine assertions within that budget, not by adding another suite. |
| P01-T02 dependency and P02 evidence handoff | Covered | Shared transactional foundation precedes dependent holds; validation and publication follow both. |

## Verdict

* Verdict: Revise
* Severity summary: 3 High, 1 Medium; 0 Critical, 0 Low.
* The bounded approach is credible and correctly refuses whole-issue acceptance. Four substantive contract/evidence gaps require direct planner corrections before implementation. None justifies inventing a human decision or expanding the agreed slice.
* Execution is Complete, independently of the Revise verdict. The planning parent should dispose of this single complete finding set and finalize without a second critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Define a fail-closed affected scope for unresolved household identity

* Related IDs: C2; FR-015/AC-021; P01-T02; bounded tenure acceptance criterion.
* Evidence: .copilot-tracking/details/2026-10-27/safety-consent-130-131-phase-details.md, P01-T02, specifies a case/household reference, Unknown/Ambiguous identity and refusal of "affected unresolved intake." It does not define how an unverified household is bound or what "affected" means. src/core/src/zava_forward/core/resident_decisions.py:506-542 gates case/measure bindings, not household bindings. The BRD explicitly forbids transferring one household's agreement to another.
* Concern: The proposed gate could depend on an unverified reference to determine applicability. A report that is registered but cannot be mapped confidently must not become irrelevant to the gate. Declaring whole-programme enumeration incomplete does not resolve safety within registered cases.
* Impact: Accepted resident decisions or a newly recorded scope could appear sufficient despite registered unresolved tenure, especially for ambiguous or several-household reports.
* Smallest useful change: State the bounded hold rule explicitly. Any registered unresolved tenure report holds the containing case's affected non-urgent work; without a verified narrower mapping, use a conservative case-wide hold. Reject conflicting explicit case bindings. Permit unknown household identity as unresolved evidence without asserting verified membership or silently dropping the hold. Scope changes, disputes, package completion and another household's acceptance must not release it. Keep independent urgent hazard response available.
* Action owner: Planning parent, then P01-T02 implementer.
* Exact resolving evidence: Revised plan/details define the binding, hold predicate and unknown/ambiguous fallback. Existing JSON/SQLite resident tests and API tests demonstrate registered Unknown/Ambiguous and multiple reported households holding despite otherwise valid acceptance, including scope-change attempts, SQL reopen and unchanged independent hazard behavior. No release or identity-verification authority is added.
* Decision route: Direct planner correction. Actual household verification and future narrower release policy remain human-needed Legal/Home Ownership/owner decisions; they are not required to implement the conservative hold.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Make nomination subject identity correctable without changing authority

* Related IDs: C1/C6; FR-037/AC-065; P01-T01; wrong-case/identity and unrelated-state acceptance criteria.
* Evidence: .copilot-tracking/plans/2026-10-27/safety-consent-130-131-plan.md requires explicit case binding and corrections retaining competing accounts. P01-T01 in the phase details defines correction of the account but no reported subject/identity revision fields or wrong-person correction behavior. docs/brds/agentic-retrofit-programme-brd.md:1635 requires a preserved original account with correctable identity. Existing authority_for and decision_record in src/core/src/zava_forward/core/resident_decisions.py distinguish task-limited representative authority from supplied consent.
* Concern: "Identity/support/risk remain Unknown" is safe against invented verification but is not a correction contract. A staff-authenticated nomination may still describe the wrong person. A trusted-intermediary channel or existing representative grant must not silently resolve that ambiguity or become works consent.
* Impact: An account-only correction can leave the wrong subject association in current views, or a later implementation can accidentally reuse an intake association as verified identity/authority.
* Smallest useful change: Define the minimal reported-subject reference and explicit unverified identity state, plus append-only subject correction provenance. Preserve the old association/account, keep competing evidence visible and mark that nomination for review. Reject silent cross-case transfer; route an erroneous case association for human reconciliation without rewriting the original. State that nomination intake/correction neither creates nor validates representative grants, measure decisions or consent, even where an existing grant is present.
* Action owner: Planning parent, then P01-T01 implementer.
* Exact resolving evidence: Revised closed input/revision contract identifies what can be corrected and what remains Unknown. Tests show wrong-person correction history and SQL reopen, cross-case denial without mutation, and unchanged consent, representative authority, ranking and support status for resident, intermediary and existing-representative examples.
* Decision route: Direct planner correction for unverified evidence capture. Identity eligibility and actual representative validation remain human-needed owner/Resident Engagement/DPO decisions under OD-41/42, not defaults.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Lock replay and projection assertions within the existing test budget

* Related IDs: C4/C7/C10; P01-T01/P01-T02; P02-T01; transactional and dual-entitlement NFRs.
* Evidence: The plan requires CAS, revalidation, rollback, private reads and SQL reopen, but its validation contract does not explicitly require commit-time interleavings or intake-specific read canaries. src/core/src/zava_forward/core/resident_decisions.py:151-171 replays each action on a detached current SQL case, and :361-422 distinguishes precommit rollback from committed confirmation failure. src/core/src/zava_forward/core/projection.py:147-187 copies resident fields and restores them after note redaction. src/api/src/zava_forward/api/server.py:999-1023 returns projected detail after persistence. Existing SQL resident tests include writer-time owner/actor changes.
* Concern: Sequential stale-version and persistence tests do not establish that new actions remain safe when replayed. Likewise, adding fields to resident_data or relying on generic note-key redaction can expose new account/source fields despite the intended dual entitlement. These are known integration-sensitive contracts, not merely a request for more general testing.
* Impact: Replay could duplicate revisions or external side effects; revoked actors/owners could commit; free text could survive redaction or cached identity checks. A response failure could be misreported as an uncommitted write and retried.
* Smallest useful change: Require replay-safe handlers with writes confined to the supplied case and audit details limited to non-sensitive identifiers. Add explicit assertions for writer-time actor/assignee change, competing revisions, rollback and truthful committed outcomes. Specify intake allow/deny projection before resident-data restoration, with canaries across detail, mutation response and applicable existing export/prompt paths; denied roles receive at most non-sensitive hold information. Do not rely on new field names being covered by NOTE_KEYS.
* Action owner: Planning parent for the validation allocation; implementer for core/API assertions.
* Exact resolving evidence: Revised P02 validation mapping stays <=12 new methods across the two named test files, with no removals. It allocates shared JSON/SQLite history/hold/identity assertions, SQL-specific interleaving/failure assertions and API schema/current-registry/projection assertions. Results prove one durable revision and success audit per successful command, no state/audit mutation on precommit denial, no replay side effects, current dual-entitlement denial after registry change, and no raw canary in denied outputs. Existing postcommit regression coverage is retained; any extension needed uses the same budget.
* Decision route: Direct planner correction. No new permission, scanner, SQL service, cloud run or human operational approval is requested.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Separate intake evidence lifecycle from the unresolved safety hold

* Related IDs: C10; P01-T01/P01-T02; revision preservation and no-silent-release requirements.
* Evidence: The plan promises retained account/tenure revisions and no release action, but does not state their relationship to existing retention deletion. src/core/src/zava_forward/core/resident_decisions.py:587-605 deletes every RESIDENT_FIELDS entry when existing resident-record deletion is authorized; the same constant participates in projection. The new ledgers' placement therefore affects both privacy and gate survival.
* Concern: Excluding new sensitive records from existing deletion handling can retain evidence outside its intended lifecycle; adding the entire ledger/hold to the deletion set can silently remove the unresolved-tenure gate. Neither behavior is an authorized retention or release decision.
* Impact: The independent slice could accidentally extend personal-data retention or clear a registered hold through an unrelated existing deletion path.
* Smallest useful change: Document field placement and lifecycle explicitly. Do not invent a new retention duration, lawful basis or operational policy. Preserve an appropriate non-sensitive unresolved hold independently of deletable account evidence so evidence deletion is not tenure approval. If applicability of existing retention authority is not established, mark real intake activation blocked pending DPO/Compliance/owner confirmation, while continuing only synthetic constructed implementation.
* Action owner: Planning parent and implementer for lifecycle separation and blocker documentation; DPO/Compliance/owner for actual retention applicability and operational activation.
* Exact resolving evidence: Revised details identify the evidence fields, hold marker and existing deletion interaction; a focused assertion within the fixed test budget proves applicable deletion cannot create permission to progress, legal-hold behavior remains intact, and no fresh retention authority is claimed. PR blocker matrix identifies the unresolved human approval rather than treating test data as approval.
* Decision route: Direct planner correction now. Any new retention policy or real-data activation is human-needed and remains stopped; no user response is required for the synthetic slice.

## Strengths and Residual Risk

* The distinction between bounded implementation criteria and issue criteria is strong. Preserve Refs #130 and Refs #131, unproven checkboxes and the criterion-by-criterion partial/blocked PR matrix.
* Existing transactional resident dispatch is a credible foundation; a new service, parallel authorization mechanism or generic challenge engine is unnecessary.
* Staff acknowledgement evidence is not message delivery. A static question checklist is not a Legal-reviewed answer pack. These boundaries are explicit and should remain so.
* Missing all-home/all-household enumeration, actual participation, OD-41/42, Legal appointment, verified tenure/representatives and approved responsibility/cost remain accepted exclusions for this slice, not waived issue criteria.
* The explicit user prohibition on --all controls. This critique does not request that gate, a cloud fallback, a skipped check represented as passing or a protection change.

## Questions or Blocking Evidence Gaps

* No significant or divergent user decision is needed to revise the bounded plan.
* Actual owner, Legal, DPO and Compliance evidence remains unavailable for operational extensions. Keep those stops in the plan, implementation documentation and draft PR; synthetic tests cannot supply it.

## Limitations

* This is a plan credibility assessment, not an implementation review, vulnerability assessment, conformance claim or legal opinion.
* No tests, cloud operations, private-data inspection or live identity validation were performed. Issue text was considered through the supplied research; no new external research was performed.
* Sources, phase details and research were not modified. Only this requested critique artifact was written; existing untracked parent artifacts were left untouched.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Define the fail-closed registered-tenure hold and ambiguous-household fallback in P01-T02, then directly resolve PC-002 through PC-004 within the existing slice and test budget.
* User response required: No for planner corrections and independent synthetic implementation. Yes only before a later operational extension requiring actual owner/Legal/DPO/Compliance authority.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/safety-consent-130-131-plan.md](.copilot-tracking/plans/2026-10-27/safety-consent-130-131-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-27/safety-consent-130-131-phase-details.md](.copilot-tracking/details/2026-10-27/safety-consent-130-131-phase-details.md) | Assessed implementation and validation details |
| [.copilot-tracking/research/2026-10-27/safety-consent-130-131-research.md](.copilot-tracking/research/2026-10-27/safety-consent-130-131-research.md) | Supplied evidence and human decision boundaries |
| [.copilot-tracking/reviews/plans/2026-10-27/safety-consent-130-131-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/safety-consent-130-131-plan-critique.md) | Complete single critique and actionable finding set |

## Next Steps

The active planning parent should revise and disposition PC-001 through PC-004 directly, preserve this original Revise outcome and finalize without another critique. Continue the ordered RPI only after disposition, retain the fixed test budget and draft-only partial-scope publication, and stop at the documented human authority gates. No user action is required for those direct corrections. This critique does not invoke another RPI stage.
