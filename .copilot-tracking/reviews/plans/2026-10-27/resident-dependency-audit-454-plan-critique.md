---
title: Resident dependency graph audit final-candidate plan critique
description: One independent graph and readiness assessment for PR 454
ms.date: 2026-10-27
---

## Metadata

* Task ID: jmservera/ama#454:dependency-audit-2026-10-27
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/resident-dependency-audit-454-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/resident-dependency-audit-454-phase-details.md
* Critique execution status: Complete
* Assessment count: One final-candidate critique; no nested agents.
* Inspected branch: docs/resident-prd-backlog-readiness-441, HEAD 3bc25aae.
  Read-only PR inspection confirmed PR 454 OPEN against main.

## Inputs and Criterion Boundary

* Caller requirements: one comprehensive graph correction covering S01-S16,
  R1-R3 and every RB row, with S17-S20 checked for adjacent regressions;
  explicit missing edges, cumulative completed R3 evidence before RB-17,
  corrected M1 critical path and one final graph reread before push.
* Assessed evidence: the named plan, phase details and research; PRD
  docs/prds/zava-forward-retrofit-programme-demonstrator.md, story table
  at lines 1110-1131 and M1/R0-R5 sequence at lines 1270-1306;
  .copilot-tracking/changes/2026-10-25/resident-prd-backlog-readiness-441-draft-backlog.md
  in full; and the active stage reconciliation and protocol clarification in
  .copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/resident-service-unregistered-proposal.md:693-728.
* Repository context: original case study, addendum, reference index and
  owner memory read; memory is context, not evidence.
* Decisions preserved: no OD-53 prerequisite for RB-17/18; OD-53 applies
  conditionally to later positive activation; routine automation OFF;
  independent urgent/help routes; M1 is partial R2; paired protocol freeze
  precedes relevant data collection; existing quality and acceptance blockers
  remain unresolved.
* Boundary: assess whether the plan credibly specifies the correction, not
  whether the currently uncorrected backlog already passes. No unrelated
  requirements-quality reassessment, live authority assessment, executable
  validation, source edit, publication or merge.
* Locked ownership: parent owns Markdown/link and diff review only. Test
  execution, removal, addition and generated targets are all none. Source
  targets are at most the two existing Markdown documents named above,
  plus original RPI evidence.

### Assessed input identity

| Input | SHA-256 |
| --- | --- |
| Plan | 827a080ac14037b992385869b21341a468a459b079500dca6b0c8e7963a81bea |
| Phase details | 23330e202d88b4ff6b60bb6e64ff8b4f7b33d42e0d6c3e62a3447aa72063bf9b |
| Research | 75c4155aeaf897a46af689b87e8ec8ed871b7e3e5dd8861272adcb733693e882 |
| PRD | 3094a602a5763ae6e25838639e1f7315735d065888c9d5b6caa3dd7ac456645b |
| Draft backlog | aa59664e5cf2cbcdba54ac342c1372128881fd037b54ca32ad25fd8d7e9e58ce |
| Active proposal | f7325a27bd2c0b244cab278925bd6caa597fdd4f734913fb4a3f4fcd5f4385fe |

## Coverage Assessment

