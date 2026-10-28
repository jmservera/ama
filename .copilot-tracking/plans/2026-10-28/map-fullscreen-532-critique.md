---
title: Map fullscreen issue 532 final-candidate plan critique
description: One independent assessment of the supplied implementation candidate
ms.date: 2026-10-28
---

## Metadata

* Task ID: 532.
* Critique date: 2026-10-28.
* Plan: .copilot-tracking/plans/2026-10-28/map-fullscreen-532-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/map-fullscreen-532-phase-details.md
* Critique execution status: Complete.
* Assessment count: one independent final-candidate critique.
* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 3 Medium, 0 Low.

## Inputs and Criterion Boundary

* Caller requirements: near-fullscreen map, narrow left panel, home summary and
  native Open home link in both modes, embedded top-right close icon and map-click
  dismissal, keyboard operation, Escape ordering, focus return, non-colour status,
  reduced motion and a manual navigation path.
* Canonical evidence:
  .copilot-tracking/research/2026-10-28/map-fullscreen-532-research.md,
  including C1-C8, W1-W4, decisions, alternatives and stated limitations.
* Constraints: native existing stack; no framework swap, briefing edits, Azure
  commands, secrets, .env or private data. Preserve the locked test ownership,
  zero-removal rule and addition budget.
* Dependency and delivery context: feat/map-fullscreen-532 stacked on
  feat/case-journey-ux-526 / PR #529; use Refs #532. Coordinator owns pushing;
  a prohibited prerequisite blocks publication, not independent local work.
* Read-only git inspection confirmed the requested topic branch and upstream
  origin/feat/case-journey-ux-526. Plan, details, research and session-state files
  were already untracked. This critique does not move, stage or modify them.
* Repository context considered: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md,
  docs/reference/memory.md and the supplied design-system, WCAG and content
  evidence pointers. Memory was treated as context, not evidence.
* Concrete risk checks were limited to mapPanel, mapAction and route abort in
  src/api/src/zava_forward/api/web/app.js; the existing constructed browser
  harness and marker assertions in
  src/api/checks/design_system_browser_check.py; focused existing test references;
  and the local publication contract in src/README.md.
* Boundary: assess FR1-FR6, non-functional requirements, AC1-AC6, all three
  phases, test budget and delivery gates. No implementation, security audit,
  independent external research or heavy validation was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1, AC1, P01-T01 | Covered | Same Leaflet instance, placeholder, named native dialog, left panel and post-move sizing are planned. |
| FR2-FR3, AC2, C6-C7 | Covered | Summary-first activation and native link use only existing permitted fields, with unavailable/withheld data distinguished. |
| FR4-FR5, AC3, P01-T02 | Partial | Dismissal ordering, stable IDs and cleanup are explicit; initial focus and missing-target fallback need PC-002. |
| FR6, AC4 | Covered | Direct list links remain; expanded external-list shortcut closes the modal before navigation/focus. |
| Non-functional requirements, C3-C5, W2-W4 | Covered | Native semantics, Fluent tokens, status words/shapes, motion suppression, safe DOM construction and small-screen checks are retained. |
| P02-T01, AC4-AC5 | Partial | Real DOM behavior, coordinator omission, network restriction and pinned axe are planned; PC-002 completes the focus assertions within the same script. |
| Test ownership and budget | Covered | src/api owns one new unit module with at most six contracts, one focused browser script and the existing marker assertion updates; no removals. |
| P02-T02 | Covered | API README controls and evidence boundaries are directly related; no unrelated knowledge-base or briefing edits. |
| P02-T03 | Partial | Required validation paths conflict with current execution constraints; PC-001. |
| P03-T01, AC6 | Covered | One independent implementation Review, refreshed guidelines and preservation of original outcomes are explicit. |
| P03-T02 | Partial | Runtime identity lookup is required, but a fixed email overrides it; PC-003. |
| P03-T03, publication follow-up | Partial | No-Azure stop and stacked PR wording are correct; exact-head coordinator prerequisites need PC-004. |
| Research Q1-Q4, C1-C8, W1-W4 | Covered | Bounded evidence supports the chosen native approach; no decision-critical research gap was identified. |

## Verdict

* Verdict: Revise.
* The interaction architecture and scope are credible. Four bounded planner-owned
  corrections are needed before execution. They do not require framework changes,
  new payloads, another critique, additional test files or removal of tests.
