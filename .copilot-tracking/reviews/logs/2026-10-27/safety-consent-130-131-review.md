---
title: Safety-consent 130-131 independent RPI Review
description: Single post-implementation assessment of bounded intake and unresolved-tenure holds
ms.date: 2026-10-27
---

## Scope and Evidence

* Task ID: 130-131; task slug: safety-consent-130-131.
* Review date: 2026-10-27.
* Review scope: P01 bounded implementation and P02 validation/documentation readiness, with whole-issue remaining work assessed separately.
* Plan: .copilot-tracking/plans/2026-10-27/safety-consent-130-131-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/safety-consent-130-131-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-27/safety-consent-130-131-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-27/safety-consent-130-131-changes.md
* Research: .copilot-tracking/research/2026-10-27/safety-consent-130-131-research.md
* Source boundary: current seven-file tracked diff, on docs/safety-consent-130; existing uncommitted parent work is evidence only.

## Opening Review State

* Interpreted review goal: independently assess source contracts, privacy, holds, retention, authority preservation and truthful evidence once; distinguish bounded engineering from whole-issue acceptance.
* Review scope: three core modules, existing core/API resident tests and two component READMEs; supplied RPI artifacts and local validation logs.
* Evidence readiness: supplied artifacts are present. P01 is marked complete; P02 publication deliberately remains pending. Research's opening In progress label is historical; its closing Planning Readiness records research execution and unresolved human gates.
* Acceptance basis: bounded plan criteria, current phase details, four dispositioned critique findings, caller restrictions and explicit whole-issue exclusions.
* First comparison boundary: inspect the complete tracked diff and the existing contracts needed to evaluate new intake, projection and persistent holds; no operational eligibility or Legal policy invented.
* Active read-only boundaries: only this canonical review record may be written. No source/artifact corrections, delegation, repeated Review, full/heavy gates, cloud, secrets, private data or uv.
* Initial blockers: no SQL Server/browser/human acceptance evidence; actual owner/Legal/DPO/Compliance decisions remain unavailable. These limit acceptance and publication claims, not the ability to review bounded source.

## Execution Status

