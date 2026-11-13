---
title: Issue 157 per-role chat limits research
ms.date: 2026-11-13
---

## Scope

Epic #157 Criterion 4 (BRD AC-103): chat consumption bounded and reported, including per-role limits and thread context, with workflow-only fallback.

## Evidence

* `chat_panel.py` has MAX_INPUT_CHARS (16000), MAX_HISTORY_CHARS (4000), MAX_QUESTION_CHARS (1000) and a receipt with `model_calls`, `context_limit_chars`, `history_limit_chars`, `memory_used`. No per-role bound, no per-thread turn bound, and the receipt reports limits only, not usage.
* `server.py` `/api/chat/status` returns `limits` (calls_per_turn, retries, output_tokens, context_chars, history_chars, memory_used) with no role view.
* `chat_isolation.current_user` refuses roles not in `projection.STAFF_ROLES` (Contractor, Application Administrator get 403), so their model calls are already 0 but not reported.
* `chat.js` `limitsNote` renders the limits sentence from status.
* Tests: `src/api/tests/test_chat_panel.py` (status, receipt, fallback tests).

## Planning readiness

Ready. Gap: explicit `role_limits`, per-thread turn bound with fallback, usage reporting in receipt.
