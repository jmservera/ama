<!-- markdownlint-disable-file -->
# RPI Plan Critique: Design traceability and review gate

## Metadata

* Task ID: 156
* Critique date: 2026-10-18
* Plan: .copilot-tracking/plans/2026-10-18/issue-156-design-traceability-gate-plan.md
* Phase details: .copilot-tracking/details/2026-10-18/issue-156-design-traceability-gate-phase-details.md
* Research: .copilot-tracking/research/2026-10-18/issue-156-design-traceability-gate-research.md
* Critique execution status: Complete
* Candidate branch: docs/design-traceability-gate-156
* Candidate source baseline: 3104bb69ddc26c81e0e9d2f57000dac1d99a419a
* Critique instance: One independent final-candidate assessment; original record.

## Inputs and Criterion Boundary

The assessment covers the supplied research, final-candidate plan, phase
details and caller direction as one complete boundary. It assesses whether an
implementer can deliver a bounded documentation slice, not whether issue #156
can close or an application can pass human design acceptance.

Production scope is exactly the existing profile synthesis,
docs/reference/README.md and docs/reference/log.md, plus the declared dated
RPI evidence. The finite inventory is eleven existing PRD perspectives and
four shared core flows: queue scope/reset, case open/return, blocked
readiness/handoff and AI draft review. Other backlog coverage is unknown,
not implicitly covered by those rows.

Evidence inspected:

* docs/case_study_48_original.md and the opening exercise/evidence boundaries
  in docs/case_study_48_addendum.md; KB routing and owner memory for context.
* docs/reference/research/ux/zava-forward-prototype-profile-review.md:
  historical source boundary, All Eleven Profile Journeys, sequencing,
  owner feedback and reconciliation, UX-01 to UX-08, and Shared Workbench IA
  Engineering Slice.
* docs/prds/zava-forward-retrofit-programme-demonstrator.md:
  Case lifecycle, role handoffs and return path; BRD and evidence trace;
  Profile Journey Contract for the Next Prototype and its research limits.
* docs/reference/research/ux/customer-journeys/customer-journey-atlas.md:
  All-user coverage and jobs to improve; exact companion-map heading
  inventory, including programme.md and finance.md; programme.md's
  current-state journey hypotheses and role-specific sections.
* docs/reference/research/ux/design-system.md: Scope and evidence and
  Decision: adopt Fluent UI (Fluent 2).
* docs/reference/research/ux/wcag-conformance-baseline.md:
  proposed target/scope, audit, manual record, draft statement and open items.
* docs/reference/research/ux/content-standard.md:
  glossary, bounded core-flow copy audit, Human review and open items.
* docs/architecture/README.md: architecture provenance and static-view limits.
* Git object/path existence for historical prototype H at
  c0f7c08aec514597af86528caf1bdad4b7250246 and engineering manifest E at
  3104bb69ddc26c81e0e9d2f57000dac1d99a419a; the latter's actual profile,
  role, workflow, unknown and unavailable entries.

Public GitHub checks were confined to supplied dependency and trace targets.
On 2026-10-18, #156 and #149 were OPEN; #150 was CLOSED and its
issuecomment-6194477486 explicitly recorded the owner's 2026-10-15 Fluent 2
choice. #399 was MERGED, with mergedAt 2026-10-18T03:41:21Z; #398 was OPEN
and draft. Feature titles for #225 to #233 corroborated the proposed
role-family trace targets. No broader feature discovery was performed.

