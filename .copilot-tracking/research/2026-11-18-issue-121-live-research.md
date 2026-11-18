---
title: Issue 121 live research (data protection, retention, rights)
ms.date: 2026-11-18
---

## Opening

Task issue-121-live. Demo only, desktop; live Azure authorised in rg ama; FOCUSED tier; no src change planned.
Unticked criteria: 1 (DH-006 no resident personal data to a model) and RAI criteria R1 to R7.
Research disposition: executed. Planning Readiness: Ready.

## Findings

* Live `/api/data-protection` (200) lists 8 classes; source `register_report` lists 10 and adds `subject_populations`, `hosting_region_vs_inference_residency`, `whole_system_coverage`, `future_real_resident` and `provider_retained_copy`. The deployed image (digest prefix 5368f4e4) predates those fields. Adverse; kept.
* Every actual class in the live register has missing approvals; `dpo_reviewed` is false; `ZF_DATA_PROCESSING` is not set, so the code default `constructed` applies.
* Model deployment `standard` is `gpt-4.1-nano` on `aif-cutover-test-rzsrg` with SKU GlobalStandard; the app runs in uksouth.
* Retention facts: Log Analytics and App Insights 90 days, SQL PITR 14 days, no SQL long-term retention, chat 30 days.
* Offline: core 52 tests OK; api test_document_controls 18 tests OK.
* Not run: real AI call, document upload, actual-mode flip (state or provider effects; the brief forbids real-AI actions).

Evidence: `.copilot-tracking/evidence/2026-11-18/issue-121-live/`.
