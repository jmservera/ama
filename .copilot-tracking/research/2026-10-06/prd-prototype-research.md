<!-- markdownlint-disable-file -->

# Task Research: prd-prototype

| Field              | Value |
|--------------------|-------|
| Date               | 2026-10-06 |
| Researcher / agent | rpi-research |
| Status             | Complete |
| Artifact path      | .copilot-tracking/research/2026-10-06/prd-prototype-research.md |

## Research Brief

* What to research: The current Proper Warm PRD, its user profiles and workflow increments, the safety boundaries that shape a usable non-production prototype, and existing UX evidence relevant to the design.
* Why it matters: The prototype should demonstrate the actual product concept without implying live authority, while making role-specific work understandable and reviewable.
* Audience or intended use: AMA project owner and stakeholder/role reviewers evaluating the proposed workbench.
* Scope: Current repository branch at latest `origin/main`; PRD, source BRD, case-study context, company profile research, and existing UX journey; later review by UX/UI Designer and relevant company-role agents.
* Non-goals: Production implementation, real personal or operational data, live integrations or actions, changing PRD decisions, treating role agents as privileged company sources, or asserting user research validation.
* Criteria: Traceable coverage of the PRD's complete intended role/profile set and core workflow, explicit draft/exercise status, observable safe boundaries, and a prototype suitable for role-by-role UX critique.
* Requested outputs: A self-contained interactive prototype plus recorded research/plan/change/review evidence and responsive UX feedback for every profile.
* Output mode: convergence

## Research Parameters

| Field | Value |
|---|---|
| Research question(s) | Which PRD workflows and user profiles must the prototype expose, and what interface pattern best demonstrates them without suggesting production authority? |
| Codebase scope | `docs/prds/proper-warm-retrofit-programme-demonstrator.md`, linked BRD/case-study context, company profile research, existing UX journey, and prototype placement conventions |
| External scope | None; use repository evidence only |
| Initial internal candidate areas | PRD, BRD, case-study addendum/original, company profile research, UX journey, `.github/agents/company-*` and UX/UI reviewer |
| Initial external candidate areas | None |
| Research posture | balanced |
| Posture provenance | default, selected for a bounded but multi-workflow/profile prototype where adjacent UX evidence may affect the design |
| Explicit limits / deadline | No extra limit or deadline stated; prototype remains non-production |
| Posture-specific completion basis | PRD/profile coverage and design boundaries are evidence-backed; remaining questions do not materially change the demonstrator |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | `.copilot-tracking/` |
| Known constraints / excluded sources | Draft PRD; constructed records only; no real resident or company data; no production deployment or live actions |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
|---|---|---|---|---|
| Instruction | `.github/copilot-instructions.md` | Applies to all workspace paths (`applyTo: "**"`) | Preserve case-study distinctions, source evidence, and docs conventions | Selected; governs research and product claims |
| Skill | `rpi-research` | Explicit RPI phase | Three-wave research and canonical evidence artifact | Selected |
| Skill | `web-artifacts-builder` | Self-contained interactive HTML prototype requested | Clawpilot-themed HTML artifact constraints | Selected for later implementation |
| Skill | `frontend-design` | Prototype is a web UI | Production-quality, distinctive visual design | Selected for later implementation |
| Skill | `hve-core-all:ux-ui-designer` | User explicitly requests UX critique for every profile | Review each actual PRD profile, identify evidence/assumptions and actionable usability issues | Selected for post-build critique |
| Specialist | Proper North Homes `company-*` agents | Role profiles provide perspectives from documented decision rights | User-perspective feedback only; distinguish case facts, hypotheses and unknowns | Select after identifying PRD roles and matching agent scope |
| Specialist | `hve-core-all:rpi-researcher` | No independent high-volume research lane established | Bounded research lane artifact | Skipped; direct repository review is sufficient |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision or selected further research |
|---|---|---|---|
| Intake | No question: the named current PRD and request to build a prototype define the outcome; use constructed records and keep it non-production per the PRD. | None | Proceed with the current PRD and inspect its profile set before design. |
| Direction change | None to date | None | None |
| Convergence | Pending synthesis | Pending | Pending |

