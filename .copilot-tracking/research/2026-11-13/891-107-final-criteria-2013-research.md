---
title: Research for the final unticked criteria of #891 (criterion 2) and #107 (criterion 7)
description: Source audit of live-chat guardrails under the demo switch and of per-assistant usage attribution
ms.date: 2026-11-13
---

## Scope and disposition

* Task: `891-107-final-criteria-2013`; branch `feat/demo-891-107-closure-verify-2013` at `origin/main` `2489d839e9a978330597563561929086ac190c47`.
* Research disposition: `executed`. Planning Readiness: `Ready`.
* Issue bodies read with `gh issue view`. #891 has one unticked criterion (2). #107 has one unticked criterion in the Tokenomics block (7, "Usage per assistant and per accepted proposal ..."); other unticked #107 items (release admission, serving-version attestation, SQL race, delivered-build evidence) are out of scope and stay unticked.

## #891 criterion 2: audit under `ZF_CHAT_DEMO_ACTIVATION=approved-2026-11-03`

The live path is `ChatPanel._ask` (`src/core/src/zava_forward/core/chat_panel.py`) then `ChatModel.__call__` (`src/agents/.../chat.py`) then `server.chat_admission` then `Ai.evidence` / `Ai._request` (`core/ai.py`) then the consumption ledger (`core/ai_consumption.py`). The demo switch changes only `ai_registry.authorizes_live` and seeds a synthetic one-day authority in `core/chat_demo_meter.py`.

| Sub-clause | Where it is enforced | Existing coverage | Gap |
| --- | --- | --- | --- |
| (a) per-call gate | `role_limits`, `over_limit` (thread turns, `calls_per_request`), authority `max_calls=1`, `max_depth=1`, `ChatModel` pre and post `admission()` | `test_continuity.ChatDemoMeterOnSqlStore` (second call held), `test_role_with_no_model_calls...` with admission patched out | No single end-to-end test with the demo switch and real admission and ledger |
| (b) token and cost admission | `Ai._request` calls `consumption.reserve` before `dispatch_check` and `urlopen`; synthetic price is admitted only for the chat task | `test_ai_consumption.test_token_and_money_limits_exact_boundary` (ledger only) | No test of an exhausted demo token or money budget stopping the chat before dispatch |
| (c) privacy refs and personal data | `ChatPrivacy._require` before any message is stored; `redact` masks personal data before the prompt | `test_demo_switch_keeps_suspension_privacy_refs_and_retention_gates` (admission wrapped, provider faked) | Provider request bytes never inspected for personal data under the switch |
| (d) retention | `ChatPrivacy.decision` retention text, `purge_retention`, `memory_used: False` in `/api/chat/status` | status assertions only | No test that the switch leaves retention unset and that nothing is purged or extended |
| (e) refusals | `out_of_scope`, `ACTION_CLAIM`, `unsupported_claims`, memory never in `sources` | scattered, mostly with a faked admission | Not exercised together with the demo switch and real dispatch |

Finding: no source defect. Every guardrail is in force; the gap is the absence of one unmistakable end-to-end proof with real admission, real SQL ledger and a faked HTTP transport only.

## #107 criterion 7: audit of usage attribution

* Registered assistant IDs (`core/assistants.REGISTRY`): `stock-prioritisation`, `assessment-preparation`, `funding-evidence`, `works-resident-coordination`, `quality-evidence`. The names `briefing_summary`, `resident_communication_draft`, `grant_evidence_assembly`, `proactive_stalled_case_scan` and `proactive_missing_evidence_scan` do not exist in code. Each registered assistant has a reactive and a proactive (`mode="proactive"`, purpose principal) trigger, so reactive and proactive are modes, not separate IDs.
* Usage envelope: `Ai._request` returns `meter_id`, `meter_root`, `usage` (tokens, cached tokens). Ledger events (`EVENT_FIELDS`): `reserved` (capability, root, retry, model), `completed` (tokens, charge, outcome, held), `output` (root, output, eligible), `review` (action). All fields are opaque hashes, closed identifiers or numbers.
* `Consumption.report` returns `by_capability` (`capability_usage`): calls, proposals, known-token proposals, total tokens, accepted proposals and `tokens_per_accepted_proposal`; cohort `accepted_proposals`, `projected_token_charge` and `cost_per_accepted_proposal` (billing joined).
* Existing tests: `test_ai_consumption.test_report_attributes_usage_per_assistant_and_accepted_proposal` (two synthetic capabilities, hand-built contexts); `test_ai_consumption_api.test_assistant_thread_preserves_usage_metadata_and_review_join` (one assistant, real service, content canaries). No test drives all five registered assistants through `invoke`, `execute`, verify and review, reconciles per-assistant usage and per-call charge from raw ledger events, and scans ledger, report, log and task-event telemetry for sentinel case text, resident name and address.

Finding: no source defect. `by_capability` carries tokens per assistant and per accepted proposal; charge per call is in `completed.charge` joined by reserved id and root. The gap is end-to-end proof across all five assistants.

## Approach decided

* Tests only, no source change. #891: new class `DemoActivationGuardrailPersistenceTests` in `src/api/tests/test_chat_panel.py` on a SQLite `SqlStore` with a real `Ai`, ledger and `chat_admission`, patching only `urllib.request.urlopen`. #107: new test in `src/api/tests/test_ai_consumption_api.py` on the existing `ConsumptionApi` fixture.
* Evidence boundary: constructed fixtures and a fake transport. No real AI, Azure, Legal, DPO or human acceptance is claimed; the demo remains a disclaimer-based decision.
* Validation tier: focused (tests-only, no workflow, dependency, SQL schema or security-control change); hosted CI and independent exact-head review remain outstanding and are not claimed.
