---
title: Screen to journey, task flow and design artefact traceability
description: Per-screen matrix linking every registered role screen and the chat and alert surfaces (#225 to #233, #159, #215) to a journey, a task flow, a design artefact, a test and the remaining design gap (issue #156)
ms.date: 2026-11-14
ms.topic: reference
---

## Scope and evidence label

Delivery slice for [#156](https://github.com/jmservera/ama/issues/156) under
[#149](https://github.com/jmservera/ama/issues/149), criterion 1: each backlog
feature with a screen links to its journey, task flow and design artefact. This
page covers the screen features [#225](https://github.com/jmservera/ama/issues/225)
to [#233](https://github.com/jmservera/ama/issues/233),
[#159](https://github.com/jmservera/ama/issues/159) and
[#215](https://github.com/jmservera/ama/issues/215). The 2026-10-18 snapshot of
all 184 issues stays in the
[prototype profile review](./zava-forward-prototype-profile-review.md#screen-backlog-coverage-snapshot-2026-10-18-156),
and the journey-level matrix stays in the
[design system](./design-system.md#journey-to-requirement-to-design-to-test-traceability).

The links record where evidence exists. They do not show that a design was
reviewed or accepted. All journeys are desk-based hypotheses until validated in
[#155](https://github.com/jmservera/ama/issues/155). No screen has a named
human design, content, accessibility or user-test acceptance, so this matrix
ticks no acceptance criterion and the design review gate stays Blocked.

Terms used in the columns:

* Journey: the role journey section the screen serves.
* Task flow: the written step sequence the screen supports. Where none is
  written, the cell says `No written task flow` and names the closest evidence.
* Design artefact: a wireframe, design contract or delivery record. Where only
  code and a delivery record exist, the cell says `No wireframe` so the gap is
  visible.
* Test: one automated source-level check. It is not conformance evidence.

## Screen matrix

| Issue | Screen or surface | Journey | Task flow | Design artefact | Test | Gap to close |
| --- | --- | --- | --- | --- | --- | --- |
| [#225](https://github.com/jmservera/ama/issues/225) | `finance-invoices` | [Finance and grants](./customer-journeys/finance.md#a-capital-and-grant-preparer) | [Independent approver and payment officer steps](./customer-journeys/finance.md#b-independent-capital-and-grant-approver) | [Finance screens delivery status](./customer-journeys/finance.md#finance-screens-delivery-status-2026-11-04-225); No wireframe | `src/api/tests/test_finance_grants_screens.py::FinanceGrantsScreens::test_roles_exclude_other_staff_and_no_controls` | Wireframe, named finance review |
| [#225](https://github.com/jmservera/ama/issues/225) | `finance-funding` | [Finance and grants](./customer-journeys/finance.md#a-capital-and-grant-preparer) | [Grant lifecycle acceptance audit](./customer-journeys/finance.md#grant-lifecycle-acceptance-audit-2026-10-17-95); No written screen task flow | [Finance screens delivery status](./customer-journeys/finance.md#finance-screens-delivery-status-2026-11-04-225); No wireframe | `src/api/tests/test_finance_grants_screens.py::FinanceGrantsScreens::test_roles_exclude_other_staff_and_no_controls` | Task flow, wireframe, named finance review |
| [#226](https://github.com/jmservera/ama/issues/226) | `asset-board` | [Asset and investment](./customer-journeys/asset.md#journey-1-asset-executive-current-state-hypothesis) | [CEO and board assurance reader](./customer-journeys/asset.md#journey-2-ceoboard-sponsor-and-assurance-reader); No written screen task flow | [Asset and board delivery status](./customer-journeys/asset.md#asset-and-board-screen-delivery-status-2026-11-04-226); No wireframe | `src/api/tests/test_asset_board_screen.py::AssetBoardScreen::test_unknowns_owner_age_and_no_controls` | Task flow, wireframe, asset staff review |
| [#227](https://github.com/jmservera/ama/issues/227) | `safety-lead` | [Safety lead map](./customer-journeys/safety.md#current-state-map-a-building-safetycompliance-lead) | No written screen task flow; same map | [Safety screens delivery status](./customer-journeys/safety.md#safety-screens-delivery-status-2026-11-04-227); No wireframe | `src/api/tests/test_safety_screens.py::SafetyScreens::test_roles_are_scoped` | Task flow, wireframe, safety review |
| [#227](https://github.com/jmservera/ama/issues/227) | `hazard-triage` | [Repairs and hazard triage map](./customer-journeys/safety.md#current-state-map-b-repairshazard-triage-and-response-staff) | No written screen task flow; same map | [Safety screens delivery status](./customer-journeys/safety.md#safety-screens-delivery-status-2026-11-04-227); No wireframe | `src/api/tests/test_safety_screens.py::SafetyScreens::test_roles_are_scoped` | Task flow, wireframe, safety review |
| [#228](https://github.com/jmservera/ama/issues/228) | `procurement-packages` | [Procurement and contracts manager](./customer-journeys/suppliers.md#1-procurementcontracts-manager-secure-accountable-delivery) | [Contractor submission, correction and acknowledgement](./customer-journeys/suppliers.md#design-contract-for-contractor-submission-correction-and-acknowledgement-proposed-2026-11-03) | [Delivery status record](./customer-journeys/suppliers.md#delivery-status-record-for-issue-228-2026-11-04); Proposed design contract | `src/api/tests/test_procurement_screens.py::PackageQueue::test_submission_is_separate_from_review_and_empty_is_unknown` | Named procurement review of the contract |
| [#228](https://github.com/jmservera/ama/issues/228) | `contractor-job-pack` | [Contractor scheduler and supervisor](./customer-journeys/suppliers.md#2-contractor-schedulersupervisor-make-a-workable-day) | [Contractor submission, correction and acknowledgement](./customer-journeys/suppliers.md#design-contract-for-contractor-submission-correction-and-acknowledgement-proposed-2026-11-03) | [Delivery status record](./customer-journeys/suppliers.md#delivery-status-record-for-issue-228-2026-11-04); Proposed design contract | `src/api/tests/test_procurement_screens.py::PackageQueue::test_submission_is_separate_from_review_and_empty_is_unknown` | Contractor contact review, no provider portal decision |
| [#229](https://github.com/jmservera/ama/issues/229) | `data-operator` | [Digital and service operator](./customer-journeys/data.md#current-map-2-digital--service-operator) | [Data steward map](./customer-journeys/data.md#current-map-1-data-steward--performance-analyst); No written screen task flow | [Data screens delivery status](./customer-journeys/data.md#data-screens-delivery-status-2026-11-04-229); No wireframe | `src/api/tests/test_data_operator_screen.py::DataOperatorScreen::test_both_values_provenance_and_preserved_eligibility` | Task flow, wireframe, operator review |
| [#230](https://github.com/jmservera/ama/issues/230) | `programme-queue` | [Programme manager and planner](./customer-journeys/programme.md#1-programme-manager--planner) | [Case queue task flow](./customer-journeys/programme.md#task-flow) | [Case queue and paging v1 state and recovery design](./customer-journeys/programme.md#programme-case-queue-and-paging-proposed-v1-state-and-recovery-design-2026-11-10-refs-156-230-149); Proposed wireframe | `src/api/tests/test_programme_screen.py::ProgrammeScreen::test_queue_shows_return_sender_owner_receiver_and_separate_responsibilities` | Named review of the proposed design |
| [#231](https://github.com/jmservera/ama/issues/231) | `technical-queue` | [Surveyor and retrofit assessor](./customer-journeys/programme.md#2-surveyor--retrofit-assessor) | [Retrofit designer and coordinator](./customer-journeys/programme.md#3-retrofit-designer--coordinator); No written screen task flow | [Technical and quality screens delivery status](./customer-journeys/programme.md#technical-and-quality-screens-delivery-status-2026-11-04-231); No wireframe | `src/api/tests/test_technical_quality_screens.py::TechnicalQueue::test_incomplete_signoff_record_cannot_show_readiness` | Task flow, wireframe, reviewer review |
| [#231](https://github.com/jmservera/ama/issues/231) | `quality-queue` | [Independent QA inspector](./customer-journeys/programme.md#4-independent-qa-inspector--retrofit-evaluator) | [Quality control continuation](./customer-journeys/programme.md#quality-control-engineering-continuation-2026-10-17-91); No written screen task flow | [Technical and quality screens delivery status](./customer-journeys/programme.md#technical-and-quality-screens-delivery-status-2026-11-04-231); No wireframe | `src/api/tests/test_technical_quality_screens.py::TechnicalQueue::test_incomplete_signoff_record_cannot_show_readiness` | Task flow, wireframe, inspector review |
| [#232](https://github.com/jmservera/ama/issues/232) | `resident-choice` | [Rented resident household](./customer-journeys/residents.md#current-journey-a-rented-resident-household) | [J1 Choose each proposed measure](./customer-journeys/residents.md#j1-choose-each-proposed-measure) and [J2 Pause or withdraw](./customer-journeys/residents.md#j2-pause-withdraw-or-ask-for-more-time) | [Resident demo redesign 2026-11-04](./resident-demo-redesign-2026-11-04.md); Written task designs | `src/api/tests/test_resident_choice_screen.py::ResidentChoiceScreen::test_choice_pause_commitment_and_access_are_distinct` | Named resident-engagement review, resident wording test |
| [#232](https://github.com/jmservera/ama/issues/232) | `resident-service-issues` | [Resident engagement and support worker](./customer-journeys/residents.md#current-journey-d-resident-engagementsupport-worker) | [J6 Challenge, complain and follow a remedy](./customer-journeys/residents.md#j6-challenge-complain-and-follow-a-remedy) | [Resident demo redesign 2026-11-04](./resident-demo-redesign-2026-11-04.md); Written task designs | `src/api/tests/test_resident_service_screen.py::ResidentServiceScreen::test_issue_owners_needs_and_commitment_are_visible` | Named resident-engagement review, resident wording test |
| [#233](https://github.com/jmservera/ama/issues/233) | All twelve role screens (eight-stage same-home map) | [Customer journey atlas](./customer-journeys/customer-journey-atlas.md#one-connected-service-journey) | [Atlas walkthrough stages](./atlas-screen-trace.md#perspectives-to-screens) | [Atlas findings and role journeys traced to screens](./atlas-screen-trace.md#atlas-design-themes-to-screens) | `src/api/tests/test_role_screens_stage_map_focus.py` | Validation in #155 |
| [#159](https://github.com/jmservera/ama/issues/159) | Case conversation panel, `web:chat-widget.js` | [Resident chat learning record](./resident-chat-learning-record.md#what-is-saved) | No written reply, abstention and failure task flow | [Content standard chat and alert-panel audit](./content-standard.md#chat-and-alert-panel-audit-extension-2026-10-18-153); No wireframe | `src/api/tests/test_chat_panel.py::PanelTests::test_answer_is_cited_labelled_and_stored_with_evidence` | Conversation recovery flow, wireframe, named review |
| [#215](https://github.com/jmservera/ama/issues/215) | Regulatory alert panel and home chat, `web:chat-widget.js` | [Regulatory UX acceptance protocol, role scripts](./regulatory-ux-acceptance-protocol.md#assistive-technology-and-keyboard-script-by-role) | [Comprehension task cards](./regulatory-ux-acceptance-protocol.md#comprehension-task-cards-and-frozen-answer-key) | [Regulatory UX acceptance protocol](./regulatory-ux-acceptance-protocol.md#purpose-and-status); No wireframe | `src/api/tests/test_home_chat_regulatory_keyboard_provenance.py` | Role and no-source state flows, staff comprehension evidence |

## What this matrix does and does not show

* Every registered role screen has a row, a journey section, a test and a named
  gap. Only the programme queue and the contractor job pack have a written
  design artefact beyond a delivery record, and both are proposed, not approved.
* Twelve screens have no standalone wireframe. Writing wireframes, task flows
  and named reviews is open design work for each screen, owned by the role
  design reviewers; it is not done by this page.
* `src/api/tests/test_screen_design_traceability.py` fails when a screen, a
  link, an anchor, a test or a gap cell is missing, or when a row claims human
  acceptance. It checks that references exist, nothing more.
* Criterion 1 of #156 stays unticked until each screen has a current design
  artefact and the evidence in the gap column.