* Execution status: Complete.
* Review execution evidence: exactly one independent assessment of the current seven-file tracked diff, supplied artifacts, relevant existing transaction/projection/API contracts and three supplied test logs. No delegated or repeated Review. No source modification or test rerun.
* Implementation execution is distinct: P01 is complete within the bounded contract; P02 validation/documentation is complete, publication is pending. This does not mean either whole issue is complete.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Nomination/correction | Reconciled | Exact original evidence, append-only subject/account corrections, named follow-up, manual channels and explicit unknowns match the plan. No operational eligibility or representative validation is implemented. |
| P01-T02 | Unverified tenure/hold | Reconciled | All registered unresolved reports hold the containing case, independent of household certainty or measure acceptance; no release action exists. |
| P02-T01 | Validation Record and Pre-Review Reconciliation | Partially complete as planned | Local validation/docs are evidenced; this Review supplies the pending independent assessment. Commit, draft PR and criterion matrix do not yet exist as publication evidence. The unchecked phase/task is accurate. |
| Follow-Up Items | Blockers and pre-review handoff | Reconciled | Actual appointments, OD-41/42, real participant evidence, verified tenure, Legal/Finance positions and privacy/retention decisions remain outside active implementation acceptance. |
| Research readiness | Planning Readiness | Reconciled with minor historical-label debt | The opening research table still says In progress, but the explicit closing disposition is executed and the accepted scope is unambiguous. This does not prevent a credible verdict or warrant editing research during Review. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/resident_decisions.py | Three closed intake actions reuse the resident ledger; nomination and correction retain exact accounts and unverified subject provenance. | _intake_fields, _intake_text, _res_nomination_record, _res_nomination_correct and existing _operation inspected. | Shared JSON/SQLite histories, rollback, schema, stale version, authority and manual-channel assertions; API integration. | Bounded contract sound; no material defect identified. Optional challenge snapshot preserves the existing challenge, not a nomination-specific disposition or dependent-proposal release. |
| P01-T02 | src/core/src/zava_forward/core/resident_decisions.py | Append-only case-versioned tenure reports with Unknown verification, Legal/cost positions and static questions; persistent conservative hold. | resident_gate checks the boolean or reports before measure bindings; scope_record refuses new scope; separate marker is outside RESIDENT_FIELDS. | Multiple ambiguous/unknown household reports, otherwise accepted measures, scope refusal, SQL reopen, legal-hold deletion denial and post-deletion hold assertions. | Bounded hold and lifecycle separation sound. Existing independent hazard route remains callable; no programme-wide household coverage established. |
| P01 privacy | src/core/src/zava_forward/core/projection.py; src/core/src/zava_forward/core/store.py | Hide both intake histories from readers lacking current dual evidence rights, including cached identities. | Store.detail checks challenge_references_visible against current registry before projection; redact_staff_detail removes histories after resident-data restoration. Contractor output and CSV use closed field sets. Existing assistants.capture uses explicit allow-lists. | Denied detail/write/API reads and account/source/lease canaries; every existing assistant capture exercised. | Raw intake is not exposed through the inspected read paths. Internal detail(user=None) intentionally remains privileged, not a public authorization bypass. |
| P01 transaction | src/core/src/zava_forward/core/resident_decisions.py; src/core/tests/test_resident_decisions.py | Reuse actor/owner checks, rowversion and detached replay; handlers mutate only supplied case and return identifier-only audit text. | Existing _operation, validate_sql, _person and API committed-outcome handling inspected. | SQLite writer-time actor/owner changes, competing tenure revision, rollback and committed acknowledgement failure tests. | One durable success and truthful postcommit outcome are asserted. Real SQL Server execution is not established by SQLite tests. |
| P02-T01 | src/core/tests/test_resident_decisions.py; src/api/tests/test_resident_api.py | Twelve new methods: six shared, three SQL-writer, three API. No removed methods or new runner. | Complete test diff inspected; new helpers reuse current fixtures. | Supplied log summaries verified; focused results and tooling passes recorded by implementer/caller. | Test ownership/budget preserved; skips remain explicit limitations. |
| P02-T01 | src/core/README.md; src/api/README.md | Describe exact required schemas, staff-only capture, permanent hold, deletion interaction, explicit refusals and actual human blockers. | Both documentation diffs inspected against handlers and existing endpoint. | Markdown/relative-link and payload comparison; diff whitespace check rerun and passed. | Accurate bounded claims. Acknowledgement is not delivery; static questions are not a reviewed-record pack; hazard refusal is not automatic dispatch. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T02 | Unknown or ambiguous household reports use a case-wide hold. | PC-001; approved independent work must not infer verified narrower scope. | Plan functional requirements, details, bounded criteria, source and changes agree. | Direct planner correction; original Complete / Revise preserved. | Compatible safety refinement, not a new operational decision. |
| P01-T01 | Correctable reported subject references retain original associations. | PC-002; correctable identity cannot imply verified resident/representative authority. | Plan, details, correction schema and history tests reconciled. | Direct planner correction, no human policy invented. | Confirmed intent preserved; cross-case transfer fails without mutation. |
| P02-T01 | Fixed test allocation explicitly covers replay, current registry, projection and canaries. | PC-003; existing SQL replay and resident-data restoration are integration-sensitive. | Twelve-method budget matches source diff and validation summary. | Direct planner correction within accepted scope. | SQLite evidence adequate for its stated boundary; no SQL Server claim. |
| P01-T02 lifecycle | Deletable evidence separated from durable unresolved marker. | PC-004; neither fresh retention authority nor release through deletion is allowed. | RESIDENT_FIELDS, boolean marker, deletion tests, READMEs and blockers agree. | Direct planner correction; actual retention applicability remains human-owned. | No material scope divergence or unsupported operational approval. |

## Critique and Material Revision Assessment

