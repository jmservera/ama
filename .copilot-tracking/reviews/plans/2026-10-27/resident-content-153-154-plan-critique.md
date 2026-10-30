---
title: Resident content and journey final-candidate plan critique
description: Independent bounded plan assessment for sibling issues 153 and 154
ms.date: 2026-10-27
---

## Metadata

* Task ID: issues-153-154
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/resident-content-153-154-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/resident-content-153-154-phase-details.md
* Research: .copilot-tracking/research/2026-10-27/resident-content-153-154-research.md
* Critique execution status: Complete
* Assessment count: One final-candidate critique; no implementation or human acceptance performed.

## Inputs and Criterion Boundary

* Assessed the supplied plan, phase details and research against the current
  #153/#154 bodies and comments, retrieved read-only using gh during this
  critique. Confirmed the #153 owner comment appoints Juan Manuel Servera;
  neither appointment nor current issue status establishes completed review.
* Read the repository knowledge-base index, owner memory, original case study,
  addendum, housing-association primer, content standard, resident journeys and
  WCAG baseline. Checked linked BRD FR-045/046, NFR-008/009, OD-41/42 and PRD
  SA-003/004, FR-045/046/048/049 and their acceptance rows.
* Inspected the existing content regression, the four proposed JavaScript
  targets, core representative authority date logic, available API browser
  scripts, relevant browser coverage and resident API fixture setup.
* Confirmed the supplied topic branch is docs/resident-ux-153. Existing
  untracked planning/research/state artifacts were observed and left unchanged.
* The authorized increment is one sibling PR: audited existing UX documents,
  index/log and the smallest safe existing-web copy fixes. No test removals,
  at most four added methods in the existing content test, four named
  JavaScript targets, no dependencies or generated source targets.
* Local-only validation is explicit direction: no --all, and this small plan
  skips --changed. No Azure, secrets, .env, private datasets, uv or live contact.
  The local-only direction is not itself a finding.
* Assessed planning credibility and bounded engineering verification only.
  Actual wording review, resident/representative usability, assistive-technology
  acceptance, hosted checks and operational privacy/service approvals are not
  supplied results and cannot be established by this critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| #153 standard, vocabulary and error coverage; C1-C3 | Covered for bounded delivery | P01-T01 requires a dated inventory, exact residual references and follow-up roles, rather than a universal lexical/error pass. |
| #153 AI and reviewed-draft authority; C13; SA-004 | Covered in design | P02-T01 preserves exact AI wording and adds draft-only/no-send and human-review boundaries; rendered coverage needs PC-002. |
| #153 named human review; W1 | Covered as incomplete acceptance | Corrects stale appointment status without inventing review of exact text or permission for live use. |
| #154 six resident tasks; C7-C10; P01-T02 | Covered for design | Choice, pause/withdrawal, appointments, updates, handover/aftercare and challenge/remedy get candidate text, receipt, owner, negative state and offline route. |
| #154 accessibility and non-digital alternatives; C12 | Covered as proposed design | Support preferences are chosen, not inferred incapacity; human usability/AT scripts remain Not run. Issue criteria matrix must retain language, literacy and adjustment needs explicitly. |
| #154 representative restrictions; C4-C5; AC-087/AC-064 | Covered | Task/scope/date allowlist, revocation, interpreter-only, several representatives and changed unsafe contact are planned. Core authority uses an exclusive review-date boundary. |
| #154 offers versus commitments; C6; AC-088/AC-062 | Covered | Distinct offer/response/confirmation and authority boundaries are explicit, without sending or works-consent inference. |
| OD-41/42; W3-W4; AC4 | Covered as unresolved | Human research and operational representative/privacy decisions remain with their actual owners. Refs, not Closes, is appropriate. |
| Four-file literal changes; locked tests | Covered | No semantic/backend/CSS/framework or stored-value changes; <=4 added content-test methods and no removals. |
| AC5; P02-T01/T02 | Partial | PC-002: browser target and changed-render-path evidence are not yet executable as specified. |
| P03-T01; independent Review and publication | Partial | PC-001: adverse Review and blocked-validation publication dispositions are not explicit. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.
* Rationale: The bounded scope, authority safeguards and honest incomplete
  acceptance are credible. Two direct planner corrections are needed before
  implementation handoff: a fail-closed publication transition and a concrete
  validation/coverage mapping. Neither requires widening scope, another
  critique or a significant user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Publication lacks an explicit adverse-Review stop condition

