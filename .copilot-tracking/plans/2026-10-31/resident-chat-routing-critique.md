---
title: Resident chat routing independent plan critique
description: Final-candidate credibility assessment and complete actionable findings
ms.date: 2026-10-31
---

## Metadata

* Task ID: resident-chat-routing
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/resident-chat-routing-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/resident-chat-routing-phase-details.md
* Critique execution status: Complete
* Independence: final-candidate assessment by the dispatched critique worker; no implementation or nested delegation.

## Inputs and Criterion Boundary

* Caller requirements: repair rules-only routing for "How's my case going" and "Is my case blocked?"; extend bounded own-case status/blocking/waiting/update/retrofit, document/paperwork missing/receipt, forms and home/address recognition after all current exclusions. Preserve complete-message refusal, safety and specialist precedence, consent and own-case authority, and unknown behavior. Add exactly four plain refusal examples. No AI activation, deployment or expanded testing scope.
* Canonical inputs: .copilot-tracking/research/2026-10-31/resident-chat-routing-research.md (C1-C7), the plan and phase details above.
* Source evidence: src/api/src/zava_forward/api/resident_demo/chat.py; src/api/src/zava_forward/api/resident_demo/app.py:399-505; src/api/tests/test_resident_chat_api.py:1-740; src/core/src/zava_forward/core/resident_assistant.py:1-116; docs/reference/research/ux/content-standard.md:15-65; src/README.md:48-98,300-315.
* Context: docs/case_study_48_original.md; opening resident-service proposal in docs/case_study_48_addendum.md; docs/reference/README.md; docs/reference/memory.md; opening customer context in docs/reference/research/sector/housing-association-primer.md. Memory is context, not evidence.
* Decisions and dependencies: retain legacy grammar and specialist/exclusion order; finite per-topic fallback; reuse existing answers; P02 depends on P01, P03 depends on P02 and critique disposition. At most three added test methods and shared matrices in the existing resident-chat module; zero removals. Focused API unit/static checks, no heavy gate or deployment. Main PR uses Refs #520 and Refs #563, with owner/hosted approval still outstanding.
* Assessment boundary: assess the supplied candidate once for requirements, research, implementation contracts, adversarial preservation, validation lock, dependencies, publication controls and missed concerns. This is not implementation verification, live acceptance, a security audit or approval of #563 activation.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Reported questions; C1, C3; P01-T01 | Covered | Existing STATUS answer can serve both questions without changing answer authority. |
| Status/waiting/blocking/update/retrofit, missing/receipt paperwork, forms, home/address; P01-T01 | Partial | Topic/intent families are named, but vocabulary and anchors alone do not establish complete-message recognition; PC-001 requires concrete positive/negative contracts. |
| Legacy complete-message refusal; C4; P01-T01, P02-T01 | Partial | Existing matrix and natural-phrase suffix extension are retained, but allowed-vocabulary malformed suffixes are not explicitly covered; PC-001. |
| Safety, consent, appointments, regulations, repair, unknown; C2, C5; P01-T01, P02-T01 | Covered | Fallback is after existing host checks; specialist and protected tests remain authoritative. Safety must still win when combined with excluded text. |
| Four refusal examples; C6; P01-T02 | Covered | Functional requirements, acceptance and details require four despite the broader introductory "three or four" wording. Implement exactly four, per caller. |
| Own-case grounding, permission, no actions/callbacks; C3, C5; P02-T01 | Covered | Constructed C-1/C-2 comparison, existing HTTP access checks and no-action assertions are scoped. Positive rules tests mean no optional advisor work, not suppression of the required fixed-answer function. |
| No activation/deployment, #563 gate; P01-P03 | Covered | No configuration, frontend, core-answer, infrastructure or data changes. Existing fake AI regression execution is not activation. |
| Focused validation/test lock; C7; P02-T01, P02-T02 | Covered | Four named existing API modules plus Ruff/mypy; zero removals, at most three new methods. Dated src/README.md explicitly permits focused-tier evidence. |
| Review and exact-candidate publication; P03-T01, P03-T02 | Partial | Clean committed checks and hosted/owner boundaries are specified, but unresolved material Review findings do not explicitly stop publication; PC-002. |

## Verdict

* Verdict: Revise
* Severity summary: 2 High, 0 Critical, 0 Medium, 0 Low.
* Rationale: the bounded routing direction is credible, but its recognition contract needs structural rejection evidence beyond token membership, and its publication contract must honor the independent Review outcome. Both are direct planner corrections within current owner direction. No significant or divergent user decision is needed.
* Preservation: this original execution status, verdict and finding set remain unchanged after parent disposition. Resolution does not retroactively make this critique Pass.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Vocabulary membership and anchors do not prove complete-message recognition

