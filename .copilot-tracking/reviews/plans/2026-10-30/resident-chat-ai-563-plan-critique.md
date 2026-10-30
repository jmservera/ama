---
title: "RPI Plan Critique: resident-chat-ai-563"
description: One final-candidate credibility assessment for the local resident generated-answer source fix
ms.date: 2026-10-30
---

## Metadata

* Task ID: issue-563
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/resident-chat-ai-563-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/resident-chat-ai-563-phase-details.md
* Critique execution status: Complete
* Assessment count: exactly one final-candidate critique
* Candidate state: feat/resident-chat-ai-563; supplied research, plan, details and session state were already untracked. They were not changed.

## Inputs and Criterion Boundary

* Caller requirements: a complete local RPI source repair for consented resident repair/free-text answers, including the dead-rat example; grounded generated prose; a thin Teams-like AI label and collapsed sources; consent first; honest inability, housing-officer help and explicit unavailable fallback.
* Scope controls: no secrets, .env, private data, Azure operations, paid inference, push or issue closure. Later local persistence must use Refs #563. This critique writes only its specified output and does not advance another lifecycle stage.
* Supplied evidence: .copilot-tracking/research/2026-10-30/resident-chat-ai-563-research.md, particularly C2-C9 and its stated W1-W2 findings. Issue/PR observations and external-source retrievals are assessed as reported research, not independently re-observed facts.
* Direct source checks: src/api/src/zava_forward/api/resident_demo/chat.py, app.py, aoai.py and web/assistant.js; src/core/src/zava_forward/core/resident_assistant.py; src/api/src/zava_forward/api/web/chat-widget.js; src/api/tests/test_resident_chat_api.py and test_resident_aoai.py; infra/resident-demo.bicep.
* Repository context: original case study, addendum, reference index, memory, housing-association primer and src/README.md local-gate guidance. Memory was used only as context.
* Decisions: extend the existing advisor rather than introduce another client; retain fixed-topic API behavior and deterministic protected routes; keep activation off by default; reuse consent, own-case projection, transport and durable accounting; preserve original adverse evidence.
* Dependencies: P01-T01 follows research and this critique; P02-T01 follows implementation; P03-T01 follows focused validation. Installed task-owned tooling and local Chromium support local checks. Deployment configuration, renewed tariff authority and live acceptance are separate owner gates.
* Assessment boundary: credibility and completeness of this candidate for bounded local implementation, not implementation correctness, actual-model relevance, legal approval, accessibility conformance, operational readiness or whole-issue acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Source diagnosis; C2-C4 | Covered | chat.route returns unknown for the reported repair example; app dispatch invokes the advisor only for Topic values; AzureAdvisor currently selects guidance IDs. The candidate changes both routing and provider capability. |
| Activation boundary; C5-C6 | Covered | configured_advisor defaults off and the supplied Bicep settings omit assistant activation. The candidate does not confuse this source observation with inspected live configuration or authorize deployment changes. |
| Repair and other in-scope free text; P01-T01 | Covered | Details introduce a generated-question method and repair routing after protected handling; unrelated questions stay refused. The separate fixed-topic API retains its bounded behavior. |
| Safety, legal, consent, appointments and action/injection handling | Covered | Plan requires deterministic protected routes ahead of repair handling; existing hazard and refusal regressions provide concrete preservation checks. |
| Grounding and source validation; C4, C9; P01-T01 | Covered | Host-owned answer/progress and repair-reporting guidance form a minimal source map. Strict bounded prose/source-ID output excludes model-supplied URLs; reporting is distinguished from diagnosis or recorded fact. |
| Consent, isolation and late results; C7; P01-T01/P02-T01 | Covered | Exact boolean consent before reads/model work, session binding, post-inference authority checks, browser withdrawal invalidation and cross-case prompt exclusion are explicit. |
| Accounting and bounded transport; C5, C7 | Covered | Both model paths reuse precommitted reservations, caps, usage checks, expiry, prompt/reply/token bounds, timeout and no retries. No SQL or tariff extension is proposed. |
| Inability, human help and unavailable states | Covered | Disabled, unavailable, budget, expiry and malformed output require explicit rules fallback with human help. Host-owned inability/advisory limits must remain visible. |
| Thin label, sources and truthful consent copy; C8, W1-W2 | Covered | Existing shared widget uses escaped text, small metadata and native closed details. Resident UI copy must disclose question transmission and remove the current contradictory assurance. |
| Unit ownership, removals and change budget | Covered | Two named API suites, at most 18 new unit methods, at most one browser check and no removals are explicit. Existing fixed-topic, consent, isolation, expiry and budget checks remain regression obligations. |
| Local browser and focused engineering checks; P02-T01 | Covered | Constructed residents and scripted Azure transport exercise the real local HTTP path, consent ordering, grounding, escaping, source keyboard operation, typography, narrow reflow and unavailable state. Ruff, mypy and affected core checks are included. |
| Independent Review and persistence; P03-T01 | Covered | One independent Review preserves original findings; local identity, Copilot trailer, Refs #563 and a post-commit full-gate attempt are specified. Failed/missing checks cannot become publication evidence. |
| Scripted versus actual-model/live acceptance | Covered | Research, plan, details and acceptance criteria consistently limit local proof. No source fix, scripted reply or browser screenshot is represented as actual-model relevance or live issue completion. |

