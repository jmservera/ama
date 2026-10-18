<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue 87 appointment commitment controls

## Metadata

* Task ID: 87; parent: 81.
* Critique date: 2026-10-18.
* Plan: .copilot-tracking/plans/2026-10-18/issue-87-appointment-controls-plan.md.
* Phase details: .copilot-tracking/details/2026-10-18/issue-87-appointment-controls-phase-details.md.
* Branch: feat/appointment-commitment-controls-87.
* Confirmed source HEAD/base: 99056cae7bc679d2ace3e42c75f28577cfce8887.
* Critique execution status: Complete.
* Execution boundary: exactly one final-candidate critique; no implementation,
  source fixes, plan edits, original Review or repeated critique.

## Inputs and Criterion Boundary

* Caller requirements: full ordered Research -> Plan plus one critique ->
  delegated Implement -> one immutable original Review. Coordinator does not
  implement source. This assessment stops at the requested critique artifact.
* Supplied research:
  .copilot-tracking/research/2026-10-18/issue-87-appointment-controls-research.md,
  including C1-C10/W1-W3, and
  .copilot-tracking/research/2026-10-18/subagents/issue-87-current-code-evidence.md.
* Requirement evidence checked at supplied pointers:
  docs/prds/zava-forward-retrofit-programme-demonstrator.md,
  DD-006, FR-031, FR-048, AC-033, AC-062, AC-064 and AC-065;
  docs/brds/agentic-retrofit-programme-brd.md,
  FR-045/046, AC-087/088, RULE-006/AC-025 and RULE-007;
  docs/case_study_48_addendum.md, Missed-Appointment Escalation Evidence
  (2026-10-04), especially lines 411-425.
* Repository context: unchanged original case study, addendum context,
  knowledge-base index, owner memory as context only, and housing-association
  primer. No new regulatory claim or operational approval is assessed.
* Four issue-criterion families: tri-party evidenced commitment; bundles cannot
  delay urgent safety; household constraints/options/deferral/pause/update owner;
  configurable provisional default five with strictly greater-than eligible
  no-access count producing human investigation only.
* Dependencies: retain merged #90/#384 quota/source/delegation/coverage/period
  controls and #88, #85, #91, #102, #101 and #117 contracts. Exclude unmerged
  #92/#389 and any invented blanket legal hold.
* Cross-cutting boundary: separate appointment-specific representative authority
  from works consent/attendance; legacy Booked remains historical/unverified;
  server-side binding, selective invalidation, direct domain/HTTP/completion/
  advance checks, durable concurrency/dedup/audit and truthful post-COMMIT results.
* Required future evidence: actual local SQL Server, real local browser with
  keyboard/offer-versus-commitment/Unknown/denials/reflow, and source-context
  nonroot hardened Docker. No real communication, booking, allocation,
  diagnoses, legal/financial approval or private datasets.
* Assessment scope: planning completeness, feasibility, support in supplied
  evidence, test ownership and policy boundaries. Source behavior is assessed
  through the supplied inventory, not a fresh source audit or execution.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Issue AC1; F2/F3; P01-T01 | Covered | Explicit resident/appointment-representative and staff provenance plus current #90 committed capacity; bounded appointment authority is separate from works/attendance. |
| Legacy Booked; direct domain/HTTP/completion/advance | Covered | Historical records cannot confer commitment; server-derived reads and consequential writes require current dependencies. |
| Capacity source/quota/delegation/coverage/period; C5-C7 | Covered | Existing guards and transaction-time revalidation are retained, not replaced by visit allocation. |
| Selective invalidation and sibling isolation | Covered | Details distinguish date/option/bundle/scope, capacity and authority dependencies; unrelated resident decisions remain intact. |
| Issue AC2; F4; P01-T01/P03-T01 | Covered | Explicit bundle agreement and competence evidence; urgent hazard service remains independent of routine gates. |
| Issue AC3; F1; P01-T01/P02-T01 | Covered | Household options/constraints/pause/deferral and named #88 update owner persist with minimum-necessary provider projection. |
| FR-048/AC-065; F7; P01-T02/P02-T01/P03-T01 | Partial | Cause/owner counts are named, but preference-breach and abortive-visit capture, projection and explicit acceptance evidence are unspecified. PC-002. |
| Issue AC4; FR-031/AC-033; RULE-006 | Partial | Default five, strict greater-than, exclusions and immutable event/configuration history are supported; counting/reset case identity is changed or ambiguous. PC-001. |
| Human investigation and corrective action; RULE-006/AC-025 | Partial | Owner/action/update are planned; prerequisite checks and distinction between investigation disposition and source-authorized case closure need an explicit contract. PC-001. |
| P01-T02 durable outcome semantics | Covered subject to PC-001 | Retry/conflicting-reference rules, configuration-independent dedup, optimistic concurrency, audit rollback and truthful committed responses are explicit. |
| P02-T01 authorization, privacy and UI | Covered | Native controls, manual route, visible missing/stale/Unknown states, provider/unknown/revoked actor denials and no sending. |
| P03-T01 local SQL/browser/container | Covered | Actual owned loopback MSSQL races/recovery and hardened nonroot source image are mandatory; missing/failed evidence withholds correctness acceptance. |
| Test ownership and removals | Covered | No removals; retain adjacent assertions; at most two focused test modules and one browser check; no fixture dumps or arbitrary count targets. |
| P03-T02 documentation and ordered RPI | Covered | Existing guides/synthesis/index/log, exact receipts, one immutable independent Review, separate correction receipts and normal gated PR flow. |
| Policy and dependency exclusions | Covered | No automatic consequence, urgent delay, live action, diagnoses, invented reporting threshold, #92/#389 import or blanket hold. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.
* Rationale: The candidate provides credible source seams, bounded scope and
  mandatory engineering gates. It nevertheless substitutes or conflates an
  investigation lifecycle for the source's same-active-case counting boundary.
  The parent must resolve that before implementation. Explicit preference-breach
  and abortive-visit acceptance coverage is also needed. These are planner-owned
  corrections, not requests for new operational policy or a second critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Investigation lifecycle is not established as the source-authorized counting and reset case

