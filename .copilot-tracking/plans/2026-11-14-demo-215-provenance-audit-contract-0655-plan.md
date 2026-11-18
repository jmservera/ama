---
title: "Plan: #215 provenance and audit contract test"
ms.date: 2026-11-14
---

* [x] Phase 1: remove three `unused-ignore` comments and fix the bare `test_role_matrix` import for the focused command.
* [x] Phase 2: add `src/api/tests/test_alert_chat_provenance_audit_contract_215.py`.
* [x] Phase 3: run the three focused validation commands and one frozen commit (`Refs #215`).

Details: [details](../details/2026-11-14-demo-215-provenance-audit-contract-0655-details.md)

## Critique (executed once)

Verdict: proceed. The critique pointed out that asserting a model name would be brittle; the test asserts `reply["model"] != "workflow-only"` and equality with the stored message instead. Held-turn assertions avoid claiming a `workflow-only` model because the provider model is recorded when it was called but produced no answer. Compatible findings applied directly.

## Validation tier

Focused (test-only change, no gate semantics, dependencies, workflows or deployment touched).
