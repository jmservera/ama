---
title: RAI Remediation Artifact and Issue Coverage Analysis
description: Evidence-grounded reuse and acceptance-criteria gaps for the merged RAI delta
ms.date: 2026-10-15
ms.topic: reference
---
<!-- markdownlint-disable-file -->
<!-- markdown-table-prettify-ignore-start -->

## Scope and Sources

Review destination: GitHub jmservera/ama. Lens: generic platform-native. Autonomy: partial. Source commit: 7a8b1fe65475752fcf242ed52acab8e7e43b58d3, after parent-verified merge of PR 72.

Authoritative scope:

* [Remediation plan](../../../plans/2026-10-15/rai-remediation-plan.md): thirteen tasks.
* [Baseline report](../../../rai-reviews/2026-10-14/rai-report-ama-20261014.md): eleven PARTIAL and eleven NOT_ASSESSED checks.
* [PRD v0.16.0](../../../../docs/prds/zava-forward-retrofit-programme-demonstrator.md): current RAI contract and retained controls.

The case original, addendum, knowledge index, memory and housing-association primer supplied context. MVP README, assistant registry, citation-validation and evaluation excerpts, and ADR 0003 supplied bounded implementation context. These reads are not fresh acceptance tests.

No replanning of all 54 functional requirements is intended. Historical draft RAI identifiers must not overwrite current journey/sensor identifiers FR-048 to FR-050 or AC-062 to AC-068.

## Evidence and Metadata Findings

* All 144 discovered issues were hydrated in supplied evidence; focused comparisons below use relevant bodies.
* There are 143 open issues and one closed issue, number 23.
* Enabled native types Task, Bug and Feature are evidenced. All observed issues currently have native type null.
* Existing epic, feature and story labels communicate repository vocabulary, not native types.
* Sub-issue reads work. Native summaries show, for example, four children under issue 104, eight under 113 and six under 123. Exact child identities were not supplied by those summaries.
* No milestones are available in the supplied milestone snapshot. Retain null; do not invent a release milestone or due date.
* Every proposed target is unassigned and has milestone null. Retain both.
* No label, native type, state or hierarchy mutation is proposed.
* Textual Parent and Depends on statements do not prove native relationships. All unverified pairings remain flattened and needs_review.

## Six-Aspect Comparison Method

Every row below considers summary, native item type, workflow state, labels/fields, acceptance criteria and hierarchy fit.

For primary targets:

* Native type is null; retain it. Task/Feature support does not prove an existing item's intended level.
* Workflow state is OPEN; preserve it.
* Current labels corroborate subject area but do not establish completion.
* Existing criteria are partially overlapping, not complete RAI coverage.
* Described parents are useful context only; exact linkage remains needs_review.

P means the existing status:partially-delivered label. N means status:not-started. Neither is a native workflow state or independently verified delivery result.

## Primary Reuse Comparisons

