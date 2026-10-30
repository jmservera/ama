---
title: Progress dashboard 533 final-candidate plan critique
ms.date: 2026-10-28
---

## Metadata

* Task ID: #533, progress-dashboard-533
* Critique date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/progress-dashboard-533-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/progress-dashboard-533-phase-details.md
* Critique execution status: Complete
* Assessment count: One final-candidate critique, with the complete finding set below.

## Inputs and Criterion Boundary

* Caller requirements: full synthetic-only dashboard and status/date/team/text-filtered,
  URL-persisted paged closed archive; native Fluent 2 foundations, no framework swap;
  separate from briefing/map; existing staff permissions; unit/browser/axe evidence;
  no Azure, az, private datasets, .env or secrets. Scratch operations must not use
  /tmp or other temporary directories.
* Supplied research: .copilot-tracking/research/2026-10-28/progress-dashboard-533-research.md.
* Read the supplied plan and phase details in full and the issue #533 body through
  its supplied W1 pointer. Read original case study, relevant addendum/index context
  and owner memory. Inspected only cited lifecycle, recommendation, case-summary,
  queue, navigation/router and data-dictionary seams necessary to assess correctness.
* Dependency: feat/progress-dashboard-533 stacked on feat/case-journey-ux-526,
  PR #529; retain that PR base and "Refs #533". No branch or remote changes made.
* Acceptance boundary: all listed dashboard measures, inclusive date selector,
  chart/table equality, demonstration labels, archive combined filters and paging,
  permissions, cancellation, failure states, browser/unit/axe checks and honest
  publication gates.
* Assessment concerns planning credibility, not implementation acceptance, fresh
  visual/accessibility conformance, source execution or live operational truth.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Dashboard daily/weekly flow, backlog and duration; Q1/Q2; P01-T01 | Partial | Explicit cohorts and missing coverage are sound; imported simulation reopen action is missing from the replay recipe (PC-003). |
| Journey/team workload, stalled and overdue; P01-T01 | Covered | Six existing journey groups, owner_role, explicit current-view labels and existing recorded-deadline semantics. |
| Synthetic-only AI briefing outcomes; C7/C8; P01-T01 | Partial | Case admission does not establish recommendation-level synthetic provenance; AI date cohort is undefined (PC-002, PC-006). |
| Inclusive date range and weekly boundaries; P01-T02 | Covered | Default, maximum span, invalid/duplicate/unknown parameters and boundary tests are assigned; AI exception noted separately. |
| Archive status/date/team/text filters; P01-T01/P02-T01 | Partial | Exact stage is substituted for status without a public mapping; current-closure date and undated membership lack rules (PC-004, PC-005). |
| Archive pagination and URL/history; P01-T02/P02-T02 | Covered | Stable ID sort, reset-on-filter, clamping, empty page and exact/full/beyond boundary tests are explicit. |
| Existing stats/cases permissions and manager archive | Covered | Server permission kinds plus manager check match existing projection/navigation boundaries. |
| Native isolated UI and accessible alternatives; P02 | Covered | Separate modules, semantic forms/tables, numeric bar values, reflow, route cancellation and pinned axe evidence assigned. |
| Synthetic constructed test data and no cloud/private reads; P02-T02/P03-T01 | Partial | Harness isolation is planned, but the explicit environment path violates the execution constraint (PC-001). |
| Unit/browser/regression validation, independent Review; P03 | Covered | Owning checks, immutable adverse outcomes and independent Review are assigned; no check has been executed by this critique. |
| Stacked branch, commits and publication restrictions | Covered | Correct branch/base and non-closing issue reference; no push/PR if the mandatory full gate needs prohibited prerequisites. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 3; Medium 3; Low 0.
* Rationale: The approach is credible and bounded, but the current instructions can
  admit non-synthetic AI activity, miscount imported reopened cases and direct a
  prohibited filesystem operation. Archive and AI cohort definitions also need
  small explicit corrections before implementation.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Validation directs work into a prohibited temporary directory

