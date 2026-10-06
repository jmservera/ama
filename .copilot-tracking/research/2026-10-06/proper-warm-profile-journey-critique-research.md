<!-- markdownlint-disable-file -->
# Task Research: proper-warm-profile-journey-critique

| Field | Value |
|---|---|
| Date | 2026-10-06 |
| Researcher / agent | rpi-research |
| Status | Complete: nine fresh company reviews, eleven-profile UX synthesis and four relayed discussions |
| Artifact path | .copilot-tracking/research/2026-10-06/proper-warm-profile-journey-critique-research.md |

## Correction and Current Review Cycle

The earlier statement that company-agent dispatch was unavailable is superseded.
On 2026-10-06, all nine repository `company-*` profiles were launched in
parallel using the agent task tool, including the Executive Reviewer omitted
from the earlier eight-perspective review. Fresh responses and the subsequent
UX/UI Designer discussion will be recorded below.

The earlier analysis also incorrectly states that workflow-card selection
only reveals explanatory text. The click handler at prototype lines
1008-1020 calls both `renderWorkflows()` and `renderCases()`, and
`filteredCases()` at lines 908-920 applies the selected workflow to the queue.
Workflow cards therefore filter cases as well as displaying descriptions.
They still do not advance a case through lifecycle stages.

The previous inline analysis below is retained as historical context, not
as the outcome of the fresh representative review. Agent perspectives remain
research instruments, not real employee interviews or validated company facts.
No prototype changes are authorized by this critique request.

## Research Brief

* What to research: Critique the prototype journey for all 11 Proper Warm PRD profiles, using applicable company-role perspectives and the updated constructed case history.
* Why it matters: Profile-by-profile critique can identify mismatches between a role's stated job, available journey, evidence and decision boundaries before later design work.
* Audience or intended use: Project owner, UX reviewer and company-role agents; inform a grounded critique and identify which issues require fresh representative input.
* Scope: The prototype, current draft PRD, original case and addendum, company profile research, prior profile UX matrix/company-role responses, and matching `.github/agents/company-*` role boundaries.
* Non-goals: Claiming new agent/user interviews when tools or responses are unavailable; production authorization; changing code/PRD; validating real company processes; legal/regulatory determinations.
* Criteria: All 11 named profiles receive an explicit journey critique; differentiate direct prototype evidence, prior role-agent perspective, and present analyst hypothesis; do not misstate company facts; record gaps and accessible/authority boundaries.
* Requested outputs: One durable profile journey critique, an honest account of whether a fresh agent discussion was possible, findings, and evidence-backed next steps.
* Output mode: research-only

## Research Parameters

| Field | Value |
|---|---|
| Research question(s) | What does each of the 11 profile journeys let a user do/understand, where does the prototype fail or mislead, and what company-role feedback is evidenced? |
| Codebase scope | Prototype, PRD, case-study context, company-role agent files and existing review artifacts |
| External scope | None |
| Initial internal candidate areas | `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html`; `.copilot-tracking/changes/2026-10-06/prd-prototype-changes.md`; `.copilot-tracking/reviews/logs/2026-10-06/prd-prototype-review.md`; `docs/prds/proper-warm-retrofit-programme-demonstrator.md`; `docs/reference/research/company/company-profile-research.md`; `.github/agents/company-*` |
| Initial external candidate areas | None |
| Research posture | focused |
| Posture provenance | Default; bounded, named internal source set and requested 11-profile scope |
| Explicit limits / deadline | No fresh company-agent dispatch endpoint is exposed in this conversation's tools; do not represent prior perspectives as a new discussion. No source edits. |
| Posture-specific completion basis | Cover all 11 prototype journeys, inspect prior role feedback and decision boundaries, and identify the smallest unresolved gap. |
| Edits allowed during research? | No; research-only |
| Resolved evidence root | `.copilot-tracking/` |
| Known constraints / excluded sources | No external sources, no inferred actual company processes, no direct user research claims. |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
|---|---|---|---|---|
| Instruction | `.github/copilot-instructions.md` | `applyTo: "**"`; read for repository and company-agent conventions | Require case-study grounding; distinguish case facts, hypotheses and unknowns; no simulated privileged employee | Selected |
| Skill | `rpi-research` | Explicit evidence gathering/critique context | Three-wave research and durable findings | Selected |
| Skill | `web-artifacts-builder` | Prototype is the reviewed artifact | Clawpilot theme and single-file artifact constraints | Reused existing task context; no edits |
| Skill | `frontend-design` | Web UI critique matches skill semantics | Interface critique | Not activated because user asked company-role perspective critique and provided an existing UX critique; no design change requested |
| Skill | `agentfinder` | Loaded in this session while checking if agent dispatch could be found | Registry search only; no authority to install/use agents | Skipped; it targets third-party discovery and does not expose local company agents |
| Research specialist | `RPI Researcher` | Would suit delegated independent research | Bounded evidence lane | Not dispatched: no agent/task dispatch tool is exposed in this session; inline assessment used |
| Specialist | `.github/agents/company-*` | Repo-defined role instruments grounded in company-profile research | Role-specific perspective, not company facts or actual-user validation | Prior feedback reused and prompts read; fresh dispatch unavailable, so no new responses attributed |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision or selected further research |
|---|---|---|---|
| Intake | The task explicitly names the prototype and all 11 profiles. No clarification needed. | None | Proceed with a focused critique. |
| Direction change | Fresh agent discussion is desired, but no agent dispatch tool is available in the current session. | Unavailable | Use prior recorded role feedback plus repo role constraints; visibly mark the fresh discussion as not performed. |
| Convergence | Research-only output; user asked for critique, not a selected product direction. | No further question needed | Keep implementation actions as options/hypotheses, not decisions. |

