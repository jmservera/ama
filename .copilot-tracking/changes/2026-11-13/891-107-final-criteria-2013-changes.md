---
title: Changes for the final unticked criteria of #891 and #107
description: Tests-only increment proving #891 criterion 2 and #107 criterion 7
ms.date: 2026-11-13
---

## Summary

Tests only. The audit found no source defect, so no file under `src/*/src/` changed. Plan: [plan](../../plans/2026-11-13/891-107-final-criteria-2013-plan.md).

## Changes

| File | Change |
| --- | --- |
| `src/api/tests/test_chat_panel.py` | New `DemoActivationGuardrailPersistenceTests` (8 tests) running the real `ChatPanel` + `ChatModel` + SQL ledger with `ZF_CHAT_DEMO_ACTIVATION=approved-2026-11-03` and a fake transport. Covers (a) per-call gate, (b) call, token and money admission before dispatch, (c) privacy refs and personal-data safeguards, (d) retention, (e) refusals and citation withholding. Imports grouped by ruff. |
| `src/api/tests/test_ai_consumption_api.py` | New `test_usage_per_assistant_and_accepted_proposal_is_attributable_and_content_free`: all five registered assistants reactive, four proactive, distinct usage each, per-assistant and per-accepted-proposal tokens and charge recomputed from raw ledger events and matched to `by_capability` and the cohort report; sentinel address, resident name and case text absent from ledger, report and captured logs, with a positive control on the provider request. |

## Divergences

* The suggested IDs `briefing_summary`, `resident_communication_draft`, `grant_evidence_assembly`, `proactive_stalled_case_scan` and `proactive_missing_evidence_scan` are not registered. The registry holds `stock-prioritisation`, `assessment-preparation`, `funding-evidence`, `works-resident-coordination` and `quality-evidence`; reactive and proactive are modes. Quality-evidence is reactive only under the demo scope.
* Test (b) is three tests (call, token, money) because the authority is immutable once seeded.
* Test (c) narrows "no PII" to the documented allowlist and redaction path.

## Validation (focused tier, local only)

* `test_chat_panel*`: core 53, api 69 (1 skipped) pass; agents has no matching tests.
* `test_ai_consumption*`: core 44, api 40 pass; agents has none.
* `test_content_standard`: api 21 pass.
* `ruff check` and `ruff format --check` on `src/core src/agents src/api`: clean. `mypy` in each project: clean.
* Mutation spot-check: a leaked sentinel in the report fails the #107 test. A planned second mutation did not target the right hook and proved nothing; not claimed.
* Not run: hosted CI, independent exact-head review, full local gate.