* Exactly one final critique is present: execution Complete, original verdict Revise, three High and one Medium finding. This Review neither replaces nor upgrades it.
* PC-001: disposition substantiated by early case-wide gate predicate and scope refusal, including unknown/ambiguous reports and existing accepted measures.
* PC-002: disposition substantiated by preserved original subject/account and append-only correction provenance, explicit Unknown identity, closed case binding and unchanged authority/consent/ranking assertions.
* PC-003: disposition substantiated by transactional dispatch, detached SQL replay, current actor/owner validation, rollback/CAS/postcommit tests, current-registry denial and projection/export/prompt canaries. SQL means SQLite execution here; opt-in SQL Server remains skipped.
* PC-004: disposition substantiated by deletable intake fields, surviving non-sensitive hold and legal-hold/deletion test. No actual retention approval inferred.
* The supplied artifact set records these compatible planner corrections before completed implementation. There is no evidence of an unaccepted significant operational decision, expanded authority or dependent-work resumption across a required human stop. No fresh critique or second Review is required or performed.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| OD-41/42 and operational nomination/representative authority | Engineering fixtures cannot supply actual validation policy, delegated authority or participant comprehension. | Owner, Resident Engagement and DPO, with Legal as applicable. | Open; RV-001, distinct human-owned follow-up. |
| Verified household/lease identity and responsibility/cost/release | No appointed Legal/Home Ownership reviewer or approved positions exist; static questions cannot substitute. | Legal, Home Ownership, Finance and owner; DPO/Compliance for real-data applicability. | Open; RV-002, distinct human-owned follow-up. |

Unresolved follow-ups remain outside active P01 completion and acceptance. Pending P02 publication is existing active work, not an invented operational extension.

## Whole-Issue Acceptance Boundary

Issue bodies were retrieved read-only with gh issue view 130/131 during this Review. Existing generic challenge functionality is inherited, not newly delivered nomination-specific acceptance.

| Criterion group | Assessment at this boundary |
| --- | --- |
| #130 original account/source/channel | Constructed staff capture is implemented, exact original retained and tested. Not a real staffed resident service acceptance. |
| #130 acknowledgement and named owner | Named registered owner and staff-recorded acknowledgement reference implemented. Actual delivery/acknowledged service and appointment not proven. |
| #130 resident/representative challenge, reviewer and outcome | Staff correction and optional same-case generic challenge snapshot implemented. Actual resident/representative validation, nomination-specific reviewer/outcome and eligibility decisions remain excluded. |
| #130 exact dependent re-review and RAI versioned explanation | Nomination review becomes stale without changing unrelated state. Generic source/policy/proposal/human-decision challenge remains separate. No end-to-end nomination-to-priority dependency/decision acceptance or new plain-language explanation is established. |
| #130 immediate hazard route | Marked nomination input is rejected with the independent hazard endpoint; existing hazard route tested independently. Automatic immediate referral is not implemented or claimed. |
| #130 unknown flags, no priority detriment and authority safeguards | Intake flags remain Unknown; tested unrelated ranking, consent, representative authority and hazard state are unchanged. This is not cohort fairness/coverage validation. |
| #130 manual/digital, keyboard and permissions | Five staff-recorded channels and permissions tested. No new UI, keyboard/screen-reader exercise or authorized representative participation/comprehension evidence. |
| #130 no automatic effects, open remedies and no inferred consent | No new sending, booking, approval, authority or challenge-resolution action. Existing remedy/challenge behavior is not replaced; tests do not constitute human acceptance. |
| #131 all homes/households and verified pre-offer route | Reports cover supplied references only; unknown/ambiguous registered cases hold conservatively. Full enumeration, verified routes and an all-offer programme gate are not established. |
| #131 attached Legal position and reviewed-record question pack | Not implemented pending actual appointment/approved evidence. Seven static questions only; Legal interpretation and Finance cost authority remain external. |
| #131 changed scope/disputes/defects/charges | Registered case hold has no release action, persists despite other household acceptance/deletion and refuses new scope. Not a new complete household dispute/package-management workflow. |
| #131 ambiguous identity/data-owner route | Ambiguity is retained, no reuse/release permitted; named follow-up staff and required data-owner/Legal next action shown. Actual data-owner appointment and verification are not proven. |
| #131 lease-detail projection | Constructed raw-read denial tested against current dual entitlement. No real-data privacy/legal acceptance inferred. |

