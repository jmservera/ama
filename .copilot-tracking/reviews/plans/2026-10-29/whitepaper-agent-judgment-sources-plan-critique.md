<!-- markdownlint-disable-file -->
# RPI Plan Critique: whitepaper-agent-judgment-sources

## Metadata

* Task ID: whitepaper-agent-judgment-sources
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/whitepaper-agent-judgment-sources-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/whitepaper-agent-judgment-sources-phase-details.md
* Critique execution status: Complete
* Assessment mode: independent plan review, not manuscript revision or scientific certification.

## Inputs and Criterion Boundary

* Read the complete supplied plan, phase details and research:
  .copilot-tracking/research/2026-10-29/whitepaper-agent-judgment-sources-research.md.
* Read docs/reference/method/scientific-paper-writing-and-review.md and the
  rpi-plan-critique template.
* Fixed owner decisions: bounded source integration and method clarity; full
  RPI; local docs(paper) commits with required trailer; no push, az, secrets
  or .env access; ASCII punctuation; no test additions or removals; PDF
  generation only with a preexisting local toolchain. This critique does not
  reopen those decisions.
* Assessed requirements, W1-W6 and C1-C4, adopted/deferred exemplar lessons,
  both phases, all four tasks, dependencies, acceptance criteria, risk and
  follow-up disposition once across the supplied boundary.
* Evidence state: the research report itself was inspected. Its accounts of
  manuscript passages and primary-source support are parent-supplied,
  unchecked in this critique. The caller confirms that the parent fully read
  both sources. No duplicate external research was needed or performed.
* Only this critique artifact is authorized for writing. No plan, manuscript,
  bibliography, historical critique, source guide, code or state was changed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| W1-W2; discussion requirement | Covered | Research separates 50 agent users from 61 recruits, four analytical choices from all decisions, induced preferences from ordinary deployment, and proposed safeguards from evaluated remedies. |
| W3, W6; background requirement | Covered | Matched representation comparison, uncertain skill-versus-raw contrast and token-cost qualification prevent a general skills-benefit or instructions-harm claim. |
| W4; learning/validity requirement | Covered | Retrieval, availability, use and outcomes remain distinct; absent AMA traces do not establish a mechanism. |
| W5; exemplar adoption; P01-T01 | Covered | Local operational definitions and selective interpretation are distinguished from the exemplar's sampled coding, matched trajectories and human checks; independent audit remains unperformed. |
| Source identity; P01-T01 and P01-T02 | Covered | Primary Anthropic page versus unread linked PDF, arXiv v1/preprint identity, genuine section locators, retrieval date, matching bibliographies and a durable claim ledger are specified. |
| Pilot, historical critique and surgical scope | Covered | Abstract, case observations/counts, pilot arms/sample/budgets, protocol, figures, tools/tests, bundle and historical critique are explicitly protected. |
| Dependencies and validation ownership; P02-T01 | Covered | Task prerequisites, existing checker/tests, zero test changes, ASCII and semantic/diff checks are specified without inventing validation outcomes. |
| Conditional PDF generation and preservation acceptance criterion | Partial | PC-002: conditional build authority conflicts with unconditional PDF preservation. |
| Independent final Review and completion; P02-T02 | Partial | PC-001: findings are routed onward without a defined effect on the current candidate's assessment status. |
| Local commits, no remote mutation and publication boundary | Covered | Commit prefix/trailer, bounded staging and no-push/no-az restrictions are explicit; full publication approval is separate. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 1; Medium 1; Low 0.
* Rationale: The scientific integration is credibly scoped. Two direct
  corrections are needed to make validation and closeout consistent with
  those boundaries. Neither requires new research, a study redesign, a
  second critique or a new owner decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Define the completion consequence of unresolved final-review findings

* Related IDs: P02-T02; acceptance criteria for source support, preservation
  and independent Review.
* Evidence: phase details, P02-T02, says findings route to authors or a later
  task, not a repeated review loop. The plan's Acceptance Criteria requires
  an independently reviewed, locally committed candidate, but neither
  document specifies the disposition of a final-review finding that a new
  claim is unsupported or a protected study boundary was changed.
* Concern: The current routing can defer a material integrity defect without
  explicitly preventing the scoped revision from being reported as accepted.
  Retaining a review artifact and passing structural tests do not establish
  scientific support. This is a missing gate consequence, not evidence that
  an actual manuscript defect exists.
* Impact: An unsupported attribution or altered pilot fact could survive
  closeout under a completion summary that obscures the unresolved issue.
* Smallest useful change: State that the single final Review reports
  execution separately from assessment. Any unresolved source-support,
  fabricated-method, protected-scope or required-validation failure must
  leave candidate assessment non-passing and be named in the final summary.
  If findings are intentionally deferred, retain the evidence and local
  commits as authorized but do not describe the candidate as accepted or
  publication-ready. Optional preferences may be deferred with rationale.
  No repeated independent review is required.
