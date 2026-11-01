# Plan: issue 164 chat registration and enablement gates (2026-11-01)

Research: ../../research/2026-11-01/issue-164-chat-registration-research.md

* [x] Phase 1: add `chat-case-conversation` entry to `ai_registry.tasks()` (kind "chat", enabled false, reviewer function, thresholds unapproved); test in core.
* [x] Phase 2: `enablement_decision` consumes the registry entry and emits per-category gate results; keep disabled and never pass; test in agents.
* [x] Phase 3: ruff check/format, mypy for touched projects, unit tests; commit; push; PR with Refs.

## Critique (single pass, direct dispositions)

* Risk: adding a task shifts registry counts/hash in other tests. Disposition: run core and api registry tests; adjust only direct count assertions.
* Risk: implying approval. Disposition: approval_state stays "unapproved", individual "unknown", `authorizes_live` stays false; test asserts it.
* Verdict: proceed.
