---
title: Case journey 526 open threads plan critique
description: One independent final-candidate assessment for the five further PR 529 threads
ms.date: 2026-10-28
---

## Metadata

* Task ID: 526-pr529-open-threads-20261028.
* Critique date: 2026-10-28.
* Plan: .copilot-tracking/plans/2026-10-28/case-journey-526-open-threads-plan.md.
* Phase details: .copilot-tracking/details/2026-10-28/case-journey-526-open-threads-phase-details.md.
* Critique execution status: Complete.
* Execution boundary: exactly one independent final-candidate critique; no
  implementation, validation execution, additional agents or remote writes.

## Inputs and Criterion Boundary

* Caller requirements: five further Copilot threads on PR #529, issue #526,
  continuing feat/case-journey-ux-526; shared live/pending dirty protection,
  isolated route tests, immutable submitted document values and record-bound
  later-edit recovery, disabled completed review actions, exact 38-scan receipt
  fixtures, and query-preserving native journey anchors synchronized after
  in-place challenge pagination. Existing stepper semantics must remain.
* Research: .copilot-tracking/research/2026-10-28/case-journey-526-open-threads-research.md,
  including C1-C7, W1-W2 and the five recorded thread IDs.
* Source evidence: the supplied app.js route, aiNotes, caseView,
  rememberCaseFields, recovery, documentsPanel, fundingPanel and beforeunload
  paths; case-workspace.js enhance/select; panels.js affectedChallengePanel
  historyFor; their owning workspace/journey tests; the journey browser harness;
  tools/rpi-checks.py verification and tools/test_rpi_checks.py receipt fixtures.
* Context: original case study, relevant addendum/index context, owner memory,
  and existing API validation instructions. Memory was not treated as evidence.
* Decisions: API units, tool units and journey axe are mandatory; nonblocking
  flock admission has a maximum 40-minute retry; no Azure, az, .env or secret
  access. The active execution constraints also forbid /tmp and /var/tmp file
  operations. Full-gate blockage prevents publication, not an authorized local
  commit. Test ownership, no removals, at most eight added unit methods and no
  additional browser scans are locked.
* Assessment covers credibility of the supplied plan and details, not
  implementation correctness, fresh hosted-thread status, accessibility
  conformance or publication eligibility. No open-ended research was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1/C5, P01-T01: shared dirty protection | Covered | Reconciliation precedes pending/DOM checks; both route and unload share it; tab-only fast path remains first. |
| C2, P01-T01: route harness isolation | Covered | Shared predicate stays inside extracted source; case/funding globals, URLSearchParams and guard dependencies are supplied; pending, clean and tab paths are required. |
| C3, P01-T02: document dispatch race | Covered | Immutable dispatch values, unchanged-only clearing, read-only copyable later values, reviewed-record identity, refresh survival and dirty warnings are explicit. |
| P01-T02: completed actions and sibling paths | Covered | Completed actions cannot issue another review; submitted replacement remains visible; resident/funding callers, proposals, replacement and recovery cleanup are inspected. |
| C4/C6, P01-T03: journey destinations | Covered | Only tab is replaced; synchronization occurs at selection/render and in-place pagination; real pagination, dirty drafts and back/forward are exercised. |
| C7, P01-T03: exact receipt contract | Covered | Verifier and fixture change together; research specifies acceptance of 38, rejection of 37/39 and serious violations; no new scans. |
| Stepper and native interaction preservation | Covered | Names, states, routing targets, native anchors, focus behavior and existing semantic tests are retained. |
| Locked test ownership/removals/maximum | Covered | Existing owning files, zero removals, eight-method maximum and bounded real-browser assertions are explicit. |
| P02-T01: API/tool/journey validation | Partial | Required suites, pinned axe, 38 scans, keyboard/zoom, Ruff and JS parse are named; filesystem/admission instructions conflict with execution constraints, PC-001. |
| P02-T02: Review and acceptance | Partial | Independent Review and preserved adverse evidence are required, but blanket finding deferral lacks an in-scope acceptance stop, PC-002. |
| P02-T02: local commit/publication boundary | Covered | No az-dependent full gate, no claimed publication pass, no remote replies/resolution before eligible publication; local commit remains authorized. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.
* Rationale: the five functional corrections have credible source-grounded
  coverage within the locked test budget. Two execution instructions need direct
  correction before implementation: prohibited filesystem operations and
  unconditional deferral of post-implementation Review findings.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Validation admission and scratch paths violate the active filesystem boundary

* Related IDs: P02-T01; mandatory API/tool/journey checks; nonblocking shared lock.
* Evidence: .copilot-tracking/details/2026-10-28/case-journey-526-open-threads-phase-details.md,
  P02-T01 explicitly selects /tmp/ama-rpi-heavy.lock. Active execution
  instructions prohibit all /tmp and /var/tmp file operations. In addition,
  tools/test_rpi_checks.py:48 uses TemporaryDirectory without an explicit
  directory, and src/api/checks/case_journey_browser_check.py:865 does the same
  for browser zoom. The phase gives no allowed scratch override.