* Related IDs: P03-T01; execution-environment constraints.
* Evidence: .copilot-tracking/details/2026-10-28/progress-dashboard-533-phase-details.md:44-45
  directs use of /tmp/ama-533-venv. The supplied research also references a /tmp
  lock. Current execution instructions prohibit all temporary-directory file
  operations, not just private dataset reads.
* Concern: The executable phase recipe conflicts with an explicit execution
  boundary. A claimed existing environment does not authorize further access or
  writes there.
* Impact: Following the plan literally cannot produce compliant validation.
* Smallest useful change: Replace the environment/scratch prescription with
  owned project-relative locations. State that prohibited historical paths in
  research are not executable instructions. Resolve a compliant shared-lock
  location through the planning parent; if a permitted common lock cannot be
  used, record heavy validation blocked rather than create an unrelated lock
  and claim shared admission.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P03-T01 gives permitted project-relative
  environment/output paths and an actual compliant shared-admission path or
  explicit blocked condition; subsequent command evidence contains no forbidden
  path operations.
* Decision route: Direct planner correction. No user decision is required to
  obey the supplied constraint; do not delete or relocate an existing environment.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Synthetic cases do not certify linked AI activity as synthetic

* Related IDs: Synthetic-only requirement; Q1; C7/C8; P01-T01/P01-T02.
* Evidence: .copilot-tracking/plans/2026-10-28/progress-dashboard-533-plan.md:48-49,63-65
  admits briefing outcomes through linked synthetic case evidence. In
  src/core/src/zava_forward/core/ai_tasks.py:172-183,212-230, records are created
  from actual task/review activity and contain user identity and output fields,
  with no automatic synthetic certification. The warning in
  docs/reference/research/retrofit-synthetic-data/data-dictionary.md:9-12 explicitly
  excludes actual user chat and tenant bindings from synthetic certification.
* Concern: A synthetic case ID is not sufficient provenance for the AI record
  itself. Linking a record to one admitted case also leaves mixed synthetic/
  unmarked case_ids ambiguous. Aggregating activity does not establish that the
  underlying activity is demonstration data.
* Impact: The synthetic-only dashboard could describe real user/model activity
  as fictional demonstration usage, violating its stated data boundary.
* Smallest useful change: Require an explicit, documented recommendation-level
  synthetic provenance contract in addition to admitted linked cases. Require
  every linked case to qualify; exclude empty, mixed and unresolved links unless
  a separately evidenced synthetic contract covers them. Return aggregate
  counts only, never user identities, output text or reviewer reasons. With no
  qualifying records, show unavailable/no recorded synthetic usage and coverage,
  not invented AI usage.
* Action owner: Planning parent, with implementation owned by P01.
* Exact resolving evidence: Plan/details define the record-level gate and
  all-links rule; unit fixtures distinguish explicitly synthetic records from
  unmarked real-activity-shaped records referencing the same synthetic case,
  mixed links and missing links; assertions prove excluded records contribute
  nothing and sensitive fields are absent from the response.
* Decision route: Direct planner correction under the already confirmed
  synthetic-only requirement. Any later request to include actual activity
  would be a significant scope decision, not a prerequisite for this task.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Imported aftercare reopen events are omitted from replay

* Related IDs: Backlog/duration/opened/closed measures; Q1/Q2; C4/C6; P01-T01.
* Evidence: .copilot-tracking/details/2026-10-28/progress-dashboard-533-phase-details.md:12-16
  enumerates Identified, Accepted handover, Withdrawn and Excluded simulation
  actions plus human closure and controlled reopen records, but not the
  simulation reopen action. The generator
  support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/zf_flow_b.py:360-385
  sets "Reopened - aftercare", later "Accepted handover" again.
  support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py:273-275
  exports those states into labelled case.history, not controlled returns.
* Concern: Supporting only controlled returns does not reconstruct imported
  simulation reopenings. Deduplicating repeated closed states without the
  intervening simulation reopen can discard the subsequent genuine closure.
