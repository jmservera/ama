---
title: RAI Remediation GitHub Issues Plan
description: Source of truth for proposed body-only updates to reusable issues
ms.date: 2026-10-15
ms.topic: reference
---
<!-- markdownlint-disable-file -->
<!-- markdown-table-prettify-ignore-start -->

## Plan Contract

Destination: GitHub jmservera/ama. Autonomy: partial. Lens: generic platform-native.

Source commit: 7a8b1fe65475752fcf242ed52acab8e7e43b58d3.

Sources:

* [Merged remediation plan](../../../plans/2026-10-15/rai-remediation-plan.md).
* [Bounded baseline report](../../../rai-reviews/2026-10-14/rai-report-ama-20261014.md).
* [PRD v0.16.0](../../../../docs/prds/zava-forward-retrofit-programme-demonstrator.md).

This plan proposes twelve body-only Updates. It does not authorize execution. Current issue titles, OPEN states, null native types, labels, null milestones and empty assignee sets remain unchanged. No priority field, due date or owner is invented.

Each item is Similar and needs_review. Body additions below are proposed acceptance conditions, not statements that tests or approvals have passed. All checkboxes remain unchecked.

## Operation Register

| Ref | Action | Existing issue | Remediation tasks | Body delta |
| --- | --- | --- | --- | --- |
| IS001 | Update | 105 | P01-T01 | Whole-system impact and authority |
| IS002 | Update | 121 | P01-T02 | Processing/retention manifest and current staff scope |
| IS003 | Update | 116 | P02-T01 | Every provider-boundary minimization |
| IS004 | Update | 106 | P02-T02, P03-T02 | Provenance, factual review and meaningful oversight |
| IS005 | Update | 107 | P03-T01 | Durable release admission and invalidation |
| IS006 | Update | 146 | P04-T01 | Owned harm indicators |
| IS007 | Update | 122 | P04-T02 | Incident suspension and controlled restart |
| IS008 | Update | 130 | P05-T01 | Accessible AI challenge/correction |
| IS009 | Update | 128 | P05-T02 | Cohort and missing-data impact evidence |
| IS010 | Update | 108 | P06-T01 | Held-out, human and net-benefit evidence |
| IS011 | Update | 145 | P06-T02 | Witnessed backup and erasure reconciliation |
| IS012 | Update | 126 | P06-T03 | Qualified current-version closure |

## Body Composition Rules

For each target:

* Re-read the current body and preserve unrelated scope, criteria and history.
* Insert the common block below, followed by that item's specific block, before its existing Dependencies section.
* If equivalent RAI criteria have appeared since the snapshot, reconcile rather than append duplicates.
* Make only the specifically identified factual-status corrections below; do not infer a delivery-label or state change.
* Expand the common block into the actual body. Do not send this plan's headings, IS references, local tracking paths or operational instructions to GitHub.
* Existing native relationship fields are untouched. Any dependency prose added by this plan describes prerequisites, not a native Link operation.
* Semantic PRD and RAI finding IDs may remain. They are traceability identifiers, not local planning references.

### Common Outbound Block

## RAI Delta Scope

Extend the existing capability with the Responsible AI contract in docs/prds/zava-forward-retrofit-programme-demonstrator.md, version 0.16.0, at source commit 7a8b1fe65475752fcf242ed52acab8e7e43b58d3.

Use the existing API, SQL state and bounded assistant runtime. Do not add a governance service or transfer resident, safety, professional, ranking, financial or release authority to AI.

The bounded RAI report accepted on 2026-10-15 is a planning baseline, not implementation acceptance, legal/privacy approval or operational release. Constructed fixtures permit safe offline development, not actual human authorization. Live use remains blocked until applicable evidence and qualified approvals exist.

## IS001 - Update issue 105

Current title: AI task registry and proposal envelope.

Current labels: feature, prd, area:ai, status:partially-delivered. Retain all.

Factual-status correction: distinguish the existing five-capability source registry from unverified whole-system coverage and personal acceptance; do not continue to describe the entire registry as simply absent or unconfirmed.

Specific outbound block:

## RAI Impact and Authority Acceptance Criteria