| Ref / candidate | Existing issue and summary overlap | Type compatibility | State | Label/field overlap | Existing criteria and exact missing coverage | Hierarchy fit / decision and review question |
| --- | --- | --- | --- | --- | --- | --- |
| IS001 / task impact and authority | 105, task registry and proposal envelope: direct registry overlap | Native null; compatible subject, intended level needs_review | OPEN | feature, prd, area:ai, P | Scope, capability, source permissions, reviewer and proposal versions exist in criteria. Missing all retained legacy families, affected-person impact, intended/prohibited use, accepted personal delegation, unknown-authority blocking and separate exercise/live acceptance. | Text parent 104; exact link unverified. Similar: extend 105 rather than add a second registry. Review whether whole-system impact records remain in this registry item. |
| IS002 / processing manifest | 121, data protection and rights: direct processing overlap | Native null; retain | OPEN | feature, brd, prd, adr, area:platform, P | Lawful basis, retention, resident-model transfer and rights appear. Missing current staff/tenant identity scope, task field/type/length manifests, raw-document necessity, provider copies/region/transfer, telemetry and restore reconciliation. Present constructed-only statement is incomplete. | Text parent 113; unverified. Similar: extend 121. Review lawful authority and record-owner scope without inventing delegates or legal conclusions. |
| IS003 / provider-boundary minimization | 116, roles and field visibility: direct prompt/projection overlap | Native null; retain | OPEN | feature, prd, adr, area:platform, P | Endpoint role matrix, contractor prompt restrictions and free-text decision appear. Missing task necessity separate from permission, every legacy/provider/document path, exact nested payload spies, input bounds and no-call denials for unknown fields/raw uploads. | Text parent 113; unverified. Similar: extend 116. Review whether all provider-boundary tests are retained here instead of split into duplicate assistant-only work. |
| IS004 / provenance and meaningful review | 106, source-linked suggestions and accept/edit/reject: direct output/review overlap | Native null; retain | OPEN | feature, prd, area:ai, P | Task/draft-only acceptance, workflow-only handling and unresolved citation marking appear. Missing authentic-original provenance, hash-versus-truth distinction, false claims with valid citations, atomic source/proposal/release rechecks, critical source comparison and demonstrated reviewer effectiveness. | Text parent 104; unverified. Similar: combine P02-T02 and P03-T02 in 106 because provenance and its review gate are inseparable here. Review combined scope before updating. |
| IS005 / durable release admission | 107, five-assistant service: direct dispatch and SQL lifecycle overlap | Native null; retain | OPEN | feature, prd, adr, area:ai, P | Registry/source allowlists, off-by-default scans, SQL leases and no domain writes appear. Missing approved release/model attestation, material-version invalidation, expiry/revocation admission, completion/reliance fences, legacy parity and allowance preservation across restart. | Text parent 104; unverified. Similar: extend 107 and consume 105's manifest, not create a parallel release service. Review retained legacy inclusion. |
| IS006 / owned harm indicators | 146, monitoring and runbooks: operational signal overlap | Native null; story label is not a type | OPEN | story, adr, area:infrastructure, P | Platform alerts, dashboard, runbook owners and log exclusions appear. Missing task/release-specific harm/disparity/review-burden indicators, denominators, windows, human thresholds, insufficient state and suspension trigger. | Text parent 136; unverified. Similar: extend with a bounded current-runtime RAI subsection, not a new platform. Review infrastructure-versus-task monitoring boundary. |
| IS007 / suspension and restart | 122, continuity and reversible changes: direct disable/fallback overlap | Native null; retain | OPEN | feature, brd, area:platform, P | Disable/manual fallback, evaluated versioned changes and exports appear. Missing durable incident-wide suspension, pending/ready proposal reliance denial, late-result quarantine, communication ownership and distinct authorized restart. | Text parent 113; unverified. Similar: extend 122. Review incident and restart authority; operator identity alone is insufficient. |
| IS008 / accessible challenge | 130, nomination and challenge: direct resident redress overlap | Native null; retain | OPEN | feature, brd, area:safety-consent, N | Original account, owner, challenge/correction, dependent re-review, manual route and no sanction appear. Missing AI/source/policy/human-decision version binding, permitted explanation, next-update commitment and exact dependent invalidation. | Text parent 81; unverified. Similar: add general AI challenge criteria without resolving nomination OD-41/OD-42 or expanding representative authority. Review this boundary explicitly. |
| IS009 / cohorts and missing-data effects | 128, equity/accessibility testing: direct fairness overlap | Native null; retain | OPEN | feature, brd, prd, area:governance, P | Keyboard/screen-reader, human missing-data review and research protocol appear. Missing paired expected-outcome cohorts, deterministic/AI comparisons, denominators, sufficiency, subgroup burden/errors, lawful fields and activation blocking. | Text parent 123; unverified. Similar: extend 128 while retaining policy signing in 79. Review denominator/threshold approvals, not invented numerical targets. |
| IS010 / held-out and human evidence | 108, AI evaluation: direct held-out/model overlap | Native null; retain | OPEN | feature, prd, adr, area:ai, P | Critical misses, model/prompt/latency/reviewer reporting and regional versions/quotas appear. Missing independent held-out split and answers, every assistant/legacy family, competent human detection, all-role effort, parser/manual comparators, consent and finite exercise authority. | Text parent 104; unverified. Similar: extend 108. Review shared boundaries with 129 and 174 together; neither journey experiments nor fixture registry replaces this evidence. |
| IS011 / backup and erasure reconciliation | 145, SQL backup/restore: direct restore overlap | Native null; retain | OPEN | feature, adr, area:infrastructure, P | PITR, ledger verification, RTO/RPO and retention appear. Missing actual document/audit reconciliation, tombstones/holds/provider copies, revoked authority and spent allowance non-resurrection, independent witnessing and disposable-only authorization. | Text parent 136; unverified. Similar: extend 145, retain 114 as store dependency. Review local disposable drill versus separately authorized Azure recovery. |
| IS012 / qualified closure and acceptance | 126, protocol and release gates: direct evidence/release overlap | Native null; retain | OPEN | feature, brd, area:governance, N | Protocol/DPIA, phase decisions and guardrail pause appear. Missing all 22 check dispositions, commit/task/release-bound closure, fresh assessment, separate legal/control/product acceptance and preserved negative/insufficient results. | Text parent 123; unverified. Similar: extend 126. Review bounded exercise closure versus future pilot gates; merging documents cannot authorize either. |