* Related IDs: issue AC4; F5/F6; plan AC4; P01-T02; P02-T01; P03-T01;
  research C2-C4; PRD DD-006/FR-031/AC-033; BRD RULE-006/AC-025.
* Evidence:
  .copilot-tracking/plans/2026-10-18/issue-87-appointment-controls-plan.md:90-98
  counts events "during active investigation lifecycle," while the investigation
  is created only after the threshold.
  .copilot-tracking/details/2026-10-18/issue-87-appointment-controls-phase-details.md:59-81
  instructs an "active investigation case/cycle," excludes inactive events, and
  provides human closure/reset without defining the counted case identity.
  The parent research's Findings, Alternatives and Decisions similarly asserts
  closure of an active investigation case and a new investigation cycle.
  In contrast, docs/case_study_48_addendum.md:411-425 and BRD RULE-006 require
  counting while the same case remains active, resetting only when a human
  closes that case, and explicitly leave operational lifecycle ratification open.
* Concern: No supplied evidence equates the threshold-created investigation task
  with the case whose earlier appointments accumulate. Literal implementation
  can either exclude events one through five because no investigation yet exists,
  or reset the count whenever an investigation task is disposed while the same
  underlying case remains active. Calling closure "human" alone does not resolve
  this distinction. Nor is there a source-backed definition of reopening or
  a new cycle in the candidate.
* Impact: The sixth eligible event can fail to trigger, or repeated task closures
  can suppress further investigation despite continuing eligible events in the
  same active case. The plan's current 4/5/6 and reset tests could pass against
  this invented lifecycle rather than the required one.
* Smallest useful change: Replace investigation-lifecycle counting with an
  explicit source-traceable same-case contract in F5/F6 and P01-T02. Specify the
  counted case identity, active-state evidence, initial counting before any
  investigation exists, authorized human closure boundary and treatment of
  subsequent/reopened activity. Distinguish task disposition, appointment/order
  completion, pause, remedy closure and genuine counted-case closure; none may
  reset merely by implication. Keep any genuinely unverified lifecycle detail
  Unknown/fail-closed rather than introducing an easier reset. Include the
  RULE-006/AC-025 human checks of confirmation, notice, attendance, accessibility/
  adjustments, contact history and relevant circumstances, with sourced or
  explicit Unknown evidence, corrective action and next update. These are
  recorded human checks, not automated cause classification or diagnosis.
* Action owner: Planning parent, reconciling its research interpretation into
  the plan/details before delegating source implementation.
* Exact resolving evidence: Revised plan/details cite the exact source wording
  and define one unambiguous case/count/reset state table. Acceptance cases must
  show events one through five count with no investigation task, event six
  creates one owned investigation, task disposition and routine order/appointment/
  pause/update/remedy changes preserve the same active-case count, and only the
  explicitly authorized human closure resets that counter while all events and
  configuration history remain. Specify an actual SQL concurrent closure/event
  assertion and a replay-after-closure assertion proving old events are not
  counted again. No future result is claimed at planning time.
* Decision route: Direct planner correction. Current caller direction already
  rejects an invented easy-reset lifecycle. If the supplied sources cannot
  establish a proposed new reset transition, omit that transition or mark it
  unresolved rather than treating critique advice as operational authorization.
  No significant or divergent user decision is presently necessary.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Preference-breach and abortive-visit counts lack an executable acceptance path

* Related IDs: FR-048/AC-065; BRD FR-046/AC-088; F7; P01-T02;
  P02-T01; P03-T01.
* Evidence:
  .copilot-tracking/plans/2026-10-18/issue-87-appointment-controls-plan.md:99-100
  names breach/abortive cause-and-owner counts, but its AC1-7 do not explicitly
  verify those counts.
  .copilot-tracking/details/2026-10-18/issue-87-appointment-controls-phase-details.md:61-72
  defines outcome provenance and mentions cause/owner counts without defining how
  a preference breach or abortive visit is captured or distinguished.
  P02-T01 offers generic owned outcomes; P03-T01 supplies general appointment
  semantics rather than a specific count/projection assertion.
  PRD AC-065 expressly requires preference breaches and abortive visits counted
  by cause and owner with reporting thresholds Unknown until supplied.
