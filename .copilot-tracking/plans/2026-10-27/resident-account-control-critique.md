---
title: Resident account control final-candidate plan critique
ms.date: 2026-10-27
---

## Metadata

* Task ID: #467; parent #466.
* Critique date: 2026-10-27.
* Plan: .copilot-tracking/plans/2026-10-27/resident-account-control-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/resident-account-control-phase-details.md
* Critique execution status: Complete.
* Assessment: exactly one independent final-candidate critique; no nested agents.

## Inputs and Criterion Boundary

* Caller requirements: employee-pattern native details/summary at the resident
  header's right edge; own authenticated email only after the existing view
  authority check; existing logout behavior unchanged.
* Research: .copilot-tracking/research/2026-10-27/resident-account-control-research.md,
  including C1-C5 and the recorded W1 retrieval.
* Decisions: focused unit/static/browser validation replaces the full local
  gate for this task. No Azure, SQL access, private datasets, secrets, environment
  files, verifier access or MAX_MAPPINGS change. Publication is a stacked PR
  targeting feat/resident-interactive, with Refs only and no merge.
* Acceptance boundary: account identity/isolation, native disclosure semantics,
  dismissal, focus and logout recovery, restored sessions, long-email reflow,
  test ownership/coverage lock, independent Review and bounded publication.
* Source inspected as needed: resident app, markup, styles and script; resident
  API tests; employee account markup/handlers; existing SQL browser harness
  boundary; safe core showcase test imports and SQL-test boundary; component
  validation guidance. Project context was consulted. No implementation,
  test execution, environment inspection or operational access was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Native account pattern; C1-C2; P01-T01 | Covered | Visible Account summary, native details, existing Sign out button, no custom menu role or framework change. |
| Own authenticated identity; C3; P01-T01 | Covered | Add only account.email after token verification and current-row authorisation in ResidentDemo.view_for; session/login contracts remain unchanged; textContent rendering and hidden-state identity reset are specified. |
| Privacy and authority regressions; C4; P01-T02 | Covered | Preserve other-email/private-ID exclusions; two sessions, forged/expired/revoked sessions and denial coverage are required. Existing HTTP tests exercise authority changes, replay and isolation. |
| Existing logout; P01-T01/P01-T02 | Covered | Keep endpoint/handler behavior and honest failure recovery; success announcement, sign-in heading focus and revocation are explicit acceptance criteria. |
| Reflow/focus; W1; P01-T01/P01-T02 | Covered | Bounded right-anchored panel, wrapping, long email, 320/390/1280px, native Enter/Space, Tab to logout, Escape-to-summary and outside dismissal are specified across the inputs. |
| Test ownership and coverage lock; P01-T02/P01-T03 | Partial | API ownership, unchanged core, no removals and addition ceilings are explicit, but the exact safe selector and runnable new browser target are not locked; PC-001. |
| Documentation and evidence; P01-T03 | Covered | Directly related API README and dated exact command/results evidence, with limitations, are required. |
| Independent Review; P02-T01 | Covered | Fresh reviewer, one review, preserved verdict, refreshed web rules and file:line findings. |
| Publication/dependency; P02-T02 | Covered | Explicit stacked base, Refs #467/Refs #466, normal push, account-derived noreply identity, no merge; hosted and human gates remain pending. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* Rationale: the small implementation is credible and the owner has resolved
  the consequential scope decisions. One direct correction is needed to make
  the claimed coverage lock executable without selecting excluded checks.
  No broader design, new research cycle or additional critique is warranted.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Lock the executable validation targets before implementation

* Related IDs: P01-T02, P01-T03; Locked Test Ownership and Validation; C4-C5.
* Evidence: .copilot-tracking/plans/2026-10-27/resident-account-control-plan.md:78-86
  promises focused core resident-showcase tests and one browser check file but
  supplies neither an exact core selector nor the new file path/invocation.
  .copilot-tracking/details/2026-10-27/resident-account-control-phase-details.md:25-38
  lists scenarios and defers command recording until implementation.
  The core test family includes test_resident_showcase.py,
  test_resident_showcase_sql.py and test_resident_showcase_verifier.py; the
  existing src/api/checks/resident_demo_browser_check.py is SQL-backed.