* Concern: the literal lock instruction cannot be executed. Merely relocating
  logs does not prevent the required checks and browser runtime from allocating
  prohibited scratch. A private replacement lock would also fail to coordinate
  with other heavy runners using a different lock inode.
* Impact: mandatory validation can be blocked or violate execution constraints;
  an uncoordinated replacement could permit concurrent heavy checks.
* Smallest useful change: revise the validation recipe to use an allowed,
  genuinely shared admission mechanism, retaining flock -n, the absolute
  2400-second deadline and bounded retries. Do not silently substitute a
  per-worktree lock. Route child-process scratch/profile/cache allocations to
  explicitly owned allowed paths through a sanitized command environment.
  Distinguish retained evidence from disposable scratch and obey the active
  relative-path creation constraint. If shared admission cannot be obtained
  within these constraints, mark heavy validation Blocked rather than use /tmp
  or run unlocked. Do not change repository-wide lock policy in this correction.
* Action owner: planning parent, with execution coordinator for shared admission.
* Exact resolving evidence: revised P02-T01 identifies the permitted shared
  lock identity or records its blocker; lists the scratch-routing environment
  and allowed destinations for Python/Chromium child processes; preserves the
  <=2400-second nonblocking retry bound, owned cleanup and separate attempt logs.
  Later execution evidence must show actual admission and permitted paths,
  not merely claim an equivalent private lock.
* Decision route: Direct planner correction. The filesystem prohibition is
  already settled; no user permission to bypass it is requested.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Blanket Review-finding deferral omits an in-scope acceptance stop

* Related IDs: P02-T02; five-thread completion; acceptance criteria.
* Evidence: .copilot-tracking/details/2026-10-28/case-journey-526-open-threads-phase-details.md,
  P02-T02 ends with "Do not repeat Review or rewrite historical failures; route
  findings as later work." The plan requires all five corrections and passing
  regressions but does not state how an adverse independent Review affects
  completion of this local candidate.
* Concern: this instruction treats an unrelated follow-up and a finding that
  invalidates one of the five fixes alike. It permits an unresolved in-scope
  defect to be deferred without an explicit Not accepted or Blocked handoff.
  Preserving the original outcome and avoiding repeated Review do not require
  treating actionable in-scope failures as completed delivery.
* Impact: the coordinator could receive a local commit described as complete
  despite unmet functional acceptance, independently of the already accepted
  Azure/publication blocker.
* Smallest useful change: distinguish out-of-scope follow-ups from in-scope
  findings. Require unresolved in-scope findings or failed mandatory checks to
  block acceptance and be named in the handoff. Preserve the one independent
  Review and its original outcome; do not imply that a later correction or
  passing rerun retroactively changes that outcome. A local evidence/checkpoint
  commit remains permitted without claiming acceptance.
* Action owner: planning parent.
* Exact resolving evidence: revised P02-T02 and acceptance wording explicitly
  require no unresolved in-scope Review findings for an accepted local
  candidate, identify the Not accepted/Blocked route otherwise, and reserve
  later-work deferral for out-of-scope findings. They retain the original
  Review record, authorized local commit and publication prohibition.
* Decision route: Direct planner correction. Current user direction already
  requires the five defects to be corrected; no divergent scope decision is
  necessary.

## Strengths and Residual Risk

* Shared reconciliation reuses the existing pendingFields cache instead of
  introducing a competing draft store.
* Later edits are deliberately distinguished from submitted values; an
  input-lock-only workaround is correctly rejected.
* The pagination hook addresses the actual replaceState path, not just initial
  href construction. Native anchors and stepper semantics remain explicit.
* The receipt correction preserves exact counts, pinned workflow bytes and
  adverse fixture coverage without expanding the scan budget.
* The accepted full-gate Azure blocker remains a publication blocker. Scoped
  local checks cannot substitute for a fresh complete exact-head receipt,
  independent approval, hosted checks or human acceptance.

## Questions or Blocking Evidence Gaps

* No unresolved user decision is necessary for the two planner corrections.
* A compatible shared admission path must be established before heavy checks;
  inability to establish it blocks those checks, not this critique.

## Limitations

* Source and test inspection were read-only. No API units, tool units, browser,
  axe, formatter, lock attempt or full gate was executed.
* Thread identities/status and W2 guideline retrieval are the supplied research
  observations, not freshly fetched evidence from this critique.
* Intake showed the expected topic branch and four existing untracked planning/
  state inputs. Those inputs were neither moved nor edited.
* This is the complete actionable finding set from this single supplied-boundary
  assessment; no additional critique pass or agent was launched.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: correct P02-T01 admission/scratch handling and P02-T02
  acceptance disposition directly, preserving the original supplied artifacts'
  historical outcomes and this critique.
* User response required: No.

## Next Steps

The active planning parent should resolve PC-001 and PC-002 directly and finalize
the candidate without another critique. This critic stops here; no implementation
or publication is authorized by the critique, and no user action is required.