* Related IDs: C1, C4; complete-message and mixed-intent functional requirements; P01-T01, P02-T01.
* Evidence: P01-T01 specifies allowed characters, per-topic vocabulary and own-record/question-intent anchors. src/api/src/zava_forward/api/resident_demo/chat.py:36-37 returns a token set, losing order and multiplicity; its current _record_question instead uses full-message grammar. src/api/tests/test_resident_chat_api.py:496-526 rejects suffixes and a repeated question after "?". The planned extension inherits those cases, but most existing unpunctuated adversaries introduce forbidden or unknown words.
* Concern: a whole-character envelope plus an allowed token set can still accept malformed text or additional same-topic questions composed entirely of allowed words. For example, "How is my case going what is my case status" and "How is my case going my case" contain the intended anchors and plausible status vocabulary, with no markup, unknown word or embedded punctuation. Per-topic separation does not resolve this. This is a gap in the planned proof, not a claim that an unimplemented classifier already accepts those examples.
* Impact: the fix could pass the inherited suffix matrix while weakening the legacy complete-recognized-message boundary. With AI off it would answer unsupported messages; under separately configured existing AI it could admit those messages to answer_question.
* Smallest useful change: retain bounded keyword/intent routing but explicitly require a structurally complete single supported request, preserving token sequence where needed and rejecting appended clauses, duplicate anchors/questions and unconsumed text. Specify concrete positive rows for every requested intent family, including receipt and both reported literals, plus all-allowed-vocabulary malformed/repeated-question negatives. Do not attempt universal grammar or broaden the task.
* Action owner: planning parent / API maintainer.
* Exact resolving evidence: P01-T01 names the structural full-message constraint and P02-T01 locks a concrete shared positive/negative matrix, including the two examples above and equivalent document/form/home compositions using the actual admitted vocabulary. Implementation evidence later shows the reported and family-positive rows map to existing answers, while those negatives and the entire inherited suffix/prefix matrix refuse through assert_host_routes with no provider selection, advisor call, accounting, token or transport work. Keep all original tests and the three-method addition cap.
* Decision route: direct planner correction; current owner direction already requires complete-message refusal. No significant or divergent user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Publication is not explicitly gated on material independent Review findings

* Related IDs: P03-T01, P03-T02; P03 dependency and original-evidence requirements.
* Evidence: P03-T01 says "Findings route to later work, not another Review in this task." P03-T02 then commits, checks, pushes and opens a PR without an outcome condition. The plan requires Review execution, but does not say that unresolved material findings block final-candidate publication.
* Concern: executing one Review is not equivalent to resolving its publication-blocking findings. The present wording permits a known routing, authority or validation defect to be deferred while the candidate is published. The one-Review direction does not authorize ignoring that Review's outcome.
* Impact: a final-candidate PR could be presented as ready despite independently identified unmet acceptance criteria. Hosted checks and eventual owner merge authority do not resolve a known failed local acceptance boundary.
* Smallest useful change: make P03-T02 conditional on an acceptable Review outcome and all publication-blocking findings being resolved with exact-candidate evidence. Preserve the original Review outcome. Compatible corrections may be documented and rerun through focused checks without invoking another Review; if independent reassessment is required to establish resolution, stop publication and report the blocker rather than silently expanding the task. Only genuinely nonblocking follow-up items may be deferred with an explicit disposition.
* Action owner: planning parent.
* Exact resolving evidence: P03-T01/P03-T02 define the stop condition and distinguish nonblocking follow-up from unmet acceptance criteria. The eventual Review and changes artifacts retain the original result, list each finding/disposition and resolving check evidence, and bind the final clean commit to focused checks before any push. An unresolved material finding records publication blocked; no second Review or gate bypass is inferred.
* Decision route: direct planner correction; no significant or divergent user decision. If the one-Review constraint leaves a material finding unverifiable, return that concrete blocker to the parent.

## Strengths and Residual Risk

* The plan rejects substring-only matching, retains legacy exact grammar, and places the fallback behind existing safety, exclusions and specialist routes.
* Existing HTTP fixtures and provider/advisor/accounting spies provide strong bounded evidence without private records, real inference or deployment.
* The explicitly accepted finite-vocabulary limit means unsupported natural wording may still refuse. It does not establish universal language understanding.
* Rules answers remain grounded summaries, not diagnoses, consent, appointment bookings, blockage determinations beyond the available record, or approval of legal duties.
* No AI activation configuration changes are planned. Mock optional-AI tests preserve existing behavior and do not lift #563's owner gate.
* Named resident-copy review and live acceptance remain unperformed and separate. Local checks cannot establish those outcomes or hosted approval.
* The plan records installed Ruff/mypy versions differing from manifest pins; report actual versions without claiming pinned-environment reproduction.

## Questions or Blocking Evidence Gaps

* No decision-critical evidence gap blocks this plan assessment.
* No user response is needed for either finding. The parent can resolve both within the existing task and validation lock.

## Limitations

* No implementation exists in the supplied candidate; neither reported-question recovery nor adversarial preservation was executed in this critique.
* The research's 69-test baseline is reported evidence, not a rerun by this worker.
* Only supplied materials and directly relevant current source/test guidance were assessed. No external research, remote lifecycle operation, dependency change, build, publication or live service check was performed.
* Existing untracked parent planning/research/state inputs were left untouched. The critique is the only written file.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent / API maintainer.
* Smallest next action: add the structural full-message recognition and explicit allowed-vocabulary adversarial matrix to P01-T01/P02-T01; then add PC-002's publication stop condition.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/resident-chat-routing-research.md](.copilot-tracking/research/2026-10-31/resident-chat-routing-research.md) | Supplied C1-C7 evidence and scope decisions |
| [.copilot-tracking/plans/2026-10-31/resident-chat-routing-plan.md](.copilot-tracking/plans/2026-10-31/resident-chat-routing-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-31/resident-chat-routing-phase-details.md](.copilot-tracking/details/2026-10-31/resident-chat-routing-phase-details.md) | Assessed completion contracts |
| [.copilot-tracking/plans/2026-10-31/resident-chat-routing-critique.md](.copilot-tracking/plans/2026-10-31/resident-chat-routing-critique.md) | Original Complete / Revise critique |

## Next Steps

The active planning parent applies compatible PC-001 and PC-002 corrections once,
records their evidence and disposition, and preserves this original Revise verdict.
No further critique, implementation by this worker, AI activation, deployment or
user action is authorized or required by this assessment.
