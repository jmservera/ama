---
title: Role task queues 76 final-candidate critique
ms.date: 2026-10-16
---

## Metadata

* Task ID: #76; role-task-queues-76.
* Critique date: 2026-10-16.
* Plan: .copilot-tracking/plans/2026-10-16/role-task-queues-76-plan.md.
* Phase details: .copilot-tracking/details/2026-10-16/role-task-queues-76-phase-details.md.
* Critique execution status: Complete.
* Assessment count: Exactly one final-candidate assessment; no implementation,
  test execution, external access or delegated review.

## Inputs and Criterion Boundary

* Caller direction: src code gaps plus supporting docs/RPI only; offline
  synthetic evidence, no owner approvals or perspective picker; preserve #116
  authentication/projection, #317 information architecture and #318 technical
  controls. Maximum three new test/check files, no removals or generated
  outputs.
* Supplied planning evidence: the plan and phase details above, and
  .copilot-tracking/research/2026-10-16/role-task-queues-76-research.md,
  including C1-C8 and its seven-row issue acceptance audit.
* Requirements evidence: docs/prds/zava-forward-retrofit-programme-demonstrator.md,
  FR-004/011/032/034 and AC-006/034/036/040; docs/case_study_48_original.md;
  docs/case_study_48_addendum.md; docs/reference/README.md;
  docs/reference/memory.md; and
  docs/reference/research/sector/housing-association-primer.md. Memory is
  context, not acceptance evidence.
* Layout evidence: docs/adrs/0006-src-layout-and-cutover.md and
  docs/architecture/mvp-to-src-parity-matrix.md.
* Relevant supplied source pointers inspected: src/core/src/zava_forward/core/
  store.py, sqlstore.py, projection.py, workflows.py, insights.py,
  signoffs.py and policies/ranking-v1.json; src/api/src/zava_forward/api/
  server.py, workbench.py and web/app.js; and
  src/api/checks/workbench_browser_check.py. These directory prefixes identify
  the individual files, not an assertion that every file was read in full.
* Assessment covers P01-P03, their tasks, acceptance evidence, dependencies,
  constraints and unresolved decisions once. It assesses implementation
  credibility, not delivered behavior or operational acceptance.
* The supplied research's issue audit is accepted as the offline issue
  evidence. No GitHub request was made. No properwarm.json, environment files,
  editor configuration or .copilot-tracking/github-issues material was read.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| #76 own list/status/next action; C1-C4 | Partial | Existing list preserved; current-step blocker and next-action derivation remain underspecified, PC-004. |
| #76 no picker; #116/#317/#318 | Covered | Plan explicitly preserves identity, role navigation, projections and domain controls rather than rebuilding them. |
| FR-004 / AC-006; C5-C7; P01-T01 | Partial | Six engineering definitions and draft-priority unavailability are explicit; temporal/state predicates and their oracles need PC-001. |
| #76 blocked-step reason/owner/action | Partial | Unknown named owner is correct; source-to-structured-step mapping needs PC-004. |
| #76 hazard clock/named owner; C7 | Covered | Recorded observations only; no statutory-clock derivation, service takeover or fabricated owner. Temporal queue use is covered by PC-001. |
| FR-034 / AC-036/040; P01-T02 / P02-T01 | Partial | Shared context and historical preservation are specified; source-trace coverage and projection-safe provenance need PC-002. |
| FR-032 / AC-034; C8; P02-T01/T02 | Partial | Server reset contract, focus and announcements are included; discriminating end-to-end proof needs PC-003. |
| C3/C5; P01-T02; JSON/SQL/CSV | Partial | Correct ordering principle and fallback are present; API/export propagation and multi-page oracles need PC-003. |
| P02-T02 validation environment | Partial | Explicit validation commands use a prohibited temporary path, PC-005. |
| P03-T01/T02; docs/RPI/delivery | Covered | Docs, parity/index/log, evidence reconciliation and PR without merge are included. Critique author does not execute delivery. |
| Owner decisions / external acceptance | Covered | Open decisions remain operational limitations, not blockers requiring approval for this offline slice. |
| Test/file/output limits | Covered | Plan locks three new test/check files maximum, preserves tests/manifests and requires constructed fixtures. Corrections below fit that boundary. |

