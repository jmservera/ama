---
title: Issue 116 live demo research
ms.date: 2026-11-18
---

## Disposition

Research disposition: executed. Planning Readiness: Ready.

## Task

Issue #116. Four unticked criteria: (1) reason roles confirmed (OD-14, OD-19); (2) allowlists at every provider boundary; (3) output, citation, error, review-record and export recheck; (4) document AI derivative or necessity exception. Docs and evidence only.

## Findings

* Prior closure comments (2026-11-05, 2026-11-17) leave all four unproved; offline provider spies (#1466) are valid within scope.
* Source map: `projection.DEFAULT_REASON_ROLES` (three roles, `ZF_REASON_ROLES` override), `Store.ai_run` (unknown task raises before the provider), `ai_tasks.run_document` and `data_protection.document_model_hold`.
* Live: one employee role only (Retrofit Programme Manager); the demo has no uploaded documents; the Playwright request context gets an Easy Auth 403 on POST, so in-page fetch is needed.
* The deployed app sets no `ZF_REASON_ROLES`; the default applies.

## Evidence

Full record: `docs/reference/research/issue-116-live-demo-evidence-2026-11-18.md`; files under `.copilot-tracking/evidence/2026-11-18/issue-116-live/`.

## Planning Readiness

Ready: no further investigation required.