* Impact: Historical backlog, closure counts and per-episode duration statistics
  are wrong for an existing generated-data path.
* Smallest useful change: Explicitly replay "Reopened - aftercare" as an open
  transition. Define whether reopened episodes contribute to the displayed
  opened count or a separately disclosed reopen count, and use that definition
  consistently in backlog reconciliation. Preserve the later closure as a new
  episode; do not infer a reopen from a generic return.
* Action owner: Planning parent, with implementation owned by P01.
* Exact resolving evidence: Revised replay recipe and a constructed imported
  history fixture with Identified -> Accepted handover -> Reopened - aftercare
  -> Accepted handover, alongside a controlled-return/reopen fixture. Tests
  assert exact daily/weekly counts, backlog between closures and both duration
  samples, including an interval beginning during aftercare.
* Decision route: Direct planner correction. This implements the existing
  reopen-aware requirement rather than changing scope.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Archive status has no explicit mapping to the planned stage filter

* Related IDs: Closed status filter; P01-T01/P02-T01.
* Evidence: .copilot-tracking/plans/2026-10-28/progress-dashboard-533-plan.md:54-55
  specifies exact stage/team, while
  .copilot-tracking/details/2026-10-28/progress-dashboard-533-phase-details.md:29-30
  specifies the public query key status. Existing
  src/core/src/zava_forward/core/store.py:167-169 returns summary status
  "Completed" for every closed case, independently of its recorded stage.
* Concern: It is undefined whether status means that shared summary status,
  recorded stage, or closure outcome. Using summary status makes the filter
  effectively constant; silently using stage presents a different concept.
* Impact: The requested status control may be nonfunctional or misleading,
  especially for Withdrawn/Excluded cases that must not imply completed works.
* Smallest useful change: Define the status vocabulary and field mapping in the
  archive contract, including facets and displayed labels. A direct, bounded
  solution is explicitly labelled "Recorded case status (stage)", preserving
  recorded stage values and Unknown rather than treating every closure as
  successful completion. Do not change the legacy shared summary.
* Action owner: Planning parent.
* Exact resolving evidence: API/UI contracts name identical values and labels;
  unit/browser fixtures with Completed, Withdrawn, Excluded and missing stage
  prove distinct filtering, combined-filter behavior and non-success wording.
* Decision route: Direct planner correction; no new authority or user choice is
  needed to make the already requested filter meaningful.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Archive date membership is undefined for reopened or undated cases

* Related IDs: Closure-date filtering; coverage; P01-T01/P01-T02/P02-T01.
* Evidence: .copilot-tracking/plans/2026-10-28/progress-dashboard-533-plan.md:54-57
  requires closure-date bounds. Phase details define per-episode durations and
  missing coverage, but do not select an archive row's closure date or explain
  membership when it is unknown. Both repeat closures and closure without a
  usable date are already within the planned evidence boundary.
* Concern: A closed case can have multiple closure events, while a legacy closed
  case may have none. Filtering on its first or any closure can return a case
  outside the selected current-closure interval; discarding undated cases by
  default silently makes the archive incomplete.
* Impact: Results, totals, facets and page boundaries can disagree depending on
  an implementer's unstated choice.
* Smallest useful change: Specify the closure that ended the latest observed
  open episode as the archive closure date, with contradictory/unusable evidence
  remaining Unknown. Include otherwise eligible undated cases when no date
  filter is applied; exclude them from bounded date matches with a visible
  unknown-date coverage count. State that archive defaults are independent of
  the dashboard's automatic last-30-days range.
* Action owner: Planning parent.
* Exact resolving evidence: Revised archive contract plus fixtures for two
  closures separated by reopen, an undated closed case, inclusive start/end
  matches and unbounded archive defaults. Tests assert IDs, totals and paging
  after each filter, without deriving closure dates from stage_since.