## Verdict

* Verdict: Revise.
* Severity summary: Three High, two Medium; zero Critical or Low.
* Rationale: The direction is credible and bounded, but permits materially
  different queue results and insufficiently discriminating acceptance checks.
  The smallest corrections are local plan/detail contracts and explicit test
  oracles, not expanded product scope or another approval gate.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Membership needs one explicit evaluation clock and lifecycle truth table

* Related IDs: FR-004, AC-006, C4-C7, P01-T01, P02-T02.
* Evidence: The plan defines seven elapsed days, EPC 30 days/Survey 180 days,
  technical reassessment, pending deadlines and pending acceptance, but does
  not identify timestamp fields, evaluation-clock authority, equality rules
  or completion predicates. Store initializes self.as_of from dataset metadata;
  workflows.py uses timezone-aware event/deadline values and distinct
  HANDOFF_PENDING, Accepted and Completed states. Hazard observations include
  both response_due_at/responded_at and resident_update_due_at/resident_updated_at.
  Resident-update commitments also exist separately on the case.
* Concern: Identical records can be classified differently by using frozen
  dataset dates, wall time or rounded stage age. An old due date alone does not
  establish outstanding work. A future deadline is valid pending work, whereas
  a future observation date is unknown evidence; the plan's general
  "future dates remain unknown" statement does not distinguish these.
* Impact: New/stale/overdue membership can disagree across requests and stores,
  keep fulfilled work overdue, or lose a resident commitment when a handoff
  changes state. Timestamp freshness can also be mistaken for evidence validity.
* Smallest useful change: Define a single injected evaluation instant and its
  published as-of semantics, exact source fields and date-only normalization,
  inclusive/exclusive thresholds, malformed/missing/future observation handling,
  relevant EPC/Survey selection, and a compact lifecycle predicate table.
  Enumerate Offered/Received/Escalated as pending acceptance, exclude
  Accepted/Completed/Declined/Withdrawn from that predicate, preserve sender
  accountability, and evaluate each deadline against its own recorded
  satisfaction evidence. State how independent case resident updates survive
  handoff completion and how unknown completion evidence is labelled.
* Action owner: Planning parent.
* Exact resolving evidence: P01 details name the fields, clock and predicates;
  deterministic synthetic expected IDs cover just below/at/above 7/30/180-day
  boundaries, missing/invalid/future observations, future/equal/past deadlines,
  fulfilled and outstanding external responses/updates, and every handoff state.
  The same fixed instant and expected IDs are reused for JSON and SQL checks.
* Decision route: Direct planner correction. Keep thresholds as labelled
  engineering definitions; no operational SLA or owner ratification is invented.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Shared context lacks an explicit provenance projection and source-trace contract

* Related IDs: #116, FR-034, AC-036/040, C3/C4/C6, P01-T02, P02-T01.
* Evidence: FR-034 includes source trace as well as queue/case/history/suggestions.
  The plan and P02 name list/detail/history/suggestions but omit the source-trace
  consumption path. projection.py:hold_notes holds reason/source on
  return-shaped records and specific NOTE_KEYS; it does not automatically hold
  arbitrary new reason/source aliases. Store.page_cases has no general staff
  detail redaction pass, while Store.detail applies redact_staff_detail.
  workflows.py:_disposition records human-written reason/source/next_action.
* Concern: "Follow existing need-to-know rules" does not identify how a newly
  shaped shared context gets projected consistently. Copying a return reason
  or source into a generic context can evade existing shape-sensitive handling.
  One aggregate source/as-of/version also need not identify the evidence behind
  each blocker, handoff or rationale. Merely placing context near a suggestion
  does not establish that its cited reviewer/prerequisite belongs to that case.
* Impact: Restricted free text can escape through queue context or provenance,
  or the views can agree on generic wording while displaying unrelated or
  unsupported source/reviewer evidence. This would undermine #116 and FR-034.