## Scope and Success Criteria

* Scope: Build a reviewable interface from current PRD evidence and request profile-by-profile UX feedback.
* Assumptions: The PRD is the target brief; "every profile" means every named user/role profile in that PRD, not a subset of dashboard modules.
* Success criteria:
  * Every role/profile and workflow surfaced by the PRD can be examined or exercised.
  * No live action, approval, or operational authority is implied.
  * Evidence class and constructed-data status remain clear.
  * UX critique explicitly covers each profile and findings are considered before completion.
  * The final artifact is verified and changes are reviewed.

## Task Research Requests

* Explicit requests: Update from latest `main`; build a prototype from the new PRD; have the UX Designer review user experience for every profile; optionally use company-role agents as user reviewers.
* Inferred research questions: Which profiles, workflow states, actions, metrics, and human authority boundaries should be demonstrated?
* Caller constraints and non-goals: Constructed/non-production evidence only; no profile feedback is treated as verified company research.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect on active brief, evidence, or revalidation |
|---|---|---|---|
| add | Include UX review for every profile and role-agent user feedback where relevant | User request | Prototype must expose role-specific surfaces; critique follows implementation |
| narrow | Use current PRD, no live data/action | PRD v0.6.2 and repository instructions | Prototype remains demonstrative and non-production |

## Research Questions

| # | Sub-question | Type | Priority | Status |
|---:|---|---|---|---|
| Q1 | What user profiles, workflows and increments are defined by the current PRD? | straightforward | H | answered |
| Q2 | What shared interaction, evidence and authority rules must the prototype preserve? | depth | H | answered |
| Q3 | Which UX/reviewer perspectives and repository output format suit the deliverable? | breadth | M | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/reference/README.md`, `docs/reference/memory.md`, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/prds/proper-warm-retrofit-programme-demonstrator.md`, `docs/brds/agentic-retrofit-programme-brd.md`, `docs/reference/research/company/company-profile-research.md`, and `docs/reference/research/ux/program-manager-document-workspace-journey.md`.
* Reused (verified) findings: PRD is draft v0.6.2 dated 2026-10-06; one role-based, home-centred workbench spans nine workflow areas and four increments; exercise data is constructed; the demonstrator does not perform live contact, supplier instructions, approvals, claim submissions or payment release.
* Superseded / stale: None. The separate document-workspace UX artifact is not evidence of retrofit-workbench usability.

## Research Cycle Log

### Cycle 1

* Active direction controls: Non-production, current PRD, all PRD profiles.
* Active research posture and completion basis: balanced; cover the exact product brief and relevant UX/safety constraints.
* Explicit limits or deadline effect: None beyond the product's non-production boundary.

#### Wave 1: Wider

