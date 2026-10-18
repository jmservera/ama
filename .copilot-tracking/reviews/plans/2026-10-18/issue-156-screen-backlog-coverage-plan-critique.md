---
title: Issue 156 screen backlog coverage plan critique
description: One independent final-candidate readiness assessment
ms.date: 2026-10-18
---

## Metadata

* Task ID: issue-156-screen-backlog-coverage.
* Critique date: 2026-10-18.
* Plan: .copilot-tracking/plans/2026-10-18/issue-156-screen-backlog-coverage-plan.md.
* Phase details: .copilot-tracking/details/2026-10-18/issue-156-screen-backlog-coverage-phase-details.md.
* Critique execution status: Partial.
* This is the one requested independent final-candidate plan critique. It is not
  the later original independent Review, an implementation review or acceptance.

## Inputs and Criterion Boundary

* Assessed the supplied plan, phase details and
  .copilot-tracking/research/2026-10-18/issue-156-screen-backlog-coverage-research.md.
* Applied the caller's complete requirement: new ordered RPI distinct from
  merged #400; supplied branch and base; bounded all-state inventory; exclusive
  evidence-backed classification; exact existing screen traces or NOT SUPPLIED;
  preserved original fifteen rows, decisions and Blocked design gate; restricted
  documentation writes; one critique and one later original independent Review;
  Not accepted means local freeze and stop, without a replacement or self-Pass.
* Read required project context, the existing profile review including
  T01-T11/C01-C04, D01-D04 and G156, the supplied atlas sections and PRD
  conversation/profile mapping. These distinguish source evidence, proposals,
  engineering and human acceptance.
* Read-only branch inspection confirmed docs/screen-backlog-coverage-156 at
  2ca6d1c48bb95b65e6c349fe508e99c00a74efbe. Existing untracked planning/state
  artifacts were not changed.
* Independently queried the research's cited public REST issue endpoint with
  state=all, per_page=100 and gh api --paginate, excluding pull-request objects.
  Examined issue membership, scope/acceptance evidence and every named edge
  case. No issue or other remote state was changed.
* The caller-supplied export files are outside the permitted file-access
  boundary. Neither file was opened or copied. Their equality and SHA-256
  values remain supplied assertions, not independently verified results.
* Boundary: credibility of the plan and its evidence/validation contract only.
  Missing designs and qualified human acceptance remain legitimate later work,
  not reasons to invent designs, close #156 or run application/browser tests.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| New RPI, branch/base and #400 separation | Covered | Correct branch/base observed; new task paths; prior records protected |
| Q1 / W2 / export-to-REST equality | Partial | Public REST independently gives 184 unique issues, 139 open/45 closed; original export comparison unavailable, PC-001 |
| Q2 / exclusive classifications | Partial | Independent reconstruction matches all four aggregate and state counts; no supplied expected per-class membership ledger, PC-002 |
| Q3 / P01-T01 / exact screen traces | Covered at planning level | Individual rows, exact partial T/C references, missing-flow sentinel, versions, checks and owner/actions required; no designs fabricated |
| P01-T01 / unknown delivery surfaces | Covered | All eight issue bodies inspected; record/control/report requirements do not select an application-screen route |
| P01-T02 / existing KB and historical gate | Covered | Three canonical targets; existing fifteen rows, D01-D04 and G156 retained; dated G01 continuation only |
| P02-T01 / semantic validation | Partial | Counts, universe, links and preservation planned; exact class/trace set checks insufficiently specified, PC-002 |
| P02-T02 / one original Review | Covered | Fresh independent Review later, no amended/replacement Review or self-Pass |
| P03 / publication and Not accepted freeze | Covered | Conditional push/PR; Not accepted remains local and stops for coordinator routing |
| Research / source attribution | Partial | Deeper incorrectly assigns storage-delivery evidence to #159, PC-003 |
| Runtime, private-data and approval boundaries | Covered | Explicit exclusions; no runtime/accessibility/human acceptance inferred |

### Independent inventory reconciliation