* Concern: A cause breakdown of no-access/provider outcomes alone cannot prove a
  preference breach or abortive visit was recorded and counted. For example, a
  confirmed visit may breach an agreed household constraint without being
  resident no-access. The present task descriptions can be satisfied without
  implementing that distinct part of F7.
* Impact: Household disruption can remain invisible in the accepted output, or
  be incorrectly added to the resident no-access investigation counter.
* Smallest useful change: Add the minimum explicit record-only representation
  and authorized recording/read projection for preference-breach and abortive-
  visit facts, cause/owner and Unknowns. Map them to a visible cause/owner count
  and an explicit AC/test selector. State whether one visit can have both facts
  and how retries avoid duplicate counts; do not invent a reporting threshold,
  automatic consequence or live control-meeting workflow.
* Action owner: Planning parent for P01-T02/P02-T01/P03-T01 and acceptance mapping.
* Exact resolving evidence: Revised details and acceptance matrix include a
  preference breach without no-access, a provider-caused abortive visit, any
  declared overlap case, duplicate retry, persistence/reload and authorized
  cause/owner projection. Expected assertions show correct separate counts,
  reporting threshold Unknown, and no increment of resident eligible no-access
  unless that event independently meets the confirmed/verified definition.
  Keep all tests inside the declared two-module/one-browser maximum.
* Decision route: Direct planner correction; already required by F7 and the
  cited accepted sources. No significant or divergent user decision.

## Strengths and Residual Risk

* The research explicitly rejects the lane's possible works-authority reuse;
  the candidate preserves distinct bounded appointment authority and works
  consent. This is an important evidence-backed boundary, not a missing feature.
* Current contractor capacity remains an evidenced home/work-order quota, not a
  fabricated crew/weekly visit slot. Existing source, delegation, coverage,
  period and quota checks remain cumulative.
* Legacy Booked is preserved as historical/unverified, and commitment is derived
  server-side at both readers and consequential writers.
* Scope/capacity/authority invalidation is selective; adjacent #88 commitments,
  remedies and hazard response are not silently cleared.
* Actual SQL concurrency/recovery, browser and hardened source-image validation
  are explicit gates, not optional receipts or substituted inherited results.
* The test addition budget and no-removals rule are workable with the existing
  procurement/resident/API suites and browser seam identified by the lane.
* Live authority, household evidence, competence, supplier commitments and policy
  ratification remain unavailable human prerequisites. Synthetic engineering
  may proceed after planning correction; it does not establish operational
  readiness, legal approval or WCAG conformance.

## Questions or Blocking Evidence Gaps

* No user question is needed for these corrections.
* PC-001 identifies an unsupported lifecycle equivalence, not permission to
  choose a new operational lifecycle. The parent must make the plan faithful
  to the supplied rule before implementation.
* Actual SQL/browser/container evidence is intentionally future work. Its
  absence does not block this planning assessment, but must block a later
  correctness pass if still absent.

## Limitations

* This is a plan critique, not source Review, security assessment or acceptance.
* The supplied current-code lane is evidence of inventory and historical test
  seams, not fresh execution. No tests, browser, Docker or SQL were run here.
* GitHub dependency status is taken from supplied research; no new external
  research, regulatory-currentness check or operational policy decision occurred.
* Existing untracked planning/research/state artifacts were left untouched.
  Only this caller-authorized critique artifact was written.
* All actionable concerns found within the supplied boundary are returned here
  together; there is no withheld finding set or proposed second critique.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Correct the counted-case identity and closure/reset
  contract, then disposition PC-002 in the same plan/details revision.
* User response required: No.
* After disposition: Finalize planning without another critique; delegate source
  implementation and retain the required later single independent original
  Review. This critique does not invoke either stage.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-18/issue-87-appointment-controls-research.md](.copilot-tracking/research/2026-10-18/issue-87-appointment-controls-research.md) | Supplied parent research and requirement provenance |
| [.copilot-tracking/research/2026-10-18/subagents/issue-87-current-code-evidence.md](.copilot-tracking/research/2026-10-18/subagents/issue-87-current-code-evidence.md) | Supplied source and validation-seam inventory |
| [.copilot-tracking/plans/2026-10-18/issue-87-appointment-controls-plan.md](.copilot-tracking/plans/2026-10-18/issue-87-appointment-controls-plan.md) | Assessed final-candidate plan, unchanged |
| [.copilot-tracking/details/2026-10-18/issue-87-appointment-controls-phase-details.md](.copilot-tracking/details/2026-10-18/issue-87-appointment-controls-phase-details.md) | Assessed phase details, unchanged |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-87-appointment-controls-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-87-appointment-controls-plan-critique.md) | This single Complete critique; verdict Revise |

## Next Steps

Planning parent resolves PC-001 and PC-002 directly, records their disposition,
and finalizes without another critique. No user action is required. Stop here:
no source implementation or original Review is performed by this assessment.
