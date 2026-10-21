<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-223-human-review-protocol

## Metadata

* Task ID: issue-223-human-review-protocol
* Critique date: 2026-10-21
* Plan: .copilot-tracking/plans/2026-10-21/issue-223-human-review-protocol-plan.md
* Phase details: .copilot-tracking/details/2026-10-21/issue-223-human-review-protocol-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: GitHub issue #223 (seeded critical defects detected and blocked; reviewer, source and reason retained; detection, corrections and total review effort versus same workflow-only scenarios; default acceptance and citation validity alone cannot pass; automation-bias test; OQ-017 reviewer authority and evidence). Owner constraints: preparation only (issuecomment-6290697705 on #126); no participants, execution, model calls, code, #222 manifest edits, PRD/ADR/case study/memory edits; thresholds, samples and roles PROPOSED/UNFILLED; outcomes NOT RUN; #108 dependency recorded, not removed; placement in src/agents/README.md plus index and append-only log.
* Research and evidence considered: .copilot-tracking/research/2026-10-21/issue-223-human-review-protocol-research.md; src/agents/README.md headings (lines 253-324); docs/reference/README.md index rows; docs/reference/log.md tail and heading format; src/api/README.md staff comprehension protocol (line 2607).
* Decisions, dependencies, and acceptance criteria considered: plan Functional Requirements FR-A to FR-F, Acceptance Criteria, P01 to P03, Follow-Up Items; #108 open, #222 unapproved, #106 closed partial.
* Assessment boundary: plan soundness and completeness against the supplied evidence only. GitHub issue text and the PRD were not re-read; their content is taken from the research citations (C1 to C12). No section text exists yet, so only the plan's intent can be judged.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| #223 criterion: seeded critical defects detected and blocked | Partial | FR-A lists classes; FR-F has only "pass/fail/insufficient/not run" with no rule content (PC-002, PC-004) |
| #223 criterion: reviewer, source, reason retained | Partial | FR-C lists fields; C7 covers reviewer_action/reason only; effort and reviewer-cited source absent; identity versus anonymity conflict (PC-005) |
| #223 criterion: detection, corrections, total effort vs workflow-only | Partial | FR-E names effort components; no pairing, counterbalancing or dependence on #222 scenarios stated (PC-003) |
| #223 criterion: default acceptance and citation validity alone cannot pass | Partial | FR-B names controls; no rule that an always-accept or citation-only baseline must fail (PC-002) |
| #223 criterion: automation-bias test | Partial | FR-B parenthetical only; no arm design, order or prevalence control (PC-004) |
| OQ-017 authority and evidence | Covered with gap | FR-D all UNFILLED; no separation of seeder, reviewer, scorer, approver or per-class domain competence (PC-006) |
| Placement (README, index, log) | Covered with gaps | Sound choice (C6, C9, C11); heading level, anchor, log type and index row form unspecified (PC-007) |
| Owner constraints and non-claims | Covered | Executive summary and requirements preserve them; #108 kept as open dependency |
| P03 validation and exit | Partial | Test command unnamed; critique disposition and log wording sequencing (PC-008) |

## Verdict

* Verdict: Revise
* Rationale: The placement, scope and owner-constraint handling are credible. The plan is, however, a topic list rather than a testable protocol specification: it never states the decision rules, comparator pairing, automation-bias design or evidence dependencies that make each #223 criterion verifiable, and its acceptance criteria ("every label") are not checkable. All findings are planner-owned corrections except one retention policy item that needs an owner or privacy decision recorded as UNFILLED.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: No criterion-to-section traceability; acceptance criteria are not checkable