The fresh cited REST source returned 184 unique non-PR issue IDs, with 139 open
and 45 closed. The following is this critic's explicit reconstruction using the
plan's broad screen-impact rule, not a claim to have compared an unpublished
research classification ledger or the original export. The four sets are
disjoint and their union equals the fresh REST issue set.

| Classification | Total | Open | Closed |
| --- | --- | --- | --- |
| includes-screen | 74 | 57 | 17 |
| no-screen | 86 | 59 | 27 |
| epic-covered | 16 | 16 | 0 |
| unknown | 8 | 7 | 1 |
| Total | 184 | 139 | 45 |

* includes-screen: 74, 75, 76, 77, 78, 79, 80, 82, 83, 84, 85, 86, 87, 88,
  90, 91, 92, 94, 95, 96, 97, 98, 99, 101, 102, 105, 106, 107, 110, 111,
  112, 116, 119, 120, 122, 130, 131, 132, 133, 134, 135, 146, 150, 151,
  152, 153, 154, 159, 160, 161, 162, 163, 211, 212, 214, 215, 217, 219,
  220, 221, 225, 226, 227, 228, 229, 230, 231, 232, 233, 327, 344, 349,
  350, 360.
* no-screen: 6, 10, 23, 33, 38, 46, 47, 48, 49, 51, 52, 53, 64, 103,
  108, 114, 115, 117, 118, 124, 128, 129, 137, 138, 139, 140, 141, 142,
  143, 144, 145, 147, 148, 155, 156, 158, 164, 166, 167, 168, 169, 170,
  171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184,
  185, 186, 188, 190, 191, 192, 193, 194, 196, 197, 198, 199, 200, 201,
  202, 203, 206, 209, 210, 216, 223, 224, 290, 322, 323, 329, 332, 339,
  351, 358.
* epic-covered: 73, 81, 89, 93, 100, 104, 109, 113, 123, 136, 149, 157,
  165, 195, 208, 218.
* unknown: 121, 125, 126, 127, 187, 189, 213, 222.

Classifications describe inventory routing, not delivered or accepted designs.
Cross-cutting permissions, projections, validation and schema controls are
included where they affect the planned visible interaction or state, even when
their own issue has no separate page. Pure experiments, test harnesses,
fixtures, technical infrastructure and documentation do not add screen rows.
These distinctions need concise individual or genuinely shared scope evidence
in the implementation; matching aggregate counts alone does not establish them.

### Named edge-case assessment

| Issues | Independent scope assessment |
| --- | --- |
| #233 | includes-screen: explicit cross-role screen-design/atlas pass; not an epic and not absorbed by #225-232 |
| #225-232 | Eight separate includes-screen issues with explicit queues/views, state distinctions and role-specific checks |
| #159 | includes-screen: case-aware conversation panel, citations, keyboard/message behavior and workflow-only fallback; storage is #160 |
| #215 | includes-screen: per-role alerts/chat patterns, doubt/no-source states and comprehension checks |
| #152 | includes-screen: responsive layouts, navigation and scope; existing IA engineering remains partial, not design acceptance |
| #76 | includes-screen: visible queue signals, status, next action, ownership and reset |
| #77 | Closed includes-screen: visible signal definitions, active scope and versioned reset; closure does not prove current design acceptance |
| #87/#88/#91 | Closed includes-screen: offer/commitment and household constraints; distinct update/remedy ownership states; quality/evidence/defect/handover state impacts |
| #101 | Closed includes-screen: heatmap/funnel, denominators, reconciliation and drill-through |
| #156 | no-screen: documentation traceability and review gate, not another application screen |

All eight unknowns were inspected individually. #121 concerns privacy/rights
records; #125 an optional read-only discovery assistant; #126 release and
benefits registers; closed #127 human-owned regulatory review; #187 simulator
replay/pause controls; #189 cost/run controls; #213 automated source-change
review routing; #222 evaluation/cohort records. None of their issue criteria
settles application UI versus CLI/report/manual delivery. Existing partial
journey context may be linked without deciding that missing surface choice.