* [ ] Inventory all five assistants and retained briefing, message, summary, priority, funding and document-reading paths, with task purpose, intended/prohibited uses, influence, affected residents/staff/providers and exercise/live scope.
* [ ] Each task records an accountable ownership function, impact/residual-risk record, permissions, review responsibility and required approval evidence. An unknown individual or delegation stays unknown and cannot authorize activation.
* [ ] Actual task, Assurance, Safety and DPO/Legal delegates personally validate their own authority where applicable. Role-agent output and fixture approval cannot substitute.
* [ ] Prohibited purposes include tenant social scoring, inferred refusal/vulnerability from silence or missing sensors, consent manipulation and unapproved staff performance/emotion assessment.
* [ ] Dated qualified UK and conditional EU intended-use, actor-role, influence and currentness review is required before affected operational reliance; housing or hosting location alone does not determine applicability.
* [ ] Owner acceptance of the bounded report, current PRD acceptance, task/control acceptance and operational release are recorded separately.
* [ ] Missing authority denies affected activation while permitting constructed offline scaffolding and independent manual/hazard work.

## RAI Prerequisites

The inventory supplies processing manifests and release admission. Qualified personal/legal decisions gate affected real processing and activation, not safe synthetic implementation.

Local trace: GOVERN-AUDIT-01/05, MAP-02/05, EU-COND-01/02, FR-036/051, AC-069. Review whole-system registry boundary before execution.

## IS002 - Update issue 121

Current title: Data protection, retention and rights controls.

Current labels: feature, brd, prd, adr, area:platform, status:partially-delivered. Retain all.

Factual-status correction: replace the unqualified current assertion that the demonstrator holds constructed data only with a distinction between constructed residents and actual staff/tenant identities and review records. Preserve dated historical observations.

Specific outbound block:

## RAI Processing and Retention Acceptance Criteria

* [ ] Map current staff/tenant identities and review records separately from constructed resident fixtures and any future real resident processing.
* [ ] Cover inputs, raw document/image bytes, prompts, outputs, citations, reviewer identity, audit, telemetry, tokens, provider processing and retained copies.
* [ ] Every task declares purpose/audience, permitted field names/types/lengths, prohibited content and minimum-necessary rationale. User permission alone does not establish task necessity.
* [ ] DPO/Legal and record owners approve applicable purpose/lawful authority, processor/region/transfer, retention, legal hold, erasure, representative authority and provider-copy treatment before affected actual processing.
* [ ] Permission to upload/store/download does not approve sending intact material to AI. Use an authorized reviewed/redacted derivative or an explicitly scoped necessity approval; otherwise deny model dispatch and preserve manual handling.
* [ ] Synthetic resident content does not remove actual staff processing from privacy scope; UK application hosting does not prove UK inference residency.
* [ ] Retention, erasure, audit and restore decisions are explicit and owned. Local deletion is not represented as provider erasure.
* [ ] Entirely constructed fixtures remain the development path where actual-processing approval is absent.

## RAI Prerequisites

Consume the whole-system inventory. Resolve DH-001, DH-002, DH-006 and DH-007 with qualified owners; no legal conclusion or retention period is invented.

Local trace: MAP-02, GOVERN-AUDIT-04, NFR-003/005. Keep existing rights criteria; legal interpretation remains qualified human work.

## IS003 - Update issue 116

Current title: Entra ID sign-in, roles and field-level visibility.

Current labels: feature, prd, adr, area:platform, status:partially-delivered. Retain all.

Specific outbound block:

## RAI Provider-Boundary Acceptance Criteria

* [ ] Apply approved task/audience field, type and size allowlists at every provider boundary, including Ai.run/_chat, Ai.evidence, Ai.look_at, document/image bytes, retained legacy families, reactive assistants and proactive scans.
* [ ] Provider-spy tests assert exact permitted payload content per role and path, including nested structures, free text, identifiers and citations, with zero hidden-field canaries.
* [ ] Unknown task/field, excessive input and unapproved raw content fail visibly before any provider call.
* [ ] Recheck permissions on outputs, citations, explanations, errors, review records and exports; input filtering alone cannot pass.
* [ ] Document AI processing requires the approved derivative or scoped necessity exception. Storage, manual reading and permitted download remain available when model processing is denied.
* [ ] Tests preserve source permissions, proposal-only writes, resident consent and independent manual/hazard routes.
* [ ] Reuse the current capture/projection/provider wrappers rather than create a parallel serializer or inference service.

## RAI Prerequisites

Use the task inventory and approved processing manifests. Offline tests use constructed payloads and isolated mocked providers, not inherited real endpoints.

Local trace: T-RAI-001, AC-053/054/060, NFR-003/005. Contractor privacy criteria remain mandatory, but contractor-only testing is insufficient.

## IS004 - Update issue 106