## Scope and Success Criteria

* Scope: All 11 profile flows in the current prototype, with past feedback assessed against the later timeline addition.
* Assumptions: The existing recorded UX matrix and eight role-agent perspectives are available as evidence from the earlier task; they are not fresh feedback on the timeline.
* Success criteria:
  * Every PRD profile is explicitly reviewed.
  * Each critique item is identified as prototype observation, prior role perspective, or analyst hypothesis.
  * Existing findings are checked against the case timeline and role limits.
  * Fresh company-agent discussion is honestly marked unavailable rather than simulated.
  * No code or PRD is changed.

## Task Research Requests

* Explicit requests: Discuss with `company-*` representatives the 11 profile journeys using the prototype and critique it.
* Inferred research questions: Which journey does each profile get; what is useful/missing/misleading; where do handoffs, history, data, resident choice or human authority need clarification?
* Caller constraints and non-goals: Use prototype; critique all 11; preserve proper role boundaries and do not invent company facts.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect on active brief, evidence, or revalidation |
|---|---|---|---|
| add | Include the updated timeline and all 11 journeys | Current user request | Compare timeline coverage with role needs and prior feedback |
| narrow | Use company role agents as bounded instruments, not validated employees | Repository conventions and company research | Do not claim real user research or company policy |
| exclude | Do not implement fixes or alter production requirements | User request is critique-only; research contract | Findings only; no code edits |

## Research Questions

