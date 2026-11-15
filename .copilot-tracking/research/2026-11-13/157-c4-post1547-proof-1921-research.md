# Research: #157 Criterion 4 proof after PR #1547 (157-c4-post1547-proof-1921)

Research disposition: executed (source reading at origin/main e3e5f60e3, which contains #1547 as ecdd707c4). Planning Readiness: Ready.

Criterion 4 text: "Chat consumption is bounded and reported before activation: calls per request, context size per thread, memory use and per-role limits, with a fallback to the workflow-only path when a limit is reached (BRD AC-103)".

## Findings

* `chat_panel.py`: `MAX_INPUT_CHARS=16000`, `MAX_HISTORY_CHARS=4000`, `MAX_QUESTION_CHARS=1000`, `MAX_THREAD_TURNS=30`, `OUTPUT_TOKENS=600`; `role_limits(role)` gives `access`, `calls_per_request` (1 or 0), `turns_per_thread`, `output_tokens`; `all_role_limits()` covers seven chat roles and two no-chat roles.
* `_ask`: `over_limit` (role with zero calls or `prior_turns >= turns_per_thread`) returns `fallback` with `THREAD_LIMIT_REACHED` and no model call; question over 1000 chars and prompt over `MAX_INPUT_CHARS` return `fallback` with `LIMIT_REACHED`.
* `server.py` `GET /api/chat/status` reports `limits` (calls_per_turn, calls_per_request, retries, output_tokens, turns_per_thread, context_chars, history_chars, `memory_used: False`), `role_limits` and `your_role_limits`, beside `activation` (`demo-only` or `disabled`).
* Receipt reports `calls_per_request`, `role_limits`, `thread_turns_used`, `thread_turn_limit`, `context_chars`, `history_chars`, `memory_used`.
* Memory: `chat_panel._ask` does not call `ChatIsolation.build_prompt`, so memory is never in the prompt; `memory_used=False` is a constant, not a measured value. Memory caps (`MEMORY_LIMIT=50` items, `MEMORY_MAX=1000` chars) live in `chat_privacy.py` and are not in the chat status or receipt. No bound exists for process or host memory.
* Per-role limits are static code constants: all chat roles share identical values; the "per-role" differentiation is chat versus no-chat.
* "Context size per thread" is bounded as per-prompt characters plus a turn count; no cumulative per-thread character or token cap exists.
* Fallback: result carries `workflow_only: True` (API test) and the widget states the workflow-only continuation.

## Open question

Whether the executed tests pass in a fresh venv and whether each clause is asserted by a test. Resolved by running them after critique.

## Boundaries

Offline; no `.env`, private data, cloud or model calls; tracking-only commit (no `src/` or `docs/` edits).