The following rows assess planned coverage, not delivered corrections or
executed acceptance tests. Research C1-C3 supplies the story/backlog/stage
comparison; C5 supplies the active proposal reconciliation.

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| RB-01; R0 | Covered | Explicit root treatment; exact candidate/fixture expectations and conditional paired protocol freeze retained. |
| RB-02; S01/S02/S05/S06/S09 fixtures | Covered | Versioned fixture path retained; research identifies identity, grant-owner, published projection, publication authority and offered-slot prerequisites. Final reread expressly checks fixtures. |
| RB-03 | Covered | R0 measurement design retained alongside M1, not made a dependency on later load execution. |
| RB-04; S01 | Covered | Synthetic identity follows RB-02; no provider selection or real-account approval inferred. |
| RB-05; S02 | Covered | RB-02/RB-04 and named 444 reuse boundary retained. External reuse agreement remains an implementation/sizing dependency, not assumed delivery. |
| RB-06; S04 | Covered | RB-05 supplies S02; revocation remains within M1. |
| RB-07; S03 | Covered | RB-05 transitively supplies S01/S02; recovery/logout remain within M1. |
| RB-08; S05 | Covered | Separate row follows RB-05; projection fixture checked. |
| RB-09; S06 | Covered | Explicit RB-08/RB-05 correction; publication-authority fixture retained. |
| RB-10; M1 | Covered | RB-03, RB-04 through RB-09 and staged M1 accessibility scripts; no full-R2/upload prerequisite. Critical-path prose explicitly branches to RB-06, RB-07 and RB-08 then RB-09. |
| RB-11; S07 | Covered | Separate RB-05/RB-09 row retained; research identifies safe file configuration and final fixture check. |
| RB-12; S08 | Covered | Adds RB-11, retains RB-05/RB-09; no clean-scan/publication conflation. |
| RB-13; S09/S10 | Covered | Separate row, retained grant/projection dependencies; explicit S09-before-S10 internal acceptance order avoids a self-cycle. |
| RB-14; S11/S12 | Covered | Adds RB-11/RB-13 to RB-05/RB-08, reaching S05/S07/S09; explicit S11-before-S12 order. |
| RB-15; S13 | Covered | RB-14 supplies S11/S12; retained RB-05/RB-08. |
| RB-16; S14 | Covered | Adds RB-15 while retaining RB-14 and prior grant/projection edges; no-detriment/help boundary retained. |
| RB-17; S15 | Covered | Requires RB-13 through RB-16 AND completed cumulative R3 evidence AND independent task registration/evaluation/release. OD-53 explicitly excluded. |
| RB-18; S16 | Covered | RB-15/RB-17 retained for task-failure verification; urgent/help route explicitly independent of task release and model. No OD-53. |
| RB-19; S17 | Covered | RB-17/RB-18 retained; conditional positive-activation OD-53 preserved, not imposed on deny-by-default tests. |
| RB-20; S18 | Covered | RB-19 and existing task-release edges retained; negative suspension versus positive activation/restart distinction preserved. |
| RB-21; S19 | Covered | Cumulative R3 comparator and RB-01-frozen baseline required; R5 collects/reviews, not retrospective protocol authoring. Conditional R4 remains distinct from completed R3. |
| RB-22; S20 | Covered | R1-R3 evidence plus conditional R4/NFR reporting retained; blocked/Not-run entries do not establish R5 completion or AC-140. |
| RB-23 | Covered | Explicit staged script dependencies required, with M1 scripts tracked separately; full R5 accessibility cannot accidentally block M1 or create a cycle. |
| RB-24 | Covered | Existing measurement/slice/scan-drill dependencies retained; conditional R4 unavailable results remain Not run. No executable run authorised by this correction. |
| G0; RB-G1 | Covered | Exact-candidate assessment/findings disposition prerequisite and existing FAIL/blocked owner acceptance preserved. This graph audit does not reassess requirements quality. |
| RB-G2; RB-G3; RB-G4 | Covered | Explicit governance inventory treatment; open decisions, deferred/unmet architecture registration and accepted-build platform evidence remain separate, not invented execution edges. |
| R1 | Covered | Identity/grants/recovery/revocation/shared-device negatives and essential privacy/accessibility evidence before advancing. |
| R2 | Covered | R1 evidence plus case/document/upload/replay/review evidence; M1 explicitly remains only a composition of R1 and part of R2. |
| R3 | Covered | R2 evidence plus appointments, reconciliation, assisted/no-detriment, accepted handoff and completed portal/workflow-only baseline under the frozen protocol. |
| R4/R5 | Covered | Task release and conditional activation separated; R5 evidence review cannot convert blocked R4 into acceptance. Active proposal reconciliation is an allowed second source target. |
| P01-T01; research C1-C3/C5 | Covered | One whole-graph edit uses all twenty story mappings and release gates rather than only comment locations. Intended edges are acyclic; internal story ordering is explicit. |
| P01-T02 | Covered | One final comparison of all stories, gates, RB rows, fixtures and cycles; Markdown/local links/diff and exact hashes only. |
| P02-T01 | Covered | One independent Review retains complete findings and assessed hashes; later findings reported, not another correction loop. |
| P02-T02; research C4 | Partial | Evidence-backed four-thread handling and no merge specified, but post-Review rebase can change assessed source without an explicit publication stop: PC-001. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 0 High, 1 Medium, 0 Low.
* Rationale: The proposed graph correction covers the supplied graph/readiness
  boundary. One publication-control gap could invalidate the sole final graph
  reread and independent Review before push. It needs a small direct planner
  correction, not further research or another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Stop publication if the late rebase changes assessed source