The caller's no-rebase, no-#398-resumption, no-UI/runtime/configuration/agent/
prompt/workflow changes and no-new-library/prototype rules are binding.
Exactly one later original independent implementation Review is permitted.
A Not accepted result freezes the local candidate and precludes a PR in
this task. These are execution constraints, not invitations to propose a
different delivery workflow.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Existing synthesis/index/log only; bounded production scope | Covered | P01 explicitly extends the existing synthesis. P01-T02 updates its KB routing and append-only log; no competing page or new prototype is planned. |
| C1/C2; eleven PRD perspectives | Covered | The inspected synthesis and PRD each contain eleven perspective rows. P01-T01 assigns T01-T11 and distinguishes perspectives from authenticated roles. |
| Four declared shared flows | Covered | Plan Scope names the four flows; P01-T01 assigns C01-C04. Existing UX checks and lifecycle/IA descriptions provide source material without manufacturing new task flows. |
| Exact feature/journey/task-flow trace | Covered | P01-T01 requires feature links, exact journey sections and matching existing flow rows. Companion-map sections exist. A shared section link must still identify its matching row, as the details require; a generic file link alone would not meet this plan. |
| C8; immutable historical artifact H | Covered | Both the exact historical object/path and latest path-changing revision were verified as c0f7c08aec514597af86528caf1bdad4b7250246. P01-T01 requires historical/source-only labeling. |
| E; current baseline engineering evidence | Covered | The pinned manifest exists and identifies version 152-ia-v1, eight roles, eleven perspectives and partial/deferred workflows. P01-T01 prohibits treating it as an approved current screen design. |
| Current design Not supplied; per-row actionability | Covered | P01-T01 requires every row to include current-design absence, requirement/check, evidence status, missing item, responsible role and concrete next action. No approval may be inferred from source coverage. |
| C4/W2; Fluent 2 decision and contradictory status text | Covered | Live owner choice/closure and pinned partial-native scope are both real. Plan AC explicitly retains the stale source sentence rather than rewriting history or inferring complete Fluent adoption. |
| Compact sourced decision register | Covered | P01-T01 specifies date/source, rationale, affected rows, status and open questions, while separating owner choice, reported feedback, derived proposals, sequencing and engineering trade-offs. |
| P01-T02; actual gate record | Covered | Details require candidate/exact artifact versions, reviewer identity/type/date, expected versus actual per gate, outcome, finding IDs, affected rows and owners/actions. The initial inspection is explicitly AI documentation evidence, not human approval. |
| C5; accessibility DoD | Covered | Existing proposed WCAG 2.2 AA target, AAA focus goal, manual checks and unconfirmed owner decisions remain linked rather than replaced by a new acceptance claim. Missing required evidence blocks overall design Pass. |
| C6; content and resident wording DoD | Covered | P01-T02 preserves named human review of exact resident-facing text and records the absent human reviewer/date. The inspected content standard requires name/role, date, exact text and outcome before use. |
| Separate documentation, engineering, human and user-research results | Covered | Functional requirements and P01-T02 require separate reporting; P02-T01 expressly prevents an accepted documentation Review from becoming overall design Pass or #156 acceptance. |
| Full backlog coverage and excluded surfaces | Covered | Research explicitly says current/future coverage is unknown. Plan Non-goals excludes named areas and identifies the four core rows as a subset, not the full content-audit surface. |
| P02-T01; documentation validation and ownership lock | Covered | Link/anchor, table, heading, source, scope, append-only and whitespace checks are specified; zero repository test additions/removals and zero generated production targets are locked. |
| #149/#150/#399/#398 dependencies | Covered | Live checks agree with supplied status. Historical issue-body absence claims are not treated as a present audit; no rebase or #398 continuation is required or authorized. |
| One original postimplementation Review and publication boundary | Covered | Plan Handoff and P02-T01 require preserving the original Review, no in-task correction/rerun and local freeze/no PR on Not accepted. Publication is conditional and does not close #156. |

## Verdict

* Verdict: Pass
* Critique execution status: Complete
* Severity counts: Critical 0; High 0; Medium 0; Low 0.
* Rationale: The plan is credible and implementable within the authorized
  documentation boundary. Required evidence, dependencies, tasks, validation
  ownership and stop conditions are sufficiently specified. Expected missing
  human/design evidence is deliberately represented as blocked acceptance,
  not omitted work or invented approval.

This is a planning verdict only. It does not assert that implementation has
occurred, that planned documentation checks have passed, that all screen
features have been inventoried, or that any human design gate can pass.

## Findings

The complete actionable PC-xxx finding set is empty. No evidence-backed
substantive plan correction or unresolved significant/divergent user decision
was identified across the supplied boundary. No finding is withheld for a
later critique. Inventing a PC-xxx item for an already specified requirement
or an explicitly accepted external evidence gap would incorrectly expand the
assessment beyond this documentation slice.

## Strengths and Residual Risk

* Existing task-flow evidence contradicts a universal reading of #156's
  historical absence statement. The plan correctly curates that evidence
  instead of commissioning replacement flows.
* The historical HTML and the migrated engineering manifest have different
  provenance and coverage. The plan preserves both without representing
  either as current approved screen designs.
* The synthesis already records UX-07's incomplete return behavior: retained
  filters do not establish restored originating focus, selection or position.
  P01-T01's requirement for source-qualified checks/status must preserve that
  limitation, not mark the case-return flow accepted from the manifest alone.
* Feature links identify responsible delivery workstreams, not delivery,
  authorization or acceptance. In particular, grouping multiple PRD
  perspectives under #231 or #228 is a trace mapping, not validated role
  equivalence. #233 does not enlarge this finite implementation into every
  atlas responsibility.
