---
applyTo: ".copilot-tracking/changes/2026-11-13/432-chat-failure-meter-1315-changes.md"
---
# Plan: 432 chat failure meter forwarding

* [ ] Phase 1: RED test in `src/agents/tests/test_chat_model.py` (post-dispatch failures carry ids; pre-dispatch denials carry None).
* [ ] Phase 2: Edit `src/agents/src/zava_forward/agents/chat.py` to attach `meter_id`/`meter_root` on every post-dispatch `ModelUnavailable`.
* [ ] Phase 3: Focused validation (agents unittest, test_ai_consumption, ruff, mypy), independent review, commit.
