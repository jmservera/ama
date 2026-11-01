# Changes: issue 164 chat registration and enablement gates (2026-11-01)

Plan: ../../plans/2026-11-01/issue-164-chat-registration-plan.md

* `src/core/src/zava_forward/core/ai_registry.py`: registered `chat-case-conversation` (kind chat, enabled false, accountable function Retrofit Programme Manager, individual unknown, thresholds proposed and unapproved, required enablement evidence). `authorizes_live` stays false.
* `src/agents/src/zava_forward/agents/chat_eval.py`: `gate_results` per-category (prompt-injection, memory-poisoning, permission, out-of-scope); `enablement_decision` binds to the registry entry, fails on any failing gate, state always disabled.
* `src/agents/tests/test_chat_eval.py`: three tests (registration, gates, failing gate).

Validation: agents chat_eval 27 tests OK; agents suite 104 run, 2 pre-existing import errors (test_chat_model, test_regulatory_gates under discover, same on base); core suite 1689 OK; api test_ai_tasks 66 OK; ruff check and format clean on touched agents files (ai_registry.py format-unclean on base, untouched style); mypy agents clean.
No deviations. No actual model calls, approvals or spend.