Current title: Suggestions, accept or reject with reason, and workflow-only fallback.

Current labels: feature, prd, area:ai, status:partially-delivered. Retain all.

Specific outbound block:

## RAI Provenance and Meaningful Review Acceptance Criteria

* [ ] Retain source identity, locator, content hash, version, origin and authorized verification separately from citation resolution. Pinned bytes and resolving references do not establish authenticity or truth.
* [ ] Accept/edit atomically rechecks actor permissions and current source, proposal and release revisions. Altered, unattributed, unauthorized, conflicting or changed originals create a visible owned hold/review.
* [ ] Distinguish citation-resolved, source-verified and human-reviewed states. Another AI verdict, filename or signature-shaped text cannot establish factual correctness.
* [ ] Constructed cases cover forged/altered sources, embedded instructions, plausible false claims with valid citations, stale/unsupported/incomplete proposals and correct controls.
* [ ] Source-based review retains reviewer, source/proposal/release versions, comparison, accept/edit/reject disposition and reason, with existing reviewer independence and domain approvals preserved.
* [ ] No seeded critical wrong, stale, unsupported or incomplete claim can satisfy a controlled gate. No default or bulk acceptance is allowed.
* [ ] Authorized competent human exercises demonstrate detection of every seeded critical defect and report corrections plus complete review effort against the same workflow-only scenarios.
* [ ] Offline gating, source-verification attestations and role-agent output are not reported as demonstrated human competence.
* [ ] Review races and exports preserve consent, ranking, work release, claim/payment, quality and hazard boundaries; template/manual fallback is not model success.

## RAI Prerequisites

Use minimized inputs, source authority and durable release admission. Engineering checks may precede authorized human evidence, but cannot close that evidence gate.

Local trace: P02-T02 and P03-T02 combined; T-RAI-002, MEASURE-01, MAP-04, AC-060/070, FR-026/027 and NFR-009. Do not duplicate the full evaluation experiment in this issue.

## IS005 - Update issue 107

Current title: Five reactive and proactive assistants on one proposal service.

Current labels: feature, prd, adr, area:ai, status:partially-delivered. Retain all.

Factual-status correction: replace the README-absence inference with bounded current evidence: the report/source identify five registered service paths and dated feasibility observations, but not approved release admission, human effectiveness or operational acceptance.

Specific outbound block:

## RAI Release Admission Acceptance Criteria

* [ ] Persist a release record binding task/purpose, provider/endpoint/deployment/actual serving-model version, prompt/policy/data/provenance/permission versions, evidence, authorized approver, residual-risk decision and expiry.
* [ ] Absent, expired, suspended, revoked or materially mismatched releases deny reactive/proactive and retained legacy dispatch with zero unauthorized provider calls; expose missing evidence, owner and manual route and retain the denial.
* [ ] Obtain authoritative serving-version attestation rather than treating a deployment alias as immutable. Unexpected returned versions quarantine results and suspend the release.
* [ ] Recheck admission and dependent versions through claim, retry, dispatch, completion, list/detail, review and export reliance.
* [ ] Independent SQL connection/worker and race tests cover material mismatches, revocation and restart. Old images/restarts cannot restore revoked approval or replenish finite allowances.
* [ ] Distinguish routine case edits, which stale exactly dependent proposals, from material purpose/model/prompt/policy/schema/provenance/permission changes requiring renewed release evidence.
* [ ] Preserve default-off authority, purpose principal restrictions, SQL deduplication/leases, source permissions and no controlled-domain writes.
* [ ] A matching approved exercise record permits bounded proposals only. Delivered-build acceptance still requires version-linked real AI, actual SQL and Azure evidence under CON-009/AC-057.
* [ ] Metadata access is not paid-inference authorization; missing serving proof or scoped approval keeps actual activation denied.

## RAI Prerequisites

Consume impact/processing manifests, minimized inputs and source assurance. Reuse additive current SQL/control contracts; no new service, queue or assistant.

Local trace: GOVERN-AUDIT-02, MN-3.2, T-RAI-005, FR-051, AC-069, NFR-014.

## IS006 - Update issue 146

Current title: Monitoring coverage: alerts, dashboards and runbooks.

Current labels: story, adr, area:infrastructure, status:partially-delivered. Retain all.

Specific outbound block:

## RAI Harm Monitoring Acceptance Criteria

