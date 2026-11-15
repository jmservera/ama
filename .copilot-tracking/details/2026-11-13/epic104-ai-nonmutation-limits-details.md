# Phase details: Epic #104 criteria 3 and 5

Plan: `.copilot-tracking/plans/2026-11-13/epic104-ai-nonmutation-limits-plan.md`.

## Phase 1: registry guard and five-assistant non-mutation

* Pin the 13 registered capabilities; fail when the registry gains or loses one without the table changing.
* Assert unapproved state, no live authority (with and without the demo env), disabled chat and concern pack.
* Run all five assistants through `AgentWorker.handle` with hostile outputs; assert unapproved envelope, rejected extra keys, unchanged snapshot, single provider call.
* AST guard: `dispatch.py` and `chat.py` import no store or controlled-record module.

## Phase 2: ranking, human route, chat, pack, held-out

* Real `Store` through the `ai_eval` harness: reordered AI output leaves `_ranking()` and `cases` unchanged; recommendation stays `Proposed`; another user cannot resolve; owner accept leaves ranking unchanged.
* `ChatPanel.ask_unstored` refuses action asks without a model and without changing the store.
* `ChatModel` refuses without admission; `chat_eval.enablement_decision` never enables.
* Aftercare pack: template-first, unapproved, only the owner reviews, concern unchanged.

## Phase 3: NFR-012

* `Consumption` over `DemoPort` for every registered capability id: no authority, expired authority, live synthetic price, call, token and money budget limits hold with a `workflow-only` alert naming the owner.
* `authorize` refuses unbounded or missing limits.
* `assistants.Limits` refuses each missing or unbounded setting.
* `chat_eval.call_authorization` and `heldout_batch.run_batch` refuse missing limits with no provider call.

## Phase 4: validation

* `python -m unittest` for the new module, then `src/agents` and relevant `src/core` tests, `ruff check`, `ruff format --check`, `mypy` in `src/agents`.
* Remove `/tmp/venv-104-2244`; commit with trailer; `git status --porcelain` empty.
