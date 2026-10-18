<!-- markdownlint-disable-file -->

# Task Research: issue-156-design-traceability-gate

| Field | Value |
| --- | --- |
| Date | 2026-10-18 |
| Researcher / agent | RPI parent, inline |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-18/issue-156-design-traceability-gate-research.md |

## Research Brief

* What to research: existing profile/core-flow inventory, journey/task-flow and design evidence, decision provenance and a truthful design-review gate for #156.
* Why it matters: make missing evidence actionable without inventing acceptance.
* Audience: feature authors, design reviewers and delivery coordinator.
* Scope: existing UX synthesis, KB index/log and dated RPI evidence.
* Non-goals: UI, runtime, configuration, agent, prompt or workflow changes; new prototype programme; backlog-wide acceptance; private data; #398 resumption; rebase.
* Criteria: exact sections, versioned sources, explicit missing evidence and human boundaries.
* Requested outputs: research, plan/details, one independent critique, implementation/changes, one original independent Review and state, committed together.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which existing home and finite inventory best support traceability? Which evidence is historical or absent? |
| Codebase scope | docs/reference/research/ux, PRD, architecture index |
| External scope | Public jmservera/ama issues and PR metadata only |
| Initial internal candidate areas | Prototype profile review, shared workbench IA, customer journey atlas, PRD evidence trace |
| Initial external candidate areas | #156, #150, #149, #399, #398 |
| Research posture | focused |
| Posture provenance | Caller bounded documentation slice |
| Explicit limits | One independent critique; one original Review; no second/amended Review; coordinator owns later corrections, at most two |
| Completion basis | Finite scope and material evidence coverage |
| Edits allowed during research | Research/state tracking only |
| Resolved evidence root | .copilot-tracking/ |
| Excluded sources | support/, private datasets, live Graph/Azure/IAM/inference |

## Extension Registry and Provenance

| Kind | Candidate | Provenance | Authority | Disposition |
| --- | --- | --- | --- | --- |
| Instruction | .github/copilot-instructions.md | Repository-wide | KB, branch and evidence conventions | Selected |
| Skill | rpi-research | Active RPI Research | Three ordered waves and evidence | Selected |
| Skill | documentation | Documentation curation | Author/validate conventions; repository-specific checks prevail | Selected for subsequent authoring |
| Skill | accessibility / web-design-guidelines | Potential UI relevance | No UI review or conformance assessment in this slice | Skipped: documentation-only evidence curation, not a site audit |
| Specialist | hve-core-all:rpi-researcher | Available | Independent research lane | Skipped: tightly coupled bounded trace handled inline |

## User Participation and Research Decisions

Caller explicitly requests the full ordered loop; no additional mode confirmation
is needed. Automatic continuation is authorized through the original Review and
publication condition, not new follow-up work. No questions: non-interactive and
sufficient scope. Human design/user acceptance is not delegated to this agent.

## Scope and Success Criteria

Preserve contrary evidence to the issue's historical "no task flows/log" claim.
Select a finite PRD profile/core-flow inventory; mark all missing designs
`Not supplied`. Distinguish documentation, engineering, human design and user
research outcomes. No AC closure or owner approval invented.

## Task Research Requests

Verify live dependencies, owner Fluent 2 decision and historical partial
implementation; source-pin representative links and statuses.

## Direction Controls

| Control | Source | Effect |
| --- | --- | --- |
| Bounded documentation only | Caller 2026-10-18 | Stop if a UI edit becomes necessary |
| Retain base 3104bb69ddc26c81e0e9d2f57000dac1d99a419a | Caller | No rebase, even if main moves |
| Preserve original critique/Review | Caller | Findings route later, no self-pass |

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Which synthesis and finite inventory? | depth | Answered C1/C2 |
| Q2 | Which existing task flows, designs and decisions are real? | depth | Answered C1/C3/C4, W2 |
| Q3 | Which acceptance gaps must remain open? | depth | Answered C5/C6/C7 |

## Prior Knowledge Gate

Read original case study, addendum opening and relevant UX assumptions, KB index
opening/routing and owner memory. Memory is context, not evidence. Clean topic
branch matches caller, HEAD is the supplied base; no existing PR for this branch.
Live #156 is open with no comments and blocked_by returns []; its body names
#150 and parent #149. #150 is closed with owner Fluent 2 comments, not proof of
full UI acceptance. #399 is now merged; retain supplied base. #398 remains draft
and outside scope, with caller reporting exhausted corrections.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Identify existing UX homes, profile inventories and evidence boundaries inline.
Initial index confirms existing design-system/WCAG/content syntheses and
historical journey research; prioritize exact sections over a new library.
Reflection: issue descriptions are historical and must not override later docs.

#### Wave 2: Deeper

Prioritized C1/C2: all eleven PRD profile rows already have entry, evidence,
safe endpoint and recovery; C3 supplies a lifecycle/return diagram. Profile
synthesis contains historical HTML and later shared IA slice, so it is the best
existing home. Inspect exact journey headings, UX-01 to UX-08, WCAG/content
records and source pins. Historical HTML last changed at
c0f7c08aec514597af86528caf1bdad4b7250246; current baseline remains 3104bb69.
Reflection: use eleven profile rows plus explicitly bounded shared core flows;
do not equate eleven research perspectives to eight authenticated roles.

#### Wave 3: Contrarian

