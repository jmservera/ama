<!-- markdownlint-disable-file -->

# Task Research: role-screens-149-safety-review

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/role-screens-149-safety-review-research.md |

## Research Brief

* What: address PR #496 discussion r4391306128, auditing the same safety-context pattern across role queues.
* Why: specialist case links must not hide projected safety markers, hazard awareness/deadlines or follow-up owners.
* Audience: implementer, independent reviewer and owner of draft parent #496.
* Scope: shared specialist renderer, existing role queue renderers, projection contracts, focused tests and scenario source binding.
* Non-goals: integrating children #487-#495, changing authority/projections, regulatory reinterpretation, redesign, main publication or live deployment.
* Criteria: reuse existing workSummary and safety presentation; tolerate contractor rows without work; executable regression covers recorded clock context and missing work.
* Requested outputs: dated full RPI evidence, scoped audit, correction, tests and draft publication.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which projected fields and existing helper preserve SA-007? Do other queues lose the same context? Which exact regressions exercise real rendering? |
| Codebase scope | src/api web/tests/checks, core projection/tests and public scenario metadata |
| External scope | Exact GitHub thread and current Web Interface Guidelines |
| Initial internal candidate areas | role-screens.js, app.js, test_role_screens.py, core projection, API README |
| Initial external candidate areas | GitHub #496, vercel-labs/web-interface-guidelines |
| Research posture | focused |
| Posture provenance | Default for named code target and supplied failure evidence |
| Explicit limits | One parent --changed gate, not --all; no uv or secrets/.env; no child mutation |
| Completion basis | Material scope coverage and evidence sufficiency |
| Edits allowed | Evidence/state only during Research |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Match/provenance | Authority / disposition |
| --- | --- | --- | --- |
| Instruction | Repository guidance | All task inputs | Selected: append-only log, Fluent/plain-language baseline, safe branch publication |
| Skill | rpi-research | Full-loop user direction | Selected: three-wave evidence |
| Skill | web-design-guidelines | Changed web code | Selected: source fetched 2026-10-27 before edits; refresh for Review |
| Skill | redesign-existing-projects | Existing app | Skipped: no design improvement/redesign, only restored existing safety context |
| Specialist | Independent plan/review agents | RPI gates | Deferred to Plan/Review, not research delegation |
| Skill | design-taste-frontend | Public pages | Skipped: app screen, not public page |

## User Participation and Research Decisions

Inputs explicitly authorize the complete correction loop and branch publication.
No interaction is needed or available. Existing parent RPI evidence is historical:
this distinct correction retains its own stable identity and parent pointer.

## Scope and Success Criteria

The user-ordered preparatory rebase completed before application investigation.
Only the two rubric bot commits conflicted and were skipped. The log merged
without conflict; verify its original content preservation before publication.
No safety state, permission or deadline calculation is to change.

## Task Research Requests and Direction Controls

* Rebase first, then resolve the single thread and comprehensively audit the same pattern.
* Use the explicitly supplied current-worktree source roots for API tests.
* Correct a stale public scenario hash only if core tests establish the failure.
* Commit dated evidence with Conventional Commit/trailer, push parent with lease,
  leave #496 draft and retain final-head review evidence.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What marker/helper/clock fields constitute existing queue context? | depth | Answered C1-C3 |
| Q2 | Which other role queues or contractor responses exhibit this pattern? | depth | Answered C2-C5 |
| Q3 | What executable checks and source bindings must be preserved? | straightforward | Answered C6-C8 |

## Prior Knowledge Gate

Read original/addendum, knowledge-base index/memory, sector primer, source gate
guide and original parent state. Cross-session branch lookup returned no rows;
tracked artifacts and exact GitHub feedback are the evidence, not assumed history.
Original parent Review is adverse and remains immutable.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Exact thread confirms missing safety marker/workSummary, including hazard clocks,
and omitted contractor work. Initial web search locates workSummary in app.js;
specialist links currently contain only a generic status sentence. Prioritize
the helper, queue callers and actual API projection contracts for Deeper.

#### Wave 2: Deeper

Inline inspection established the exact contract: staff open-case responses carry
`hazard` and role-projected `work`; contractor allow-lists carry neither. Existing
`workSummary` names the task owner separately from each hazard follow-up owner,
and maps all clock records with awareness, elapsed hours, response/update due
times and external timing authority. It requires a real work object. Generic
mine/all queues already show the marker and call this helper for every row.

Reflection: restore this same context in the one shared specialist host, not in
each independent child module. Render work for every supplied row, not just
hazard rows, preserving handoff/source context consistently. Guard only the
optional projected work boundary, not malformed internal clock arrays.

#### Wave 3: Contrarian