* Decision route: Direct planner correction consistent with the accepted
  no-invented-dates and complete paged-archive direction.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: AI outcomes lack a date-range cohort definition

* Related IDs: Date selector and accepted/changed/rejected briefing measures;
  Q2/C7; P01-T01/P01-T02/P02-T01.
* Evidence: .copilot-tracking/plans/2026-10-28/progress-dashboard-533-plan.md:45-53
  dates closures and explicitly exempts current workflow/team/stalled/overdue
  measures from historical reconstruction, but supplies no temporal rule for AI.
  src/core/src/zava_forward/core/ai_tasks.py:174-176,307-309 supplies both created
  and resolved_at, which can fall in different ranges.
* Concern: Counting briefings created in range by their latest review state,
  versus reviews recorded in range, gives different accepted/changed/rejected
  totals. Neither the response nor UI contract tells the implementer which
  question the date selector answers.
* Impact: The dashboard can appear date-filtered while presenting outcomes from
  outside the chosen interval, and exact-number tests have no agreed oracle.
* Smallest useful change: Choose and label one cohort explicitly. A bounded
  choice is synthetic briefing review events with resolved_at in range, grouped
  by Accepted/Edited/Rejected, with Edited displayed as Changed. Define the
  treatment of missing/invalid review dates and distinguish unreviewed/held/
  quarantined records rather than count them as a completed review. Retain the
  existing task=briefing and source=ai boundary; rules/templates stay separate.
* Action owner: Planning parent.
* Exact resolving evidence: Plan/details and UI definition agree on the date
  field, timezone/calendar-day convention and categories. Unit fixtures place
  creation before the range and review inside it, creation inside and review
  after it, and missing review timestamps; exact counts change predictably with
  the selected interval.
* Decision route: Direct planner correction. The user has requested date-based
  synthetic usage, not a specific competing analytics cohort.

## Strengths and Residual Risk

* Separate progress/archive modules avoid widening briefing/map or legacy queue
  scope. Manager-only archive access and stats authorization preserve authority.
* Missing evidence is not converted into approval, savings, safety compliance or
  reconstructed historical team ownership. Existing overdue clocks are reused.
* Stable paging, URL restoration, table parity, cancellation and synthetic
  browser-server ownership are explicitly testable.
* Existing human screen-reader/user acceptance and full Fluent component
  adoption gaps remain disclosed, not claimed complete through axe alone.
* Full exact-head gate and hosted/human approval remain separate from local
  delivery. Prohibited Azure prerequisites block publication, not authorize a
  bypass or cloud fallback.

## Questions or Blocking Evidence Gaps

* No significant or divergent user decision is required by these findings.
* Recommendation provenance is a missing contract, not evidence that private
  data was read. The fail-closed synthetic-only result is available without
  opening a private dataset.
* If compliant shared heavy-check admission cannot be established, the planning
  parent must record validation blocked rather than weaken concurrency controls.

## Limitations

* No application tests, browser/axe runs, dataset reads, secret/environment-file
  access, Azure commands or source edits were performed.
* Source inspection was bounded to the supplied evidence seams. No open-ended
  research or fresh design/accessibility audit was undertaken.
* PR #529's live lifecycle was not re-queried; the caller's explicit stacked
  dependency and supplied research establish this critique's branch boundary.
* Existing untracked RPI inputs were left intact. Only this critique artifact
  was written; this assessment does not certify implementation or publication.

## Recommended Next Action

* Highest-impact finding: PC-002, preventing actual AI activity from being
  presented as synthetic demonstration usage.
* Action owner: Planning parent.
* Smallest next action: Add the fail-closed recommendation provenance contract,
  then directly disposition all six findings in plan/details with their
  resolving tests and compliant validation paths.
* User response required: No.

## Next Steps

The active planning parent should revise and finalize directly, preserving this
original Complete / Revise critique. Do not run another critique for this
candidate. Continue implementation only after these corrections are reflected;
no user action or peer-stage invocation is required from this critique worker.
