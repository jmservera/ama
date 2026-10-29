---
title: Whole-project Responsible AI review of Zava Forward
description: Repository-only NIST AI RMF review of resident and employee services, bounded agents, chat, IoT, data and infrastructure
ms.date: 2026-10-28
ms.topic: reference
---

## Result and evidence boundary

Evidence: Zava Forward has substantial bounded synthetic engineering controls:
proposal-only assistants, separate human decisions, scoped projections,
explicit model failures, deterministic policies, consent-dependent sensor
admission and audit evidence. Unknown: qualified whole-project operational
acceptance. This review does not establish safety, fairness, accessibility
conformance, privacy approval, legal compliance or measured benefit.

Evidence: this assessment uses NIST AI RMF 1.0, Govern, Map, Measure and
Manage, and the planner's AI STRIDE overlay. It examines baseline
`9bfed51863b05a25e9939d82504c576524688e14`, the fetched `origin/main` when work
began on `docs/rai-review-project`, including merged PR #525. Open PRs are
candidate evidence only. No application source changes, private dataset reads,
secrets/`.env` reads, external research, `az`, Azure or paid model calls were
performed.

Evidence: each assertion is labelled. `Evidence` means inspected source,
test assertions or an attributed repository/tracker record, not proof of
deployed effectiveness. `Hypothesis` means proposed risk, action or acceptance
criterion. `Unknown` means missing or unverified evidence. Table rows inherit
their classification; test-source inspection is not a fresh test run.
Sources are repository paths pinned to the baseline above. Memory was read
for preferences, not treated as evidence.

Evidence: the dated
[six-phase plan](../../../../.copilot-tracking/rai-plans/2026-10-28-zava-forward-project/rai-plan.md),
[source evidence lanes](../../../../.copilot-tracking/rai-plans/2026-10-28-zava-forward-project/evidence-lanes.md),
[tracker evidence](../../../../.copilot-tracking/rai-plans/2026-10-28-zava-forward-project/tracker-evidence.json)
and [state](../../../../.copilot-tracking/rai-plans/2026-10-28-zava-forward-project/state.json)
hold the full inventory, risk screening, seven-characteristic mapping, twelve
threat hypotheses, impact assessment, twelve control surfaces, evidence
register, tradeoffs and local backlog handoff. The explicit end-to-end request
permits draft analytical completion, not invented Phase 2/3/6 confirmation,
human residual-risk acceptance or GitHub issue creation.

Evidence: the [2026-10-14 recovered review](../reports/2026-10-14/rai-report-ama-20261014.md)
remains an earlier, bounded assessment with planning-only owner acceptance.
Its 29 checks, eleven partial findings and eleven unassessed findings are
historical, not this review's score or automatically resolved by new code.
`src/core/src/zava_forward/core/governance.py:85-185` explicitly keeps baseline
evidence claims unverified and findings open.

## Scope and autonomy

| Classification | Surface | Current authority and evidence |
| --- | --- | --- |
| Evidence | Resident site | Synthetic own-case allowlisted showcase; separate loopback representative preview is not production enrolment. `src/api/src/zava_forward/api/resident_demo/app.py:138-173`; `src/core/src/zava_forward/core/resident_showcase.py:515-556`; `resident_preview.py:402-457` in that core directory |
| Evidence | Employee site and briefing | Case work and reading aids with AI/rules/proposal labelling; six retained AI tasks remain alongside five assistants. `src/core/src/zava_forward/core/ai_registry.py:37-61`; `src/api/src/zava_forward/api/web/app.js:275-324` |
| Evidence | Stock Prioritisation | Recommends/explains disclosed evidence gaps; cannot change deterministic ranking. Coordinator/Programme Manager verifies then accepts proposal |
| Evidence | Assessment Preparation | Drafts a completeness checklist; Coordinator/Programme Manager reviews, not professional assessment sign-off |
| Evidence | Funding Evidence | Drafts evidence gaps; Grants and Evidence Officer/Programme Manager reviews, not submission, eligibility or payment |
| Evidence | Works/Resident Coordination | Drafts updates/options from preferences and committed capacity; Coordinator/Liaison/Programme Manager reviews, no sending, scheduling or works consent |
| Evidence | Quality Evidence | Flags discrepancies; Quality Inspector/Programme Manager review includes independence, not quality acceptance |
| Evidence | Five-agent common contract | `src/core/src/zava_forward/core/assistants.py:31-56,87-172,995-1046`; `src/api/tests/test_assistants.py:193-278`. Source verification is separate from accept/edit; generation/review leave controlled domain unchanged |
| Evidence | Employee chat | Existing case panel and per-user thread/memory infrastructure, not yet the all-screen five-skill experience requested by open #530. `src/core/src/zava_forward/core/chat_panel.py:260-304`; `src/agents/README.md:253-300` |
| Evidence | Resident chat and callbacks | Grounded own-record explanation, bounded model guidance and explicit record-use permission. SQLite callback agenda makes separately confirmed synthetic writes; nobody will call. Not works appointments or consent. `src/api/src/zava_forward/api/resident_demo/agenda.py:14-20,158-227`; `resident_demo/app.py:462-529` in that API directory; PR #525 |
| Evidence | Regulatory lookup | Server-selected excerpts and recorded facts, no generative legal conclusions or legal tools. `src/agents/src/zava_forward/agents/regulatory_chat.py:1-115` |
| Evidence | IoT/data | Synthetic register/climate pipeline and SQL admission/DQ checks; readings do not approve safety, ranking or works. `src/core/src/zava_forward/core/sensor_consumer.py:246-265,496-648` |
| Evidence | Infrastructure/jobs | Private/keyless authored controls and bounded explicit jobs; scheduled generic version-printing entrypoint is not programme supervision. `infra/modules/iothub.bicep:95-213`; `src/orchestrator/src/zava_forward/orchestrator/__main__.py:1-3`; `infra/modules/containerapps.bicep:336-374` |