| # | Sub-question | Type | Priority | Status |
|---:|---|---|---|---|
| Q1 | What are the 11 journeys and what can the prototype actually demonstrate for each? | breadth | H | Answered with bounded prototype critique |
| Q2 | Which previous company-role findings still apply, and does the updated timeline address them? | depth | H | Answered; timeline improves visibility but not PRD-grade event history |
| Q3 | Can company-role agents be re-engaged here, and what can be concluded without fresh responses? | straightforward | H | Fresh dispatch unavailable; prior feedback and written role boundaries used |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/reference/README.md`; `docs/reference/memory.md`; `docs/case_study_48_original.md`; `docs/case_study_48_addendum.md`; `docs/reference/research/sector/housing-association-primer.md`; `docs/prds/proper-warm-retrofit-programme-demonstrator.md`; previous changes, review and checkpoint; tool list for current session.
* Reused (verified) findings: PRD v0.6.2 names 11 provisional profiles and nine workflows; prototype has eight constructed cases; prior UX Designer review covered all 11 profiles; eight company-role perspectives previously responded. Review RV-001 led to an illustrative three-entry history on each constructed case.
* Superseded / stale: The previous role critique predates the case-history addition and cannot be treated as feedback on that new interaction.

## Research Cycle Log

### Cycle 1

* Active direction controls: Use the prototype and all 11 profiles; distinguish prior role feedback from new direct discussions.
* Active research posture and completion basis: Focused; the named PRD/prototype and prior role-feedback record bound the inquiry.
* Explicit limits or deadline effect: No fresh agent dispatch available; mark this as an evidence gap and do not impersonate agents.

#### Wave 1: Wider

* Plan and independent lanes: Enumerate all 11 profiles, prototype tasks/workflow areas, applicable company-role perspectives and earlier feedback themes.
* Worker evidence relationships or inline fallback: Inline; no agent dispatch tool available. Used prior changes record, company-agent definitions and PRD.
* Reflection: Each of the 11 PRD roles maps to a prototype profile, but the implemented journeys are role-filtered queues over eight constructed cases, not 11 validated end-to-end user journeys (C1-C3). Prior UX feedback covers all profiles; role-agent input covers eight role lenses (C4-C5). Provider/Contractor Contact, Quality and Assurance, and Digital Operator/Auditor have no dedicated matching company-role agent.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Role-to-workflow fit, selected-case timeline details, distinction between static example and real history, and authority boundaries.
* Plan and independent lanes: Inspected profile definitions, cases, filtering, detail rendering and prior role findings against PRD role table, handoff requirements and agent charters.
* Worker evidence relationships or inline fallback: Inline assessment; no fresh agent responses attributed.
* Reflection: Each case has three illustrative history entries, but the UI labels them as constructed and the PRD calls for timestamped progression and event details including source, actor and version (C2-C3). The new UI is useful for discussing a scenario but does not satisfy the PRD's full event-history requirement. Existing feedback on other interactions remains prior feedback only (C4-C5).

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge whether role-specific queues meaningfully support a full journey; whether a static three-step timeline satisfies audit/history needs; whether a staff-facing Provider profile is intelligible; whether more detail risks invented authority/data.
* Plan and independent lanes: Compare against PRD case-history acceptance and role boundaries; consider a transparent sample-only journey instead of simulating a live workflow.
* Worker evidence relationships or inline fallback: Inline; no external research or fresh agent dispatch.
* Reflection: Keep the prototype explicitly scenario-based rather than add fabricated operational data. This avoids implying real permissions, audit history, resident contact, supplier commitment or statutory decisions. The trade-off is that several roles cannot test their end-to-end tasks until representative evidence and safe synthetic event data are supplied (C2-C3, C6-C8). No fresh agent response is not evidence of endorsement or rejection.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition | Evidence-based rationale | Primary-artifact treatment |
|---|---|---|---|---|
| Role-specific queues are useful for orientation but do not by themselves constitute journeys | C1-C3 | Accepted as a prototype critique | Each constructed case is associated with one workflow; no connected progression across roles is shown | Finding F1; validate task sequence with users |
| Added case history addresses visual history visibility, not PRD event-history behavior | C2-C3 | Accepted | Constructed entries are not timestamped events with actor, event order, version and preserved corrections as AC-025 specifies | Finding F2; keep illustrative labels; do not present as audit evidence |
| Profile-specific decisions and handoffs need stronger boundaries for several roles | C1, C3, C6-C8 | Accepted as a risk/hypothesis | Role responsibilities and approval boundaries vary; no prototype control should imply authorization, acceptance or resident consent | Finding F3; ask role-specific questions in fresh representative review |
| New direct company-role feedback was obtained for this timeline update | Session tool inventory; C4-C5 | Rejected | Only previously recorded feedback is available; this session exposes no agent-dispatch endpoint | Consultation gap; no new responses attributed |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: No, within the available source set.
* Trigger or stop basis: All 11 prototype profiles, prior role feedback, eight role-agent charters and relevant PRD acceptance criteria were inspected. Without live agent dispatch or user research, further inline work would repeat the same evidence rather than close the participation gap.
* Revised brief or revalidation required: None currently.
* Readiness effect: The critique is a bounded design input, not validated user research or a replacement for the requested fresh company-role discussion.

## Evidence Log

* Delegation: Inline fallback because no agent/task dispatch tool is exposed; prior agents' feedback is recorded in the existing changes record, not newly obtained.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|---|---|---|---|---|---|
| C1 | The prototype defines 11 profiles and a separate set of workflow cards. | `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html:817-842,887-939` | view | High | Direct implementation observation; not evidence users identify with these profile names. |
| C2 | Eight constructed cases are available; case detail renders a constructed-history disclosure. | `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html:843-856,957-979` | view | High | Scenario content, not operational events. |
| C3 | PRD requires role-owned handoffs and historical progression; AC-025 specifies event order, source, actor and version. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:298-310,538-551` | view | High | Requirements, not implemented or validated behavior. |
| C4 | Prior UX review records profile-by-profile review and eight role-perspective dispositions. | `.copilot-tracking/changes/2026-10-06/prd-prototype-changes.md:34-80` | view | High | Predates the latest case-history disclosure. |
| C5 | The profile table names user jobs and required information, including asset baselines, housing support, supplier capacity, assurance and integration recovery. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:187-205` | view | High | Provisional design personas, not confirmed company titles, duties or permissions. |
| C6 | Company role/decision map reserves decisions across assets, safety, finance, procurement, resident choice and professional approval; provider variation is explicit. | `docs/reference/research/company/company-profile-research.md:284-297` | view | High | Sector-informed boundaries, not company-specific approvals. |
| C7 | Asset executive has delegated approval limits; data/performance does not own investment; building safety owns safety systems; finance does not choose technical measures. | `.github/agents/company-executive-director-assets.agent.md:31-45`; `.github/agents/company-data-performance-lead.agent.md:35-48`; `.github/agents/company-building-safety-compliance.agent.md:29-31`; `.github/agents/company-finance-capital-grants.agent.md:28-42` | view | High | Role-charter constraints, not new consultation results. |
| C8 | Housing receives resident concerns; procurement does not own technical specifications; resident engagement cannot make service decisions or override consent; programme manager cannot commit capital. | `.github/agents/company-neighbourhood-housing-officer.agent.md:28-30`; `.github/agents/company-procurement-contracts.agent.md:29-42`; `.github/agents/company-resident-engagement-insight.agent.md:28-42`; `.github/agents/company-retrofit-programme-manager.agent.md:27-40` | view | High | Role-charter constraints, not new consultation results. |
| C9 | The current session tool inventory exposes no local agent/task dispatch mechanism. | Current session tool inventory (not a repository file) | tool inspection | High | No new company-agent discussion was performed. |

### External Evidence

No external sources used.

### Contradictions / Conflicts

No source conflict was found. The apparent mismatch is between prototype scope and PRD intent: the prototype is a constructed-data concept, while several PRD workflow and audit requirements describe future product behavior. Keep those categories separate. PRD role names remain provisional, and company-profile boundaries are sector-informed rather than Proper North Homes facts (C3, C5-C6).

## Findings Mapped to Questions and Evidence

### Q1: What each profile can do and what is missing

The prototype supports profile-filtered case queues, workflow entry points and selected case detail; the scenarios are constructed (C1-C2). Each row is analyst critique, not a fresh agent or user statement. Prior role feedback is included only where evidenced in the earlier review record (C4).

| PRD profile | Journey available in prototype | Critique and remaining gap | Evidence status |
|---|---|---|---|
| Asset and investment | Portfolio overview and asset/investment case queue. | Useful orientation, but no inspectable asset-level condition freshness, shared-works dependency, budget envelope or forecast assumptions. Static totals cannot support prioritisation or explain cohort inclusion. Prior asset/data perspectives flagged ambiguous forecast and stage-count labels; the current examples should remain clearly illustrative, and a genuine investment decision still needs baselines and assumptions. | Prototype observation + prior role perspective; actual asset decisions unvalidated (C1-C2, C4-C5). |
| Retrofit programme coordinator | Programme view spanning constructed cases and workflow cards. | Broadest coordination view. The nine workflow cards filter the queue and describe conceptual areas; the eight cases remain stage-specific examples rather than an interactive home lifecycle. History does not establish handoff sender/receiver, acceptance, due date or next resident update. It supports a walkthrough, not a live handoff. | Prototype observation + PRD gap (C1-C3); workflow behavior corrected in the fresh review cycle. |
| Retrofit case team | Case queue and detail associated with a retrofit stage. | A case appears in one workflow slice, without a complete step sequence, responsible role, next resident update or validated transitions. The profile cannot rehearse one home's journey through survey, delivery and close-out. | Prototype observation + PRD gap; team workflow needs validation (C1-C3, C5). |
| Technical assessor and design reviewer | Limited design/review scenario in the workflow set. | Evidence lineage, design revision, assumptions, shared works and explicit review/return outcome are not represented as a traceable task. Viewing a case must not imply professional approval. | Prototype observation + role-boundary hypothesis (C1-C3, C6-C7). |
| Neighbourhood housing and resident liaison | Resident/housing-related scenario in a staff queue. | Does not show the resident's chosen contact route, consent state, reasonable adjustments, communication history or agreed next update. Those omissions are appropriate for a no-live-resident prototype, but mean the resident-facing journey is untested. | Prototype observation + prior housing/resident themes; behavior unvalidated (C1-C2, C4, C6, C8). |
| Repairs and building safety | Safety/referral case in the staff queue. | Does not show confirmed referral receipt, accountable receiver, urgency, due date, decision status or recovery from an unaccepted handoff. It must not imply a statutory conclusion or acted-on referral. | Prototype observation + role boundary; no real safety workflow validated (C1-C3, C6-C7). |
| Procurement and contract management | Supplier/capacity-related case or workflow view. | A capacity example is not a procurement journey: package, time period, evidence of capacity, procurement route, contract status and award authority are not linked. Prior company-role input cannot confirm supplier commitments or technical acceptance. | Prototype observation + prior role perspective; commercial details unknown (C1-C2, C4, C6, C8). |
| Provider / contractor contact | Staff-facing case view mentioning provider/contractor context. | Does not demonstrate an external provider portal or contractor journey: no provider identity/access, submission, clarification, evidence upload, acknowledgement or response state. Make the boundary explicit so the role label is not mistaken for a tested external experience. | Prototype observation; no matching dedicated company-role agent or direct provider research (C1-C2, C5). |
| Quality and assurance | Evidence/assurance scenario surfaced through a role queue. | Does not expose item-level evidence, acceptance criteria, defect ownership, reinspection, exception closure or immutable source/version history. It can prompt discussion but cannot support an assurance decision. | Prototype observation + PRD gap; no matching dedicated company-role agent (C1-C3, C5-C6). |
| Finance and grant administrator | Finance/invoice-related exception view. | An invoice exception is not a full finance/grant journey: no award terms, claim eligibility, committed/paid ledger, forecast variance, evidence reconciliation or approval authority. Keep invoice and grant states distinct; do not infer payment or award. | Prototype observation + prior finance-role perspective; actual controls unknown (C1-C2, C4-C7). |
| Digital operator and auditor | Data/source exception and returned-case examples. | Hints at data-quality and recovery work but omits import run identity, component health, permissions, failed/replayed operation state, audit export and version comparison. A static source-conflict label cannot rehearse recovery or reconstruct a decision. | Prototype observation + PRD gap; no matching dedicated company-role agent (C1-C3, C5). |

### Q2: Previous feedback and the added history

The earlier UX review covered all 11 profiles, and eight company-role perspectives were recorded. Those findings remain contextual input for the earlier interface, not fresh reaction to the later history disclosure (C4). The current timeline improves inspectability: reviewers can see a short scenario-specific sequence in case detail. However, the entries are constructed/illustrative (C2), while the PRD requires named receiver, accepted/rejected/returned handoff status and due dates, and AC-025 requires ordered history with timestamp, source, actor and version (C3). The timeline is a useful prototype prompt, not validated audit or event history.

### Q3: Fresh company-role discussion

No direct discussion with company-role agents occurred during this research cycle. The current session has no agent-dispatch tool (C9). The eight existing role perspectives were reused only as prior feedback; the three profiles without dedicated matching company-role agents cannot be represented by another role's opinion (C4, C7-C8). Written agent charters constrained interpretation; they were not used to impersonate new responses.

## Key Discoveries

* **F1 - Queue coverage is not end-to-end journey coverage.** All profile names and nine workflow cards are present, but the queues use eight stage-specific constructed cases. Workflow-card selection filters the queue and reveals explanatory text; it does not advance a home through connected, role-owned stages. This is adequate for concept orientation, not for validating programme handoffs (C1-C2; click-handler behavior corrected in the fresh review cycle).
* **F2 - History is illustrative, not audit-grade.** The disclosure makes case history visible, but entries do not provide the PRD's timestamp/source/actor/version evidence or full handoff states. Keep the sample-only warning prominent and do not present it as compliance, audit or operational history (C2-C3).
* **F3 - Profile labels must not imply authorization.** The prototype does not implement access controls or approval. Role boundaries vary across resident consent, safety judgment, procurement, finance and delegated asset approval. Profile selection is a view filter, not a permission change (C1, C6-C8).
* **F4 - Three profiles lack a matching company-role lens.** Provider/Contractor Contact, Quality and Assurance, and Digital Operator/Auditor have no fresh or dedicated role-agent response in this critique. Analogous procurement, data/performance or UX perspectives do not validate those journeys (C4-C5, C7-C8).
* **F5 - No direct user validation.** UX/role reviews are bounded design perspectives. Resident, staff, supplier and contractor workflows, accessibility needs and task success remain hypotheses until checked with appropriate people (C4-C5).

## Alternatives and Decision State

### Selected Recommendation

Not applicable in research-only mode. Fresh role-agent discussion could not be performed.

## Open Questions, Risks, and Residual Uncertainty

Fresh discussion should ask each available role representative to identify the first task they would perform, the minimum evidence needed to accept or return a handoff, and which timeline details are necessary without implying a real event log. The provider, quality and digital journeys need an appropriate representative or actual user because no dedicated matching company-role lens was available. Direct staff/resident/provider validation and accessibility testing remain open. No source changes were made.

## Current Decisions

* Research disposition: Executed for all 11 prototype profiles; fresh representative discussion not completed because dispatch is unavailable.
* Planning Readiness: Evidence supports a bounded critique and focused follow-up questions, not implementation planning or production requirement decisions. Research-only mode is preserved.

## Potential Next Research

* Re-engage matching company-role agents once a direct agent-dispatch capability is available; focus on whether timeline details are sufficient and which role journeys require explicit handoff/history context.

## Research Self-Check

* All 11 PRD profiles have an explicit critique, including the three without dedicated company-role agents.
* Three ordered waves were completed: profile/workflow breadth; comparison with PRD handoffs/history and prior feedback; contrarian check against over-simulating authority or audit evidence.
* Internal factual findings have stable evidence IDs and workspace-relative path/line locations. No external sources were used.
* The artifact distinguishes prototype observations, prior feedback, sector-informed role boundaries and analyst hypotheses; no company facts or fresh agent responses are invented.
* No source or PRD files were edited. Fresh company-representative discussion and direct user research remain unavailable in this session.

## Sources

Repository sources only; no external sources used.

| Artifact | Description |
|---|---|
| [.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html](../../prototypes/2026-10-06/proper-warm-retrofit-workbench.html) | Current constructed-data prototype reviewed |
| [docs/prds/proper-warm-retrofit-programme-demonstrator.md](../../../docs/prds/proper-warm-retrofit-programme-demonstrator.md) | Current PRD, profile definitions and workflow/history requirements |
| [.copilot-tracking/changes/2026-10-06/prd-prototype-changes.md](../../changes/2026-10-06/prd-prototype-changes.md) | Prior profile critique, company-role perspectives and case-history implementation record |
| [docs/reference/research/company/company-profile-research.md](../../../docs/reference/research/company/company-profile-research.md) | Sector-informed company role and decision boundaries |

## Next Steps

This historical next step is superseded by the fresh review cycle below.

## Fresh Parallel Company Review - 2026-10-06

All nine company profiles were dispatched before collecting any results.
These are fresh read-only source reviews of the current prototype, including
the added case history. They are not browser usability tests, employee
interviews or company approvals.

| Company profile | Agent ID | Status |
| --- | --- | --- |
| Asset Executive | c0e5ed57-7784-4c44-985f-2662371166d1 | Own-role review received |
| Data and Performance | efb91fa0-b671-49cf-b821-3f8ebf55e08b | Received |
| Building Safety | 9dc59d8b-90b0-4591-ab88-5241dc34f9d9 | Received |
| Neighbourhood Housing | a9a36611-bd73-4140-b52b-5163fa8f9378 | Received |
| Finance and Grants | 061e5acf-83c8-40cf-a527-9fa59ade138a | Received |
| Executive Reviewer | 149fa9ab-02c4-4cbc-bd6f-71307ecc558f | Received |
| Procurement and Contracts | a6ef6829-b65a-483d-955b-61fd8439eacf | Received |
| Resident Engagement | ca524a2c-718d-4393-abe1-2e04ba35863d | Received |
| Retrofit Programme Manager | c174b5ad-d9d5-4641-8141-622c70ab9d89 | Received |

### Responses Received

| Perspective | Fresh findings and recommendations | Questions for UX discussion |
| --- | --- | --- |
| Executive Reviewer | Portfolio card filters to no matching case; explain concept-only coverage or add a constructed portfolio scenario. Three-entry narrative history is not audit evidence. Profile filters are not permissions or complete journeys. Headline populations (128 exercise homes, 42 active, 7 holds/reviews, 19 handover) need an explicit relationship to the eight inspectable cases. Accept the existing unknown/authority labels as strengths, not production functionality. | Which workflow anchors the demonstration? Should role walkthroughs foreground accountable handoffs or the shared queue? |
| Neighbourhood Housing | EX-HOME-208 lacks actionable next-update owner/date and service/complaint route; EX-HOME-863 lacks return reason/receiver; EX-HOME-531 lacks visible awareness time and owned follow-up. Represent unknowns without inventing company channels, support needs or SLAs. Explain portfolio's empty queue. Existing sample-view, source-context and no-contact boundaries are strengths. | What minimum fields make a resident-update commitment actionable without implying contact occurred? How should consent, access, complaints and support be distinguished with minimum necessary information? |
| Resident Engagement | EX-HOME-208 does not demonstrate measure-specific choice, pause or withdrawal (FR-014/AC-017). EX-HOME-531/863 need distinct accountable owner, proposed receiver and update owner (FR-011/AC-014, FR-015/AC-018). Add fabricated accessible-contact and complaint/defect routes, not sensitive resident history. Focused resident queue excludes related safety/quality/return exceptions; prefer two or three richer linked scenarios over additional profiles. Existing no-wider-consent, authoritative-hazard-service and independent-quality boundaries are strengths. | Which synthetic resident journey comes first: paused measure, accessible contact or complaint/defect with hazard? How is update responsibility retained while an operational handoff is unaccepted? |
| Procurement and Contracts | Queue header "Next owner" displays the current `item.owner`, especially misleading for unassigned EX-HOME-863 (HTML 680, 939-940, 964-966). EX-HOME-317 cannot demonstrate package/capacity readiness without period, scope, call-off and work-order version (AC-019). Narrative history does not reconstruct returns. Static "Why is this suggested?" still describes a missing link for supplier, quality and invoice cases; make rationale case-specific. Provider review is an adjacent lens, not contractor validation. | Prioritize capacity reconciliation or draft-package readiness? Can one linked package demonstrate provider correction, independent quality review and a finance exception with distinct owners? |
| Finance and Grants | EX-HOME-752 lacks constructed invoice/commitment/work-order/accepted-milestone comparison (FR-018/AC-021). Finance and portfolio do not demonstrate separate investment, grant, claim and cash states (FR-019/AC-022). Return history lacks receiving owner/reason. Enrich invoice evidence while leaving payment unavailable and company limits unknown; keep budget, invoice, payment, grant and cash distinct. | Deepen invoice match first or add separate grant/cash ledger? Which review-owner/handoff details can be shown without implying known authority limits? |
| Data and Performance | Histories lack time/actor/version and EX-HOME-863 source wording says "with return reason" while its context says reason absent. Fixed 128/42/7/19 snapshot cannot reconcile to eight cases and is not filter-responsive. EX-HOME-646 does not expose its conflicting values/dates. Portfolio empty state, retained search on profile switch and workflow overriding profile scope need explicit filter chips/reset. Agent reports source inspection and browser checks; this record does not independently certify browser conformance. | Test finding work or explaining waits first? Should workflow cards filter cases, open module context, or expose explicitly separate actions? |
| Retrofit Programme Manager | EX-HOME-104, 317 and 422 are separate homes, not one end-to-end path. EX-HOME-863/531 lack receiving ownership, return reason and next-update commitment. EX-HOME-317/422 share EX-BLDG-21 but do not expose the dependency's separate sequencing impact on each home. Recommend one read-only synthetic lifecycle and shared-building context; preserve independent home states, offered/committed capacity and professional authority (FR-001/002/011/013/015-017/022). | Anchor one home's lifecycle or a shared-building sequencing story? Deepen returned programme work or unreceived hazard referral first? |
| Building Safety | EX-HOME-531 shows "Repairs service" as current owner while receipt is unconfirmed; distinguish destination, accepting owner and chase owner. Awareness timestamp is referenced but not displayed, and history lacks actor/time/version. Linked hold lacks affected-work scope and accountable human release evidence. Workbench labels cannot establish hazard decisions or release (FR-011/015/022, AC-014/018/025). | Who retains chase responsibility until receipt and what evidence proves receipt/acceptance? How are held scope and release reviewer shown without transferring hazard authority? |
| Asset Executive | Label fixed 128-home snapshot as independent of eight cases, not a queue drill-through. Current asset exception view does not demonstrate investment evidence; baselines, condition freshness, capital envelope and approvals stay unknown. Add small shared-building context for EX-HOME-317/422 without merging their states. History remains illustrative. A bounded exception-to-accountable-owner slice can precede a fuller lifecycle. Only this agent's own-role source findings are attributed here; its nested review/UX orchestration and participation claims are outside this review's provenance. | Prioritize delivery blockers or missing investment evidence? Which evidence and role establish each home's exposure to a shared-package dependency? |

### Independent Coverage Check

Extracting the prototype's data definitions confirmed 11 profiles, nine
workflows, eight cases and three history entries per case. Default queues are:

| Profile ID | Constructed case suffixes |
| --- | --- |
| asset | 317, 646, 752 |
| coordinator | 104, 208, 317, 422, 531, 646, 752, 863 |
| case-team | 104, 208, 317, 422, 531, 863 |
| technical | 104 |
| resident | 208 |
| safety | 531 |
| procurement | 317 |
| provider | 317 |
| quality | 422 |
| finance | 752 |
| digital | 646, 863 |

The `portfolio` workflow has no matching case. Workflow selection does filter
the queue; this corrects the earlier inline critique.

### UX/UI Designer Synthesis and Discussion

The UX/UI Designer was launched as agent
`53381997-d5e8-401a-9802-53261ea4ab40` after eight company responses,
then received the ninth Asset response. Its initial synthesis covers all
11 profiles with hypothesized JTBD, current path, safe block/recovery/handoff
and integrated accessibility considerations. No interviews, device-context
validation or WCAG conformance assessment was claimed.

The designer could not message peers from its own tool surface. The parent
therefore relayed its four bounded proposals to Procurement, Resident
Engagement, Building Safety and Data/Performance for response and subsequent
designer disposition. Receipt and acceptance were explicitly corrected as
separate states: receipt alone does not establish acceptance. Retained chase
ownership is a proposed exercise behavior pending real company validation,
not an established company rule.

Initial priorities:

* Correct current/receiving ownership labels, case-specific suggestion
  rationale and EX-HOME-863's contradictory source/return wording.
* Expose active filter scope/reset; distinguish an unrepresented portfolio
  scenario from a search with no matches. Disclose the fixed snapshot's
  separate denominator/as-of scope.
* Next, deepen a read-only synthetic home journey and a second-home
  shared-building dependency. Keep consent, safety, quality, capacity and
  invoice/payment/grant/cash states independent.
* Defer authenticated permissions, live integrations/contact, operational
  transitions, approved company controls and durable audit history. Source
  review does not certify accessibility or validate real user behavior.

### Peer Replies and Final UX Disposition

| Peer | Response to relayed proposal | Final UX disposition |
| --- | --- | --- |
| Procurement | Agrees, amended to draft package readiness rather than release. Add unknown/unmet prerequisites and named next reviewer; readiness is not instruction, booking, commitment, acceptance or payment. | Adopt draft-readiness framing and independent submission/review boundaries. |
| Resident Engagement | Owner/due/status alone insufficient: add update purpose/linked issue, minimum-necessary safe-route/adjustment reference or unknown, sent time/evidence. Sent does not imply receipt or understanding. Outstanding owner persists until sent or explicitly reassigned; actual continuity rule requires validation. | Adopt amendment. Treat continuity as synthetic scenario assumption, not company policy; validate with Housing/Programme and real users. |
| Building Safety | Show referral destination/chase owner, sent time/reference, confirmed receiving role/time only with evidence, pending follow-up; hold scope/source/status and read-only human release-decision evidence in authoritative service. | Separate sent, receipt, acceptance, resolution and authorization. Workbench cannot judge release sufficiency or own hazard clock/classification/closure. |
| Data and Performance | Reconciliation and visible scope before analytics; unresolved conflict with provenance/resolution owner valid. Reveal denominator/as-of/filter impact and source values; separate cohort or reconcile; unrepresented portfolio is not no actual work. | Adopt source/filter-first sequencing without demanding conflict resolution as proof of completeness. |

After receiving the ninth Asset review and all four replies, the designer's
final recommendation is correctness/evidence/filter clarity, then a bounded
exception-to-accountable-owner slice, then a broader read-only lifecycle.
Link EX-HOME-317/422 to their shared building without transferring either
home's gates. Preserve the fixed snapshot as explicitly independent of
the eight cases, rather than claiming metric drill-through.

The complete eleven-profile JTBD/route/safe-block/accessibility matrix,
ranked acceptance checks, evidence limits and discussion amendments are filed
in the knowledge base:
[Proper Warm Prototype Profile Review](../../../docs/reference/research/ux/proper-warm-prototype-profile-review.md).
The knowledge-base index and append-only log were updated. No prototype
fixes were implemented by this review. Company processes, real device/context,
accessibility needs and user-success thresholds remain unvalidated.

### Final Handoff Check

The UX/UI Designer read the filed knowledge-base review and returned `PASS`:
the document distinguishes nine company-profile calls from four actual
proposal discussions, adjacent lenses from real-user evidence, immediate
correctness fixes from later lifecycle scope, receipt from acceptance, and
sent update evidence from resident receipt/understanding. It also makes the
unchanged prototype explicit.

The parent checked all eleven profile rows, four discussion dispositions,
dated frontmatter, relative source links and the Git whitespace/diff scope.
Only review documentation, its knowledge-base index/log and this working
record were changed. Existing uncommitted prototype/RPI artifacts were not
discarded, moved or included in a commit.