All proposed fields other than body remain unchanged. Exact acceptance additions are in [issues-plan.md](./issues-plan.md).

## Secondary Comparisons and Fan-Out Review

The following are supporting or alternative matches, not additional proposed Updates. They must be considered together with the primary targets rather than silently selecting the first search result.

| Candidate / existing | Summary overlap | Type | State | Labels/fields | Criteria coverage | Hierarchy fit and decision |
| --- | --- | --- | --- | --- | --- | --- |
| Restore / 114 | Durable SQL and deletion reapplication overlap | null | OPEN | feature, adr, area:platform, P; milestone null | Backup/restore/deletion criteria overlap but do not include the full RAI drill | Text parent 113, with one child in native summary. Similar; use as retained store dependency, concentrate drill in 145. |
| Processing / 117 | Document retention/hold overlap | null | OPEN | feature, adr, area:platform, P; milestone null | Scanning and approved retention job do not approve inference or prove erasure reconciliation | Text parent 113. Similar; retain storage control, do not duplicate its scanning deliverable in 121/116. |
| Cohorts / 79 | Deterministic ranking and policy ownership overlap | null | OPEN | feature, prd, adr, area:case-workbench, P | Determinism/hash/owner signing are necessary, not subgroup evaluation | Text parent 73. Similar; retain policy authority here, evaluation in 128. |
| Evidence / 129 | Journey experiments and non-AI comparison overlap | null | OPEN | feature, prd, adr, area:governance, N | Five bundles and scope mapping do not cover all assistant/legacy held-out or human criteria | Text parent 123. Similar; preserve bundle boundaries, do not treat it as complete RAI evaluation. |
| Evidence / 174 | Evaluation dataset registry overlap | null | OPEN | story, prd, area:synthetic-data, P | Version/purpose and reproducible scale fixture do not prove held-out independence or model/human results | Text parent 167. Similar; consume registry evidence, do not duplicate scale-fixture work. |
| Processing / 163 | Privacy, staff notice and provider handling overlap | null | OPEN | feature, brd, prd, area:agent-chat, N | Criteria cover future chat/memory messages and rights, not every current legacy/assistant path | Text parent 157. Similar subject, different future capability. No Change; do not activate chat scope through this delta. |
| Evaluation / 164 | Grounding, review and injection overlap | null | OPEN | feature, prd, adr, area:agent-chat, N | Multi-turn and memory criteria do not replace current task evaluation | Text parent 157. Similar subject, separate future capability. No Change. |
| RAI closure / 23 | Rubric recording failure, not RAI closure | null | CLOSED | No labels, no milestone, no assignee | Body records failure to supply 20 rubric criterion IDs at historical commit 3d7ad6d799a5654b4c61cdcc9070ae34d9d4914c; no RAI acceptance criteria | No established RAI parent. Distinct; historical closed work only, not remediation evidence and not reopened. |