* Complete describes execution of this assessment only. It does not mean the plan,
  implementation, accessibility acceptance or publication gate has passed.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Validation paths are prohibited in the current execution context

* Related IDs: P02-T03, AC5; research direction controls.
* Evidence:
  .copilot-tracking/details/2026-10-28/map-fullscreen-532-phase-details.md:42-47
  requires a venv and shared lock under /tmp. Current caller execution constraints
  prohibit file operations there and require newly created working files to be
  project-relative.
* Concern: The proposed dependency setup and lock admission cannot be executed as
  written. Substituting an unrelated project-local lock would also lose shared
  exclusion against other heavy-check owners.
* Impact: Validation either stops before running or violates execution/isolation
  constraints; an uncoordinated replacement lock risks concurrent heavy runs.
* Smallest useful change: Use a permitted project-relative dependency environment
  only after the actual missing-dependency result. State that shared-lock admission
  is blocked unless coordination supplies a permitted way to acquire the same
  shared exclusion. Preserve nonblocking admission and the existing 40-minute
  bound where acquisition is permitted. Do not silently relocate the lock or run
  unlocked. Identify permitted evidence storage separately from the external final
  publication receipt, which remains a coordinator responsibility if unavailable.
* Action owner: Planning parent; coordinator owns shared-lock availability.
* Exact resolving evidence: Revised P02-T03 names the permitted environment/output
  paths and either identifies an allowed shared-lock mechanism with the same
  exclusion or explicitly records the affected checks as Blocked with the
  coordination resume condition. No /tmp or other forbidden-directory operation
  remains an implementation instruction.
* Decision route: Direct planner correction. No significant/divergent user
  decision; current execution restrictions already resolve the conflict.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Focus entry and missing-marker recovery are not defined

* Related IDs: FR2, FR4-FR5, AC3-AC4, P01-T01-T02, P02-T01.
* Evidence:
  .copilot-tracking/details/2026-10-28/map-fullscreen-532-phase-details.md:12-25
  makes the title focusable, requires stable-ID recovery and forbids ordinary
  redraw focus theft, but does not state actual initial focus or fallback targets.
  src/api/src/zava_forward/api/web/app.js:1335-1344 leaves marker activation focus
  on the marker; mapPanel replaces markers during draw.
* Concern: A focusable heading is not a focus-entry policy. Keyboard activation
  needs a defined route into the summary and its Open home action, particularly
  when the expanded sidebar precedes map markers in DOM order. Filtering,
  clustering or failure can remove the focused card/marker, making the promised
  current-marker return impossible.
* Impact: An implementation could satisfy visible card and Escape assertions
  while leaving focus on a removed element, resetting it to the document, or
  requiring an unintuitive traversal to reach the new summary.
* Smallest useful change: Specify the initial dialog target and the keyboard
  marker-to-summary focus transition. Define a connected, visible, in-surface
  fallback when the selected marker no longer exists, and preserve focus when an
  ordinary redraw does not invalidate its target. Keep the existing marker-ID
  return and second-Escape-to-toggle behavior.
* Action owner: Planning parent.
* Exact resolving evidence: P01 details name the entry and fallback targets and
  activation/redraw conditions. The existing planned browser script asserts
  keyboard activation reaches the summary/Open home without pointer input,
  same-ID redraw preserves or restores the intended target, and selection
  removal/failure leaves focus on the named connected target inside the dialog
  when expanded. Extend assertions within the locked file/contract budget.
* Decision route: Direct planner correction. Choosing deterministic focus
  mechanics within the requested interaction is not a divergent product decision.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Commit email must be derived from the authenticated identity

* Related IDs: P03-T02.
* Evidence:
  .copilot-tracking/details/2026-10-28/map-fullscreen-532-phase-details.md:57-59
  requires gh api user but then specifies a fixed numeric-ID/login email.
  Repository instructions require deriving both components from that response.
* Concern: The lookup does not control the configured email. A different
  authenticated account would still be committed under the fixed identity.
* Impact: Local author/committer attribution can be incorrect despite a successful
  identity lookup.
* Smallest useful change: Replace the fixed address with the runtime-derived
  {id}+{login}@users.noreply.github.com formula; configure repository-local email
  and use it for both author and committer. Keep the Conventional Commit and
  Copilot-trailer requirements.
* Action owner: Planning parent.
* Exact resolving evidence: P03-T02 contains no fixed account/email and explicitly
  derives the address from the returned id and login before local commits.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Coordinator handoff omits the exact-head publication sequence