* Action owner: Planning parent; implementation parent applies the closeout rule.
* Exact resolving evidence: P02-T02 and the acceptance/closeout wording
  explicitly define non-passing disposition for unresolved material findings.
  At execution, the final review and summary list each material finding's
  applied correction or unresolved disposition, with actual evidence locators.
* Decision route: Direct planner correction. No user decision is required;
  this implements the fixed scientific-integrity and single-review boundaries.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Make the PDF preservation criterion conditional

* Related IDs: P02-T01; Scope and Non-Goals; Acceptance Criteria; Locked
  Validation Ownership.
* Evidence: the plan's Acceptance Criteria requires the PDF to be unchanged,
  and Scope and Non-Goals does not include it among canonical targets.
  Locked Validation Ownership permits generated main.pdf with an existing
  documented local TeX toolchain. Phase details P02-T01 requires keeping the
  tracked PDF unchanged specifically when no build occurs.
* Concern: Discovery of the permitted preexisting compiler makes the authorized
  build and unconditional preservation criterion incompatible.
* Impact: The implementer could either reject an authorized generated update
  or claim that a changed PDF satisfies an unchanged-PDF criterion.
* Smallest useful change: Define two explicit branches: without an eligible
  existing toolchain, preserve the PDF and report no build/log/layout check;
  with one, allow only the corresponding main.pdf generated update, record
  the exact command and outcome, and report which log/layout checks actually
  ran. Keep figures, bundle, tools/tests and other protected files frozen.
  Align the scope exception and acceptance criterion with these branches.
* Action owner: Planning parent.
* Exact resolving evidence: Consistent conditional PDF wording in Scope,
  Acceptance Criteria and P02-T01. Execution evidence must subsequently show
  either the unchanged tracked PDF and no-build limitation or the authorized
  generated PDF diff and actual build/check results.
* Decision route: Direct planner correction. The owner already authorized
  only conditional generation with a preexisting toolchain.

## Strengths and Residual Risk

* The proposal adopts explanatory clarity rather than borrowing performed
  methods: no fabricated coding, inter-rater agreement, ablations or pilot
  results are authorized.
* The research retains counterevidence and exemplar reporting qualifications,
  including the no-hint qualification and confounded framework/model changes.
  It does not treat the exemplar as blanket methodological certification.
* The original critique remains historical evidence, not fresh approval.
* No broader source audit or new empirical work is promised. Independent
  O1-O5 assignment audit, meaningful human judgment, source interpretation
  and publication decisions remain author responsibilities.
* A missing compiler and the no-az publication-gate constraint may leave
  generation or publication validation unperformed. Recording those limits
  is appropriate; neither justifies installation or prohibited execution.
* Venue rules were not supplied or assessed. This is generic scientific
  integrity advice, not a venue-compliance determination.

## Questions or Blocking Evidence Gaps

* No owner question or decision-critical research gap blocks this plan
  critique. Both findings can be corrected directly within fixed decisions.

## Limitations

* The manuscript, checker/tests and source snapshots were not independently
  reread or executed. This assessment tests the plan against supplied
  evidence, not the truth of every source claim or the final manuscript.
* Parent-reported full-text coverage is not relabeled as this critic's own
  primary-source verification. The planned final Review must assess the
  actual edits and ledger, not merely inherit a plan-level assessment.
* This assisted critique is not independent human peer review, statistical
  review, ethics certification or author approval.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the explicit unresolved-material-finding
  closeout rule and align the conditional PDF exception, then finalize the
  plan without another critique.
* User response required: No.
* Work execution: Complete. Assessment status: Revise; scientific source
  support remains parent-reported rather than independently reverified here.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/whitepaper-agent-judgment-sources-plan.md](.copilot-tracking/plans/2026-10-29/whitepaper-agent-judgment-sources-plan.md) | Reviewed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/whitepaper-agent-judgment-sources-phase-details.md](.copilot-tracking/details/2026-10-29/whitepaper-agent-judgment-sources-phase-details.md) | Reviewed implementation and validation details |
| [.copilot-tracking/research/2026-10-29/whitepaper-agent-judgment-sources-research.md](.copilot-tracking/research/2026-10-29/whitepaper-agent-judgment-sources-research.md) | Supplied evidence and adoption boundaries |
| [.copilot-tracking/reviews/plans/2026-10-29/whitepaper-agent-judgment-sources-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/whitepaper-agent-judgment-sources-plan-critique.md) | This single independent critique |

## Next Steps

The active planning parent should resolve PC-001 and PC-002 directly and
finalize without another critique. No user action is required. This reviewer
stops after the authorized critique artifact.