There is no Match for a complete RAI task outcome. No missing/truncated primary body requires Uncertain. Unknown authority, thresholds and relationship metadata remain needs_review rather than being converted into Distinct creates.

## Thirteen-Task Coverage

| Source task | Planned ref / target | Required delta |
| --- | --- | --- |
| P01-T01 | IS001 / 105; IS012 / 126 for acceptance | Whole-system impact, purpose and personally accepted authority |
| P01-T02 | IS002 / 121 | Minimum-necessary processing, staff scope and retention |
| P02-T01 | IS003 / 116 | Every provider boundary, payload spies and no-call denials |
| P02-T02 | IS004 / 106 | Provenance and factual assurance distinct from citation resolution |
| P03-T01 | IS005 / 107 | Durable release/model admission and invalidation |
| P03-T02 | IS004 / 106; IS010 / 108 for human evidence | Source-based review plus witnessed effectiveness |
| P04-T01 | IS006 / 146 | Owned indicators and honest insufficient readiness |
| P04-T02 | IS007 / 122 | Persistent suspension and controlled restart |
| P05-T01 | IS008 / 130 | Accessible challenge and precise correction |
| P05-T02 | IS009 / 128 | Cohort/missing-data impact evaluation |
| P06-T01 | IS010 / 108 | Held-out quality, oversight and net benefit |
| P06-T02 | IS011 / 145 | Witnessed backup/erasure reconciliation |
| P06-T03 | IS012 / 126 | Fresh version-bound closure and qualified acceptance |

## Residual Coverage

Statuses below are retained baseline dispositions, not new findings or closures.

| Residual ID | Baseline | Planned refs | Required closure evidence |
| --- | --- | --- | --- |
| T-RAI-001 | PARTIAL, MEDIUM, CONFIRMED | IS002, IS003 | Approved necessity and exact payload/role/upload tests |
| T-RAI-002 | PARTIAL, MEDIUM, CONFIRMED | IS004, IS010 | Trusted-original, altered-source and plausible-false-claim proof |
| MEASURE-01 | PARTIAL, MEDIUM, DOWNGRADED | IS004, IS010 | Factual support and observed critical-defect detection |
| GOVERN-AUDIT-02 | PARTIAL, MEDIUM, DOWNGRADED | IS005 | Actual serving-version attestation and admission denial |
| MN-3.2 | PARTIAL, MEDIUM, DOWNGRADED | IS005, IS012 | Material invalidation, renewed evidence and authorized release |
| MAP-02 | PARTIAL, MEDIUM, DOWNGRADED | IS001, IS002, IS012 | Current staff-data, purpose and processor authority |
| MN-4.1 | PARTIAL, MEDIUM, DOWNGRADED | IS006 | Approved windows/thresholds/owners and breach test |
| MN-4.3 | PARTIAL, MEDIUM, DOWNGRADED | IS007 | Suspension, owned communication and distinct restart approval |
| GOVERN-AUDIT-01 | PARTIAL, LOW, DOWNGRADED | IS001, IS012 | Personally accepted accountability and delegation |
| MAP-01 | PARTIAL, LOW, DOWNGRADED | IS009, IS012 | Approved ranking/hash/missing-data impact |
| MAP-04 | PARTIAL, LOW, DOWNGRADED | IS004, IS008, IS010 | Representative participation, competence and complete benefit evidence |

## NOT_ASSESSED Coverage

These are evidence gaps, not eleven additional proven incidents.

