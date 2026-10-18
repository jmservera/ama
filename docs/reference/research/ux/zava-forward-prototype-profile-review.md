---
title: Zava Forward Prototype Profile Review
description: Company-role critique, dated owner usability feedback and proposed next-prototype acceptance checks
ms.date: 2026-10-18
ms.topic: reference
---

## Design traceability and review gate (2026-10-18, #156)

This register extends the existing journey and prototype research for
[#156](https://github.com/jmservera/ama/issues/156), under
[#149](https://github.com/jmservera/ama/issues/149). It records a finite
documentation slice, not completion of either issue. The issue's original
"no task flows/log" description is historical: the
[profile routes below](#all-eleven-profile-journeys),
[PRD profile contract](../../../prds/zava-forward-retrofit-programme-demonstrator.md#profile-journey-contract-for-the-next-prototype),
[lifecycle and return flow](../../../prds/zava-forward-retrofit-programme-demonstrator.md#case-lifecycle-role-handoffs-and-return-path)
and [design choices](#design-decisions-and-open-questions) already supply
relevant evidence. Their existence does not prove accepted screen designs.

### Declared inventory and source versions

Coverage is exactly T01-T11, the eleven PRD research perspectives, plus four
shared core flows C01-C04: queue scope/reset, case open/return, blocked
readiness/handoff and AI draft review. These are not authenticated-role
equivalents. Feature-to-perspective links are this register's interpretation,
not owner-approved role mappings. Existing journeys are research hypotheses.
The [PRD evidence trace](../../../prds/zava-forward-retrofit-programme-demonstrator.md#brd-and-evidence-trace)
retains upstream authority and proposed-requirement limits.

Complete current/future screen-backlog coverage is **unknown**. Import/export,
operations/account, direct resident/representative screens
([#154](https://github.com/jmservera/ama/issues/154)), regulatory alerts/chat
([#215](https://github.com/jmservera/ama/issues/215)) and other feature-specific
states are outside this finite inventory. The coordinator must reconcile the
remaining screen features before claiming #156's universal coverage criterion.
[#233](https://github.com/jmservera/ama/issues/233) remains the wider atlas-to-screen
workstream, not a claim that this register covers every atlas journey.

| Source | Exact version and use | Evidence boundary |
| --- | --- | --- |
| H, [historical HTML prototype][design-h] | 2026-10-06 artifact, commit `c0f7c08aec514597af86528caf1bdad4b7250246` | Actual constructed prototype, inspected in the historical review below; not a current approved wireframe, runtime or user study |
| E, [shared IA manifest][design-e] | `152-ia-v1`, at baseline `3104bb69ddc26c81e0e9d2f57000dac1d99a419a` | Actual engineering fixture/coverage artifact, not a screen wireframe; eight auth roles, eleven perspectives, all nine workflows partial/deferred |
| S, source documents linked here | Baseline `3104bb69ddc26c81e0e9d2f57000dac1d99a419a`, inspected 2026-10-18 | Exact journey, flow, UX-check, WCAG and content sections; later engineering evidence does not update historical prototype acceptance |
| Current reviewable screen designs | Not supplied | Design owner must provide exact versions and state/recovery coverage for each affected row |

[H][design-h] and [E][design-e] are immutable source links; local synthesis
links below are read at S. Neither proves current rendered behavior.
The [architecture Excalidraw views](../../../architecture/README.md#scope-and-reading-order)
describe system architecture, not screen layouts, and cannot fill a missing
wireframe. No new prototype, screen drawing or user review is created here.

### Profile design trace

Each flow link names an existing section and the matching row or role, rather
than implying that opening a document demonstrates a task. Requirement IDs
refer to the [PRD requirements](../../../prds/zava-forward-retrofit-programme-demonstrator.md#functional-requirements);
UX checks refer to the [existing proposed checks](#proposed-acceptance-checks-for-the-next-prototype),
not executed acceptance. E statuses describe the shared IA slice only, not
every later feature implementation. Responsible roles below are requested
follow-up owners, not named people or supplied company delegations.

| Row / screen feature | Exact journey section | Existing task-flow section / matching row | Actual artifact / version | Requirement / check | Evidence status | Missing item / owner role / next action |
| --- | --- | --- | --- | --- | --- | --- |
| T01 Asset and investment, [#226](https://github.com/jmservera/ama/issues/226) | [Asset Executive hypothesis](./customer-journeys/asset.md#journey-1-asset-executive-current-state-hypothesis) | [All eleven flows](#all-eleven-profile-journeys), Asset and investment: queue -> source conflict -> resolution role | [H][design-h], asset queue; [E][design-e], Asset profile deferred | FR-003/004; UX-04; unknown investment inputs remain unknown | Historical source only; no investment approval | Current design: Not supplied / Asset product and design owners / supply exact queue/conflict design and review unresolved-input handling |
| T02 Programme coordinator, [#230](https://github.com/jmservera/ama/issues/230) | [Programme Manager / planner](./customer-journeys/programme.md#1-programme-manager--planner) | [PRD profile flow](../../../prds/zava-forward-retrofit-programme-demonstrator.md#profile-journey-contract-for-the-next-prototype), Programme coordinator: returned queue -> ownership -> reset | [H][design-h], case 863; [E][design-e], Programme profile partial | FR-011/032/033; UX-02/03/05 | Historical return example; shared IA partial, no complete handoff acceptance | Current design: Not supplied / Programme and design owners / supply sent/received/accepted/returned states with separate chase/update ownership |
| T03 Retrofit case team, [#230](https://github.com/jmservera/ama/issues/230) | [Connected service journey](./customer-journeys/customer-journey-atlas.md#one-connected-service-journey) | [PRD profile flow](../../../prds/zava-forward-retrofit-programme-demonstrator.md#profile-journey-contract-for-the-next-prototype), Retrofit case team; [lifecycle/return](../../../prds/zava-forward-retrofit-programme-demonstrator.md#case-lifecycle-role-handoffs-and-return-path) | [H][design-h], separate home examples; [E][design-e], case-team profile partial | FR-001/002/035; UX-04/07; separate home decisions | Historical snapshots are not one connected home lifecycle | Current design: Not supplied / Programme and design owners / supply linked-home flow without transferring sibling consent or acceptance |
| T04 Assessor, designer and Coordinator, [#231](https://github.com/jmservera/ama/issues/231) | [Assessor](./customer-journeys/programme.md#2-surveyor--retrofit-assessor) and [designer/coordinator](./customer-journeys/programme.md#3-retrofit-designer--coordinator) | [All eleven flows](#all-eleven-profile-journeys), Retrofit Assessor, designer and Coordinator: technical queue -> missing reference -> competent return | [H][design-h], case 104; [E][design-e], technical profile partial, script deferred | FR-008/013; UX-04; stale/missing evidence blocks readiness | Historical missing-reference example, not professional sign-off | Current design: Not supplied / Technical and design owners / supply separate assessor/designer/coordinator review and return designs |
| T05 Housing and Resident Engagement, [#232](https://github.com/jmservera/ama/issues/232) | [Resident engagement/support worker](./customer-journeys/residents.md#current-journey-d-resident-engagementsupport-worker) | [PRD profile flow](../../../prds/zava-forward-retrofit-programme-demonstrator.md#profile-journey-contract-for-the-next-prototype), Housing and Resident Engagement: choice -> service -> owned update | [H][design-h], case 208; [E][design-e], Housing profile partial | FR-014/045; UX-08; contact/access is not works consent | Staff-facing hypothesis; no resident contact or wording acceptance | Current design: Not supplied / Housing, Resident Engagement and design owners / supply measure/version choice and safe-route/update states for named wording review |
| T06 Repairs and Building Safety, [#227](https://github.com/jmservera/ama/issues/227) | [Repairs/hazard response](./customer-journeys/safety.md#current-state-map-b-repairshazard-triage-and-response-staff) | [All eleven flows](#all-eleven-profile-journeys), Repairs and Building Safety: referral -> receipt/acceptance -> owned follow-up | [H][design-h], case 531; [E][design-e], Safety profile partial | FR-015; UX-04/05; external service owns hazard decisions | Historical referral example and partial IA; no authority inferred | Current design: Not supplied / Building Safety and design owners / supply distinct referral, receipt, acceptance and restart-evidence states |
| T07 Procurement and contracts, [#228](https://github.com/jmservera/ama/issues/228) | [Procurement/contracts manager](./customer-journeys/suppliers.md#1-procurementcontracts-manager-secure-accountable-delivery) | [All eleven flows](#all-eleven-profile-journeys), Procurement and contract manager: package -> scope/capacity -> draft review | [H][design-h], case 317; [E][design-e], Procurement profile deferred | FR-016; UX-04; offer is not commitment | Historical draft package, not work release or booking | Current design: Not supplied / Procurement and design owners / supply period/version, offered/committed and unmet-prerequisite designs |
| T08 Provider / contractor, [#228](https://github.com/jmservera/ama/issues/228) | [Contractor scheduler/supervisor](./customer-journeys/suppliers.md#2-contractor-schedulersupervisor-make-a-workable-day) | [PRD profile flow](../../../prds/zava-forward-retrofit-programme-demonstrator.md#profile-journey-contract-for-the-next-prototype), Provider / contractor contact: intake -> correction -> independent review | [H][design-h], staff-facing case 317; [E][design-e], Provider profile partial | FR-016/017; UX-04; submission is not independent acceptance | Historical H has no provider identity/portal; E only assigned-job/projection slice | Current design: Not supplied / Supplier product and design owners / supply bounded submission/correction design and independent-review handoff |
| T09 Quality and assurance, [#231](https://github.com/jmservera/ama/issues/231) | [Independent QA inspector/evaluator](./customer-journeys/programme.md#4-independent-qa-inspector--retrofit-evaluator) | [All eleven flows](#all-eleven-profile-journeys), Quality and assurance: incomplete pack -> defect owner -> reinspection/disposition | [H][design-h], case 422; [E][design-e], Quality profile partial | FR-008/017; UX-04; incomplete evidence prevents handover | Historical incomplete pack; IA navigation is not QA acceptance | Current design: Not supplied / Quality and design owners / supply per-measure evidence, return and independent acceptance states |
| T10 Finance and Grants, [#225](https://github.com/jmservera/ama/issues/225) | [Grant preparer](./customer-journeys/finance.md#a-capital-and-grant-preparer) and [payment officer](./customer-journeys/finance.md#c-payment-officer) | [PRD profile flow](../../../prds/zava-forward-retrofit-programme-demonstrator.md#profile-journey-contract-for-the-next-prototype), Finance and Grants: match exception -> review -> safe block/export | [H][design-h], case 752 invoice exception; [E][design-e], Finance profile partial | FR-018/019/042; UX-04; application, award, claim and cash separate | H does not demonstrate later application draft/export contract; E navigation only | Current design: Not supplied / Finance and design owners / supply exact invoice and application-pack designs, preserving separate approvals and unknown route/schema |
| T11 Digital operator and auditor, [#229](https://github.com/jmservera/ama/issues/229) | [Digital/service operator](./customer-journeys/data.md#current-map-2-digital--service-operator) and [audit reviewer](./customer-journeys/data.md#current-map-4-independent-audit--regulatory-assurance-reviewer) | [All eleven flows](#all-eleven-profile-journeys), Digital operator and auditor: conflict/return -> original sources -> owned recovery | [H][design-h], cases 646/863; [E][design-e], Digital profile deferred | FR-012/022/024; UX-03/04; no silent correction or replay | Narrative history is not operational audit evidence | Current design: Not supplied / Data/operator and design owners / supply both source values, event metadata and explicit recovery design |

### Shared core-flow design trace

| Row / screen feature | Exact journey section | Existing task-flow section / matching check | Actual artifact / version | Requirement / check | Evidence status | Missing item / owner role / next action |
| --- | --- | --- | --- | --- | --- | --- |
| C01 Queue scope/reset, [#152](https://github.com/jmservera/ama/issues/152) | [Programme planner](./customer-journeys/programme.md#1-programme-manager--planner) | [Existing IA flow](#shared-workbench-ia-engineering-slice-2026-10-15), own/programme -> filter -> reset; [UX-02/03](#proposed-acceptance-checks-for-the-next-prototype) | [H][design-h], historical filtering; [E][design-e], scope/reset fixture | FR-032/035; AC-034; distinguish no matches, unavailable scenario and failure | E bounded engineering; historical owner feedback and later #24 source differ | Current design: Not supplied / Workbench design owner / supply queue-state designs and compare visible counts/reset to exact fixture |
| C02 Case open/return, [#152](https://github.com/jmservera/ama/issues/152) | [Programme planner](./customer-journeys/programme.md#1-programme-manager--planner) | [PRD profile flow](../../../prds/zava-forward-retrofit-programme-demonstrator.md#profile-journey-contract-for-the-next-prototype), Programme coordinator recovery; [UX-07](#proposed-acceptance-checks-for-the-next-prototype) | [H][design-h], historical detail; [E][design-e], back fixture and first-page limitation | FR-001/002/032; UX-07; retain queue context and originating focus/position | IA retains filters/sort but first page/main focus; full restoration unmet | Current design: Not supplied / Workbench design owner / supply open/close/return design and explicitly assess selection, position and focus |
| C03 Blocked readiness/handoff, [#230](https://github.com/jmservera/ama/issues/230) | [Connected service journey](./customer-journeys/customer-journey-atlas.md#one-connected-service-journey) | [Lifecycle/return flow](../../../prds/zava-forward-retrofit-programme-demonstrator.md#case-lifecycle-role-handoffs-and-return-path); [UX-04/05](#proposed-acceptance-checks-for-the-next-prototype) | [H][design-h], held/returned examples; [E][design-e], handoff workflow deferred | FR-008/011/033; SA-003; reason, owner, next action | Historical examples, not complete ownership/accepted-handoff evidence | Current design: Not supplied / Programme and design owners / supply blocked/unknown/returned/accepted states with accountable next action |
| C04 AI draft review, [#152](https://github.com/jmservera/ama/issues/152) shared pattern; [#233](https://github.com/jmservera/ama/issues/233) journey application | [Controlled proposal opportunities](./customer-journeys/customer-journey-atlas.md#divergent-opportunities-beyond-another-chatbot) | [Existing UX-06 flow](#proposed-acceptance-checks-for-the-next-prototype), inspect inputs -> draft/recommend/flag -> human review or manual/failure route | [H][design-h], static suggestion only; [E][design-e] does not test AI draft review | FR-025-028; SA-004; accepted draft is not approval/consent/safety decision | No AI quality, complete manual recovery or human design acceptance established here | Current design: Not supplied / Assistant product, content and design owners / supply exact draft/review/failure states with optional manual route and source labels |

### Design decisions and open questions

The register consolidates existing choices; it does not grant new delivery or
professional authority. Source dates and classifications are part of each row.

| Decision | Source / date | Rationale and affected rows | Status | Open question / next owner action |
| --- | --- | --- | --- | --- |
| D01 Adopt Fluent UI (Fluent 2), not extend the bespoke MVP | [Actual owner decision, 2026-10-15](https://github.com/jmservera/ama/issues/150#issuecomment-6194477486); [pinned design-system scope](./design-system.md#decision-adopt-fluent-ui-fluent-2) | Owner selected the alternative; use one coherent foundation across T01-T11/C01-C04. A consistency rationale is this register's interpretation, not a quoted owner reason. | Owner-selected; live #150 CLOSED when checked 2026-10-18. Pinned S still says partial native/token foundations and "Issue #150 stays open." That sentence is historical/stale status, not current issue status. Closure alone is not full Fluent/runtime or human acceptance evidence. | Design/engineering owners supply exact implementation/adoption evidence; do not silently convert pinned partial scope to full acceptance |
| D02 Make context visible and case return recoverable | [Owner notes, 2026-10-07](#owners-notes); [derived design direction](#design-direction-derived-from-the-notes); [later source reconciliation, 2026-10-13](#later-pinned-source-reconciliation-2026-10-13) | Owner reported unclear role/workflow changes and requested full-screen case work. Queue context, reset and focus/position restoration are derived recovery requirements/proposals, not proof they were delivered. T02/T03/T11/C01/C02. | Reported owner experience plus sourced design interpretation. Later #24 filtering code does not disprove earlier feedback or pass UX-02/03. | Workbench design owner supplies exact current candidate and visible recovery evidence; UX-07 full restoration remains unmet in shared IA slice |
| D03 Correct misleading fields/filters, deepen one exception, then connect one home | [Existing sequencing synthesis, 2026-10-06 review](#sequencing-and-scope-trade-off) | Keep scope reviewable; invoice depth before a new ledger, draft package readiness before release. T02-T04/T07/T09-T11/C03. A second home explains dependency, never transfers approval. | Source-based synthesis/proposal, not an owner-approved delivery sequence or user-validated priority | Programme/design owners confirm next bounded delivery slice and retain independent decisions |
| D04 Preserve honest partial recovery and separate permissions from navigation | [Shared IA engineering slice, 2026-10-15](#shared-workbench-ia-engineering-slice-2026-10-15), [E][design-e] | Existing implementation keeps scope/query/filter/sort but returns to first page/main focus; do not claim full UX-07. T02/T03/T05/C01/C02. | Engineering behavior/limit, not human design acceptance; rationale to expose the limitation is this register's interpretation | Workbench owner records exact restoration design and checks; owner device/browser decisions remain open |

### Design review checklist and definition of done

Use this gate for each affected screen row before calling its design accepted.
For a new screen feature, add its trace row and exact candidate version first.
Record reviewer name/role, date, expected versus actual, outcome, findings and
next action for that version. A source link or an unchecked box is not a result.

* [ ] Trace is complete: feature, exact journey and existing task flow,
  reviewable screen artifact/version, requirement/check and evidence status;
  any gap has a responsible role and next action.
* [ ] Exact screen versions show applicable default, focus, disabled, error,
  loading, empty and blocked states; recovery preserves necessary context and
  permissions. Status is understandable without colour. Human approvals and
  resident choice are never inferred from receipt, navigation or a draft.
* [ ] Accessibility evidence follows the existing
  [proposed WCAG 2.2 AA scope](./wcag-conformance-baseline.md#decision-target-level-and-scope),
  [audit](./wcag-conformance-baseline.md#audit) and
  [manual check record](./wcag-conformance-baseline.md#manual-check-record):
  keyboard/focus, names/labels/status announcements, contrast/non-colour cues,
  targets, zoom/reflow and relevant errors/authentication, with tester/date,
  exact candidate/tool/browser, results and exceptions. Static checks or
  native controls do not establish conformance; unconfirmed scope/tester
  decisions remain open, not waived.
* [ ] Content follows the [plain-language standard](./content-standard.md#content-standard)
  and [core-flow audit](./content-standard.md#copy-audit-of-the-core-flow):
  reason, owner and next action; exact AI/manual labels; no implied approval.
  [Named human resident-wording review](./content-standard.md#human-review)
  records name/role, date, exact text/version and outcome before any use.
  Missing approval keeps resident-facing drafts not approved.
* [ ] A named human design reviewer records the actual task/state review and
  finding dispositions for the exact versions. Direct accessible staff,
  provider and resident research is reported separately, with actual methods,
  observations and limitations under
  [#155](https://github.com/jmservera/ama/issues/155); role-agent opinions are
  not participant evidence or resident validation.

Missing required trace, reviewable design, accessibility or content evidence
prevents overall **Pass**. Missing required human acceptance also keeps the
gate open. Use **Blocked** for absent prerequisite evidence and **Not accepted**
for an assessed candidate with unresolved defects; neither is Pass. A
documentation-complete register or engineering check cannot override either.
User-research validation is a separate result, never inferred from a design
review. No proposed WCAG scope, reading-age target or resident review is
silently approved by this checklist.

### Recorded design evidence review

| Field | Actual record |
| --- | --- |
| Record / date | G156-2026-10-18, evidence inspection on 2026-10-18 |
| Candidate boundary | T01-T11/C01-C04 documentation addition; source baseline S, historical H and engineering E at the exact versions above |
| Reviewer | Copilot documentation agent, automated source/evidence inspection only; not a human design reviewer |
| Human reviewer / review date | Not supplied / Not supplied |
| Current screen artifact/text versions for human acceptance | Not supplied; H and E are not substitutes |
| Overall design outcome | Blocked: required current designs and human/accessibility/content evidence not supplied |

| Check | Expected evidence | Actual evidence / outcome | Finding, affected rows / owner role / next action |
| --- | --- | --- | --- |
| Finite trace documentation | Fifteen declared rows with resolvable sources, exact versions and actionable gaps | Fifteen records checked: links/anchors, table shape and pinned artifact paths resolve. Broader backlog coverage unknown, not all-screen acceptance | G01, all rows and remaining screens / coordinator / reconcile remaining feature inventory |
| Exact screen/state designs | Current reviewable versions for applicable states and recovery | Not supplied; H historical, E engineering only. Blocked | G02, all rows / design owner / supply versioned current screen artifacts and state coverage |
| Recovery/ownership design assessment | Actual expected/observed result for UX-02/03/05/07 on exact candidate | Historical owner report and later source reconciliation retained; IA return-position/focus limit remains. Human review Not supplied. Blocked | G03, T02/T03/T11/C01-C03 / Workbench and Programme design owners / assess exact candidate, record expected versus actual and dispositions |
| Accessibility | Required versioned static/rendered/manual evidence and applicable owner scope decisions under existing baseline | Historical partial audit/engineering only; required current manual record Not supplied. Blocked, no conformance claim | G04, all rows / accessibility owner and named testers / record required checks and unresolved scope decisions |
| Content and resident wording | Exact copy review; named human review of resident-facing text before use | Existing bounded copy audit; current exact text and human approval Not supplied. Blocked | G05, all rows; resident wording particularly T05/C04 / content owner and named human reviewer / supply text versions and actual review outcome |
| Human design review | Named reviewer/role/date, exact versions, actual findings and dispositions | Not supplied. Blocked | G06, all rows / design owner / assign human reviewer and record actual results |
| Direct user research | Actual accessible staff/provider/resident research for candidate tasks | Not supplied. Not validated; historical role research is hypothesis only | G07, all rows / research owner / run approved representative-user study and record observations/limits separately |

| Independently reported result | Status at this record |
| --- | --- |
| Documentation completeness, finite inventory only | Complete for the fifteen evidence records: link/anchor/table/source/diff checks performed; no claim of full #156 coverage or complete design evidence |
| Engineering | Historical/source-inspected partial evidence only; no fresh runtime checks in this documentation slice |
| Human design review | Not supplied; not accepted by a person |
| User-research validation | Not supplied; not validated |
| Overall design gate | Blocked; no #156 AC, board or parent acceptance changed |

[design-h]: https://github.com/jmservera/ama/blob/c0f7c08aec514597af86528caf1bdad4b7250246/.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html
[design-e]: https://github.com/jmservera/ama/blob/3104bb69ddc26c81e0e9d2f57000dac1d99a419a/src/api/checks/workbench-manifest.json

## Outcome and Evidence Boundary

### Hazard referral evidence engineering continuation (2026-10-17, #85)

The [existing referral/home-hold contract](../../../../src/core/README.md#hazard-referral-and-home-retrofit-holds-85)
already records source/awareness, separate sent/receipt/acceptance, owned
follow-up, fixed affected-home scope, independent restart evidence and external
response/resident-update times. The workbench does not classify hazards,
calculate statutory clocks, close the external case or send resident messages.
This audit corrects evidence integrity, not those service responsibilities.

Fresh fictional probes found an unregistered actor accepted, a repair recorder
self-releasing by email casing and a failed save leaving a success audit without
the hazard. The hazard-owned correction reuses current registered staff lookup,
checks caller and destination again under the SQL writer transaction, binds the
receiver's persisted identity and compares historical email/code/OID for
independence. Existing provisional role/delegation boundaries are not new
authority. BRD hazard intent is FR-003/RULE-003; the issue's older BRD FR-015
pointer now describes tenure. PRD FR-015/AC-018/038 remain the hazard reference.

Canonical JSON/SQLite evidence: 33 run, one JSON-only skip on SQLite.
Actual task-owned loopback SQL Server: 16 run, one JSON-only skip, including
separate-connection authority revocation/substitution and failed release/audit/
recovery-read cases. Failed SQL events cannot leave a staged success audit;
earlier pending audit remains exactly once. JSON saves precede success audit,
but its separate files are not transactional: post-save audit failure explicitly
requires reload/reconciliation rather than claiming rollback.

The one independent Review returned Complete / Not accepted for a reproduced
post-commit synchronization defect: recovery replayed already-committed prior
audit. Authorized correction ONE marks the acknowledged COMMIT and distinguishes
its recovery from uncommitted rollback. Canonical one-shot/persistent fault
checks pass on SQLite and actual task-owned SQL Server, retaining committed
release and both audit entries exactly once with explicit outcome warnings.
The original adverse Review remains; parent checks do not establish independent
final-head closure or operational acceptance.

No web source changed, and no new browser, human or WCAG acceptance is claimed.
The [existing API and manual screen](../../../../src/api/README.md#hazard-referral-and-retrofit-hold-api-85)
preserve Fluent 2/native semantics and unknown timing signals. Verified service
delivery/receipt, operational responsibility/timing/escalation ratification,
real professional approval and Azure/model/human acceptance remain open.
No regulatory snapshot was edited and no legal currentness claim is made.

### Assessment reconciliation engineering continuation (2026-10-17, #84)

Original post-implementation Review: **Not accepted, blocking recovery defect**. An
independent early/persistent discard-read failure probe found that outer lock
cleanup can still commit a failed success audit or replace the original
operation error. The normal-recovery evidence below remains valid but is not
sufficient acceptance.

Coordinator-authorized correction ONE fixes canonical discard ordering:
failed writes/audits and validation state are cleared, known cache snapshots
restored and the sync watermark invalidated before any reload reads. Actual
one-shot/persistent failure tests preserve the original error, prevent audit
leaks, release locks and force later reload, across all three decision wrappers.
Ten selected canonical tests pass on actual task-owned local SQL Server;
102 focused core/gate tests, 69 shared cleanup-consumer tests and 72 targeted
API tests (one existing browser skip) also pass. Bounded independent verification
closes RV-001 for this correction, with 91 focused tests and two constructed
snapshot probes. Original Review remains historical; #84 remains open and no
professional, source-policy or operational approval is granted.

Current constructed checks independently preserve both stock assertions and
query owner, four separate versioned technical sign-offs, affected-only
reassessment, and explicit Unknown support alongside non-flag ranking factors.
These mechanisms were already delivered; the continuation does not redesign
their UI or change the deterministic ranking policy.

The [core decision boundary](../../../../src/core/README.md#stock-comparisons-and-human-technical-sign-offs-84)
now prevents cached revoked/removed/changed-OID identities from making stock
or technical decisions. SQL rechecks inside its existing writer transaction
and discards failed staged decisions/audits, preventing a later success-shaped
audit for an unchanged design. The
[API contract](../../../../src/api/README.md#stock-reconciliation-api-84)
retains human-only decisions even for stale authenticated sessions.

Eight selected canonical tests passed on an isolated local SQL Server 2022
container on 2026-10-17, including second-connection authority change and
case/audit failure with reopen. No private stock or real map dataset was used.
This is engineering evidence, not new professional competence/delegation,
stock-source authority, health inference, direct-human/WCAG acceptance,
live/Azure/model acceptance or full BRD AC-065 cohort/referral completion.
JSON retains its separate-file crash-atomicity limitation; nomination,
self-referral and challenge remain #130 by owner direction.

### Controlled bulk edit engineering continuation (2026-10-17, #78)

The [migrated API bulk contract](../../../../src/api/README.md#controlled-bulk-preview-api-78)
adds a server-owned preview and all-or-nothing application for administrative
case explanations and existing handoff due/next-action fields. Every selected
ID has an inspectable old/new change, validation failure and predicted outcome
before apply. Foreign/missing records disclose no field values. No-op targets
remain unchanged without invented edit versions.

The [core implementation boundary](../../../../src/core/README.md#controlled-administrative-bulk-edits-78)
retains source/version, named actor, timestamp, reason and field changes in
case history and immutable audit. SQL rechecks current identity/OID, field/
owner rights, case rowversions and guardrails under the existing writer lock.
Issuer-bound preview hashes, durable consumption and failure recovery prevent
changed instructions, stale targets and concurrent replay from bypassing
authority. Ownership still requires receiver acceptance; controlled approvals,
resident commitments and hazard clocks are outside the closed field contract.

This is local synthetic core/API engineering evidence, not a new UI, direct
staff/resident research, WCAG conformance or live SQL Server acceptance.
JSON retains its separate-file audit/state limitation. Existing evidence-upload
and handoff-transfer provenance have not been established as complete FR-005
acceptance; the bounded delivery must not be read as full PRD acceptance.
Historical prototype findings below remain historical.

Correction cycle ONE on PR #378 fixes RV-001: immutable issued outcomes and
failures, exact ordered records/IDs and complete snapshots now determine
eligibility regardless of mutable status. Every target, including no-ops, is
revalidated inside the SQL writer transaction. Synthetic cached/persisted
status-reset regressions preserve cases/history and show refusal rather than
success audit. The original RPI Review remains historical Not accepted.

Correction ONE recorded RV-002 as a source-confirmed partial FR-005 criterion,
not merely missing test evidence. At that point evidence upload accepted
file/name/kind only; its hash/version,
display name/date and separate email/time audit lack supplied source/version
and change reason. Handoff history retains email/time/role and versioned
sender/receiver snapshots, but offer/accept have no explicit source-version
contract and acceptance has no reason input or complete old/new ownership
provenance event. Current API/UI callers do not supply those missing inputs.
Those missing inputs/events were an implementation gap, not an actual
human-approval dependency. The explicit correction TWO instruction supersedes
the residual-only disposition for the existing upload/offer/accept paths.

Same-PR integration after #377 merged onto main92d4f89 retains separate form
staging and bulk modules, both Store/projection/API protections and checked SQL
documents. 110 joint synthetic focused tests pass, including upstream
pending/missing-rescan durability, permissions, rollback and SQL reopen.
All earlier findings remain historical; RV-001 correction survives unchanged.
Integration alone did not satisfy RV-002 or confer real schema authority,
final-head independent acceptance or merge permission.

Correction TWO implements required user-supplied source reference, source
version and change reason in existing upload and handoff offer/accept UI/API/
store contracts. Handoffs carry the current history version for stale refusal.
Complete immutable events retain exact document-reference and ownership
old/new values, named actor, UTC time and change version; SQL commits them with
case/history changes and rechecks current identity. Filename/hash/acceptance
state never supply invented source or reason. Historical missing data stays
Unknown (legacy); old clients missing metadata get actionable refusal.

Native labeled forms preserve Fluent-token styling, recipient-only acceptance
and existing permissions; errors remain inline with focus and entered values.
Local synthetic Chromium covers required-field focus, Enter upload/offer/
accept, stale refusal, recipient ownership, 390px/reduced-motion and SQL reopen/
audit equality. This is no screen-reader/WCAG, human or live-platform approval.
The original Review and review512a59c4 Revise remain historical; final-head
coordinator independent reassessment is still required, not fabricated Pass.
Actual form/schema authority remains an unrelated human prerequisite, not a
blocker used to omit this implementation.

### Queue signal engineering continuation (2026-10-17, #77)

The [src API queue completion](../../../../src/api/README.md#queue-signal-completion-77-2026-10-17)
extends the existing staff queue, not this historical prototype. All six queue
definitions and five Show only signals are discoverable in one native
disclosure. Effective perspective, workflow stage, query and own/all scope are
explicit; the stage filter narrows authenticated scope without simulating a role.
Reset consumes versioned server scope/order/filters and retains focus and status.
Selected-case rationale/reviewers are compared to that case's API record; absent
proposed owner stays Unknown, never assigned by inference.

Local Chromium checks use three constructed cases, exact differing surname
order, expanded-definition reflow and reduced motion. No private dataset or live
model/platform is used. This is engineering evidence, not staff comprehension,
screen-reader/WCAG conformance, nine-workflow representation, operational signal
ratification or actual AI/SQL Server/Azure acceptance. Historical findings below
remain historical; no customer outcome or owner approval is invented.

The source-inspected findings below describe the 2026-10-06 HTML artifact,
not every subsequent prototype. The separate
[2026-10-07 owner feedback](#owner-usability-feedback-2026-10-07) records
reported impressions of a later application without inspecting its code or
independently reproducing its behavior. Proposed checks are not passed tests.

All nine repository `company-*` profiles were launched in parallel to review
the current [constructed-data prototype](../../../../.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html).
Their own-role findings were collected, then the UX/UI Designer synthesized
all eleven [PRD profiles](../../../prds/zava-forward-retrofit-programme-demonstrator.md#users-and-personas).
Four focused proposal discussions with Procurement, Resident Engagement,
Building Safety and Data/Performance were relayed through the coordinating
agent because the designer's own tool surface could not message peers.

This is source-based design research, not employee/resident interviews,
validated company practice, operational approval or an accessibility
conformance assessment. The role agents are research instruments grounded in
the [original case](../../../case_study_48_original.md),
[addendum](../../../case_study_48_addendum.md) and
[company-role evidence](../company/company-profile-research.md).
Recommendations, JTBD statements and user behavior/accessibility expectations
below are hypotheses pending direct, accessible user research.

The prototype remains unchanged by this review. No authentication, actual
permissions, live communication, integration, persistence, professional
sign-off, operational handoff, work instruction or payment is implemented.
The provider perspective is staff-facing, not a contractor portal. Residents
are affected stakeholders, not authorized users of this non-production MVP.

## What the Prototype Actually Covers

Source inspection and extraction of the data definitions establish eleven
profile perspectives, nine workflow cards, eight constructed cases and three
illustrative history entries per case. Workflow-card selection both displays
context and filters the queue; it does not progress a case through stages.
Profile selection is a view filter, not authorization.

The portfolio workflow has no matching case. Fixed headline values for a
128-home scenario, 42 active journeys, seven holds/reviews and nineteen homes
at handover are not derived from the eight inspectable case examples.
Narrative history has source context, but no event timestamps, actors or
versions. These limits do not invalidate a concept walkthrough; they prevent
claiming full PRD workflow, analytics or audit acceptance.

### All Eleven Profile Journeys

Each JTBD is an assumed job statement: when in the stated situation, the
user wants the stated action so they can reach the stated outcome. Observed
prototype behavior is distinguished from the proposed next slice.
Case numbers below abbreviate `EX-HOME-`.

| PRD perspective | Assumed job and current entry | Current route and safe endpoint | Proposed recovery/handoff and integrated accessibility |
| --- | --- | --- | --- |
| Asset and investment | When reviewing candidate homes, inspect data quality and dependencies to prepare an evidence-grounded investment discussion. Asset queue: 317, 646, 752. | Inspect source conflict, capacity dependency or invoice exception. Eligibility stays unknown; no investment decision follows from fixed metrics. | Expose conflict sources and a named resolution role; link building context and show investment inputs as unknown. Keyboard-operable links and textual source dates/unknowns; disclose metric population separately. |
| Programme coordinator | When coordinating teams, identify blocked work and accountable ownership to prepare the next handoff. All eight cases. | Select workflow and case, inspect snapshot/history. Unassigned receiver and missing return reason remain open; no accepted handoff is demonstrated. | Separate current owner, destination, receiver, chase owner and update owner. Announce filter/result changes; provide visible reset and labelled status fields. |
| Retrofit case team | When preparing a home's next step, inspect evidence and dependencies to avoid assuming another role's approval. Queue: 104, 208, 317, 422, 531, 863. | Inspect home/building context and held stage examples. Different homes do not constitute one home's lifecycle. | Start with a linked exception-to-owner slice, then a read-only lifecycle. Distinguish home/building headings and each home's independent consent, holds and acceptance. |
| Retrofit Assessor, designer and Coordinator | When reviewing a technical pack, inspect sources, design version and missing evidence to complete or return work within competent scope. Queue: 104. | Missing design reference blocks demonstrated readiness; opening the case is not sign-off. | Show missing reference, review/return reason and separate competent reviewers. Textual missing states and keyboard-navigable evidence; no color-only approval cue. |
| Housing and Resident Engagement | When handling a resident service issue, understand measure-specific choice and an accessible next-update commitment to preserve continuity. Queue: 208. | Decision scope and contact/access details unknown; no wider consent or communication inferred. | Separate choice, access, service, complaint, defect and hazard routes. Update purpose, owner, illustrative due date, safe-route/adjustment reference and sent evidence; labelled minimum-necessary fields, not sensitive history. |
| Repairs and Building Safety | When a potential hazard is reported, inspect awareness/referral evidence and affected retrofit scope to chase an authoritative-service response. Queue: 531. | Receipt/service unconfirmed; workbench cannot classify, close or run the hazard clock. | Distinct destination, chase owner, receipt and acceptance. Scoped hold/source and read-only authoritative human decision reference; text states and accessible announcements must not imply release. |
| Procurement and contract manager | When reviewing a package, distinguish offered capacity and draft scope from commitments to prepare accountable review. Queue: 317. | Period/package/capacity unconfirmed; no instruction or schedule issued. | Draft-package panel with period, scope/version, offered/committed state, call-off/work-order reference, unmet prerequisite and named next reviewer. Text labels and independent provider/quality/finance handoffs. |
| Provider / contractor contact | When responding to authorized package information, understand scope and evidence requirements to prepare a submission without self-approval. Queue: 317. | Staff-facing example only; no provider identity, approved intake or submission path. | Keep portal boundary visible. Future constructed submission/correction stays separate from independent review; keyboard-readable checklist/statuses. Procurement is an adjacent lens, not provider validation. |
| Quality and assurance | When inspecting delivered work, compare per-measure evidence and defects to independently accept or return it. Queue: 422. | Incomplete pack, no accepted handover or safety conclusion. | Navigable positive-evidence checklist, specific return reason, defect owner/reinspection and independent disposition. Textual incomplete states; submission never equals acceptance. Programme/Procurement provide adjacent, not dedicated inspector evidence. |
| Finance and Grants | When reviewing an invoice, compare authorized scope and accepted milestone evidence to disposition an exception without implying payment or grant approval. Queue: 752. | Quantity difference unresolved; payment unauthorized and grant/cash status not inferred. | Constructed line comparison and review owner first. Keep budget, commitment, invoice, payment, award, claim and cash separate; readable labelled rows, unknown monetary authority remains unknown. |
| Digital operator and auditor | When diagnosing conflict/return, trace sources and outcomes to prepare owned recovery without silent changes. Queue: 646, 863. | Conflicting values/run/event metadata not exposed; no replay or audit reconstruction. | Show both source values/provenance and unresolved eligibility; preserve original input. Active scope/reset, structured event fields and accessible status text. Data/Performance is an adjacent lens, not actual operator validation. |

## Ranked Recommendations and Acceptance Evidence

These are proposed checks for a later iteration, not assertions that the
prototype already meets them or that a company usability threshold is known.

| Priority | Recommendation and evidence | Proposed check |
| --- | --- | --- |
| P0: Correct ownership semantics | Table says "Next owner" but renders `item.owner`, which detail labels current owner. Especially misleading for 863 with unassigned receiver. HTML queue header/rendering and case detail, lines 680, 939-940, 964-966. | Queue and detail distinguish current owner and proposed/accepting receiver; unassigned remains unassigned. Changing view never assigns work. |
| P0: Correct explanations | Static suggestion rationale describes a missing link across capacity, quality and invoice cases. 863's source says "with return reason" while its context says reason absent. HTML lines 770-774, 851, 981-983. | All eight cases have rationale matching their own evidence/unknown; source and context agree. No proposal satisfies a gate or commits a transition. |
| P1: Make view scope recoverable | Search persists across profile changes; selected workflow overrides profile-focus filtering; portfolio has no sample. HTML `filteredCases`, `renderCases` and handlers, lines 908-955, 992-1020. | Active profile, workflow and search scope visible; one documented reset returns the expected view. Differentiate no supplied portfolio scenario from no search matches, without implying no actual work. |
| P1: Explain metric population | Fixed snapshot cannot reconcile to eight inspectable cases. HTML lines 626-641, 723-732. | State population, illustrative/as-of context and filter impact. Either reconcile a small cohort to records or clearly label snapshot independent of the case examples. Handover stage does not imply accepted handover. |
| P1: Deepen evidence, not dashboard volume | 646 hides compared values; 317 hides package scope/period; 752 hides match inputs. PRD FR-012/016/018/029, AC-015/019/021/031. | One static comparison shows sources and missing prerequisites with a named review role; unresolved evidence is a valid safe endpoint. Do not manufacture real company values. |
| P2: Add a connected synthetic slice | Current cases are stage snapshots, with 317/422 sharing a building but not a demonstrated dependency. PRD FR-001/002/011/022 and AC-012-014/025. | First demonstrate exception -> evidence -> accountable owner, then a read-only lifecycle with a second-home dependency. Preserve separate home gates and source/actor/time/version labels on any constructed events. |

### Sequencing and Scope Trade-Off

The Asset perspective favors a smaller exception-to-accountable-owner
walkthrough; the designer initially proposed a wider home lifecycle. Sequence
them rather than treat them as equivalent scope: correct misleading fields and
filters, deepen one exception/package comparison, then connect a synthetic
home journey. Show a second home only to explain shared-building impact,
never to transfer consent, hold release or quality acceptance.

Prioritize invoice-match depth over a new grant ledger, and draft package
readiness over work release. Add accessible service/choice and return/referral
scenarios as explicit synthetic states, not operational actions. No invented
company SLAs, approval limits, resident preferences or grant conditions are
needed to demonstrate unknowns and safe blocks.

## UX Discussion and Amendments

| Discussant | Designer proposal | Fresh response and disposition |
| --- | --- | --- |
| Procurement and Contracts | One package links scope/capacity/version and independent provider, quality and finance roles. | Agrees with amendment: anchor **draft** package readiness, not release. Show unknown/unmet prerequisites and named next reviewer; constructed readiness is not instruction, booking, contractual commitment, acceptance or payment. |
| Resident Engagement | Update owner, due date and proposed/sent status independent of operational acceptance. | Requires more: update purpose/linked issue; reference safe route and necessary adjustment or explicit unknown; sent timestamp/evidence, not proof of receipt/understanding. Outstanding responsibility remains until sent or explicitly reassigned in the proposed exercise; Housing/Programme must validate real continuity rules. |
| Building Safety | Destination, confirmed receiver, retained chase owner and scoped hold tied to authoritative human evidence. | Minimum synthetic evidence: sent time/reference, receipt state, confirmed receiving role/time only when evidenced, owned follow-up; hold scope/source/status and read-only release-decision/evidence reference. Receipt, acceptance, hazard resolution and work authorization are distinct. Workbench does not judge release sufficiency. |
| Data and Performance | Source/metric reconciliation and filter visibility before richer analytics. | Agrees with amendment: unresolved conflict with evidence and resolution owner is valid. Show denominator/as-of/filter impact; reconcile or label a separate cohort; both 646 values/provenance; portfolio "no representative supplied" not "no work." |

## Accessibility and Human Validation

For each journey, proposed keyboard navigation must retain logical focus and
visible focus indication; labels, heading structure, error/status
announcements and source links must work with screen readers. Verify WCAG AA
text contrast, non-color state meaning, minimum 24-by-24 CSS pixel targets,
200% text zoom and narrow layouts. Prior spot checks and native controls do
not establish conformance.

Real staff/provider research should test locating the right work, explaining
an unknown, identifying an accountable next step and recovering filters.
Direct accessible resident research must validate choice, support, contact
and redress semantics before product requirements are finalized. Device,
environment, accessibility needs, company ownership and acceptance thresholds
remain unknown; do not invent performance metrics or emotional observations.

## Provenance and Related Evidence

Detailed agent IDs, own-role findings, discussion questions and correction
history are in the
[review working record](../../../../.copilot-tracking/research/2026-10-06/proper-warm-profile-journey-critique-research.md#fresh-parallel-company-review---2026-10-06).
The earlier eight-role feedback predates the timeline and is kept separate in
the [prototype change record](../../../../.copilot-tracking/changes/2026-10-06/prd-prototype-changes.md).
Earlier claims that dispatch was unavailable and workflow cards only showed
text are superseded by the fresh review and verified source behavior.

All nine top-level company agents supplied own-role critiques, including the
Executive Reviewer. Any nested reviews or coordination attempted by individual
reviewers are excluded from this review's participation and agreement claims.
Four recommendation discussions were actually relayed and answered; this is
not nine-way consensus or real-user validation. No original case, PRD,
prototype, regulatory snapshot or owner memory was changed.

## Owner Usability Feedback (2026-10-07)

### Source, Status and Scope

The project owner supplied the following feedback on 2026-10-07 while reviewing
the application served at `localhost:3410`. The related prototype
[PR #24](https://github.com/jmservera/ama/pull/24) is provenance only, not a
dependency or a merge prerequisite for these learnings. The URL identifies the
review context; it is not a durable evidence artifact.

This section captures owner-reported observations and requested direction,
not independently verified implementation facts, representative staff or
resident research, approved production requirements or user-tested success.
No runtime inspection, UI implementation, resident-data generation or prototype
code import accompanies this documentation capture. The original case,
addendum, PRD and owner memory remain unchanged.

The earlier source review found that workflow selection filtered the HTML
queue. The owner now reports that changing role or workflow does not visibly
change the UI or filters in the later application. These statements concern
different review contexts and evidence types. Do not silently replace either
with a universal implementation claim; verify the next artifact directly.

### Later Pinned-Source Reconciliation (2026-10-13)

The requested UX Designer review inspected final #24 source
`6029dc248911ddd3eebece5fb2067d881920494c` without running it.
Its [workflow handler](https://github.com/jmservera/ama/blob/6029dc248911ddd3eebece5fb2067d881920494c/apps/proper-warm/public/app.js#L135-L155)
sets the workflow filter and reloads cases; the
[scope/reset, failure and detail paths](https://github.com/jmservera/ama/blob/6029dc248911ddd3eebece5fb2067d881920494c/apps/proper-warm/public/app.js#L205-L345)
show scope/counts, clear failed list metrics and keep case detail independent
of register filters. These later source affordances neither disprove the
owner's earlier perception nor establish that the reviewed runtime used
this pin. UX-02/03 remain unexecuted; preserve both evidence types.

The [closure synthesis](./prototype-learnings-and-simplicity-review.md#draft-ux-closure-review-2026-10-13)
retains uncertain-write recovery and unique #58 journeys; it recommends
retirement or carry-forward, not a passed usability study or new requirement.

### Owner's Notes

> Take these notes: I like the style, logo, fonts and colors. Page seems clear,
> but the red or redish colors are appearing in multiple places and seem like
> they are errors when they are not. When we change the role or the workflow,
> the UI or the filters do not change, it must be clear when is it perpared to
> the next step, who takes the case, what will the agent do with the data or
> what decisions will us help with. Furthermore we should be able to open a
> case full screen, and having full address, phone of the resident, all the
> data needed at hand to fulfill the necessary data and steps. Review this,
> take the notes and store them in a new branch & PR where we could merge this
> information to influence the next prototype, but without storing the current
> code, just the learnings.

### Design Direction Derived from the Notes

| Owner feedback | Proposed next-prototype direction | Boundary |
| --- | --- | --- |
| Style, logo, fonts, colors and general page clarity are liked. | Preserve the brand identity, typography, general palette and clear page structure; correct semantic color use rather than redesign the brand. | A positive owner impression is not a general usability or accessibility finding. |
| Red/reddish elements look like errors where none are intended. | Reserve reddish operational status/action emphasis for genuine errors or blocking conditions. Use neutral informational/selection styling elsewhere; pair every state with explicit text and an appropriate icon, never color alone. | Retaining brand artwork does not justify error-like emphasis on routine metrics, selection or normal progress. Contrast still needs checking. |
| Role/workflow changes do not make the UI or filters visibly different. | Make active role/perspective, workflow, scope and result count visible. Contextualize queues, filters, evidence and available actions; explain unchanged/shared results, unavailable scenarios and pending, empty, loading or failed states. | A selectable prototype perspective is not authenticated authorization and changing context never changes case state. |
| Readiness and the person taking the case must be clear. | Show current stage, next step, missing/stale/conflicting evidence, readiness basis, current accountable owner, proposed destination and receiving owner. Distinguish sent, received and explicitly accepted handoffs, retaining an accountable chase owner while acceptance is pending. | Readiness for human review is not permission to release work. Unknown/unassigned ownership stays explicit; never infer acceptance from receipt. |
| Explain what the agent does with data and which decisions it supports. | Show agent purpose, permitted inputs with source/date/version, intended output, rationale, uncertainty and next human reviewer. Separate extraction, reconciliation, drafts, recommendations and raise-only flags from decisions and actions. | No agent approval of safety, professional work, consent, investment, procurement, payment, claims or quality; no external action merely because a suggestion is accepted. |
| Open a case full screen with address, phone and necessary working data at hand. | Provide a full-screen case workspace with case/home identity, full synthetic address, resident phone, contact preference, necessary accessibility adjustments or explicit unknowns, evidence, tasks, blockers, owners and next step. Provide a clear return to the originating queue. | Use only synthetic, clearly labelled records in the prototype. Production disclosure must follow role, case and field permissions and minimum-necessary purpose; do not expose sensitive histories by default or invent missing values. |

The contact request means sufficient information for the permitted task, not
unrestricted resident disclosure. Safe contact, preferences and adjustments
must be distinguishable from consent to a measure; no phone number, accessible
route or appointment record establishes consent. No real PII is recorded here.
Actual contact details, company access rules and adjustment needs remain
unknown pending authorized validation.

### Proposed Acceptance Checks for the Next Prototype

These checks translate the owner notes into candidate walkthroughs. All are
unexecuted; they supplement rather than approve or silently revise the
[PRD](../../../prds/zava-forward-retrofit-programme-demonstrator.md).
Publish the next artifact's scenario manifest and expected results before
running them. Static/mock states must be labelled as such.

| Check | Scenario and expected evidence | Related PRD anchor |
| --- | --- | --- |
| UX-01: Preserve identity, correct status color | Compare the next artifact with the reviewed brand reference: logo, type and general palette remain recognizable. Inspect normal, selected, informational, error and blocked examples: only genuine error/blocking states use reddish operational emphasis, and each state remains understandable without color through text/icons. Check text contrast and keyboard-visible focus, not appearance alone. | NFR-001; owner-requested semantic-color refinement |
| UX-02: Context has visible effect | Switch between two represented perspectives and two workflows using pointer and keyboard. Check visible context, expected case IDs/counts, applicable filters, evidence and actions against the manifest. Shared results are explained; unavailable actions state why. Announce updated scope/results without unexpected focus movement. An incompatible retained filter or selected case is cleared or explicitly explained. | FR-003/004/032/035; AC-005/006/034 |
| UX-03: Honest state and recovery | Exercise pending handoff, loading, no matches, no representative scenario and load failure through labelled mocks if needed. Each has distinct text; loading/failure never looks like success or zero actual work. Reset returns the declared perspective defaults with a usable focus position. | FR-032/035; AC-034; NFR-001/006 |
| UX-04: Readiness is evidence-based | Open ready-for-review and blocked/unknown examples. Identify current stage, next task, evidence/source/version, unmet prerequisite and responsible role without guessing. Missing evidence or approval keeps the step blocked/unknown; ready-for-review wording never claims authorized release or professional acceptance. | FR-008/025; AC-011/016/028 |
| UX-05: Ownership survives a handoff | Compare unassigned, sent, received, accepted and returned synthetic examples. Current owner, destination, proposed/confirmed receiver, chase owner and next-update owner are separately labelled. Receipt alone is not acceptance; an accepted state names its receiver and supporting event, and a pending/returned case still has an accountable follow-up. | FR-011/033; AC-014/035/036 |
| UX-06: Agent contribution is inspectable | Inspect a draft, a recommendation and a raise-only flag. Explain which permitted inputs/sources were used, what the agent produces, which decision it supports, what is unknown, who reviews it and what it cannot do. Unsupported inputs remain unknown; accepting a suggestion creates at most the permitted task/draft, not approval or external action. Include the explicit workflow-only/failure route. | FR-025-028; AC-028-030 |
| UX-07: Full-screen case is recoverable | From a filtered queue open a case full screen by keyboard; identity, evidence, tasks, readiness and owners remain accessible. Return restores role/workflow/search/filter/sort context, selection, queue position and focus to the originating control. Check logical headings, focus order/visibility, a labelled return/close control, narrow layout and 200% text zoom; no required task depends on hover or pointer alone. | FR-001/002/032; NFR-001; owner-requested full-screen refinement |
| UX-08: Necessary contact context, not invented data | Inspect a complete synthetic contact example and an incomplete one. Full address including postcode, resident phone, preferred/safe contact route and necessary adjustment references are available for the represented permitted task; missing fields say unknown/not supplied and name a follow-up, not fabricated values. Label all examples synthetic and provide no real contact actions. For production, require separate role/case/field access-denial checks across case detail, search, exports and AI inputs before release; hiding fields in a demo is not authorization evidence. | FR-003/014; AC-005/017/037; NFR-002/005 |

Use UX-01 to UX-03 for orientation first, UX-04 to UX-06 for an
exception-to-accountable-owner walkthrough, and UX-07 to UX-08 for the expanded
case workspace. Record artifact version, fixture IDs, expected versus actual
results and remaining gaps when these checks are eventually run. No timing,
completion-rate or satisfaction threshold is invented from this feedback.
Staff and accessible resident validation, production authority and privacy
review remain separate future gates.

## Shared Workbench IA Engineering Slice (2026-10-15)

Issue [#152](https://github.com/jmservera/ama/issues/152) retains shared
information architecture and layout; role-specific screens belong to #225 to
#233. Its owner comments move legacy paths to the accepted
[ADR 0006](../../../adrs/0006-src-layout-and-cutover.md) API web project without
changing acceptance criteria. The migrated runtime, not the retired prototype
perspective selector, is the implementation base.

The [API workbench guide](../../../../src/api/README.md#shared-workbench-information-architecture-152)
and [versioned synthetic manifest](../../../../src/api/checks/workbench-manifest.json)
define this bounded slice: server-described existing navigation, explicit
own/programme scope, reset to own defaults, mine/all return with retained
filters, early expanded safety information and responsive wrapping using the
merged Fluent-derived foundations. Navigation does not grant access. Existing
server role/case/field projection, human approval, resident consent and AI
release controls remain unchanged.

Engineering checks use fictional identities and records against a real local
API, including queue and hazard-case layouts at 320, 390, 768, 1024 and 1280 CSS
pixels and 200% root text enlargement. These widths are test inputs, not an
owner-approved supported-device matrix. The manifest distinguishes eight
implemented auth roles from eleven PRD research perspectives; all nine
workflows remain partial or deferred rather than being declared accepted.

UX-07 above remains only partially addressed: returning to a list retains its
mine/all scope, query, filters and sort but reloads the first page and focuses
main, not the originating row or previous queue position. Reset separately
restores own/default order and focuses its control. Full selection/focus/
position restoration, complete AC-034/043 profile journeys, browser zoom,
screen-reader/human task validation and owner device/browser decisions remain
unmet. Local browser checks do not establish actual model inference,
SQL Server/Azure durability, operational safety authority or customer outcomes.

## Provider capacity engineering continuation (2026-10-17, #90)

The migrated procurement/store/controller paths had delivered screens but
still admitted numeric-only commitments, unversioned appointment changes and
case advancement without a booked order. This bounded continuation enforces
the four issue criteria rather than claiming that previous UI delivery proves
them. Source requirements are PRD FR-016 and BRD RULE-007/008; BRD FR-016 is
exception control, not an interchangeable identifier.

The [core contract](../../../../src/core/README.md#evidenced-provider-capacity-and-controlled-orders-90)
binds original clean uploaded bytes/hash/version, dated human review,
covered homes, delivery interval and home-order units to the package scope
and trusted named contract delegation. Larger offers and unknown/legacy
commitments cannot authorize work. Each order mutation retains issuer and
version; system drafts never become instructions; two fictional contractors
see only their own orders and cannot write. Existing resident commitments,
safety/building gates, #78 provenance and #97 forms remain independent.

The [API/screen replay](../../../../src/api/README.md#provider-capacity-and-order-api-90)
uses tiny temporary fictional stores. Executed local SQL Server 2022 checks
exercise the same inherited domain/HTTP behavior and deterministic writer,
authority and source races, not Azure or live supplier orders. The browser
journey covers labelled evidence inputs, keyboard save/refusal focus,
at-quota booking, own-order views and 320/390/1280 reflow/reduced motion.
This narrows engineering gaps only: no real contract delegation, legal
signature verification, staff comprehension, screen-reader acceptance,
full WCAG conformance, financial commitment or actual company approval is
established. The procurement-manager research instrument is not such approval.

The coordinator's correction ONE review of PR #384 head 527a537 returned
Revise: blank immutable contract versions made new packages permanently
unusable. Creation now refuses omitted/empty/whitespace versions before
mutation, and the existing screen retains inputs with inline field focus.
The existing scenario manifest's exact public fixture hash is refreshed
without changing eleven/nine unavailable journey claims or provisional/
proposed authority. The safety-flow test now supplies a fictional evidenced
booking after independent release, rather than relying on removed bypass
behavior. These implementation corrections do not supersede the historical
Review or establish external correction acceptance; coordinator closure is
still required.