* Plan and independent lanes: Identify profiles, workflows, increments, prototype surface conventions, and existing UX/research guidance.
* Worker evidence relationships or inline fallback: Inline repository evidence; no suitable independent lane is needed.
* Reflection: PRD v0.6.2 identifies 11 provisional workspaces, nine connected workflow areas and four increments. Residents are affected stakeholders, not users of the non-production MVP. Company-role research provides eight matching internal role lenses; provider, quality and digital operator profiles still need direct UX coverage.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Role-specific entry points must serve the same home/building case, with workflow queues and shared handoffs; safe actions, evidence classification and dashboard caveats are product-wide.
* Plan and independent lanes: Trace interaction requirements, action authority, evidence status, accessibility and validation to the PRD/BRD.
* Worker evidence relationships or inline fallback: Inline repository evidence.
* Reflection: Authority, privacy, accessibility, proposal review and workflow-only fallback are explicit PRD requirements. Role labels may shape the view but cannot authorize actions. Product profiles and system decisions remain draft; company approval, permissions, baselines and direct user validation are open.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge a selectable role view as potentially misleading; verify affected stakeholders are not accidentally given login journeys; check that an AI surface or portfolio chart does not imply verified data or authority. No live data/actions or changed requirements.
* Plan and independent lanes: Compare with the PRD's single-workbench rationale and constraints; test the document-workspace UX evidence for transferability and status.
* Worker evidence relationships or inline fallback: Inline repository evidence. Role-agent and UX Designer feedback is implementation review, not evidence that company users validated the PRD.
* Reflection: The PRD rules out permission by view selection; residents are not MVP users; all company baselines, authorities and actual role titles remain unknown. The old document-workspace study explicitly says reported/assumed and unvalidated, so no direct usability claim can be carried over.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition | Evidence-based rationale | Primary-artifact treatment |
|---|---|---|---|---|
| PRD v0.6.2 is the requested source baseline. | C1, C2 | accepted | The index names this as the current draft, and its dated frontmatter and scope agree. | Prototype will be linked to draft requirements, not treated as PRD approval. |
| The prototype should support all 11 listed workspaces on common records rather than become 11 independent products. | C3, C4 | accepted | PRD says roles use common governed case data and one workbench. | Role navigation will change task context, not identity or authority. |
| Prototype coverage includes all nine workflow areas and four increments. | C4, C5 | accepted | Both are explicit in the PRD; its success measure expects 9/9 workflows. | Include portfolio/workflow navigation and identify later-increment features as demonstrative. |
| Exercise status, safe authority boundaries, transparent evidence and accessibility must be visible. | C6, C7, C10 | accepted | PRD explicitly constrains data, permissions, proposals, charts, accessibility and no-live actions. | Mark constructed/demo data and avoid success-shaped approval actions. |
| Existing UX study proves this workbench's needs. | C9 | rejected | It is about a document workspace, not retrofit delivery, and its behaviors are expressly unvalidated. | Reuse only generic design hypotheses; request the specified profile-by-profile critique. |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: balanced scope covered by current PRD/BRD and prior UX evidence; contrarian checks did not reveal a missing source that would change a non-production prototype direction.
* Revised brief or revalidation required: none
* Readiness effect: Ready for Plan; implement the current draft with all PRD profiles and explicit provisional/non-production cues.

## Evidence Log

