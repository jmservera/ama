---
title: Zava Forward whole-project Responsible AI plan
description: Repository-only six-phase NIST AI RMF assessment, threat model, impact and proposed handoff
ms.date: 2026-10-28
ms.topic: reference
---

## System Definition

Evidence: assessment baseline is `9bfed51863b05a25e9939d82504c576524688e14`,
equal to fetched `origin/main` when work began on `docs/rai-review-project`.
This is a documentation assessment, not an application change, penetration
test, new model evaluation or observed deployment review.

Evidence: the user requests every analytical phase, repository-only evidence
and local backlog proposals without issue creation. Phase 2, 3 and 6 human
confirmations remain unrecorded; proceeding with draft analysis does not
manufacture those confirmations. The state records analytical progress
separately from qualified acceptance.

Evidence: NIST AI RMF 1.0 is the default evaluation framework (U.S. Government
work, not subject to copyright protection in the United States). Function and
subcategory identifiers below use the planner's embedded reference-pack
aliases, `GV`, `MP`, `MS`, `MN`. The local
[`Responsible AI Release Position`](../../../docs/case_study_48_addendum.md#responsible-ai-release-position-2026-10-14)
already adopts the four functions. This is a risk-based mapping, not exhaustive
subcategory conformance or a legal risk classification.

Evidence: evidence labels apply to every statement in this assessment:
`Evidence` means an inspected repository/tracker assertion or source behavior,
not independent proof of effectiveness; `Hypothesis` means a proposed risk,
treatment or acceptance criterion; `Unknown` means missing or unverified
evidence. Table cells inherit their row's classification unless explicitly
qualified. Reported prior checks are historical evidence, not tests rerun here.

### Boundary and intended use

Evidence: the original case describes a North of England housing association
with 60,000 homes and five L2-L4 agent ambitions. The addendum explicitly
restricts current assistance to recommendations, drafts and flags. The
customer is an exercise case, not an accessible organisation that can supply
real delegations. Source: `docs/case_study_48_original.md:10-45`;
`docs/case_study_48_addendum.md:139-170,967-1013,1471-1530`.

Evidence: scope includes resident and employee sites, five bounded assistants,
both chats, retained briefing/message/summary/priority/funding/document paths,
deterministic policy, regulatory lookup, IoT, data, orchestration, evaluation
and infrastructure. `src/README.md:11-54` defines the five Python projects
and currently API-hosted assistant runtime. No private data, secrets, `.env`,
Azure, `az`, paid inference or external evidence retrieval is part of this review.

Unknown: current deployed versions, provider processing terms, actual personal
data contents, legal currentness and qualified operational acceptance cannot
be established by this source-only review.

### AI Component Inventory

| ID | Classification | Component and inputs/outputs | Actual autonomy and accountable boundary | Evidence |
| --- | --- | --- | --- | --- |
| A1 | Evidence | `stock-prioritisation`: home/survey and public ranking facts to cited data-gap proposal | Recommend/explain only; Coordinator or Programme Manager verifies then accepts. Cannot reorder investment queue | `src/core/src/zava_forward/core/assistants.py:31-44,87-108,995-1046`; `ranking.py:64-87` in the same directory |
| A2 | Evidence | `assessment-preparation`: survey/design hashes, measures and design version to checklist | Draft only; Coordinator/Programme Manager reviews proposal, not professional assessment approval | `src/core/src/zava_forward/core/assistants.py:34-35,109-121,995-1046` |
| A3 | Evidence | `funding-evidence`: structured funding/finance/grant/evidence metadata to gaps | Draft only; Grants and Evidence Officer/Programme Manager reviews. No eligibility, award, submission or payment authority | `src/core/src/zava_forward/core/assistants.py:36-38,122-139,995-1046` |
| A4 | Evidence | `works-resident-coordination`: preferences, recorded appointment outcomes, handoff and committed capacity to update/options | Draft only; Coordinator/Resident Liaison Officer/Programme Manager reviews. Does not send, schedule or secure works consent | `src/core/src/zava_forward/core/assistants.py:39-41,140-146,995-1046` |
| A5 | Evidence | `quality-evidence`: per-measure checklists and active quality evidence to discrepancies | Flag/propose only; Quality Inspector/Programme Manager review includes independence check. Not autonomous QA acceptance | `src/core/src/zava_forward/core/assistants.py:42-44,147-151,1017-1029` |
| A6 | Evidence | Retained `briefing`, `message`, `summary`, `priority`, `funding_draft`, `read_document` | Text aids, no model tools/domain actions; ordinary human controls remain separate | `src/core/src/zava_forward/core/ai_registry.py:37-61`; `ai.py:108-204`; `ai_tasks.py:88-161` |
| A7 | Evidence | Employee case conversation and per-user thread/memory infrastructure | Bounded answer/proposal; workflow fallback, not all-screen five-skill employee chat | `src/agents/src/zava_forward/agents/chat.py:1-38`; `src/agents/README.md:253-300`; open issue #530 |
| A8 | Evidence | Resident own-record chat, advisory model route and synthetic callback agenda | Explanation and slot proposal; separate explicit synthetic booking/cancellation confirmation. Not works appointment, consent or staff dispatch | Merged PR #525 and open issue #520; channel evidence register |
| A9 | Evidence | Regulatory cards and home-specific extractive lookup | Server-selected excerpts and facts; refuses legal decisions, no model tool or legal approval | `src/agents/src/zava_forward/agents/regulatory_chat.py:1-115`; `src/agents/README.md:67-135,195-225` |
| A10 | Evidence | Deterministic ranking, holds, workflow and sensor admission/DQ; trend analytics remains proposed | Rules/flags, not an additional autonomous agent. Human policy approval and safety service remain distinct | `src/core/src/zava_forward/core/ranking.py:64-142`; `governance.py:1-21`; data/infrastructure evidence register |
| A11 | Evidence | Worker, importer and orchestrator scaffolding | Transport/projection/scheduled bounded processing, not approval or programme-supervisor decision authority | `src/agents/src/zava_forward/agents/dispatch.py:1-9,43-91,157-232`; `src/README.md:36-54`; data/infrastructure evidence register |
| A12 | Unknown | Independent discovery assistant, model training/fine-tuning or autonomous programme supervisor | No current approval or evaluated implementation established; do not infer from architecture aspiration | Original brief; open issue #125; `docs/case_study_48_addendum.md:1505-1530` |

Evidence: all five assistant model requests use inert, closed snapshots and a
JSON proposal schema; permitted field contents can still contain identifying
text. Source IDs/hashes resolve provenance, not semantic entailment.
`src/core/src/zava_forward/core/assistants.py:87-172,223-250,289-344`.
Unknown: actual serving-model versions and training-data provenance beyond
repository configuration; no model training evidence is asserted.

### Data flows and trust boundaries

| Classification | Boundary | Relevant risk and restriction |
| --- | --- | --- |
| Evidence | Synthetic generation/import -> stock/cases/sensors | Constructed records do not validate reality, permissions, lawful basis or physical calibration |
| Evidence | Authenticated resident/employee -> server projection -> model | Login, own-case grant, chat record-use permission, sensor permission and works consent are different authorities |
| Evidence | Model -> citation/schema validation -> proposal review -> ordinary case control | Model prose is untrusted; accepting a proposal does not sign off work or send it |
| Evidence | Local legal snapshots -> cards/lookup -> human interpretation | Quoted source is evidence of recorded wording, not current legal advice or satisfied duty |
| Evidence | Device/register -> ingestion/checkpoint -> SQL -> review signal/UI | Mapping, provenance and admission precede use; missing data is not safety clearance |
| Evidence | SQL/content/history -> audit/telemetry/export/restore | Retained content and immutable history need distinct access, retention and deletion treatment |
| Hypothesis | Future queue/tool/connector -> controlled action | Revalidate purpose, actor, scope, task/release and idempotency at each crossing; never inherit authority from a prompt |

### Risk Classification Screening

Evidence: prohibited-use screening runs first against the local registry:
tenant social scoring, inferring refusal/vulnerability from silence or missing
sensors, consent manipulation, unapproved staff performance/emotion assessment
and model-controlled changes/approvals/sending are prohibited purposes.
`src/core/src/zava_forward/core/ai_registry.py:20-35,87-104`.
Unknown: independent legal screening against current applicable prohibited-use
law. NIST supplies no universal statutory prohibited-use list.

Hypothesis: repository-intended uses do not establish an expressly prohibited
purpose, so continue draft risk analysis while recording legal screening as
unresolved, not a passed legal gate.

| Classification | Planner indicator | Activation and basis |
| --- | --- | --- |
| Evidence | Safety/reliability, binary | Active: hazards, quality and resident safety routing; A5/A8/A10 |
| Evidence | Rights/fairness/privacy, categorical | Active: consent, identity, resident support and missingness; A1/A4/A7/A8 |
| Evidence | Security/explainability, continuous | Active qualitatively: untrusted prompts/sources, cited explanations and release control; no defensible numeric score |
| Hypothesis | Suggested depth | Three active indicators -> Comprehensive under planner screening heuristic, not a NIST legal risk category |
| Unknown | Confirmation | No separate human tier/scope/acceptance confirmation recorded |

## Stakeholder Impact

| Classification | Stakeholder | Benefit hypothesis, harm pathway and decision right |
| --- | --- | --- |
| Hypothesis | Residents, including people with support, language, disability or digital-access needs | Clearer case explanations could reduce effort; inaccessible or falsely reassuring advice could delay help. Residents retain choice and assisted challenge; no inferred refusal |
| Hypothesis | Representatives/households | Explicit scoped grants could support assistance; identity confusion could expose another household. Representation is not a blanket grant or works consent |
| Hypothesis | Housing, Engagement, Safety and Repairs | Evidence-led triage could help; automation bias or unacknowledged referral could delay ownership. Humans own safety decisions and independent emergency routes |
| Hypothesis | Assessors, Coordinators, Quality and contractors | Draft completeness could reduce rework; plausible wrong evidence could contaminate sign-off. Competent independent professionals retain acceptance |
| Hypothesis | Finance, Grants, Programme and executives | Better evidence could support control; fabricated eligibility, costs or benefit claims could misallocate money. Humans retain expenditure/submission authority |
| Hypothesis | Digital, DPO/Legal/Compliance, Assurance and Data | Traceability could support review; overcollection and retained history could increase exposure. Qualified named humans approve interpretation and residual risk |

Evidence: role names are proposed exercise functions, not appointed company
individuals (`docs/case_study_48_addendum.md:150-170,990-1008`).
Evidence: Juan Manuel Servera is explicitly the exercise Legal, Compliance and
DPO owner in `src/agents/README.md:91-95` and
`src/agents/src/zava_forward/agents/regulatory_chat.py:10,83`.
Unknown: actual task/release/incident approvers and professional delegations;
`src/core/src/zava_forward/core/rai_release.py:21-24`.
Hypothesis: route legal interpretation to that named exercise owner and require
the relevant qualified human before operational use; do not appoint fictional
employees or assign professional competence by this document.

## Standards Mapping

| Function | Classification and source | Covered evidence | Outstanding assessment/decision |
| --- | --- | --- | --- |
| Govern: GV-1.1/1.3/1.5/1.6, GV-2.1/2.2, GV-3.2, GV-5, GV-6 | Evidence: addendum RAI gates; registry/release/governance source | Inventory, intended/prohibited use, proposal boundary, versioned admission and baseline-preserving claim register | Unknown: personal validation of authority, approved tolerances/training, privacy/provider terms, legal currentness, representative participation |
| Map: MP-1/2, MP-3.2/3.5, MP-4, MP-5 | Evidence: original/addendum; inventory and stakeholder table | Actual channel differences, missing data, safety/consent boundary and human responsibility are explicit | Unknown: direct resident research, contextual task benefits and actual downstream use. Hypothesis: keep synthetic callback and operational agenda separate |
| Measure: MS-1.1/1.3, MS-2.2-2.11/2.13, MS-3.3, MS-4.2 | Evidence: `src/agents/README.md:67-135,253-300,331-465`; authored tests | Scripted/finite extractive and mutation coverage, explicit known chat grounding blocker, proposed human/cohort protocols | Unknown: held-out real-model correctness, independent adjudication, fairness, comprehension and actual review effort. No overall product pass |
| Manage: MN-1, MN-2.1/2.3/2.4, MN-3.2, MN-4 | Evidence: release/incident/governance source, existing issues #146/#219/#221/#223 | Denial/quarantine/manual continuity and bounded response mechanisms; historical findings remain open | Unknown: approved harm thresholds, staffed escalation, witnessed restart/restore and ongoing provider/model monitoring |

| Characteristic | Classification | Phase 3 tracker status and evidence limit |
| --- | --- | --- |
| Valid and Reliable | Evidence | Mapped / partial: schema and citation checks; unresolved valid-citation false claim, actual-model evaluation unknown |
| Safe | Evidence | Mapped / partial: human hazard route and holds; multilingual/indirect hazard recall and accepted emergency handling unknown |
| Secure and Resilient | Evidence | Mapped / partial: scoped projection/release/finite allowance; semantic injection and live boundary assurance unknown |
| Accountable and Transparent | Evidence | Mapped / partial: provenance, labels and review records; HAX comprehension and named operational authority unknown |
| Explainable and Interpretable | Evidence | Mapped / partial: deterministic reasons/excerpts; generated claim support and resident understanding unknown |
| Privacy-Enhanced | Evidence | Mapped / partial: field contracts and isolation; semantic text minimisation, processor terms and history erasure unknown |
| Fair with Harmful Bias Managed | Evidence | Mapped / gap in outcome evidence: support uncertainty visible; development manifest unapproved, no representative fairness result |

Evidence: the framework pack is embedded workflow reference material, not
external project evidence. Regulatory snapshots are immutable and dated;
`docs/reference/regulatory/README.md:23-90` requires qualified currentness
checks. Unknown: present legal position; no external lookup was authorized,
so no UK/EU classification or compliance conclusion is made.

## Threat Addendum

Evidence: the Microsoft-authored AI STRIDE overlay supplies the taxonomy.
Each scenario below is a Hypothesis, not a verified exploit, incident or
observed injury. Concern is proposed impact priority, not a measured
likelihood. IDs are local to this dated plan; historical `T-RAI-001/002` in
the 2026-10-14 report remain historical and must always be qualified by date.
Unknown: no reusable Security Planner state was found, so no fabricated
`T-{BUCKET}-AI-*` cross-reference is assigned.

| ID | Concern | STRIDE/category | Hypothesis, affected components and outcome | Evidence/control reference |
| --- | --- | --- | --- | --- |
| T-RAI-001 | High | Tampering/output manipulation | A1-A9: false assertion with a valid source ID persuades a reviewer/resident | E03/E04/E06; C01/C04 |
| T-RAI-002 | High | Tampering/prompt injection | A4/A6-A9: question, document or memory text redirects explanation or embeds a false action claim | E03/E04/E06; C01/C05 |
| T-RAI-003 | High | Spoofing/information disclosure | A7/A8: confused identity, stale representative scope or session leaks another household/user's context | E08; C02 |
| T-RAI-004 | High | Elevation of privilege/tool misuse | A4/A8/A11: chat suggestion is mistaken for authorized booking, works consent, sending or domain approval | E02/E03/E08; C03 |
| T-RAI-005 | High | Safety evasion/over-reliance | A8/A10: indirect hazard misses lexical routing; no alert or callback is mistaken for safety-service acceptance | E02/E08/E09; C04 |
| T-RAI-006 | High | Bias amplification/feature uncertainty | A1/A10: Unknown support ranks with No, and incomplete or absent data disadvantages vulnerable residents | E05; C06 |
| T-RAI-007 | High | Information disclosure | A6-A9: allowed free text, model output or immutable history retains personal/sensitive content beyond purpose | E02/E07/E08/E10; C07 |
| T-RAI-008 | High | Tampering/release drift | A1-A11: dependent ranking/checklist/source/model changes outlive an evaluated release | E03/E07/E11; C08 |
| T-RAI-009 | High | Repudiation/oversight failure | A1-A11: structurally complete attestation or audit is mistaken for competent verification, delivery receipt or qualified approval | E03/E07/E09; C09 |
| T-RAI-010 | High | Data poisoning/misuse escalation | A8/A10/A11: synthetic device/stock evidence or derived climate signals are mistaken for real consent, calibration or hazard diagnosis | E09/E10; C10 |
| T-RAI-011 | Medium | Denial of service/resource misuse | A1-A9/A11: provider outage, exhausted allowance or inaccessible loading state blocks usable assistance or pressures manual service | E03/E07/E08/E09; C11 |
| T-RAI-012 | High | Third-party/monitoring failure | All: stale legal sources, provider/image dependencies or unowned alerts permit unsafe reliance despite nominal CI success | E02/E04/E11; C12 |

Unknown: no training pipeline or model checkpoint provenance was established.
Hypothesis: training-data poisoning is a supplier assurance question here;
runtime evidence/source poisoning is the demonstrated architectural exposure,
not evidence that this project trains or retrains models.

## Control Surface Catalog

Evidence: coverage means inspected engineering/documentation coverage, not
operational acceptance. Each control entry is partial unless stated gap.
Hypothesis: residual treatments are proposed and require the backlog's human
owners before activation.

| Control | Threats | Prevent / detect / respond evidence | Coverage and residual |
| --- | --- | --- | --- |
| C01 | 001/002 | Closed snapshots, inert instructions, JSON/schema/citation validation; explicit unknown reconciliation and manual fallback | Evidence: partial, E03/E04/E06. Unknown: claim entailment and real-model injection resistance |
| C02 | 003 | Server-owned identity/projection, current role checks, isolated threads and session boundaries | Evidence: partial, E03/E08. Unknown: full representative/recovery and deployed cross-surface matrix |
| C03 | 004 | Proposal-only provider, separate human controls; explicit synthetic callback confirmation/cancellation | Evidence: partial, E03/E08. Unknown: real connector authorization; no live appointment authority inferred |
| C04 | 001/005 | Human referral/holds, manual help and model-independent warning inside resident chat; safety-focused eval checks | Evidence: partial, E02/E04/E08/E09. Unknown: always-visible urgent route, staffed receipt, multilingual sensitivity and safe under-refusal/false-refusal balance |
| C05 | 002 | History exclusions, narrow memory consent/lifecycle, lexical refusal and action-claim checks | Evidence: partial, E06/E08. Unknown: semantic poisoning resistance; employee grounding blocker remains |
| C06 | 006 | Deterministic versioned policy, Unknown-support reason, drafted paired missingness protocol | Evidence: implementation partial; outcome evidence gap, E05. Unknown: approved policy and fair outcomes |
| C07 | 007 | Closed field contracts, role restrictions, content lifecycle and metadata-only audit patterns | Evidence: partial, E02/E07/E08/E10. Unknown: approved lawful retention, ledger history/backup erasure and per-task text necessity |
| C08 | 008 | Release binding, expiry/revocation, in-flight quarantine and rechecked source signatures | Evidence: partial, E03/E07. Unknown: dependent policy closure; open PR #504 is not baseline implementation |
| C09 | 009 | Explicit source verification then same-reviewer accept, independent quality review, append-only events | Evidence: partial, E03/E07/E09. Unknown: human critical-defect detection and actual delegated authority |
| C10 | 010 | Synthetic provenance/fixtures, sensor admission, human review-only signals, bounded ingestion | Evidence: partial, E09/E10. Unknown: physical validation, per-record provenance completeness and live governance |
| C11 | 011 | Finite attempts/allowance/timeouts, workflow fallback, separate manual callback path | Evidence: partial, E03/E08. Unknown: cold-start comprehension and operational capacity/availability |
| C12 | 012 | Source-change review, task suspension/manual continuity, pinned infrastructure/image definitions | Evidence: partial, E04/E09/E11. Unknown: accepted alert thresholds, supplier review, actual drill and retained unfixed image-risk decision |

### Impact assessment and monitoring

Hypothesis: prioritize safety delay, unauthorized consequential action,
cross-person disclosure and unsupported high-stakes statements before cosmetic
improvements. Unknown: incidence, probability and monetary harm; no fabricated
numeric risk score or benefit estimate is assigned.

Hypothesis: task owners and independent Assurance should evaluate supported
claims, unsafe non-refusals/false refusals, hazard misses, current-source
coverage, role denials, corrections, review effort and accessibility by
approved scenario/cohort. Report numerator, eligible denominator, missingness,
task/model/prompt/policy/source versions, uncertainty and adjudicator. Unknown
or zero eligible evidence is not a passing rate; any safety-critical miss
needs separate disposition. Thresholds, sampling and alert periods remain
unapproved, not invented here.

Evidence: `src/agents/README.md:67-135,253-300,331-465` separates scripted and
extractive checks from actual-model quality and human effectiveness.
Hypothesis: compare the identical task against cards/manual workflow, counting
preparation, correction and review effort, not acceptance clicks alone.
Unknown: representative fairness, calibrated confidence, net benefit and
resident/reviewer comprehension.

Evidence: telemetry-foundations was consulted for audit/measurement planning.
Hypothesis: use existing report fields as evidence first; future instrumentation
should follow OpenTelemetry domain conventions, correlate `trace_id`/`span_id`
and use resource attributes `service.name`, `service.version` and
`deployment.environment`. Do not export prompts, names, email, addresses,
device IDs, health/support narratives or free-text questions into metric
dimensions. Separate access-controlled content/audit stores from diagnostic
telemetry; proposed aggregate RAI measures above are not newly coined telemetry
instrument names. Unknown: deployed instrumentation/retention effectiveness.

Hypothesis: before operational release, record a named incident receiver,
triage/escalation and accessible human contact path; rehearse task suspend,
manual/hazard continuity, communication, evidence-preserving recovery and
separately approved restart. Do not pause emergency handling while waiting for
a model, assessment, data consent or callback.

## Evidence Register

| ID | Classification | Source and verification status | Supports |
| --- | --- | --- | --- |
| E01 | Evidence | `docs/case_study_48_original.md:10-45`; `docs/reference/memory.md:8-17`; `src/README.md:11-54`; inspected, not customer validation | Scope/history; memory is preference context only |
| E02 | Evidence | `docs/case_study_48_addendum.md:23-98,139-170,967-1130,1212-1278,1471-1530`; `docs/reference/regulatory/README.md:23-90`; inspected dated proposals/snapshots | Boundaries, legal and retention uncertainty |
| E03 | Evidence | `src/core/src/zava_forward/core/assistants.py:31-56,87-172,223-250,289-344,995-1046`; `src/api/tests/test_assistants.py:193-278`; inspected source/tests, not rerun here | A1-A5; T001/002/004/008/009/011; C01/02/03/08/09/11 |
| E04 | Evidence | `src/agents/README.md:67-135,195-225,253-300`; `src/agents/src/zava_forward/agents/regulatory_chat.py:1-115`; inspected development evidence, not legal/operational recall | T001/005/012; C01/04/12 |
| E05 | Evidence | `src/core/src/zava_forward/core/ranking.py:64-142`; `stock.py:52-77`; `docs/reference/research/evaluation/cohort-evaluation-review-pack.md:8-140`; inspected source/draft, not fairness findings | T006; C06 |
| E06 | Evidence | `src/agents/tests/test_chat_eval.py:31-106`; `src/agents/README.md:253-300`; inspected tests explicitly retain unsupported-claim blocker | T001/002; C01/05 |
| E07 | Evidence | `src/core/src/zava_forward/core/ai_registry.py:20-104`; `assistant_release.py:15-19,69-134`; `rai_release.py:21-24,45-98`; `export_fields.py:1-103`; `governance.py:1-21,85-185`; inspected source, not appointed authority | T007/008/009/011; C07/08/09/11 |
| E08 | Evidence | Channel source and tests in [bounded evidence lanes](./evidence-lanes.md#resident-and-employee-channels); source inspection plus tracker assertions, not a fresh browser/model run | A7/A8; T003/004/005/007/011; C02/03/04/05/07/11 |
| E09 | Evidence | IoT/orchestrator source and tests in [bounded evidence lanes](./evidence-lanes.md#data-iot-and-infrastructure); inspected source, no cloud/private data | A10/A11; T005/009/010/011/012; C04/09/10/11/12 |
| E10 | Evidence | Synthetic provenance and privacy limits in [bounded evidence lanes](./evidence-lanes.md#data-iot-and-infrastructure); inspected generators/contracts only | T007/010; C07/10 |
| E11 | Evidence | [Tracker snapshot](./tracker-evidence.json), captured `gh issue list`, `gh pr list` and selected `view` evidence; bounded retrieval, not all historical conversations | Unmerged remediation, HAX/employee requests, residual deployment/evaluation acceptance |
| E12 | Evidence | `docs/reference/research/reports/2026-10-14/rai-report-ama-20261014.md:1-85`; inspected historical baseline with planning-only acceptance | No silent closure or replacement of earlier findings |

## Tradeoffs

| Classification | Tension | Proposed decision and residual human ownership |
| --- | --- | --- |
| Hypothesis | Explanation vs privacy | Show scoped source/reason, not hidden support details or another person's data; DPO/task owner approves necessary disclosure |
| Hypothesis | Immutable accountability vs erasure | Keep minimum authorized evidence and separate content/history policy; named Legal/DPO decides each retention/rights exception, not an agent |
| Hypothesis | Fast automated help vs safe reliance | Bounded routine source answers only; consequent/uncertain/safety decisions retain human route. Measure false refusals as well as unsafe answers |
| Hypothesis | Determinism vs fairness | Reproducible order permits audit but does not resolve Unknown-support disadvantage; policy owner and Resident Engagement decide after approved paired evaluation |
| Hypothesis | Consent/data minimisation vs hazard access | Optional model/record use must not disable independent human/emergency reporting; consent types remain separate |
| Hypothesis | Low-friction demo vs identity/production safety | Fake-email/shared-credential showcase is explicitly synthetic, never production identity or delegated representative proof |
| Hypothesis | Rich synthetic coverage vs scientific validity | Keep seeded stress/coverage evidence; do not infer calibration, epidemiology, real cohorts or benefit |
| Hypothesis | Monitoring vs surveillance | Aggregate bounded measurements with restricted diagnostic content; no staff performance/emotion assessment or household profiling by reuse |

## Review Summary

Evidence: all six analytical phases are represented. The
[original independent review](./independent-review.md) and
[local validation/publication record](./validation.md) preserve actual
outcomes separately from qualified acceptance. The durable
[project synthesis](../../../docs/reference/research/rai/project-rai-review.md)
contains the authoritative proposed backlog list with priorities, existing
issue/PR relationships, evidence gates and suggested accountable functions.
No GitHub issue is created; no acceptance checkbox or earlier report is changed.

| Review dimension | Classification | Assessment |
| --- | --- | --- |
| Boundary clarity | Evidence | Inventory covers both sites/chats, briefing, five assistants, deterministic and extractive paths, IoT, data and infrastructure; production unknowns retained |
| Risk coverage | Evidence | Twelve scoped threat hypotheses with local IDs; no invented exploitation, likelihood, training pipeline or legal risk tier |
| Controls | Evidence | Twelve prevent/detect/respond surfaces traced; all partial, with explicit gap in representative outcome evidence |
| Evidence sufficiency | Unknown | Operational correctness, effective oversight, legal/privacy approvals, fairness and direct accessibility acceptance remain unestablished |
| Future governance | Hypothesis | Reuse existing issues before new work; require named holders, version-bound evidence and incident/manual-continuity drill |
| Classification alignment | Evidence | Comprehensive analytic depth follows three active planner indicators; not statutory classification |
| Human acceptance | Unknown | Phase 2/3/6 confirmation and qualified release acceptance not recorded; analytical completion is not approval |

Evidence: signing was not requested; no signature or manifest trust is claimed.
Evidence: required complete local publication gate contains `az bicep`
commands (`tools/rpi-checks.py:1322-1346,1451-1452`) prohibited by this task.
Hypothesis: preserve a local commit and report publication blocked rather than
run forbidden commands, substitute a partial receipt or waive the gate.
Unknown: full exact-head gate and hosted checks until permitted prerequisites
and publication conditions can be satisfied.

Evidence: this assessment is assistive output only. Independent qualified
Legal/Compliance, Safety, privacy, professional and resident review remains
necessary before relying on suggested mitigations. It is not legal advice,
compliance certification, operational release or regulatory sign-off.