* Related IDs: P01-T02, P02-T01, P02-T02; final-graph-reread requirement.
* Evidence: .copilot-tracking/plans/2026-10-27/resident-dependency-audit-454-plan.md:118-124
  schedules pull/rebase after Review and before push.
  .copilot-tracking/details/2026-10-27/resident-dependency-audit-454-phase-details.md:54-62
  says to report an invalidated assessment if source changes, but then
  instructs push and thread handling without explicitly stopping that path.
* Concern: The plan detects the possibility of changed source, but reporting
  invalidation alone does not ensure the pushed graph is the graph reread
  once and independently reviewed. A late rebase can change PRD dependencies,
  backlog edges or active proposal reconciliation after those checks.
* Impact: The parent could publish a different graph or resolve graph threads
  with evidence that does not assess the published source. That undermines
  the caller's final-reread boundary even if the invalidation is disclosed.
* Smallest useful change: Make P02-T02 explicitly compare assessed PRD,
  backlog and proposal hashes after synchronization and immediately before
  push. If assessed source changed, stop publication and thread resolution,
  report invalidation and the changed paths, and do not start another
  correction/reread/Review cycle. A bot-only update leaving assessed source
  byte-identical may continue, with the old Review scope stated accurately.
* Action owner: Planning parent.
* Exact resolving evidence: Plan and phase details both contain that
  fail-closed publication condition; the later changes record records the
  assessed versus pre-push source hashes and either byte identity or an
  explicit stopped publication. No new executable validation is required.
* Decision route: Direct planner correction. Existing owner direction already
  supplies the one-cycle limit; no significant or divergent user decision.

## Strengths and Residual Risk

* The plan distinguishes engineering prerequisites, internal acceptance order
  and cumulative release evidence. Merely adding RB-15 to RB-17 would not
  have met S15; the plan correctly requires completed R3, including R2/R1
  and the portal-only baseline.
* The source maximum, no-test ownership and docs-only validation are explicit.
  No broader local gate is required or claimed by this critique.
* Current source defects identified in the research are implementation work
  already planned, not additional critique findings.
* All acceptance observations remain Not run. Quality FAIL, G0 blocking,
  unregistered architecture, unknown sizing and live authority are preserved
  limitations, not newly accepted risks or approvals.
* C4 thread contents were supplied through the research evidence log, not
  independently re-retrieved. The graph findings were independently checked
  against the supplied local PRD and backlog instead.

## Questions or Blocking Evidence Gaps

* None for the bounded assessment. PC-001 is planner-owned; no user answer
  is needed and no additional research is requested.

## Limitations

* This is a plan critique, not the later final graph reread or implementation
  Review. It does not consume either of those planned checks.
* No source was corrected, no runtime/test command was run, no historical
  outcome was changed and no publication or thread mutation occurred.
* No requirements-quality debt outside graph/readiness was assessed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the fail-closed source-identity condition to
  P02-T02 in the plan/details and record disposition of this original critique.
* User response required: No.
* Return this complete finding set to the parent; do not commission another
  critique or expand the correction boundary.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/resident-dependency-audit-454-plan.md](../../../plans/2026-10-27/resident-dependency-audit-454-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-27/resident-dependency-audit-454-phase-details.md](../../../details/2026-10-27/resident-dependency-audit-454-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-27/resident-dependency-audit-454-research.md](../../../research/2026-10-27/resident-dependency-audit-454-research.md) | Supplied dependency derivation |
| [.copilot-tracking/reviews/plans/2026-10-27/resident-dependency-audit-454-plan-critique.md](./resident-dependency-audit-454-plan-critique.md) | This single complete critique |

## Next Steps

The active planning parent may resolve PC-001 directly and preserve this
original Revise outcome. No user action is required. This critique stops here;
it authorises no implementation, publication, nested review or merge.