* Related IDs: Acceptance Criteria, P01-T02, P03-T01, all FR
* Evidence: .copilot-tracking/plans/2026-10-21/issue-223-human-review-protocol-plan.md (Acceptance Criteria: "Section exists with every label"); .copilot-tracking/details/2026-10-21/issue-223-human-review-protocol-phase-details.md (P01-T02 content list)
* Concern: "Every label" and "issue criteria unchanged" are undefined, so a reviewer cannot tell whether the section satisfies #223 preparation. No mapping ties each #223 criterion and OQ-017 to a named subsection and its NOT RUN status.
* Impact: Completeness and the "no criterion ticked" claim cannot be independently verified.
* Smallest useful change: Add to the plan and to P01-T02 a required traceability table in the README section (one row per #223 criterion and OQ-017: subsection, PROPOSED/UNFILLED items, status NOT RUN) and rewrite acceptance as a checklist of those rows plus a grep-able list of required labels.
* Action owner: planning parent
* Exact resolving evidence: Revised plan acceptance criteria and P01-T02 that enumerate the six criteria and OQ-017 with target subsection names; final diff shows the table.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Blocking and pass rules, and the "default acceptance / citation validity alone cannot pass" test, are unspecified

* Related IDs: FR-B, FR-F, C1, C2, C8
* Evidence: plan FR-B and FR-F; research C1, C2, C8 (citation validity is lexical, claim grounding unproven)
* Concern: FR-F gives only outcome labels. Nothing states that an always-accept reviewer and a citation-validity-only checker are run as baselines and must fail; that a disposition counts as a detection only when the reason is source-grounded and checked against the frozen key; or that any undetected valid-citation-wrong seeded defect blocks (NFR-009, C5). Rubber-stamp signals (very short review time, boilerplate reason) are not defined.
* Impact: The central #223 criterion could be met by a protocol that rewards default acceptance.
* Smallest useful change: In FR-F and P01-T02 require: (a) per-case detection scored on disposition plus source-grounded reason against a frozen key; (b) zero undetected critical seeded defects as a PROPOSED blocking rule; (c) mandatory always-accept and citation-only negative-control arms that must be shown to fail; (d) PROPOSED rubber-stamp indicators; (e) rule that insufficient evidence means not passed.
* Action owner: planning parent
* Exact resolving evidence: Revised FR-F and P01-T02 listing (a) to (e) with PROPOSED labels and no numbers asserted as approved.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Workflow-only comparator and effort measurement lack pairing, order and #222 dependency definition

* Related IDs: FR-E, C5, #222, #108
* Evidence: plan FR-E and Follow-Up Items; research C5 (pair AI-assisted and workflow-only runs), counter-evidence that no effort field is built
* Concern: The plan lists effort components but not: same scenarios per arm (sourced from the #222 manifest, which is unapproved and may not be edited here); how a reviewer seeing the same scenario in both arms is counterbalanced or separated by a washout; clock start and stop rules; that corrections are counted both as detections and as rework effort; or that effort capture is a protocol definition, not a built metric (the research notes it).
* Impact: A later evaluation could not compare total effort fairly, or could depend on scenario definitions this work must not create.
* Smallest useful change: Specify in FR-E and P01-T02 that scenario identity and cohort labels are inputs from the approved #222 manifest and are UNFILLED here; state the pairing, counterbalancing, clock boundaries and unit of analysis; state explicitly that no effort field exists in the current review record (C7) and that building one is a separate approved item.
* Action owner: planning parent
* Exact resolving evidence: Revised FR-E and P01-T02 with a "Dependencies" subsection naming #222 as an input and the effort-field gap, and a diff showing no #222 file touched.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Automation-bias test is a one-line parenthetical, not a design

* Related IDs: FR-B, C10, C3
* Evidence: plan FR-B ("confident wording, accept-first ordering, correct proposals mixed in"); research C10 (ADR mandatory RAI tests include reviewer automation bias)
* Concern: No arms (AI-suggested wrong versus neutral/unlabelled versus workflow-only), no counterbalanced ordering, no seeded-defect prevalence (vigilance depends on base rate; too-frequent defects inflate detection), no mix of correct proposals to measure false-reject, no measure of acceptance-rate drift across a session, and no fatigue or batch-size control.
* Impact: A passing result could reflect an unrealistically defect-rich session rather than real resistance to automation bias.
* Smallest useful change: Add to FR-B and P01-T02 an automation-bias design block: arms, order counterbalancing, PROPOSED prevalence band, correct-control share, per-position acceptance tracking, confidence-wording manipulation, session-length cap, each labelled PROPOSED/UNFILLED.
* Action owner: planning parent
* Exact resolving evidence: Revised FR-B and P01-T02 containing the listed design elements; each numeric item labelled PROPOSED.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Retention fields are not reconciled with the existing record, and reviewer identity conflicts with the anonymity precedent

* Related IDs: FR-C, C7, C9
* Evidence: research C7 (reviewer_action, reviewer_reason, override text, source hashes, prompt version exist); C9 (comprehension protocol uses anonymous study codes and forbids private staff identifiers)
* Concern: The plan says fields are "mapped to the existing record" without separating existing fields from gaps (reviewer-cited source, effort times, defect-key reference, arm, order position). #223 requires reviewer retained, while the nearest precedent forbids private staff identifiers. The protocol must not pick a side silently.
* Impact: Either the criterion is unmet by design or a privacy duty is breached when retention is later approved.
* Smallest useful change: In FR-C and P01-T02 add a three-column table (field, exists in C7 or gap, status) and record reviewer identity versus pseudonymous code as an UNFILLED privacy and consent decision with both options and consequences; do not choose.
* Action owner: planning parent to draft; owner and privacy lead to decide later
* Exact resolving evidence: README section table marking each field exists/gap and the identity-versus-code item listed under Follow-Up Items as an unresolved owner decision.
* Decision route: direct planner correction now (record as UNFILLED); the substantive choice is a significant user decision deferred and already outside this task

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: OQ-017 evidence lacks role separation and per-class domain competence

* Related IDs: FR-D, C3, C4, C5, C12
* Evidence: research C12 (recorder separate from approver), C5 (Finance approval of financial fields), C4 (OQ-017 open)
* Concern: FR-D lists authority, competence, independence and conflicts but not the separation of case-key author, seeder, reviewer, scorer and protocol approver; nor that each seeded class needs its competent reviewer role (financial, hazard/safety, legal/regulatory) and a non-reviewer adjudicator for disputed keys. Evidence that makes review "meaningful" (training, time allowed, authority to block without penalty) is not listed.
* Impact: Review by an unqualified or non-independent person could pass and be mistaken for meaningful oversight.
* Smallest useful change: Extend the FR-D table with role-separation rows, per-class competence rows, authority-to-block and no-penalty rows and adjudication; all roles UNFILLED, no named people.
* Action owner: planning parent
* Exact resolving evidence: README OQ-017 table containing those rows with UNFILLED labels and a statement that OQ-017 remains open.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Missing seeded-defect integrity, over-blocking and sample-power statements

* Related IDs: FR-A, FR-E, FR-F, C8
* Evidence: plan FR-A and FR-E; research C8 (valid-citation-wrong remains an open critical gap)
* Concern: No requirement that the defect key be frozen before review and withheld from reviewers and from any model or prompt; no leakage rule for public fixtures; no measure of false blocks on correct controls (cost of over-rejection and review burden); no statement that "zero misses" over n seeded defects bounds the miss rate only loosely (about 3/n at 95 percent), so any PROPOSED sample must be described with that limitation; critical versus non-critical defect definition is not stated.
* Impact: An unscored false-block rate and weak sample reasoning would let a lenient or over-cautious protocol look adequate.
* Smallest useful change: Add to FR-A, FR-E, FR-F: frozen key and hash, leakage rule, critical-defect definition tied to a named source, false-block rate on correct controls, and a PROPOSED-sample note stating the confidence limitation without asserting approved sizes.
* Action owner: planning parent
* Exact resolving evidence: Revised requirements and P01-T02 content list containing each item.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: Placement details and validation steps are under-specified

* Related IDs: P01-T01, P02-T01, P02-T02, P03-T01, P03-T02, C6, C11
* Evidence: src/agents/README.md headings (H2 "AI evaluation harness" at 253, H3 "Priority repetition accounting (#108, 2026-10-18)" at 294, H2 "Validation record" at 324); docs/reference/log.md heading format `## [YYYY-MM-DD] type | title` with a `query`, `update` or `plan` type; docs/reference/README.md has task rows ("Inspect ...") linking README anchors and a files table; research confirms index lists src READMEs
* Concern: Placement is sound, but the plan does not fix the heading level (H3 under the harness H2, matching #108), the GitHub anchor (meaningful-human-review-protocol-223-proposed-not-run) used by the index and any cross-link from the #108 section, the index form (an "Inspect ..." task row with a Refs-only #223 non-claim, or a README files-table update), the log type and heading, or the exact focused tests. "focused existing agents ai_eval tests" has no command. The log entry must not state or imply that the critique outcome or any criterion is met. The plan also lacks a statement that the dated research, plan, details and this critique are committed unchanged as original RPI evidence, and that the local gate (python3 tools/rpi-checks.py --all) and publication are NOT performed and not satisfied.
* Impact: Broken anchors, inconsistent index form or an unverifiable test claim; the evidence commit may be incomplete.
* Smallest useful change: Specify in P01/P02/P03: H3 placement and anchor, one index row of the "Inspect ..." form with a Refs #223 non-claim, one `query` log entry in the existing heading format, the exact test command from src/agents (for example `PYTHONPATH=../core/tests python3 -m unittest discover -s tests -q`, confirm against src/agents/README.md), an anchor check, ASCII/em-dash grep over added lines, and an explicit "local gate and publication not performed" statement.
* Action owner: planning parent
* Exact resolving evidence: Revised P01 to P03 with those specifics; later, the diff shows only the three target files plus tracking artifacts, and the anchor resolves.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-009 -->
### PC-009 [Low]: Critique disposition and dependency recording need a closing step

* Related IDs: Critique Disposition, Follow-Up Items, #108, #222
* Evidence: plan "Critique Disposition: Pending"; Follow-Up Items
* Concern: After revision the disposition must record each PC-xxx as accepted or rejected with rationale, leaving this critique unaltered. Follow-Up Items should also carry the identity-retention decision (PC-005), a base freshness check (fetch origin/main before commit; plan base 993a7b88), and the #108 status wording ("open; PR #405 offline accounting only; no criterion ticked") in the section's dependency block.
* Impact: Weak audit trail and possible stale base.
* Smallest useful change: Update the disposition table and Follow-Up Items accordingly during the revision.
* Action owner: planning parent
* Exact resolving evidence: Plan Critique Disposition listing PC-001 to PC-009 outcomes; Follow-Up Items including the added entries.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Placement in the existing evaluation protocol area with the comprehension-protocol precedent is well evidenced and avoids a new governance surface.
* Owner constraints, non-claims, #108 and #222 dependency handling, Refs-only wording and exit at a local commit are faithfully preserved.
* Rejected alternatives (new page, PRD edit, code) are justified.
* Residual risk (accepted pending owner): the protocol remains unapproved; thresholds, samples, panel, identity policy and OQ-017 holders stay UNFILLED, and effort capture is not built.

## Questions or Blocking Evidence Gaps

* None blocking. The reviewer identity versus pseudonymous code policy (PC-005) is an owner and privacy decision, deferred and recorded as UNFILLED; no user response is needed to revise.

## Limitations

* Plan-level critique only; no README section draft exists. The #223 issue body, PRD, owner comment and README log conventions were not re-fetched beyond the supplied research and headings reviewed. Anchor, test command and log type are suggestions to be confirmed by the planner.

## Recommended Next Action

* Highest-impact finding: PC-002
* Action owner: planning parent
* Smallest next action: Revise plan FR-B/FR-F and P01-T02 to state blocking, negative-control and traceability rules (PC-001 to PC-004), then address PC-005 to PC-009 in the same revision.
* User response required: no