* [ ] Each task/serving release declares applicable harm/quality/disparity/review-burden indicators, denominators, observation window, thresholds, accountable monitoring/incident owners and response.
* [ ] Include unsupported claims, critical misses, stale review attempts, challenges, cohort errors and complete review effort where applicable.
* [ ] Missing samples, usage, approvals or thresholds display insufficient/blocked rather than zero or green. Approval rate is not safety evidence.
* [ ] Seeded critical harm or an approved threshold breach creates an owned incident and invokes task suspension.
* [ ] Reconcile windows, denominators and repeated events across restart. Disabled tasks still expose monitoring ownership and manual-route status.
* [ ] Telemetry excludes raw prompts/source text, sensitive reasons, tokens and unnecessary identities; permitted restricted evidence is retained separately.
* [ ] Constructed thresholds support offline tests only; live thresholds require explicit named-human approval.
* [ ] Implement through existing audit/report/UI surfaces without adding an observability platform or requiring unrelated future IoT delivery.

## RAI Prerequisites

Consume current release/review records and the incident-control path. Preserve existing infrastructure alert/runbook criteria.

Local trace: MN-4.1 and NFR-014. Review this task-level subsection's fit within the broader infrastructure monitoring issue.

## IS007 - Update issue 122

Current title: Service continuity, versioning, exportability and integration.

Current labels: feature, brd, area:platform, status:partially-delivered. Retain all.

Specific outbound block:

## RAI Incident and Restart Acceptance Criteria

* [ ] Persist task/release suspension, incident owner, affected proposal/version set, containment, communication owner/audience and restart decision.
* [ ] Recheck suspension epoch at invoke/scan/claim/dispatch/complete and list/detail/review/export reliance; server enforcement does not depend on disabled buttons.
* [ ] Independent SQL connection, concurrent suspend/review, race and restart tests cover queued, leased and ready proposals and old-image restart.
* [ ] In-flight calls may complete and remain charged/unknown; late results are quarantined and cannot become actionable. Do not claim remote cancellation or exactly-once billing.
* [ ] Corrective evidence and distinct authorized human approval gate restart. Replayed, stale, self-approved or unauthorized restart fails.
* [ ] Preserve reconstructable permitted history without current reliance.
* [ ] Manual case work, accessible challenge and independent hazard response remain available during suspension.
* [ ] A witnessed authorized drill exercises suspension, owned communication responsibility and restart. Constructed templates do not send live notices or contact residents automatically.

## RAI Prerequisites

Use approved authority, current release state and owned monitoring. Operator identity alone does not establish restart authority.

Local trace: MN-4.3, FR-053, AC-072 and NFR-014. Existing continuity/export/versioning criteria remain.

## IS008 - Update issue 130

Current title: Nomination, self-referral, acknowledgement and challenge route.

Current labels: feature, brd, area:safety-consent, status:not-started. Retain all.

Specific outbound block:

## RAI Challenge and Correction Acceptance Criteria

* [ ] Link a supplied constructed challenge/correction to relevant source, policy/proposal and human-decision versions, with a human owner, next-update commitment and resolution evidence.
* [ ] Provide permitted plain-language explanation of AI involvement, sources/policy reasons, uncertainty and human decision ownership.
* [ ] Exercise digital and equivalent staff-recorded non-digital routes, including keyboard access and field-permission checks.
* [ ] Correction stales exactly dependent proposals/reviews, preserving prior versions and unrelated decisions.
* [ ] No challenge, silence, sensor absence or correction infers consent/refusal, vulnerability, sanction, complaint closure or hazard-clock change.
* [ ] Preserve representative task limits and open-remedy protections in AC-063/064. Generic AI challenge does not resolve nomination-specific FR-037/OD-41/OD-42.
* [ ] Representative participation and comprehension require authorized human evidence; constructed UI checks alone cannot pass that gate.
* [ ] Nothing is sent, booked or approved automatically.

## RAI Prerequisites

Use minimized sources, provenance, release and suspension controls. Retain original nomination/self-referral scope and its unresolved authority decisions.

Local trace: MEASURE-03, MAP-04, FR-052/043, AC-071.

## IS009 - Update issue 128

Current title: Accessibility, equity and journey ownership testing.

Current labels: feature, brd, prd, area:governance, status:partially-delivered. Retain all.

Specific outbound block:

## RAI Cohort Acceptance Criteria