* Related IDs: P03-T01, AC5, ordered RPI requirement.
* Evidence: .copilot-tracking/plans/2026-10-27/resident-content-153-154-plan.md,
  P03-T01, says to retain the independent Review outcome and route findings
  rather than another implementation/review loop, followed by commit/push/PR.
  .copilot-tracking/details/2026-10-27/resident-content-153-154-phase-details.md,
  P03-T01, likewise says to preserve findings and route later work without
  re-review, then publish. P03 depends on validation being complete, but AC5
  permits explicit blocked results; neither source defines which outcomes
  prevent publication.
* Concern: The single-Review limit and local-only exception are clear, but
  there is no explicit branch for a Not accepted/Blocked Review or a missing
  required engineering check. An implementer could interpret recording and
  routing findings as sufficient to proceed to publication.
* Impact: A candidate with an authority/copy regression or unverified required
  check could be pushed and presented as ready despite adverse independent
  evidence. The owner-approved validation limit does not approve ignoring an
  adverse result.
* Smallest useful change: Add an explicit P03 transition: publish only after
  the independent Review accepts the unchanged reviewed source boundary and
  required local engineering checks pass. On an adverse/blocked result,
  preserve evidence and stop publication; return the issue to the parent
  without silently repairing and publishing an unreviewed candidate or
  automatically starting another Review. Keep the separately planned human
  wording/usability/AT steps Not run; those are not newly required engineering
  checks or implied whole-issue acceptance.
* Action owner: Planning parent.
* Exact resolving evidence: Matching plan and phase-details completion rules
  explicitly identify publish versus stop outcomes, required local-check
  disposition and reviewed-source boundary. Later changes evidence records
  the actual independent outcome without changing the original Review.
* Decision route: Direct planner correction. No user response is needed to
  make publication fail closed; any later request to continue after an adverse
  Review is outside this critique.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Resolve browser checks and copy-path coverage before handoff

* Related IDs: AC5, P02-T01, P02-T02, C2/C4/C13.
* Evidence: The plan's locked validation boundary names
  design_system_browser_check and resident_commitments_browser_check, with an
  inspect-and-substitute fallback. The latter is not present under
  src/api/checks. The existing
  src/api/checks/design_system_browser_check.py exercises workbench/map,
  viewport, non-colour and reduced-motion behavior, but does not assert the
  proposed draft heading/disclaimer, representative review-date copy,
  assistant review disclaimer or timecapture wording.
  src/api/checks/assistants_browser_check.py does exercise proposal rendering,
  source verification and acceptance, but is not selected in the plan.
  Phase details require actual browser evidence for changed render paths
  where fixtures support them while prohibiting new test files and limiting
  added methods to test_content_standard.py.
* Concern: The plan defers the actual browser selection and does not map
  existing checks, bounded manual browser inspection or string regressions to
  the four changed surfaces. Passing the design-system browser check cannot
  establish that the new copy renders in those paths. The current wording
  also leaves unclear how to meet the stronger phase-detail completion rule
  without exceeding the locked test/source targets.
* Impact: Implementation may either overclaim rendered-copy evidence, expand
  test files outside the agreed boundary or reach Review without a reproducible
  account of what was actually checked.
