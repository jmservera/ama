# Plan: 157 C4 status depth and memory caps (1953)

1. core `chat_panel.py`: add `AGENT_DEPTH = 1`, `MEMORY_CAPS` (max_items from `chat_privacy.MEMORY_LIMIT`, max_item_chars from `MEMORY_MAX`, prompt_injection False), `CALLS_PER_REQUEST_NOTE`; add `agent_depth`/`memory_caps` to `role_limits` outputs? No: add to a shared `status_limits()` helper used by server.
2. `server.py` status `limits`: use helper; add `agent_depth`, `memory_caps`, `calls_per_request_basis` ("cap; dispatch count assumed one when provider record absent").
3. `chat.js` limitsNote: show calls_per_request cap, agent depth, memory not used; plain language.
4. Tests (api `test_chat_panel.py`): Application Administrator 403 + zero model calls; agent_depth==1 and memory_caps; fallback after THREAD_LIMIT_REACHED then case read (GET /api/cases/ZF-1) 200 unchanged.
5. Run core/api chat tests, widget focus, content standard, ruff, mypy.
Tier: Focused (no gate/security change).
