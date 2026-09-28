<!-- markdownlint-disable-file -->
# Review: Agent What-If Study validity after the Review-progress-challenge merge

## Executive Summary

* Assessment: the study's headline conclusion still holds after the merge. None of the 20 scenarios creates an end-to-end agent, and nothing merged from BRD v0.3.0 to v0.5.0 contradicts that. Six things need updating: two material defects (Article 22 citations and role attribution) and four consistency gaps against the agent-led modernisation reframe, the pilot measurement design and the transparency controls.
* Why this matters: the study is cited from the addendum, the index and the mentor deck. As written it repeats the Article 22 citation error already corrected in CON-003, attributes eleven answers to perspectives that have no role agent, and reads "Do not build as agent" against a proposal that is now agent-led.
* Review execution: Complete
* Assessed outcome: Defects found
* Validation coverage: read-only relative-link check on the study passed (0 broken); regulatory claims compared against local snapshots only; no online legal check and no role-agent re-run
* Confidence and limitations: high for citation, identifier and terminology findings, which are text comparisons; medium for the reframe reconciliation, which is interpretive

The assessment above is the reviewer's proposal. Parent Decision Record contains the final decisions and next actions, or states that decisions are pending.

## What You May Not Know

* The study was written on a branch that did not contain BRD v0.3.0 to v0.5.0. The role agents answered from the addendum as it stood on main on 27 September, before the agent-led modernisation reframe, the pilot measurement protocol and the transparency review. The reframe does not reintroduce any end-to-end agent, so the verdicts survive, but the role answers were not re-validated against the current addendum.
* The value-versus-complexity grid is the author's coarse scoring, as the study itself states. Under the proposed OD-34 resolution, scaling is decided by the pilot's Comparison 2 evidence, not by the grid.

## Findings and Proposed Routes

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Article 22 citations point to text the local snapshot omits

The study cites "UK GDPR Article 22" eight times (SP2 scoring row, the SP2 clarification answer and verdict, the Stock Prioritisation aggregate verdict and stop criteria, Cross-Cutting Findings, and question 9). The local consolidated text replaces Article 22 with a row of dots and holds the rules in Articles 22A to 22D. This is the same error the transparency review corrected in CON-003 on 26 September.

* Related scope: Stock Prioritisation What-If 2; Aggregate Verdict and Stop Criteria for Stock Prioritisation; Cross-Cutting Findings; Questions for Proper North Homes; Scoring Table row SP2
* Expected behavior: cite the provisions in the dated local snapshot. Article 22A defines solely automated significant decisions. Article 22B restricts such decisions based on Article 9 special category data unless explicit consent or a law-based condition with Article 9(2)(g) applies. Article 22C(2) requires information, representations, human intervention and contest safeguards. This is consistent with BRD CON-003, which cites UK GDPR Articles 22A to 22C (docs/reference/regulatory/data-protection/uk-gdpr-current-text.md, converted 2026-09-19).
* Observed behavior and evidence: docs/reference/research/company/agent-what-if-study.md uses "Article 22" throughout. docs/reference/regulatory/data-protection/uk-gdpr-current-text.md shows "Article 22 . . ." under its heading, followed by Articles 22A, 22B, 22C and 22D.
* Impact: a reader following the citation finds no text. The SP2 answer also misses the stricter Article 22B restriction that applies when vulnerability (health) data feeds a solely automated ranking.
* Resolution condition: no bare "Article 22" citation remains. Each reference names Articles 22A to 22C, or 22B where special category data is involved, with the local snapshot link and retrieval date.
* Proposed destination: rpi-implement
* Smallest useful next action: replace the eight references and correct the SP2 answer's legal framing, keeping it labelled as a sector-informed hypothesis for DPO decision

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Eleven answers are attributed to perspectives that have no role agent

The study says each clarification question was put to the relevant `company-*` role agents. Eleven answers, all in the extended scenarios, are attributed to roles for which no agent exists:

* `Chief Data and Digital Officer`: seven answers
* `Executive Director of Finance and Governance`: two answers
* `Company Secretary and Head of Governance`: one answer
* `Head of Internal Audit and Assurance`: one answer

The eight role agents are the Head of Building Safety and Compliance, Data and Performance Lead, Executive Director of Assets, Head of Finance for Capital Investment and Grants, Neighbourhood Housing Officer, Head of Procurement and Contract Management, Head of Resident Engagement and Insight, and Retrofit Programme Manager.

* Related scope: Grant and Funding What-If 2 and 3; Coordination What-If 2 and 3; Quality Verification What-If 3; Programme Supervisor What-If 2; Damp-and-Mould What-If 2 and 3
* Expected behavior: per the repository's company profile agent conventions, answers come from the role agents anchored to the case, the addendum and company-profile-research.md, or are labelled as the author's own hypothesis.
* Observed behavior and evidence: .github/agents/company-*.agent.md defines eight personas; none of the four titles appears in any agent or in docs/reference/research/company/company-profile-research.md. The 2026-09-27 log entry says "the same role agents were asked".
* Impact: the study presents unanchored answers with the same evidence standing as role-agent hypotheses. This is the "articulate answer becomes a fact" risk the role agents exist to prevent.
* Resolution condition: every answer is either produced by an existing role agent and attributed to it, or relabelled as an author hypothesis with no role-agent anchor, with the limitation recorded in the study and the log.
* Proposed destination: rpi-research, to re-run the eleven questions with the nearest existing role agents. The alternative is a relabel as rpi-implement.
* Smallest useful next action: owner decision between re-running and relabelling

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Verdicts and sequencing are not reconciled with the agent-led modernisation reframe

BRD v0.4.0 and the addendum now propose agent-led modernisation of the existing model. The Agentic Architecture Brief places bounded agent capabilities inside each capability area, for example reconciliation and plain-language score explanation in property data and prioritisation. The study's scenario verdicts read "Do not build as agent", and its sequencing section reads as a build order.

* Related scope: Summary of Revised Verdicts; per-scenario verdicts; Sequencing Implied by the Grid
* Expected behavior: the study states that "Do not build as agent" means do not build the requested end-to-end agent, and maps its surviving bounded-AI candidates to the Architecture Brief. It also states that the grid is a candidate order for Phase 0 and Comparison 2 testing, while scaling follows the pilot gate under the proposed OD-34 resolution.
* Observed behavior and evidence: docs/case_study_48_addendum.md (Where Agents Fit and Where They Do Not; Agentic Architecture Brief; Pilot Success Measures). BRD OD-34 and RULE-019. The study has no reference to the reframe, OD-34 or Comparison 2.
* Impact: readers of the deck and addendum may see the study as contradicting the agent-led proposal, or treat the grid as a scaling decision.
* Resolution condition: a short reconciliation in the study links the verdict vocabulary to the Architecture Brief and positions the grid under OD-34, RULE-019 and Comparison 2.
* Proposed destination: rpi-implement
* Smallest useful next action: add a "Reconciliation With the Current BRD" section and a sentence in Sequencing

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Value tests and stop criteria omit the controls merged in BRD v0.5.0

The study's added stop tests are:

* false-provenance rate
* equity check
* awareness timestamp
* DPIA

They do not reference the BRD controls that now govern the same ground:

* RULE-019: frozen pilot protocol with Comparison 1 and Comparison 2
* RULE-024: guardrail pause
* FR-042: prioritisation policy with per-home reason codes, which bears on SP1 to SP3
* FR-043: AI capability register and Board assurance report, which every augmented module would enter
* FR-044: output provenance on every agent output, which bears on AS1 and QV1 evidence assessments
* OD-36: DPIA for measurement data
* OD-39: missing transparency sources