Use Refs #130 and Refs #131. No whole-issue checkbox should be ticked solely from these bounded tests.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Whole-issue nomination service and human acceptance remain open

* Finding class: accepted residual work, not a bounded source defect.
* Related scope: P01-T01 and the first plan Follow-Up Item; #130/FR-037/OD-41/42.
* Evidence: .copilot-tracking/plans/2026-10-27/safety-consent-130-131-plan.md, Scope and Non-Goals / Follow-Up Items; src/core/src/zava_forward/core/resident_decisions.py, _res_nomination_record and _res_nomination_correct; src/core/README.md and src/api/README.md.
* Impact: Staff intake cannot establish actual nomination eligibility, valid representative decisions, acknowledged delivery, human reviewer/outcome, exact nomination-dependent prioritisation re-review, immediate hazard dispatch or representative comprehension. Calling #130 complete would overstate resident service and authority.
* Destination: distinct follow-up owned by owner/Resident Engagement/DPO, with specialist Legal/Compliance input as applicable; do not add it to completed P01.
* Smallest useful next action: obtain the actual OD-41/42 and operational authority/participation decisions, then scope separately approved operational work. Keep the draft PR partial with these criteria unproven.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Verified tenure and reviewed responsibility evidence remain human-gated

* Finding class: accepted residual work, not a defect in the conservative hold.
* Related scope: P01-T02 and the second plan Follow-Up Item; #131/FR-015/AC-021.
* Evidence: src/core/src/zava_forward/core/resident_decisions.py, _res_tenure_intake and resident_gate; .copilot-tracking/details/2026-10-27/safety-consent-130-131-phase-details.md, P01-T02; src/core/README.md.
* Impact: Registered Unknown/Ambiguous evidence remains safely held, but supplied reports do not prove complete household coverage, verified pre-offer routes, an actual Legal appointee, reviewed lease responsibility, approved cost/consultation or a pack grounded in reviewed records. Evidence deletion must never be treated as approval.
* Destination: distinct follow-up owned by Legal/Home Ownership/Finance and owner; DPO/Compliance must establish real-data processing/retention applicability and any future release policy.
* Smallest useful next action: record actual appointment and approved verification/responsibility/cost/privacy decisions before separately authorizing operational intake or release. Preserve the existing case-wide hold in the meantime.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Publication remains unexecuted and must not imply unrun acceptance

* Finding class: remaining P02 work and explicit publication limitation, not an implementation defect.
* Related scope: P02/P02-T01 and the pending draft-PR acceptance criterion.
* Evidence: current worktree is uncommitted; plan and changes deliberately retain pending publication. No PR URL, clean committed exact-head assessment or verified local-gate receipt is supplied. src/README.md, Local RPI gate, describes a dated small-issue focused-test policy, while the supplied standing repository instructions require the complete gate before final-candidate publication; the caller explicitly prohibits --all and does not authorize heavy --changed for this slice.
* Impact: This source Review and focused passing logs do not themselves authorize push, satisfy hosted checks or resolve the publication-policy discrepancy. Neither full-gate readiness nor real SQL Server/browser/human acceptance may be claimed.
* Destination: existing P02-T01 publication owner/active parent, not another Review or automatic source change.
* Smallest useful next action: preserve this outcome, retain the original dated artifacts, prepare a criterion-by-criterion Refs-only draft handoff, and reconcile the applicable publication requirement with the owner before any prohibited gate or publication under an unsatisfied required gate. Do not waive protections or fabricate a receipt.

## Defects

