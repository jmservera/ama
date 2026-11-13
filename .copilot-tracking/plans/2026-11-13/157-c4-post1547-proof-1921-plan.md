# Plan: #157 Criterion 4 post-#1547 proof (157-c4-post1547-proof-1921)

Tier: Focused (tracking-only, no `src/` or `docs/` change).

1. Run `test_chat_panel` (core, api) and `test_chat_widget_focus` in `/tmp/venv-157c4-1921` (pip install of core, agents, api).
2. Map each clause to source and the asserting test; classify `PROVEN` or `NOT FULLY PROVEN` strictly (a clause is PROVEN only when source enforces it, status or receipt reports it, and a passing test asserts it).
3. Write the proof table to the changes file, with gaps and follow-ups.
4. Independent `code-review`, then clean local commit; remove only `/tmp/venv-157c4-1921`.

Critique amendments (applied directly, see critique file): a clause is PROVEN only with enforcement, pre-activation reporting (status endpoint or widget, not a receipt) and a passing asserting test; trace the adapter for provider calls and retries; qualify roles without a test; add an agent-depth row for AC-103; separate fallback message from workflow continuation.