* Related scope: Value Test and Stop Criteria; Cross-Cutting Findings
* Expected behavior: augmentation tests reuse the canonical BRD controls rather than a parallel list.
* Observed behavior and evidence: the BRD rows FR-042, FR-043, FR-044, RULE-019, RULE-024, OD-36 and OD-39 in docs/brds/agentic-retrofit-programme-brd.md. The study's Value Test and Stop Criteria section cites none of them.
* Impact: the tests could diverge from the BRD, and augmentations would miss the transparency gate and capability register.
* Resolution condition: the Value Test and Stop Criteria section maps each addition to, or places it alongside, the governing BRD identifiers.
* Proposed destination: rpi-implement
* Smallest useful next action: add the cross-references

<!-- rpi:review id=RV-005 -->
### RV-005 [Low]: Superseded terminology and legacy identifiers

The study uses "shared foundation" throughout, while the addendum and BRD have used "digital foundation" since v0.4.0. It also cites legacy aliases BR-011, BR-013, BR-016 and BR-020, although the BRD had already moved to canonical identifiers when the study was written.

* Related scope: whole study
* Expected behavior: current terminology, or an explicit mapping, and canonical identifiers. BR-011 maps to FR-011, BR-013 to FR-013, BR-016 to NFR-001 and BR-020 to RULE-006, per the BRD Legacy Identifier Map.
* Observed behavior and evidence: the study body; BRD Legacy Identifier Map rows for BR-011, BR-013, BR-016 and BR-020.
* Impact: minor friction and inconsistency with the deck and addendum.
* Resolution condition: the study states that its "shared foundation" is the addendum's digital foundation, and it cites canonical identifiers with legacy aliases in brackets.
* Proposed destination: rpi-implement
* Smallest useful next action: add a terminology note and replace the four identifiers

<!-- rpi:review id=RV-006 -->
### RV-006 [Low]: Addendum cross-reference and index row describe only the first session

The addendum paragraph and the index catalog row describe the initial augmentations only. They omit the extension to 20 scenarios, the value-versus-complexity grid and the sequencing. The addendum paragraph also says "shared foundation" beside text that says "digital foundation".

* Related scope: docs/case_study_48_addendum.md (Challenge of the Requested Agents); docs/reference/README.md (Research Syntheses row)
* Expected behavior: the summaries match the current study.
* Observed behavior and evidence: both passages list photos, GPS, invoices, consent and capacity feeds only.
* Impact: readers underestimate the study's scope.
* Resolution condition: both summaries mention the 20 scenarios and the grid, use "digital foundation" and name the corrected UK GDPR provisions.
* Proposed destination: rpi-implement
* Smallest useful next action: edit both passages and append a log entry

## Parent Decision Record

<!-- Decisions live here. Append events; never rewrite the evidence body above to fit a decision. -->

### Current Disposition

* Based on events: RD-001 to RD-009
* Review execution: Complete
* Final outcome: Defects found; all six findings accepted and resolved in follow-up implementation on 2026-09-27
* Finding decisions and next actions: RV-001, RV-003 to RV-006 implemented; RV-002 re-run with the Data and Performance Lead (seven answers) and the Housing Finance and Grants Lead (two answers), and the governance and internal audit answers relabelled as author hypotheses
* Decisions still needed: none

This summary is derived from Decision History, not a second decision record. The latest event for each subject governs; refresh this summary after appending decisions and on recovery.

### Decision History

Append events in order. Never rewrite or delete an earlier row. The latest event for a subject is current.

