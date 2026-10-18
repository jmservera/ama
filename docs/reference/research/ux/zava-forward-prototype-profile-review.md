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

At the original fifteen-row inspection, complete current/future screen-backlog
coverage was **unknown**. The later
[bounded issue inventory](#screen-backlog-coverage-snapshot-2026-10-18-156)
enumerates the remaining feature coverage without changing this original gate
record or supplying missing designs. Import/export,
operations/account, direct resident/representative screens
([#154](https://github.com/jmservera/ama/issues/154)), regulatory alerts/chat
([#215](https://github.com/jmservera/ama/issues/215)) and other feature-specific
states were outside this finite inventory. The dated inventory continuation
below now reconciles those feature scopes; #156's universal criterion still
requires the actual missing design artifacts and flow evidence.
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

## Screen backlog coverage snapshot (2026-10-18, #156)

This is the inventory continuation of
[#156](https://github.com/jmservera/ama/issues/156), not a replacement for
T01-T11/C01-C04, D01-D04 or G156 above. The
[owner's partial-delivery record](https://github.com/jmservera/ama/issues/156#issuecomment-6245518420)
keeps AC1 unticked after [#400](https://github.com/jmservera/ama/pull/400).
The source work below is complete for its declared issue universe; absent
design artifacts do not make inventory enumeration human-blocked.

### Universe, provenance and classification rules

The snapshot contains **all 184 public repository issues**, 139 open and
45 closed, captured on 2026-10-18 with retrieval completed before
**04:13:45 UTC**. It includes the open backlog and closed/delivered features,
not just fifteen profile examples. Issue numbers are sparse, from 6 to 360.
Pull requests, PR comments as separate backlog items, private data and work not
expressed as a repository issue are excluded. New issues or subsequent scope
changes require a dated delta; this is not a claim about all future screens.

The coordinator's all-state export (500 maximum) contained
184 unique issues, below its 500 cap. Independently traversing every REST page
with `gh api --paginate 'repos/jmservera/ama/issues?state=all&per_page=100'`,
excluding objects with `pull_request`, returned the same 184 IDs and per-ID
states: zero missing, extra, duplicate or state-mismatched issues. The
[REST issue source](https://api.github.com/repos/jmservera/ama/issues?state=all&per_page=100)
is mutable; the membership/state tables below are the frozen public projection.
Original export SHA-256:
`e3774b99ab045926f971b47b321847d35fef59c5368ecf1b3bedba7f28291117`;
captured REST JSONL SHA-256:
`c3364f3da214433d9773e1b02cfbc3a0efc432f062ba5c942408c6e7bc341016`.
Raw exports remain temporary, not a second knowledge library.

Issue scope/acceptance text was read, including non-screen-named stories and
all ambiguities. Linked current-source context is pinned to repository
**`2ca6d1c48bb95b65e6c349fe508e99c00a74efbe`** (also this slice's base);
the [PRD][bc-prd] is candidate v0.17.0, not fresh approval.
Live issue delivery paragraphs can be stale: #162 still says chat endpoints
do not exist, while the [current panel guide][bc-panel] describes merged
#160-163 storage. Source existence does not establish current rendered behavior.

| Exclusive classification | Total | Open | Closed | Meaning |
| --- | --- | --- | --- | --- |
| includes-screen | 74 | 57 | 17 | Explicit user-visible task, content, state or effect on a screen; includes cross-cutting changes, not only new pages |
| no-screen | 86 | 59 | 27 | Inspected scope requires data, service, tests, research, documentation or infrastructure, without an additional prescribed screen |
| epic-covered | 16 | 16 | 0 | Aggregate routed to classified children; "covered" means inventory routing, not delivered or accepted |
| unknown | 8 | 7 | 1 | Body reviewed; screen versus CLI/report/manual delivery remains an actual owner choice |
| Total | 184 | 139 | 45 | Disjoint membership, including closed issues; no silently omitted remainder |

Classification is intentionally conservative about visible effects. #327 stays
screen-bearing despite being a queue-performance fix; #160 storage prescribes
user thread actions; #110 ingestion requires visible exceptions. Conversely
#105's schema/envelope and #162's server isolation prescribe no additional UI;
their visible dependencies are #219 and #159-161. #117 has visible document
availability/retention controls in current source; #210 explicitly requires a
non-AI provision viewer. These distinctions cannot be proved by matching totals
or title keywords alone.

### Known screen features and exact trace or gap

Every row below is **includes-screen**. O/C records issue Open/Closed at the
snapshot, not design acceptance. The issue link targets its acceptance criteria
and is the feature/check provenance; checks remain required, not newly executed.
Journeys are hypotheses. A stage-based journey is not silently a detailed screen
task flow: where only partial flow context exists, the feature-specific gap is
explicit. T/C references identify exact existing rows in the
[profile trace](#profile-design-trace) or [core trace](#shared-core-flow-design-trace).

**All 74 issues lack a supplied current reviewable screen-design version.**
`NOT SUPPLIED` in the design column names that gap, not missing code or a
human approval. H/E retain their exact historical/engineering versions above;
only the explicitly named historical portion is linked, never the whole later
feature. API guides are supporting engineering evidence, not design artifacts.
Responsible roles are requested owners, not named delegations. For every row,
the design owner must supply a versioned candidate including applicable default,
focus, disabled, loading, empty, error, blocked and recovery states, then apply
the [existing design gate](#design-review-checklist-and-definition-of-done).
The last column adds the domain-specific missing evidence/action.

| Issue / state / screen evidence and check | Exact journey section | Existing task flow / explicit feature gap | Design artifact and version evidence | Responsible role / next action |
| --- | --- | --- | --- | --- |
| [#74](https://github.com/jmservera/ama/issues/74#acceptance-criteria) O: versioned home links and separate shared/per-home evidence | [Connected stages 2-3][bc-connected] | [Lifecycle/return][bc-lifecycle]; detailed linked-record navigation NOT SUPPLIED | NOT SUPPLIED; [H][design-h] T03 separate-home examples only | Programme + design / specify linked-record navigation without inherited approval |
| [#75](https://github.com/jmservera/ama/issues/75#acceptance-criteria) O: shared building systems, holds and cost views; [engineering](../../../../src/api/README.md#building-shared-context-issue-75) | [Designer/coordinator][bc-technical] | [Lifecycle/return][bc-lifecycle] dependency context; building-view task flow NOT SUPPLIED | NOT SUPPLIED | Technical + design / separate shared facts, home cost allocations and independent decisions |
| [#76](https://github.com/jmservera/ama/issues/76#acceptance-criteria) O: role queues, full-screen case and visible next action; [engineering](../../../../src/api/README.md#role-task-queues-and-shared-case-context-76) | [Programme planner][bc-programme] | [Profile flow][bc-profile], Programme coordinator; C01-C03 partial | NOT SUPPLIED; [H][design-h]/[E][design-e] C01-C03 only | Workbench + Programme design / cover all queue signals and current accountable ownership |
| [#77](https://github.com/jmservera/ama/issues/77#acceptance-criteria) C: signal definitions, active scope and reset; [dated source](#queue-signal-engineering-continuation-2026-10-17-77) | [Programme planner][bc-programme] | [IA flow][bc-ia], own/programme -> filter -> reset; C01 | NOT SUPPLIED; [H][design-h]/[E][design-e] C01 partial | Workbench design / design exact versioned default, reset, selected rationale and unknown owner states |
| [#78](https://github.com/jmservera/ama/issues/78#acceptance-criteria) C: editable fields and bulk preview; [engineering](../../../../src/api/README.md#controlled-bulk-preview-api-78) | [Data steward][bc-data] | NOT SUPPLIED for preview -> inspect failures -> apply -> per-case outcome | NOT SUPPLIED | Data + design / show source/version/reason and forbidden controlled actions in preview/recovery |
| [#79](https://github.com/jmservera/ama/issues/79#acceptance-criteria) O: ranking reason codes and policy owner; [source behavior][bc-staff] | [Asset baseline][bc-asset] | [Asset flow][bc-eleven] T01 partial; policy inspection task flow NOT SUPPLIED | NOT SUPPLIED; [H][design-h] T01 queue only | Asset/policy + design / supply explain-order and unsigned/unknown policy-owner states |
| [#80](https://github.com/jmservera/ama/issues/80#acceptance-criteria) O: workbook mapping/conflict preview and every-list export | [Data steward][bc-data] | NOT SUPPLIED for import/row fix/export/read-only comparison | NOT SUPPLIED | Data + design / design declared workbook errors, lineage and one-way source protection |
| [#82](https://github.com/jmservera/ama/issues/82#acceptance-criteria) O: pass/fail/unknown reasons at controlled transitions | [Connected stages 3-6][bc-connected] | [Lifecycle/return][bc-lifecycle]; C03 partial | NOT SUPPLIED; [H][design-h] blocked examples, not all gates | Programme/control + design / show each missing prerequisite and independent authority |
| [#83](https://github.com/jmservera/ama/issues/83#acceptance-criteria) O: return/reopen and distinct handoff ownership states; [engineering](../../../../src/api/README.md#return-and-handoff-api-83) | [Programme planner][bc-programme] | [Lifecycle/return][bc-lifecycle]; [profile flow][bc-profile], Programme coordinator | NOT SUPPLIED; [H][design-h] T02/C03 returned example only | Programme + design / separate sent, receipt, acceptance, chase and update ownership |
| [#84](https://github.com/jmservera/ama/issues/84#acceptance-criteria) C: both stock values, sign-offs and design version; [engineering](../../../../src/api/README.md#stock-reconciliation-api-84) | [Assessor][bc-assessor] / [designer][bc-technical] | [Technical flow][bc-eleven] T04; conflict-to-reapproval details NOT SUPPLIED | NOT SUPPLIED; [H][design-h] T04 missing-reference example | Technical + design / design compared sources and only affected reapproval |
| [#85](https://github.com/jmservera/ama/issues/85#acceptance-criteria) C: visible referral receipt/acceptance, hold and service times | [Repairs/hazard][bc-safety] | [Safety flow][bc-eleven] T06 | NOT SUPPLIED; [H][design-h] T06 historical referral only | Safety + design / retain external hazard authority, unknown times and owned follow-up |
| [#86](https://github.com/jmservera/ama/issues/86#acceptance-criteria) O: per-measure decisions, representative authority and withdrawal; [engineering](../../../../src/api/README.md#resident-decisions-and-representative-api-86) | [Household][bc-household] / [representative][bc-representative] | [Profile flow][bc-profile], Housing and Resident Engagement; pause/authority expiry details NOT SUPPLIED | NOT SUPPLIED; [H][design-h] T05 contact only, not decision-state designs | Housing + design / design Not recorded, limited/disputed authority and scoped pause/review |
| [#87](https://github.com/jmservera/ama/issues/87#acceptance-criteria) C: offers, confirmed commitments and household constraints | [Household][bc-household] | [Appointment boundary](./customer-journeys/residents.md#appointment-control-engineering-boundary-2026-10-18-87); full offer/confirmation task-flow design NOT SUPPLIED | NOT SUPPLIED | Housing/coordination + design / show three confirmations, no-access investigation and independent urgent route |
| [#88](https://github.com/jmservera/ama/issues/88#acceptance-criteria) C: update commitments and separately owned remedy states | [Engagement][bc-engagement] / [redress][bc-redress] | [Resident criterion audit](./customer-journeys/residents.md#resident-commitment-and-remedy-criterion-audit-2026-10-17-88); update/remedy screen flow NOT SUPPLIED | NOT SUPPLIED | Housing/redress + design / separate response, remedy, defect, charge-query and closure states |
| [#90](https://github.com/jmservera/ama/issues/90#acceptance-criteria) C: committed capacity, versioned orders and own-order view | [Procurement][bc-supplier] | [Procurement flow][bc-eleven] T07; [profile flow][bc-profile], Provider T08 partial | NOT SUPPLIED; [H][design-h] T07/08 draft package, no booking/portal | Procurement + design / show capacity evidence, instruction authority and draft-only readiness |
| [#91](https://github.com/jmservera/ama/issues/91#acceptance-criteria) C: checklist, defects, remediation and independent handover | [Independent QA][bc-quality] | [Quality flow][bc-eleven] T09; [lifecycle][bc-lifecycle] | NOT SUPPLIED; [H][design-h] T09 incomplete-pack example | Quality + design / design current per-measure review, evidence replacement and reinspection |
| [#92](https://github.com/jmservera/ama/issues/92#acceptance-criteria) O: recorded consultation status controlling contract release | [Leasehold service][bc-leasehold] | NOT SUPPLIED for Legal status -> contract let/renew block -> reviewed resolution | NOT SUPPLIED | Legal/contracts + design / decide status-entry/review surface; unknown blocks release, no lease inference |
| [#94](https://github.com/jmservera/ama/issues/94#acceptance-criteria) C: invoice intake, line exceptions, holds and Finance disposition | [Payment officer][bc-payment] | [Profile flow][bc-profile], Finance and Grants T10 | NOT SUPPLIED; [H][design-h] T10 invoice exception only | Finance + design / design line comparison, independent review and record-only outcome |
| [#95](https://github.com/jmservera/ama/issues/95#acceptance-criteria) C: separate grant stages and dashboard meaning | [Grant preparer][bc-finance] / [approver][bc-finance-approver] | [Profile flow][bc-profile], Finance T10 partial; full grant-stage flow NOT SUPPLIED | NOT SUPPLIED; [H][design-h] does not cover later application/export contract | Finance/grants + design / separate opportunity, application, award, claim and cash evidence |
| [#96](https://github.com/jmservera/ama/issues/96#acceptance-criteria) O: assisted form review, validation and export | [Grant preparer][bc-finance] | [Assisted form sequence][bc-forms]; T10 partial | NOT SUPPLIED | Finance/forms + design / design candidate lineage, field disposition, stale dependencies and reviewed export |
| [#97](https://github.com/jmservera/ama/issues/97#acceptance-criteria) O: schema/candidate lineage supporting form fields; [engineering](../../../../src/api/README.md#form-schema-and-candidate-api-97) | [Grant preparer][bc-finance] | [Assisted form sequence][bc-forms]; schema selection/staging details NOT SUPPLIED | NOT SUPPLIED | Forms + design / design unknown/unapproved template and raw candidate lineage without invented authority |
| [#98](https://github.com/jmservera/ama/issues/98#acceptance-criteria) O: field review, validation report and pack history | [Grant preparer][bc-finance] | [Assisted form sequence][bc-forms] | NOT SUPPLIED | Forms/Finance + design / design per-field correction, validation and exact stale-review recovery |
| [#99](https://github.com/jmservera/ama/issues/99#acceptance-criteria) O: human-approved investment inputs and breach pause signal | [Asset executive][bc-asset] / [Board][bc-board] | NOT SUPPLIED for envelope inspection -> breach -> human disposition | NOT SUPPLIED | Asset/Finance + design / show unknown inputs, downside and pause without investment approval |
| [#101](https://github.com/jmservera/ama/issues/101#acceptance-criteria) C: map, funnel, denominators and drill-through | [Programme planner][bc-programme] | [Population/funnel boundary](./customer-journeys/programme.md#coordinator-population-and-observed-funnel-boundary-2026-10-17-101); complete map/funnel task flow NOT SUPPLIED | NOT SUPPLIED | Programme/Data + design / show selection versus metric population, missing coordinates and partial history |
| [#102](https://github.com/jmservera/ama/issues/102#acceptance-criteria) C: historical progression, forecast and export | [Programme planner][bc-programme] / [Board][bc-board] | [Historical progress boundary](./customer-journeys/programme.md#historical-progress-engineering-boundary-2026-10-17-102); report/forecast/export task flow NOT SUPPLIED | NOT SUPPLIED | Programme/Data + design / design as-of/denominator, declared assumptions and unresolved exceptions |
| [#106](https://github.com/jmservera/ama/issues/106#acceptance-criteria) C: cited suggestions and accept/edit/reject/manual path | [Bounded opportunities][bc-opportunities] | [UX-06][bc-ux], inspect -> draft -> human review/manual; C04 | NOT SUPPLIED; [H][design-h] C04 static suggestion only | Assistant/content + design / design review reason, unverified source and failure/manual states |
| [#107](https://github.com/jmservera/ama/issues/107#acceptance-criteria) O: five assistants' optional proposal/review surfaces | [Bounded opportunities][bc-opportunities] | [Five assistant contract][bc-assistants]; C04 partial, per-capability task flows NOT SUPPLIED | NOT SUPPLIED | Assistant owners + design / supply each source/reviewer/denial path; proactive scan never acts as approval |
| [#110](https://github.com/jmservera/ama/issues/110#acceptance-criteria) O: invalid/out-of-order/unmapped readings visible as exceptions | [Data operator][bc-operator] | NOT SUPPLIED for ingestion exception -> inspection -> controlled recovery | NOT SUPPLIED | Data/IoT operator + design / locate owned exception surface without exposing device IDs/raw readings |
| [#111](https://github.com/jmservera/ama/issues/111#acceptance-criteria) O: deterministic human sensor-review task and INSUFFICIENT state | [Evaluator][bc-quality] / [Data][bc-data] | NOT SUPPLIED for signal -> human task -> insufficiency/review outcome | NOT SUPPLIED | Sensor/evaluation + design / show version/source limits, never hazard diagnosis or reduced priority |
| [#112](https://github.com/jmservera/ama/issues/112#acceptance-criteria) C: protected map/export/AI context; [source](../../../../src/core/README.md#sensor-admission-and-external-context-112) | [DPO/control reviewer][bc-control] | NOT SUPPLIED for monitoring privacy admission and map/export state inspection | NOT SUPPLIED | DPO/Data + design / preserve raw-reading exclusions and synthetic-only admission labels |
| [#116](https://github.com/jmservera/ama/issues/116#acceptance-criteria) O: sign-in and role/field visibility; [source][bc-staff] | NOT SUPPLIED for sign-in/account journey; [operator context][bc-operator] only | NOT SUPPLIED for sign-in, denied role, logout/account recovery | NOT SUPPLIED | Identity/workbench + design / supply permitted/denied/account states without treating navigation as rights |
| [#117](https://github.com/jmservera/ama/issues/117#acceptance-criteria) O: upload scan availability, retention approval and legal holds; [source][bc-staff] | [Data operator][bc-operator] / [control reviewer][bc-control] | NOT SUPPLIED for scan pending/refusal, retention approval and hold recovery | NOT SUPPLIED | Records/DPO + design / design unavailable documents and separate human deletion/hold controls |
| [#119](https://github.com/jmservera/ama/issues/119#acceptance-criteria) O: licensed map with accessible list alternative | [Programme planner][bc-programme] | NOT SUPPLIED for map -> equivalent list -> case and unavailable-tile recovery | NOT SUPPLIED | Map/accessibility + design / supply equivalent population/navigation and approved provider state |
| [#120](https://github.com/jmservera/ama/issues/120#acceptance-criteria) O: gated staff-time entry, notice and aggregate reports; [source][bc-staff] | NOT SUPPLIED for staff-time capture journey; [control context][bc-control] only | NOT SUPPLIED for notice -> own entries -> gated/suppressed report | NOT SUPPLIED | Staff/privacy + design / supply off/approval-gap/notice states, never infer DPIA approval |
| [#122](https://github.com/jmservera/ama/issues/122#acceptance-criteria) O: manual fallback, disable and evidence export | [Data operator][bc-operator] | [UX-06][bc-ux] manual/failure partial; service outage/disable/export flow NOT SUPPLIED | NOT SUPPLIED | Operator + design / show honest outage and controlled recovery, keep manual safety paths |
| [#130](https://github.com/jmservera/ama/issues/130#acceptance-criteria) O: nomination, acknowledgement and challenge | [Nomination/challenge][bc-nomination] | [Nomination staged subjourney][bc-nomination] | NOT SUPPLIED | Housing/intake + design / design original account, identity correction and acknowledged owner; urgent route independent |
| [#131](https://github.com/jmservera/ama/issues/131#acceptance-criteria) O: tenure verification and reviewed responsibility-question pack | [Leasehold service][bc-leasehold] / [shared owner][bc-shared-owner] | [Leasehold stage map][bc-leasehold]; detailed pack/authority task flow NOT SUPPLIED | NOT SUPPLIED | Leasehold/Legal + design / show ambiguity/unknown route and human-reviewed terms, no lease interpretation |
| [#132](https://github.com/jmservera/ama/issues/132#acceptance-criteria) O: job pack, submission/correction and offline/no-show recovery | [Installer][bc-installer] / [scheduler][bc-scheduler] | [Profile flow][bc-profile], Provider T08 partial; offline capture task flow NOT SUPPLIED | NOT SUPPLIED; [H][design-h] T08 staff package, no provider identity/portal | Procurement/fieldwork + design / design mediated intake, acknowledgement versus acceptance and safe recovery |
| [#133](https://github.com/jmservera/ama/issues/133#acceptance-criteria) O: concern route, human investigation and lived-performance view | [Household][bc-household] / [Evaluator][bc-quality] | [Connected stages 7-8][bc-connected]; detailed aftercare task flow NOT SUPPLIED | NOT SUPPLIED | Aftercare/Quality + design / show concern/remedy owner and unknown outcomes without blame or savings promise |
| [#134](https://github.com/jmservera/ama/issues/134#acceptance-criteria) O: eleven walkthroughs and connected same-home acceptance | [Connected journey][bc-connected] | [Profile contract][bc-profile] / [lifecycle][bc-lifecycle] | NOT SUPPLIED; [H][design-h]/[E][design-e] T01-T11 partial/deferred, not connected acceptance | Programme + design / supply genuinely linked same-home states and independent sibling decisions |
| [#135](https://github.com/jmservera/ama/issues/135#acceptance-criteria) O: conflict, failure and stranded-work exception queue | [Data steward][bc-data] / [operator][bc-operator] | [Digital flow][bc-eleven] T11 partial; import/model recovery task flow NOT SUPPLIED | NOT SUPPLIED; [H][design-h] T11 narrative, not operational audit | Data/operator + design / show both sources and owned controlled recovery, no silent replay |
| [#146](https://github.com/jmservera/ama/issues/146#acceptance-criteria) O: operational dashboard/workbook, alerts and runbooks | [Data operator][bc-operator] | NOT SUPPLIED for dashboard -> alert -> owned runbook/recovery | NOT SUPPLIED | Operations + design / identify external workbook versus workbench surface and exact budget/error states |
| [#150](https://github.com/jmservera/ama/issues/150#acceptance-criteria) C: component states, tokens and AI review pattern | [All-user atlas](./customer-journeys/customer-journey-atlas.md#all-user-coverage-and-jobs-to-improve) | [Core UX checks][bc-ux]; shared pattern state flows NOT SUPPLIED | NOT SUPPLIED; [design specification](./design-system.md#component-inventory) at source base, not current rendered acceptance | Design-system owner / evidence selected Fluent 2 implementation and every applicable component state; D01 status caveat retained |
| [#151](https://github.com/jmservera/ama/issues/151#acceptance-criteria) O: keyboard, focus, reflow, errors and equivalent charts | [Profile journeys][bc-profile] | [UX-02/03/07][bc-ux]; [manual check record](./wcag-conformance-baseline.md#manual-check-record), not results | NOT SUPPLIED | Accessibility + design / assign exact scope/candidate/testers and record actual checks, not conformance by assertion |
| [#152](https://github.com/jmservera/ama/issues/152#acceptance-criteria) O: responsive shared IA and recoverable navigation | [Programme planner][bc-programme] | [IA flow][bc-ia]; C01/C02/C04 | NOT SUPPLIED; [E][design-e] `152-ia-v1` engineering, partial/deferred | Workbench + design / supply supported-device choice and full selection/position/focus return design |
| [#153](https://github.com/jmservera/ama/issues/153#acceptance-criteria) O: statuses, next actions, errors, AI and resident copy | [Engagement][bc-engagement] / [profile contract][bc-profile] | [Core copy audit](./content-standard.md#copy-audit-of-the-core-flow); UX-03/04/06 partial | NOT SUPPLIED; content standard at source base, not accepted current text versions | Content + design / version exact strings, remove internal terms, obtain named resident-wording review |
| [#154](https://github.com/jmservera/ama/issues/154#acceptance-criteria) O: staff-supported resident/representative choice, visits, updates and aftercare | [Household][bc-household], [shared owner][bc-shared-owner], [representative][bc-representative] | [Connected stages][bc-connected]; detailed accessible/non-digital interaction task flows NOT SUPPLIED | NOT SUPPLIED; T05 is staff-only historical context, not direct resident designs | Resident Engagement + design / supply task-limited authority, safe contact and non-digital alternatives; no portal inferred |
| [#159](https://github.com/jmservera/ama/issues/159#acceptance-criteria) O: optional cited case conversation panel; [source][bc-panel] | [PRD journey/agent/UI mapping][bc-chat-map] | [Chat mapping][bc-chat-map] entry/draft/manual partial; detailed conversation recovery flow NOT SUPPLIED | NOT SUPPLIED; no H/E chat design | Assistant + design / design reply/abstention/failure/announcement states; panel is distinct from #160 storage |
| [#160](https://github.com/jmservera/ama/issues/160#acceptance-criteria) O: own thread list/resume/archive/delete | [PRD staff chat mapping][bc-chat-map] | NOT SUPPLIED for thread lifecycle; FR-056/AC-094-095 in [chat requirements][bc-chat-requirements] are checks, not flow | NOT SUPPLIED | Chat/privacy + design / supply own-thread lifecycle and metadata/content distinction |
| [#161](https://github.com/jmservera/ama/issues/161#acceptance-criteria) O: opt-in inspect/edit/delete/expiry and off states | [PRD staff chat mapping][bc-chat-map] | NOT SUPPLIED for preference consent, inspection, edit, withdrawal and expiry | NOT SUPPLIED | Chat/DPO + design / supply memory states; unknown retention remains unknown, never controlled evidence |
| [#163](https://github.com/jmservera/ama/issues/163#acceptance-criteria) O: free-text warning, transparency and rights handling; [panel source][bc-panel] | [DPO/control reviewer][bc-control]; staff privacy journey NOT SUPPLIED | NOT SUPPLIED for notice/warning/rights interaction | NOT SUPPLIED | DPO/content + design / design minimised warning and request route without setting unapproved retention |
| [#210](https://github.com/jmservera/ama/issues/210#acceptance-criteria) C: explicit non-AI read-only provision viewer | [Control reviewer][bc-control] / [source change][bc-source-change] | NOT SUPPLIED for viewer search -> provision/status -> missing/partial source | NOT SUPPLIED | Regulatory product + design / supply non-AI source-viewer flow, dates/completeness and no-source state |
| [#211](https://github.com/jmservera/ama/issues/211#acceptance-criteria) O: human rule-card review/hold lifecycle; [API-only boundary](../../../../src/api/README.md#rule-card-approval-api-211) | [Controlled source change][bc-source-change] | [Source-change stages][bc-source-change] partial; rule-card interaction task flow NOT SUPPLIED | NOT SUPPLIED; source explicitly says no rule-card UI delivered | Compliance + design / supply separate author/owner/hold states; no source download or role nomination means approval |
| [#212](https://github.com/jmservera/ama/issues/212#acceptance-criteria) O: cited step alerts, owner, clock and acknowledgement | [Regulatory role needs][bc-reg-roles] | [Regulatory integration sequence][bc-reg-flow]; alert acknowledgement flow NOT SUPPLIED | NOT SUPPLIED | Compliance/Safety + design / design unknown/future/stale states and independent emergency intake |
| [#214](https://github.com/jmservera/ama/issues/214#acceptance-criteria) O: home chat, conflicting sources and one-action doubt route | [Control reviewer][bc-control] / [role needs][bc-reg-roles] | [When in doubt][bc-doubt]; chat -> referral -> owner response details NOT SUPPLIED | NOT SUPPLIED | Regulatory/chat + design / design source/status dates, refusal and owned doubt, never legal conclusion |
| [#215](https://github.com/jmservera/ama/issues/215#acceptance-criteria) O: role-shaped alert/chat patterns and comprehension; [engineering](../../../../src/api/README.md#regulatory-alert-and-home-chat-ux-215) | [Regulatory role needs][bc-reg-roles] | [Integration][bc-reg-flow] / [doubt routes][bc-doubt]; full role/state task flows NOT SUPPLIED | NOT SUPPLIED; existing patterns/protocol are not passed comprehension or current design acceptance | Compliance/content + design / supply all role patterns, no-source/doubt states and actual staff comprehension evidence |
| [#217](https://github.com/jmservera/ama/issues/217#acceptance-criteria) O: regulatory privacy warning and unknown/simulated retention; [source](../../../../src/api/README.md#regulatory-security-privacy-and-audit-217) | [DPO/control reviewer][bc-control] | NOT SUPPLIED for regulatory privacy disclosure/rights interaction | NOT SUPPLIED | DPO/regulatory + design / supply exact warning/status text; simulated settings never imply approved disposal |
| [#219](https://github.com/jmservera/ama/issues/219#acceptance-criteria) O: visible release denial, missing evidence, owner/manual route; [source](../../../../src/api/README.md#rai-task-release-api-219) | [Control reviewer][bc-control] / [operator][bc-operator] | [UX-06][bc-ux] manual route partial; release-denial task flow NOT SUPPLIED | NOT SUPPLIED | AI release/control + design / show version mismatch, expiry, authority gap and non-actionable drafts |
| [#220](https://github.com/jmservera/ama/issues/220#acceptance-criteria) O: challenge/correction, explanation, owner and update | [Nomination/challenge][bc-nomination] / [redress][bc-redress] | [Challenge stages][bc-nomination]; AI/policy-specific interaction flow NOT SUPPLIED | NOT SUPPLIED | Housing/redress + design / supply accessible digital/staff-recorded routes and independent resolution |
| [#221](https://github.com/jmservera/ama/issues/221#acceptance-criteria) O: operator suspension and visible blocked proposals/manual route | [Data operator][bc-operator] | [Operator recover stage][bc-operator] context; suspend/incident/restart task flow NOT SUPPLIED | NOT SUPPLIED | Operator/AI release + design / design scoped suspension, separate restart authority and uninterrupted manual/hazard work |
| [#225](https://github.com/jmservera/ama/issues/225#acceptance-criteria) O: Finance/grants role screens | [Preparer][bc-finance] / [approver][bc-finance-approver] / [payment][bc-payment] | [Profile flow][bc-profile], Finance T10; [forms][bc-forms] | NOT SUPPLIED; [H][design-h]/[E][design-e] T10 partial | Finance + design / supply invoice/route/claim pack versions and explicit unknown/exception states |
| [#226](https://github.com/jmservera/ama/issues/226#acceptance-criteria) O: Asset/Board source conflicts, investment and phase views | [Asset][bc-asset] / [Board][bc-board] | [Asset flow][bc-eleven] T01; Board investment/phase flow NOT SUPPLIED | NOT SUPPLIED; [H][design-h]/[E][design-e] T01 partial/deferred | Asset + design / design portfolio scope, source age and missing investment inputs without approval |
| [#227](https://github.com/jmservera/ama/issues/227#acceptance-criteria) O: safety referral queue and hold/release evidence | [Safety lead](./customer-journeys/safety.md#current-state-map-a-building-safetycompliance-lead) / [repairs][bc-safety] | [Safety flow][bc-eleven] T06 | NOT SUPPLIED; [H][design-h]/[E][design-e] T06 partial | Safety + design / show awareness/source and distinct referral/receipt/acceptance with authoritative release evidence |
| [#228](https://github.com/jmservera/ama/issues/228#acceptance-criteria) O: procurement capacity and staff-facing contractor capture | [Procurement][bc-supplier] / [scheduler][bc-scheduler] / [installer][bc-installer] | [Procurement flow][bc-eleven] T07; [profile flow][bc-profile], Provider T08 | NOT SUPPLIED; [H][design-h]/[E][design-e] T07/08 partial/deferred | Procurement + design / supply draft readiness and submission/correction designs; no provider portal or booking inferred |
| [#229](https://github.com/jmservera/ama/issues/229#acceptance-criteria) O: data conflict/exception/recovery screens | [Data steward][bc-data] / [operator][bc-operator] / [auditor](./customer-journeys/data.md#current-map-4-independent-audit--regulatory-assurance-reviewer) | [Digital flow][bc-eleven] T11 | NOT SUPPLIED; [H][design-h]/[E][design-e] T11 historical/deferred | Data/operator + design / supply compared values, original source/event metadata and controlled recovery |
| [#230](https://github.com/jmservera/ama/issues/230#acceptance-criteria) O: Programme queues, handoffs and lifecycle/funnel | [Programme planner][bc-programme] / [connected journey][bc-connected] | [Profile flow][bc-profile] T02/03; [lifecycle][bc-lifecycle] C03 | NOT SUPPLIED; [H][design-h]/[E][design-e] partial, separate homes not one lifecycle | Programme + design / supply return/sender/current-owner states, separate chase/update and connected-home evidence |
| [#231](https://github.com/jmservera/ama/issues/231#acceptance-criteria) O: assessor/designer/QA evidence, sign-off and returns | [Assessor][bc-assessor] / [designer][bc-technical] / [QA][bc-quality] | [Technical/Quality flows][bc-eleven] T04/09 | NOT SUPPLIED; [H][design-h]/[E][design-e] partial, technical script deferred | Technical/Quality + design / supply separate competent returns, per-measure pack and independent reinspection |
| [#232](https://github.com/jmservera/ama/issues/232#acceptance-criteria) O: housing/contact-centre/engagement staff screens | [Housing officer](./customer-journeys/frontline.md#1-neighbourhood-housing-officer), [contact centre](./customer-journeys/frontline.md#2-contact-centre--assisted-intake-staff-proxy), [engagement][bc-engagement] | [Profile flow][bc-profile], Housing T05 | NOT SUPPLIED; [H][design-h]/[E][design-e] T05 partial, not #154 direct designs | Housing + design / supply measure/version choice, purpose/owner/safe-route update; access never consent |
| [#233](https://github.com/jmservera/ama/issues/233#acceptance-criteria) O: cross-role atlas-to-screen design pass, not an epic | [Atlas themes](./customer-journeys/customer-journey-atlas.md#five-design-themes-and-tensions) / [connected journey][bc-connected] | [All eleven flows][bc-eleven] / [profile contract][bc-profile]; theme-to-state task-flow resolutions NOT SUPPLIED | NOT SUPPLIED; [H][design-h]/[E][design-e] fifteen prior rows are not all atlas designs | Atlas/design owners / record every theme/perspective resolution or explicit deferral and actual same-home walkthrough |
| [#327](https://github.com/jmservera/ama/issues/327) C: queue filter latency and CSV behavior under scale | [Programme planner][bc-programme] | [IA filter/reset][bc-ia] C01; no new flow prescribed | NOT SUPPLIED; [E][design-e] queue fixture, not 60k performance/design acceptance | Workbench + design / retain filter/count/status behavior while assessing slow/loading recovery |
| [#344](https://github.com/jmservera/ama/issues/344#acceptance-criteria) O: public welcome, browser sign-in and deployed workbench access | NOT SUPPLIED for entry/account journey; [operator context][bc-operator] | NOT SUPPLIED for public entry -> Entra -> role workbench -> failure recovery | NOT SUPPLIED | Identity/deployment + design / supply entry/denial/callback states; redirect is not successful role access |
| [#349](https://github.com/jmservera/ama/issues/349#acceptance-criteria) O: sign-in callback/session, logout/account switch and denial | NOT SUPPLIED for authenticated account journey | NOT SUPPLIED for account switching and unknown/wrong-role recovery | NOT SUPPLIED | Tenant/identity + design / supply user-facing recovery designs; actual tenant authority remains separate |
| [#350](https://github.com/jmservera/ama/issues/350#acceptance-criteria) O: deployed feature parity across roles, profile/session, maps, chat and law | [Profile journeys][bc-profile]; account/photo journey NOT SUPPLIED | [Existing profile flows][bc-profile] partial; [dated parity audit](../../../architecture/mvp-to-src-parity-matrix.md#public-deployment-feature-audit-2026-10-16) is engineering inventory, not task flow | NOT SUPPLIED; historical asset presence is not rendered/authorized parity | Workbench/deployment + design / map missing current account/photo and other parity-state designs; no whole-UI validation claimed |
| [#360](https://github.com/jmservera/ama/issues/360#acceptance-criteria) O: direct demo HTTPS welcome/sign-in/role entry | NOT SUPPLIED for direct-ingress entry journey; [operator context][bc-operator] | NOT SUPPLIED for direct entry/auth/error recovery | NOT SUPPLIED | Deployment/identity + design / supply direct entry states; no live migration, deletion or spend authorized here |

### Reviewed ambiguities requiring only explicit surface decisions

These eight **unknown** issues are not unreviewed inventory. Their bodies were
inspected; each has precisely one unresolved delivery-surface question. They
are excluded from the 74 known-screen count, not declared screen-free. If an
owner selects a screen, add its exact trace/design requirement; no human design
approval is implied by making that choice. Current screen artifact and detailed
interaction task flow are **NOT SUPPLIED for all eight**.

| Issue / state / evidence | Existing partial journey/flow context | Missing choice / responsible role / next action |
| --- | --- | --- |
| [#121](https://github.com/jmservera/ama/issues/121#acceptance-criteria) O: lawful-basis/retention records and rights requests must be logged/responded to; no interface specified | [DPO/control reviewer][bc-control]; no rights-request interaction flow | DPO/records + product / select existing service/manual record versus dedicated rights UI; specify requester/handler surfaces if needed |
| [#125](https://github.com/jmservera/ama/issues/125#acceptance-criteria) O: optional read-only discovery assistant, readiness and comparator; no entry/output surface specified | [Data steward][bc-data] discovery context; no assistant task flow | Discovery product owner / select report/CLI/manual analysis versus workbench assistant surface |
| [#126](https://github.com/jmservera/ama/issues/126#acceptance-criteria) O: benefits register, phase release decision and guardrail pause; no UI specified | [Board journey][bc-board] / [operator][bc-operator] | Sponsor/Programme / select governed document/register versus phase-gate screen; do not assume #226 supplies it |
| [#127](https://github.com/jmservera/ama/issues/127#acceptance-criteria) C: review-item logging and human-approved activation; closure says nothing about screen choice | [Controlled source-change stages][bc-source-change] | Compliance product owner / identify document/API review route or screen; keep #213 automation distinct |
| [#187](https://github.com/jmservera/ama/issues/187#acceptance-criteria) O: simulator replay, speed/pause controls and fault truth; interface unspecified | [Operator recovery][bc-operator] context, not simulator UI flow | Simulator owner / select CLI/run configuration versus operator screen; record control surface |
| [#189](https://github.com/jmservera/ama/issues/189#acceptance-criteria) O: simulator start/stop/scale controls, owner/time limit/budget; interface unspecified | [Operator][bc-operator] context, not cost-control UI flow | Simulator/Finance owner / select CLI/job-budget control versus dashboard; no run/spend approved |
| [#213](https://github.com/jmservera/ama/issues/213#acceptance-criteria) O: automated detection stores review items and routes to owner; no human interaction surface specified | [Source-change stages][bc-source-change]; #211 API is not a delivered review UI | Compliance/operator product owner / identify review queue UI versus API/document route and handoff |
| [#222](https://github.com/jmservera/ama/issues/222#acceptance-criteria) O: versioned cohort/error/burden evaluation record; no viewer prescribed | [Data steward][bc-data] / [control reviewer][bc-control] | Evaluation/RAI owner / select versioned report versus screen; define scope without inventing approved thresholds |

### No-screen membership and exclusion evidence

All issues listed here are **no-screen**, under the bounded rule above. The
rationale describes their required deliverable, not a statement that they have
no dependencies, could never affect UI or are fully delivered. O/C columns
freeze issue state. Explicit screen-impact dependencies already have rows above;
there is no "other" bucket.

| Inspected scope / exclusion rationale | Open issue IDs | Closed issue IDs |
| --- | --- | --- |
| Workflow detection/scoring failures; automation fixes, not product screens | [#6](https://github.com/jmservera/ama/issues/6), [#10](https://github.com/jmservera/ama/issues/10), [#33](https://github.com/jmservera/ama/issues/33), [#38](https://github.com/jmservera/ama/issues/38), [#46](https://github.com/jmservera/ama/issues/46), [#47](https://github.com/jmservera/ama/issues/47), [#48](https://github.com/jmservera/ama/issues/48), [#49](https://github.com/jmservera/ama/issues/49) | [#23](https://github.com/jmservera/ama/issues/23), [#51](https://github.com/jmservera/ama/issues/51), [#52](https://github.com/jmservera/ama/issues/52), [#53](https://github.com/jmservera/ama/issues/53), [#64](https://github.com/jmservera/ama/issues/64), [#206](https://github.com/jmservera/ama/issues/206) |
| Registry schema/envelope, evaluation or server isolation, not an additional UI; visible release/panel effects map to #219/#159-161 | [#108](https://github.com/jmservera/ama/issues/108), [#162](https://github.com/jmservera/ama/issues/162), [#164](https://github.com/jmservera/ama/issues/164), [#216](https://github.com/jmservera/ama/issues/216), [#223](https://github.com/jmservera/ama/issues/223) | [#103](https://github.com/jmservera/ama/issues/103), [#105](https://github.com/jmservera/ama/issues/105) |
| Discovery, equity/journey experiments and usability study/protocol, not new screen delivery; candidate screens stay separately mapped | [#124](https://github.com/jmservera/ama/issues/124), [#128](https://github.com/jmservera/ama/issues/128), [#129](https://github.com/jmservera/ama/issues/129), [#155](https://github.com/jmservera/ama/issues/155) | None |
| Documentation/authority decisions and legal assessment; #156 is this register/gate, not another application screen | [#156](https://github.com/jmservera/ama/issues/156), [#224](https://github.com/jmservera/ama/issues/224) | [#158](https://github.com/jmservera/ama/issues/158), [#209](https://github.com/jmservera/ama/issues/209) |
| SQL/ledger/digest, deployment/CI, credentials, network/governance and recovery infrastructure; operator dashboard #146 and browser entry #344/#349/#360 separately included | [#114](https://github.com/jmservera/ama/issues/114), [#115](https://github.com/jmservera/ama/issues/115), [#118](https://github.com/jmservera/ama/issues/118), [#137](https://github.com/jmservera/ama/issues/137), [#138](https://github.com/jmservera/ama/issues/138), [#139](https://github.com/jmservera/ama/issues/139), [#140](https://github.com/jmservera/ama/issues/140), [#141](https://github.com/jmservera/ama/issues/141), [#142](https://github.com/jmservera/ama/issues/142), [#143](https://github.com/jmservera/ama/issues/143), [#144](https://github.com/jmservera/ama/issues/144), [#145](https://github.com/jmservera/ama/issues/145), [#147](https://github.com/jmservera/ama/issues/147), [#148](https://github.com/jmservera/ama/issues/148), [#358](https://github.com/jmservera/ama/issues/358) | [#290](https://github.com/jmservera/ama/issues/290), [#322](https://github.com/jmservera/ama/issues/322), [#323](https://github.com/jmservera/ama/issues/323), [#339](https://github.com/jmservera/ama/issues/339), [#351](https://github.com/jmservera/ama/issues/351) |
| Synthetic inventory/generator/dictionary/fixtures and provenance/refresh; consume screen requirements but do not supply screen designs | [#167](https://github.com/jmservera/ama/issues/167), [#172](https://github.com/jmservera/ama/issues/172), [#175](https://github.com/jmservera/ama/issues/175), [#176](https://github.com/jmservera/ama/issues/176) | [#166](https://github.com/jmservera/ama/issues/166), [#168](https://github.com/jmservera/ama/issues/168), [#169](https://github.com/jmservera/ama/issues/169), [#170](https://github.com/jmservera/ama/issues/170), [#171](https://github.com/jmservera/ama/issues/171), [#173](https://github.com/jmservera/ama/issues/173), [#174](https://github.com/jmservera/ama/issues/174) |
| Sensor backfill/stream models, identity/schema, validation and documentation; replay/run-control surface ambiguities #187/#189 are not hidden here | [#177](https://github.com/jmservera/ama/issues/177), [#178](https://github.com/jmservera/ama/issues/178), [#179](https://github.com/jmservera/ama/issues/179), [#180](https://github.com/jmservera/ama/issues/180), [#181](https://github.com/jmservera/ama/issues/181), [#183](https://github.com/jmservera/ama/issues/183), [#184](https://github.com/jmservera/ama/issues/184), [#185](https://github.com/jmservera/ama/issues/185), [#186](https://github.com/jmservera/ama/issues/186), [#188](https://github.com/jmservera/ama/issues/188), [#190](https://github.com/jmservera/ama/issues/190), [#191](https://github.com/jmservera/ama/issues/191), [#192](https://github.com/jmservera/ama/issues/192), [#193](https://github.com/jmservera/ama/issues/193), [#194](https://github.com/jmservera/ama/issues/194) | [#182](https://github.com/jmservera/ama/issues/182) |
| Source-layout ADR/parity matrix, migration/repointing, cut-over/retirement and link/KB cleanup; preserve existing UI, do not design new screens | [#198](https://github.com/jmservera/ama/issues/198), [#199](https://github.com/jmservera/ama/issues/199), [#200](https://github.com/jmservera/ama/issues/200), [#201](https://github.com/jmservera/ama/issues/201), [#202](https://github.com/jmservera/ama/issues/202), [#203](https://github.com/jmservera/ama/issues/203) | [#196](https://github.com/jmservera/ama/issues/196), [#197](https://github.com/jmservera/ama/issues/197) |
| Rule-engine regression tests and source-monitor retry scheduling; screen/review scope belongs to #212/#213 respectively | None | [#329](https://github.com/jmservera/ama/issues/329), [#332](https://github.com/jmservera/ama/issues/332) |

### Aggregate epic routing

These sixteen issues are **epic-covered**, all Open. Child ranges name existing
issue IDs, not evidence of delivery, deferral or accepted design. The preceding
tables classify every child individually, including no-screen and unknown
children; no epic is substituted for a screen-feature row.

| Epic | Classified feature routes |
| --- | --- |
| [#73](https://github.com/jmservera/ama/issues/73) Home case/workbench | #74-80; linked queue follow-up #327 |
| [#81](https://github.com/jmservera/ama/issues/81) Safety/consent/lifecycle | #82-88; related journey features #130-131 |
| [#89](https://github.com/jmservera/ama/issues/89) Capacity/orders/quality | #90-92; related capture/aftercare #132-133 |
| [#93](https://github.com/jmservera/ama/issues/93) Finance/forms | #94-99 |
| [#100](https://github.com/jmservera/ama/issues/100) Insight/export | #101-103 |
| [#104](https://github.com/jmservera/ama/issues/104) Bounded AI | #105-108 |
| [#109](https://github.com/jmservera/ama/issues/109) Monitoring | #110-112 |
| [#113](https://github.com/jmservera/ama/issues/113) Platform/privacy | #114-122 |
| [#123](https://github.com/jmservera/ama/issues/123) Discovery/release governance | #124-129; cross-cutting journey contracts #130-135 |
| [#136](https://github.com/jmservera/ama/issues/136) Bicep/deployment | #137-148; related deployment follow-ups #322/#339/#344/#349/#350/#351/#358/#360 |
| [#149](https://github.com/jmservera/ama/issues/149) UX/accessibility | #150-156; role screens #225-233 |
| [#157](https://github.com/jmservera/ama/issues/157) Chat/memory | #158-164 |
| [#165](https://github.com/jmservera/ama/issues/165) Synthetic programme | #166-194, including nested aggregate stories #177/#184/#190 classified by their own prescribed data scope |
| [#195](https://github.com/jmservera/ama/issues/195) Source consolidation | #196-203/#290; related owner check cleanup #323 |
| [#208](https://github.com/jmservera/ama/issues/208) Regulatory assistant | #209-217; regression/retry follow-ups #329/#332 |
| [#218](https://github.com/jmservera/ama/issues/218) RAI controls | #219-224 |

### Coverage disposition and remaining real gates

The four classifications reconcile to **184/184** issues; every one of the
**74 known screen issues has an individual trace or explicit evidence gap**.
The eight remaining ambiguities are precisely the surface decisions listed
above, not an unspecified unreviewed backlog. This dated inventory supersedes
only G01's "broader backlog coverage unknown" for this snapshot; the original
fifteen-row inspection record is retained as historical evidence.

Literal #156 AC1 is **not fully satisfied**: all 74 current screen-design
versions are NOT SUPPLIED, and individual rows explicitly identify absent or
partial detailed task flows and missing journey families (account
entry #116/#344/#349/#360, staff-time #120, staff privacy #163, and account/photo
within parity #350 are separately identified, not assumed complete).
Existing exact linked sections supply only their stated portions. The design
owner must attach actual reviewable versions; product/domain owners must supply
the named detailed flow gaps, and choose the eight unresolved delivery surfaces.
These are concrete artifact/owner decisions, not authorization for new UI here.

G02-G07 remain open and overall design acceptance remains **Blocked**: current
design/state versions, named human design review, required current manual
accessibility evidence, exact content/resident-wording review and direct user
research are not supplied by an issue inventory. Preserve the owner-selected
Fluent 2 foundation, existing WCAG/content scope and unresolved decisions.
Historical H, engineering E, source code, API contracts, architecture drawings,
closed issues and a completed documentation check cannot replace those gates.
No new UI validation, conformance, real benefit or whole-issue acceptance is
claimed. Manual/non-digital paths, resident consent/withdrawal, independent
safety intake, professional judgment and all human financial/legal/release
approval boundaries remain unchanged.

[bc-prd]: ../../../prds/zava-forward-retrofit-programme-demonstrator.md
[bc-connected]: ./customer-journeys/customer-journey-atlas.md#one-connected-service-journey
[bc-programme]: ./customer-journeys/programme.md#1-programme-manager--planner
[bc-assessor]: ./customer-journeys/programme.md#2-surveyor--retrofit-assessor
[bc-technical]: ./customer-journeys/programme.md#3-retrofit-designer--coordinator
[bc-quality]: ./customer-journeys/programme.md#4-independent-qa-inspector--retrofit-evaluator
[bc-asset]: ./customer-journeys/asset.md#journey-1-asset-executive-current-state-hypothesis
[bc-board]: ./customer-journeys/asset.md#journey-2-ceoboard-sponsor-and-assurance-reader
[bc-data]: ./customer-journeys/data.md#current-map-1-data-steward--performance-analyst
[bc-operator]: ./customer-journeys/data.md#current-map-2-digital--service-operator
[bc-control]: ./customer-journeys/data.md#current-map-3-dpo--legal--control-reviewer
[bc-safety]: ./customer-journeys/safety.md#current-state-map-b-repairshazard-triage-and-response-staff
[bc-household]: ./customer-journeys/residents.md#current-journey-a-rented-resident-household
[bc-shared-owner]: ./customer-journeys/residents.md#current-journey-b-shared-owner-or-leaseholder
[bc-representative]: ./customer-journeys/residents.md#current-journey-c-authorised-carer-advocate-or-interpreter
[bc-engagement]: ./customer-journeys/residents.md#current-journey-d-resident-engagementsupport-worker
[bc-redress]: ./customer-journeys/frontline.md#3-complaint--redress-handler-distinct-proxy
[bc-supplier]: ./customer-journeys/suppliers.md#1-procurementcontracts-manager-secure-accountable-delivery
[bc-scheduler]: ./customer-journeys/suppliers.md#2-contractor-schedulersupervisor-make-a-workable-day
[bc-installer]: ./customer-journeys/suppliers.md#3-installersubcontractor-field-worker-do-the-right-work-safely
[bc-finance]: ./customer-journeys/finance.md#a-capital-and-grant-preparer
[bc-finance-approver]: ./customer-journeys/finance.md#b-independent-capital-and-grant-approver
[bc-payment]: ./customer-journeys/finance.md#c-payment-officer
[bc-leasehold]: ./customer-journeys/customer-journey-atlas.md#leasehold-service-staff-current-state-map
[bc-nomination]: ./customer-journeys/customer-journey-atlas.md#nomination-prioritisation-and-challenge-subjourney
[bc-source-change]: ./customer-journeys/customer-journey-atlas.md#controlled-source-to-rule-change-subjourney
[bc-opportunities]: ./customer-journeys/customer-journey-atlas.md#divergent-opportunities-beyond-another-chatbot
[bc-reg-roles]: ./regulatory-literacy-for-journeys.md#needs-by-journey-role
[bc-reg-flow]: ./regulatory-literacy-for-journeys.md#integration-design-for-agents
[bc-doubt]: ./regulatory-literacy-for-journeys.md#when-in-doubt-expected-agent-behaviour
[bc-profile]: ../../../prds/zava-forward-retrofit-programme-demonstrator.md#profile-journey-contract-for-the-next-prototype
[bc-lifecycle]: ../../../prds/zava-forward-retrofit-programme-demonstrator.md#case-lifecycle-role-handoffs-and-return-path
[bc-forms]: ../../../prds/zava-forward-retrofit-programme-demonstrator.md#form-extraction-and-assisted-filling
[bc-assistants]: ../../../prds/zava-forward-retrofit-programme-demonstrator.md#five-reactive-and-proactive-assistants-2026-10-13
[bc-chat-map]: ../../../prds/zava-forward-retrofit-programme-demonstrator.md#journey-agent-and-ui-mapping
[bc-chat-requirements]: ../../../prds/zava-forward-retrofit-programme-demonstrator.md#product-requirements
[bc-eleven]: #all-eleven-profile-journeys
[bc-ia]: #shared-workbench-ia-engineering-slice-2026-10-15
[bc-ux]: #proposed-acceptance-checks-for-the-next-prototype
[bc-panel]: ../../../../src/api/README.md#conversation-panel-issue-159
[bc-staff]: ../../../../src/api/README.md#what-staff-see

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

## Consultation record engineering continuation (2026-10-17, #92)

The issue's old "not evidenced in mvp" note is stale: #90/#384 already migrated
the provider package, capacity, delegation and work-order paths to `src/core`.
The remaining gap is consultation recording and gating, not a missing module.
BRD RULE-023 and CON-004 require a named Legal record before let/renew;
PRD FR-007 and CON-002 preserve independent approvals and authoritative systems.
These are repository requirements, not a new statement of current legislation.
Local regulatory snapshots are unchanged and no legal-currentness check or
operational interpretation was performed.

The [core contract](../../../../src/core/README.md#consultation-records-and-confirmation-holds-92)
and [API](../../../../src/api/README.md#consultation-record-api-and-unknown-hold-92)
retain the four supplied statuses with named human decision-maker text,
original clean document/hash/version, reason, server recorder/time, exact
contract/scope and optimistic history version. Recording is not approval:
all entries are unverified and effective consultation remains unknown.
Current contract-manager delegations are not Legal authority; ADR 0005's
named exercise Legal capacity covers fictional rule cards/source proposals,
not contract consultation. No new role, mapping, grant or fabricated approval
was introduced.

The historical 2026-10-17 implementation below is superseded for hold scope only
by the 2026-10-18 owner direction in the next subsection; its original evidence
and independent verdict are not amended.

Unknown held actual issue, reissue, correction/reopening, positive booking
and final-order case advancement. Drafts, capacity, negative appointments,
withdrawal and factual historical completion retain existing checks. Unmocked
fictional tests reach downstream seams using explicit historical orders, not
simulated consultation approval. Legacy #90/building/hazard/resident/role-matrix
regressions isolate only the new hold to keep their independent controls tested;
those successful paths are not currently available application clearance.
Existing generated fixtures/hash manifests are unchanged.

Both exact issue criteria remain partial: no verified Legal recorder is
available and no dedicated contract/framework/call-off let/renew path exists.
Actual order holds do not prove a nonexistent letting/renewal workflow.
The next authority contract needs named human approval and scoped integration,
not a role-agent endorsement or automatic interpretation of applicability.

Coordinator-authorized PR #389 integration onto main 1a05dfb8, including
merged hazard #388, had only an append-only-log manual conflict. Own src
added/removed bytes and original independent Review are retained; upstream
hazard/shared SQL recovery is byte-unchanged. Fresh combined JSON/SQLite/API/
manifest validation ran 348 executions (300 passes, 48 explicit skips);
configured core/API lint/format/types passed. Earlier 70 actual MSSQL passes
remain historical, not a new integration run. Coordinator final-head review
is still pending.

The missing genuine contract let/renew seam is unfinished workflow engineering,
distinct from the missing actual authorized human Legal decision. The supplied
decision-recording seam is already implemented fail-closed; missing approval
does not prohibit that mechanic. A bounded coordinator follow-up can separately
plan the package-linked authoritative let/renew transition and exact consultation
guard, with fictional unknown/stale/unauthorized tests and no live contracts,
financial purchase API or portal. It is not current plan completion or acceptance.

## Scoped consultation hold owner direction (2026-10-18, #92)

The owner directed: "Limit the hold to consultation-dependent actions; preserve
unrelated service work". This approves scope behavior, not Legal clearance,
contractual power, spend or deployment. A separate new full RPI task preserves
all prior consultation-record-controls-92 evidence and original verdicts.

Source trace found no genuine contract/framework/call-off let/renew transition
or authoritative consultation-applicability relation. Existing contract-action
delegations and capacity case/provider/source bindings are not Legal authority.
No client boolean, naming inference, fixture hash or supplied source status
can establish applicability or clearance. All supplied decisions remain
unverified, with effective status unknown and source/recorder/version intact.

Five indiscriminate consultation checks were removed from ordinary service order
issue, reissue, correction, positive booking and final advance. Existing
source-backed building dependencies/holds keep their exact case/package scope
and unknown-applicability refusals. Package-aware instructions can exclude
another package's hold, but final case advancement retains the existing case-wide
building gate. Different-case eligibility remains independent. These generic
scoped holds are not a verified Legal consultation workflow.

Main's appointment resident/staff/capacity commitment, hazard/resident/stock/
funding/technical/provider permissions and SQL optimistic/atomic writer controls
are retained. Direct consultation refusal remains unconditional. No web, role,
SQL-store, queue or export implementation changed; no approval was manufactured
to obtain service success, and affected regression bypass mocks were removed.

Both exact issue criteria remain partial. Actual Legal authority, genuine
let/renew enforcement, human/live acceptance and coordinator final-head
independent review remain unmet. No issue, board, merge or deployment action
is authorized by these engineering results.