* [ ] Predeclare independently expected paired constructed cohorts differing in source/sensor completeness, accessibility/contact needs and provider-versus-resident appointment history while holding relevant facts constant.
* [ ] Evaluate deterministic prioritisation and AI tasks; preserve named ranking-policy ownership, hash/order approval and transparent non-AI comparison.
* [ ] Missing/declined sensors and non-response never lower service or priority; do not infer vulnerability, refusal or protected characteristics.
* [ ] Retain cohort/version definitions and eligible, tested, abstained and failed counts, sufficiency, subgroup errors/exclusions, review burden, uncertainty and human disposition.
* [ ] Detect every seeded unjustified exclusion/deprioritisation defect. A failing subgroup cannot be averaged away.
* [ ] Unapproved thresholds, missing/small samples or exceeded thresholds block affected activation pending human disposition.
* [ ] Use protected-characteristic fields only with lawful minimum-necessary approval. Generated cohorts do not establish population fairness.
* [ ] Include geography/archetype where approved and relevant. Sensor completeness fixtures do not provision devices or invent hazard/dew-point thresholds.

## RAI Prerequisites

Use lawful processing fields, minimized inputs, current releases and the accessible challenge route. Ranking owners approve policy; evaluation does not ratify it. Future IoT Hub ingestion and unresolved sensor research remain separate.

Local trace: MAP-01, MEASURE-03, FR-054/012, AC-073, NFR-012/014.

## IS010 - Update issue 108

Current title: AI evaluation harness and model selection.

Current labels: feature, prd, adr, area:ai, status:partially-delivered. Retain all.

Specific outbound block:

## RAI Held-Out and Human Evidence Acceptance Criteria

* [ ] Freeze task/model/prompt/policy/source versions, an independently labelled held-out split, expected outcomes, critical errors, cohorts, sufficient samples and approved thresholds before evaluation. Held-out answers never enter prompts or tuning.
* [ ] Cover all five assistants and each retained legacy family, correct controls, ambiguity, abstention, source integrity and factual support.
* [ ] Record critical errors/misses, usable coverage, subgroup results and applicable calibration. If meaningful scored predictions are absent, document calibration as not applicable rather than inventing it.
* [ ] Authorized competent human participants detect and block every seeded critical wrong/stale/unsupported/incomplete proposal, including valid-citation errors.
* [ ] Compare full preparation, checking, correction, re-review, coordination, resident and support effort and cost against manual/template and parser/rules alternatives. Finance validates any incremental-benefit interpretation; saved minutes alone are capacity, not cash savings.
* [ ] Record hashes, split/seed, denominators, actual serving version, usage, unknown liabilities, reviewer protocol and pass/fail/insufficient outcomes. Retain negative/inconclusive results.
* [ ] Actual calls require separate finite call/token/budget/expiry authorization, approved payload/provider handling and serving attestation. Human participation requires appropriate consent, accessibility and privacy authorization.
* [ ] Dry runs and scripted providers remain not evaluated for actual-model and human effectiveness. Role agents are not participant substitutes.
* [ ] Delivered builds retain real AI/SQL/Azure proof under CON-009/AC-057 without treating a successful inference as semantic accuracy, fairness or net benefit.

## RAI Prerequisites

Complete relevant input, source, release, incident, challenge and cohort controls before the authorized exercises. Reuse the existing evaluation harness; dataset registry and journey bundles supply evidence without duplicating their separate scope.

Local trace: MEASURE-01/02/03/04, MAP-04, T-RAI-002/005, AC-070/073, NFR-009. Budget or participant absence leaves the relevant gate insufficient.

## IS011 - Update issue 145

Current title: Azure SQL pilot tier, backup restore and recovery proof.

Current labels: feature, adr, area:infrastructure, status:partially-delivered. Retain all.

Specific outbound block:

## RAI Restore and Erasure Acceptance Criteria

* [ ] On explicitly authorized disposable infrastructure, restore an actual backup together with document/audit state; seed/reset or database restart alone cannot pass.
* [ ] Reconcile versions/counts, permitted history and current authority; reapply erasure tombstones and legal holds.
* [ ] Prove that restored state does not resurrect revoked release/identity permission, suspended proposals, erased content or spent allowance.
* [ ] DPO/record owners approve retention/hold/audit conflicts and provider-copy handling. Local deletion does not prove provider erasure.
* [ ] Independent qualified owners witness expected/actual results and retain residual failures.
* [ ] Observe existing fixed disposable local SQL restrictions. No pilot/live database is targeted; any Azure recovery exercise requires separate authorization and bounded runbook.
* [ ] SQLite/SQL-shape emulation is labelled lower-tier evidence. Missing drill authority leaves the drill blocked without erasing completed offline regressions.
* [ ] Publish only permitted hashes/status/counts, not credentials or private records.

