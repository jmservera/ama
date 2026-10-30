<!-- markdownlint-disable-file -->
# RPI Plan Critique: resident-live-acceptance

## Metadata

* Task ID: resident-live-acceptance-2026-10-30
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/resident-live-acceptance-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/resident-live-acceptance-phase-details.md
* Critique execution status: Complete
* Original outcome: Revise. Preserve this original assessment after corrections.

## Inputs and Criterion Boundary

* Read only the supplied research, plan and phase details, plus the activated
  skill's critique template. No optional application sources were necessary.
* Research: .copilot-tracking/research/2026-10-30/resident-live-acceptance-research.md.
* Caller direction: resident-only authenticated Playwright acceptance on the
  named ca-resident-demo origin; real CSRF form; trimmed credentials read
  inside automation only; no credential disclosure, recording, Azure access
  or secret inspection; at most two attempts and immediate first-401 stop.
* Assessed AC-01 through AC-04, C1-C7/W1-W4 as represented in Research,
  P01-T01 through P02-T03, dependencies, change budget, validation ownership,
  exact-script fingerprinting, local-only Refs commit and external gate.
* All 19 compound issue criteria must remain proven or unmet, including
  employee obligations that resident-shell observations cannot accept.
* This is the single final-candidate critique, not implementation, live
  acceptance, source verification or a second assessment of historical work.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC-01; P01-T01; C4-C5 | Covered | Actual form/CSRF machinery, one planned attempt, two-attempt ceiling, generic 401 and immediate stop are explicit. |
| Credential protection; P01-T01 | Covered | In-automation trimming, masked inputs, no raw errors, no recordings or exports, allowlisted output and finally cleanup are specified. |
| Runtime dependency; P01-T01 | Partial | PC-001: selected runtime is in a prohibited temporary directory. |
| AC-02; W1-W3; P02-T01 | Partial | PC-002: counts and IDs exist, but the exact compound requirements are absent from the supplied inputs. |
| AC-03; P01-T02 | Partial | PC-003: pre-consent negative testing assumes the authenticated identity starts unconsented. |
| Chat interaction and relevance; P01-T02 | Covered | Persistent thread/composer, Enter, Shift+Enter, Send, labels/sources, selector limitation, rat relevance and honest fallback are included. |
| Accessibility basics; C6-C7; P01-T02 | Covered | Keyboard/focus, three widths, overflow, polite updates and reduced motion are scoped without full conformance claims. |
| Employee boundaries; AC-02; P02-T01 | Covered | #551/#552 and the employee selector are not accepted from resident shell evidence; historical source coverage is distinguished. |
| Change budget and validation ownership | Covered | Maximum additions, no removals, script/JSON ownership, syntax, before/after fingerprint, secret exclusion, matrix, diff and independent Review are specified. |
| AC-04; P02-T02-T03 | Covered | Original independent Review, local Refs-only commit, no push, privacy-safe identity and blocking external gate are explicit. |

## Verdict

* Verdict: Revise.
* Rationale: The bounded acceptance approach is credible, but the runtime
  contradicts an explicit execution restriction, the complete criterion
  boundary is not reproducible from the supplied evidence, and consent
  testing needs a safe branch for an already-consented identity. These are
  direct planner corrections, not reasons to broaden access or request secrets.
* Severity counts: Critical 0; High 1; Medium 2; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Replace the prohibited temporary-directory runtime

* Related IDs: Research Wave 2; plan Non-Functional Requirements; P01-T01.
* Evidence: .copilot-tracking/research/2026-10-30/resident-live-acceptance-research.md
  selects an existing temporary-directory runtime;
  .copilot-tracking/plans/2026-10-30/resident-live-acceptance-plan.md and
  .copilot-tracking/details/2026-10-30/resident-live-acceptance-phase-details.md
  prescribe executing it. Current execution instructions prohibit any file
  operations in temporary directories, not merely storing final evidence there.
* Concern: The first implementation task requires reading/executing files
  from a prohibited location.
* Impact: Implementation cannot follow the candidate literally within the
  current execution constraints.
* Smallest useful change: Select and verify a non-temporary runtime. If the
  chosen interpreter reports a missing dependency, use a permitted
  project-relative environment and explicitly account for its ignored
  generated files and gate implications; do not copy/read the prohibited
  runtime. If no permitted runtime is available, record an execution blocker.
* Action owner: Planning parent.
* Exact resolving evidence: Revised plan and P01-T01 identify the permitted
  interpreter and dependency check or explicit blocked path; any environment
  additions are reconciled with the change budget and validation input rules.
* Decision route: Direct planner correction. No user decision is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Make all compound acceptance requirements available before testing

