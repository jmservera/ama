<!-- markdownlint-disable-file -->
# RPI Phase Details: Design traceability and review gate

## Metadata

* Task ID: 156
* Task slug: issue-156-design-traceability-gate
* Date: 2026-10-18
* Related plan: .copilot-tracking/plans/2026-10-18/issue-156-design-traceability-gate-plan.md
* Research: .copilot-tracking/research/2026-10-18/issue-156-design-traceability-gate-research.md
* Initial direction: existing profile synthesis, finite inventory, no UI changes.
* Initial readiness: evidence sufficient; single independent critique later Pass.
* Current state: P01/P02 complete; original Review Complete / Conformant,
  preserved unchanged. Integration publication complete at
  4a1542b8ee9506aea2bcb92042efdf7b35155ab5; metadata-only correction ONE
  reconciles current handoffs. External final-head gate pending; no new Review.
* Current integration base: 3bc46912684cb4d865572023a6d16da14b9b8463.
* Documentation source baseline remains 3104bb69ddc26c81e0e9d2f57000dac1d99a419a.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Curate evidence and gate | Complete | P01-T01, P01-T02 |
| P02 | Validate and reconcile | Complete | P02-T01 |

## Coordinator integration boundary (2026-10-18)

Same task/session/PR400; no feature/correction scope. Rebase authorized from old
published 6af9dd81e0089f8998bb8d575329c6bc1d4fc110 onto exact current integration
base above. Replayed head before receipt commit:
23b2d8758cbcceedf251d6c87c79f2a01e44d9a8. Integration publication completed at
4a1542b8ee9506aea2bcb92042efdf7b35155ab5. Rebase/lease instructions are
historical, already executed. PR400 reports the exact latest publication head,
including metadata-only correction ONE, not a new reviewed candidate.

One append-only log conflict resolved with upstream #172 entry followed by the
unchanged #156 entry; index auto-merge retains both routes. Validate all thirteen
upstream files: eleven exact bytes plus exact additive index/log composition.
Own synthesis and frozen assessment bytes must match old published head; source
pins do not become the integration base. Documentation checker is rerun using
an explicit base argument, preserving link/anchor/table/pin checks rather than
testing an empty worktree diff. Actual receipts are in changes. No runtime or
human evidence is produced. Independent integrated-head acceptance remains open.

Correction ONE (2026-10-18): coordinator supplied independent reviewer
8c47ce3f's single Medium stale-publication metadata finding. Reconcile
plan/details/changes/state only. Preserve all delivery documents and original
critique/Review bytes. Publication itself is complete; current remaining action
is external final-head acceptance. Normal push only, no rebase/force-push,
replacement Review or claim of independent closure.

<!-- rpi:phase id=P01 -->
## P01: Curate existing evidence and gate

Context: C1 already contains profile/task routes, source review, owner-reported
feedback and later IA engineering. Do not create a parallel library. Intent:
make links and missing evidence reviewable. Boundaries: production edits only
to profile synthesis, KB index/log. Dependency: research and critique gate.
Completion: finite register, decision log and actual blocked review record.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add finite trace and decision registers

* Context/evidence: C1/C2 eleven proposed profiles; C3 lifecycle and evidence
  trace; C4 partial Fluent foundation versus W2 live owner choice/closed issue.
* Intent: fifteen explicit rows, IDs T01-T11 and C01-C04, with role and
  feature links (#226, #230, #231, #232, #227, #228, #225, #229; shared #152).
* Existing task flows: link exact PRD Profile Journey Contract and matching row,
  local All Eleven Profile Journeys matching row, lifecycle/return section,
  UX-02/03/05/06/07 or shared IA section as appropriate. These are existing
  flow descriptions, not newly fabricated screen drawings.
* Journey evidence: use exact atlas/role journey section anchors, explicitly
  research hypotheses. Related profile grouping is an author mapping.
* Historical artifact H: tracked 2026-10-06 HTML at immutable
  c0f7c08aec514597af86528caf1bdad4b7250246. Current baseline artifact E:
  src/api/checks/workbench-manifest.json pinned at 3104bb69, engineering-only.
* Each row states historical/source-only, current design `Not supplied`,
  requirement/check, missing item, responsible role and concrete next action.
  Unknown design/user acceptance must not be inferred from source coverage.
* Decision register: Fluent 2 actual owner choice with date/URL; owner-reported
  context/recovery plus derived proposal separated; sequencing is sourced
  synthesis, not an owner-approved release plan; IA trade-off is engineering.
* Validation: row count and all columns, exact links/anchors and pins; original
  scope text remains intact. No private data, source/runtime or prototype edits.
* Unresolved: complete backlog coverage/current accepted designs remain open.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Record gate and KB navigation

* Depends on P01-T01 stable row inventory.
* Expected review fields: candidate baseline/exact artifact versions, reviewer
  identity/type and review date, expected versus actual for every gate,
  outcome and finding ID/affected row/owner role/next action.
* Actual initial review is an AI documentation evidence inspection, not a
  named human design review. Record human reviewer/date as Not supplied.
* Checklist: complete trace and exact design; default/focus/disabled/error/
  loading/empty/blocked states; safe recovery, minimum-necessary permissions,
  human/resident boundaries; linked WCAG baseline including manual evidence;
  content standard and named exact resident-text review; direct user research.
* Missing required evidence cannot produce overall Pass. Report documentation
  completeness, historical engineering, human design and user research
  separately. Human/user checks stay unchecked; no conformance assertion.
* Link existing WCAG/content sections without weakening their proposed target,
  manual requirements or named resident-wording review.
* Update synthesis ms.date, existing KB row description/date, append log entry
  without rewriting history. No new competing page.
* Completion evidence: diff, checklist and actual blocked record.

<!-- rpi:phase id=P02 -->
## P02: Validate and hand off original candidate

Context: no repository-wide docs lint/build exists. Intent: check exact changed
documentation and preserve independent Review boundary. Dependency: P01.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Check documentation and reconcile evidence

* Parent checks git diff --check, table cell counts, heading sequence, link
  destinations and GitHub-style anchors for every added/edited Markdown link.
  Verify pinned public artifact links through Git object existence and exact
  path/version; compare representative source contents/sections independently
  of row wording. No dependency install or external page crawl needed.
* Review diff for ASCII, plain wording, immutable historical text and append-only
  log; record exact commands/results and unperformed checks in changes.
* Lock test ownership/removals/additions as plan; no repository tests added or
  removed, no generated runtime targets. Session-local standard-library checker
  permitted; no tooling committed outside evidence.
* Reconcile plan markers/details/changes before original Review. Original
  independent Review writes only its assigned artifact and does not fix.
* Accepted bounded documentation Review is not overall design Pass, #156
  acceptance, owner/human approval or CI success. Not accepted means freeze,
  commit locally, no PR; coordinator owns correction routing.
* Completion evidence: changes record receipts and one original Review.