## RAI Prerequisites

Use retention/authority decisions and persisted release/suspension state. Retain the issue's existing tier, PITR and recovery-objective scope; this subsection does not authorize environment changes.

Local trace: MN-2.3, GOVERN-AUDIT-04, T-RAI-005, NFR-005/006/011.

## IS012 - Update issue 126

Current title: Frozen protocol, benefits register and phase release gates.

Current labels: feature, brd, area:governance, status:not-started. Retain all.

Specific outbound block:

## RAI Closure and Qualified Acceptance Criteria

* [ ] Track all eleven residuals and eleven unassessed checks with current commit, task/release version, evidence, accountable decision-maker and explicit implemented/source-tested, observed, proposed, insufficient or independently accepted disposition.
* [ ] Residual register includes T-RAI-001/002, MEASURE-01, GOVERN-AUDIT-01/02, MAP-01/02/04 and MN-3.2/4.1/4.3.
* [ ] Unassessed register includes GOVERN-AUDIT-04/05, MAP-05, MEASURE-02/03/04, MN-2.3, T-RAI-005 and EU-COND-01/02/04.
* [ ] After implementation, obtain a fresh current-source assessment with complete inline verifier evidence; do not replay baseline recovery or reinterpret DOWNGRADED as closed.
* [ ] Preserve the original baseline and dated report acceptance. Code-only passes cannot close human, privacy/legal, actual-model, recovery or operational gates.
* [ ] Qualified task/ranking/incident/DPO/Legal/operational owners decide their own applicable acceptance and residual-risk boundaries; record evidence and authority without automatic signatures.
* [ ] Current PRD quality review and owner acceptance remain separate from report acceptance and remediation completion.
* [ ] Update existing addendum/PRD/ADRs and knowledge index/append-only log with supported current evidence, preserving historical versions and negative/insufficient outcomes.
* [ ] Live use stays blocked and affected dispatch disabled until appropriate evidence and approvals exist. Conditional EU assurance applies only after qualified applicability review.
* [ ] Any delivered application build also satisfies its version-linked real AI, SQL and Azure contract and effective scoped spending authorization.

## RAI Prerequisites

Consume completed engineering, held-out/human evidence and witnessed restore results. Existing pilot phase/tranche decisions remain separate; this issue update does not authorize capture, deployment, paid calls, research or live release.

Local trace: P06-T03 and all 22 baseline open checks. The executor must not copy local trace lines into GitHub.

## Hierarchy and Dependency Record

| Ref | Textual existing parent | Exact native pair | Planned relationship operation |
| --- | --- | --- | --- |
| IS001 | 104 | needs_review | None |
| IS002 | 113 | needs_review | None |
| IS003 | 113 | needs_review | None |
| IS004 | 104 | needs_review | None |
| IS005 | 104 | needs_review | None |
| IS006 | 136 | needs_review | None |
| IS007 | 113 | needs_review | None |
| IS008 | 81 | needs_review | None |
| IS009 | 123 | needs_review | None |
| IS010 | 104 | needs_review | None |
| IS011 | 136 | needs_review | None |
| IS012 | 123 | needs_review | None |

All affected relationships are flattened in this plan. Do not relink an existing item based on this table.

Implementation sequencing follows the source plan, not the order of tracker Updates:

* Inventory and processing manifests precede input/source/release controls.
* Input/source controls precede release admission and meaningful review.
* Monitoring and suspension consume release/review controls.
* Challenge/cohort work consumes permissions, invalidation and suspension.
* Actual-model/human and backup exercises require their specific approvals.
* Closure consumes all relevant evidence and qualified acceptance.

No native dependency links are proposed.

## Totals and Missing Categories

* Updates: 12, all body-only and needs_review.
* Creates: 0. Existing capabilities provide coherent homes for the missing criteria.
* Links: 0. No new endpoints are created; exact existing pairings were not hydrated.
* Comments, transitions, closes, assignments, label/type/milestone changes: 0.
* Match: none for a complete primary task outcome.
* Uncertain: none from missing primary body hydration.
* Distinct primary creates: none; closed rubric issue 23 is Distinct context.
* Thirteen remediation tasks map to twelve issues because source provenance and meaningful source review are combined in issue 106.

Coverage is reviewable, not executed. No existing issue currently contains the complete relevant delta, and proposed checklists do not prove completed controls.

<!-- markdown-table-prettify-ignore-end -->