Challenged the assumption that a generic status is adequate: status may name a
different owner, and closed cases explicitly say Completed even with a later
hazard (C3/C5). Challenged universal work availability: contractor rows have no
work by deliberate privacy contract (C4). Do not synthesize staff context or
request extra endpoints for them. Unknown clock fields already have explicit
Unknown text from the server/helper and must remain visible.

Inventory covered all web case-list consumers: specialist host, mine/all task
queues (all seven staff roles), contractor jobs, manager closed-case archive,
coordinator lifecycle record table, overview map/list, pending handoffs and
finance/work-order lists. Only specialist and mine/all consume open-case
`work` projections. The latter already preserve them. Contractor jobs deliberately
omit them; closed archive and coordinator summaries do not receive work. Maps,
handoffs and domain lists are not work-context projections. No duplicated
specialist queues exist on this parent; all nine child views use this host.

Reflection: fixing the host addresses every installed specialist role without
changing permissions. Archive/coordinator backend enrichment would be a distinct
feature, not a second occurrence of dropping an available work projection.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Restore marker and guarded workSummary in host | C1-C4, W1 | Accepted | Reuses existing authoritative projection/presentation |
| Duplicate timing calculations or fetch staff-only data | C2-C4 | Rejected | Wrong authority and privacy boundary |
| Rewrite each child or broaden archive/coordinator schema | C5 | Rejected for this correction | No duplicated host; those summaries do not project work |
| Add executable renderer and actual browser checks | C6-C7 | Accepted | Existing units only check source strings; parent browser normally has an empty registry |

#### Cycle Re-entry Evaluation

No further cycle required: all material questions answered; no remaining source
gap changes this bounded fix. All research stayed inline because it is a single
continuous projection/render trace.

## Evidence Log

| ID | Claim / finding | Location | Confidence |
| --- | --- | --- | --- |
| W1 | Exact unresolved thread requests projected marker, workSummary and contractor guard | https://github.com/jmservera/ama/pull/496#discussion_r4391306128 (retrieved 2026-10-27) | High |
| W2 | Current web rules require semantic navigation, non-colour context, localized dates and keyboard access | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-10-27) | High |
| C1 | Specialist queue currently renders only label(row) | src/api/src/zava_forward/api/web/role-screens.js:73-81 | High |
| C2 | Existing helper maps all hazard clocks, handoff and source context; mine/all queues show hazard marker and helper | src/api/src/zava_forward/api/web/app.js:312-320,353-365 | High |
| C3 | Open staff rows receive work; hazard marker is independent of generic status; closed archive has no work projection | src/core/src/zava_forward/core/store.py:166-191,250-277,295-307; src/core/src/zava_forward/core/sqlstore.py:927-963 | High |
| C4 | Contractor summary allow-list excludes hazard and work; tests assert no work for actual contractor HTTP calls | src/core/src/zava_forward/core/projection.py:42-43,82-86; src/api/tests/test_task_queue_api.py:180-200 | High |
| C5 | Other case-list consumers have different bounded schemas; no additional dropped open-task work projection | src/api/src/zava_forward/api/web/app.js:297-308,804-830,1013-1040,1204-1208; src/api/src/zava_forward/api/web/panels.js:424; src/api/src/zava_forward/api/web/ops.js:124 | High |
| C6 | Host tests are currently static; parent browser checks empty registry, child tests install their own expectations | src/api/tests/test_role_screens.py:1-40; src/api/checks/role_screens_browser_check.py:15-40 | High |
| C7 | Existing synthetic fixture includes an open hazard and separate aware/response times; browser checks own loopback server | src/api/checks/role_screens_fixtures.py:35-42; src/api/checks/workbench_browser_check.py:18-61 | High |
| C8 | Manifest validator checks current source hashes without mutating; relevant tests assert version/coverage unchanged | src/core/tests/test_scenario_manifest.py:17-34; src/README.md:57-151 | High |

## Findings, Alternatives and Decision State

Selected approach: add the existing `Safety issue open` text/class from the
projected hazard flag and `row.work && workSummary(row.work)` to each specialist
link. Keep native links, URL selection/page, server scoping, recorded context
and external timing authority unchanged. No new helper or abstraction is needed.

## Open Questions, Risks and Further Research

Missing work must not crash or invent clock records. Test actual host rendering,
multiple independent clocks, different task/follow-up owners, Unknown values,
non-hazard work and contractor-shaped no-work rows. Parent browser coverage needs
a test-only installed module because the production parent registry is empty.
Human/screen-reader/Fluent adoption acceptance and integrated child validation
remain separate. No legal currentness claim is made by restoring recorded data.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready (C1-C8, W1-W2).
Self-check: three waves complete in order, alternatives resolved, all questions
answered, no source changes during Research. Parent may advance to Plan.