Evidence: the original L2 recommend, L3 draft/act and L4 autonomous-flag
ambitions remain historical in
[original Case Study 48](../../../case_study_48_original.md), lines 26-34.
The [addendum](../../../case_study_48_addendum.md#responsible-ai-release-position-2026-10-14)
narrows current authority to recommend/draft/flag. No model may diagnose,
release holds, infer consent, commit funds, approve professional work, submit
claims, accept quality or close complaints.
Unknown: appointed operational holders and competent delegations
(`src/core/src/zava_forward/core/rai_release.py:21-24`).

## NIST AI RMF assessment

| Function | Classification | Positive evidence | Unresolved evidence and recommended disposition |
| --- | --- | --- | --- |
| Govern | Evidence | Task inventory, prohibited purposes, release validation, audit and manual controls: `src/core/src/zava_forward/core/ai_registry.py:20-104`; `assistant_release.py:69-134`; `rai_release.py:45-98` | Unknown: named authority, legal/privacy/provider acceptance and tolerances. Hypothesis: keep operational release withheld; draft assessment is not approval |
| Map | Evidence | Addendum identifies human/resident boundaries and model-vs-rules division: `docs/case_study_48_addendum.md:967-1013,1471-1530` | Unknown: actual customer baseline, resident participation and contextual outcomes. Hypothesis: explicitly separate preview/showcase, synthetic callback and operational service |
| Measure | Evidence | Scripted/finite extractive and mutation evaluations, explicit unresolved chat grounding case: `src/agents/README.md:67-135,253-300`; `src/agents/tests/test_chat_eval.py:31-106` | Unknown: independently held-out actual-model correctness, human effectiveness, fairness and direct accessibility/comprehension. Hypothesis: evaluate each path and policy with version-bound evidence, not aggregate acceptance clicks |
| Manage | Evidence | Denial/quarantine, source rechecks, manual continuity and constructed incident/restart mechanisms: `src/core/src/zava_forward/core/assistants.py:995-1046`; `assistant_release.py:69-149`; issues #146/#219/#221 | Unknown: approved harm thresholds, receiver capacity, witnessed restore/restart and actual service response. Hypothesis: named drills and evidence-linked gates before expansion |

Hypothesis: Comprehensive assessment depth is appropriate because all three
planner screening indicators activate: safety/reliability,
rights/fairness/privacy and security/explainability. This is a planner
heuristic, not a NIST-prescribed score or statutory risk tier. Evidence:
intended purposes exclude social scoring, consent manipulation and model
action authority (`src/core/src/zava_forward/core/ai_registry.py:20-35`).
Unknown: current legal prohibited-use/applicability determination.

Evidence: all seven trustworthiness characteristics are mapped in the plan.
Validity, safety, resilience, transparency, explanation and privacy have partial
engineering evidence; fairness has a material outcome-evidence gap.
Unknown: no characteristic has qualified whole-project acceptance.

## Material gaps and contradictions

| ID | Classification | Observation, impact boundary and evidence |
| --- | --- | --- |
| F01 | Evidence | Resident hazard detection is finite English matching; lane inspection identifies "My ceiling is collapsing in my home" reaching ordinary home-topic handling. Urgent warning is inside initially hidden chat, not proven always-visible site-wide. `src/api/src/zava_forward/api/resident_demo/chat.py:28-38,40-185`; `resident_demo/web/assistant.js:200-204,273-276`. Hypothesis: missed reports could delay help; no observed injury or measured miss rate |
| F02 | Evidence | Employee citation parsing checks allowed IDs, not entailment; the golden suite deliberately retains unsupported-claim-with-valid-citation as a critical enablement blocker. Generic `/messages` uses a different path from cited `/ask`. `src/core/src/zava_forward/core/chat_panel.py:136-180,223-240`; `chat_isolation.py:114-137`; `src/api/src/zava_forward/api/server.py:674-677`; `src/agents/tests/test_chat_eval.py:31-106`. Unknown: actual-model semantic assurance |
| F03 | Evidence | Broad "Workflow only ... for my AI requests" wording accompanies briefing mode, while `/ask` carries no corresponding preference. `src/api/src/zava_forward/api/web/app.js:275-324`; `web/chat.js:43-54`; `server.py:469-470,674-677`. Hypothesis: expectation mismatch, not a demonstrated paid-dispatch bypass |
| F04 | Evidence | HAX-focused loading/briefing work is an open owner request (#531), not delivered acceptance. AI/rules/source distinction, claim references, meaningful action wording, refresh and correction require a trace. Existing labels do not establish understood capability/limits. Unknown: toolkit guideline-ID verification; no external HAX source was fetched |
| F05 | Evidence | Login, record-use permission, representative scope, monitoring choice and works consent are distinct. Withdrawing chat record use does not cancel a synthetic reservation; cancellation marks it cancelled, not erased. Sensor withdrawal blocks new admission but accepted replay may remain a historical receipt. `src/api/src/zava_forward/api/resident_demo/web/assistant.js:118-139,170-175`; `resident_demo/agenda.py:203-227`; `src/core/src/zava_forward/core/sensor_consumer.py:562-594`. Unknown: accepted cross-store withdrawal/retention lifecycle |
| F06 | Evidence | Unknown support receives a human-review reason but sorts with No in the boolean priority key. Draft paired/cohort protocol remains unapproved and not fairness evidence. `src/core/src/zava_forward/core/ranking.py:64-87,114-128`; `stock.py:52-77`; `docs/reference/research/evaluation/cohort-evaluation-review-pack.md:8-140`. Hypothesis: incomplete recording can disadvantage people; not proof of unlawful discrimination |
| F07 | Evidence | Field allowlists constrain shape, not semantics of names/adjustments/free text. Chat redaction is best-effort, memory expiry is not a message policy, referred copies survive sender deletion. Audit content removal and later full-content retention directions remain subject to DPO resolution. `src/core/src/zava_forward/core/export_fields.py:1-103`; `chat_privacy.py:36-79,122-157,329-346`; `docs/case_study_48_addendum.md:1258-1278`; `src/api/README.md:1405-1420`. Unknown: approved erasure/hold/backup reconciliation |
| F08 | Evidence | Source has release gates, but dependent ranking/checklist binding correction remains open PR #504, not baseline delivery. Formal source verification can record a person's attestation without proving their competence or that wrong text was detected. `src/core/src/zava_forward/core/assistants.py:296-308,995-1046`; #219/#223/#504. Unknown: actual approved release and oversight effectiveness |
| F09 | Evidence | Reproducible sensor/fault fixtures are not calibration or resident evidence; private geography may use real map anchors. Pattern checks and three historically incomplete provenance entries do not establish all-data PII absence or rights clearance. `src/core/src/zava_forward/core/synthetic/indoor_projection.py:10-42`; `synthetic/privacy.py:139-159,214-285`; `docs/reference/research/retrofit-synthetic-data/README.md:37-45`; `provenance-register.json:24-51` in that research directory |
| F10 | Evidence | Sensor IDs/contract lengths, dated-effect delivery and versions differ between older addendum/dictionary text and newer implementation. Digest module says locked while Bicep creates unlocked retention. `docs/case_study_48_addendum.md:1435-1438`; `docs/reference/research/iot-sensor-analytics-research-plan.md:62,328-335`; `docs/reference/research/retrofit-synthetic-data/data-dictionary.md:414-433`; `src/core/src/zava_forward/core/synthetic/sensor_identity.py:9-23`; `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py:3-4`; `infra/modules/storage.bicep:75-81`. No silent reconciliation or historical result promotion |
| F11 | Evidence | Separate identities coexist with account-scoped storage grants, API DDL rights and API-identity digest job. Defaults for backup/soft-delete/log/audit retention are infrastructure settings, not approved legal periods. `infra/main.bicep:242-247`; `infra/modules/storage.bicep:96-103`; `infra/scripts/create-sql-users.py:21-24`; `infra/modules/containerapps.bicep:377-415`. Unknown: deployed effective least privilege and accepted retention/first anchor |
| F12 | Evidence | Native controls, manual alternatives and prior automated browser/axe evidence coexist with unrun AT/human acceptance. PR #525 reports contrast incompletes and unfixed image findings despite passing its fixable-only gate. `docs/reference/research/ux/wcag-conformance-baseline.md:120-132,192-207`; `src/api/checks/resident_assistant_browser_check.py:620-626`; PR #525. Unknown: WCAG conformance, understood sources/consent and residual dependency-risk acceptance |
| F13 | Evidence | Import quarantine synthetic labels/export notes are not source-provenance enforcement; export library accepts caller-supplied rows. Generic importer/orchestrator entrypoints are scaffolding, not integrated autonomous workers. `src/importer/src/zava_forward/importer/quarantine.py:77-85`; `export.py:17-21,36-42,64-75`; `src/importer/src/zava_forward/importer/__main__.py:10-23`; `src/orchestrator/src/zava_forward/orchestrator/__main__.py:1-3`. Unknown: authenticated end-to-end admission/export controls |
| F14 | Evidence | Closed issue state is not independent acceptance: `tools/backlog-sync.py:72-80` can tick criteria from state alone. #521's extension request does not prove a changed runtime cutoff; open #530/#531 are not merged functionality. Hypothesis: require receipts and named decisions rather than tracker state |

## Proposed backlog handoff

Hypothesis: this list is the local handoff, not new issues, approved
requirements or assigned people. High/Medium denote proposed review priority
before real-user reliance, not exploit severity. Suggested functions require
named human acceptance; do not duplicate existing work or import open-PR code.
Threat IDs below are local to the dated plan, not historical finding closure.

* Hypothesis: B01, High, human safety path and resident hazard recall
  (F01, T-RAI-005; Refs #520, #164, #85). Housing/Safety and Engagement should
  approve visible urgent help outside closed chat and test indirect,
  multilingual, typo and mixed-purpose reports, no-AI/no-record-use and outage
  scenarios. Demonstrate explicit human referral/receipt semantics; never
  imply an alert, diagnosis or safe home from callback/no sensor signal.
* Hypothesis: B02, High, uniform grounding and no-AI contracts
  (F02/F03, T-RAI-001/002/004; Refs #164, #159, #530, PR #503).
  Digital/task owners should test `/ask` and `/messages`, exact source
  freshness, unsupported claims with valid IDs, memory poisoning, false action
  claims and consistent workflow-only choice. Record actual-model evidence
  separately from scripted cases; retain the known blocker until justified.
* Hypothesis: B03, High, consent/representation/action matrix
  (F05, T-RAI-003/004; Refs #86, #162, #441, #520). Engagement/DPO/Digital
  should test person/case/task grants, representative revocation/recovery,
  separate record/monitoring/works choices, callback confirmation/cancel and
  assisted parity. Explain that record-use withdrawal does not erase/cancel
  prior records. No synthetic booking becomes an operational appointment.
* Hypothesis: B04, High, approved retention and erasure/restore
  (F05/F07, T-RAI-007/009; Refs #121, #163, #217, #117).
  Named DPO/Legal/record owners should inventory chat/messages/memory,
  referral copies, callbacks, sensor readings/rejected deliveries, exports,
  SQL ledger history, Blob versions/logs/backups; decide purpose/retention/hold
  exceptions and test removal or documented lawful retention plus deletion
  reapplication after restore. Do not copy private content into diagnostics.
* Hypothesis: B05, High, fairness and missing-data policy
  (F06/F09, T-RAI-006/010; Refs #222, #108, #128).
  Data/Resident Engagement/Assurance/DPO should approve policy/cohort fields,
  independent custody/labels and paired support/sensor/source/contact/access
  scenarios before evaluation. Report denominators, uncertainty, missed safety
  cases and review burden; decide Unknown-support treatment explicitly.
  Published development fixtures cannot become held-out evidence.
* Hypothesis: B06, High, named release and meaningful oversight
  (F08, T-RAI-001/008/009; Refs #219, #223, #218, PR #504).
  Programme, competent task owners and independent Assurance should validate
  delegated holders, dependent policy/checklist/model/prompt/permission
  invalidation and renewal; separately test whether reviewers detect plausible
  wrong/stale/incomplete output against workflow-only total effort.
  Source-verification clicks and synthetic release records cannot pass.
* Hypothesis: B07, High, versioned sensor consent and safety validation
  (F05/F09, T-RAI-005/010; Refs #110, #111, #112, #177, #184, #190, PR #508).
  Data/Safety/DPO should bind actor/purpose/notice/control revision, test
  withdrawal through credentials/transport/derived copies, and separately
  approve calibration/freshness/sufficiency and review-signal error analysis.
  Label historical replay correctly and retain equal non-monitoring service.
* Hypothesis: B08, High, owned monitoring/incident/manual-continuity drill
  (F08/F11/F12, T-RAI-009/011/012; Refs #146, #221, #122, #145).
  Digital/Safety/task owners should approve measures, thresholds, observation
  windows and alert receivers; witness suspend, accessible manual handling,
  independent hazard access, notification, recovery and authorized restart.
  Report supported claims, unsafe/false refusals, coverage, corrections and
  total effort by approved cohorts; use bounded aggregate telemetry, not
  questions, identifiers or support narratives as metric dimensions.
* Hypothesis: B09, Medium, HAX transparency and task accessibility
  (F04/F12, T-RAI-001/009/011; Refs #531, #128, #149, #119).
  UX/Engagement/Assurance should map the locally requested HAX behaviors to
  each surface: capability/limits, AI vs rules/data, statement sources,
  refresh, mismatch, outcome-labelled review/correction and safe undo.
  Verify loading/fallback manually and with automated checks; obtain
  task-based screen-reader/voice-control/zoom and resident comprehension
  evidence separately. Toolkit source verification remains pending under this
  repository-only review, not assumed complete.
* Hypothesis: B10, Medium, trusted synthetic provenance and importer integration
  (F09/F13, T-RAI-002/007/010; Refs #165, #172, #175, #174).
  Data/DPO/Assurance should reconcile source rights/retrieval, enforce
  synthetic admission before cloning/relabelling, bind importer reviewers to
  authenticated identities and gate exports. Independently adjudicate labels;
  document that pattern scans are not universal DLP or calibrated reality.
* Hypothesis: B11, Medium, least privilege and infrastructure assurance
  (F11/F12, T-RAI-003/007/009/012; Refs #140, #141, #138, #118).
  Digital/security/record owners should justify table/container rights,
  first-anchor/retention-lock decisions and effective route denial; separately
  record provider processing/transfer and retained unfixed image risks.
  Any later live verification needs explicit authority; no Azure action is
  requested or authorized by this handoff.
* Hypothesis: B12, Medium, reconcile evidence and legal/expiry gates
  (F10/F14, T-RAI-008/009/012; Refs #224, #194, #521, #126).
  Documentation/task owners should reconcile current contract/version text
  with exact source and preserve adverse/historical outcomes; evidence-link
  every acceptance rather than infer it from closed issues. Juan Manuel
  Servera, named exercise Legal/Compliance/DPO owner, should obtain qualified
  dated official-source/currentness/applicability decisions and route affected
  requirements/tests for approval. Record approved expiry/rotation changes
  before reliance, not merely the request.

## Human review and publication boundary

Evidence: Juan Manuel Servera is named as exercise Legal, Compliance and DPO
owner in `src/agents/src/zava_forward/agents/regulatory_chat.py:10,83`
and `src/agents/README.md:91-95`. Unknown: actual company appointees,
professional competence/delegations and accepted release/incident holders.
Hypothesis: legal interpretation remains with named qualified humans, not
this review or role agents.

Evidence: the [regulatory register](../../regulatory/README.md), lines 23-90, treats
local copies as dated snapshots requiring currentness checks before
consequential use. Unknown: present legal position. This review deliberately
does not refresh official sources, activate rules, infer EU territorial
applicability or derive statutory clocks from exercise targets.

Evidence: complete local publication validation requires `az bicep` commands
in `tools/rpi-checks.py:1322-1346,1451-1452`, while this task prohibits `az`
and Azure. Hypothesis: retain a local Conventional Commit and report publication
blocked rather than execute forbidden commands, downgrade the mandatory gate
or claim a passing receipt. Unknown: complete exact-head gate, independent
publication assessment and hosted approval until the publication conditions
can be met.

Evidence: the [original independent review](../../../../.copilot-tracking/rai-plans/2026-10-28-zava-forward-project/independent-review.md)
found no blocking or nonblocking issues in its representative sample.
The [validation record](../../../../.copilot-tracking/rai-plans/2026-10-28-zava-forward-project/validation.md)
preserves an initial citation-bound failure, mechanical corrections and
passing local documentation checks. Neither is a qualified human approval,
complete product evaluation or exact-head publication receipt.

Evidence: this is assistive planning, not legal advice, compliance
certification, qualified RAI sign-off or approval to expose real residents.
Independent human review and the owner's merge decision remain separate.