* Related IDs: AC-02; W1-W3; P02-T01; 550-01..09; 551-01..04; 552-01..06.
* Evidence: .copilot-tracking/research/2026-10-30/resident-live-acceptance-research.md
  records issue URLs, counts and high-level summaries, not the 19 compound
  definitions. The plan calls these the exact criteria in Research, while
  P02-T01 first instructs writing them during evidence reconciliation.
* Concern: Neither this critique nor an implementer restricted to these
  inputs can trace every required subpart to a planned observation. A
  19-row count alone cannot show that a faithful summary retained every
  obligation.
* Impact: A partial criterion could be reported Proven, or a required
  observation could be discovered only after the bounded browser run.
* Smallest useful change: Before live execution, persist the exact retrieved
  definitions or complete faithful compound summaries within an existing
  owned artifact. Map each subpart to its planned observation or explicit
  unmet/out-of-resident-scope boundary. If the previously retrieved text is
  unavailable, record that evidence gap and prohibit a whole-criterion
  Proven verdict until its definition is established.
* Action owner: Planning parent.
* Exact resolving evidence: An ordered 19-entry requirements baseline with
  source/date, all compound subparts, observation ownership and the rule that
  any required unproven subpart keeps the whole criterion Unmet. Employee
  #551/#552 obligations remain unmet from this resident-only run.
* Decision route: Direct planner correction using already-authorized issue
  evidence, not an instruction for this critique to retrieve anything.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Branch consent testing on the observed initial consent state

* Related IDs: AC-03; P01-T02; resident consent before assistant requests.
* Evidence: .copilot-tracking/details/2026-10-30/resident-live-acceptance-phase-details.md
  instructs trying a question before granting permission and establishing
  that no assistant POST occurs. No supplied evidence establishes the
  account's initial consent state or that an ephemeral browser resets
  server-side consent.
* Concern: An already-consented identity can legitimately send a request at
  this step. That would not test pre-consent enforcement and must not be
  misclassified as a consent defect or proof of the negative boundary.
* Impact: The consent result can be misleading, and the intended no-request
  negative test can issue an actual assistant request unexpectedly.
* Smallest useful change: Inspect only the necessary consent-control state
  before submitting any question. Run the negative test only when the UI
  establishes an unconsented state. If already consented, record that
  initial state and mark the pre-consent transition unproven unless a normal,
  explicitly authorized reset path is established; do not invent a fresh
  state, manipulate backend consent or treat existing consent as a defect.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T02 contains explicit initially-unconsented,
  initially-consented and indeterminate branches; the JSON/matrix records
  initial state, observed request ordering and unmet transition coverage
  without retaining resident records or identity.
* Decision route: Direct planner correction. Current scope already permits
  honest unmet results, so no additional user decision is required.

## Strengths and Residual Risk

* The immediate 401 stop is stronger than the two-attempt ceiling; generic
  denial is not diagnosed as a password, domain or account problem.
* No secret repair, Azure work, employee authentication, fake AI responses,
  product fixes, screenshots or remote publication is authorized.
* The plan preserves original adverse outcomes, requires direct applicable
  evidence and does not convert basic checks into accessibility acceptance.
* Deployment parity, account eligibility, AI response availability and
  employee-surface acceptance remain explicitly unresolved. A blocked login
  is an honest bounded outcome, not authenticated-feature acceptance.
* Independent Review and the local gate do not establish human approval.

## Questions or Blocking Evidence Gaps

* No new user question is required. The planning parent owns all three
  corrections.
* Exact compound definitions are missing from the supplied assessment
  boundary; this limits requirement-level assurance, not permission for the
  bounded real-form attempt after planner reconciliation.

## Limitations

* No browser request, credential/private-file access, GitHub retrieval,
  application-source inspection, runtime probe or implementation occurred.
* Referenced issue bodies, historical Review, guidelines and regulatory or
  accessibility sources were considered only as summarized in Research.
* Only this critique artifact was written. No other source or outcome was
  changed. This complete finding set is not a request for another critique.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Replace the prohibited runtime, then reconcile
  PC-002 and PC-003 directly in the existing plan/details before execution.
* User response required: No.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/research/2026-10-30/resident-live-acceptance-research.md | Supplied evidence summary and research boundary. |
| .copilot-tracking/plans/2026-10-30/resident-live-acceptance-plan.md | Final-candidate requirements, budget and validation. |
| .copilot-tracking/details/2026-10-30/resident-live-acceptance-phase-details.md | Task-level execution and evidence instructions. |
| .copilot-tracking/plans/2026-10-30/resident-live-acceptance-critique.md | Original independent critique and complete finding set. |

## Next Steps

The active planning parent should resolve PC-001 through PC-003 directly,
preserve this original Revise outcome, and finalize without another critique.
No user action or implementation by this critic is required.