* Planned link/table checks establish navigability and document integrity;
  semantic source review remains necessary to avoid a valid link pointing to
  the wrong task or check. P02-T01 already requires that independent comparison.
* The remaining risks below are explicitly retained by the plan and caller.
  They are not prerequisites for curation, but cannot be waived by its completion.

## Questions or Blocking Evidence Gaps

There is no decision-critical evidence gap preventing this planning assessment
or implementation of the bounded documentation slice. The following actual
human/product evidence remains absent and must appear as open register/gate
items, not as completed checks:

| Residual gap | Action owner | Exact later resolving evidence | Route and effect |
| --- | --- | --- | --- |
| Current screen-design artifacts and human design assessment | Design owner and named human reviewer | Exact artifact/version for affected rows, reviewer name/role/date, states and recovery reviewed, expected versus actual, findings and disposition | External evidence supply and human decision; absent evidence keeps overall design Blocked. No new prototype work is authorized here. |
| Manual accessibility and applicable scope decisions | Accessibility owner, owner and named manual testers | Applicable baseline target/scope confirmation plus versioned keyboard, screen-reader, zoom/reflow and other required check records with tester/date/tool/browser, criteria, outcomes and exceptions | Later named-human validation; static/native or engineering checks are insufficient. |
| Resident-facing wording approval | Content owner and named human wording reviewer | Exact text/version, reviewer name/role, date and outcome, covering every relevant resident-facing draft before use | Existing mandatory human approval, not an optional substitute or new policy decision. |
| Direct accessible staff/provider/resident research | Research owner and appropriate participants | Exact candidate/scenario, method, participant/accessibility context, actual observations/results and limits; no synthetic-role consensus substituted for participants | Later research evidence; documentation and engineering completion remain separate. |
| Coverage of remaining present/future screen backlog | Delivery coordinator | Explicit screen-feature inventory reconciled to journeys, flows, artifacts, checks and gaps beyond the fifteen declared rows | Separate bounded follow-up decision; coverage is currently unknown and #156 stays open. |

These owners are responsible roles, not invented named people or claims that
the fictional company has supplied operational delegations. Current direction
already resolves how to handle their absence: record it honestly and block the
affected acceptance, without expanding this implementation.

## Limitations

* This assessment verified material plan claims against supplied sources and
  their relevant sections, not every historical document or backlog item.
  No open-ended research, broad site audit or new evidence collection was done.
* No browser, assistive-technology, runtime, SQL, Azure, model, user or resident
  checks were executed or inferred. Those are not documentation-slice tests.
* External checks establish observed public status on 2026-10-18, not complete
  acceptance histories or the correctness of live software. #398's exhausted
  correction limit is binding supplied direction, not independently reaudited.
* Missing current design evidence is not a claim that no design artifact can
  exist anywhere; it means none is supplied for this gate.
* Initial source-read output exceeded tool display limits; focused file ranges
  were subsequently read for the material claims. Shell rg was unavailable;
  focused grep/sed reads supplied the necessary evidence. Neither limits this
  completed criterion assessment.
* Existing untracked research/plan/details/state were caller inputs and were
  not altered. This critique writes only its assigned artifact.

## Recommended Next Action

* Highest-impact finding: None; no actionable PC-xxx finding.
* Action owner: Planning parent.
* Smallest next action: Record the Pass disposition outside this immutable
  critique, then implement P01-T01, P01-T02 and P02-T01 within the locked scope.
* User response required: No.
* Preserve this original critique unchanged. Do not request another critique.
  The later original implementation Review is a different stage, not a rerun
  or a mechanism to convert missing human evidence into design Pass.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-18/issue-156-design-traceability-gate-research.md](.copilot-tracking/research/2026-10-18/issue-156-design-traceability-gate-research.md) | Supplied research and evidence boundary |
| [.copilot-tracking/plans/2026-10-18/issue-156-design-traceability-gate-plan.md](.copilot-tracking/plans/2026-10-18/issue-156-design-traceability-gate-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-18/issue-156-design-traceability-gate-phase-details.md](.copilot-tracking/details/2026-10-18/issue-156-design-traceability-gate-phase-details.md) | Assessed task details and validation lock |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-156-design-traceability-gate-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-156-design-traceability-gate-plan-critique.md) | One original independent critique |

## Next Steps

Return Complete / Pass to the active planning parent for disposition and the
already authorized implementation handoff. No user action is required.
This reviewer stops here without implementation, source/state changes,
another reviewer or an amendment to this original critique.