* No material bounded implementation defect identified in the inspected diff and dependent contracts. No rpi-implement finding is raised.
* This is not a vulnerability assessment, legal opinion or accessibility conformance claim.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | Distinct human-owned nomination follow-up | Owner/Resident Engagement/DPO; actual policy and participation decisions | Explicitly excluded operational acceptance, not faulty intake. |
| RV-002 | Distinct human-owned tenure/privacy follow-up | Legal/Home Ownership/Finance/DPO/Compliance; appointment and approved evidence | Engineering cannot manufacture verified positions or release authority. |
| RV-003 | Existing P02-T01 continuation | Active parent/publication owner; reconcile gate applicability and retain partial draft matrix | Publication proof and policy constraints remain unresolved. |

Later implementation of findings does not require another Review. No rpi-plan or rpi-research command is imposed on the accepted bounded scope: the missing actual human decisions are known, not a request for agents to invent evidence.

## Residual Work

* RV-001 and RV-002 preserve both existing plan follow-ups distinctly.
* Real SQL Server behavior, real participant accessibility/comprehension, actual service delivery and operational release remain unproven. Future owners must select and execute required acceptance evidence before making those claims.
* RV-003 remains publication work under the active parent. No source fix or second Review is authorized by this record.

## Blockers and Remaining Work

* Review blocker: none; credible bounded evidence was sufficient for this single completed assessment.
* Whole-issue/live blockers: actual OD-41/42, Legal/Home Ownership appointment, verified household/representative authority, reviewed responsibility/cost, real participant evidence and approved privacy/retention/release decisions.
* Publication blocker: this Review cannot certify compliance with the complete-gate instruction while --all is prohibited and no receipt exists. The dated small-issue policy in src/README.md must be reconciled by the publication owner; do not execute an unapproved gate or imply policy compliance from this Review.
* Remaining active work: P02-T01 commit/publication evidence and one combined draft PR with explicit partial/blocked criterion matrix, subject to publication safeguards. Human operational gates do not by themselves prohibit a properly qualified source-only draft; the separate publication-policy constraint still applies.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| PYTHONPATH=tests python3 -m unittest test_resident_decisions test_hazard_referral test_consultation_controls test_quality_procurement -q (src/core) | Combined resident/hazard/consultation/procurement | Passed, supplied log inspected | 373 tests, 95.288s, OK, 87 skipped. Injected fault traces are expected test evidence, not an observed suite failure. |
| PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q (src/api) | Full API discovery | Passed, supplied log inspected | 1124 tests, 625.226s, OK, 314 skipped. Summary located in api-discovery.log despite later diagnostic output. |
| Resident API discovery for test_resident_api.py | Focused resident HTTP boundary | Passed, supplied log inspected | 16 tests, 17.465s, OK, 1 skipped. Missing law-store checks explicitly remain Unknown. |
| Changed intake selectors | Focused new core behavior | Passed, caller/changes evidence | 24 tests, OK, 9 opt-in SQL Server skips; 15 executed JSON/SQLite checks. Exact selector argv not independently supplied or rerun. |
| Focused Ruff, test formatter and mypy | Changed targets | Passed, caller/changes evidence | Implementer reports clean results after typed-compatible callback corrections; tool receipts were not independently reproduced during Review. |
| git diff --check | Current tracked diff | Passed, independently executed | No whitespace errors. |
| Source/schema/docs comparison | Complete seven-file diff and relevant existing contracts | Complete, independently executed | Compared all changed production code, tests and README additions once; no source changes. |
| SQL Server integration | Real SQL Server | Skipped | Opt-in environment not run. SQLite SQL-writer tests do not establish SQL Server acceptance. |
| Browser, accessibility and real participant acceptance | UI and actual users | Not run | No web change; no real participation or accessibility acceptance available or claimed. |
| --all / heavy --changed / hosted checks | Publication/release | Not run | Caller prohibits full gate and limits heavy changed gate to large changes; this is a bounded slice. No cloud substitute, receipt fabrication or skip-as-pass claim. Hosted checks remain future evidence. |

Logs read: external session files core-boundary-tests.log, api-discovery.log and resident-api-tests.log supplied by the caller. Their final summaries corroborate counts, not clean exact-head receipt identity; no new tests or output files were created.