* Smallest useful change: Select existing browser modules and the targeted
  unit selector now, with working directory and fixture invocation. Map each
  changed surface to existing automated coverage, bounded manual browser
  inspection using existing synthetic fixtures, or an explicitly unperformed
  rendered check. Use <=4 new methods only in the existing content test for
  literal assertions; do not modify browser check sources or add dependencies.
  Keep unavailable engineering prerequisites explicitly blocked, following
  PC-001 rather than counting a generic browser pass as copy coverage.
  Configure any required scratch/browser profile paths under the worktree
  before launch: the existing resident API test uses default
  tempfile.TemporaryDirectory(), so invocation must not default to /tmp.
* Action owner: Planning parent, with execution evidence owned by the API
  implementation parent.
* Exact resolving evidence: The plan/details contain real module names,
  exact local invocations, repository-local scratch configuration and a
  four-surface coverage table separating source assertions from rendered
  inspection. Subsequent changes evidence records commands, counts,
  exercised states and blocked/unperformed checks, without changing the
  locked source/test boundary.
* Decision route: Direct planner correction. No significant user decision,
  heavy gate, new dependency or additional critique is required.

## Strengths and Residual Risk

* The six task contracts are appropriately distinct from staff role screens
  and from the later optional-portal proposal. No portal implementation is
  smuggled into #154.
* The representative label correction follows actual exclusive date logic,
  rather than inventing a new expiry policy. Scheduling, interpreting,
  disclosure and works-decision authority remain distinct.
* Dynamic server errors, evidence quotations and stored finance values remain
  visible audit residuals, not falsely certified by a lexical guard.
* Appointment, complaint response, remedy, handover and financial closure are
  separate design states; offers and recorded responses do not imply confirmed
  commitments.
* The plan preserves Fluent 2, native semantics, non-colour signals and reduced
  motion, optional assistance/manual routes and human/resident decisions.
* Existing incomplete WCAG, comprehension, wording and resident/representative
  validation remain disclosed. Juan Manuel Servera's appointment is confirmed;
  actual review of exact text still needs its own record.
* The bounded delivery intentionally leaves both issues partial. Broader
  reason/owner/action coverage and OD-41/42 operational decisions are follow-up
  work, not blockers to authoring synthetic candidate designs.

## Questions or Blocking Evidence Gaps

* No decision-critical user question is required for these corrections.
* No missing evidence prevents this planning verdict. Actual future
  engineering results and human acceptance are not asserted.

## Limitations

* This was a read-only evidence assessment except for this critique artifact.
  No tests, browser sessions, live contacts, implementation edits, commits,
  branch changes, pushes or other agents were invoked.
* Linked evidence was inspected only as needed for this bounded plan. This
  is not an exhaustive code audit, a fresh web-interface-guidelines review of
  changed implementation, a legal/current-regulatory assessment or a WCAG
  conformance finding. Guidelines must still be fetched before web edits and
  refreshed for the planned independent Review.
* Only the supplied candidate was assessed, once. Findings are the complete
  actionable set identified within this boundary, not a request for serial
  critique passes.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the fail-closed Review/publication disposition,
  resolve PC-002's local-check and surface mapping, and record both critique
  dispositions directly in the existing plan/details.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/resident-content-153-154-plan.md](.copilot-tracking/plans/2026-10-27/resident-content-153-154-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-27/resident-content-153-154-phase-details.md](.copilot-tracking/details/2026-10-27/resident-content-153-154-phase-details.md) | Assessed task boundaries and completion rules. |
| [.copilot-tracking/research/2026-10-27/resident-content-153-154-research.md](.copilot-tracking/research/2026-10-27/resident-content-153-154-research.md) | Supplied evidence and readiness assessment. |
| [.copilot-tracking/reviews/plans/2026-10-27/resident-content-153-154-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/resident-content-153-154-plan-critique.md) | This single independent critique. |

## Next Steps

The active planning parent should correct PC-001 and PC-002 and finalize the
plan with their dispositions, without another plan critique. No user action is
required. This critique stops here; it does not implement, publish or accept
the candidate on behalf of residents or the owner.