* Smallest useful change: Specify the context fields and origin references,
  their role-aware projection before serialization in both stores, and a
  source-trace rendering/reuse task. Preserve safe generated labels separately
  from human-written evidence. Keep historical snapshots immutable and distinguish
  current context from event-time context. Bind each rationale/source/version
  and proposed reviewer/prerequisite to the selected case; absent data stays Unknown.
* Action owner: Planning parent.
* Exact resolving evidence: P01/P02 detail identifies the shared projection entry
  point and source-trace consumer. Synthetic sentinel strings in return,
  handoff and hazard free text are present only for permitted roles and absent
  from restricted list/detail/context/export responses and unchanged contractor
  outputs. Two cases with different sources, versions and prerequisites show
  consistent per-case queue/detail/history-current/source/suggestion context;
  switching cases, including a delayed obsolete response, never swaps evidence.
  Historical event ownership remains unchanged.
* Decision route: Direct planner correction using existing role rules. Do not
  request or manufacture new role/redaction approval.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: End-to-end queue and reset checks need discriminating oracles

* Related IDs: C5/C8, FR-032/034, AC-006/034/040, P01-T02, P02-T02.
* Evidence: server.py:filt currently accepts stage/area/wave/owner/contractor/flag
  only. JSON and CSV both call it, but CSV bypasses the JSON paging branch and
  its local error handling. SqlStore.page_cases uses optimized SQL when limited
  and Store fallback when unlimited. app.js uses limit=50 and
  next_cursor for load-more, but CSV is unlimited. The existing workbench browser
  fixture has three cases. Reset defaults are currently hardcoded in app.js.
* Concern: "Compare list/detail context and CSV membership" and "semantic queue
  membership/reset" do not require an oracle that catches a dropped queue query,
  filtering after pagination, cursor gaps/duplicates, or a browser ignoring the
  server reset contract. Three cases cannot expose a page-boundary defect.
  Invalid queue tests do not yet specify both endpoints' expected responses.
* Impact: Unit predicates can pass while HTTP/browser filters return unfiltered
  rows or wrong totals, later matching records are unreachable, exports diverge,
  or reset remains effectively client-hardcoded.
* Smallest useful change: Explicitly wire and validate the queue parameter
  through filt, JSON, CSV, Store and SqlStore, including unavailable/unknown
  values. Add an independent expected-ID/count/order matrix with more than 50
  constructed records and mixed matches across page boundaries; exercise
  keyset load-more and a non-default sort with existing filters. For reset,
  require a server-supplied default different from the old hardcoded one in a
  bounded test, then verify clearing every override and selection.
* Action owner: Planning parent.
* Exact resolving evidence: Details state matching authorized JSON/SQL/CSV ID
  sets, exact totals, ordered concatenated pages without duplicates or omissions,
  consistent controlled error semantics for invalid/unavailable queues on JSON
  and CSV, and unchanged records. Browser checks assert the emitted queue query,
  visible reason, all-scope/search/stage/area/wave/owner/flag/queue/sort reset,
  first page, no selected case, server-defined order/version, logical focus and
  result announcement. Extend existing files or stay within three new files;
  do not produce checked-in fixtures, screenshots or generated outputs.
* Decision route: Direct planner correction; no new endpoints, grants or
  perspective controls are needed.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Blocked-step structure and next-action precedence are not mapped to recorded controls

* Related IDs: #76 blocked-step criterion, C4/C7, P01-T01, P02-T01.
* Evidence: P01 says to reuse reasons/accountability and derive typed context.
  Store.gate_reasons returns prose combining funding, hazard, resident and
  technical checks; Store.detail adds building blockers separately.
  signoffs.py:missing_items supplies item/assigned_to, while technical_gate
  formats these into prose. The case also has waiting_on/reason and independent
  return/handoff next_action records.
* Concern: There is no mapping from these sources to blocked step,
  reason, responsible role, named person, next action and source, or a rule for
  which current action leads when multiple controls apply. Parsing prose can
  confuse a responsible role with a named owner; reading only gate_reasons
  omits the separate building blockers. A release prerequisite need not mean
  the current stage itself is blocked.