* Related IDs: P03-T01-T03, AC6, publication follow-up.
* Evidence:
  .copilot-tracking/details/2026-10-28/map-fullscreen-532-phase-details.md:53-65
  puts Review before local commits and hands publication to the coordinator.
  .copilot-tracking/plans/2026-10-28/map-fullscreen-532-plan.md:123-125
  retains full-gate and hosted requirements, but does not assign receipt
  verification and independent exact-head assessment.
  src/README.md:150-159 requires an external receipt, current-main verification
  immediately before independent exact-head review and push, and invalidation
  after candidate/base/environment changes.
* Concern: The single earlier implementation Review is not automatically an
  assessment of the subsequently committed, fully gated exact head. The handoff
  correctly blocks an Azure-dependent gate but lacks the explicit resume sequence
  required before any later coordinator push.
* Impact: A local commit plus historical Review could be mistaken for publication
  readiness after the coordinator clears prerequisites.
* Smallest useful change: Assign the coordinator an explicit blocked-publication
  checklist: preserve the original Review; commit the final source and dated
  evidence; run the required complete local gate only when all commands and
  filesystem prerequisites are permitted; retain a new external receipt; fetch
  main and verify the receipt against current origin/main immediately before
  independent exact-head assessment and push. Any later candidate/base/input
  change invalidates that gate. Never invoke az or push while blocked.
* Action owner: Planning parent defines the handoff; coordinator executes it.
* Exact resolving evidence: P03-T03 records that sequence, its owner and blocked
  prerequisites, distinguishes the original one-time RPI Review from publication
  exact-head assessment, and leaves publication unmet until both evidence stages
  exist. Preserve the parent PR base and Refs #532 wording.
* Decision route: Direct planner correction applying existing publication rules;
  no new user decision, second plan critique or repeated original Review required.

## Strengths and Residual Risk

* Moving the existing map avoids a second Leaflet instance and preserves its
  viewport; native modal semantics avoid an unnecessary custom focus trap.
* Summary fields stay within the existing map payload and coordinator omissions.
  Manual direct links, non-colour symbols and motion suppression remain explicit.
* Real DOM tests cover behavior rather than claiming static contracts prove
  keyboard or geometry acceptance. The test budget can accommodate the requested
  corrections without additional files.
* Research records the source-retrieval recovery and alternatives. No additional
  research or framework decision is necessary for this bounded plan.
* Human assistive-technology and real-staff acceptance, hosted checks and full
  publication evidence remain unmet outside this critique. Known Azure/full-gate
  limitations are not an implementation failure or permission to bypass gates.

## Questions or Blocking Evidence Gaps

* No unresolved user product choice or decision-critical research gap.
* Shared-lock availability and full-gate prerequisites remain execution blockers
  if they cannot be satisfied within current restrictions. Record them honestly;
  do not infer successful validation from plan completeness.

## Limitations

* This is one plan assessment, not an implementation review, live browser result,
  security audit, fresh remote PR-lifecycle check or accessibility certification.
* External research findings are assessed as supplied; no external source was
  re-fetched. Relevant source reads only resolved concrete planning risks.
* No heavy checks, Azure commands, dependency installation or private-data access
  were performed. Only this critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent, with coordinator for shared-lock availability.
* Smallest next action: Correct P02-T03's prohibited paths and explicitly record
  any shared-lock blocker, then resolve PC-002 through PC-004 in the same planner
  revision. Preserve this original Revise verdict and disposition each finding.
* User response required: No. All four findings are planner-owned corrections.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/map-fullscreen-532-plan.md](.copilot-tracking/plans/2026-10-28/map-fullscreen-532-plan.md) | Assessed final candidate |
| [.copilot-tracking/details/2026-10-28/map-fullscreen-532-phase-details.md](.copilot-tracking/details/2026-10-28/map-fullscreen-532-phase-details.md) | Assessed task details |
| [.copilot-tracking/research/2026-10-28/map-fullscreen-532-research.md](.copilot-tracking/research/2026-10-28/map-fullscreen-532-research.md) | Canonical supplied research |
| [.copilot-tracking/plans/2026-10-28/map-fullscreen-532-critique.md](.copilot-tracking/plans/2026-10-28/map-fullscreen-532-critique.md) | Complete critique, Revise verdict |

## Next Steps

The active planning parent should resolve PC-001 through PC-004 and finalize the
plan without another critique. No user action is required. This reviewer stops
here; implementation, checks, commits and publication are not part of this task.
