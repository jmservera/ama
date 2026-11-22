---
title: Data Protection Criteria Live Re-check (Issue 121, 2026-11-22)
description: Re-check of the six unticked criteria of issue 121 on revision 0000053 of the synthetic demo; the deployed-parity gap is closed and no source gap remains
author: AMA programme
ms.date: 2026-11-22
ms.topic: reference
---

## Scope and result

Synthetic demo, desktop only; owner decisions of 2026-11-18 apply (live Azure authorised, resource group `ama`; DPO and Legal approval not needed for the demo). No source file changed and no Azure resource was created or changed, so nothing needs deleting. No legal interpretation is made. Builds on the [2026-11-18](./issue-121-live-data-protection-evidence-2026-11-18.md) and [2026-11-19](./issue-121-live-20261119-2026-11-19.md) notes, which found the deployed image older than the source register. That gap is now closed: `ca-cutover-test-demo-api` runs revision `0000053` (digest prefix `065628c9`) and its register matches source.

Playwright Chromium, 2026-11-22 about 20:35 to 20:45 UTC. Sign-in credentials were read at run time and never printed; the saved `/api/me` response was reduced to its key names. Evidence is under `.copilot-tracking/evidence/2026-11-22/issue-121-live/`.

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Live register | `GET /api/data-protection` 200: `label` `synthetic-demo`, `dpo_reviewed` false, 10 classes (including `future_real_resident` and `provider_retained_copy`), `subject_populations`, `population_separation`, `hosting_region_vs_inference_residency`, `whole_system_coverage`. Every actual class lists missing approvals and retention "Unknown until Legal sets a period" | `probe2.json`, [screenshot](./issue-121-live-data-protection-register-2026-11-22.png) |
| Residency | `application_hosting_region` `uksouth`, `uk_hosting_does_not_prove_uk_inference_residency` true, `inference_residency_verified` false, `transfer_position_approved` false | `probe2.json` |
| Retention queue and audit | `/api/retention` 200, zero records, label "synthetic-demo placeholder ... not an approved retention schedule"; `/api/audit-check` `intact` true, 5715 entries, no digest mismatch | `probe2.json` |
| Staff-role limit | `/api/documents` and `/api/rights` return 403 "Your role does not include this" for the test account | `probe2.json` |
| Document hold | 17 uploaded synthetic documents exist across 40 cases checked. One live `read-doc` on an uploaded `text/plain` document with no derivative returned status 200, `source` `template`, `model` null and the reason "Intact material is not sent; use a reviewed, redacted derivative or a scoped necessity exception. Handle the item manually; a named human decides. No model is used." The call appended AI-record rows to demo state (it was repeated while the probe was being debugged); no resource was created | `probe3.json`, `probe4.json` |
| Unknown task | A live AI POST with an unregistered task returned 400 "Unknown request." before any provider call | `probe5.json` |
| Retention settings (read-only) | Log Analytics 90 days; SQL point-in-time restore 14 days; SQL long-term retention weekly, monthly and yearly `PT0S`; `CHAT_RETENTION_DAYS` 30; `ZF_DATA_PROCESSING` unset so the code default `constructed` applies; model account in `uksouth`. These are demo configuration values, not an approved schedule | `azure-config-readonly.txt` |
| Offline tests | core `test_data_protection`, `test_ai_provider_payload_spy`, `test_ai_input_bounds`: 56 tests OK; api `test_document_controls`: 19 tests OK | `offline-core-tests.txt`, `offline-api-tests.txt` |

## Criteria

Status values: proven (for the demo), unproven, with the basis.

| Criterion | Status | Basis and limit |
| --- | --- | --- |
| Map staff/tenant identities and review records separately from fixtures and future residents | Proven | Live `subject_populations` and `population_separation` separate `fixture_resident`, staff, tenant, review and `future_real_resident` |
| Cover inputs, raw bytes, prompts, outputs, citations, reviewer identity, audit, telemetry, tokens, provider processing, retained copies | Proven | Live `whole_system_coverage` lists eight surfaces; `provider_retained_copy` class present; offline tests pass |
| Every task declares purpose, audience, fields, prohibited content and necessity | Proven offline; live partly | Offline manifest tests pass; live unknown task refused. The live manifest cannot be enumerated through any endpoint, so it is not shown live |
| DPO/Legal and record owners approve purpose, processor, transfer, retention, hold, erasure, representative authority, provider copies | Unproven | Production-only (#1906, owner decision 2026-11-18). Live register records no approvals and no named owners, the expected state |
| Upload/store/download permission does not approve sending intact material to AI | Proven | Live hold above, no model call; offline tests |
| Retention, erasure, audit and restore decisions explicit and owned; local deletion is not provider erasure | Explicit proven; owners unproven | Live statement "Local deletion is not provider erasure", retention values above, audit chain intact. Named owners and approved periods are production-only (#1906 to #1908) |

## Follow-ups

* Names, approved retention periods and the transfer position stay with #1906 to #1908.
* Closing the issue is for the owner; criteria 4 and the owner half of the last criterion cannot be proven in the demo.

## Evidence limits

* Hosted CI, human approval and independent exact-head review are not observed.
* The raw `/api/me` identity response is not retained.
* Offline test counts are not live results.