* Impact: Queue labels can contradict detail or recommend the wrong current
  action despite preserving the underlying domain controls.
* Smallest useful change: Add a short source-to-field mapping for existing
  structured control data and an explicit deterministic multi-blocker/current
  action rule. Label the affected step instead of treating every downstream
  prerequisite as a current-stage stop. Include building, resident, technical,
  funding and hazard sources without rewriting their decision logic.
* Action owner: Planning parent.
* Exact resolving evidence: Details define structured derivation without parsing
  display prose or assigning people from role labels. Synthetic cases cover a
  building-only blocker, multiple simultaneous controls, a future-step
  prerequisite, missing technical evidence, and a role-only assignment;
  list/detail show the same affected step, reason, next action and explicit
  named-owner Unknown.
* Decision route: Direct planner correction. Existing control owners and
  technical decisions remain authoritative; no assignment or approval is inferred.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Planned validation depends on a prohibited temporary path

* Related IDs: Plan User Decisions and Requirements, P02-T02.
* Evidence: The plan requires /tmp/zf164 and phase details invoke its Python.
  The active execution constraint prohibits temporary-directory file operations.
* Concern: The prescribed environment cannot be prepared or used as written
  within the current task boundary.
* Impact: A following implementer may violate the constraint or omit validation
  while reporting the plan as executable.
* Smallest useful change: Replace temporary-path instructions with an existing
  approved interpreter or a project-relative ignored environment/runtime
  location. Set runner scratch/cache/output paths within the permitted project
  tree where needed; retain absolute current-worktree PYTHONPATH and pip-only
  dependency handling. Do not restore dependencies without a documented missing
  dependency or manifest change.
* Action owner: Planning parent.
* Exact resolving evidence: P02 commands use no prohibited temporary locations,
  distinguish transient runtime data from deliverables, and explicitly suppress
  browser screenshots/traces/generated reports. The final allowed diff contains
  source/docs/RPI only, at most three new test/check files and no removals.
* Decision route: Direct planner correction to honor the active constraint.
  No owner response is required.

## Strengths and Residual Risk

* Draft ranking policy is correctly unavailable as approved priority. Accepted
  AI advice is not promoted to programme priority.
* SQL fallback before slicing, unchanged contractor output, named-owner Unknown,
  sender accountability and historical snapshot preservation are sound choices.
* No database migration, live dependency, new identity system, perspective
  simulator or task-writing API is proposed.
* Engineering definitions remain provisional. Operational policy ratification,
  legal/professional decisions, direct human validation and live SQL Server,
  Azure or AI results remain explicitly unmet, not newly required approvals for
  this slice.

## Questions or Blocking Evidence Gaps

* None requiring a user answer. The supplied evidence supports all five direct
  planner corrections. Do not resolve operational unknowns by inventing policy
  owners or approvals.

## Limitations

* This is a plan credibility assessment, not a source implementation review.
  No tests were run and no behavior is claimed delivered.
* Source inspection was bounded to supplied evidence and directly referenced
  contracts. No fresh issue comments, private data or external services were
  accessed. No claim is made about uninspected implementation paths.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Revise the membership clock/source/state truth table,
  then incorporate PC-002 through PC-005 into the same plan/detail revision.
* User response required: No.
* Final-candidate handoff: Reconcile this one complete finding set directly;
  finalize the plan without another critique. This reviewer stops here.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-16/role-task-queues-76-plan.md | Final candidate assessed; unchanged. |
| .copilot-tracking/details/2026-10-16/role-task-queues-76-phase-details.md | Phase details assessed; unchanged. |
| .copilot-tracking/research/2026-10-16/role-task-queues-76-research.md | Supplied offline research and issue audit; unchanged. |
| .copilot-tracking/reviews/2026-10-16/role-task-queues-76-critique.md | Single complete finding set and handoff. |

## Next Steps

Planning parent applies the five direct corrections and finalizes without a
second critique. No user action is required. No implementation or further
review is performed by this critique task.