## Verdict

* Verdict: Blocked.
* Rationale: the core plan is bounded and its aggregate classification is
  independently reproducible. However, the explicitly required original
  export-to-REST comparison cannot be independently established from accessible
  inputs. There is also a substantive semantic-validation gap and one incorrect
  evidence attribution. Resolve these through the planning parent; do not run
  another critique.
* Severity summary: one High, one Medium, one Low; zero Critical.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Original export comparison lacks accessible verifying evidence

* Related IDs: Q1, W2, P01-T01, P02-T01; all-state export reconciliation requirement.
* Evidence: the caller supplies two raw exports outside the permitted file-access
  boundary. The research records their hashes and claims equal sets, but supplies
  neither the original export's ID/state projection nor an accessible comparison
  record. This critique independently verifies the fresh REST universe only.
* Concern: the required independent original-export comparison is unverified.
  A fresh REST query is not the supplied coordinator export, even when its total
  and state counts agree.
* Impact: declaring the snapshot fully reconciled would overstate the evidence;
  equal totals can conceal different issue IDs.
* Smallest useful change: make the original export's ID/state projection and
  provenance available in a permitted workspace-relative evidence location,
  without reading or copying forbidden paths; then record its exact set
  comparison with the captured REST universe. If the original export is
  unavailable, record that limitation rather than claim it was checked.
* Action owner: planning parent/coordinator holding the original supplied export.
* Exact resolving evidence: an accessible, provenance-bound original-export
  projection and comparison recording 184 unique IDs, zero export-only IDs,
  zero REST-only IDs, matching per-ID states and 139 open/45 closed, with capture
  identity/hash references and the command/result. Keep raw data uncommitted.
* Decision route: direct evidence/planner correction, not a significant or
  divergent user decision. Do not replace the original export silently.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Count checks do not establish issue-class and screen-trace identity

* Related IDs: Q2, P01-T01, P02-T01, P02-T02; exclusive classification and
  every-known-screen trace requirements.
* Evidence: phase details P02-T01 compares extracted IDs to REST/export IDs and
  counts states, classes and unique trace rows. P02-T02 specifies classification
  reconciliation with representative edge cases. Research gives class totals
  and eight unknown IDs, but not expected membership for the other three sets.
* Concern: the stated validation can pass a count-preserving classification
  swap or 74 unique trace rows that do not equal the includes-screen IDs.
  Representative checks do not demonstrate the complete classification.
  This critique's reconstructed membership matches the totals but cannot prove
  the research intended the same members.
* Impact: a known screen issue could remain untraced while every stated count
  and total-universe check passes.
* Smallest useful change: explicitly freeze the evidence-backed per-class ID
  sets in the task evidence and require issue-to-class agreement against that
  source, not just totals. Require trace-ID set equality with includes-screen,
  exact unknown membership and no traces substituted from excluded classes.
  Have the one original Review assess this complete mapping, with deeper
  source checks for ambiguous and named edge cases.
* Action owner: planning parent.
* Exact resolving evidence: revised P02-T01/P02-T02 contract and later validation
  output showing zero issue-class mismatches, zero missing/extra screen trace
  IDs, no duplicates or class overlaps, all eight expected unknowns and
  evidence-backed routes for all sixteen epics. Each trace must also satisfy
  the required link/version-or-NOT-SUPPLIED, check and owner/action fields.
* Decision route: direct planner correction; user requirements already settle
  the desired completeness. No user response required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: Research attributes chat-storage delivery evidence to the panel issue

* Related IDs: research Cycle 1 / Deeper, C3, P01-T01; explicit #159 edge case.
* Evidence: research says "#159 says storage exists while #162 still says
  endpoints do not exist". Public #159 instead describes the conversation panel
  and says no multi-turn, follow-up, streaming or resumable panel exists.
  PRD FR-055 maps the panel to #159; FR-056 maps thread storage to #160.