Challenge issue body "no task flows/log": C1/C2/C3 already contradict a universal
absence claim. Existing design choices, owner notes and sequencing are real
but not a unified trace register. Challenge apparent #150 acceptance: W2
establishes closed issue/owner choice, while pinned C4 explicitly says partial
native/token implementation and stale "stays open." Preserve both temporal
facts in the new dated section, not silently promote full adoption. C5 and C6
still lack manual/human results; architecture C7 is not a screen wireframe.
Reflection: an honest missing-evidence register can be documentation-complete
while overall design remains Blocked; no user study or current approved
wireframe is supplied by these sources.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Extend profile synthesis | C1/C2 | Accepted | Existing profile flows, checks and IA all co-located |
| New competing library | Caller/C1 | Rejected | Duplicates existing evidence and violates bounded scope |
| Eleven profiles plus named shared core flows | C1/C2/C5/C6 | Accepted | Finite reproducible inventory; not all backlog coverage |
| Overall design Pass | C4/C5/C6/C7 | Rejected | Exact current designs and required human evidence absent |
| Full feature inventory and human evidence | W1/W3/C2 | Deferred | Coordinator/design/research owners must supply and assess |

#### Cycle Re-entry Evaluation

No further cycle needed: finite documentation design is evidence-backed; the
missing human evidence cannot be produced by further repository search. Ready
to plan truthful curation, not ready for screen acceptance.

## Evidence Log

### Codebase Evidence

| ID | Finding | Location | Tool | Confidence / boundary |
| --- | --- | --- | --- | --- |
| C1 | Eleven profile flows, sequencing, UX checks and later IA evidence coexist | docs/reference/research/ux/zava-forward-prototype-profile-review.md:213-301,343-355,391-450 | view/rg | High; historical versus later evidence distinguished |
| C2 | Finite eleven-profile proposed contract | docs/prds/zava-forward-retrofit-programme-demonstrator.md:1905-1954 | view | High; proposed constructed walkthroughs |
| C3 | Existing lifecycle/return task flow and evidence trace | docs/prds/zava-forward-retrofit-programme-demonstrator.md:1407-1438,1675-1690 | view | High; not absent as issue body implies |
| C4 | Owner Fluent choice, partial native foundations, stale issue-open sentence | docs/reference/research/ux/design-system.md:18-33 | view/git log | High; source last changed a6e26fef42f7bea08ec763fc83facd16dc0302d6 |
| C5 | Proposed AA scope and Not run manual evidence | docs/reference/research/ux/wcag-conformance-baseline.md:23-34,86-104,127-136 | view | High; no conformance |
| C6 | Core-flow copy audit and missing named human wording review | docs/reference/research/ux/content-standard.md:79-117 | view | High; no resident approval |
| C7 | Excalidraw describes architecture, not screen layouts | docs/architecture/README.md:18-38 | view | High; cannot fill missing wireframe |
| C8 | Historical prototype exists, immutable source revision | .copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html:680,908-1020 | git ls-files/log; C1 source inspection | High existence/version; not a new runtime inspection |
| C9 | Journey sections explicitly hypothetical | docs/reference/research/ux/customer-journeys/programme.md:50-104; finance.md:49-104 | view/rg | High; exact headings used for links, not company observations |

Source baseline for all C evidence unless otherwise specified:
3104bb69ddc26c81e0e9d2f57000dac1d99a419a. No source mutation during research.
Research inline: no independent lane would improve this tightly coupled trace.

### External Evidence

| ID | Finding | URL | Retrieved |
| --- | --- | --- | --- |
| W1 | #156 open, no comments; body depends on #150, parent #149; API blocked_by empty | https://github.com/jmservera/ama/issues/156 | 2026-10-18 |
| W2 | Closed #150; explicit owner Fluent 2 decision 2026-10-15 | https://github.com/jmservera/ama/issues/150#issuecomment-6194477486 | 2026-10-18 |
| W3 | #149 open; child acceptance and actual usability evidence remain required | https://github.com/jmservera/ama/issues/149 | 2026-10-18 |
| W4 | #399 merged, head 60501707608a24816ad7b3f5c3b92bbe9eb802f0 | https://github.com/jmservera/ama/pull/399 | 2026-10-18 |
| W5 | #398 open draft, head 1144647c8d539716e8ddddf9daa47407c9bd00ac | https://github.com/jmservera/ama/pull/398 | 2026-10-18 |

## Findings Mapped to Questions and Evidence

Q1: extend C1, not a new IA page. Q2: C1/C2/C3 supply real existing task-flow
sections; C8 is a historical demonstrator, no approved current wireframe.
Q3: C4/C5/C6 block full acceptance; W1/W3 keep #156/#149 open.

## Alternatives and Decision State

Selected: extend the existing profile synthesis with a dated register, eleven
profile rows, a named shared-core-flow inventory, decision register and an actual
blocked gate record. Separate IA home rejected because IA is already a section
of C1. New competing design library rejected by caller.

## Open Questions, Risks, and Residual Uncertainty

Human design review, resident wording review and complete backlog coverage are
not supplied by inspected evidence. Require named people, exact artifact/text
versions and actual outcomes later. Source pinning is not a rendered review.
Current whole-application/backlog coverage remains unknown, including #215 and
future screen features outside the declared finite inventory.

## Current Decisions

Caller scope and W2 Fluent 2 choice confirmed; recovery and sequencing from C1
remain sourced proposals/interpretations, not newly invented owner decisions.

## Potential Next Research

Inventory remaining screen features with coordinator; design owner supplies exact
current artifacts; named accessibility/content/user-research owners record results.

## Planning Readiness

Ready for bounded documentation planning, not design acceptance.
Research disposition: executed. Full Wider -> Deeper -> Contrarian cycle complete.

## Artifact Self-Check

Opening state preceded UX investigation. Three waves and contrary evidence
recorded. C/W claims have locations, dates and boundaries. No phase skipped;
no implementation or source edits performed in Research.
