<!-- markdownlint-disable-file -->

# Task Research: regulatory-assistant-208

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/regulatory-assistant-208-research.md |

## Research Brief

* What to research: remaining acceptance criteria for #208, #214, #216, #215 and #217 against current src implementations.
* Why: deliver independently safe synthetic engineering without implying legal approval or operational acceptance.
* Audience: exercise owner and independent PR reviewers.
* Scope: existing regulatory retrieval, chat, gates, privacy, audit and role-shaped UI.
* Non-goals: real data, private datasets, secrets, Azure changes, paid inference, legal interpretation, rule activation or fabricated human evidence.
* Criteria: actual issue criteria, BRD FR-051/AC-099/OD-50, PRD FR-060/AC-104-106/OQ-026, ADR 0005 and ADR 0006.
* Requested outputs: dated research, plan/details, changes and independent Review; evidence-backed acceptance disposition.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which gaps can be implemented independently, and which require actual human decisions? |
| Codebase scope | src/core, src/agents, src/api, directly related documentation |
| External scope | Named GitHub issues; current web guidelines if web files change |
| Initial internal candidate areas | Regulatory chat, privacy, evaluation harness, API and workbench |
| Initial external candidate areas | jmservera/ama issues 208, 214, 216, 215, 217, 440 |
| Research posture | focused |
| Posture provenance | Default for bounded named issue task |
| Explicit limits | Local tests only; at most one scoped changed gate with nonblocking heavy lock; no full gate authorized by caller |
| Completion basis | Material in-scope criteria mapped to code/evidence or explicit missing human authority |
| Edits allowed during research | No source edits |
| Resolved evidence root | .copilot-tracking/ |
| Excluded sources | Private datasets, .env, secrets, live processing |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority | Disposition |
| --- | --- | --- | --- | --- |
| Instruction | Repository instructions | All files | ADR 0006, approval, branch and publication boundaries | Selected |
| Skill | rpi-research | Required RPI loop | Three research waves and evidence | Selected |
| Skill | web-design-guidelines, accessibility | UI work if needed | Review changed UI against fetched rules | Deferred until web scope established |
| Specialist | Independent critique and Review | Required RPI phases | Read-only bounded assessment | Selected for later phases |
| Research specialist | RPI Researcher | Registered | Independent uncertainty only | Skipped: continuous existing implementation trace |

## User Participation and Research Decisions

| Checkpoint | Rationale | Direction | Decision |
| --- | --- | --- | --- |
| Intake | Explicit full ordered loop and noninteractive host | User authorizes all four phases and PR publication | Execute bounded loop without routine prompts |
| Authority | User forbids guessing owner/Legal/DPO/Compliance decisions | Real approval unavailable | Implement independent work; retain live and acceptance blockers |

## Scope and Success Criteria

Every criterion must be evidenced or explicitly unproven. Existing checked issue
boxes are historical claims, not fresh proof. Synthetic fixture evidence does
not establish real appointments, DPO retention approval, staff comprehension,
approved evaluation thresholds or live readiness.

## Task Research Requests

Deliver one branch/PR for the four listed children; retain workflow names,
namespace packages and tests outside packages.

## Direction Controls

| Type | Boundary | Source | Effect |
| --- | --- | --- | --- |
| Exclude | Azure, paid inference, private data | User | Local synthetic evidence only |
| Narrow | #214, #216, #215, #217 | User | Other epic children are dependency evidence, not new delivery |
| Exclude | Full --all gate | User | Publication conflict with repository mandatory full gate must remain explicit; do not claim scoped evidence satisfies it |

## Research Questions

| # | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | What is already implemented and where are remaining behavioral gaps? | depth | High | Open |
| Q2 | Which acceptance items need human evidence? | straightforward | High | Open |
| Q3 | What local tests prove the independent changes? | depth | High | Open |

## Prior Knowledge Gate

Read all five named issues with gh issue view, #440, reference index, memory,
original case study, addendum and linked BRD/PRD rows. Branch
feat/regulatory-assistant-208 is clean, has no prior PR, and starts at
0ded682bab690d24eb59b78e704be82d337bf6cd. ADR 0005 records synthetic development
acceptance on 2026-10-16; issue boilerplate saying "proposed only" is stale.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Located existing chat, privacy, evaluation, API and browser checks under src.
Reflection: this is completion/hardening, not a greenfield assistant. Prioritize
unchecked criteria and contradictory stale issue descriptions.

#### Wave 2: Deeper

Traced retrieval, storage, output grading, role guards, browser checks and
retention. Conflict outputs show both versions but only offer a manual doubt
action; test_regulatory_chat explicitly expects zero owner threads after a
conflict. Existing audit records contain no consumption outcome counters.
The comparator leaves service cost null without naming missing price/billing
inputs. Existing role-shaped alert/chat UI and actual browser harness can be
extended without a redesign. Installed project imports initially failed;
installed core/agents/API and their existing dev extras with pip into an
external session venv.