## Outcome

* Outcome: Residual work.
* Outcome rationale: bounded implementation matches the reconciled accepted direction and all four critique corrections are substantiated. No material source defect was identified. Actual whole-issue human evidence and operational work remain open by design; pending publication and its policy constraint remain separate. This is not Conformant whole-issue acceptance, release approval or issue closure.
* Original outcome preservation: this single Complete / Residual work Review is the original assessment. The critique remains Complete / Revise. Later implementation, publication or approvals must not rewrite either original outcome.
* Severity summary: 0 Critical, 0 High, 2 Medium residual human follow-ups, 1 Low publication/remaining-work finding.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement handoff needed at this boundary. |
| Decision gap or invalid assumption in bounded design | None | No new operational decision inferred or active scope revision needed. |
| Material evidence gap preventing bounded Review | None | Logs/source sufficient for stated engineering boundary; unrun acceptance remains disclosed. |
| Non-blocking whole-issue residual work | Distinct follow-ups RV-001 and RV-002 | Named human owners supply actual decisions/evidence before operational extension. |
| Pending publication and safeguards | Existing P02-T01 / RV-003 | Active parent resolves applicable publication policy, then proceeds only within authorization. |

* Execution status: Complete.
* Outcome: Residual work.
* Validation coverage: independently inspected source and supplied core/API summaries; focused tooling evidence attributed; SQL Server/browser/human/complete-gate acceptance not claimed.
* Blockers: no bounded source blocker found; human operational gates and publication-policy reconciliation remain.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/safety-consent-130-131-research.md](.copilot-tracking/research/2026-10-27/safety-consent-130-131-research.md) | Supplied evidence and human decision boundary |
| [.copilot-tracking/plans/2026-10-27/safety-consent-130-131-plan.md](.copilot-tracking/plans/2026-10-27/safety-consent-130-131-plan.md) | Reconciled bounded plan and pending publication |
| [.copilot-tracking/details/2026-10-27/safety-consent-130-131-phase-details.md](.copilot-tracking/details/2026-10-27/safety-consent-130-131-phase-details.md) | Phase contracts and test ownership |
| [.copilot-tracking/reviews/plans/2026-10-27/safety-consent-130-131-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/safety-consent-130-131-plan-critique.md) | Preserved original Complete / Revise critique |
| [.copilot-tracking/changes/2026-10-27/safety-consent-130-131-changes.md](.copilot-tracking/changes/2026-10-27/safety-consent-130-131-changes.md) | Implementation and validation evidence |
| [src/core/src/zava_forward/core/resident_decisions.py](src/core/src/zava_forward/core/resident_decisions.py) | Intake, transactional dispatch, holds and deletion |
| [src/core/src/zava_forward/core/projection.py](src/core/src/zava_forward/core/projection.py) | Dual-entitlement redaction |
| [src/core/src/zava_forward/core/store.py](src/core/src/zava_forward/core/store.py) | Current-reader denial and shared read/gate paths |
| [src/core/tests/test_resident_decisions.py](src/core/tests/test_resident_decisions.py) | Constructed histories, holds, privacy and writer races |
| [src/api/tests/test_resident_api.py](src/api/tests/test_resident_api.py) | HTTP intake and projection assertions |
| [src/core/README.md](src/core/README.md) | Engineering and operational boundaries |
| [src/api/README.md](src/api/README.md) | Closed request contract and limitations |
| [src/README.md](src/README.md) | Dated local-gate tier policy relevant to publication |
| [.copilot-tracking/reviews/logs/2026-10-27/safety-consent-130-131-review.md](.copilot-tracking/reviews/logs/2026-10-27/safety-consent-130-131-review.md) | This single independent Review |

## Next Steps

The active parent retains this Complete / Residual work result and original critique, resolves the publication-policy constraint before push, and completes existing P02-T01 only within authorization with one Refs #130 / Refs #131 draft and explicit unproven-criteria matrix. Actual human follow-ups remain separate and stopped. No further source edit, delegated assessment, gate or second Review is performed here.
