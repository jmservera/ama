---
title: Data Protection, Retention and Rights Live Demo Evidence (Issue 121)
description: Per-criterion record of the eight unticked criteria of issue 121 on the deployed synthetic demo, with what was proven, what was not and why
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: this is the synthetic demo, desktop only. Live
Azure was authorised (resource group `ama`, cap USD 700, no drills, no Key
Vault rotation, no production change). DPO and Legal approval, billing
reconciliation and person-run assistive-technology testing are not needed for
the demo; DPO, Legal and retention-lock items are production-only (#1905 to
#1908). No source file changed. No Azure resource or setting was created or
changed, so nothing needs deleting. Sign-in credentials were read from the
owner's files at run time and never printed; the retained evidence holds no
account name, object id or tenant id (the identity response was reduced to
role and counts before saving; the raw identity response is not retained). The
subscription id in the Azure configuration output was replaced with
`<subscription-id>` in a correction pass.

Target: `ca-cutover-test-demo-api`, Playwright Chromium, 1366 by 900, 2026-11-18
about 10:55 to 11:00 UTC. Evidence files are under
`.copilot-tracking/evidence/2026-11-18/issue-121-live/`.

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Live register | `GET /api/data-protection` returns 200 with 8 classes, `label` `synthetic-demo`, `dpo_reviewed` false, owners "DPO and Legal (named owners not yet recorded)". Every actual class (`staff_identity`, `tenant_identity`, `review_record`, `raw_document`, `prompt_output`, `audit_ledger`, `telemetry`) lists missing approvals; retention reads "Unknown until Legal sets a period" | `probe1.json`, [screenshot](./issue-121-live-data-protection-register-2026-11-18.png) |
| Live register vs source | The deployed register lacks `subject_populations`, `population_separation`, `hosting_region_vs_inference_residency`, `whole_system_coverage` and the classes `future_real_resident` and `provider_retained_copy`, which the source `register_report` returns (10 classes). The deployed image (digest prefix `5368f4e4`) predates them | `probe1.json`; source run offline |
| Processing mode | `ZF_DATA_PROCESSING` is not among the app's environment variables, so the code default `constructed` applies; the demo profile is `demo` | `azure-config-readonly.txt` |
| Model location | Deployment `standard` is `gpt-4.1-nano` on `aif-cutover-test-rzsrg` with SKU GlobalStandard; application hosting is `uksouth` | `azure-config-readonly.txt` |
| Retention settings | Log Analytics and App Insights 90 days; SQL point-in-time restore 14 days; SQL long-term retention weekly, monthly and yearly all `PT0S` and immutability disabled; chat `CHAT_RETENTION_DAYS` 30. These are demo configuration values, not an approved schedule | `azure-config-readonly.txt` |
| Retention queue and audit | `/api/retention` 200 with zero records and the label "synthetic-demo placeholder ... not an approved retention schedule"; `/api/audit-check` reports `intact` true, 1610 entries | `probe1.json` |
| Offline gate tests | core `test_data_protection`, `test_ai_provider_payload_spy`, `test_ai_input_bounds`: 52 tests OK; api `test_document_controls`: 18 tests OK | `offline-core-tests.txt`, `offline-api-tests.txt` |
| Earlier live refusals | An unknown or missing AI task returns 400 before any provider call (see the [#116 record](./issue-116-live-demo-evidence-2026-11-18.md)); not repeated here | cited |

## Acceptance criteria

Status values: proven (for the demo), unproven, deferred (production-only).

| Criterion | Status | Basis and limit |
| --- | --- | --- |
| No resident personal data reaches a model until the transfer position is approved (DH-006) | Proven for the demo by construction and offline gate; live denial unproven | The demo holds constructed resident fixtures only and runs in `constructed` mode; the live register shows no TRANSFER approval for any actual class and `transfer_position_approved` is false in source. The dispatch gate denies actual-class dispatch without references (`model_dispatch`, offline tests). No live refused dispatch was exercised: it needs an actual-mode flip or a real AI call, which the brief forbids. Production transfer approval is #1906 |
| Map staff/tenant identities and review records separately from constructed fixtures and future real residents | Proven offline; live partly | Source `subject_populations` and `population_separation` separate them (test `test_subject_populations_separate_...`). Live shows the staff, tenant, review and fixture classes as separate rows but lacks the population fields and `future_real_resident` (image predates them) |
| Cover inputs, raw bytes, prompts, outputs, citations, reviewer identity, audit, telemetry, tokens, provider processing and retained copies | Proven offline; live partly | Source `whole_system_coverage` lists eight surfaces and the 10 classes (test `test_whole_system_task_manifests_...`). Live register covers raw document, prompt output, audit and telemetry rows but not provider retained copies |
| Every task declares purpose, audience, permitted fields, prohibited content and minimum-necessary rationale | Proven offline; live partly | `test_every_task_declares_purpose_necessity_prohibited` and `test_user_permission_never_establishes_task_necessity_...` pass; a live unknown task is refused (#116 record). The live task manifest was not enumerated |
| DPO/Legal and record owners approve purpose, processor/region/transfer, retention, legal hold, erasure, representative authority and provider-copy treatment | Deferred | Production-only (#1906, owner decision 2026-11-18). Live register records no approvals and names no owners, which is the expected state |
| Permission to upload/store/download does not approve sending intact material to AI | Proven offline; live unproven | `test_resident_ai_consent_blocks_document_model_...` and `test_reviewed_redacted_derivative_...` pass. No uploaded document exists in the demo and an upload would change state, so no live hold was shown |
| Synthetic resident content does not remove actual staff processing from privacy scope; UK hosting does not prove UK inference residency | Proven | Live: `staff_identity` is an actual class in scope while residents are fixtures; the model deployment is GlobalStandard while the app is in `uksouth`. Source states `inference_residency_verified` false and the notes `uk_hosting_does_not_prove_uk_inference_residency`; the live register lacks that block |
| Retention, erasure, audit and restore decisions are explicit and owned; local deletion is not provider erasure | Partly proven; ownership deferred | Explicit for the demo: the live register states retention is unknown until Legal acts; the statement "Local deletion is not provider erasure" is live; PITR, log retention and chat retention values are recorded above; the audit chain is intact. `test_rights_ledger_never_represents_local_deletion_as_provider_erasure` passes. Named owners and approved periods are production-only (#1906 to #1908) |

## Adverse and corrective evidence

* The first live read returned the signed-in identity with a name, object id and
  tenant id; the saved `probe1.json` was reduced to role and counts, and a
  literal scan found no remaining match. The run script prints no credential.
* The deployed register is older than the source register. This is a
  deployed-parity gap, not a defect in the source; redeploying is a change the
  brief excludes.
* Offline test counts are not live results.

## Follow-ups

* Redeploy the demo image so the live register shows populations, residency and
  provider retained copies, then repeat the live register probe.
* Upload one synthetic document, with owner agreement to the state change, and
  record the document model hold.
* Named owners, approved retention periods and the transfer position stay with
  #1906 to #1908.

## Evidence limits

* Raw output not retained: the first identity response (reduced by hand before saving).
* Retained: `offline-core-tests.txt`, `offline-api-tests.txt`, `azure-config-readonly.txt` (subscription id redacted), `probe1.json` and the register screenshot linked above.
* Hosted CI, human approval and independent exact-head review are not observed.