Reflection: automatically route supported conflicts atomically with their
stored evidence, add content-free offline consumption records, and name
unknown cost inputs without granting any spend authority.

#### Wave 3: Contrarian

Challenged the apparent completion implied by checked boxes and the generated
60,000-home report. The evaluation is implementer-authored and stateless, not
the continuing pipeline, held-out legal grading, a staff trial or model proof.
The ship recommendation correctly remains cards_only. Synthetic retention
references are deliberately not DPO-approved disposal schedules. Trusted
RegulatoryChat capability checks exist, but real Entra assignments have not
been verified. No owner thresholds, DPO periods or comprehension outcomes may
be supplied by this implementation.

Reflection: preserve the existing no-provider path and explicit admission,
keep live use blocked, report all remaining human criteria as unmet, and
exercise rollback/restart and revoked-role cases for the new metadata/routes.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Conflict only prompts for manual referral | C5, C6 | Accepted for implementation | #214 requires conflicting sources shown and escalated |
| Add a model to complete the ADR flow | C1, C7 | Rejected | No provider/spend authorization or measured chat ship value |
| Metadata-only offline usage and explicit Unknown cost | C7-C10 | Accepted for implementation | Independent tokenomics delta without inventing prices or budgets |
| Declare WCAG/DPIA/owner gates satisfied | C1, C8-C10 | Rejected | Engineering/simulated evidence is not actual acceptance |

#### Cycle Re-entry Evaluation

No further cycle required: existing interfaces and tests cover the independent
slice. Further discovery cannot supply the missing human decisions.

## Evidence Log

| ID | Finding | Location | Tool | Confidence |
| --- | --- | --- | --- | --- |
| C1 | Synthetic development accepted; operational approval absent | docs/adrs/0005-regulatory-compliance-assistant.md:12 | read | High |
| C2 | Source projects, namespace boundaries and mandatory full publication gate | src/README.md:34 | read | High |
| C3 | Proposal-only regulatory intent | docs/brds/agentic-retrofit-programme-brd.md, FR-051/AC-099/OD-50 | search/read | High |
| C4 | Required grounding, conflict handling and paired comparison | docs/prds/zava-forward-retrofit-programme-demonstrator.md, FR-060/AC-104-106 | search/read | High |
| C5 | Conflicts returned without automatic referral; ask/doubt separately commit | src/core/src/zava_forward/core/regulatory_chat.py:175,293,383 | read | High |
| C6 | Conflict test expects no owner inbox | src/core/tests/test_regulatory_chat.py:197 | read | High |
| C7 | Comparator is unexecuted and recommends cards_only | src/agents/src/zava_forward/agents/regulatory_gates.py:248 | read | High |
| C8 | DPO report is review-only; all non-chat periods unknown | src/core/src/zava_forward/core/regulatory_privacy.py:18 | read | High |
| C9 | Existing accessible native alert/chat patterns and warning | src/api/src/zava_forward/api/web/chat.js:119,171 | read | High |
| C10 | Seeded baseline is not continuing-stock or staff evidence | src/agents/tests/regulatory_gate_fixture.py:390 | read | High |

External interface guidelines retrieved 2026-10-27:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Repository Fluent 2, plain ASCII content and WCAG evidence boundaries take
precedence over generic typography recommendations. Accessibility skill
selected for WCAG interpretation; its uv scanner is excluded by caller policy,
so use the existing pinned Playwright/axe harness.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Readiness |
| --- | --- | --- | --- |
| Q1 | Complete atomic conflict routing and offline economics; preserve architecture | C5-C10 | Ready |
| Q2 | Thresholds, staff trial, DPIA, retention and real role assignments remain unproven | C1, C7-C10 | Explicit residuals |
| Q3 | Existing JSON/SQLite, API, pure graders and actual local browser harness apply | C5-C10 | Ready |

## Alternatives and Decision State

Develop only independent synthetic gaps using the existing architecture; do not
replace existing abstractions or claim simulated approvals satisfy actual gates.

## Open Questions, Risks and Residual Uncertainty

Actual owner-approved thresholds, staff comprehension, DPO review, retention
periods and real Entra separation cannot be inferred. #440 remains an epic
closure prerequisite. Caller authorization excludes the repository-required full
publication gate; publication must not be presented as gate-compliant.

## Planning Readiness

Ready for independent synthetic implementation only. Live activation,
whole-issue closure and publication remain blocked; no acceptance boxes ticked.

## Research Disposition

Executed, complete. Required wider, deeper and contrarian waves completed in
order inline. No independent research lane was needed. Evidence and limits
self-check complete; handoff to the parent-owned Plan phase.