* Concern: the cited contradiction conflates a panel feature with its storage
  dependency and can seed an incorrect delivery/evidence statement in the trace.
* Impact: implementation could mislabel existing storage as a delivered
  conversation panel or retain an untraceable contradiction.
* Smallest useful change: correct the research attribution to the actual storage
  issue/source and keep #159 panel scope separate from #160 storage/lifecycle;
  retain any genuine stale-delivery contradiction with exact source evidence.
* Action owner: planning parent.
* Exact resolving evidence: corrected Deeper source attribution and distinct
  #159/#160 trace provenance consistent with PRD FR-055/FR-056, without claiming
  that storage proves a current panel design or accepted behavior.
* Decision route: direct evidence correction, not a new user decision.

## Strengths and Residual Risk

* New task identity, correct base and protected #400 records preserve ordered
  workstream lineage.
* All-state enumeration retains delivered screens; the explicit unknown set
  resists invented surface choices.
* Existing partial traces are usable without turning historical H or engineering
  E into current design acceptance. Missing designs remain explicit.
* Original fifteen rows, decision register and Blocked gate are protected; G01
  gets a dated inventory continuation rather than rewritten historical results.
* Documentation-only validation is proportionate. No runtime, browser, model,
  deployment, legal, accessibility-conformance or human-acceptance result is
  claimed by this critique.
* One independent Review remains later. A Not accepted result must remain
  unchanged, freeze locally and stop; no corrective implementation/replacement
  Review is authorized by this critique.

## Questions or Blocking Evidence Gaps

* PC-001 is an evidence-access gap for the planning parent/coordinator, not a
  request for a new scope choice. No question is routed to the user here.
* Missing screen designs and named human approvals do not block this bounded
  documentation inventory; they continue to block design acceptance.

## Limitations

* Neither original raw export nor its reported SHA-256 was independently read
  or recomputed. Fresh public responses are a later observation and cannot
  certify historical byte identity.
* Some exploratory command outputs exceeded the tool's display limit; those
  generated output files were not opened. Bounded subsequent queries supplied
  the membership, aggregate results and edge-case evidence used here.
* No implementation exists in the candidate diff for this critique to accept.
  The explicit reconstruction is planning evidence, not executed per-screen
  acceptance or an independently accepted classification ledger.
* Only this critique artifact was written. Plan, details, research, state,
  canonical documentation and earlier review records remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent/coordinator.
* Smallest next action: supply the permitted original-export projection and
  record the comparison; directly resolve PC-002 and PC-003 in finalization.
* User response required: no scope/decision response; source holder must clear
  the evidence gap.
* Do not dispatch a second critique. Preserve this Partial/Blocked outcome and
  its dispositions. Once resolved, finalize the plan and follow the ordered
  implementation/validation path to the one original independent Review.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-18/issue-156-screen-backlog-coverage-plan.md](.copilot-tracking/plans/2026-10-18/issue-156-screen-backlog-coverage-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-18/issue-156-screen-backlog-coverage-phase-details.md](.copilot-tracking/details/2026-10-18/issue-156-screen-backlog-coverage-phase-details.md) | Assessed task and validation details |
| [.copilot-tracking/research/2026-10-18/issue-156-screen-backlog-coverage-research.md](.copilot-tracking/research/2026-10-18/issue-156-screen-backlog-coverage-research.md) | Research claims and supplied provenance |
| [docs/reference/research/ux/zava-forward-prototype-profile-review.md](docs/reference/research/ux/zava-forward-prototype-profile-review.md) | Protected historical traces, decisions and Blocked gate |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-156-screen-backlog-coverage-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-156-screen-backlog-coverage-plan-critique.md) | This single independent critique |

## Next Steps

Planning parent: clear PC-001 and apply the direct PC-002/PC-003 corrections,
record dispositions and finalize without another critique. No user command or
new user decision is required. Do not start the original independent Review in
this critique; it belongs after implementation and validation. If that later
Review is Not accepted, preserve it, freeze locally and stop for coordinator
routing without a second/amended Review or self-Pass.