| Check | Planned refs | Evidence still required |
| --- | --- | --- |
| GOVERN-AUDIT-04 | IS002, IS011 | Qualified privacy/retention/processor decisions and reconciliation |
| GOVERN-AUDIT-05 | IS001, IS012 | Exercise and operational acceptance distinguished |
| MAP-05 | IS001, IS012 | Dated qualified UK and conditional EU intended-use/currentness review |
| MEASURE-02 | IS010 | Actual serving-model held-out quality; applicable calibration or explicit not-applicable rationale |
| MEASURE-03 | IS008, IS009, IS010 | Lawful representative fairness, accessibility and challenge evidence |
| MEASURE-04 | IS010 | Complete all-role effort and incremental benefit with Finance validation |
| MN-2.3 | IS011 | Witnessed actual backup/erasure/history reconciliation |
| T-RAI-005 | IS005, IS010, IS011 | Operational/model-integrity evidence beyond scripted feasibility |
| EU-COND-01 | IS001, IS012 | Qualified territorial/currentness determination |
| EU-COND-02 | IS001, IS012 | Actual actor roles, influence and intended-use analysis |
| EU-COND-04 | IS010, IS011, IS012 | Qualified operational assurance if applicability is established |

## PRD and Retained-Control Coverage

| Contract | Planned refs | Coverage boundary |
| --- | --- | --- |
| FR-051, AC-069 | IS001, IS005 | Version-bound release, intended use and zero-call admission denial |
| FR-052, AC-071 | IS008 | Permitted explanation, human/non-digital route and precise correction |
| FR-053, AC-072 | IS006, IS007 | Harm trigger, suspension, manual continuity and authorized restart |
| FR-054, AC-073 | IS009, IS010 | Cohorts, denominators, insufficient samples and activation blocking |
| AC-070; FR-026/027; NFR-009 | IS004, IS010 | Factual source review and demonstrated critical-defect detection |
| NFR-014 | IS005, IS006, IS007, IS009, IS012 | Material change, owned monitoring, thresholds and release decisions |
| FR-036, AC-058 | IS001, IS005 | Registry approval and default-off authority retained |
| NFR-003/005, AC-053/054/060 | IS002, IS003, IS004 | Permission, necessity, injection resistance and output/review/export boundaries |
| FR-028, AC-061 | IS005, IS007, IS011 | Manual fallback, SQL lifecycle and authority/allowance durability |
| FR-043, AC-051 | IS004, IS008 | Exactly dependent invalidation; unrelated decisions preserved |
| FR-012, NFR-012 | IS009 | Deterministic ranking ownership, missing-data honesty and denominator integrity |
| FR-045, AC-063/064 | IS008 | Representative limits and open-remedy rights retained |
| CON-009, AC-057 | IS005, IS010, IS012 | Real AI/SQL/Azure evidence for a delivered build; mocks are development evidence only |
| NFR-005/006/011 | IS002, IS011 | Retention, actual recovery and erasure/authority reconciliation |

Retain baseline PASS controls GOVERN-AUDIT-03, MAP-03, MEASURE-05, MN-2.4, T-RAI-003, T-RAI-004 and EU-COND-03 as regression obligations across IS003 to IS011. Their inspected-path PASS does not become universal legacy coverage, human competence, legal certification or deployed isolation.

## Gaps and Decision

The current backlog covers subject areas but does not fully ensure execution of the merged RAI plan. Missing acceptance categories are:

* Whole-system accountability and actual staff/tenant processing.
* Task necessity across every provider/document/legacy boundary.
* Trusted provenance and factual support beyond resolving citations.
* Actual serving-model/version-bound release admission.
* Owned harm monitoring and incident-wide suspension/restart.
* Accessible challenge and denominator-aware cohort evidence.
* Independent held-out, representative-human and complete-effort benefit evidence.
* Actual backup/erasure reconciliation and qualified version-bound closure.

The smallest proposed plan is twelve Updates, zero Creates and zero Links. One existing review issue carries two closely connected remediation tasks. This closes planning coverage only; it does not execute remediation or close findings.

All twelve Updates require human review of Similar reuse boundaries. Exact hierarchy pairs, operational delegates, legal applicability, cohorts, thresholds, participant authority and budgets remain needs_review. Existing labels and native types are preserved; no speculative owner, date or milestone is assigned.

<!-- markdown-table-prettify-ignore-end -->