| Event | Subject | Decision source | Status or value | Proposed destination | Final destination | Owner | More information needed | Smallest next action | Rationale |
|---|---|---|---|---|---|---|---|---|---|
| RD-001 | participation | system | user-owned | none | none | owner | none | Compare evidence | Standalone `/rpi-review` invocation by the owner; the request also asks to fix anything that should be updated |
| RD-002 | execution | agent | Complete | none | none | review parent | none | Resolve finding routes | One comparison pass covered every section of the study and its three registrations |
| RD-003 | RV-001 | user request | accepted | rpi-implement | rpi-implement | review parent | none | Done: citations replaced | Owner asked to fix anything that should be updated |
| RD-004 | RV-002 | user | accepted, re-run | rpi-research | rpi-research then rpi-implement | review parent | none | Done: nine answers re-run and replaced; two relabelled | Owner chose to re-run with the nearest role agents and relabel answers with no matching agent |
| RD-005 | RV-003 | user request | accepted | rpi-implement | rpi-implement | review parent | none | Done: reconciliation section and sequencing note | Owner asked to fix anything that should be updated |
| RD-006 | RV-004 | user request | accepted | rpi-implement | rpi-implement | review parent | none | Done: Value Test cross-references | Owner asked to fix anything that should be updated |
| RD-007 | RV-005 | user request | accepted | rpi-implement | rpi-implement | review parent | none | Done: terminology mapping and canonical IDs | Owner asked to fix anything that should be updated |
| RD-008 | RV-006 | user request | accepted | rpi-implement | rpi-implement | review parent | none | Done: addendum paragraph, index row, log entry | Owner asked to fix anything that should be updated |
| RD-009 | final outcome | agent | Defects found; all six resolved | none | none | review parent | none | Mentor deck slide 10 to reflect the corrected study | Implementation verified by the link and attribution checks below; online legal check remains out of scope |

## Validation Evidence

| Command | Scope | Status | Summary |
|---|---|---|---|
| Relative-link resolution over the study's Markdown links (read-only) | docs/reference/research/company/agent-what-if-study.md | Passed | 0 broken relative links |
| Role attribution comparison against `.github/agents/company-*.agent.md` | Study clarification answers | Failed | 11 answers attributed to 4 perspectives with no agent (RV-002) |
| Regulatory citation comparison against local snapshots | UK GDPR and Awaab's Law citations | Failed | Article 22 references do not resolve (RV-001); Awaab's Law section 3 and 3.5 citations match the local guidance |
| Online official-source check | Regulatory claims | Skipped | Outside the review boundary; the study already records this limitation |
| Post-implementation link and anchor check (read-only) | agent-what-if-study.md after fixes | Passed | 0 broken links or anchors; no bare "Article 22" citation; no attribution to a role without an agent |
| BRD identifier check on re-run answers | Identifiers cited by the two role agents | Passed | All cited FR, NFR, RULE, CON and AC identifiers exist in BRD v0.5.0 |

## Risks, Blockers, and Residual Work

* Blockers: none
* Remaining active work: none
* Residual work: re-validate the role answers against the current addendum when the role agents are next run (see What You May Not Know)

## Review Record

### Scope and Evidence

* Task ID: agent-what-if-study-post-merge
* Review date: 2026-09-27
* Review scope: full task
* Assessed boundary: docs/reference/research/company/agent-what-if-study.md and its knowledge-base registrations (addendum cross-reference, index rows, log entries) against the merged state of docs/brds/agentic-retrofit-programme-brd.md v0.5.0, docs/case_study_48_addendum.md, docs/reference/research/company/pilot-measurement-challenge.md and docs/reference/regulatory/data-protection/uk-gdpr-current-text.md after merge commit baef324
* Review depth and provenance: standard; default
* Candidate identity: agent-what-if-study.md last changed in b1bab12, SHA-256 prefix 96FC831F692E; merged tree baef324
* Review execution: Complete
* Helper use: none
* Plan: none; the study was produced without an RPI plan
* Plan critique: none
* Changes: none; change evidence is the log entries dated 2026-09-27 in docs/reference/log.md and commits 7e70174, f48fdc6, b1bab12
* Other evidence considered: merge commit baef324; .github/copilot-instructions.md conventions; .github/agents/company-*.agent.md