## Verdict

* Verdict: Pass
* Rationale: the candidate addresses the two independently evidenced source limitations, identifies the necessary generated-answer boundary and preserves the existing consent, authority and cost controls. Its implementation and validation obligations are sufficiently concrete within the locked change budget. Known model-quality, activation and live-acceptance limits are explicitly retained rather than hidden.
* Severity summary: Critical 0; High 0; Medium 0; Low 0.

## Findings

No actionable PC-xxx findings were identified within the supplied candidate boundary. This is the complete original finding set, not a deferred subset. No planner correction or significant/divergent user decision is required by this critique.

## Strengths and Residual Risk

* A configuration-only fix is correctly rejected: enabling inference would still leave repair questions outside the provider path and leave existing provider replies limited to prewritten sentences.
* The candidate preserves fixed-topic compatibility without requiring typed questions to remain template selections. Existing typed-question/template equality assertions will need to reflect that intentional distinction; preserving the explicit topic API, not obsolete free-text expectations, is the stated contract.
* Nonempty permitted source IDs and escaped prose prove structural constraints, not that every generated claim is supported. The candidate explicitly retains actual-model evaluation and human approval as separate gates; this Pass does not accept hallucinations or certify safe model behavior.
* Scripted output can prove HTTP routing and rendering of non-canned transport text. It cannot establish the model's ability to answer the dead-rat question appropriately.
* Default-off configuration and the dated tariff mean local delivery may leave a running deployment rules-only. The plan explicitly discloses that limitation and does not authorize activation.
* Independent Review may still find implementation defects. Its original verdict must be preserved; this planning Pass cannot preapprove source, review outcomes or a failed full local gate.

## Questions or Blocking Evidence Gaps

* None for the bounded local implementation decision.
* Actual model relevance, authenticated deployment behavior, renewed inference authority where needed, human content acceptance and assistive-technology acceptance remain unproven follow-up gates, not omitted local evidence.

## Limitations

* No tests, browser checks, model calls, cloud operations or fresh external retrievals were performed during critique. Existing UI source was inspected for feasibility, not subjected to a standalone UI or accessibility audit.
* Supplied research records the #563/#562 symptom and W1-W2 retrievals. This assessment does not independently verify those remote observations.
* No source, plan, details, research, session state or prior review record was edited. No delegation, commit, push or lifecycle progression was performed.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: planning parent.
* Smallest next action: record this original Complete / Pass disposition without another critique, and use the existing P01-T01 boundaries when the parent resumes its authorized lifecycle.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/resident-chat-ai-563-research.md](.copilot-tracking/research/2026-10-30/resident-chat-ai-563-research.md) | Supplied diagnosis and evidence boundary |
| [.copilot-tracking/plans/2026-10-30/resident-chat-ai-563-plan.md](.copilot-tracking/plans/2026-10-30/resident-chat-ai-563-plan.md) | Assessed final candidate |
| [.copilot-tracking/details/2026-10-30/resident-chat-ai-563-phase-details.md](.copilot-tracking/details/2026-10-30/resident-chat-ai-563-phase-details.md) | Assessed implementation and validation details |
| [.copilot-tracking/reviews/plans/2026-10-30/resident-chat-ai-563-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/resident-chat-ai-563-plan-critique.md) | Complete original critique and verdict |

## Next Steps

Return Complete / Pass to the planning parent. No user action is required. This critique stops here; recording disposition and any subsequent lifecycle progression belong to the parent, not this invocation.