* Concern: the lock constrains counts and broad ownership, but still leaves
  safety-relevant test selection and the runnable browser entry point to the
  implementer. This is an ambiguity, not evidence that an unsafe command has
  been run. A family wildcard or reuse of the existing browser target would
  not satisfy this owner's boundary.
* Impact: validation can drift into excluded SQL/verifier checks, or produce
  evidence for a different harness without demonstrating the promised new
  real-HTTP browser coverage.
* Smallest useful change: add a compact validation ownership/target map to the
  plan or phase details. Name src/api/tests/test_resident_demo_api.py for API
  assertions and the exact existing methods to amend; identify the planned
  additions within the four-method ceiling. Select only
  src/core/tests/test_resident_showcase.py for the extra core check, explicitly
  excluding SQL/verifier siblings. Name the one new no-SQL browser file and
  its command/working directory, assigning the already-listed browser
  scenarios to it. Record the full API discovery command and changed-file
  static-check targets alongside these selectors. Do not expand coverage
  counts, edit core, use the SQL harness or add infrastructure.
* Action owner: planning parent.
* Exact resolving evidence: the final plan/details contain the named paths,
  working directories and runnable selectors, an assertion-to-owner map
  retaining all currently promised scenarios and exclusions, and unchanged
  addition ceilings. An acceptable core selector is
  `python3 -m unittest discover -s tests -p 'test_resident_showcase.py' -q`
  from src/core with the project distribution installed. During implementation,
  dated changes evidence must record those actual commands/results and
  browser assertions; unavailable checks must remain explicitly blocked.
* Decision route: direct planner correction. The owner already chose focused
  validation and excluded operational access; no user decision is required.

## Strengths and Residual Risk

* Server-derived identity is projected only after the existing authority check;
  no client-selected identity, extra persistence or session-endpoint disclosure
  is proposed.
* Scope is appropriately small: move the existing logout control, reuse native
  disclosure semantics and local design tokens, preserve recovery/focus behavior.
* Existing HTTP authority tests remain the owner of session/isolation behavior;
  browser checks complement rather than replace them.
* Focused Chromium checks do not establish screen-reader interoperability,
  formal accessibility acceptance or WCAG conformance. The plan explicitly
  leaves human acceptance outside this change.
* The full local gate is intentionally omitted by current owner direction,
  not a critique blocker. Hosted checks/rubric and human review remain distinct
  pending gates; focused evidence must not be presented as their completion.

## Questions or Blocking Evidence Gaps

* No unresolved user choice or decision-critical research gap.
* PC-001 is the complete actionable finding set for the supplied boundary.

## Limitations

* This is a plan credibility assessment, not an implementation review or a
  passing test/browser result. No new UI-guideline retrieval or fresh complete
  UI conformance review is claimed; W1 is the supplied research record.
* No Azure, SQL, private datasets, secrets, environment files or verifier
  artifacts were accessed. No source, plan, phase details or research was
  changed. Only this critique artifact was written.
* Remote PR lifecycle and hosted checks were not independently verified.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: directly lock the safe validation selectors, browser
  entry point and assertion owners in the existing plan/details, then record
  this critique's disposition.
* User response required: no.
* Stop: this critique is complete. Do not commission another critique for this
  correction; return to the active parent for direct revision and handoff.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/resident-account-control-plan.md](.copilot-tracking/plans/2026-10-27/resident-account-control-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-27/resident-account-control-phase-details.md](.copilot-tracking/details/2026-10-27/resident-account-control-phase-details.md) | Assessed phase details. |
| [.copilot-tracking/research/2026-10-27/resident-account-control-research.md](.copilot-tracking/research/2026-10-27/resident-account-control-research.md) | Supplied evidence and decisions. |
| [.copilot-tracking/plans/2026-10-27/resident-account-control-critique.md](.copilot-tracking/plans/2026-10-27/resident-account-control-critique.md) | Complete independent critique. |

## Next Steps

The active planning parent resolves PC-001 directly and finalizes the bounded
plan before implementation. No user action is required. This reviewer stops
after the critique artifact.