### Opening Review State

* Interpreted review goal: decide whether the what-if study's verdicts, citations, identifiers and terminology remain valid against the BRD v0.3.0 to v0.5.0 changes, the agent-led modernisation reframe, the pilot measurement design and the transparency review that arrived through the merge, and identify what must be updated
* Review scope: full task
* Evidence readiness: study, merged BRD, addendum, pilot measurement challenge, log and local regulatory snapshots are available; no plan, critique or changes record exists
* Acceptance basis: repository conventions in .github/copilot-instructions.md (evidence labelling, dated regulatory citations to local snapshots, flag contradictions, keep proposals distinguishable) and consistency with the current BRD, addendum and regulatory snapshots
* First comparison boundary: study text against merged documents; no role agents re-run and no online legal checks
* Active read-only boundaries: this review writes only this record; fixes follow as separate implementation work at the owner's request
* Authority: the review parent compares evidence and writes findings; final outcome, route dispositions, and continuation are recorded in Parent Decision Record
* Initial blockers: none

### Acceptance and Change Coverage

| Requirement or scope | Implementation and validation evidence | Assessment | Finding or rationale |
|---|---|---|---|
| Headline verdict still valid after merge | Addendum Where Agents Fit, Agentic Architecture Brief; BRD v0.5.0 | Met | Reframe adds bounded agents, not end-to-end agents |
| Regulatory citations resolve to dated local snapshots | uk-gdpr-current-text.md; awaabs-law-phase-1-guidance-2025.md | Gap | RV-001 |
| Evidence labelling and role-agent provenance | company-*.agent.md | Gap | RV-002 |
| Consistency with current proposal and pilot gate | Addendum; BRD OD-34, RULE-019 | Gap | RV-003 |
| Consistency with transparency and measurement controls | BRD FR-042 to FR-044, RULE-019, RULE-024, OD-36, OD-39 | Gap | RV-004 |
| Terminology and identifiers | BRD Legacy Identifier Map | Gap | RV-005 |
| Knowledge-base registrations | Addendum paragraph; README rows; log entries | Gap | RV-006; log entries accurate as history and left unchanged |
| Awaab's Law and sensor-absence rule | Addendum "must not use the absence of a sensor alert"; study DM2 section 3.5 citation | Met | Consistent |
| Relative links | Link check | Met | 0 broken |

### Critique and Follow-Up Assessment

* Latest critique dispositions: no plan critique exists
* Material revisions: the merge brought BRD v0.3.0 to v0.5.0 into the study's branch; assessed above
* Dependent-work pause assessment: the mentor deck slide 10 cites this study; any corrections must flow to it
* Justification assessment: not applicable

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|---|---|---|---|
| Re-validate role answers against the current addendum | Needs new role-agent runs | Owner | Distinct follow-up |

### Reviewer Self-Check

* [x] Every supplied requirement, acceptance criterion, in-scope marker, material update, critique disposition, validation result, blocker, remaining item, and plan follow-up has an assessment or explicit gap.
* [x] Findings are substantive, evidence-grounded, severity-graded, and use stable `RV-xxx` IDs with expected and observed behavior, a resolution condition, and one proposed route each.
* [x] Execution status, assessed outcome, validation coverage, limitations, and proposed routes are complete and internally consistent.
* [x] The summary is scoped and advisory, findings keep their supporting context together, and acceptance coverage distinguishes demonstrated gaps from unassessed behavior.
* [x] Standard review completely assessed the material boundary while omitting restatement, cosmetic feedback, exhaustive strengths, low-impact suggestions, and continual narration; deep review remained inside the supplied boundary.
* [x] The review did not mutate source, the plan, critique, research, or changes record, and ran only a read-only link check; no helper was used.
* Checked boundary: every section of the study, the addendum cross-reference, index rows and the two 2026-09-27 log entries
* Missing or limited evidence: no online legal check; role answers not re-run