* Delegation: inline; no independent research lane met the delegation threshold.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|---|---|---|---|---|---|
| C1 | The knowledge-base index identifies PRD v0.6.2 as the current draft for all nine BRD workflows and four increments. | `docs/reference/README.md:82` | read / rg | high | Catalog summary dated 2026-10-06. |
| C2 | The product is one role-based, home-centred workbench; data is constructed and live decisions/actions are out of scope. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:34-72` | read | high | Executive Summary and case framing. |
| C3 | PRD role workspaces are explicitly provisional; the 11 rows name the complete in-scope profile set; residents are affected stakeholders, not MVP users. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:187-210` | read / rg | high | Profile/workspace choice is not authentication; direct user research remains open. |
| C4 | The workbench covers nine named workflow modules using common records and role views. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:264-280` | read | high | Workflow coverage and role mapping. |
| C5 | Four increments move from shared foundation to workflow coverage, coordinator insight and bounded-agent comparison; all remain one non-production product. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:604-627` | read / rg | high | Later increment surfaces may be clearly labelled demonstrative. |
| C6 | Role-context selection cannot grant access; suggestions create tasks/drafts only; AI is cited/unapproved and has a workflow-only fallback. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:289-316` | read / rg | high | Design boundary for controls and proposal state. |
| C7 | Accessibility requires keyboard/focus/readable status and chart equivalents; all MVP records must be constructed and non-identifying. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:328-378` | read / rg | high | Prototype should provide accessible controls and non-colour status. |
| C8 | Company role research contains an eight-role decision map and warns approval limits/reporting lines vary; no company authorities may be inferred. | `docs/reference/research/company/company-profile-research.md:284-297` | read | high | Role agents provide perspective, not company facts. |
| C9 | Prior UX artifact is specific to a repository document workspace and labels behavior as reported/assumed pending direct validation. | `docs/reference/research/ux/program-manager-document-workspace-journey.md:1-14` | read | high | Transfer only generic usability/accessibility hypotheses. |
| C10 | Draft PRD calls for all nine workflows represented, validated role tasks, permission boundaries and safety/resident/finance guardrails. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:648-662` | read / rg | high | Test target for prototype completeness, not a claim of product acceptance. |

### External Evidence

No external sources used.

### Contradictions / Conflicts

* No material conflict identified yet.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|---|---|---|---|---|
| Q1 | The current PRD names 11 workspaces and nine workflows in four increments. | C1, C3, C4, C5 | high | Represent every profile and workflow in the prototype. |
| Q2 | Shared home/building records, human authority, clear exercise status, accessible UI, and no-live-action constraints shape all views. | C2, C6, C7, C10 | high | Include explicit safe demonstration states and traceable interactions. |
| Q3 | UX/UI Designer should assess all 11 profiles; eight matching company-role agents can add bounded perspectives corresponding to PRD roles. | C3, C8, C9 | high | Run profile-by-profile critique after implementation; preserve gaps where no company role exists. |

## Key Discoveries

* The task targets one shared workbench, not 11 isolated products or persona dashboards; its 11 provisional profiles span internal roles and an external provider contact.
* All nine workflows belong in the scope. The four increments supply a completeness check, but a clickable demonstration does not prove acceptance evidence.
* The PRD is a draft and the records are constructed, so the prototype must make its exercise status conspicuous and present role switching as a view, never as access control.
* Existing UX evidence is from a different document-workspace concept and is explicitly unvalidated; use it only to seed accessibility and interaction checks.

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: A single-file interactive workbench with role-specific queues over common constructed home/building cases, an explicit profile picker, workflow navigation, evidence/status cues, accessible portfolio views, and source-linked proposals that never execute a real approval or external action.
* Rationale: The PRD explicitly chooses one shared workbench, all nine workflows and role-specific screens; it calls for source-linked next-step proposals, transparent forecasts and no live authority. A one-file artifact fits this repository's documentation-first structure and is easy to review.
* Evidence refs: C1-C7, C10.
* Implementation impact: New `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html`; no production app or PRD requirements will be altered.
* Confidence: high for scope/boundaries; medium for specific interaction hierarchy until the UX Designer reviews it.

## Open Questions, Risks, and Residual Uncertainty

* The PRD's company baselines, operational approvals and role ownership remain open; do not simulate them as known.
* A visual prototype cannot evidence authentication, server-side permissions, complete acceptance tests or actual workflow outcomes.
* Role-agent responses are bounded perspective checks, not evidence of actual employees, contractors or residents validating the product.

## Current Decisions

* Research disposition: executed (in progress).
* Planning Readiness: Ready. All profiles/workflows and the non-production boundary are specified; implementation can show concepts without resolving open operational decisions.

## Potential Next Research

* Company baselines, named product owner, approved permissions and direct user research remain open per PRD. These do not block a clearly labelled exercise prototype.

## Research Self-Check

* Primary artifact created before further substantive research: yes.
* Three ordered waves completed in order: yes.
* Stable code/external evidence IDs: C1-C10; no external evidence used.
* Scope, user request, non-goals and constraints recorded: yes.
* Planning Readiness: Ready.
* Research disposition: executed.
* Another cycle required: no; balanced coverage is adequate for Plan, with UX validation intentionally deferred to the post-build reviewer.

## Sources

* Repository sources only; all future prototype claims must keep draft assumptions and constructed records distinct from company facts.

## Advisory Next Step

* Proceed to Plan using this research artifact; review every profile with UX/UI Designer after the prototype exists.

| Artifact | Description |
|---|---|
| [.copilot-tracking/research/2026-10-06/prd-prototype-research.md](.copilot-tracking/research/2026-10-06/prd-prototype-research.md) | Completed research and planning-readiness evidence |
| [.copilot-tracking/rpi-sessions/2026-10-06/prd-prototype-state.json](.copilot-tracking/rpi-sessions/2026-10-06/prd-prototype-state.json) | RPI task state |

## Next Steps

* Advance to Plan; implement the converged non-production prototype and validate UX for all 11 profiles.
